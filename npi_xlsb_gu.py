import pyxlsb
from pyxlsb import open_workbook
from pyxlsb import convert_date

import re

wb = open_workbook('npi16.xlsb')

nets    = {}
params  = {}
rows    = wb.get_sheet('Norm_KPI').rows()

i = 0
for row in rows:
    #print(row)
    #print(type(row))
    prev_param=''
    if i == 0:
        for Cell in row:
            param=Cell.v
            param = param.upper();
            param = param.replace('  ', ' ')
            param = param.replace(' ', '_')
            param = param.replace('__', '_')
            param = param.replace('_МГЦ', '')
            if param == 'SUMMER':
                param=prev_param.replace('_NORM','_SUMMER')
                prev_param = ''
            elif re.search('(NET|REGION|MONTH|PRIORITY|INFORMATIONAL)', param):
                next
            else:
                param=(param+'_NORM')
                prev_param = param
            params[Cell.c]=param
            #print(str(Cell.c)+param+'-')

#        break
    else:
        ii = 0
        norms={}
        Net=''
        for Cell in row:
            #print(str(ii))
            if params[ii] == 'MONTH':
                Day=convert_date(Cell.v).day
                StrDay=''
                if Day<10:
                    StrDay='0'+str(Day)
                else:
                    StrDay=str(Day)
                MM = convert_date(Cell.v).month
                StrMM = ''
                if MM<10:
                    StrMM='0'+str(MM)
                else:
                    StrMM=str(MM)
                Month="TO_DATE('"+StrDay+'.'+StrMM+'.'+str(convert_date(Cell.v).year)+"','DD.MM.YYYY')"
                #print(params[ii]+' '+Month)
                norms[params[ii]] = Month
            else:
                norm_value=str(Cell.v)
                #if norm_value == 'None':
                if re.search('(^None$|^-$)', norm_value):
                    norm_value=''
                elif re.search('\*', norm_value):
                    norm_value = norm_value.replace('*', '')
                    norm_value = norm_value.replace(',', '.')
                    norm_value = float(norm_value)
                else:
                    norm_value=Cell.v
                if Net == 'Yoshkar-Ola':# Sochi  Yoshkar-Ola
                    if params[ii] == 'CUNSSR_2G3G_NORM': #INFORMATIONAL CUNSSR_2G3G_NORM
                        print(norm_value)
                norms[params[ii]]=norm_value
                if params[ii] == 'NET':
                    Net=Cell.v
            ii +=1
        #print(norms)
        nets[Net+'_'+Month]=norms
        #if Net=='Yoshkar-Ola':
            #print(norms)
#        norms{}

    i += 1

#print(nets)
#for param in params:
#    print (param)
##from pyxlsb import convert_date
##print(convert_date(41235.45578))
# datetime.datetime(2012, 11, 22, 10, 56, 19)

sql_list=[]
sql="INSERT INTO NPI.TEST_PY_NORM_NPI ({param_name}) VALUES ({param_value})"
for netmonth in nets:
    #print(nets[net])
    param_names     = ''
    param_values    = ''
    normatives      =  nets[netmonth]
    zpt=''
    for param in normatives:
        param_names     = param_names+zpt+param
        if param == 'MONTH':
            param_values_sh = "{param_value}"
        else:
            param_values_sh = "'{param_value}'"
        param_values    = param_values+zpt+param_values_sh.format(param_value=normatives[param])
        zpt = ','
    sql_list.append(sql.format(param_name=param_names,param_value=param_values))
    #print(sql.format(param_name=param_names,param_value=param_values))


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
cur.execute('TRUNCATE TABLE NPI.TEST_PY_NORM_NPI')
con.commit()


g=0
b=0
for sql in sql_list:
    #print(sql)
    try:
        cur.execute(sql)
        g+=1
    except cx_Oracle.DatabaseError as error:
    # Log error as appropriate
        print(sql)
        print(error)
        b+=1
        #raise #=break of script
con.commit()
cur.close()
con.close()

allR=g+b
print("RECORDS: "+str(allR)+', SUCCESFULL: '+str(g)+', FAILED: '+str(b))
