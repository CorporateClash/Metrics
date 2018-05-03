import os
import sys
import tempfile

fname = tempfile.gettempdir() + os.path.sep + "cache.txt"

def _create():
    if os.path.exists(fname):
        return
    with open(fname, 'a'):
        os.utime(fname, None)

_create()

# Cache: wait for a subsequent run to be executed before changing website status
def present(value):
    with open(fname, "r") as file:
        data = file.readlines()
        return value + "\n" in data

def create(value):
    with open(fname, "a") as file:
        file.write(value + "\n")

def delete(value):
    with open(fname, "r+") as file:
        data = file.readlines()
        if value + "\n" not in data:
            return
        file.seek(0)
        data.remove(value + "\n")
        file.writelines(data)
        file.truncate()
        file.close()