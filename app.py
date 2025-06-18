"""
Application stub
"""
import pickle
import shutil
import SMART
import os
import time
import subprocess

def initialize():
    # perform heavy stuff here
    return True


def do_stuff():
    # do whatever you need to do
    out = SMART.run(directory)
    response = ['Conversion exitosa', out[0], out[1]]
    subprocess.run(["attrib","+H","directory.pkl"],check=True)
    return response

def load_dir(dir):
    # Load the directory
    global directory
    directory = dir
    return

def replace_dummy(dest):
    print(dest+ " is the destination file")
    time.sleep(1)  # Wait for the file to be ready
    dirname = os.path.dirname(__file__)
    # Replace the dummy file with the actual file
    shutil.copyfile(os.path.join(dirname, "data.xlsx"), dest)
