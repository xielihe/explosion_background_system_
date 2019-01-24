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
import docx
import datetime
import time
import pytz
from django_filters.rest_framework import DjangoFilterBackend


from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler

from apps.basic.models import *
from apps.basic.serializers import *
from apps.utils.permissions import *
from apps.basic.filters import *
from apps.match.views import *
from apps.sample.models import *


def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    """
    # 在更新最后登录时间之前比较，分两类，炸药和爆炸装置的
    oldLastLogin = user.last_login
    if oldLastLogin == None:
        oldLastLogin = datetime.min.replace(tzinfo=pytz.timezone('Asia/Shanghai'))
    # print(datetime.min)
    # # 记得要加时区，datetime的min是不含时区的
    # minTime = datetime.min.replace(tzinfo=pytz.timezone('Asia/Shanghai'))
    # if oldLastLogin > minTime:
    #     print('True')

    if exploSample.objects.all().count() >0 :
        exploSampleLast = exploSample.objects.all().order_by('-inputDate')[0].inputDate
    else:
        exploSampleLast = datetime.min.replace(tzinfo=pytz.timezone('Asia/Shanghai'))

    if exploSampleFTIR.objects.all().count() >0 :
        exploSampleFTIRLast = exploSampleFTIR.objects.all().order_by('-inputDate')[0].inputDate
    else:
        exploSampleFTIRLast = datetime.min.replace(tzinfo=pytz.timezone('Asia/Shanghai'))

    if exploSampleRaman.objects.all().count() >0:
        exploSampleRamanLast =exploSampleRaman.objects.all().order_by('-inputDate')[0].inputDate
    else:
        exploSampleRamanLast = datetime.min.replace(tzinfo=pytz.timezone('Asia/Shanghai'))

    if exploSampleXRD.objects.all().count() >0:
        exploSampleXRDLast = exploSampleXRD.objects.all().order_by('-inputDate')[0].inputDate
    else:
        exploSampleXRDLast = datetime.min.replace(tzinfo=pytz.timezone('Asia/Shanghai'))

    if exploSampleXRF.objects.all().count() >0:
        exploSampleXRFLast = exploSampleXRF.objects.all().order_by('-inputDate')[0].inputDate
    else:
        exploSampleXRFLast = datetime.min.replace(tzinfo=pytz.timezone('Asia/Shanghai'))

    if exploSampleGCMS.objects.all().count() >0:
        exploSampleGCMSLast = exploSampleGCMS.objects.all().order_by('-inputDate')[0].inputDate
    else:
        exploSampleGCMSLast = datetime.min.replace(tzinfo=pytz.timezone('Asia/Shanghai'))


    if oldLastLogin < exploSampleLast or oldLastLogin < exploSampleFTIRLast or oldLastLogin < exploSampleRamanLast or oldLastLogin < exploSampleXRDLast or oldLastLogin < exploSampleXRFLast or oldLastLogin < exploSampleGCMSLast:
        exploUpdate = True
    else:
        exploUpdate = False

    if devSample.objects.all().count()>0:
        devSampleLast = devSample.objects.all().order_by('-inputDate')[0].inputDate
    else:
        devSampleLast = datetime.min.replace(tzinfo=pytz.timezone('Asia/Shanghai'))

    if devPartSample.objects.all().count() >0:
        devPartSampleLast = devPartSample.objects.all().order_by('-inputDate')[0].inputDate
    else:
        devPartSampleLast = datetime.min.replace(tzinfo=pytz.timezone('Asia/Shanghai'))

    if devPartSampleFTIR.objects.all().count() >0:
        devPartSampleFTIRLast = devPartSampleFTIR.objects.all().order_by('-inputDate')[0].inputDate
    else:
        devPartSampleFTIRLast = datetime.min.replace(tzinfo=pytz.timezone('Asia/Shanghai'))

    if devPartSampleRaman.objects.all().count() >0:
        devPartSampleRamanLast = devPartSampleRaman.objects.all().order_by('-inputDate')[0].inputDate
    else:
        devPartSampleRamanLast = datetime.min.replace(tzinfo=pytz.timezone('Asia/Shanghai'))

    if devPartSampleXRF.objects.all().count() >0:
        devPartSampleXRFLast = devPartSampleXRF.objects.all().order_by('-inputDate')[0].inputDate
    else:
        devPartSampleXRFLast = datetime.min.replace(tzinfo=pytz.timezone('Asia/Shanghai'))

    if devShapeSample.objects.all().count() >0:
        devShapeSampleLast = devShapeSample.objects.all().order_by('-inputDate')[0].inputDate
    else:
        devShapeSampleLast = datetime.min.replace(tzinfo=pytz.timezone('Asia/Shanghai'))

    if PCBImgSample.objects.all().count() >0:
        PCBImgSampleLast = PCBImgSample.objects.all().order_by('-inputDate')[0].inputDate
    else:
        PCBImgSampleLast = datetime.min.replace(tzinfo=pytz.timezone('Asia/Shanghai'))

    if oPartImgSample.objects.all().count() >0:
        oPartImgSampleLast = oPartImgSample.objects.all().order_by('-inputDate')[0].inputDate
    else:
        oPartImgSampleLast = datetime.min.replace(tzinfo=pytz.timezone('Asia/Shanghai'))

    if logoImgSample.objects.all().count()>0:
        logoImgSampleLast = logoImgSample.objects.all().order_by('-inputDate')[0].inputDate
    else:
        logoImgSampleLast = datetime.min.replace(tzinfo=pytz.timezone('Asia/Shanghai'))


    if oldLastLogin < devSampleLast or oldLastLogin < devPartSampleLast or oldLastLogin <devPartSampleFTIRLast or oldLastLogin < devPartSampleRamanLast or oldLastLogin < devPartSampleXRFLast or oldLastLogin < devShapeSampleLast or oldLastLogin < PCBImgSampleLast or oldLastLogin < oPartImgSampleLast or oldLastLogin <logoImgSampleLast:
        devUpdate = True
    else:
        devUpdate = False
    # 返回之前记录用户最后登陆时间,django默认只会记录登陆后台管理系统最后时间,JWT不记录
    user.last_login = datetime.now().strftime('%Y-%m-%d %H:%M')
    # 存的格式都一样，只是显示的格式不同而已
    user.save()
    return {
        'token': token,
        'username': user.username,
        'exploUpdate':exploUpdate,
        'devUpdate':devUpdate
    }

# Create your views here.
class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            users = userProfile.objects.filter(isDelete=False)
            user = users.get(username=username)
            if user.check_password(password):
                return user
        except Exception as e:
            return None

class UserViewset(viewsets.ModelViewSet):
    """
    用户
    """
    # 更新也用这个Serilizer，保证了更新时用户名，即手机号的唯一性
    # serializer_class = UserRegSerializer
    queryset = userProfile.objects.all()
    pagination_class = MyPageNumberPagination
    # 查看详情时不是id而是用户名
    lookup_field = "username"
    permission_classes = (IsAuthenticated,IsSuperAdmin,)
    filter_backends = (DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter)
    filter_class = userFilter
    search_fields = ("name","phone","email", "unit","department","posts","note")
    ordering_fields = ("id",)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        return  UserRegSerializer
    def get_permissions(self):
        if self.action == "retrieve" or self.action =="list":
            return [IsAuthenticated(),]
        else:
            return [IsAuthenticated(),IsSuperAdmin(),]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        # 注意！这里不是每次登陆的时候的过程，而是创建新用户的时候的逻辑！
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["username"] = user.username
        re_dict["name"] = user.name #if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)


    def perform_create(self, serializer):
        return serializer.save()


    def perform_update(self, serializer):
        if ('password' in serializer.validated_data.keys()):
            password =serializer.validated_data['password']
            user = self.get_object()
            user.set_password(password)
            serializer.validated_data['password'] = user.password
        serializer.save()

    def perform_destroy(self, instance):
        instance.isDelete = True
        instance.save()

class methodDetectViewset(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    """
 #   authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
#    lookup_field = "goods_id"
    permission_classes = (IsAuthenticated, IsAdmin)
    pagination_class = MyPageNumberPagination
    def get_queryset(self):
        return methodDetect.objects.all()

    def get_serializer_class(self):
        return methodDetectSerializer

    def perform_create(self, serializer):
        return serializer.save()

class devDetectViewset(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    """
 #   authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
#    lookup_field = "goods_id"
    permission_classes = (IsAuthenticated, IsAdmin)
    pagination_class = MyPageNumberPagination
    def get_queryset(self):
        return devDetect.objects.all()

    def get_serializer_class(self):
        return devDetectSerializer