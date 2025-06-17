"""
Application stub
"""
import pickle
import shutil
import SMART
import os
import time

def initialize():
    # perform heavy stuff here
    return True


def do_stuff():
    # do whatever you need to do
    with open('directory.pkl','rb') as f:
        dir = pickle.load(f)
    out = SMART.run(dir)
    response = ['This is response from Python backend', out[0], out[1]]
    return response

def load_dir(dir):
    # Load the directory
    with open('directory.pkl', 'wb') as f:
        pickle.dump(dir, f)
        return
def replace_dummy(dest):
    print(dest+ " is the destination file")
    time.sleep(1)  # Wait for the file to be ready
    dirname = os.path.dirname(__file__)
    # Replace the dummy file with the actual file
    shutil.copyfile(os.path.join(dirname, "data.xlsx"), dest)
