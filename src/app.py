"""
Application stub
"""

import shutil
import SMART as SMART
import os
import sys
import df2xl


def initialize():
    # perform heavy stuff here
    return True


def do_stuff(f):
    # do whatever you need to do
    global formato
    formato = f
    if formato == 'SMART':
        out = SMART.run(directory)
        response = ['Conversion exitosa', out]
    else:
        return
    return response

def to_excel(df):
    out =  df2xl.run(df, formato)
    return out
    
    


def load_dir(dir):
    # Load the directory
    global directory
    directory =  dir
    return

def get_dir():
    # Get the current directory
    global directory
    d = directory.split('\\')[-1]
    return d

def replace_dummy(dest):
    dirname = os.path.dirname(__file__)
    temp_dir = os.path.join(os.environ['LOCALAPPDATA'], 'Format-Tool')
    # Replace the dummy file with the actual file
    if getattr(sys, 'frozen', False):
        shutil.copyfile(os.path.join(temp_dir, "data.xlsx"), dest)

    else:
        shutil.copyfile(os.path.join(dirname, "..\\data.xlsx"), dest)


    