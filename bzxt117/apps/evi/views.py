# -*- coding: utf-8 -*-

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from rest_framework import viewsets
import json
import re
from rest_framework.response import Response
from rest_framework import status

from apps.evi.serializers import *
from apps.evi.models import *
from apps.match.models import *
from apps.utils.permissions import *
from bzxt117.settings import MEDIA_ROOT
from utils.PCB import *
from utils.GCMS_handle import *
from apps.match.views import MyPageNumberPagination




# 物证更新在匹配界面的提示表现在所有相关的匹配结果全部为空，即一旦物证文件变化相关匹配结果会删除，那么数据库无法得到相关数据，在前端展示为空
# 物证的匹配结果一旦删除，在前端展示的时候会表示成一个表是空的，而不像一个样本变化时如果只是删除匹配结果而不是更新匹配结果的话在前端根本看不出来，因为少一行没有提示
# 因此要维护好当物证文件一旦变化，匹配结果也要删除


class exploEviViewset(viewsets.ModelViewSet):
    """
    炸药及原材料常见样本管理
    list:
        获取
    create:
        添加
    update:
        更新
    delete:
        删除
    """
    queryset = exploEvi.objects.all()
    #queryset = exploSample.objects.filter(sname="样本3")
    serializer_class = exploEviSerializer
    # permission_classes = (IsAuthenticated,IsAllowExploUpdate)
    pagination_class = MyPageNumberPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("caseName","evidenceName","note")
    ordering_fields = ("id","inputDate")

    def get_permissions(self):
        if self.action == "delete" or "update" or "partial_update":
        #     return [permissions.IsAuthenticated(),IsAdmin()]
        # elif self.action == "update":
            return [permissions.IsAuthenticated(),IsAllowExploUpdate()]
        else:
            return [permissions.IsAuthenticated(),]

class exploEviFTIRViewset(viewsets.ModelViewSet):

    queryset = exploEviFTIR.objects.all()
    #queryset = exploSample.objects.filter(sname="样本3")
    # serializer_class = exploSampleFTIRSerializer
    # permission_classes = (IsAuthenticated,IsAllowExploUpdate)
    pagination_class = MyPageNumberPagination
    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return exploEviFTIRDetailSerializer
        return exploEviFTIRSerializer

    def get_permissions(self):
        if self.action == "delete" or "update" or "partial_update":
        #     return [permissions.IsAuthenticated(),IsAdmin()]
        # elif self.action == "update":
            return [permissions.IsAuthenticated(),IsAllowExploUpdate()]
        else:
            return [permissions.IsAuthenticated(),]

class exploEviFTIRTestFileViewset(viewsets.ModelViewSet):
    pagination_class = MyPageNumberPagination
    queryset = exploEviFTIRTestFile.objects.all()
    #queryset = exploSample.objects.filter(sname="样本3")
    # serializer_class = LsitExploSampleFTIRTestFileSerializer
    # permission_classes = (IsAuthenticated,IsAdmin)
    parser_classes = (MultiPartParser, FileUploadParser,)

    def get_serializer_class(self):
        if self.action == "create":
            return LsitExploEviFTIRTestFileSerializer
        return exploEviFTIRTestFileSerializer

    # list方法：返回列表 都可以
    # create方法：创建一个实例 都可以
    # retrieve方法：返回一个具体的实例 都可以
    # update方法：对某个实例进行更新 第三角色需验证
    # delete方法：删除某个实例 第三角色不可以
    def get_permissions(self):
        if self.action == "delete" or "update" or "partial_update":
        #     return [permissions.IsAuthenticated(),IsAdmin()]
        # elif self.action == "update":
            return [permissions.IsAuthenticated(),IsAllowExploUpdate()]
        else:
            return [permissions.IsAuthenticated(),]

    # 物证文件删除，由于外键关联，会自动删除关联的FTIR表的匹配信息，但综合表和报告表的也应该手动删除
    def perform_destroy(self, instance):
        synMatchs = exploSynMatch.objects.filter(exploEvi = instance.exploEviFTIR.exploEvi )
        for synMatch in synMatchs:
            synMatch.delete()
        reportMatchs = exploReportMatch.objects.filter(exploEvi = instance.exploEviFTIR.exploEvi )
        for reportMatch in reportMatchs:
            reportMatch.delete()
        instance.delete()

class exploEviRamanViewset(viewsets.ModelViewSet):
    pagination_class = MyPageNumberPagination
    queryset = exploEviRaman.objects.all()
    #queryset = exploSample.objects.filter(sname="样本3")
    # serializer_class = exploEviRamanSerializer
    # permission_classes = (IsAuthenticated,IsAdmin)
    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return exploEviRamanDetailSerializer
        return exploEviRamanSerializer

    def get_permissions(self):
        if self.action == "delete" or "update" or "partial_update":
        #     return [permissions.IsAuthenticated(),IsAdmin()]
        # elif self.action == "update":
            return [permissions.IsAuthenticated(),IsAllowExploUpdate()]
        else:
            return [permissions.IsAuthenticated(),]

class exploEviRamanTestFileViewset(viewsets.ModelViewSet):
    pagination_class = MyPageNumberPagination
    queryset = exploEviRamanTestFile.objects.all()
    #queryset = exploSample.objects.filter(sname="样本3")
    # serializer_class = exploEviRamanTestFileSerializer
    # permission_classes = (IsAuthenticated,IsAdmin)
    parser_classes = (MultiPartParser, FileUploadParser,)

    def get_serializer_class(self):
        if self.action == "create":
            return LsitExploEviRamanTestFileSerializer
        return exploEviRamanTestFileSerializer

    def get_permissions(self):
        if self.action == "delete" or "update" or "partial_update":
        #     return [permissions.IsAuthenticated(),IsAdmin()]
        # elif self.action == "update":
            return [permissions.IsAuthenticated(),IsAllowExploUpdate()]
        else:
            return [permissions.IsAuthenticated(),]

    def perform_destroy(self, instance):
        synMatchs = exploSynMatch.objects.filter(exploEvi = instance.exploEviRaman.exploEvi )
        for synMatch in synMatchs:
            synMatch.delete()
        reportMatchs = exploReportMatch.objects.filter(exploEvi = instance.exploEviRaman.exploEvi )
        for reportMatch in reportMatchs:
            reportMatch.delete()
        instance.delete()

class exploEviXRDViewset(viewsets.ModelViewSet):
    pagination_class = MyPageNumberPagination
    queryset = exploEviXRD.objects.all()
    #queryset = exploSample.objects.filter(sname="样本3")
    # serializer_class = exploEviXRDSerializer
    # permission_classes = (IsAuthenticated,IsAdmin)
    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return exploEviXRDDetailSerializer
        return exploEviXRDSerializer

    def get_permissions(self):
        if self.action == "delete" or "update" or "partial_update":
        #     return [permissions.IsAuthenticated(),IsAdmin()]
        # elif self.action == "update":
            return [permissions.IsAuthenticated(),IsAllowExploUpdate()]
        else:
            return [permissions.IsAuthenticated(),]

class exploEviXRDTestFileViewset(viewsets.ModelViewSet):
    pagination_class = MyPageNumberPagination
    queryset = exploEviXRDTestFile.objects.all()
    #queryset = exploSample.objects.filter(sname="样本3")
    # serializer_class =exploEviXRDTestFileSerializer
    # permission_classes = (IsAuthenticated,IsAdmin)
    parser_classes = (MultiPartParser, FileUploadParser,)


    def get_serializer_class(self):
        if self.action == "create":
            return LsitExploEviXRDTestFileSerializer
        return exploEviXRDTestFileSerializer

    def get_permissions(self):
        if self.action == "delete" or "update"or "partial_update":
            #     return [permissions.IsAuthenticated(),IsAdmin()]
            # elif self.action == "update":
            return [permissions.IsAuthenticated(), IsAllowExploUpdate()]
        else:
            return [permissions.IsAuthenticated(), ]

    # 物证文件删除，由于外键关联，会自动删除关联的FTIR表的匹配信息，但综合表和报告表的也应该手动删除
    def perform_destroy(self, instance):
        synMatchs = exploSynMatch.objects.filter(exploEvi = instance.exploEviXRD.exploEvi )
        for synMatch in synMatchs:
            synMatch.delete()
        reportMatchs = exploReportMatch.objects.filter(exploEvi = instance.exploEviXRD.exploEvi )
        for reportMatch in reportMatchs:
            reportMatch.delete()
        instance.delete()

class exploEviXRFViewset(viewsets.ModelViewSet):
    pagination_class = MyPageNumberPagination
    queryset = exploEviXRF.objects.all()
    #queryset = exploSample.objects.filter(sname="样本3")
    # serializer_class = exploEviXRFSerializer
    # permission_classes = (IsAuthenticated,IsAdmin)
    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return exploEviXRFDetailSerializer
        return exploEviXRFSerializer

    def get_permissions(self):
        if self.action == "delete" or "update" or "partial_update":
        #     return [permissions.IsAuthenticated(),IsAdmin()]
        # elif self.action == "update":
            return [permissions.IsAuthenticated(),IsAllowExploUpdate()]
        else:
            return [permissions.IsAuthenticated(),]

class exploEviXRFTestFileViewset(viewsets.ModelViewSet):
    pagination_class = MyPageNumberPagination
    queryset = exploEviXRFTestFile.objects.all()
    #queryset = exploSample.objects.filter(sname="样本3")
    # serializer_class = exploEviXRFTestFileSerializer
    # permission_classes = (IsAuthenticated,IsAdmin)
    parser_classes = (MultiPartParser, FileUploadParser,)

    def get_serializer_class(self):
        if self.action == "create":
            return LsitExploEviXRFTestFileSerializer
        return exploEviXRFTestFileSerializer

    def get_permissions(self):
        if self.action == "delete" or "update" or "partial_update":
            #     return [permissions.IsAuthenticated(),IsAdmin()]
            # elif self.action == "update":
            return [permissions.IsAuthenticated(), IsAllowExploUpdate()]
        else:
            return [permissions.IsAuthenticated(), ]

    def perform_destroy(self, instance):
        synMatchs = exploSynMatch.objects.filter(exploEvi = instance.exploEviXRF.exploEvi )
        for synMatch in synMatchs:
            synMatch.delete()
        reportMatchs = exploReportMatch.objects.filter(exploEvi = instance.exploEviXRF.exploEvi )
        for reportMatch in reportMatchs:
            reportMatch.delete()
        instance.delete()

class exploEviGCMSViewset(viewsets.ModelViewSet):
    pagination_class = MyPageNumberPagination
    queryset = exploEviGCMS.objects.all()
    #queryset = exploSample.objects.filter(sname="样本3")
    # serializer_class = exploEviGCMSSerializer
    # permission_classes = (IsAuthenticated,IsAdmin)
    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return exploEviGCMSDetailSerializer
        return exploEviGCMSSerializer

    def get_permissions(self):
        if self.action == "delete" or "update" or "partial_update":
        #     return [permissions.IsAuthenticated(),IsAdmin()]
        # elif self.action == "update":
            return [permissions.IsAuthenticated(),IsAllowExploUpdate()]
        else:
            return [permissions.IsAuthenticated(),]

class exploEviGCMSTestFileViewset(viewsets.ModelViewSet):
    pagination_class = MyPageNumberPagination
    queryset = exploEviGCMSTestFile.objects.all()
    #queryset = exploSample.objects.filter(sname="样本3")
    # serializer_class = exploEviGCMSTestFileSerializer
    # permission_classes = (IsAuthenticated,IsAdmin)
    parser_classes = (MultiPartParser, FileUploadParser,)
    def get_serializer_class(self):
        if self.action == "create":
            return LsitExploEviGCMSTestFileSerializer
        return exploEviGCMSTestFileSerializer

    def get_permissions(self):
        if self.action == "delete" or "update" or "partial_update":
        #     return [permissions.IsAuthenticated(),IsAdmin()]
        # elif self.action == "update":
            return [permissions.IsAuthenticated(),IsAllowExploUpdate()]
        else:
            return [permissions.IsAuthenticated(),]

    def perform_destroy(self, instance):
        synMatchs = exploSynMatch.objects.filter(exploEvi = instance.exploEviGCMS.exploEvi )
        for synMatch in synMatchs:
            synMatch.delete()
        reportMatchs = exploReportMatch.objects.filter(exploEvi = instance.exploEviGCMS.exploEvi )
        for reportMatch in reportMatchs:
            reportMatch.delete()
        instance.delete()

class devEviViewset(viewsets.ModelViewSet):
    pagination_class = MyPageNumberPagination
    queryset = devEvi.objects.all()
    #queryset = exploSample.objects.filter(sname="样本3")
    serializer_class = devEviSerializer
    # permission_classes = (IsAuthenticated,IsAdmin)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("caseName","evidenceName","note","Factory","Model","Logo","Color","Material","Shape","thickness")
    ordering_fields = ("id","inputDate")

    def get_permissions(self):
        if self.action == "delete" or "update" or "partial_update":
        #     return [permissions.IsAuthenticated(),IsAdmin()]
        # elif self.action == "update":
            return [permissions.IsAuthenticated(),IsAllowExploUpdate()]
        else:
            return [permissions.IsAuthenticated(),]

class devEviFTIRViewset(viewsets.ModelViewSet):
    queryset = devEviFTIR.objects.all()
    #queryset = exploSample.objects.filter(sname="样本3")
    pagination_class = MyPageNumberPagination
    # serializer_class = devEviFTIRSerializer
    # permission_classes = (IsAuthenticated,IsAdmin)
    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return devEviFTIRDetailSerializer
        return devEviFTIRSerializer

    def get_permissions(self):
        if self.action == "delete" or "update" or "partial_update":
        #     return [permissions.IsAuthenticated(),IsAdmin()]
        # elif self.action == "update":
            return [permissions.IsAuthenticated(),IsAllowExploUpdate()]
        else:
            return [permissions.IsAuthenticated(),]

class devEviFTIRTestFileViewset(viewsets.ModelViewSet):
    queryset = devEviFTIRTestFile.objects.all()
    #queryset = exploSample.objects.filter(sname="样本3")
    # serializer_class = devEviFTIRTestFileSerializer
    pagination_class = MyPageNumberPagination
    # permission_classes = (IsAuthenticated,IsAdmin)
    parser_classes = (MultiPartParser, FileUploadParser,)
    def get_serializer_class(self):
        if self.action == "create":
            return LsitdevEviFTIRTestFileSerializer
        return devEviFTIRTestFileSerializer

    def get_permissions(self):
        if self.action == "delete" or "update" or "partial_update":
        #     return [permissions.IsAuthenticated(),IsAdmin()]
        # elif self.action == "update":
            return [permissions.IsAuthenticated(),IsAllowExploUpdate()]
        else:
            return [permissions.IsAuthenticated(),]

    def perform_destroy(self, instance):
        compMatchs = devCompMatch.objects.filter(devEvi=instance.devEviFTIR.devEvi_id)
        for compMatch in compMatchs:
            compMatch.delete()
        synMatchs = devSynMatch.objects.filter(devEvi_id=instance.devEviFTIR.devEvi_id)
        for synMatch in synMatchs:
            synMatch.delete()
        instance.delete()

class devEviRamanViewset(viewsets.ModelViewSet):
    queryset = devEviRaman.objects.all()
    #queryset = exploSample.objects.filter(sname="样本3")
    # serializer_class = devEviRamanSerializer
    # permission_classes = (IsAuthenticated,IsAdmin)
    pagination_class = MyPageNumberPagination
    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return devEviRamanDetailSerializer
        return devEviRamanSerializer

    def get_permissions(self):
        if self.action == "delete" or "update" or "partial_update":
        #     return [permissions.IsAuthenticated(),IsAdmin()]
        # elif self.action == "update":
            return [permissions.IsAuthenticated(),IsAllowExploUpdate()]
        else:
            return [permissions.IsAuthenticated(),]

class devEviRamanTestFileViewset(viewsets.ModelViewSet):
    queryset = devEviRamanTestFile.objects.all()
    pagination_class = MyPageNumberPagination
    #queryset = exploSample.objects.filter(sname="样本3")
    # serializer_class = devEviRamanTestFileSerializer
    # permission_classes = (IsAuthenticated,IsAdmin)
    parser_classes = (MultiPartParser, FileUploadParser,)
    def get_serializer_class(self):
        if self.action == "create":
            return LsitdevEviRamanTestFileSerializer
        return devEviRamanTestFileSerializer

    def get_permissions(self):
        if self.action == "delete" or "update" or "partial_update":
        #     return [permissions.IsAuthenticated(),IsAdmin()]
        # elif self.action == "update":
            return [permissions.IsAuthenticated(),IsAllowExploUpdate()]
        else:
            return [permissions.IsAuthenticated(),]

    def perform_destroy(self, instance):
        compMatchs = devCompMatch.objects.filter(devEvi=instance.devEviRaman.devEvi_id)
        for compMatch in compMatchs:
            compMatch.delete()
        synMatchs = devSynMatch.objects.filter(devEvi_id=instance.devEviRaman.devEvi_id)
        for synMatch in synMatchs:
            synMatch.delete()
        instance.delete()

class devEviXRFViewset(viewsets.ModelViewSet):
    queryset = devEviXRF.objects.all()
    pagination_class = MyPageNumberPagination
    #queryset = exploSample.objects.filter(sname="样本3")
    # serializer_class = devEviXRFSerializer
    # permission_classes = (IsAuthenticated,IsAdmin)
    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return devEviXRFDetailSerializer
        return devEviXRFSerializer

    def get_permissions(self):
        if self.action == "delete" or "update" or "partial_update":
        #     return [permissions.IsAuthenticated(),IsAdmin()]
        # elif self.action == "update":
            return [permissions.IsAuthenticated(),IsAllowExploUpdate()]
        else:
            return [permissions.IsAuthenticated(),]

class devEviXRFTestFileViewset(viewsets.ModelViewSet):
    queryset = devEviXRFTestFile.objects.all()
    pagination_class = MyPageNumberPagination
    #queryset = exploSample.objects.filter(sname="样本3")
    # serializer_class = devEviXRFTestFileSerializer
    # permission_classes = (IsAuthenticated,IsAdmin)
    parser_classes = (MultiPartParser, FileUploadParser,)
    def get_serializer_class(self):
        if self.action == "create":
            return LsitdevEviXRFTestFileSerializer
        return devEviXRFTestFileSerializer

    def get_permissions(self):
        if self.action == "delete" or "update" or "partial_update":
        #     return [permissions.IsAuthenticated(),IsAdmin()]
        # elif self.action == "update":
            return [permissions.IsAuthenticated(),IsAllowExploUpdate()]
        else:
            return [permissions.IsAuthenticated(),]

    def perform_destroy(self, instance):
        compMatchs = devCompMatch.objects.filter(devEvi=instance.devEviXRF.devEvi_id)
        for compMatch in compMatchs:
            compMatch.delete()
        synMatchs = devSynMatch.objects.filter(devEvi_id=instance.devEviXRF.devEvi_id)
        for synMatch in synMatchs:
            synMatch.delete()
        instance.delete()

class devShapeEviViewset(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    queryset = devShapeEvi.objects.all()
    serializer_class = devShapeEviSerializer
    pagination_class = MyPageNumberPagination

    def get_permissions(self):
        if self.action == "delete" or "update" or "partial_update":
        #     return [permissions.IsAuthenticated(),IsAdmin()]
        # elif self.action == "update":
            return [permissions.IsAuthenticated(),IsAllowExploUpdate()]
        else:
            return [permissions.IsAuthenticated(),]

    def perform_create(self, serializer):
        evi = serializer.save()
        id = evi.id
        #重命名
        name = str(evi.originalUrl).split("/")[-1]
        picType = os.path.splitext(name)[1]
        path = os.path.join(MEDIA_ROOT,"image/devShapeEvi/original/")
        os.rename(os.path.join(MEDIA_ROOT,str(evi.originalUrl)), os.path.join(path, str(id) + picType))
        evi.originalUrl = "image/devShapeEvi/original/" + str(id) + picType
        evi.save()
        #特征匹配
        if evi.isCircuit == False:
            FeatureMatching(id)
            evi.featureUrl = "file/devShapeEvi/feature/" + str(id) + ".harris"
            evi.save()
            fileUrl = os.path.join(MEDIA_ROOT,"file/devShapeEvi/match/"+ str(id)+".txt")
            file = open(fileUrl)
            seq = re.compile("\s+")
            for line in file:
                lst = seq.split(line.strip())
                shapeMatch = devShapeMatch()
                shapeMatch.devShapeEvi_id = lst[0]
                shapeMatch.devShapeSample_id = lst[1]
                shapeMatch.matchDegree = lst[2]
                shapeMatch.matchSampleCoordi = json.dumps(lst[3:6])
                shapeMatch.matchEviCoordi = json.dumps(lst[6:])
                shapeMatch.isCircuit = False
                shapeMatch.save()
            file.close()
            os.remove(fileUrl)

        return evi

    def perform_update(self, serializer):
        evi = serializer.save()
        id =evi.id
        if evi.isCircuit == False:
            FeatureMatching(id)
            evi.featureUrl = "file/devShapeEvi/feature/" + str(id) + ".harris"
            evi.save()
        else:
            middle = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "utils/middle/")
            if evi.isFirst == True:

                # 写文件
                rectUrl = os.path.join(middle, str(id) + "-1.txt")
                proUrl = os.path.join(middle, str(id) + "-2.txt")
                backUrl = os.path.join(middle, str(id) + "-3.txt")
                boardUrl = os.path.join(middle, str(id) + "-4.txt")

                rect = open(rectUrl, "w")
                rect.write(evi.rectCoordi)
                rect.close()
                pro = open(proUrl, "w")
                pro.write(evi.proCoordi)
                pro.close()
                back = open(backUrl, "w")
                back.write(evi.backCoordi)
                back.close()
                board = open(boardUrl, "w")
                board.write(evi.boardCoordi)
                board.close()

                getPCB(id, "Evi")

                evi.blackWhiteUrl = "image/devShapeEvi/blackWhite/" + str(id) + ".jpg"
                evi.interColorUrl = "image/devShapeEvi/interColor/" + str(id) + ".jpg"
                evi.middleResultUrl = "file/devShapeEvi/middleResult/" + str(id) + ".txt"

                os.remove(rectUrl)
                os.remove(proUrl)
                os.remove(backUrl)
                os.remove(boardUrl)

                evi.save()
            else:
                compCheckUrl = os.path.join(middle, str(id) + "-5.txt")
                boardCheckUrl = os.path.join(middle, str(id) + "-6.txt")

                compCheck = open(compCheckUrl, "w")
                compCheck.write(evi.compCheckCoordi)
                compCheck.close()
                boardCheck = open(boardCheckUrl, "w")
                boardCheck.write(evi.boardCheckCoordi)
                boardCheck.close()

                segComp(id, "Evi")

                evi.featureUrl = "file/devShapeEvi/feature/" + str(id) + ".harris"
                evi.resultPicUrl = "image/devShapeEvi/result/" + str(id) + ".jpg"
                evi.resultFileUrl = "file/devShapeEvi/result/" + str(id) + ".seg"

                os.remove(compCheckUrl)
                os.remove(boardCheckUrl)
                evi.save()

                CompMatching(id)

        fileUrl = os.path.join(MEDIA_ROOT,"file/devShapeEvi/match/"+ str(id)+".txt")
        if os.path.exists(fileUrl):
            file = open(fileUrl)
            seq = re.compile("\s+")
            for line in file:
                lst = seq.split(line.strip())
                shapeMatch = devShapeMatch()
                shapeMatch.devShapeEvi_id = lst[0]
                shapeMatch.devShapeSample_id = lst[1]
                shapeMatch.matchDegree = lst[2]
                shapeMatch.matchSampleCoordi = json.dumps(lst[3:6])
                shapeMatch.matchEviCoordi = json.dumps(lst[6:])
                shapeMatch.isCircuit = evi.isCircuit
                shapeMatch.save()
            file.close()
            # os.remove(fileUrl)
        return evi
