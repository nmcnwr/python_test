import cx_Oracle


ip = '10.136.12.164'
port = 1521
SID = 'RAN'
dsn_tns = cx_Oracle.makedsn(ip, port, SID)
print (dsn_tns)
con = cx_Oracle.connect('CC', 'CC', dsn_tns)

#con = cx_Oracle.connect('CC/CC@10.136.12.164/RAN')
#con = cx_Oracle.connect("CC", "CC", "Violet")


connstr = 'CC/CC@10.136.12.164:1521/RAN'
con = cx_Oracle.connect(connstr)

cur = con.cursor()
cur.execute('SELECT ID, NAME, CODE, CODE2 FROM CC.DIC_VENDORS')
for result in cur:
    print(result)
cur.close()
con.close()