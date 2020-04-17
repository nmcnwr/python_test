import pandas as pd

dates = ['DT']
indexcols = ['LAC', 'CELLID']
df1 = pd.read_csv('test_CDR.csv', sep=';', parse_dates=dates, index_col=indexcols)

df1['DD'] = df1['DT'].dt.date
del df1['DT']

print('df1 RAW:')
print(df1.head(20))

idx = df1.groupby(['LAC', 'CELLID'])['DD'].transform(max) == df1['DD']
df2 = df1[idx]
print('df2 last cell date:')
print(df2)

# df3 = df2.groupby(['LAC', 'CELLID', 'DD']).mean()
#
# print('df3 Groupping:')
# print(df3.head(20))

agglist = {'CDR': ['mean', 'count'], 'CunSR': 'mean'}
df4 = df2.groupby(['LAC', 'CELLID', 'DD']).agg(agglist)
print('df4 Groupping:')
print(df4.head(20))
