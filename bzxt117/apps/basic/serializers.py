# -*- coding: utf-8 -*-
import re
from rest_framework import serializers
from datetime import datetime
from datetime import timedelta
from rest_framework.validators import UniqueValidator
import docx
import numpy as np
import os

from apps.basic.models import *
from bzxt117.settings import MEDIA_ROOT

class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化类
    """

    class Meta:
        model = userProfile
        fields = "__all__"

class UserRegSerializer(serializers.ModelSerializer):
    # username=mobile
    username = serializers.CharField(label="手机", help_text="手机", required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=userProfile.objects.all(), message="该手机已被注册过")])

    password = serializers.CharField(
        style={'input_type': 'password'},help_text="密码", label="密码",# write_only=True,
    )

    def validate_role(self, role):
        # 注意参数，self以及字段名
        # 注意函数名写法，validate_ + 字段名字
        if self.context["request"].user.role == 3:
            raise serializers.ValidationError("您没有执行该操作的权限。")
        elif self.context["request"].user.role == 2 and role != 3:
            raise serializers.ValidationError("您没有执行该操作的权限。")
        else:
            return role

    # def validate(self, attrs):
    #     attrs["mobile"] = attrs["username"]
    #     return attrs

    # save方法掉的create函数
    def create(self, validated_data):
        user = super(UserRegSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    # def update(self, instance, validated_data):
    #     user = super(UserRegSerializer, self).create(validated_data=validated_data)
    #     password = user.set_password(validated_data["password"])
    #     validated_data["password"] = password
    #     instance.save()

    class Meta:
        model = userProfile
        fields = ("id","name","username","password","phone","email","unit","department","posts","role","isDelete","picUrl","note")

class methodDetectSerializer(serializers.ModelSerializer):
    handledData = serializers.SerializerMethodField()

    def get_handledData(self, obj):
        path = os.path.join(MEDIA_ROOT, "GCMS.npy")
        data = np.load(path).item()
        # print(type(data))
        # print(data[0])

        return data
    class Meta:
        model = methodDetect
        fields = ("id","method","handledData")

class methodDetectCreateSerializer(serializers.Serializer):
    fileDoc = serializers.FileField(write_only=True,)


    def create(self, validated_data):
        doc = validated_data['fileDoc']
        file = docx.Document(doc)
        for para in file.paragraphs:
            data = para.text.strip()
            if len(data)!=0:
                methodCreate = methodDetect.objects.get_or_create(method = para.text)
                # methodSE = methodDetectSerializer(methodCreate,context=self.context)
        return {'state':"over"}


class devDetectSerializer(serializers.ModelSerializer):
    class Meta:
        model = devDetect
        fields = "__all__"