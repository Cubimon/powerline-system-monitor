import psutil

def usage(pl, format="{0:.1f}/{1:.1f} G"):
    virtual_memory = psutil.virtual_memory()
    return [{
        "contents": format.format(virtual_memory.used / 10**9, virtual_memory.total / 10**9),
        "highlight_groups": ["memory_usage"]
            }]
