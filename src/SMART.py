#SAE_autoconverter
#by kike
import pandas as pd
import xlsxwriter as xw
from IPython.display import display
import os

def run(dir):
    dirname = os.path.dirname(__file__)

    writer = pd.ExcelWriter(os.path.join(dirname,"..\\data.xlsx"), engine="xlsxwriter")

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


    print(cleanerdf.to_string())
    print(fdf.to_string())
    fdf.to_excel(writer, sheet_name= 'Sheet1',header= False , index= False, startcol= 1, startrow= 6)
    wkbk = writer.book
    ws1 = writer.sheets['Sheet1']

    #FORMATS

    merge_format = wkbk.add_format(
        {
            "bold": 1,
            "border": 1,
            "align": "center",
            "valign": "vcenter",
            "fg_color": "yellow",
        }
    )

    f1 = wkbk.add_format(
        {
            "bold": 1,
            "align": "center",
            "valign": "vcenter",
            "font_size": 15
        }
    )

    f2 = wkbk.add_format(
        {
            'bold':1,
            'font_size':15
        }
    )

    f3 = wkbk.add_format(
        {
            'bold': 1,
            'align': 'center',
            'font_size': 20,
            'font_color': 'blue'

        }
    )

    f4 = wkbk.add_format(
        {
            'bold': 1,
            'align': 'right',
            'font_size':15
        }
    )

    f5 = wkbk.add_format(
        {
            'bottom': 5,
            'bold':1
        }
    )

    f6 = wkbk.add_format(
        {
            'border': 6,
            'bold':1,
            'font_size':16,
            'align': 'center',
            'fg_color':'yellow'
        }
    )

    (max_row, max_col) = fdf.shape

    column_settings = [{"header": column} for column in fdf.columns]
    extra_cols = ['BQT.','CAJA.','OBSERVACIONES']
    extra_cols_settings = [{"header": column} for column in extra_cols]
    merged_cols = column_settings + extra_cols_settings
    ws1.add_table(6, 1, max_row+6, max_col +3, {"columns": merged_cols})

    ws1.set_column(max_col+5,max_col+5, 30)
    ws1.set_column(max_col-1,max_col+2, 15,f1)

    ws1.write_formula(xw.utility.xl_rowcol_to_cell(max_row+6, max_col-1),"{=SUM("+xw.utility.xl_range(7,max_col-1,max_row+5, max_col+1)+")}",f6)
    ws1.write_formula(xw.utility.xl_rowcol_to_cell(max_row+6, max_col),"{=SUM("+xw.utility.xl_range(7,max_col,max_row+5, max_col)+")}",f6)

    ws1.insert_image('A1', os.path.join(dirname,'..\\assets\\FLIX.png'))
    ws1.insert_image('I1', os.path.join(dirname,'..\\assets\\SMART.png'))

    ws1.autofit()

    ws1.merge_range("F6:G6", "CANTIDAD PEDIDA", merge_format)
    ws1.merge_range("H6:I6", "CONFIRMACION EMBALAJE", merge_format)



    ws1.set_column(2,2, 15,f1)


    ws1.write('B5','CLIENTE:',f4)
    ws1.write('C5',' SMART CEDIS CD JUAREZ ',f2 )

    ws1.write('B6', 'FECHA DE EMBARQUE:',f4)
    ws1.write('C6', '',f2)

    ws1.write('D2', 'SOLICITUD DE PEDIDO', f3)
    ws1.write('D3', 'PLANTAS', f3)

    ws1.write(max_row + 8,1,'NO. WET PACK:' ,f4)
    ws1.write(max_row + 9,1,'NO. AQUABOX:' ,f4)
    ws1.write(max_row + 10,1,'NO. AQUAPOLLO:' ,f4)
    ws1.write(max_row + 11,1,'TOTAL DE EMPAQUES:' ,f4)

    ws1.write(max_row + 8,2,'' ,f5)
    ws1.write(max_row + 9,2,'' ,f5)
    ws1.write(max_row + 10,2,'' ,f5)
    ws1.write(max_row + 11,2,'' ,f5)

    ws1.write(max_row+11,4,'ENTREGÒ:',f4)
    ws1.write(max_row+11,5,'',f5)
    ws1.write(max_row+11,6,'',f5)



    writer.close()
    return [(os.path.join(dirname,"..\\data.xlsx")),dir.split('\\')[-1]]  # Return the path to the output file and the original directory name