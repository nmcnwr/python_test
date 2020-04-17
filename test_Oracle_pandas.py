from sqlalchemy import create_engine
import pandas as pd
engine = create_engine('oracle://CC:CC@Violet')
con = engine.connect()
outpt = con.execute("SELECT * FROM CC.DIC_NET_NSS_NOKIA")
df = pd.DataFrame(outpt.fetchall())
df.columns = outpt.keys()
print(df.head())

df.to_sql('server1_er_3g_15min', engine, if_exists='replace', index=False)

con.close()
