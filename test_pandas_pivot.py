import pandas as pd
import openpyxl


parse_dates = ['DATETIME_ID', 'DATETIME_SVR']

df1 = pd.read_csv('temp/siq_2020_03_03_1450_msk.csv', delimiter=';', decimal=',', parse_dates=parse_dates)

df1['DATE'] = df1['DATETIME_ID'].dt.date

# Take only needed columns
df2 = df1.loc[:, ('LAC', 'Element', 'BeelineObject', 'CELL_ID', 'DATE', 'CDR', 'CunSSR')]

#pd.set_option('display.max_columns', None)


df41 = pd.pivot_table(df2
                        , index=['LAC', 'Element', 'BeelineObject', 'CELL_ID']
                        , columns=['DATE']
                        , values=["CDR"]
                        , aggfunc={'CDR': 'mean'}
                        )#.reset_index()
print(df41.head(5))

df41.to_excel("temp/siq_2020_03_03_1450_msk.xlsx")

