import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy import types
from sqlalchemy.types import DateTime

print('df400 to Oracle...')
import datetime
DT = datetime.datetime.now()
filename = 'er_7g'


dict_ = {'filename': filename, 'DT': DT}
df = pd.DataFrame([dict_])
print(df.head())

engine = create_engine('oracle://CC:CC@Violet')

con = engine.connect()
sql = ("""
MERGE INTO CC.OPER_LOG T2
USING (	select 'er_5g' FILENAME, sysdate DT from DUAL) T1
on (T2.FILENAME=T1.FILENAME)
WHEN MATCHED THEN UPDATE SET T2.DT = SYSDATE 
WHEN NOT MATCHED THEN 	INSERT (T2.FILENAME, T2.DT)	VALUES (T1.FILENAME, T1.DT)
""")
con.execute(sql)

dtyp = {'filename': types.VARCHAR(50), 'DT': types.DateTime}
df.to_sql('oper_log', engine, if_exists='append', index=False, dtype=dtyp)

con.close()
