#!/usr/bin/python3
#encoding=utf-8
from PIL import Image
import sys
charlist = ['o', '#', '$', '%', '&', '?', '*', 'o', '/', '{', '[', '(', '|',\
          '!', '^', '~', '-', '_', ':', ';', ',', '.', '`', ' ']
count = len(charlist)

def toText(image_file):
    image_file=image_file.convert("L")
    asd =''
    for h in range(0,  image_file.size[1]):
        for w in range(0, image_file.size[0]):
            gray = image_file.getpixel((w,h))
            asd += charlist[int(gray/(255/(count-1)))]
            asd += '\r\n'
    return asd

def toText2(image_file):
    asd =''
    for h in range(0,  image_file.size[1]):
        for w in range(0, image_file.size[0]):
            color = image_file.getpixel((w,h))
            if color.__len__() == 4:
                r, g, b, a = color
                gray = int(r* 0.2+g* 0.5+b* 0.1+0.2*a)
            else:
                r, g, b = color
                gray = int(r* 0.299+g* 0.587+b* 0.114)
            asd += charlist[int(gray/(255/(count-1)))]
        asd += '\r\n'
    return asd

def main():
    size = []
    if sys.argv.__len__() < 2:
        print("Usage:{0} ImageName size\n\tExample: {1} exa.png 50x50".format(sys.argv[0],sys.argv[0]))
        return 0
    if sys.argv.__len__() == 3:
        size = sys.argv[2].split('x')
        size = [int(i) for i in size]
    image_file = Image.open(sys.argv[1])
    if not size:
        size = image_file.size
    image_file=image_file.resize((int(size[0]),
                             int(size[1])))
    print('name:{}'.format(sys.argv[1]),'size:',image_file.size[0],'x',image_file.size[1])
    print(toText2(image_file))
if __name__ == '__main__':
        main()
