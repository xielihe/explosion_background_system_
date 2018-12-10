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
import numpy as np

data = np.load('XRD.npy')
print(type(data))
print(data[0])
# data.tolist()
# print(type(data))
# list 转 numpy
# np.array(a)
#
# ndarray 转 list
# a.tolist()

data2 = np.load('GCMS.npy')
print(data2)
data2 = data2.item()
print(data2['119'])
data3 = data2['119']
print(data3[0])
