from PIL import Image
import numpy as np

w, h = 2, 2
data = np.zeros((h, w, 3), dtype=np.uint8)
data[0:1, 0:2] = [255, 0, 0] # red patch in upper left
data[1:2, 0:2] = [0, 0, 255] # red patch in upper left
data[1, 1] = [0, 255, 0]
print(data)
img = Image.fromarray(data, 'RGB')
img.save('my.png')
img.show()