import pandas as pd


parse_dates = ['DATETIME_ID', 'DATETIME_SVR']

df1 = pd.read_csv('temp/siq_2020_03_01_wl225687.csv', delimiter=';', decimal=',', parse_dates=parse_dates)

df1['DATE'] = df1['DATETIME_ID'].dt.date

# Take only needed columns
df2 = df1.loc[:, ('LAC', 'Element', 'BeelineObject', 'CELL_ID', 'DATE', 'CDR')]

print(df2.head(5))

df2['Element'] = "Element:" + df2['Element'] + ",LAC:" + df2['LAC'].map(str) + ",node:" + df2['BeelineObject'] + ",CELL_ID:" + df2['CELL_ID'].map(str)

df55 = df2.loc[:, ('Element',  'DATE', 'CDR')]



print(df55.columns)

# Dataframe with FDN:
print(df55.head(10))

#pd.set_option('display.max_columns', None)
#pd.set_option('display.max_rows', None)



df4 = pd.pivot_table(df55
                        , index=['Element',  'DATE']
                        , values=["DATE", 'Element', 'CDR']
                        , aggfunc={'CDR': 'mean'}
                        ).reset_index()
# transfer column names
#   Index(['LAC', 'BeelineObject', 'DATE', 'mean CDR', 'count Element'], dtype='object')
#   Index(['_LAC', '_BeelineObject', '_DATE', 'mean_CDR', 'count_Element'], dtype='object')
##df_agg_BS.columns = ["Val_".join((j, i))for i, j in df_agg_BS.columns]



print(df4.head(5))


df5 = df4.pivot(index='Element', columns='DATE', values='CDR')
print(df5.head(10))

