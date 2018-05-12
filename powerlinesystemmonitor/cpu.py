import psutil

"""
:param pl:
:param format: freq_all_cur, freq_all_min, freq_all_max,      all cores:   current, min, max
               freq_0_cur,   freq_0_min,   freq_0_max,        first core:  current, min, max
               freq_1_cur,   freq_1_min,   freq_1_max         second core: current, min, max
"""
def frequency(pl, format="{freq_all_cur:0.1f}/{freq_all_max:0.1f} GHz", factor=10**-3):
    data = {}
    append_frequency(data, factor)

    return [{
        "contents": format.format(**data),
        "highlight_groups": ["cpu_frequency"]
            }]

"""
:param format: util_all,       all cores
               util_0,         first core
               util_1,         second core
"""
def utilization(pl, format="{util_all} %"):
    data = {}
    append_utilization(data)

    return [{
        "contents": format.format(**data),
        "highlight_groups": ["cpu_utilization"]
            }]

def temperature(pl, label="Package id 0", format="{0:.1f} °C"):
    sensors = psutil.sensors_temperatures()
    for group_name, group in sensors.items():
        for sensor in group:
            if sensor.label == label:
                return [{
                         "contents": format.format(sensor.current),
                         "highlight_groups": ["cpu_temperature"]
                        }]

def append_frequency(data, factor):
    core_data = psutil.cpu_freq()
    data["freq_all_cur"] = core_data.current * factor
    data["freq_all_min"] = core_data.min * factor
    data["freq_all_max"] = core_data.max * factor
    idx = 0
    for core_data in psutil.cpu_freq(True):
        data["freq_{}_cur".format(idx)] = core_data.current * factor
        data["freq_{}_min".format(idx)] = core_data.min * factor
        data["freq_{}_max".format(idx)] = core_data.max * factor
        idx += 1

def append_utilization(data):
    data["util_all"] = psutil.cpu_percent()
    i = 0
    for perc in psutil.cpu_percent(percpu=True):
        data["util_{}".format(i)] = perc
        i += 1

 
