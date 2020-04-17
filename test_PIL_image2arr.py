

from PIL import Image
import numpy as np
im = Image.open('my_1.png')
im2arr = np.array(im) # im2arr.shape: height x width x channel

print(im2arr)
print(im2arr.shape)
#arr2im = Image.fromarray(im2arr)