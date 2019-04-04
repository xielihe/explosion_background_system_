from django.shortcuts import render
from rest_framework import serializers
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from rest_framework.views import APIView
from django.db.models import Q
import json
import re
from rest_framework.pagination import PageNumberPagination
#导入`connection`
from django.db import connection
from itertools import chain

from apps.match.serializers import *
from utils.permissions import *
from apps.match.models import *
from apps.evi.models import *
from apps.sample.serializers import *
from utils.CalculateSim import CalculateSimilarity
from utils.ComScore import ComScore
from utils.PCB import *
from django_filters.rest_framework import DjangoFilterBackend


class MyPageNumberPagination(PageNumberPagination):
    # 指定这一页有多少个
    page_size=10  #默认两个

    page_size_query_param = 'page_size'  #传一个size参数 一页显示多少  http://127.0.0.1:8000/wordSelect/?page=1&page_size=3
    # 代表多少页
    max_page_size = 10  #一页显示最大5个
    # 代表多少页
    # ？page = 2&page_size=20
    page_query_param = 'page'  #页码

# 语义筛选接口
class wordSelect(APIView):
    def post(self,request):
        Color = request.POST["Color"]
        Shape = request.POST["Shape"]
        Material = request.POST["Material"]
        thickness = request.POST["thickness"]
        keyWords = request.POST["keyWords"]
        devEviId = int(request.POST["devEviId"])
        # 待语义匹配的物证对象
        devEviSelect = devEvi.objects.get(id = devEviId)


        #创建分页对象
        pg = MyPageNumberPagination()
        sampleQuery = devPartSample.objects.all()
        finalQuery = devPartSample.objects.none()
        # 建一个空的queryset
        if Color == 'True':
            sampleQuery = sampleQuery.filter(Color = devEviSelect.Color)
        if Shape == 'True':
            sampleQuery = sampleQuery.filter(Shape=devEviSelect.Shape)
        if Material == 'True':
            sampleQuery = sampleQuery.filter(Material = devEviSelect.Material)
        if thickness == 'True':
            sampleQuery = sampleQuery.filter(thickness = devEviSelect.thickness)
        keyWordList = keyWords.split()
        sampleQueryRES = sampleQuery
        for keyWord in keyWordList:
            querySetN = devPartSample.objects.none()
            cursor = connection.cursor()  # 要想使用sql原生语句，必须用到execute()函数 #然后在里面写入sql原生语句
            # concat(Origin,Factory,Model,Logo,function,note) 不能用，因为concat是连接字段，是把所有字段连在一起作为一个，因此那种_的就不适用，不能简单用concat来进行对所有字段的搜索。
            # 所以只能用or连接。
            # ps：CONCAT()可以连接一个或者多个字符串,CONCAT_WS()可以添加分割符参数。
            select_words = 'select * from sample_devpartsample where Origin like "%s" or Factory like "%s" or Model like "%s" or Logo like "%s" or function like "%s"'% (keyWord,keyWord,keyWord,keyWord,keyWord)
            cursor.execute(select_words)
            # 使用一个变量来接收查询到的数据，WHERE note LIKE keyWord
            # fetchall（）返回查询到的所有数据
            # sampleQueryRES = cursor.fetchall()
            tempResults = cursor.fetchall()
            querySetN = sampleQueryRES.filter(id__in=[tempResult[0] for tempResult in tempResults])
            keyWord1 = re.sub('[_%]', ' ',keyWord)
            keyWordList1s = keyWord1.split()
            for keyWordList1 in keyWordList1s:
                tempQuery = sampleQueryRES.filter(note__icontains=keyWordList1)
                querySetN =querySetN|tempQuery
            finalQuery =querySetN|finalQuery
            # for tempResult in tempResults:
            #     tempSampleQuery = sampleQueryRES.filter(id = tempResult[0])
            #     if len(tempSampleQuery) > 0:
            #         querySetN.append(tempSampleQuery)
        #     不用去重，因为合并的时候取或就自动去重了
        # finalQuery = finalQuery.values('id').distinct().order_by('id')

        #  此时为一个tuple的列表，要使用id进行filter可以方便将list重新转化为Queryset

        # for keyWord in keyWordList:
        #     sampleQueryRES = sampleQueryRES.filter(Q(Origin__icontains=keyWord)|Q(Factory__icontains=keyWord)|Q(Model__icontains=keyWord)
        #                                      |Q(Logo__icontains=keyWord)|Q(function__icontains=keyWord)|Q(note__icontains=keyWord))

        #在数据库中获取分页数据
        pager_roles = pg.paginate_queryset(queryset=finalQuery, request=request,view=self)
        #对分页数据进行序列化
        ser = PagerSerialiser(instance=pager_roles, many=True)

        return pg.get_paginated_response(ser.data)  # 返回上一页或者下一页

        # sampleJSON = devPartSampleSerializer(instance=sampleQueryRES, many=True)
        # samples = json.dumps(sampleJSON.data, ensure_ascii=False)
        #
        # return Response({
        #     "result": samples,
        # }, status=status.HTTP_201_CREATED)

# 开始比对接口
class startMatch(APIView):
    # 1：exploMatchFTIR，2：exploMatchRaman，3：exploMatchXRD，4：exploMatchXRF，5：exploMatchGCMS，
    # 6：devMatchFTIR，7:devMatchRaman,8:devMatchXRF,9:PCBImgMatch,10:oPartImgMatch,11:logoImgMatch
    # 12:devShapeMatch
    # get方法是请求在url中的参数的，而post是请求在request中的参数的
    def post(self,request):
        # 此时type等都是str类型哦
        type = int(request.POST["type"])
        eviFileId = int(request.POST["eviFileId"])

        # 没法直接用type当成类去做filter
        # result = type.objects.all()
        # python没有switch case
        #创建分页对象
        pg = MyPageNumberPagination()
        resultDict = {}

        # Create your tests here.
        def gci(filepath, fileList):
            # 遍历filepath下所有文件，包括子目录
            if os.path.exists(filepath) == False:
                raise APIException("想要遍历的文件夹路径不存在")
            files = os.listdir(filepath)
            for fi in files:
                fi_d = os.path.join(filepath, fi)
                fileList.append(fi_d)

        # 生成综合匹配的各自匹配的结果列表
        # type = 1/2,对应炸药和爆炸装置，id即为物证的id，comDict是那个列表
        def comDict(type, eviId, comDictDict):
            if type == 1:
                FTIRs = []
                RAMANs = []
                XRDs = []
                XRFs = []
                GCMSs = []

                comListFTIR = []
                comListRAMAN = []
                comListXRD = []
                comListXRF = []
                comListGCMS = []

                FTIRs = exploMatchFTIR.objects.filter(exploEviFTIRTestFile__exploEviId=eviId)
                for FTIR in FTIRs:
                    idScoreList = []
                    idScoreList.append(FTIR.exploSampleFTIRTestFile.exploSampleFTIR.exploSample_id)
                    idScoreList.append(FTIR.Score)
                    comListFTIR.append(idScoreList)
                comDictDict["FTIR"] = comListFTIR

                RAMANs = exploMatchRaman.objects.filter(exploEviRamanTestFile__exploEviId=eviId)
                for RAMAN in RAMANs:
                    idScoreList = []
                    idScoreList.append(RAMAN.exploSampleRamanTestFile.exploSampleRaman.exploSample_id)
                    idScoreList.append(RAMAN.Score)
                    comListRAMAN.append(idScoreList)
                comDictDict["RAMAN"] = comListRAMAN

                XRDs = exploMatchXRD.objects.filter(exploEviXRDTestFile__exploEviId=eviId)
                for XRD in XRDs:
                    idScoreList = []
                    idScoreList.append(XRD.exploSampleXRDTestFile.exploSampleXRD.exploSample_id)
                    idScoreList.append(XRD.Score)
                    comListXRD.append(idScoreList)
                comDictDict["XRD"] = comListXRD

                XRFs = exploMatchXRF.objects.filter(exploEviXRFTestFile__exploEviId=eviId)
                for XRF in XRFs:
                    idScoreList = []
                    idScoreList.append(XRF.exploSampleXRFTestFile.exploSampleXRF.exploSample_id)
                    idScoreList.append(XRF.averScore)
                    comListXRF.append(idScoreList)
                comDictDict["XRF"] = comListXRF

                GCMSs = exploMatchGCMS.objects.filter(exploEviGCMSFile__exploEviId=eviId)
                for GCMS in GCMSs:
                    idScoreList = []
                    idScoreList.append(GCMS.exploSampleGCMSFile.exploSampleGCMS.exploSample_id)
                    idScoreList.append(GCMS.Score)
                    comListGCMS.append(idScoreList)
                comDictDict["GCMS"] = comListGCMS
            elif type == 2:
                FTIRs = []
                RAMANs = []
                XRFs = []

                comListFTIR = []
                comListRAMAN = []
                comListXRF = []

                FTIRs = devMatchFTIR.objects.filter(devEviFTIRTestFile__devEviId=eviId)
                for FTIR in FTIRs:
                    idScoreList = []
                    idScoreList.append(FTIR.devPartSampleFTIRTestFile.devPartSampleFTIR.devPartSample_id)
                    idScoreList.append(FTIR.Score)
                    comListFTIR.append(idScoreList)
                comDictDict["FTIR"] = comListFTIR

                RAMANs = devMatchRaman.objects.filter(devEviRamanTestFile__devEviId=eviId)
                for RAMAN in RAMANs:
                    idScoreList = []
                    idScoreList.append(RAMAN.devPartSampleRamanTestFile.devPartSampleRaman.devPartSample_id)
                    idScoreList.append(RAMAN.Score)
                    comListRAMAN.append(idScoreList)
                comDictDict["RAMAN"] = comListRAMAN

                XRFs = devMatchXRF.objects.filter(devEviXRFTestFile__devEviId=eviId)
                for XRF in XRFs:
                    idScoreList = []
                    idScoreList.append(XRF.devPartSampleXRFTestFile.devPartSampleXRF.devPartSample_id)
                    idScoreList.append(XRF.averScore)
                    comListXRF.append(idScoreList)
                comDictDict["XRF"] = comListXRF

        if type == 1:
            sampleList = []
            score_dict = {}
            score_dictSim = {}
            result_dict = {}
            querysetList = []
            #     输入参数: file_type - - 检测方法（‘GCMS’，‘XRD’，‘XRF’，‘FTIR’，‘RAMAN’）
            #     evi_sample_dir - - 物证样本路径（更新时为常见样本路径）
            #     common_database - - 标准样本数据库的路径列表，List类型
            #     score_dict - - 空字典，以存储结果
            # 输出参数: score_dict
            # 返回值: 0 —— 成功，其他数值 —— 失败

            # 容错
            if exploEviFTIRTestFile.objects.filter(id=eviFileId).count() != 1:
                raise APIException("爆炸物证文件id输入错误，无法找到对应文件")
            gci(os.path.join(MEDIA_ROOT, "file/exploSampleFTIRTestFile/handled"), sampleList)
            eviFile = exploEviFTIRTestFile.objects.get(id=eviFileId)

            result = CalculateSimilarity('FTIR', os.path.join(MEDIA_ROOT, str(eviFile.txtHandledURL)), sampleList,
                                         score_dict)
            if result != '0':
                raise APIException("物证文件与样本比对程序CalculateSimilarity出错")
            for id, score in score_dict.items():
                match = exploMatchFTIR.objects.get_or_create(exploEviFTIRTestFile_id=eviFileId, exploSampleFTIRTestFile_id=id)
                matchObj = match[0]
                matchObj.Score = score
                matchObj.save()
                querysetList.append(matchObj)

            # # #     输入参数: result - - 得分字典
            # # #     格式如
            # # #     {FTIR: [[id, score], [id, score], ...],
            # # #      XRD: [[id, score], [id, score], ...],
            # # #      XRF: [[id, score], [id, score], ...], ...
            # # #      }
            # # # 输出参数: score_dict
            # # # 返回值: 0 —— 成功，其他数值 —— 失败
            comDict(1, eviFile.exploEviId, score_dictSim)

            result = ComScore(score_dictSim, result_dict)
            if result != '0':
                raise APIException("物证与各个样本的综合得分程序 ComScore出错")
            resultDict = result_dict
            for id, score in result_dict.items():
                match = exploSynMatch.objects.get_or_create(exploEvi_id=eviFile.exploEviId, exploSample_id=id)
                matchObj = match[0]
                matchObj.Score = score
                matchObj.save()
            pager_roles = pg.paginate_queryset(queryset=querysetList, request=request,view=self)
            ser = exploMatchFTIRSerializer(instance=pager_roles, many=True)
            return pg.get_paginated_response(ser.data)  # 返回上一页或者下一页
        #     returnResult = comDict(result, score_dictSim)
        #     # # 如果物证更新后再次要求匹配或者是重复请求，先删除，在做匹配
        #     # results = exploMatchFTIR.objects.filter(exploEviFTIRTestFile_id = eviFileId)
        #     # for result in results:
        #     #     result.delete()
        #     #调用FTIR的匹配函数,传入参数为物证id，注意要同时维护综合表：
        #     # 不管是先全删除还是直接存入匹配数据，都是全部做完再操作综合表：全删，重做综合表
        #         # # exploSyn_Match不能重名exploSynMatch！！
        #         # exploSyn_Match = exploSynMatch()
        #         # exploSyn_Match.exploEvi_id = eviId
        #         # exploSyn_Match.exploSample_id = 1
        #         # exploSyn_Match.Score = 100
        #         # # 外键空值的时候可以赋值为None,代表数据库中的NULL，且序列化的时候也不会出问题的~
        #         # exploSyn_Match.checkHandle = None
        #         # exploSyn_Match.expertHandle_id = 2
        #         # exploSyn_Match.save()
        elif type == 2:
            #     exploMatchRaman
            sampleList = []
            score_dict = {}
            score_dictSim = {}
            result_dict = {}
            querysetList = []

            # 容错
            if exploEviRamanTestFile.objects.filter(id=eviFileId).count() != 1:
                raise APIException("爆炸物证文件id输入错误，无法找到对应文件")

            gci(os.path.join(MEDIA_ROOT, "file/exploSampleRamanTestFile/handled"), sampleList)
            eviFile = exploEviRamanTestFile.objects.get(id=eviFileId)

            result = CalculateSimilarity('RAMAN', os.path.join(MEDIA_ROOT, str(eviFile.txtHandledURL)), sampleList,
                                         score_dict)
            if result != '0':
                raise APIException("物证文件与样本比对程序CalculateSimilarity出错")
            for id, score in score_dict.items():
                match = exploMatchRaman.objects.get_or_create(exploEviRamanTestFile_id=eviFileId,
                                                              exploSampleRamanTestFile_id=id)
                matchObj = match[0]
                matchObj.Score = score
                matchObj.save()
                querysetList.append(matchObj)

            comDict(1, eviFile.exploEviId, score_dictSim)

            result = ComScore(score_dictSim, result_dict)
            if result != '0':
                raise APIException("物证与各个样本的综合得分程序 ComScore出错")
            resultDict = result_dict
            for id, score in result_dict.items():
                match = exploSynMatch.objects.get_or_create(exploEvi_id=eviFile.exploEviId, exploSample_id=id)
                matchObj = match[0]
                matchObj.Score = score
                matchObj.save()
            pager_roles = pg.paginate_queryset(queryset=querysetList, request=request,view=self)
            ser = exploMatchRamanSerializer(instance=pager_roles, many=True)
            return pg.get_paginated_response(ser.data)  # 返回上一页或者下一页
        elif type == 3:
            # exploMatchXRD
            sampleList = []
            score_dict = {}
            score_dictSim = {}
            result_dict = {}
            querysetList = []

            # 容错
            if exploEviXRDTestFile.objects.filter(id=eviFileId).count() != 1:
                raise APIException("爆炸物证文件id输入错误，无法找到对应文件")

            gci(os.path.join(MEDIA_ROOT, "file/exploSampleXRDTestFile/handled"), sampleList)
            eviFile = exploEviXRDTestFile.objects.get(id=eviFileId)

            result = CalculateSimilarity('XRD', os.path.join(MEDIA_ROOT, str(eviFile.txtHandledURL)), sampleList,
                                         score_dict)
            if result != '0':
                raise APIException("物证文件与样本比对程序CalculateSimilarity出错")
            for id, score in score_dict.items():
                match = exploMatchXRD.objects.get_or_create(exploEviXRDTestFile_id=eviFileId,
                                                            exploSampleXRDTestFile_id=id)
                matchObj = match[0]
                matchObj.Score = score
                matchObj.save()
                querysetList.append(matchObj)

            comDict(1, eviFile.exploEviId, score_dictSim)

            result = ComScore(score_dictSim, result_dict)
            if result != '0':
                raise APIException("物证与各个样本的综合得分程序 ComScore出错")
            resultDict = result_dict
            for id, score in result_dict.items():
                match = exploSynMatch.objects.get_or_create(exploEvi_id=eviFile.exploEviId, exploSample_id=id)
                matchObj = match[0]
                matchObj.Score = score
                matchObj.save()
            pager_roles = pg.paginate_queryset(queryset=querysetList, request=request,view=self)
            ser = exploMatchXRDSerializer(instance=pager_roles, many=True)
            return pg.get_paginated_response(ser.data)  # 返回上一页或者下一页
        elif type == 4:
            # exploMatchXRF
            sampleList = []
            score_dict = {}
            score_dictSim = {}
            result_dict = {}
            querysetList = []

            # 容错
            if exploEviXRFTestFile.objects.filter(id=eviFileId).count() != 1:
                raise APIException("爆炸物证文件id输入错误，无法找到对应文件")

            gci(os.path.join(MEDIA_ROOT, "file/exploSampleXRFTestFile/handled"), sampleList)
            eviFile = exploEviXRFTestFile.objects.get(id=eviFileId)

            result = CalculateSimilarity('XRF', os.path.join(MEDIA_ROOT, str(eviFile.handledURL)), sampleList,
                                         score_dict)

            if result != '0':
                raise APIException("物证文件与样本比对程序CalculateSimilarity出错")

            for id, score in score_dict.items():
                match = exploMatchXRF.objects.get_or_create(exploEviXRFTestFile_id=eviFileId,
                                                            exploSampleXRFTestFile_id=id)
                matchObj = match[0]
                matchObj.averScore = score
                matchObj.save()
                querysetList.append(matchObj)

            comDict(1, eviFile.exploEviId, score_dictSim)

            result = ComScore(score_dictSim, result_dict)
            if result != '0':
                raise APIException("物证与各个样本的综合得分程序 ComScore出错")
            resultDict = result_dict
            for id, score in result_dict.items():
                match = exploSynMatch.objects.get_or_create(exploEvi_id=eviFile.exploEviId, exploSample_id=id)
                matchObj = match[0]
                matchObj.Score = score
                matchObj.save()
            pager_roles = pg.paginate_queryset(queryset=querysetList, request=request,view=self)
            ser = exploMatchXRFSerializer(instance=pager_roles, many=True)
            return pg.get_paginated_response(ser.data)  # 返回上一页或者下一页
        elif type == 5:
            # exploMatchGCMS
            sampleList = []
            score_dict = {}
            score_dictSim = {}
            result_dict = {}
            querysetList = []

            # 容错
            if exploEviGCMSFile.objects.filter(id=eviFileId).count() != 1:
                raise APIException("爆炸物证文件id输入错误，无法找到对应文件")

            gci(os.path.join(MEDIA_ROOT, "file/exploSampleGCMSTestFile/handled"), sampleList)
            eviFile = exploEviGCMSFile.objects.get(id=eviFileId)

            result = CalculateSimilarity('GCMS', os.path.join(MEDIA_ROOT, str(eviFile.txtHandledURL)), sampleList,
                                         score_dict)
            if result != '0':
                raise APIException("物证文件与样本比对程序CalculateSimilarity出错")
            for id, score in score_dict.items():
                match = exploMatchGCMS.objects.get_or_create(exploEviGCMSFile_id=eviFileId,
                                                             exploSampleGCMSFile_id=id)
                matchObj = match[0]
                matchObj.Score = score['score']
                matchObj.msName = score['evi_MS']
                matchObj.save()
                querysetList.append(matchObj)

            comDict(1, eviFile.exploEviId, score_dictSim)


            result = ComScore(score_dictSim, result_dict)
            if result != '0':
                raise APIException("物证与各个样本的综合得分程序 ComScore出错")
            resultDict = result_dict
            for id, score in result_dict.items():
                match = exploSynMatch.objects.get_or_create(exploEvi_id=eviFile.exploEviId, exploSample_id=id)
                matchObj = match[0]
                matchObj.Score = score
                matchObj.save()
            pager_roles = pg.paginate_queryset(queryset=querysetList, request=request,view=self)
            ser = exploMatchGCMSSerializer(instance=pager_roles, many=True)
            return pg.get_paginated_response(ser.data)  # 返回上一页或者下一页
        elif type == 6:
            # devMatchFTIR
            sampleList = []
            score_dict = {}
            score_dictSim = {}
            result_dict = {}
            querysetList = []

            # 容错
            if devEviFTIRTestFile.objects.filter(id=eviFileId).count() != 1:
                raise APIException("爆炸物证文件id输入错误，无法找到对应文件")

            gci(os.path.join(MEDIA_ROOT, "file/devPartSampleFTIRTestFile/handled"), sampleList)
            eviFile = devEviFTIRTestFile.objects.get(id=eviFileId)

            result = CalculateSimilarity('FTIR', os.path.join(MEDIA_ROOT, str(eviFile.txtHandledURL)), sampleList,
                                         score_dict)
            if result != '0':
                raise APIException("物证文件与样本比对程序CalculateSimilarity出错")
            for id, score in score_dict.items():
                match = devMatchFTIR.objects.get_or_create(devEviFTIRTestFile_id=eviFileId,
                                                           devPartSampleFTIRTestFile_id=id)
                matchObj = match[0]
                matchObj.Score = score
                matchObj.save()
                querysetList.append(matchObj)

            comDict(2, eviFile.devEviFTIR.devEvi_id, score_dictSim)
            result =  ComScore(score_dictSim, result_dict)
            if result != '0':
                raise APIException("物证与各个样本的综合得分程序 ComScore出错")
            resultDict = result_dict
            for id, score in result_dict.items():
                match = devCompMatch.objects.get_or_create(devEvi_id=eviFile.devEviId, devPartSample_id=id)
                matchObj = match[0]
                matchObj.Score = score
                matchObj.save()
            pager_roles = pg.paginate_queryset(queryset=querysetList, request=request,view=self)
            ser = devMatchFTIRSerializer(instance=pager_roles, many=True)
            return pg.get_paginated_response(ser.data)  # 返回上一页或者下一页
        elif type == 7:
            # devMatchRaman
            sampleList = []
            score_dict = {}
            score_dictSim = {}
            result_dict = {}
            querysetList = []

            # 容错
            if devEviRamanTestFile.objects.filter(id=eviFileId).count() != 1:
                raise APIException("爆炸物证文件id输入错误，无法找到对应文件")

            gci(os.path.join(MEDIA_ROOT, "file/devPartSampleRamanTestFile/handled"), sampleList)
            eviFile = devEviRamanTestFile.objects.get(id=eviFileId)

            result = CalculateSimilarity('RAMAN', os.path.join(MEDIA_ROOT, str(eviFile.txtHandledURL)), sampleList,
                                         score_dict)
            if result != '0':
                raise APIException("物证文件与样本比对程序CalculateSimilarity出错")
            for id, score in score_dict.items():
                match = devMatchRaman.objects.get_or_create(devEviRamanTestFile_id=eviFileId,
                                                            devPartSampleRamanTestFile_id=id)
                matchObj = match[0]
                matchObj.Score = score
                matchObj.save()
                querysetList.append(matchObj)

            comDict(2, eviFile.devEviRaman.devEvi_id, score_dictSim)
            result =  ComScore(score_dictSim, result_dict)
            if result != '0':
                raise APIException("物证与各个样本的综合得分程序 ComScore出错")
            resultDict = result_dict
            for id, score in result_dict.items():
                match = devCompMatch.objects.get_or_create(devEvi_id=eviFile.devEviId, devPartSample_id=id)
                matchObj = match[0]
                matchObj.Score = score
                matchObj.save()
            pager_roles = pg.paginate_queryset(queryset=querysetList, request=request,view=self)
            ser = devMatchRamanSerializer(instance=pager_roles, many=True)
            return pg.get_paginated_response(ser.data)  # 返回上一页或者下一页
        elif type == 8:
            # devMatchXRF,
            sampleList = []
            score_dict = {}
            score_dictSim = {}
            result_dict = {}
            querysetList = []

            # 容错
            if devEviXRFTestFile.objects.filter(id=eviFileId).count() != 1:
                raise APIException("爆炸物证文件id输入错误，无法找到对应文件")

            gci(os.path.join(MEDIA_ROOT, "file/devPartSampleXRFTestFile/handled"), sampleList)
            eviFile = devEviXRFTestFile.objects.get(id=eviFileId)

            result = CalculateSimilarity('XRF', os.path.join(MEDIA_ROOT, str(eviFile.handledURL)), sampleList,
                                         score_dict)
            if result != '0':
                raise APIException("物证文件与样本比对程序CalculateSimilarity出错")

            for id, score in score_dict.items():
                match = devMatchXRF.objects.get_or_create(devEviXRFTestFile_id=eviFileId,
                                                          devPartSampleXRFTestFile_id=id)
                matchObj = match[0]
                matchObj.averScore = score
                matchObj.save()
                querysetList.append(matchObj)

            comDict(2, eviFile.devEviXRF.devEvi_id, score_dictSim)
            result =  ComScore(score_dictSim, result_dict)
            if result != '0':
                raise APIException("物证与各个样本的综合得分程序 ComScore出错")
            resultDict = result_dict
            for id, score in result_dict.items():
                match = devCompMatch.objects.get_or_create(devEvi_id=eviFile.devEviId, devPartSample_id=id)
                matchObj = match[0]
                matchObj.Score = score
                matchObj.save()
            pager_roles = pg.paginate_queryset(queryset=querysetList, request=request,view=self)
            ser = devMatchXRFSerializer(instance=pager_roles, many=True)
            return pg.get_paginated_response(ser.data)  # 返回上一页或者下一页
        elif type == 9:
            querysetList = []
            eviFile = devShapeEvi.objects.get(id=eviFileId)
            # 存储feature文件（暂无）
            # 特征匹配
            FeatureMatching(eviFileId)
            # 特征匹配文件提取
            matchUrl = os.path.join(MEDIA_ROOT, "image/devShapeEvi/match/" + str(eviFileId)+"/"+ str(eviFileId)  + ".txt")
            if os.path.exists(matchUrl):
                file = open(matchUrl)
                seq = re.compile("\s+")
                for line in file:
                    lst = seq.split(line.strip())
                    shapeMatch1 = devShapeMatch.objects.get_or_create(devShapeEvi_id = eviFileId,devShapeSample_id = lst[0])
                    #注意get_or_create结果是tuple，得取出来才能赋值
                    shapeMatch = shapeMatch1[0]
                    # 存得分
                    shapeMatch.matchDegree = lst[1]
                    # 存样本坐标
                    shapeMatch.matchSampleCoordi = json.dumps(lst[2:4])
                    # 存物证坐标
                    shapeMatch.matchEviCoordi = json.dumps(lst[4:6])
                    # 存半径
                    shapeMatch.matchRadius = json.dumps(lst[6])
                    # 在存一条匹配记录的时候直接把图片存到里面去
                    # shapeMatch.matchPicURL = "image/devShapeEvi/match/" + str(eviFileId) + "/" + str(
                    #     eviFileId) + "_" + str(lst[0]) + ".jpg"
                    shapeMatch.save()
                    querysetList.append(shapeMatch)
                file.close()
                #维护形态综合表
                #之前的成分综合表是把一个物证和一个样本的五种类型的所有结果的综合
                #现在的形态综合就是只有一种类型，把这个类型的所有结果中最高的一对取出来放到综合中,每个物证图片和样本一对，且综合表中每个物证和样本一对
                #先把这张图片的形态匹配表中的所有记录对应的样本id找出来
                matchSampleIds = devShapeMatch.objects.filter(devShapeEvi_id=eviFileId).values_list('devShapeSample__devPartSample_id',flat=True)
                #对于这张图片的每个样本的多张图片的匹配记录中找出最高的那一对作为这个图片和这个样本的记录
                for matchSampleId in matchSampleIds:
                    matchs = devShapeMatch.objects.filter(devShapeEvi_id=eviFileId,devShapeSample__devPartSample_id = matchSampleId).order_by('-matchDegree')
                    # if matchs.count() >1 :
                    #     match = matchs[0]
                    # else:
                    #     match = matchs
                    match = matchs[0]

                    #将这个图片对应的物证和样本添加到形态综合表中
                    multiMatchs = devShapeMultiMatch.objects.get_or_create(devEvi=eviFile.devEvi,devPartSample_id = matchSampleId)
                    multiMatch = multiMatchs[0]
                    multiMatch.Score = match.matchDegree
                    multiMatch.save()
            else:
                raise APIException("匹配文件不存在")
            pager_roles = pg.paginate_queryset(queryset=querysetList, request=request,view=self)
            ser = devShapeMatchSerializer(instance=pager_roles, many=True)
            return pg.get_paginated_response(ser.data)  # 返回上一页或者下一页
        else:
            return  Response("fail")

        # 会返回201的response，且因为Response是rest_framework的，因此只能最低使用APIView
        #在数据库中获取分页数据
        # 应该每个类型返回依次，因为涉及到queryset和serializer，
        # pager_roles = pg.paginate_queryset(queryset=resultDict, request=request,view=self)
        # #对分页数据进行序列化
        # # 应该对应的是要返回数据的match的serializer
        # ser = exploMatchFTIRSerializer(instance=pager_roles, many=True)

        # return pg.get_paginated_response(ser.data)  # 返回上一页或者下一页
        # return  Response("success")

# # 综合表维护接口（重新生成综合表）
# class SynUpdate(APIView):
#     # 生成综合匹配的各自匹配的结果列表
#     # type = 1/2,对应炸药和爆炸装置，id即为物证的id，comDict是那个列表
#     def post(self,request):
#         # 此时type等都是str类型哦
#         type = int(request.POST["type"])
#         eviFileId = int(request.POST["eviFileId"])
#         # 没法直接用type当成类去做filter
#         # result = type.objects.all()
#         # python没有switch case
#         #创建分页对象
#         pg = MyPageNumberPagination()
#         def comDict(type, eviId, comDictDict):
#             if type == 1:
#                 FTIRs = []
#                 RAMANs = []
#                 XRDs = []
#                 XRFs = []
#                 GCMSs = []
#
#                 comListFTIR = []
#                 comListRAMAN = []
#                 comListXRD = []
#                 comListXRF = []
#                 comListGCMS = []
#
#                 FTIRs = exploMatchFTIR.objects.filter(exploEviFTIRTestFile__exploEviId=eviId)
#                 for FTIR in FTIRs:
#                     idScoreList = []
#                     idScoreList.append(FTIR.exploSampleFTIRTestFile.exploSampleFTIR.exploSample_id)
#                     idScoreList.append(FTIR.Score)
#                     comListFTIR.append(idScoreList)
#                 comDictDict["FTIR"] = comListFTIR
#
#                 RAMANs = exploMatchRaman.objects.filter(exploEviRamanTestFile__exploEviId=eviId)
#                 for RAMAN in RAMANs:
#                     idScoreList = []
#                     idScoreList.append(RAMAN.exploSampleRamanTestFile.exploSampleRaman.exploSample_id)
#                     idScoreList.append(RAMAN.Score)
#                     comListRAMAN.append(idScoreList)
#                 comDictDict["RAMAN"] = comListRAMAN
#
#                 XRDs = exploMatchXRD.objects.filter(exploEviXRDTestFile__exploEviId=eviId)
#                 for XRD in XRDs:
#                     idScoreList = []
#                     idScoreList.append(XRD.exploSampleXRDTestFile.exploSampleXRD.exploSample_id)
#                     idScoreList.append(XRD.Score)
#                     comListXRD.append(idScoreList)
#                 comDictDict["XRD"] = comListXRD
#
#                 XRFs = exploMatchXRF.objects.filter(exploEviXRFTestFile__exploEviId=eviId)
#                 for XRF in XRFs:
#                     idScoreList = []
#                     idScoreList.append(XRF.exploSampleXRFTestFile.exploSampleXRF.exploSample_id)
#                     idScoreList.append(XRF.averScore)
#                     comListXRF.append(idScoreList)
#                 comDictDict["XRF"] = comListXRF
#
#                 GCMSs = exploMatchGCMS.objects.filter(exploEviGCMSFile__exploEviId=eviId)
#                 for GCMS in GCMSs:
#                     idScoreList = []
#                     idScoreList.append(GCMS.exploSampleGCMSFile.exploSampleGCMS.exploSample_id)
#                     idScoreList.append(GCMS.Score)
#                     comListGCMS.append(idScoreList)
#                 comDictDict["GCMS"] = comListGCMS
#             elif type == 2:
#                 FTIRs = []
#                 RAMANs = []
#                 XRFs = []
#
#                 comListFTIR = []
#                 comListRAMAN = []
#                 comListXRF = []
#
#                 FTIRs = devMatchFTIR.objects.filter(devEviFTIRTestFile__devEviId=eviId)
#                 for FTIR in FTIRs:
#                     idScoreList = []
#                     idScoreList.append(FTIR.devPartSampleFTIRTestFile.devPartSampleFTIR.devPartSample_id)
#                     idScoreList.append(FTIR.Score)
#                     comListFTIR.append(idScoreList)
#                 comDictDict["FTIR"] = comListFTIR
#
#                 RAMANs = devMatchRaman.objects.filter(devEviRamanTestFile__devEviId=eviId)
#                 for RAMAN in RAMANs:
#                     idScoreList = []
#                     idScoreList.append(RAMAN.devPartSampleRamanTestFile.devPartSampleRaman.devPartSample_id)
#                     idScoreList.append(RAMAN.Score)
#                     comListRAMAN.append(idScoreList)
#                 comDictDict["RAMAN"] = comListRAMAN
#
#                 XRFs = devMatchXRF.objects.filter(devEviXRFTestFile__devEviId=eviId)
#                 for XRF in XRFs:
#                     idScoreList = []
#                     idScoreList.append(XRF.devPartSampleXRFTestFile.devPartSampleXRF.devPartSample_id)
#                     idScoreList.append(XRF.averScore)
#                     comListXRF.append(idScoreList)
#                 comDictDict["XRF"] = comListXRF
#
#
#
#         # comDict(1, eviFile.exploEviId, score_dictSim)
#         #
#         # result = ComScore(score_dictSim, result_dict)
#         # resultDict = result_dict
#         # for id, score in result_dict.items():
#         #     match = exploSynMatch.objects.get_or_create(exploEvi_id=eviFile.exploEviId, exploSample_id=id)
#         #     matchObj = match[0]
#         #     matchObj.Score = score
#         #     matchObj.save()
#         # pager_roles = pg.paginate_queryset(queryset=querysetList, request=request, view=self)
#         # ser = exploMatchFTIRSerializer(instance=pager_roles, many=True)
#         # return pg.get_paginated_response(ser.data)  # 返回上一页或者下一页
#         #


class createExploReport(APIView):
    # 将炸药核准结果变成报告记录接口
    # 和在核准那里不同的是核准那里要根据该条记录是否被专家核准过等判断是否要在报告表中新增一条记录或者将专家核准的结果把普通用户核准的结果替换
    # 而这里报告生成的方式是无论是谁核准的，在综合表中的记录都拿出来（通过id的形式），到时候报告表就根据这些id来生成。
    # 所以核准（综合表）只是记录核准情况，并不会对报告表中的记录产生什么影响，等到生成报告表时才会去查找所有核准过的综合记录的id
    def post(self,request):
        exploId = int(request.POST["exploId"])
        # 将报告表中的该物证对应的记录拿出来，如果没有就按照物证序号建立一条记录
        reportMatch = exploReportMatch.objects.get_or_create(exploEvi_id = exploId)
        reportMatchList = []
        # 获取炸药成分综合匹配结果id列表
        # 先把这个额乌镇对应的所有记录筛选出来
        reportMatchList1= exploSynMatch.objects.filter(exploEvi_id = exploId)
        # 再把所有核准过的（包括普通人员核准和专家核准的）的所有匹配结果的id以列表的形式提取出来
        reportMatchList = reportMatchList1.filter(Q(isCheck=2) | Q(isExpertCheck=2)).values_list("id", flat=True)
        # 将id列表转换为字符串，方便存入数据库中
        reportMatch.exploSynMatch = " ".join(reportMatchList)
        # 提取报告的id用于返回
        reportId = reportMatch.id
        reportMatch.save()

        return Response({
            "exploId": exploId,
            "reportId":reportId
        }, status=status.HTTP_201_CREATED)

# 将爆炸装置核准结果变成报告记录接口
class createDevReport(APIView):
    def post(self,request):
        devEviId = int(request.POST["devEviId"])
        synMatch = devSynMatch.objects.get_or_create(devEvi_id = devEviId)
        devShapeMultiMatchList = []
        devCompMatchList = []
        # 获取形态综合匹配结果核准过的id列表
        devShapeMultiMatchList1 = devShapeMultiMatch.objects.filter(devEvi_id = devEviId)
        devShapeMultiMatchList = devShapeMultiMatchList1.filter(Q(isCheck=2) | Q(isExpertCheck=2)).values_list("id", flat=True)
        devCompMatchList1 = devCompMatch.objects.filter(devEvi_id = devEviId).values_list("id", flat=True)
        devCompMatchList = devCompMatchList1.filter(Q(isCheck=2) | Q(isExpertCheck=2)).values_list("id", flat=True)
        synMatch.devShapeMultiMatch = " ".join(devShapeMultiMatchList)
        synMatch.devCompMatch = " ".join(devCompMatchList)
        reportId = synMatch.id
        synMatch.save()

        return Response({
            "devEviId": devEviId,
            "reportId":reportId
        }, status=status.HTTP_201_CREATED)

class exploMatchFTIRViewset(viewsets.ModelViewSet):
    """
    """
    permission_classes = (IsAuthenticated,IsAdmin)
    pagination_class = MyPageNumberPagination
 #   authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
#    lookup_field = "goods_id"
    filter_backends = (DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter)
    #search_fields是模糊搜索，区别于  filter_fields = ('term',)
    filter_fields = ("exploEviFTIRTestFile_id",)
    # search_fields = ("exploSampleFTIRTestFile_id", "exploEviFTIRTestFile_id","Score")
    ordering_fields = ("-Score",)


    def get_queryset(self):
        return exploMatchFTIR.objects.all()

    def get_serializer_class(self):
        return exploMatchFTIRSerializer

class exploMatchRamanViewset(viewsets.ModelViewSet):
    """
    """
    permission_classes = (IsAuthenticated,IsAdmin)
    pagination_class = MyPageNumberPagination
    filter_backends = (DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter)
    #search_fields是模糊搜索，区别于  filter_fields = ('term',)
    filter_fields = ("exploEviRamanTestFile_id",)
    ordering_fields = ("-Score",)
 #   authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
#    lookup_field = "goods_id"

    def get_queryset(self):
        return exploMatchRaman.objects.all()

    def get_serializer_class(self):
        return exploMatchRamanSerializer

class exploMatchXRDViewset(viewsets.ModelViewSet):
    """
    """
    permission_classes = (IsAuthenticated,IsAdmin)
    pagination_class = MyPageNumberPagination
    filter_backends = (DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter)
    #search_fields是模糊搜索，区别于  filter_fields = ('term',)
    filter_fields = ("exploEviXRDTestFile_id",)
    ordering_fields = ("-Score",)
 #   authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
#    lookup_field = "goods_id"

    def get_queryset(self):
        return exploMatchXRD.objects.all()

    def get_serializer_class(self):
        return exploMatchXRDSerializer

class exploMatchXRFViewset(viewsets.ModelViewSet):
    """
    """
    permission_classes = (IsAuthenticated,IsAdmin)
    pagination_class = MyPageNumberPagination
    filter_backends = (DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter)
    #search_fields是模糊搜索，区别于  filter_fields = ('term',)
    filter_fields = ("exploEviXRFTestFile_id",)
    ordering_fields = ("-averScore",)
 #   authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
#    lookup_field = "goods_id"

    def get_queryset(self):
        return exploMatchXRF.objects.all()

    def get_serializer_class(self):
        return exploMatchXRFSerializer

class exploMatchGCMSViewset(viewsets.ModelViewSet):
    """
    """
    permission_classes = (IsAuthenticated,IsAdmin)
    pagination_class = MyPageNumberPagination
    filter_backends = (DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter)
    #search_fields是模糊搜索，区别于  filter_fields = ('term',)
    filter_fields = ("exploEviGCMSFile_id",)
    ordering_fields = ("-Score",)
 #   authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
#    lookup_field = "goods_id"

    def get_queryset(self):
        return exploMatchGCMS.objects.all()

    def get_serializer_class(self):
        return exploMatchGCMSSerializer

class exploSynMatchViewset(viewsets.ModelViewSet):
    """
    """
    permission_classes = (IsAuthenticated,IsAdmin)
    pagination_class = MyPageNumberPagination
    filter_backends = (DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter)
    #search_fields是模糊搜索，区别于  filter_fields = ('term',)
    filter_fields = ("exploEvi_id",)
    ordering_fields = ("-Score",)
 #   authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
#    lookup_field = "goods_id"

    def get_queryset(self):
        return exploSynMatch.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve" or self.action == "list":
            return exploSynMatchDetailSerializer
        # partial_update和update不同方法！
        # 这里对应的是核准
        elif self.action == "update" or "partial_update":
            return exploSynMatchCheckSerializer
        return exploSynMatchCreateSerializer

class exploReportMatchViewset(viewsets.ModelViewSet):
    """
    """
    permission_classes = (IsAuthenticated,IsAllowExploUpdate)
    pagination_class = MyPageNumberPagination
    filter_backends = (DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter)
    #search_fields是模糊搜索，区别于  filter_fields = ('term',)
    filter_fields = ("exploEvi_id",)
 #   authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
#    lookup_field = "goods_id"

    def get_queryset(self):
        return exploReportMatch.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return exploReportMatchDetailSerializer
        return exploReportMatchSerializer

class devMatchFTIRViewset(viewsets.ModelViewSet):
    """
    """
    permission_classes = (IsAuthenticated,IsAdmin)
    pagination_class = MyPageNumberPagination
    filter_backends = (DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter)
    #search_fields是模糊搜索，区别于  filter_fields = ('term',)
    filter_fields = ("devEviFTIRTestFile_id",)
    ordering_fields = ("-Score",)
 #   authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
#    lookup_field = "goods_id"

    def get_queryset(self):
        return devMatchFTIR.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return devMatchFTIRDetailSerializer
        return devMatchFTIRSerializer

class devMatchRamanViewset(viewsets.ModelViewSet):
    """
    """
    permission_classes = (IsAuthenticated,IsAdmin )
    pagination_class = MyPageNumberPagination
    filter_backends = (DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter)
    #search_fields是模糊搜索，区别于  filter_fields = ('term',)
    filter_fields = ("devEviRamanTestFile_id",)
    ordering_fields = ("-Score",)
 #   authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
#    lookup_field = "goods_id"

    def get_queryset(self):
        return devMatchRaman.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return devMatchRamanDetailSerializer
        return devMatchRamanSerializer

class devMatchXRFViewset(viewsets.ModelViewSet):
    """
    """
    permission_classes = (IsAuthenticated,IsAdmin )
    pagination_class = MyPageNumberPagination
    filter_backends = (DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter)
    #search_fields是模糊搜索，区别于  filter_fields = ('term',)
    filter_fields = ("devEviXRFTestFile_id",)
    ordering_fields = ("-averScore",)
 #   authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
#    lookup_field = "goods_id"

    def get_queryset(self):
        return devMatchXRF.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return devMatchXRFDetailSerializer
        return devMatchXRFSerializer

class devCompMatchViewset(viewsets.ModelViewSet):
    """
    """
    permission_classes = (IsAuthenticated,IsAllowDevUpdate)
    pagination_class = MyPageNumberPagination
    filter_backends = (DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter)
    #search_fields是模糊搜索，区别于  filter_fields = ('term',)
    filter_fields = ("devEvi_id",)
    ordering_fields = ("-Score",)
 #   authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
#    lookup_field = "goods_id"

    def get_queryset(self):
        return devCompMatch.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve"or self.action == "list":
            return devCompMatchDetailSerializer
        # partial_update和update不同方法！
        # 这里对应的是核准
        elif self.action == "update" or "partial_update":
            return devCompMatchCheckSerializer
        return devCompMatchCreateSerializer

class devShapeMatchViewset(viewsets.ModelViewSet):
 #   authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
#    lookup_field = "goods_id"
    permission_classes = (IsAuthenticated,IsAdmin)
    pagination_class = MyPageNumberPagination
    filter_backends = (DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter)
    #search_fields是模糊搜索，区别于  filter_fields = ('term',)
    filter_fields = ("devShapeEvi_id",)
    ordering_fields = ("-matchDegree",)
    def get_queryset(self):
        return devShapeMatch.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return devShapeMatchDetailSerializer
        return devShapeMatchSerializer

class devShapeMultiMatchViewset(viewsets.ModelViewSet):
    """
    形态综合表
    """
    permission_classes = (IsAuthenticated,IsAllowDevUpdate)
    pagination_class = MyPageNumberPagination
    filter_backends = (DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter)
    #search_fields是模糊搜索，区别于  filter_fields = ('term',)
    filter_fields = ("devEvi_id",)
    ordering_fields = ("-Score",)
 #   authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
#    lookup_field = "goods_id"

    def get_queryset(self):
        return devShapeMultiMatch.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve"or self.action == "list":
            return devShapeMultiMatchDetailSerializer
        # partial_update和update不同方法！
        # 这里对应的是核准
        elif self.action == "update" or "partial_update":
            return devShapeMultiMatchCheckSerializer
        return devShapeMultiMatchSerializer


class devSynMatchViewset(viewsets.ModelViewSet):
    """
    报告表
    """
    permission_classes = (IsAuthenticated,IsAdmin)
    pagination_class = MyPageNumberPagination
    filter_backends = (DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter)
    #search_fields是模糊搜索，区别于  filter_fields = ('term',)
    filter_fields = ("devEvi_id",)
    # filter_backends = (filters.OrderingFilter,)
    # ordering_fields = ("-ScoreComp","-ScoreShape")
 #   authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
#    lookup_field = "goods_id"

    def get_queryset(self):
        return devSynMatch.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return devSynMatchDetailSerializer
        return devSynMatchSerializer