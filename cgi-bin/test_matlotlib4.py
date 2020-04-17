import numpy as np
import matplotlib.pyplot as plt

t = np.arange(0, 1 + 0.01, 0.01)
s = np.arange(0, 1 + 0.01, 0.01)

t[41:60] = np.nan

print('t=', t)
print('s=', s)

plt.subplot(2, 1, 1)
plt.plot(t, s, '-', lw=2)

plt.xlabel('time (s)')
plt.ylabel('voltage (mV)')
plt.title('A sine wave with a gap of NaNs between 0.4 and 0.6')
plt.grid(True)



plt.tight_layout()
plt.show()