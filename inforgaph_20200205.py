
import cx_Oracle
import pandas as pd
import numpy as np
from PIL import Image
from matplotlib import cm

# Globus_Tafr_ER2G.sql
# Globus_Traffic.sql


with open('Globus_Tafr_ER2G.sql', 'r') as sql:
    query = sql.read()

connstr = 'glview/readonly@192.168.181.125:1521/orcl'
con = cx_Oracle.connect(connstr)
cur = con.cursor()
cur.execute(query)

df_ora = pd.read_sql(query, con=con)                # create DataFrame from Pivot SQL
df_drop = df_ora.drop(df_ora.columns[[0]], axis=1)  # drop date column
df_fillna = df_drop.fillna(-0.1)                    # change NaN to -0.1
np_array = df_fillna.values                         # convert DataFrame to Numpy array values

#print(np_array)

ar11 = np_array
ar2 = (ar11 - np.min(ar11))/np.ptp(ar11)            # Normalize data from 0 to 1
#print(ar2)

img = Image.fromarray(np.uint8(cm.jet(ar2)*255))    # colormap heatmap "jet"

#im2arr = np.array(img)
#print(type(im2arr))

#img = Image.fromarray(im2arr)


# Image resize:
basewidth = 300
wpercent = (basewidth / float(img.size[0]))
hsize = int((float(img.size[1]) * float(wpercent)))
img_ready = img.resize((basewidth, hsize), Image.NEAREST)  # Image.NEAREST<->Image.ANTIALIAS




img_ready.save('image_from_Globus.png')
img_ready.show()

#done: на рисунке создать столбец будних и выходных дней
#note:  -0.1 [  0   0 127 255]
#done: увеличить image в два-три раза

#todo: отобразить часы 00:00 - 00:23
#todo: opencv - добавить заголовок, легенду, оси, даты

#todo: замена в sql #cell
#todo: выборка объекта из глобуса по номеру сектора
#todo: globus - cell drops sql


#todo: cell drop map from adamdb



