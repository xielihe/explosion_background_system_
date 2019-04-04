# import sys
# import os
#
# #获取当前文件的路径
# pwd = os.path.dirname(os.path.realpath(__file__))
# #把项目的根目录加到python的根搜索路径之下
# sys.path.append(pwd + "../")
#
# #设置model的环境变量
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bishe430.settings")
#
# import django
# django.setup()
#
# #可以直接使用model了
#
# from match.models import *
#
# match = exploMatch()
# match.exploSample_id = 1
# match.exploEvi_id = 4
# match.matchDegree = 88.888
# match.matchType = 4
# match.save()
# import numpy as np
#
# data = np.load('XRD.npy')
# print(type(data))
# print(data[0])
# # data.tolist()
# # print(type(data))
# # list 转 numpy
# # np.array(a)
# #
# # ndarray 转 list
# # a.tolist()
#
# data2 = np.load('GCMS.npy')
# print(data2)
# data2 = data2.item()
# print(data2['119'])
# data3 = data2['119']
# print(data3[0])

# import re
# # 去除\r\n\t字符
# s = '_实在__%buxing'
# s1 = re.sub('[_%]', ' ', s)
# s1List = s1.split()
# print(s1List)

#  First, [download the Windows installer](http://www.reportlab.com/software/opensource/rl-toolkit/download/) and [source](https://bitbucket.org/rptlab/reportlab)
# - Then try this on Python command line:从reportlab.pdfgen导入画布，从reportlab.lib.unit进口英寸，
# cm c=canvas.canvas(‘ex.pdf’)c.drag图像(‘ar.jpg’，0，0，10*厘米，10*cm)
# c.showPage()
# c.Save()

#!/usr/bin/env python
# import os
# import sys
# from reportlab.lib.pagesizes import A4, landscape
# from reportlab.pdfgen import canvas
# ，在Python中\是转义符，\u表示其后是UNICODE编码，因此\User在这里会报错，在字符串前面加个r表示就可以了
# f_jpg = r"C:\Users\Administrator\Pictures\8.png"
# filename = ''.join(f.split('/')[-1:])[:-4]
# f_jpg = filename+'.jpg'
# print f_jpg
# def conpdf(f_jpg):
#   f_pdf = r'C:\Users\Administrator\Pictures\8.pdf'
#   (w, h) = landscape(A4)
#   c = canvas.Canvas(f_pdf, pagesize = landscape(A4))
#   c.drawString(0, 0, "你好")
#   # c.drawImage(f_jpg, 0, 0, w/2, h/2)
#   c.showPage()
#   c.save()
#   print("okkkkkkkk.")
# conpdf(f_jpg)


# from PIL import Image
# import math
# x1,x2,y1,y2 = 0
# b=math.atan2(y2-y1,x2-x1)
# jiaodu = b/math.pi*180
#
# # 读取图像
# im = Image.open(r"C:\Users\Administrator\Pictures\8.png")
# im.show()
#
# # 指定逆时针旋转的角度
# im_rotate = im.rotate(jiaodu)
# im_rotate.show()
# im_rotate.save(r"C:\Users\Administrator\Pictures\101.png")

# import subprocess
# import os
#
# from bzxt117.settings import MEDIA_ROOT,BASE_DIR
#
# path2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# main = os.path.join(path2, 'utils/test.exe')
# # main = "E:\QQPCmgr\Documents\Visual Studio 2015\Projects\test\Debug\test.exe"
# if os.path.exists(main):
#     # id是最后的return的int值，即0
#     # out是执行过程中cout的所有值，比如这里是’6\n100 200 300 400'
#     id,out= subprocess.getstatusoutput(main + r' '+"ok" + r' ' + "1"+r" "+"2"+r' '+"ok" + r' ' + "1"+r" "+"2"+r' '+"ok" + r' ' + "1"+r" "+"2"+r' '+"ok" + r' ' + "1"+r" "+"2"+r' '+"ok" + r' ' + "1"+r" "+"2"+r' '+"ok" + r' ' + "1"+r" "+"2"+r' '+"ok" + r' ' + "1"+r" "+"2"+r' '+"ok" + r' ' + "1"+r" "+"2"+r' '+"ok" + r' ' + "1"+r" "+"2"+r' '+"ok" + r' ' + "1"+r" "+"2"+r' '+"ok" + r' ' + "1"+r" "+"2"+r' '+"ok" + r' ' + "1"+r" "+"2"+r' '+"ok" + r' ' + "1"+r" "+"2")
#     print (id)
#     # print ('*'*10)
#     # print(situation)
#     print ('*'*10)
#     print (out)
# else:
#     print("0")
print ('*'*10)