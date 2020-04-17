import pyxlsb
from pyxlsb import open_workbook
from pyxlsb import convert_date

import re


wb = open_workbook('temp/w44.xlsb')
RECDATE_SH="TO_DATE('28.10.2019','DD.MM.YYYY')"



RECDATEemptyFLAG=0
RECDATEshCHflag=0
params={}
ROWSlist  = []
rows    = wb.get_sheet('KPIs_GU_W').rows()

cellsList=[1,0,2,3,4,5,6,7,8,9,10,11,12,20,21,22,23,24,25,26,27,28,29,30,31,32,33]

print("SEARCHING "+RECDATE_SH+" on KPIs_GU_W")

i = 0
for row in rows:
    #print(row)
    #print(type(row))
    prev_param=''
    if i == 0:
        for CellL in cellsList:
            Cell=row[CellL]
            param=Cell.v
            #print(param)
            param = param.upper();
            param = param.replace('  ', ' ')
            param = param.replace(' ', '_')
            param = param.replace('__', '_')
            param = param.replace('_%', '_PERCENT')
            params[CellL]=param
            #print(param)
        #break
        #import sys
        #sys.exit()
    else:
        RECDATEflag = 0
        ROW         = {}
        for CellL in cellsList:
            Cell        = row[CellL]
            PARAMname   = params[CellL]
            #print(PARAMname)
            if PARAMname == 'RECDATE':
                if Cell.v:
                    try:
                        Day=convert_date(Cell.v).day
                    except AttributeError as error:
                        print(i)
                        print(error)
                        raise #=break of script
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
                    RECDATE="TO_DATE('"+StrDay+'.'+StrMM+'.'+str(convert_date(Cell.v).year)+"','DD.MM.YYYY')"
                    #print(RECDATE)
                    if RECDATE == RECDATE_SH:
                        RECDATEflag = 1
                        RECDATEshCHflag = 1
                        ROW[PARAMname] = RECDATE
                    elif RECDATEshCHflag == 1:
                        RECDATEshCHflag = 2
                        #print('1 '+PARAMname)
                        #import sys
                        #sys.exit()
                else:
                    RECDATEemptyFLAG=1
                    print("break 1: Cell.v for RECDATE is empty")
                    break
            elif RECDATEflag == 1:
                ROW[PARAMname] = str(Cell.v)
                if re.search('(^None$|^-$)', ROW[PARAMname]):
                    ROW[PARAMname]=''
                elif PARAMname == 'GEOUNIT_ID':
                    ROW[PARAMname]=re.sub('\.0$', '', ROW[PARAMname], count=0)

        if RECDATEemptyFLAG == 1 or RECDATEshCHflag == 2:
            print("break 2: if RECDATEemptyFLAG == 1 or RECDATEshCHflag == 2")
            break
        elif RECDATEflag ==1:
            #print(ROW)
            ROWSlist.append(ROW)

    i += 1




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
sql="DELETE FROM NPI.V1904_XLSB_GU WHERE RECDATE={RECDATEsh}".format(RECDATEsh=RECDATE_SH)
print(sql)
cur.execute(sql)
cur.execute("alter session  set NLS_NUMERIC_CHARACTERS= '.,'")
con.commit()

SUCC    =0
FAILED  =0
sql="INSERT INTO NPI.V1904_XLSB_GU ({param_name}) VALUES ({param_value})"
for ROW in ROWSlist:
    param_names = ''
    param_values = ''
    zpt = ''
    for CellL in cellsList:
        PARAM=params[CellL]
        param_names     = param_names+zpt+PARAM
        if PARAM == 'RECDATE':
            param_values_sh = "{param_value}"
        else:
            param_values_sh = "'{param_value}'"
        param_values    = param_values+zpt+param_values_sh.format(param_value=ROW[PARAM])
        zpt = ','
    SQL=sql.format(param_name=param_names,param_value=param_values)
    try:
        cur.execute(SQL)
        SUCC+=1
    except cx_Oracle.DatabaseError as error:
    # Log error as appropriate
        print(SQL)
        print(error)
        FAILED+=1
        #raise #=break of script


ALL=SUCC+FAILED
con.commit()
cur.close()
con.close()

print("RECORDS: "+str(ALL)+', SUCCESSFUL: '+str(SUCC)+', FAILED: '+str(FAILED))
