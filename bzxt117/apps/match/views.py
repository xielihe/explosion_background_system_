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
from rest_framework.pagination import PageNumberPagination


from apps.match.serializers import *
from utils.permissions import *
from apps.match.models import *
from apps.evi.models import *
from apps.sample.serializers import *

class MyPageNumberPagination(PageNumberPagination):
    # 指定这一页有多少个
    page_size=1  #默认两个

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
        keyWord = request.POST["keyWord"]
        devEviId = int(request.POST["devEviId"])
        # 待语义匹配的物证对象
        devEviSelect = devEvi.objects.get(id = devEviId)

        #创建分页对象
        pg = MyPageNumberPagination()
        sampleQuery = devPartSample.objects.all()
        if Color == 'True':
            sampleQuery = sampleQuery.filter(Color = devEviSelect.Color)
        if Shape == 'True':
            sampleQuery = sampleQuery.filter(Shape=devEviSelect.Shape)
        if Material == 'True':
            sampleQuery = sampleQuery.filter(Material = devEviSelect.Material)
        if thickness == 'True':
            sampleQuery = sampleQuery.filter(thickness = devEviSelect.thickness)

        sampleQueryRES = sampleQuery.filter(Q(Origin__icontains=keyWord)|Q(Factory__icontains=keyWord)|Q(Model__icontains=keyWord)
                                         |Q(Logo__icontains=keyWord)|Q(function__icontains=keyWord)|Q(note__icontains=keyWord))
        #在数据库中获取分页数据
        pager_roles = pg.paginate_queryset(queryset=sampleQueryRES, request=request,view=self)
        #对分页数据进行序列化
        ser = PagerSerialiser(instance=pager_roles, many=True)

        return pg.get_paginated_response(ser.data)  # 返回上一页或者下一页

        # sampleJSON = devPartSampleSerializer(instance=sampleQueryRES, many=True)
        # samples = json.dumps(sampleJSON.data, ensure_ascii=False)
        #
        # return Response({
        #     "result": samples,
        # }, status=status.HTTP_201_CREATED)

class startMatch(APIView):
    # get方法是请求在url中的参数的，而post是请求在request中的参数的
    def post(self,request):
        # 此时type等都是str类型哦
        type = int(request.POST["type"])
        eviId = int(request.POST["eviId"])
        # 没法直接用type当成类去做filter
        # result = type.objects.all()
        # python没有switch case

        #创建分页对象
        pg = MyPageNumberPagination()

        if type == 1:
            # 如果物证更新后再次要求匹配或者是重复请求，先删除，在做匹配
            results = exploMatchFTIR.objects.filter(exploEviFTIR_id = eviId)
            for result in results:
                result.delete()
            #调用FTIR的匹配函数,传入参数为物证id，注意要同时维护综合表：
            # 不管是先全删除还是直接存入匹配数据，都是全部做完再操作综合表：全删，重做综合表
                # # exploSyn_Match不能重名exploSynMatch！！
                # exploSyn_Match = exploSynMatch()
                # exploSyn_Match.exploEvi_id = eviId
                # exploSyn_Match.exploSample_id = 1
                # exploSyn_Match.Score = 100
                # # 外键空值的时候可以赋值为None,代表数据库中的NULL，且序列化的时候也不会出问题的~
                # exploSyn_Match.checkHandle = None
                # exploSyn_Match.expertHandle_id = 2
                # exploSyn_Match.save()
        elif type ==2:
        #     exploMatchRaman
            pass

        #修改得分，同时核准置为False，核准人员为None
        # 会返回201的response，且因为Response是rest_framework的，因此只能最低使用APIView
        #在数据库中获取分页数据
        # 应该每个类型返回依次，因为涉及到queryset和serializer，
        pager_roles = pg.paginate_queryset(queryset=results, request=request,view=self)
        #对分页数据进行序列化
        # 应该对应的是要返回数据的match的serializer
        ser = exploMatchFTIRSerializer(instance=pager_roles, many=True)

        return pg.get_paginated_response(ser.data)  # 返回上一页或者下一页


class exploMatchFTIRViewset(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    """
    permission_classes = (IsAuthenticated,)
    pagination_class = MyPageNumberPagination
 #   authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
#    lookup_field = "goods_id"
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ("Score",)

    def get_queryset(self):
        return exploMatchFTIR.objects.all()

    def get_serializer_class(self):
        return exploMatchFTIRSerializer

class exploMatchRamanViewset(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    """
    permission_classes = (IsAuthenticated,)
    pagination_class = MyPageNumberPagination
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ("Score",)
 #   authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
#    lookup_field = "goods_id"

    def get_queryset(self):
        return exploMatchRaman.objects.all()

    def get_serializer_class(self):
        return exploMatchRamanSerializer

class exploMatchXRDViewset(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    """
    permission_classes = (IsAuthenticated,)
    pagination_class = MyPageNumberPagination
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ("Score",)
 #   authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
#    lookup_field = "goods_id"

    def get_queryset(self):
        return exploMatchXRD.objects.all()

    def get_serializer_class(self):
        return exploMatchXRDSerializer

class exploMatchXRFViewset(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    """
    permission_classes = (IsAuthenticated,)
    pagination_class = MyPageNumberPagination
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ("averScore",)
 #   authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
#    lookup_field = "goods_id"

    def get_queryset(self):
        return exploMatchXRF.objects.all()

    def get_serializer_class(self):
        return exploMatchXRFSerializer

class exploMatchGCMSViewset(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    """
    permission_classes = (IsAuthenticated,)
    pagination_class = MyPageNumberPagination
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ("Score",)
 #   authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
#    lookup_field = "goods_id"

    def get_queryset(self):
        return exploMatchGCMS.objects.all()

    def get_serializer_class(self):
        return exploMatchGCMSSerializer

class exploSynMatchViewset(viewsets.ModelViewSet):
    """
    """
    permission_classes = (IsAuthenticated,)
    pagination_class = MyPageNumberPagination
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ("Score",)
 #   authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
#    lookup_field = "goods_id"

    def get_queryset(self):
        return exploSynMatch.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return exploSynMatchDetailSerializer
        # partial_update和update不同方法！
        # 这里对应的是核准
        elif self.action == "update" or "partial_update":
            return exploSynMatchSerializer
        return exploSynMatchCreateSerializer

class exploReportMatchViewset(viewsets.ModelViewSet):
    """
    """
    permission_classes = (IsAuthenticated,)
    pagination_class = MyPageNumberPagination
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ("Score",)
 #   authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
#    lookup_field = "goods_id"

    def get_queryset(self):
        return exploReportMatch.objects.all()

    def get_serializer_class(self):
        return exploReportMatchSerializer

class devMatchFTIRViewset(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    """
    permission_classes = (IsAuthenticated,)
    pagination_class = MyPageNumberPagination
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ("Score",)
 #   authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
#    lookup_field = "goods_id"

    def get_queryset(self):
        return devMatchFTIR.objects.all()

    def get_serializer_class(self):
        return devMatchFTIRSerializer

class devMatchRamanViewset(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    """
    permission_classes = (IsAuthenticated, )
    pagination_class = MyPageNumberPagination
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ("Score",)
 #   authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
#    lookup_field = "goods_id"

    def get_queryset(self):
        return devMatchRaman.objects.all()

    def get_serializer_class(self):
        return devMatchRamanSerializer

class devMatchXRFViewset(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    """
    permission_classes = (IsAuthenticated, )
    pagination_class = MyPageNumberPagination
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ("averScore",)
 #   authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
#    lookup_field = "goods_id"

    def get_queryset(self):
        return devMatchXRF.objects.all()

    def get_serializer_class(self):
        return devMatchXRFSerializer

class devCompMatchViewset(viewsets.ModelViewSet):
    """
    """
    permission_classes = (IsAuthenticated, )
    pagination_class = MyPageNumberPagination
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ("Score",)
 #   authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
#    lookup_field = "goods_id"

    def get_queryset(self):
        return devCompMatch.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return devCompMatchDetailSerializer
        # partial_update和update不同方法！
        # 这里对应的是核准
        elif self.action == "update" or "partial_update":
            return devCompMatchSerializer
        return devCompMatchCreateSerializer

class devShapeMatchViewset(viewsets.ModelViewSet):
 #   authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
#    lookup_field = "goods_id"
    permission_classes = (IsAuthenticated,)
    pagination_class = MyPageNumberPagination
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ("matchDegree",)
    def get_queryset(self):
        return devShapeMatch.objects.all()

    def get_serializer_class(self):
        # 这里对应的是核准
        if self.action == "update" or "partial_update":
            return devShapeMatchDetailSerializer
        return devShapeMatchSerializer

class devSynMatchViewset(viewsets.ModelViewSet):
    """
    """
    permission_classes = (IsAuthenticated,)
    pagination_class = MyPageNumberPagination
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ("ScoreComp","ScoreShape")
 #   authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
#    lookup_field = "goods_id"

    def get_queryset(self):
        return devSynMatch.objects.all()

    def get_serializer_class(self):
        return devSynMatchSerializer