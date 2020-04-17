import pandas as pd
import numpy as np
import scipy.stats



#df = pd.DataFrame(np.random.randn(10, 4), columns=list('ABCD'))

# list2 = [42,	33, 47, 39, 38, 46, 44, 164, 2204, 2284, 2286, 2151, 2495]
list2 = [1,2,3,4,3,2,1,6]
df = pd.DataFrame([list2])
print(df)

axisvalues = list(range(1, len(df.columns)+1))

# axisvalues = [1,2,3,4]


def calc_slope(row):
    a = scipy.stats.linregress(row, y=axisvalues)
    return a.slope

df["slope"] = df.apply(calc_slope, axis=1)


print(df)

