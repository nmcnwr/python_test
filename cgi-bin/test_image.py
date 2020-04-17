#!C:\BeelineProgFiles\python\python.exe
print("Content-Type: image/png\n\n")
print()



from PIL import Image
# im = Image.open("../lena.jpg")
# im.show()


basewidth = 300
img = Image.open('../lena.jpg')
wpercent = (basewidth/float(img.size[0]))
hsize = int((float(img.size[1])*float(wpercent)))
img = img.resize((basewidth,hsize), Image.ANTIALIAS)
#img.save('../lena.jpg')
img.show()