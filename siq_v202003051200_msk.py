import pandas as pd
import numpy as np
import openpyxl
from datetime import date, timedelta
import re
import scipy.stats

parse_dates = ['DATE_ID']



df01 = pd.read_csv('temp/siq_v202003051200_msk.csv', delimiter=';', decimal=',', parse_dates=parse_dates)
df02 = pd.read_csv('temp/siq_v202003051200_msk.csv', delimiter=';', decimal=',', parse_dates=parse_dates)

df1 = pd.concat([df01, df02], axis=1).reindex(df01.index)
print(df01.head(5))
print(df02.head(5))
print(df1.head(5))



# full screen option (printing)
pd.set_option('display.max_columns', None)

# get yesterday
yesterday = date.today() - timedelta(days=1)
yesterday = yesterday.strftime('%Y-%m-%d')


# if case then

df1['Period'] = 'BeforeYDA'
df1.loc[df1['DATE_ID'] == yesterday, 'Period'] = 'Yesterday'


print(df1.head(3))

#
# # Take only needed columns
# df2 = df1.loc[:, ('LAC', 'Element', 'BeelineObject', 'CELL_ID', 'DATE', 'CDR', 'CunSSR')]
#
#
#

df1['DATE_ID'] = df1['DATE_ID'].dt.date
# in pivot tables - columns change value from 'DatePeriod'<->'Period'
# NOTE use DatePeriod for test !!!
#     NOTE use Period for real data !!!
#


df42 = pd.pivot_table(df1
                        , index=['Element', 'BeelineObject']
                        , columns=['DatePeriod', 'DATE_ID']
                        , values=["CDR_Drops"]
                        )#.reset_index()
df42["CDR_Drops"] = df42["CDR_Drops"].fillna(0.0).astype(int)


# df42 = df42.div(df42.sum(axis=1), axis=0)
# print('_'*20, 'Normalize', '_'*20)
# print(df42.head(5))

# axisvalues = list(range(1, len(df42.columns)+1))
#
# def calc_slope(row):
#     a = scipy.stats.linregress(row, y=axisvalues)
#     return a.slope
#
# df42['slope'] = df42.apply(calc_slope, axis=1)

# check if row is monotonic decrease
# df42['df_status'] = df42.T.apply(lambda x: x.is_monotonic)
# #df42 = df42.rename({'df_status': 'decrease'}, axis='columns')
#
# df42 = df42.rename(columns = {'NaT': 'Name1', 'NaT': 'Name2'})


print(df42.head(5))

df41 = pd.pivot_table(df1
                        , index=['Element', 'BeelineObject']
                        , columns=['DatePeriod']
                        , values=["CDR_Drops"]
                        , aggfunc={'CDR_Drops': 'mean'}
                        )#.reset_index()

# float to int:

df41["CDR_Drops"] = df41["CDR_Drops"].fillna(0.0).astype(int)

df41.columns = ['SumKPI_BeforeYDA', 'SumKPI_YDA']
df41['Diff_Drops'] = df41['SumKPI_YDA']*100/df41['SumKPI_BeforeYDA']
print(df41.head(5))

print('_'*30, 'Total', '_'*30)
pd.set_option('display.max_columns', None)
df43 = pd.concat([df42, df41], axis=1).reindex(df42.index)






headers = list(df43.columns)

# new headers
new_column_list = []

for id, item in enumerate(headers):
    if type(item) is str:
        new_column_list.insert(id, item)
    else:
        new_column_list.insert(id, str(item[2]))

# set new header
df43.columns = new_column_list

df43 = df43.rename(columns={'NaT': 'Name1', 'NaT': 'Name2'})

# for better view in Excel reset_index
df43 = df43.reset_index(drop=False)
print(df43.head(5))


df43.to_excel("temp/siq_202003051200_msk.xlsx")
