"""
Application stub
"""

import shutil
import SMART 
import SORIANA
import os
import sys
import df2xl
import pandas as pd
import obsdict
import SAE
import WALMARTCS



def initialize():
    # perform heavy stuff here
    return True


def do_stuff(f,t):
    # do whatever you need to do
    global formato
    global convert_to
    formato = f
    convert_to = t
    if formato == 'SMART':
        out = SMART.run(directory)
        response = ['Conversion exitosa', out]
    elif formato == 'SORIANA':
        out = SORIANA.run('cSORIANA',directory)
        response = ['Conversion exitosa', out]
    return response
def S1():
    out=SORIANA.run('fix_template',directory)
    df2xl.run(out, 'fix_template')
    return
def S2():
    out=SORIANA.run('wkly_dist',directory)
    df2xl.run(out, 'wkly_dist')
    return

def to_excel(df):
    obsdict.obsdict(df)
    out =  df2xl.run(df, formato)
    return out

def SMART_SAE():
    df = SMART.run(directory, case=1)
    out = SAE.convert_to_SAE(case=1, df=df)
    return out

def SORIANA_SAE():
    df=SORIANA.run('SAE',directory)
    out = SAE.convert_to_SAE(case=3,df=df)
    return out

def WALMART_SAE(save_folder):
    WALMARTCS.run(directory,save_folder)



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

def replace_dummy(dest,data):
    dirname = os.path.dirname(__file__)
    temp_dir = os.path.join(os.environ['LOCALAPPDATA'], 'Format-Tool')
    # Replace the dummy file with the actual file
    if getattr(sys, 'frozen', False):
        shutil.copyfile(os.path.join(temp_dir, data), dest)

    else:
        shutil.copyfile(os.path.join(dirname, "..\\"+data), dest)


    