import pandas as pd
from datetime import datetime

parse_dates = ['DATETIME']
df1 = pd.read_csv("arr2img_3.csv", delimiter=',', parse_dates=parse_dates)


print(df1.head())
print(type(df1))

dt_min = min(df1["DATETIME"]).date()
dt_max = max(df1["DATETIME"]).date()

print('50')
start_point = str(dt_min)
start_hour = datetime.strptime(start_point,'%Y-%m-%d')
print(start_hour)

print(55)
stop_point = str(dt_max)+' 23:45:00'
stop_hour = datetime.strptime(stop_point, '%Y-%m-%d %H:%M:%S')
print(stop_hour)


print(70)
print(dt_min,' - ',dt_max)

print(120)
idx1 = pd.period_range(start_hour, stop_hour, freq='H', name='time')

print(idx1)
print(type(idx1))


