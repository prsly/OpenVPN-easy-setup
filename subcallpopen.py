import subprocess


def subcall(arg, pipe):
    if pipe == 1:
        return subprocess.call(arg, shell=True, stdout=subprocess.PIPE)
    else:
        return subprocess.call(arg, shell=True)


def subpopen(arg):
    return subprocess.Popen(arg, shell=True, stdout=subprocess.PIPE)
