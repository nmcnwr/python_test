import pyxlsb

from pyxlsb import open_workbook
from pyxlsb import convert_date

wb = open_workbook('npi.xlsb')
nets={}

params={}
rows=wb.get_sheet('Norm_KPI').rows()
i = 0
for row in rows:
    prev_param=''
    if i == 0:
        for Cell in row:
            if 'CELL_DL_AVG_THR' in Cell.v:
                param=Cell.v
                print(param)
                print(param.replace('МГц', ''))
        break
    i += 1
