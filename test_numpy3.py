import numpy as np

ar3 = np.arange(6)

print(ar3)

ar4 = ar3.reshape(2, 3)
print(ar4)

ar5 = np.transpose(ar4)
print(ar5)

ar4 = np.array([1,2,3])
ar4_square = np.square(ar4)

print('ar4_square=', ar4_square)