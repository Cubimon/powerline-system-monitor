from powerline.lib.threaded import ThreadedSegment
import i3ipc
from threading import Thread

i3conn = i3ipc.Connection()
global i3mode
i3mode = "default"

def mode_change_event(self, e):
    global i3mode
    i3mode = e.change

i3conn.on("mode", mode_change_event)

def window_name(pl, max_length=20):
    text = i3conn.get_tree().find_focused().name
    if len(text) > max_length:
        text = text[0:max_length]
    return [{
        "contents": text, 
        "highlight_groups": ["window_name"]
            }]

def mode(pl):
    return [{
        "contents": i3mode,
        "highlight_groups": ["mode"]
            }]

Thread(target=lambda: i3conn.main()).start()

