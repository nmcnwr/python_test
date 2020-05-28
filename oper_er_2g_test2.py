import pandas as pd
import numpy as np

df = pd.DataFrame({
    'group': [1, 1, 2, 3, 3, 3, 4],
    'param': ['a', 'a', 'b', np.nan, 'a', 'a', np.nan]
})
print(df)

print(df.groupby('param')['group'].nunique())

df2 = pd.DataFrame({
    'cell': [1, 1, 1, 3, 3, 3, 3],
    'value': [0, 0, 2, 0, 0, 3, 6]
})
df2['above_zero'] = (df2.value > 0).map({True: 1, False: 0})
df2['above_threshold'] = (df2.value > 3).map({True: 1, False: 0})

print(df2)
agglist = {'value': [('nunique', 'nunique'), ('lambda', lambda x: x.ne(0).sum()), ('sum', sum)],
           'above_zero': [('nunique', 'nunique'), ('lambda', lambda x: x.ne(0).sum()), ('sum', sum)],
           'above_threshold': [('nunique', 'nunique'), ('lambda', lambda x: x.ne(0).sum()), ('sum', sum)],
           }

print(df2.groupby(["cell"]).agg(agglist))
# print(df2.groupby('cell')['value'].nunique())

