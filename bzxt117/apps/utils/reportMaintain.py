# import sys
# import os
# from django.db.models import Q
#
# #获取当前文件的路径
# pwd = os.path.dirname(os.path.realpath(__file__))
# #把项目的根目录加到python的根搜索路径之下
# sys.path.append(pwd + "../")
#
# #设置model的环境变量
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bzxt117.settings")
#
# import django
# django.setup()
#
# #可以直接使用model了
# from apps.match.models import *
# def reportMaintain(type):
# # type = 0表示是炸药的，type= 1表示是爆炸装置的成分，type = 2表示是爆炸装置的形态
#     if type == 0:
#         # 取出炸药的综合匹配表中的所有物证序号列表
#         eviList = exploSynMatch.objects.values_list('exploEvi', flat=True)
#         for evi in eviList:
#             # 对每一个综合表中的物证，在报告表中查询或创建对应的记录
#             match = exploReportMatch.objects.get_or_create(exploEvi_id = evi)
#             # 如果被核准过，此条记录不变
#             if (Q(match.isCheck == 2) | Q(match.isExpertCheck == 2)):
#                 continue
#             #  如果没被核准过，将报告表的记录保持为综合表的得分最大值
#             else:
#                 highestScore = exploSynMatch.objects.filter(exploEvi_id = evi).order_by('Score')[0]
#                 match.exploSample = highestScore.exploSample
#                 match.Score = highestScore.Score
#                 match.save()
#     elif type == 1:
#          # 取爆炸装置的，爆炸装置分两种，成分和形态
#          # 成分：
#          devList = devCompMatch.objects.values_list('devEvi', flat=True)
#          for dev in devList:
#              match = devSynMatch.objects.get_or_create(devEviComp = dev)
#              if(Q(match.isCheckComp == 2)|Q(match.isExpertCheckComp == 2)):
#                  continue
#              else:
#                  highestScore = devCompMatch.objects.filter(devEvi_id = dev).order_by('Score')[0]
#                  match.devPartSampleComp = highestScore.devPartSample
#                  match.ScoreComp = highestScore.Score
#                  match.save()
#     elif type == 2:
# #         爆炸装置形态
#           pass


