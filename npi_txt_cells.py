

import re

NUMBER_VALS=['GEOUNIT_ID','GU_GROUP','NRI_SITEID','NRI_BAND','W_GU_NET','CELL_PERC_VOICE','BAD_VOICE_PERC','BT_VOICE','CELL_PERC_DATA','BAD_DATA_PERC','BT_DATA','CELL_PERC_LS_1100','A1100_PERC','LS_TR_1100','CELL_PERC_LS_2500','A2500_PERC','LS_TR_2500','BAD_TRAF_VOICE','TRAF_VOICE_INT','BAD_TRAF_DATA','LS_TRAF_1100','LS_TRAF_2500','TRAF_DATA_INT','ATT_VOICE','TRAF_VOICE_BH','CUNSSR_VOICE','CDR_VOICE','S_CONG','ATT_DATA','TRAF_DATA_BH','USERS_DATA_TR_BH','CUNSSR_DATA','CDR_DATA','TROUGHPUT','USERS_BH','USER_THROUGHPUT_BH','BC_VOICE_D','BC_DATA_D','LAC_BSS_NAME','BANDWIDTH']

ROWSlist  = []
i = 0
f = open('temp/W16_Cells.txt', 'r', encoding='ANSI')

'''
ii = 1
try:
    for row in f:
        ii+=1
except:
    # Log error as appropriate
    print(ii)
    raise #=break of script
'''

for row in f:
    #print(row)
    row=re.sub('п»ї','',row)
    row = re.sub('#ДЕЛЕНИЕ/0', '', row)
    row=row.rstrip('\n\r')
    #print(row)
    if i == 0:
        PARAM_NAMES=row.split('\t')
        par_i = 0
        for param in PARAM_NAMES:
            param = param.upper();
            param = param.replace('_%', '_PERC')
            #print(param)
            if re.search('^\d', param):
                param='A'+param
            #print(param)
            PARAM_NAMES[par_i]=param
            par_i += 1
#    elif i>10:
#        break
    else:
        PARAM_VALUES=row.split('\t')
        ROW={}
        val_i = 0
        for val in PARAM_VALUES:
            param_name=PARAM_NAMES[val_i]
           # print(param_name + " " + val)
            val = re.sub('\'', '', val)
            val = re.sub('^\s*', '', val)
            val = re.sub('\s*$', '', val)
            #print (param_name+" "+val)
            if param_name == 'RECDATE':
                val="TO_DATE('"+val+"','DD.MM.YYYY')"
            #print(param_name + " " + val)
            ROW[param_name] = val
            val_i += 1
        ROWSlist.append(ROW)

    i += 1
f.close()



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
sql="TRUNCATE TABLE NPI.V1904_CELLS_TEMP"
print(sql)
cur.execute(sql)
con.commit()

SUCC    =0
FAILED  =0
sql="INSERT INTO NPI.V1904_CELLS_TEMP ({param_name}) VALUES ({param_value})"
for ROW in ROWSlist:
    #print(ROW)
    param_names = ''
    param_values = ''
    zpt = ''
    for PARAM in PARAM_NAMES:
        #print(PARAM)
        #print(ROW[PARAM])
        param_names     = param_names+zpt+PARAM
        #if PARAM in NUMBER_VALS:
            #ROW[PARAM]=param.replace('.', ',')
        if PARAM == 'RECDATE':
            param_values_sh = "{param_value}"
        else:
            param_values_sh = "'{param_value}'"
        param_values    = param_values+zpt+param_values_sh.format(param_value=ROW[PARAM])
        zpt = ','

    SQL=sql.format(param_name=param_names,param_value=param_values)
    #print(SQL)
    try:
        cur.execute(SQL)
        SUCC+=1
    except cx_Oracle.DatabaseError as error:
    # Log error as appropriate
        print(SQL)
        print(error)
        FAILED+=1
        #raise #=break of script
    ALL = SUCC + FAILED
    if ALL in [100000,200000,300000,400000,500000,600000,700000,800000,900000]:
        print("IN PROGRESS: RECORDS: " + str(ALL) + ', SUCCESSFUL: ' + str(SUCC) + ', FAILED: ' + str(FAILED))

TOTAL=SUCC+FAILED
con.commit()
cur.close()
con.close()

print("TOTAL: RECORDS: "+str(TOTAL)+', SUCCESSFUL: '+str(SUCC)+', FAILED: '+str(FAILED))
