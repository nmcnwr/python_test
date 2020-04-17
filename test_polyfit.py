import numpy as np
import pandas as pd

#
# revenue = [0.024911032, 0.021352313, 0.03024911, 0.017793594, 0.037366548, 0.017793594, 0.010676157, 0.026690391, 0.024911032, 0.019572954, 0.019572954, 0.713523132, 0.035587189]
# months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
# df = pd.DataFrame({'months': months, 'revenue': revenue})
#
# print(df)
#
# df[months].T.diff().fillna(0) <= 0


#
# import matplotlib.pyplot as plt
#
#
# df.plot(x='months', y='revenue', kind='scatter')
#
# plt.ylabel('some numbers')
# plt.show()



my_df = pd.DataFrame({'A':[1,2,3],'B':[2,2,2],'C':[3,1,1]})
print(my_df)

my_df['monotonic'] = my_df.T.apply(lambda x: x.is_monotonic)
my_df = my_df.rename({'monotonic': 'monotonic status'}, axis='columns')
print(my_df)
