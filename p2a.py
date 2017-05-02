#!/usr/bin/python3
from PIL import Image
import sys
charlist = ['o', '#', '$', '%', '&', '?', '*', 'o', '/', '{', '[', '(', '|',\
          '!', '^', '~', '-', '_', ':', ';', ',', '.', '`', ' ']
count = len(charlist)

def toText(image_file):
    image_file=image_file.convert("L")#转灰度
    asd =''#储存字符串
    for h in range(0,  image_file.size[1]):#hasattr
        for w in range(0, image_file.size[0]):#warning
            gray = image_file.getpixel((w,h))
            asd += charlist[int(gray/(255/(count-1)))]
            asd += '\r\n'
    return asd

def toText2(image_file):
    asd =''#储存字符串
    for h in range(0,  image_file.size[1]):#hasattr
        for w in range(0, image_file.size[0]):
            if sys.argv[1].endswith('.png'):
                r,g,b,a =image_file.getpixel((w,h))
                gray =int(r* 0.2 + g*0.3 + b*0.1 + 0.2*a)
            else:
                r,g,b =image_file.getpixel((w,h))
                gray =int(r* 0.299+g* 0.587+b* 0.114)
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
    image_file = Image.open(sys.argv[1]) # 打开图片
    if not size:
        size = image_file.size
    image_file=image_file.resize((int(size[0]),
                             int(size[1])))#调整图片大小
    print('name:{}'.format(sys.argv[1]),'size:',image_file.size[0],'x',image_file.size[1])
    print(toText2(image_file))
if __name__ == '__main__':
        main()
