import pandas as pd 
import os
import sys
import webview
import shutil
import SAE

def run(dir,save_folder):
    if getattr(sys, 'frozen', False):
        dirname = os.path.join(os.path.abspath(os.path.dirname(__file__)))
        temp_dir = os.path.join(os.environ['LOCALAPPDATA'], 'Format-Tool')
        os.makedirs(temp_dir, exist_ok=True)
    else:
        dirname = os.path.join(os.path.abspath(os.path.dirname(__file__)),'..')
        temp_dir = dirname

    
    xl = pd.ExcelFile(dir)
    for sheet in xl.sheet_names:
        if not sheet.startswith('CONCENTRADO'):
            df = xl.parse(sheet)
            client = df.iloc[1,3]
            df.drop(columns=[df.columns[0],df.columns[1]], inplace=True)
            df=df.dropna(axis='columns', how='all')
            df=df.dropna(axis='rows', how='all')
            
            df=df.rename(columns=df.loc[5])
            df= df.drop(index=[2,5])
            df= df.dropna(subset=[df.columns[0],df.columns[2]], how='any')

            print("df:", df.to_string())
            print(df.columns)
            print("client:", client)
            SAE.convert_to_SAE(case=2,df=df)
            client =str(client)
            print(client.split('(')[0]+'.MOD')
            dest = str(client.split('(')[0]+'.MOD')
            print(save_folder[0])
            if '"' in dest:
                continue
            else:
                shutil.copyfile(
                    os.path.join(temp_dir, "temp.MOD"),
                    os.path.join(save_folder[0], dest)
                )