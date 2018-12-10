from django.shortcuts import render
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework.mixins import CreateModelMixin
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler


from apps.user_operation.serializers import *
from apps.user_operation.models import *
from utils.permissions import *
from apps.match.views import *
#User = get_user_model()

# Create your views here.
class userMessageViewset(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    不支持更新
    """
 #   authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
#    lookup_field = "goods_id"
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ("sendUser","receiveUser")
    pagination_class = MyPageNumberPagination
    # filter_backends = (filters.SearchFilter)
    # search_fields = ("title","message",)

    # 只能对收件人为自己的信息进行操作   不可以，因为如果这样就无法查看自己发出的消息
    # 因此在前端带着过滤字段来请求，sendUser和receiveUser等于请求用户来查看自己收到的和自己发送的
    def get_queryset(self):
        return userMessage.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return userMessageDetailSerializer
        return userMessageSerializer

    # 用户查看一条信息时，该消息置为已读，但不会同时赋予该条物证的权限，而是点击允许授权才会授权
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # # 判断是否为空值用is None
        # # 如果发送者（请求者）是普通用户，而接受者（被请求者）是管理员或者超级管理员，才会去创建权限
        # if instance.sendUser.role == 3 and instance.receiveUser.role <= 2:
        #     # 如果消息中的炸药id和爆炸装置id都不为空才会创建一条权限机制
        #     if (instance.exploEviId is not None) or (instance.devEviId is not None):
        #     # ifinstance.exploEviId!= NULL)and (instance.devEviId == NULL)):
        #     # 第一次读的时候，即此时hasRead = False，这时候才去创建权限记录。
        #         if instance.hasRead == False:
        #             # 可能重复哦
        #             allow_Update = allowUpdate()
        #             allow_Update.entitled = instance.sendUser
        #             allow_Update.authorized = instance.receiveUser
        #             allow_Update.exploEviId = instance.exploEviId
        #             allow_Update.devEviId = instance.devEviId
        #             allow_Update.save()
        if instance.receiveUser == request.user:
            instance.hasRead = True
            instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class allowUpdateViewset(viewsets.ModelViewSet):
    """
   前端需要判断如果发送者（请求者）是普通用户，而接受者（被请求者）是管理员或者超级管理员，才会去创建权限
   这时当用户点击允许授权时会来请求这个新建接口
    """
 #   authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
#    lookup_field = "goods_id"
    permission_classes = (IsAuthenticated, IsAdmin)
    def get_queryset(self):
        return allowUpdate.objects.all()

    def get_serializer_class(self):
        return allowUpdateSerializer

    def perform_create(self, serializer):
        serializer.save()