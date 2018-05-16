from powerline.lib.threaded import KwThreadedSegment
from powerline.segments import with_docstring
from powerline.lib.humanize_bytes import humanize_bytes
import psutil
from time import time

def usage(pl, location="/", format="{0:.1f} G"):
    disk_usage = psutil.disk_usage(location)
    return [{
        "contents": format.format(disk_usage.free / 10**9),
        "highlight_groups": ["disk_usage"]
            }]


class TrafficSegment(KwThreadedSegment):

    prev_counters = None
    prev_time = None

    @staticmethod
    def key(disk="", **kwargs):
        return disk

    def compute_state(self, disk):
        cur_time = time()
        counters = None
        if len(disk) == 0:
            counters = psutil.disk_io_counters()
        else:
            counters = psutil.disk_io_counters(perdisk=True)
        if self.prev_counters is None:
            self.prev_counters = counters
            self.prev_time = cur_time
            return None
        data = {}
        if len(disk) == 0:
            data["read_speed"]  = humanize_bytes((counters.read_bytes - self.prev_counters.read_bytes)   / (cur_time - self.prev_time))
            data["write_speed"] = humanize_bytes((counters.write_bytes - self.prev_counters.write_bytes) / (cur_time - self.prev_time))
        else:
            if disk in counters.keys() and disk in self.prev_counters.keys():
                data["read_speed"]  = humanize_bytes((counters[disk].read_bytes - self.prev_counters[disk].read_bytes)   / (cur_time - self.prev_time))
                data["write_speed"] = humanize_bytes((counters[disk].write_bytes - self.prev_counters[disk].write_bytes) / (cur_time - self.prev_time))
        self.prev_counters = counters
        self.prev_time = cur_time
        return data

    def render_one(self, data, format="{read_speed:>7} {write_speed:>7}", **kwargs):
        if data is None or "read_speed" not in data or "write_speed" not in data:
            return None
        return [{
            "contents": format.format(**data),
            "highlight_groups": ["traffic"]
                }]

traffic = with_docstring(TrafficSegment(),
''' Get hdd traffic

:param disk: partition to measure traffic
:param format: use {read_speed} and {write_speed}
''')

# TODO: implement as segment class
# util_per_partition[partition].read_bytes/write_bytes 
#def traffic(pl, partition="sdb2", format="{0:1.f}"):
#    util_per_partition = disk_io_counters(True)
#    if partition not in util_per_partition:
        
