import pandas as pd
import os
import sys

def convert_to_SAE( case=1, df = pd.DataFrame(),e="" ):
    """
    This function takes a DataFrame and converts it to the SAE format.
    :param df: The DataFrame to be converted.
    :param case: The case number for the conversion .
    :return: the file location of the temporary SAE.MOD file.
    """
    # Determine the directory based on whether the script is frozen or not
    if getattr(sys, 'frozen', False):
        dirname = os.path.join(os.path.abspath(os.path.dirname(__file__)))
        temp_dir = os.path.join(os.environ['LOCALAPPDATA'], 'Format-Tool')
        os.makedirs(temp_dir, exist_ok=True)
    else:
        dirname = os.path.join(os.path.abspath(os.path.dirname(__file__)),'..')
        temp_dir = dirname
    os.remove(os.path.join(temp_dir, "temp.MOD"))
    #Copy the template MOD file to a temporary MOD file
    

    if case == 1:

        with open(os.path.join(dirname, 'assets\\MOD_templates\\MOD.xml')) as t, open(os.path.join(temp_dir, "temp.MOD"), 'a') as f:
            for line in t:
                f.write(line)

        nomcli="OPJUAREZ"
        headers =str(
                '<ROW  CVE_CLPV="5"'
                'NUM_ALMA="1"'
                'CVE_PEDI=""'
                'ESQUEMA="0"'
                'DES_TOT="0"' 
                'DES_FIN="0"'
                'CVE_VEND=""'
                'COM_TOT="0" '
                'NUM_MONED="1"'
                'TIPCAMB="1.000000"'
                'STR_OBS=""'
                'MODULO="FACT"'
                'CONDICION="SMART CEDIS CD JUAREZ"'
                '><dtfield>\n'
            )   
        with open(os.path.join(temp_dir, "temp.MOD"), 'a') as f:
            f.write(headers)
        for _, row in df.iterrows():
            print(row)
            print(row['CAJA'])
            cant = int(row["CAJA"]) * int(row["EMPAQUE"])
            if cant !=0:
                newrow = (
                    f'<ROWdtfield '
                    f'CANT="{cant}" '
                    f'CVE_ART="{row["CODIGO DEL PRODUCTO"]}" '
                    f'DESC1="0" '
                    f'DESC2="0" '
                    f'DESC3="0" '
                    f'IMPU1="0" '
                    f'IMPU2="0" '
                    f'IMPU3="0" '
                    f'IMPU4="" '
                    f'COMI="0" '
                    f'PREC="{row["PRECIO"]}" '
                    f'NUM_ALM="1" '
                    f'STR_OBS="" '
                    f'REG_GPOPROD="0" '
                    f'COSTO="0" '
                    f'TIPO_PROD="P" '
                    f'TIPO_ELEM="N" '
                    f'TIP_CAM="1" '
                    f'UNI_VENTA="pz" '
                    f'IMP1APLA="6" '
                    f'IMP2APLA="6" '
                    f'IMP3APLA="6" '
                    f'IMP4APLA="0" '
                    f'PREC_SINREDO="" '
                    f'COST_SINREDO="0" '
                    f'/>\n'
                )
                with open(os.path.join(temp_dir, "temp.MOD"), 'a') as f:
                    f.write(newrow)
        with open(os.path.join(temp_dir, "temp.MOD"), 'a') as f:
                f.write('</dtfield></ROW></ROWDATA></DATAPACKET>')
    if case == 2:
        with open(os.path.join(dirname, 'assets\\MOD_templates\\MOD.xml')) as t, open(os.path.join(temp_dir, "temp.MOD"), 'a') as f:
            for line in t:
                f.write(line)

        con = ("SUPERCENTER "+e.split()[1])

        headers =str(
               '<ROW CVE_CLPV="         4" ' \
               'NUM_ALMA="1" ' \
               'CVE_PEDI="" ' \
               'ESQUEMA="1" ' \
               'DES_TOT="0" ' \
               'DES_FIN="0" ' \
               'CVE_VEND="" ' \
               'COM_TOT="0"' \
               ' NUM_MONED="1" ' \
               'TIPCAMB="1" ' \
               f'STR_OBS="{con}" ' \
               'MODULO="FACT" ' \
               f'CONDICION="{con}">'
               '<dtfield>\n'
            )   
        with open(os.path.join(temp_dir, "temp.MOD"), 'a') as f:
            f.write(headers)
        df = df.loc[:, ~df.columns.duplicated()]

        # 1️⃣ Coerce to numeric, compute cant
        df["CAJAS"]     = pd.to_numeric(df["CAJAS"],     errors="coerce").fillna(0)
        df["AQUA\nBOX"] = pd.to_numeric(df["AQUA\nBOX"], errors="coerce").fillna(0)
        df["cant"]      = (df["CAJAS"] * df["AQUA\nBOX"]).astype(int)

        # 2️⃣ Group & sum, dropping zero‐cant rows if you like
        agg = (
            df[df["cant"] != 0]
            .groupby("CODIGO\nPRODUCTO", as_index=False)["cant"]
            .sum()
        )

        # 3️⃣ Emit one row per code
        with open(os.path.join(temp_dir, "temp.MOD"), 'a') as f:
            for _, row in agg.iterrows():
                cdp  = row["CODIGO\nPRODUCTO"]
                cant = row["cant"]
                newrow = (
                    f'<ROWdtfield '
                    f'CANT="{cant}" '
                    f'CVE_ART="{cdp}" '
                    f'DESC1="0" '
                    f'DESC2="0" '
                    f'DESC3="0" '
                    f'IMPU1="0" '
                    f'IMPU2="0" '
                    f'IMPU3="0" '
                    f'IMPU4="" '
                    f'COMI="0" '
                    f'PREC="" '
                    f'NUM_ALM="1" '
                    f'STR_OBS="" '
                    f'REG_GPOPROD="0" '
                    f'COSTO="0" '
                    f'TIPO_PROD="P" '
                    f'TIPO_ELEM="N" '
                    f'TIP_CAM="1" '
                    f'UNI_VENTA="pz" '
                    f'IMP1APLA="6" '
                    f'IMP2APLA="6" '
                    f'IMP3APLA="6" '
                    f'IMP4APLA="0" '
                    f'PREC_SINREDO="" '
                    f'COST_SINREDO="0" '
                    f'/>\n'
                )
                with open(os.path.join(temp_dir, "temp.MOD"), 'a') as f:
                    f.write(newrow)
        with open(os.path.join(temp_dir, "temp.MOD"), 'a') as f:
                f.write('</dtfield></ROW></ROWDATA></DATAPACKET>')

    if case==3:
        with open(os.path.join(dirname, 'assets\\MOD_templates\\MOD.xml')) as t, open(os.path.join(temp_dir, "temp.MOD"), 'a') as f:
            for line in t:
                f.write(line)

        con = ("SORIANA")

        headers =str(
               '<ROW CVE_CLPV="         4" ' \
               'NUM_ALMA="1" ' \
               'CVE_PEDI="" ' \
               'ESQUEMA="1" ' \
               'DES_TOT="0" ' \
               'DES_FIN="0" ' \
               'CVE_VEND="" ' \
               'COM_TOT="0"' \
               ' NUM_MONED="1" ' \
               'TIPCAMB="1" ' \
               f'STR_OBS="{con}" ' \
               'MODULO="FACT" ' \
               f'CONDICION="{con}">'
               '<dtfield>\n'
            )   
        with open(os.path.join(temp_dir, "temp.MOD"), 'a') as f:
            f.write(headers)
        df = df.loc[:, ~df.columns.duplicated()]

        # 1️⃣ Coerce to numeric, compute cant
        df["CANTIDAD"]     = pd.to_numeric(df["CANTIDAD"],     errors="coerce").fillna(0)
        df["PRECIO"]     = pd.to_numeric(df["PRECIO"],     errors="coerce").fillna(0)

        # 2️⃣ Group & sum, dropping zero‐cant rows if you like
        agg = (
            df[df["CANTIDAD"] != 0]
            .groupby("CÓDIGO", as_index=False)["CANTIDAD"]
            .sum()
        )

        # 3️⃣ Emit one row per code
        with open(os.path.join(temp_dir, "temp.MOD"), 'a') as f:
            for _, row in agg.iterrows():
                cdp  = row["CÓDIGO"]
                cant = row["CANTIDAD"]
                prec = row['PRECIO']
                newrow = (
                    f'<ROWdtfield '
                    f'CANT="{cant}" '
                    f'CVE_ART="{cdp}" '
                    f'DESC1="0" '
                    f'DESC2="0" '
                    f'DESC3="0" '
                    f'IMPU1="0" '
                    f'IMPU2="0" '
                    f'IMPU3="0" '
                    f'IMPU4="" '
                    f'COMI="0" '
                    f'PREC="{prec}" '
                    f'NUM_ALM="1" '
                    f'STR_OBS="" '
                    f'REG_GPOPROD="0" '
                    f'COSTO="0" '
                    f'TIPO_PROD="P" '
                    f'TIPO_ELEM="N" '
                    f'TIP_CAM="1" '
                    f'UNI_VENTA="pz" '
                    f'IMP1APLA="6" '
                    f'IMP2APLA="6" '
                    f'IMP3APLA="6" '
                    f'IMP4APLA="0" '
                    f'PREC_SINREDO="" '
                    f'COST_SINREDO="0" '
                    f'/>\n'
                )
                with open(os.path.join(temp_dir, "temp.MOD"), 'a') as f:
                    f.write(newrow)
        with open(os.path.join(temp_dir, "temp.MOD"), 'a') as f:
                f.write('</dtfield></ROW></ROWDATA></DATAPACKET>')


    return os.path.join(temp_dir, "temp.MOD")

