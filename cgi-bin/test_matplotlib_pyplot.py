import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
np.random.seed(1977)


x = np.random.normal(0, 1, 1000).cumsum()




# Set every third value to NaN
x[::3] = np.nan

# Set a few bigger gaps...
x[20:100], x[200:300], x[400:450] = np.nan, np.nan, np.nan

# Use pandas with a limited forward fill
# You may want to adjust the `limit` here. This will fill 2 nan gaps.
filled = pd.Series(x).fillna(limit=2, method='ffill')

# Let's plot the results
fig, axes = plt.subplots(nrows=2, sharex=True)
axes[0].plot(x, color='lightblue')
axes[1].plot(filled, color='lightblue')

axes[0].set(ylabel='Original Data')
axes[1].set(ylabel='Filled Data')

plt.show()