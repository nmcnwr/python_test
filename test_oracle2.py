#import os
#os.environ["LD_LIBRARY_PATH"] = "C:\oracle\ora11\lib"

#print(os.environ["ORACLE_HOME"])
#os.environ["ORACLE_HOME"] = "C:\oracle\ora11"

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

# Delete rows
statement = 'delete from DIC_VENDORS where ID=6'
cur.execute(statement)

# Insert default rows
rows = [(7, 'ZTE', 'Z', 'ZT')]
cur.bindarraysize = 1
cur.setinputsizes(int, 50, 1, 2)
cur.executemany("insert into DIC_VENDORS(ID, NAME, CODE, CODE2) values (:1, :2, :3, :4)", rows)
con.commit()

cur.execute('SELECT ID, NAME, CODE, CODE2 FROM CC.DIC_VENDORS')
for result in cur:
    print(result)

cur.close()
con.close()

