import pandas as pd

f = 'logs/test_dataframe_isnull.csv'

df = pd.read_csv(
    f,
    delimiter=';',
    decimal='.',
    header=0,
    index_col=["LAC", "CELL_NAME", "SITE_NAME", 'Element', 'Server', 'BAND', 'PERIOD_DURATION'],
    parse_dates=["DATETIME_ID"],

)

print(df.head(5))

# df2 = df.drop(df[df.CDR == NaN].index)
# df3 = pd.isna(df['CDR'])
# print(df3.head(5))

df = df[(df['CDR'].notnull()) & (df['CDR_Attempts'].notnull())]
print(df.head(5))

