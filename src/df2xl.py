import os
import pandas as pd
import xlsxwriter as xw
import sys

def run(fdf, format ):
    global temp_dir, dirname
    if getattr(sys, 'frozen', False):
            dirname = os.path.join(os.path.abspath(os.path.dirname(__file__)))
            temp_dir = os.path.join(os.environ['LOCALAPPDATA'], 'Format-Tool')
            os.makedirs(temp_dir, exist_ok=True)

    else:
        dirname = os.path.join(os.path.abspath(os.path.dirname(__file__)),'..')
        temp_dir = dirname

    def write_fix_template(df):
        writer = pd.ExcelWriter(os.path.join(temp_dir,"data3.xlsx"), engine="xlsxwriter")
        df.to_excel(writer, sheet_name= 'hoja1',header= True , index= False, startcol= 0, startrow= 0)
        wkbk = writer.book
        ws1 = writer.sheets['hoja1']
        (max_row, max_col) = df.shape

        #FORMATS
        f1= wkbk.add_format(
            {
                'border': 1,
                'bold':1,
                'font_size':15
            }
        )
        f2= wkbk.add_format(
            {
                'border': 1,
                'bold':1,
                'font_size':15,
                'num_format':'dd/mm/yy'
            }
        )

        ws1.conditional_format(0,0,max_row,max_col-1, {'type': 'cell',
                                     'criteria': '>=',
                                     'value': 0, 'format': f1})
        ws1.conditional_format(0,0,max_row,max_col-1, {'type': 'cell',
                                     'criteria': '<',
                                     'value': 0, 'format': f1})


        

        ws1.autofit()
        ws1.set_column(0, max_col-1, 20)
        writer.close()
        return
    
    def write_wkly_dist(df):
        writer = pd.ExcelWriter(os.path.join(temp_dir,"data2.xlsx"), engine="xlsxwriter")
        df.to_excel(writer, sheet_name= 'hoja2',header= True , index= False, startcol= 0, startrow= 0)
        wkbk = writer.book
        ws1 = writer.sheets['hoja2']
        (max_row, max_col) = df.shape

        #FORMATS
        f1= wkbk.add_format(
            {
                'border': 1,
                'bold':1,
                'font_size':15
            }
        )
        f2= wkbk.add_format(
            {
                'border': 1,
                'bold':1,
                'font_size':15,
                'num_format':'dd/mm/yy'
            }
        )

        ws1.conditional_format(0,0,max_row,max_col-1, {'type': 'cell',
                                     'criteria': '>=',
                                     'value': 0, 'format': f1})
        ws1.conditional_format(0,0,max_row,max_col-1, {'type': 'cell',
                                     'criteria': '<',
                                     'value': 0, 'format': f1})


        ws1.write_formula('C2', '=TODAY()', f2)
        ws1.write_array_formula(2,2,max_row,2,'=C2',f2)

        ws1.write('E2','5532 Hermosillo',f1)
        ws1.write_array_formula(2,4,max_row,4,'=E2',f1)

        ws1.autofit()
        ws1.set_column(0, max_col-1, 20)
        writer.close()
        return

        
    def write_sheet_smart(ffdf, name):

        numeric_cols = ['CAJA', 'BQT', 'EMPAQUE']
        for col in numeric_cols:
            if col in ffdf.columns:
                ffdf[col] = pd.to_numeric(ffdf[col], errors='coerce')
        writer = pd.ExcelWriter(os.path.join(temp_dir,"data.xlsx"), engine="xlsxwriter")
        print(ffdf.to_string())
        xoff = 1
        yoff = 7
        ffdf.to_excel(writer, sheet_name= name,header= False , index= False, startcol= xoff, startrow= yoff)
        wkbk = writer.book
        ws1 = writer.sheets[name]

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

        (max_row, max_col) = ffdf.shape

        column_settings = [{"header": column} for column in ffdf.columns]
        merged_cols = column_settings
        ws1.add_table(6, 1, max_row+6, max_col, {"columns": merged_cols})

        ws1.set_column(max_col+5,max_col+5, 30)
        ws1.set_column(max_col-4,max_col-1, 15,f1)  

        ws1.write_formula(xw.utility.xl_rowcol_to_cell(max_row+yoff, max_col-4),"{=SUM("+xw.utility.xl_range(7,max_col-4,max_row+yoff-1, max_col-4)+")}",f6)
        ws1.write_formula(xw.utility.xl_rowcol_to_cell(max_row+yoff, max_col-3),"{=SUM("+xw.utility.xl_range(7,max_col-3,max_row+yoff-1, max_col-3)+")}",f6)

        ws1.insert_image('I1', os.path.join(dirname,'assets\\images\\SMART.png'))
        ws1.insert_image('A1', os.path.join(dirname,'assets\\images\\FLIX.png'))
        

        ws1.autofit()

        ws1.merge_range("F6:G6", "CANTIDAD PEDIDA", merge_format)
        ws1.merge_range("H6:I6", "CONFIRMACION EMBALAJE", merge_format)



        ws1.set_column(2,2, 15,f1)
        

        ws1.write('B5','CLIENTE:',f4)
        ws1.write('C5',' SMART CEDIS CD JUAREZ ',f2 )

        ws1.write('B6', 'FECHA DE EMBARQUE:',f4)
        ws1.write('C6', '',f2)

        ws1.write('D2', 'SOLICITUD DE PEDIDO', f3)
        ws1.write('D3', name, f3)

        ws1.write(max_row + 8,1,'NO. WET PACK:' ,f4)
        ws1.write(max_row + 9,1,'NO. AQUABOX:' ,f4)
        ws1.write(max_row + 10,1,'NO. AQUAPOLLO:' ,f4)
        ws1.write(max_row + 11,1,'TOTAL DE EMPAQUES:' ,f4)

        ws1.write(max_row + 8,2,'' ,f5)
        ws1.write(max_row + 9,2,'' ,f5)
        ws1.write(max_row + 10,2,'' ,f5)
        ws1.write(max_row + 11,2,'' ,f5)

        ws1.write(max_row+11,4,'ENTREGÓ:',f4)
        ws1.write(max_row+11,5,'',f5)
        ws1.write(max_row+11,6,'',f5)
        writer.close()
        return
    
    def write_sheet_soriana(ffdf, name):

        ffdf.drop(columns=['Tipo'], inplace=True)
        numeric_cols = ['CAJA', 'BQT', 'AQUABOX']
        for col in numeric_cols:
            if col in ffdf.columns:
                ffdf[col] = pd.to_numeric(ffdf[col], errors='coerce')
        writer = pd.ExcelWriter(os.path.join(temp_dir,"data1.xlsx"), engine="xlsxwriter")
        ffdf.to_excel(writer, sheet_name= name,header= False , index= False, startcol= 1, startrow= 7)
        wkbk = writer.book
        ws1 = writer.sheets[name]

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

        (max_row, max_col) = ffdf.shape

        column_settings = [{"header": column} for column in ffdf.columns]
        merged_cols = column_settings
        ws1.add_table(6, 1, max_row+6, max_col, {"columns": merged_cols})

        ws1.set_column(max_col+5,max_col+5, 30)
        ws1.set_column(max_col-4,max_col-1, 15,f1)  

        ws1.write_formula(xw.utility.xl_rowcol_to_cell(max_row+7, max_col-4),"{=SUM("+xw.utility.xl_range(7,max_col-4,max_row+6, max_col-4)+")}",f6)
        ws1.write_formula(xw.utility.xl_rowcol_to_cell(max_row+7, max_col-3),"{=SUM("+xw.utility.xl_range(7,max_col-3,max_row+6, max_col-3)+")}",f6)

        ws1.insert_image('I1', os.path.join(dirname,'assets\\images\\Soriana.png'))
        ws1.insert_image('A1', os.path.join(dirname,'assets\\images\\FLIX.png'))
        

        ws1.autofit()

        ws1.merge_range("E6:F6", "CANTIDAD PEDIDA", merge_format)
        ws1.merge_range("G6:H6", "CONFIRMACION EMBALAJE", merge_format)



        ws1.set_column(2,2, 15,f1)
        

        ws1.write('B5','CLIENTE:',f4)
        ws1.write('C5',' SORIANA CEDIS HERMOSILLO',f2 )

        ws1.write('B6', 'FECHA DE EMBARQUE:',f4)
        ws1.write('C6', '',f2)

        ws1.write('D2', 'SOLICITUD DE PEDIDO', f3)
        ws1.write('D3', '', f3)

        ws1.write(max_row + 8,1,'NO. WET PACK:' ,f4)
        ws1.write(max_row + 9,1,'NO. AQUABOX:' ,f4)
        ws1.write(max_row + 10,1,'NO. AQUAPOLLO:' ,f4)
        ws1.write(max_row + 11,1,'OTROS' ,f4)
        ws1.write(max_row + 12,1,'TOTAL DE EMPAQUES:' ,f4)

        ws1.write(max_row + 8,2,'' ,f5)
        ws1.write(max_row + 9,2,'' ,f5)
        ws1.write(max_row + 10,2,'' ,f5)
        ws1.write(max_row + 11,2,'' ,f5)
        ws1.write(max_row + 12,2,'' ,f5)

        ws1.write(max_row+8,4,'ENTREGÓ:',f4)
        ws1.write(max_row+8,5,'',f5)
        ws1.write(max_row+8,6,'',f5)
        ws1.write(max_row+9,5,'',f5)
        ws1.write(max_row+9,6,'',f5)

        ws1.write(max_row+11,4,'RECIBIÓ:',f4)
        ws1.write(max_row+11,5,'',f5)
        ws1.write(max_row+11,6,'',f5)
        ws1.write(max_row+12,5,'',f5)
        ws1.write(max_row+12,6,'',f5)

        writer.close()
        return



   
    def is_unique(s):
        a = s.to_numpy()
        return (a[0] == a).all()
    if format == 'SMART':
        if is_unique(fdf['Tipo']):
            name = str(fdf['Tipo'].values[0])
            fdf.drop(columns=['Tipo'], inplace=True, errors='ignore')
            write_sheet_smart(fdf, name)
        else:
            fdf1 = fdf[fdf['Tipo'] == 'flor'].copy()
            write_sheet_smart(fdf1, 'flor')
            fdf2 = fdf[fdf['Tipo'] == 'planta'].copy()
            write_sheet_smart(fdf2, 'planta')
    elif format == 'wkly_dist':
       write_wkly_dist(fdf)
       print('DDDD')
    elif format =='SORIANA':
        write_sheet_soriana(fdf, 'cSORIANA')
    elif format == 'fix_template':
        write_fix_template(fdf)
    return [(os.path.join(temp_dir,"\\data.xlsx")),dirname.split('\\')[-1]]  # Return the path to the output file and the original directory name