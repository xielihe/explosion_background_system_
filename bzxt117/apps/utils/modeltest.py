import sys
import os

#获取当前文件的路径
pwd = os.path.dirname(os.path.realpath(__file__))
#把项目的根目录加到python的根搜索路径之下
sys.path.append(pwd + "../")

#设置model的环境变量
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bishe430.settings")

import django
django.setup()

#可以直接使用model了

from user_operation.models import exploMatch

match = exploMatch()
match.exploSample_id = 1
match.exploEvi_id = 4
match.matchDegree = 88.888
match.matchType = 4
match.save()

