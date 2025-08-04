import pandas as pd
import os
import sys

def convert_to_SAE( case=1, df = pd.DataFrame() ):
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

    #Copy the template MOD file to a temporary MOD file
    

    if case == 1:

        with open(os.path.join(dirname, 'MOD.xml')) as t, open(os.path.join(temp_dir, "temp.MOD"), 'a') as f:
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
                '><dtfield>'
            )   
        with open(os.path.join(temp_dir, "temp.MOD"), 'a') as f:
            f.write(headers)
        for row in df.iterrows():
            cant = row["CAJA"]*row["EMPAQUE"]
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
                f'STR_OBS="{row["OBSERVACIONES"]}" '
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
        with open(os.path.join(dirname, 'MOD.xml')) as t, open(os.path.join(temp_dir, "temp.MOD"), 'a') as f:
            for line in t:
                f.write(line)

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
               'STR_OBS="SUPERCENTER" ' \
               'MODULO="FACT" ' \
               'CONDICION="SUPERCENTER">'
               '<dtfield>'
            )   
        with open(os.path.join(temp_dir, "temp.MOD"), 'a') as f:
            f.write(headers)
        for row in df.iterrows():
            try:
                cant = int(row["CAJAS"])*int(row["AQUA\nBOX"])
            except TypeError:
                cant=0
            if cant !=0:
                cdp = row["CODIGO\nPRODUCTO"]
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
                    f'STR_OBS="{row["OBSERVACIONES"]}" '
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

