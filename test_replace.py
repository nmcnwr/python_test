import pyxlsb

from pyxlsb import open_workbook
from pyxlsb import convert_date

wb = open_workbook('npi.xlsb')

# Using the sheet index (1-based)
##with wb.get_sheet(1) as sheet:
    # Do stuff with sheet

# Using the sheet name
##with wb.get_sheet('Sheet1') as sheet:
    # Do stuff with sheet
#sheet=wb.get_sheet('Norm_KPI')

# You can use .rows(sparse=True) to skip empty rows
##for row in sheet.rows():
##    print(row)
    # [Cell(r=0, c=0, v='TEXT'), Cell(r=0, c=1, v=42.1337)]
'''
i=0
for row in sheet.rows():
    print(row[0].v)
    if i == 5:
        break
    i += 1
'''
'''
i=0
for row in sheet.rows():
    for Cell in row:
        print(Cell.v)
    if i == 5:
        break
    i += 1
'''
nets={}

params={}
rows=wb.get_sheet('Norm_KPI').rows()
#print(type(rows))

i = 0
for row in rows:
#    print(type(row))
    prev_param=''
    if i == 0:
        for Cell in row:
            param=''
            if Cell.v == 'Summer':
                param=prev_param+'_SUMMER'
                prev_param = ''
            else:
                param=Cell.v+'_NORM'
                #param = param.replace('  ', ' ')
                #param = param.replace(' ', '_')
                #param = param.replace('__', '_')
                param = param.replace('5 МГЦ_NORM', '')
                prev_param = param
            param=param.upper()
            params[Cell.c]=param
            print(param)

#        break
    else:
        ii = 0
        norms={}
        Net=''
        for Cell in row:
            if params[ii] == 'Month':
#                print(params[ii])
                Day=convert_date(Cell.v).day
                StrDay=''
                if Day<10:
                    StrDay='0'+str(Day)
                else:
                    StrDay=str(Day)
                Month="TO_DATE('"+StrDay+'.'+str(convert_date(Cell.v).month)+'.'+str(convert_date(Cell.v).year)+"','DD.MM.YYYY')"
                norms[params[ii]] = Month
            else:
                norms[params[ii]]=Cell.v
                if params[ii] == 'Net':
                    Net=Cell.v
            ii +=1
        #print(norms)
        nets[Net]=norms
#        norms{}

    i += 1

#print(nets)
#for param in params:
#    print (param)
##from pyxlsb import convert_date
##print(convert_date(41235.45578))
# datetime.datetime(2012, 11, 22, 10, 56, 19)
'''
sql="INSERT INTO NPI.TEST_PY_NORM_NPI ({param_name}) VALUES ({param_value});"
for net in nets:
    #print(nets[net])
    param_names     = ''
    param_values    = ''
    normatives      =  nets[net]
    zpt=''
    for param in normatives:
        param_names     = param_names+zpt+param
        param_values_sh = "'{param_value}'"
        param_values    = param_values+zpt+param_values_sh.format(param_value=normatives[param])
        zpt = ','
print(sql.format(param_name=param_names,param_value=param_values))
'''
'''
import cx_Oracle


ip = '10.136.12.164'
port = 1521
SID = 'RAN'
dsn_tns = cx_Oracle.makedsn(ip, port, SID)
print (dsn_tns)
con = cx_Oracle.connect('NPI', 'NPI', dsn_tns)

#con = cx_Oracle.connect('CC/CC@10.136.12.164/RAN')
#con = cx_Oracle.connect("CC", "CC", "Violet")


connstr = 'NPI/NPI@10.136.12.164:1521/RAN'
con = cx_Oracle.connect(connstr)

cur = con.cursor()
cur.execute('SELECT *  FROM NPI.TEST_PY_NORM_NPI')
columns = [col[0] for col in cur.description]
#for result in cur:
#    print(result)
result_set = cur.fetchall()
for row in result_set:
    rows = dict(zip(columns, row))
    print(rows)
cur.close()
con.close()
'''