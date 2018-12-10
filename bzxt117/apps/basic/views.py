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
from django_filters.rest_framework import DjangoFilterBackend


from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler

from apps.basic.models import *
from apps.basic.serializers import *
from apps.utils.permissions import *
from apps.basic.filters import *
from apps.match.views import *

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
    serializer_class = UserRegSerializer
    queryset = userProfile.objects.all()
    pagination_class = MyPageNumberPagination
    # 查看详情时不是id而是用户名
    lookup_field = "username"
    permission_classes = (IsAuthenticated,IsSuperAdmin,)
    filter_backends = (DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter)
    filter_class = userFilter
    search_fields = ("name","phone","email", "unit","department","posts","note")
    ordering_fields = ("id",)
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
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username

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
#     permission_classes = (IsAuthenticated, IsAdmin)
    pagination_class = MyPageNumberPagination
    def get_queryset(self):
        return methodDetect.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return methodDetectCreateSerializer
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