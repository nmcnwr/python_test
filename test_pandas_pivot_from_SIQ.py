import pandas as pd
import openpyxl


parse_dates = ['minD', 'maxD']

df1 = pd.read_csv('temp/siq_2020_02_24_vs_2020_03_04_msk.csv', delimiter=';', decimal=',', parse_dates=parse_dates)

print(df1.head(5))

#
# df1['DATE'] = df1['DATETIME_ID'].dt.date
#
# # Take only needed columns
# df2 = df1.loc[:, ('LAC', 'Element', 'BeelineObject', 'CELL_ID', 'DATE', 'CDR', 'CunSSR')]
#
pd.set_option('display.max_columns', None)
#
#



df41 = pd.pivot_table(df1
                        , index=['Element', 'BeelineObject']
                        , columns=['DatePeriod']
                        , values=["CDR_Drops"]

                        ).reset_index()

df41.columns = ['Element', 'BeelineObject', 'Drops_LastWeek', 'Drops_Yesterday']
df41['Diff_Drops'] = df41['Drops_Yesterday']*100/df41['Drops_LastWeek']
print(df41.head(5))

print('_'*20, 'test1')
df_test1 = df41[(df41.BeelineObject == 'WL225687')]
print(df_test1.head(5))

print('_'*20, 'test2')
df_test2 = df41[(df41.Diff_Drops > 100) & (df41.Drops_Yesterday > 20) & (df41.Element == 'RNC5BAR')]
print(df_test2.head(10))


#
# df41.to_excel("temp/siq_2020_02_24_vs_2020_03_04_msk.xlsx")
#
