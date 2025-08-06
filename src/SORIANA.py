import pandas as pd 
import os
import sys
import pickle

def run(f,dir):
    if getattr(sys, 'frozen', False):
        dirname = os.path.join(os.path.abspath(os.path.dirname(__file__)))
        temp_dir = os.path.join(os.environ['LOCALAPPDATA'], 'Format-Tool')
        os.makedirs(temp_dir, exist_ok=True)
    else:
        dirname = os.path.join(os.path.abspath(os.path.dirname(__file__)),'..')
        temp_dir = dirname

    def cSoriana():
        xl = pd.ExcelFile(dir)#TODO replace with selected file
        df = xl.parse(xl.sheet_names[0])
        df=df.drop(columns=['Unnamed: 0','Unnamed: 2','Unnamed: 3'])
        df.columns= df.iloc[6]
        ogdf = df.copy()
        df.drop(index=[0,1,2,3,4,5,6], inplace=True)


        outdf = pd.DataFrame(columns=['PRODUCTO','AQUABOX','CODIGO DEL PRODUCTO','BQT','CAJA','CAJA.','BQT.','OBSERVACIONES'])

        df = df.loc[:, ~pd.isnull(df.columns)]

        df=df.dropna(subset=[df.columns[0]], how='any')

        
        for i in df.columns[1:-1:]:
            numeric_mask = pd.to_numeric(df[i], errors='coerce').notnull()
            s =sum(pd.to_numeric(df[i], errors='coerce').dropna())
            if s!=0:

                outdf = outdf._append(
                    {
                        'PRODUCTO':i, 
                        'AQUABOX':ogdf.at[3,i], 
                        'CODIGO DEL PRODUCTO':ogdf.at[5,i], 
                        'BQT':(s*ogdf.at[3,i]),
                        'CAJA':s
                    },
                    ignore_index=True
                )
        
        dict={}
        if os.path.exists(os.path.join(temp_dir, "obsdict.pkl")):
            with open(os.path.join(temp_dir, "obsdict.pkl"), 'rb') as f:
                dict = pickle.load(f)
        for i in outdf.index:
            if str(outdf.at[i,'CODIGO DEL PRODUCTO']) in dict:
                outdf.at[i,'OBSERVACIONES'] = dict[str(outdf.at[i,'CODIGO DEL PRODUCTO'])][1]
            else:
                outdf.at[i,'OBSERVACIONES'] = ''

        outdf.fillna('', inplace=True)
        
        return outdf

    def fix_template():
        xl = pd.ExcelFile(dir)#TODO replace with selected file
        df = xl.parse(xl.sheet_names[0])
        df=df.drop(columns=['Unnamed: 0','Unnamed: 2','Unnamed: 3'])

        df.columns= df.iloc[6]
        ogdf = df.copy()
        
        df.drop(index=[0,1,2,3,4,5,6], inplace=True)


        outdf = pd.DataFrame(columns=['CÓDIGO','MATERIAL(No Modificar)','TEXTO(No Modificar)','CANTIDAD (Kilos ó Piezas)','UMP(No Modificar)','T(No Modificar)','FECHA (DD.MM.AAAA)','PRECIO NETO (Costo)','MONEDA','POR','CPP','GRUPO ART(No Modificar)','CENTRO (Tienda)','PROVEEDOR'])

        df = df.loc[:, ~pd.isnull(df.columns)]

        df=df.dropna(subset=[df.columns[0]], how='any')
        

        for i in df.columns[1:-1:]:
            numeric_mask = pd.to_numeric(df[i], errors='coerce').notnull()
            
            outdf = outdf._append(

                {
                    'CÓDIGO':str(ogdf.at[5,i]), 
                    'MATERIAL(No Modificar)':ogdf.at[4,i], 
                    'TEXTO(No Modificar)':i, 
                    'CANTIDAD (Kilos ó Piezas)':sum(pd.to_numeric(df[i], errors='coerce').dropna()),
                    'PRECIO NETO (Costo)':ogdf.at[2,i],
                    'CENTRO (Tienda)': 5532,
                    'PROVEEDOR': 392381
                },

                ignore_index=True

                )
            outdf.fillna('', inplace=True)
        print("outdf:", outdf.to_string())
        return outdf

    def wkly_dist():
        xl = pd.ExcelFile(dir)#TODO replace with selected file
        df = xl.parse(xl.sheet_names[0])
        df=df.drop(columns=['Unnamed: 0','Unnamed: 2','Unnamed: 3'])
        ogdf = df.copy()

        df.columns= df.iloc[6]
        ogdf = df.copy()
        df.drop(index=[0,1,2,3,4,5,6], inplace=True)


        outdf = pd.DataFrame(columns=['Material','Cantidad','Fecha','Centro','CEDIS'])

        df = df.loc[:, ~pd.isnull(df.columns)]

        df=df.dropna(subset=[df.columns[0]], how='any')

        for i in df.columns[1:-1:]:
            numeric_mask = pd.to_numeric(df[i], errors='coerce').notnull()
            for j in df.index[numeric_mask].tolist():
                outdf = outdf._append({'Material':ogdf.at[4, i], 'Cantidad': df.at[j, i], 'Centro': df.at[j,df.columns[0]]}, ignore_index=True)
                outdf.fillna('', inplace=True)
            
        return outdf
    def SAE():
        xl = pd.ExcelFile(dir)#TODO replace with selected file
        df = xl.parse(xl.sheet_names[0])
        df=df.drop(columns=['Unnamed: 0','Unnamed: 2','Unnamed: 3'])

        df.columns= df.iloc[6]
        ogdf = df.copy()
        
        df.drop(index=[0,1,2,3,4,5,6], inplace=True)


        outdf = pd.DataFrame(columns=['CÓDIGO','CANTIDAD','PRECIO'])

        df = df.loc[:, ~pd.isnull(df.columns)]

        df=df.dropna(subset=[df.columns[0]], how='any')
        

        for i in df.columns[1:-1:]:
            numeric_mask = pd.to_numeric(df[i], errors='coerce').notnull()
            
            outdf = outdf._append(

                {
                    'CÓDIGO':str(ogdf.at[5,i]), 
                    'CANTIDAD':sum(pd.to_numeric(df[i], errors='coerce').dropna()),
                    'PRECIO':ogdf.at[2,i]
                },

                ignore_index=True

                )
            outdf.fillna('', inplace=True)
        print("outdf:", outdf.to_string())
        return outdf


    if f == 'cSORIANA':
        return cSoriana()
    if f == 'fix_template':
        return fix_template()
    if f == 'wkly_dist':
        return wkly_dist()
    if f == 'SAE':
        return SAE()

