import pandas as pd

parse_dates = ['DATE_ID']



df01 = pd.read_csv('temp/siq_v202003051200_msk.csv', delimiter=';', decimal=',', parse_dates=parse_dates)
df02 = pd.read_csv('temp/siq_v202003051205_msk.csv', delimiter=';', decimal=',', parse_dates=parse_dates)


#frames = [df01, df02]

#df1 = pd.concat(frames)

df1 = pd.concat([df02, df01], axis=0)#.reindex(df01.index)
print(df01.describe())
print(df02.describe())

print(df1.describe())
df2 = df1[(df1.BeelineObject == '10447')]

print(df2.head(60))
