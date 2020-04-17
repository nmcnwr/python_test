import pandas as pd
import numpy as np
import pandas_profiling

#parse_dates = ['DATETIME_ID', 'DATETIME_SVR']
parse_dates = ['DATE_ID']
df1 = pd.read_csv('temp/siq_v202003051200_msk.csv', delimiter=';', decimal=',', parse_dates=parse_dates)


# df2 = df1.loc[:, ('LAC', 'Element', 'CELL_ID',  'CDR', 'CunSSR')]
df2 = df1.loc[:, ('BeelineObject', 'DATE_ID',  'CDR_Drops')]


df3 = df2 #.head(5000)

#pandas_profiling.ProfileReport(df3)

profile = df3.profile_report(title='Pandas Profiling Report')
profile.to_file(output_file='temp/PandasProfilingReport_2.html')
