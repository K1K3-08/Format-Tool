"""
Application stub
"""

import shutil
import SMART as SMART
import os
import sys


def initialize():
    # perform heavy stuff here
    return True


def do_stuff():
    # do whatever you need to do
    out = SMART.run(directory)
    response = ['Conversion exitosa', out[0], out[1]]
    return response

def load_dir(dir):
    # Load the directory
    global directory
    directory =  dir
    return

def replace_dummy(dest):
    dirname = os.path.dirname(__file__)
    temp_dir = os.path.join(os.environ['LOCALAPPDATA'], 'Format-Tool')
    # Replace the dummy file with the actual file
    if getattr(sys, 'frozen', False):
        shutil.copyfile(os.path.join(temp_dir, "data.xlsx"), dest)

    else:
        shutil.copyfile(os.path.join(dirname, "..\\data.xlsx"), dest)


    