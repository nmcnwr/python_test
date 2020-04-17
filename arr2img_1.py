# import pandas as pd
#
# df = pd.read_csv('arr2img_1.csv', sep=',', header=None)
# print(df.values)


import numpy as np

# ar1 = np.genfromtxt('arr2img_2.csv',delimiter=',')
# ar11 = np.transpose(ar1)


ar11 = np.genfromtxt('arr2img_globus1.csv',delimiter=',')



ar2 = (ar11 - np.min(ar11))/np.ptp(ar11) #Normalize
#print(ar1)
#print(ar2)

from PIL import Image
from matplotlib import cm



#https://stackoverflow.com/questions/10965417/how-to-convert-a-numpy-array-to-pil-image-applying-matplotlib-colormap
#colormap: https://matplotlib.org/xkcd/examples/color/colormaps_reference.html

img = Image.fromarray(np.uint8(cm.jet(ar2)*255))

# print(ar11)
#
img.save('my_1.png')
img.show()



