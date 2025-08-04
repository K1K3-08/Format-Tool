import pandas as pd
import sys
import os
import pickle

def obsdict(df):

    dict = {}
    if getattr(sys, 'frozen', False):
        dirname = os.path.join(os.path.abspath(os.path.dirname(__file__)))
        temp_dir = os.path.join(os.environ['LOCALAPPDATA'], 'Format-Tool')
    else:
        dirname = os.path.join(os.path.abspath(os.path.dirname(__file__)),'..')
        temp_dir = dirname

    if os.path.exists(os.path.join(temp_dir, "obsdict.pkl")):
        with open(os.path.join(temp_dir, "obsdict.pkl"), 'rb') as f:
            dict = pickle.load(f)

    for i in df.index:
            dict[df.at[i,'CODIGO DEL PRODUCTO']] = [df.at[i,'Tipo'],df.at[i,'OBSERVACIONES']]

    with open(os.path.join(temp_dir, "obsdict.pkl"), 'wb') as f:
        pickle.dump(dict, f)
        
    return