from flask import Flask, send_from_directory
from PIL import Image, ImageDraw, ImageFont
from hashlib import md5

# make Flag File
testFlag = 'flag{' + md5().hexdigest() + '}'
img = Image.open('./backJpeg.jpg')
w, h = img.size
imgdraw = ImageDraw.Draw(img)
imgdraw.text((w / 10, h / 3), str(testFlag), fill='#000000')
print('FLAG: ' + testFlag)
print('IMG SIZE x: ' + str(w) + ' y: ' + str(h))
img = img.rotate(90, expand = 1)
img.save('./flagJpeg.jpg')

# Write the flag in the picture 
flagImg = Image.open('./flagJpeg.jpg')
hiddenImg = Image.open('./hiddenJpeg.jpg')
width = flagImg.size[0]
height = flagImg.size[1]
flagImg = flagImg.convert('RGB')
array = []
for i in range(width):
     for j in range(height):
          r, g, b = flagImg.getpixel((i,j))
          rgb = (r, g, b)
          hiddenImg.putpixel(((i+2) * 19,(j + 62) * 11), rgb)
hiddenImg.save('flag.png')

# Start Web Service
app = Flask(__name__)
@app.route('/', methods=['GET'])
def displayFlag():
     return send_from_directory('./','flag.png')

if __name__ == '__main__':
   app.run(port=8088)

# from PIL import Image
# img = Image.open('./flag - 副本.png')
# pic = Image.new('RGB',(1000,1000), (255,255,255))
# nx = [0,49,98,147,196,245,294,343,392,441,490,539,588,637,686,735,784,833,882,931,980,1029,1078,1127,1176,1225,1274,1323,1372,1421,1470,1519,1568,1617,1666,1715,1764,1813,1862,1911,1960,2009,2058,2107,2156,2205,2254,2303,2352,2401,2450,2499,2548,2597,2646,2695,2744,2793,2842,2891,2940,2989,3038,3087,3136,3185,3234,3283,3332,3381,3430,3479,3528,3577,3626,3675,3724,3773,3822,3871,3920,3969,4018,4067,4116,4165,4214,4263,4312,4361,4410,4459,4508,4557,4606,4655,4704,4753,4802,4851,4900,4949,4998,5047,5096,5145,5194,5243,5292,5341,5390,5439,5488,5537,5586,5635,5684,5733,5782,5831,5880,5929,5978,6027,6076,6125,6174,6223,6272,6321,6370,6419,6468]
# ny = [0,32,64,96,128,160,192,224,256,288,320,352,384,416,448,480,512,544,576,608,640,672,704,736,768,800,832,864,896,928,960,992,1024,1056,1088,1120,1152,1184,1216,1248,1280,1312,1344,1376,1408,1440,1472,1504,1536,1568,1600,1632,1664,1696,1728,1760,1792,1824,1856,1888,1920,1952,1984,2016,2048,2080,2112,2144,2176,2208,2240,2272,2304,2336,2368,2400,2432,2464,2496,2528,2560,2592,2624,2656,2688,2720,2752,2784,2816,2848,2880,2912,2944,2976,3008,3040,3072,3104,3136,3168,3200,3232,3264,3296,3328,3360,3392,3424,3456,3488,3520,3552,3584,3616,3648,3680,3712,3744,3776,3808,3840,3872,3904,3936,3968,4000,4032,4064,4096,4128,4160,4192,4224,4256,4288,4320,4352,4384,4416,4448,4480,4512,4544,4576,4608,4640,4672,4704,4736,4768,4800,4832,4864,4896,4928,4960,4992,5024,5056,5088,5120,5152,5184,5216,5248,5280,5312,5344,5376,5408,5440,5472,5504,5536,5568,5600,5632,5664,5696,5728,5760,5792,5824,5856,5888,5920,5952,5984,6016,6048,6080,6112,6144,6176,6208,6240,6272,6304,6336,6368,6400,6432,6464]
# x,y = img.size
# for i in range(120):
#      for j in range(200):
#           t = img.getpixel((nx[i],ny[j]))
#           pic.putpixel((i,j),(t))
# pic.show()

# from PIL import Image
# import numpy as np
# img = Image.open(r'./flag.png')
# w, h = img.size
# x = np.arange(220, 8428, 44)
# y = np.arange(344, 5984, 86)
# print(y)
# res = Image.new('RGB', (100, 100))
# for i in range(86):
#      for j in range(25):
#           t = img.getpixel((x[i],y[j]))
#           res.putpixel((i,j),(t))
#           # p = img.getpixel(((x-220)//86,(y-344)//44))
#           # p = img.getpixel((w[(x-220)//86],y[(y-344)//44]))

# res.save('output.png')

# from PIL import Image
# im = Image.open('./aa.png')
# background = Image.open('./ez.jpg')
# width = im.size[0]
# height = im.size[1]
# im = im.convert('RGB')
# array = []
# for i in range(width):
#      for j in range(height):
#           r, g, b = im.getpixel((i,j))
#           rgb = (r, g, b)
#           background.putpixel(((i+10)*49,(j+3)*32), rgb)
# background.show()
# background.save('flag.png')


# from PIL import Image
# water = Image.open('./flag1.png')
# # wx,wy = water.size
# wx = water.size[0]
# wy = water.size[1]
# pix = water.load()
# background = Image.open('./background.jpg')
# x,y = background.size
# for i in range(wx):
#      for j in range(wy):
#           # tx = (i // 10) * 5
#           # ty = (j // 10) * 5
#           r, g, b = pix[i, j]
#           print(r,g,b)
#           # background.putpixel((tx+10,ty+20), (r,g,b))
# # background.show()