import pandas as pd

df = pd.read_csv('Gogol_settings/adam_threshold.tbl', delimiter=';', decimal='.', header=0)
print(df.head(5))
df2 = df[(df['KL_VENDOR'] == 'Er') & (df['KL_TECH'] == '2G')]


