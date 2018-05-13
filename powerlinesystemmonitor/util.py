import subprocess

def noop(pl, content="", highlight_groups=["noop"]):
    return [{
        "contents": content,
        "highlight_groups": highlight_groups
            }]

def bash(pl, command="", highlight_groups=["bash"]):
    return [{
        "contents": subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).stdout.read().strip().decode("utf-8"),
        "highlight_groups": highlight_groups
            }]
