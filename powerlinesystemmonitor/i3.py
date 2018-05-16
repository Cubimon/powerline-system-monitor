from powerline.lib.threaded import KwThreadedSegment
from powerline.segments import with_docstring
import i3ipc
from threading import Thread, Lock
from collections import deque

i3conn = i3ipc.Connection()
# mode
global i3mode
i3mode = "default"
mutex = Lock()

# TODO: do as segment class

def mode_change_event(self, e):
    global i3mode
    mutex.acquire()
    i3mode = e.change
    mutex.release()

i3conn.on("mode", mode_change_event)


class WindowNameSegment(KwThreadedSegment):

    pos = 0
    prev_name = ""

    @staticmethod
    def key(max_length=20, **kwargs):
        return max_length

    def compute_state(self, max_length):
        new_name = i3conn.get_tree().find_focused().name
        if new_name is None:
            return None
        if len(new_name) < max_length:
            self.pos = 0
        else:
            self.pos = (self.pos + int(max_length * 0)) % len(new_name)
        if self.prev_name != new_name:
            self.prev_name = new_name
            self.pos = 0
        rotated_name = new_name[self.pos:] + new_name[:self.pos]
        rotated_shortened_name = rotated_name[:max_length]
        return ("{0:^" + str(max_length) + "}").format(rotated_shortened_name)

    def render_one(self, name, **kwargs):
        if name is None:
            return None
        return [{
                "contents": name, 
                "highlight_groups": ["window_name"]
                }]

window_name = with_docstring(WindowNameSegment(),
'''Return name of focused i3 window

:param max_length:
    maximum length of window name

''')

def mode(pl, hidden_modes=[]):
    mutex.acquire()
    mode = i3mode
    mutex.release()
    if mode in hidden_modes:
        return None
    return [{
        "contents": mode,
        "highlight_groups": ["mode"]
            }]

Thread(target=lambda: i3conn.main()).start()

