import psutil

def usage(pl, location="/", format="{0:.1f} G"):
    disk_usage = psutil.disk_usage(location)
    return [{
        "contents": format.format(disk_usage.free / 10**9),
        "highlight_groups": ["disk_usage"]
            }]

# TODO: implement as segment class
# util_per_partition[partition].read_bytes/write_bytes 
#def traffic(pl, partition="sdb2", format="{0:1.f}"):
#    util_per_partition = disk_io_counters(True)
#    if partition not in util_per_partition:
        
