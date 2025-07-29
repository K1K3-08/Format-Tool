#SAE_autoconverter
#by kike
import pandas as pd
import xlsxwriter as xw
from IPython.display import display
import os
import sys
import pickle

def run(dir):
    """    This function processes an Excel file, cleans it, and writes the cleaned data to a new Excel file.
    :param dir: The directory of the input Excel file.
    :return: A list containing the path to the output Excel file and the original directory name.
    """
    # Determine the directory based on whether the script is frozen or not
    
    if getattr(sys, 'frozen', False):
        dirname = os.path.join(os.path.abspath(os.path.dirname(__file__)))
        temp_dir = os.path.join(os.environ['LOCALAPPDATA'], 'Format-Tool')
        os.makedirs(temp_dir, exist_ok=True)
    else:
        dirname = os.path.join(os.path.abspath(os.path.dirname(__file__)),'..')
        temp_dir = dirname

    itr =0

    df = pd.read_excel(dir)
    cleandf = df.dropna(how='all').dropna(axis='columns',how='all').dropna(subset=df.columns[0])

    headInd = cleandf[cleandf[cleandf.columns[cleandf.isin(['LINEA']).any(bool_only=True)][0]]=='LINEA'].index[0]
    cleanerdf = cleandf.rename(columns=cleandf.loc[headInd]).loc[(headInd+1):]
    cleanerdf=cleanerdf.dropna(subset='ITEM')
    cleanerdf = cleanerdf.set_index('LINEA')

    for i in cleanerdf['COMPRA'].values:
        itr+=1
        cleanerdf.at[itr,'COMPRA']=i[1:]

    cleanerdf.rename(columns={cleanerdf.columns[1]:'PRODUCTO','COMPRA':'EMPAQUE', 'BARRAS':'CODIGO DEL PRODUCTO', 'CANT.':'CAJA'},inplace=True)
    fdf = cleanerdf[['PRODUCTO','EMPAQUE','ITEM','CODIGO DEL PRODUCTO','CAJA']].copy()

    blist = []

    itr = 0
    for i in fdf['EMPAQUE']:
        itr+=1
        blist.append(int(fdf.at[itr,'CAJA'])*int(i))

    BQT = pd.Series(blist,index=fdf.index)
    fdf.insert(loc=4, column='BQT', value=BQT)
    fdf.insert(len(fdf.columns), column='BQT.', value='')
    fdf.insert(len(fdf.columns), column='CAJA.', value='')  
    fdf.insert(len(fdf.columns), column='OBSERVACIONES', value='')
    fdf.insert(0, column='Tipo', value='flor')

    dict = {}
    if os.path.exists(os.path.join(temp_dir, "obsdict.pkl")):
        with open(os.path.join(temp_dir, "obsdict.pkl"), 'rb') as f:
            dict = pickle.load(f)
    for i in fdf.index:
        if fdf.at[i,'CODIGO DEL PRODUCTO'] in dict:
            fdf.at[i,'Tipo'] = dict[fdf.at[i,'CODIGO DEL PRODUCTO']][0]
            fdf.at[i,'OBSERVACIONES'] = dict[fdf.at[i,'CODIGO DEL PRODUCTO']][1]
        else:
            fdf.at[i,'Tipo'] = 'flor'
            fdf.at[i,'OBSERVACIONES'] = ''
        

    print("fdf:", fdf)

    return fdf

    
    