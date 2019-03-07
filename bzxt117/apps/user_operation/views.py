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
import pytz
import datetime
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
        # elif self.action == "list":
        #     return userMessageTestSerializer
        return userMessageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({
            "isSend": True,
        }, status=status.HTTP_201_CREATED)
        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        message1 = serializer.save()
        if self.request.user.role == 3:
            # 普通用户发送信息默认的是全体管理员和专家，如果不是普通用户则正常建立
            experts = userProfile.objects.filter(Q(role =2)| Q(role = 4))
            for expert in experts:
                userMess = userMessage()
                userMess.sendUser = message1.sendUser
                userMess.receiveUser = expert
                userMess.title = message1.title
                userMess.message = message1.message
                userMess.exploEviId = message1.exploEviId
                userMess.devEviId = message1.devEviId
                userMess.hasRead = message1.hasRead
                userMess.hasHandle = message1.hasHandle
                userMess.sendDate = message1.sendDate
                userMess.save()
            message1.delete()

    def perform_update(self, serializer):
        # 更新的时候只要有一个handle其余该标题和用户的消息全置为已处理。
        if ('hasHandle' in serializer.validated_data.keys()):
            userMess = self.get_object()
            Messs = userMessage.objects.filter(title = userMess.title,sendUser = userMess.sendUser)
            userMess.handleUser = self.request.user
            userMess.save()
            for Mess in Messs:
                Mess.hasHandle = True
                Mess.handleUser = self.request.user
                Mess.save()
            # user.set_password(password)
            # serializer.validated_data['password'] = user.password
        serializer.save()


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
        if instance.receiveUser == request.user:
            instance.hasRead = True
            instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

# 判断消息是否更新
class messageUpdate(APIView):
    def get(self,request):
        receiver = request.user
        if userMessage.objects.filter(receiveUser = receiver).count()>0:
            lastMessage = userMessage.objects.filter(receiveUser = receiver,hasRead = False,hasHandle = False).order_by('-sendDate')[0].sendDate
        else:
            lastMessage = datetime.min.replace(tzinfo=pytz.timezone('Asia/Shanghai'))
        # tempTime = datetime.now() -timedelta(minutes=3)


        if (datetime.now() -timedelta(minutes=3)).replace(tzinfo=pytz.timezone('Asia/Shanghai'))<= lastMessage:
            isUpdate = True
        else:
            isUpdate = False
        return Response({
            "isMessageUpdate": isUpdate,
        }, status=status.HTTP_200_OK)

class userMessageFileViewset(viewsets.ModelViewSet):
    queryset = userMessageFile.objects.all()
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FileUploadParser,)
    pagination_class = MyPageNumberPagination
    def get_serializer_class(self):
        if self.action == "create":
            return LsituserMessageFileSerializer
        return userMessageFileSerializer

