import numpy as np

ar1 = np.ones([5,5])
print(ar1)

ar2 = np.zeros([3,3])
print(ar2)

ar1[1:-1,1:-1] = ar2


ar1[2,2] = 9
print(ar1)

ar1_max = np.max(ar1)
ar1_mean = np.mean(ar1)
ar1_sum = np.sum(ar1)

print(ar1_max, ar1_mean, ar1_sum)

ar1_max_axis0 = ar1.max(axis=0)
print(ar1_max_axis0)
