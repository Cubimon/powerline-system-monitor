import subprocess
import re

def usage(pl, gpu=0, nvformat="csv,noheader", queries=[], format="{0:.1f}"):
    data = []
    for query in queries:
        data.append(single_query(gpu, nvformat, query))
    return [{
        "contents": format.format(*data),
        "highlight_groups": [query]
            }]

def single_query(gpu, nvformat, query):
    valueStr = subprocess.Popen(["nvidia-smi", "-i", str(gpu), "--format={}".format(nvformat), "--query-gpu={}".format(query)], stdout=subprocess.PIPE).stdout.read().strip().decode("utf-8")
    reResult = value = re.findall("\d+\.\d*|\d*.\d+|\d+", valueStr)
    if len(reResult) < 1:
        return -1
    return float(reResult[0])
