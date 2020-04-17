import pandas as pd
import glob
import os
import time

parse_dates = ['DATETIME_ID', 'DATETIME_SVR']



path = r'C:\Web\NMCPython\kpistat_2csv'                     # use your path
all_files = glob.glob(os.path.join(path, "dwhdb_MSK_202003*_er_3g_15min.res"))     # advisable to use os.path.join as this makes concatenation OS independent


datatype_dict = {
'CDR': 'float16',
'CDR_Attempts': 'uint16',
'CDR_Drops': 'uint16',
'CunSR': 'float16',
'CunSR_Attempts': 'uint16',
'CunSR_Drops': 'uint16',
'CunSSR': 'float16',
'CunSSR_Attempts': 'uint16',
'CunSSR_Drops': 'uint16',
'LAC': 'uint16',
'CELL_ID': 'uint16',
'RAB_DR_PS': 'float16',
'RAB_DR_PS_Attempts': 'uint16',
'RAB_DR_PS_Drops': 'uint16',
'RAB_FR_PS': 'float16',
'RAB_FR_PS_Attempts': 'uint16',
'RAB_FR_PS_Drops': 'uint16',
'RAB_Setup_FR_CS': 'float16',
'RAB_Setup_FR_CS_Attempts': 'uint16',
'RAB_Setup_FR_CS_Drops': 'uint16',
'RRC_CSetup_FR_CS': 'float16',
'RRC_CSetup_FR_CS_Attempts': 'uint16',
'RRC_CSetup_FR_CS_Drops': 'uint16',
'RRC_CSetup_FR_PS': 'float16',
'RRC_CSetup_FR_PS_Attempts': 'uint16',
'RRC_CSetup_FR_PS_Drops': 'uint16',
'U_CunSR_PS': 'float16',
'U_CunSR_PS_Attempts': 'uint16',
'U_CunSR_PS_Drops': 'uint16',
'U_CunSSR_PS': 'float16',
'U_CunSSR_PS_Attempts': 'uint16',
'U_CunSSR_PS_Drops': 'uint16'

}



df_from_each_file = (pd.read_csv(f, delimiter=';', decimal='.', parse_dates=parse_dates, header=0, dtype=datatype_dict) for f in all_files)
concatenated_df = pd.concat(df_from_each_file, ignore_index=False)


# view mem usage of df:

concatenated_df.info(memory_usage='deep')
# doesn't create a list, nor does it append to one

time.sleep(10)
df2 = concatenated_df.loc[:, ('LAC',  'CELL_ID', 'DATETIME_SVR', 'CDR_Drops')]
del concatenated_df

print('_'*20, 'memory_usage df2:')
df2.info(memory_usage='deep')

#df3 = df2[(df2.LAC == 27913)]
#df3 = df2[(df2.LAC == 27913) & (df2.CELL_ID == 31051)]
#df3 = df2[(df2.LAC == 46138) & (df2.CELL_ID == 19866)]
df3 = df2 # [(df2.LAC == 46138)]



df41 = pd.pivot_table(df3
                        , index=['LAC', 'CELL_ID']
                        , columns=['DATETIME_SVR']
                        , values=["CDR_Drops"]

                        ).reset_index()



headers = list(df41.columns)

# new headers
new_column_list = []

for id, item in enumerate(headers):
    if type(item) is str:
        new_column_list.insert(id, item)
    else:
        new_column_list.insert(id, str(item[1]))

# set new header
new_column_list[0] = 'LAC'
new_column_list[1] = 'CELL_ID'
# print(new_column_list)
# print(new_column_list[-1])
df41.columns = new_column_list
# print(df41.head())

dates = list(df41.columns)

dates.remove('LAC')
dates.remove('CELL_ID')
dates.remove(new_column_list[-1])
# print(dates)
df41['lastt'] = df41.iloc[:, -1]
df41['before'] = df41[dates].mean(axis=1)
df41['diff'] = df41['lastt']*100/df41['before']


df41 = df41.fillna(0)
df42 = df41[(df41.lastt > 5)]

df52 = df42.loc[:, ('LAC', 'CELL_ID', 'before', 'lastt', 'diff')]
print(df52.head(500))

time.sleep(10)
