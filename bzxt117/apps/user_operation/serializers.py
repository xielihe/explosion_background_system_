# -*- coding: utf-8 -*-
import re
from rest_framework import serializers
from datetime import datetime
from datetime import timedelta
from rest_framework.validators import UniqueValidator

from apps.user_operation.models import *
from apps.basic.serializers import *

class userMessageSerializer(serializers.ModelSerializer):
    sendUser = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    sendDate = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = userMessage
        fields = "__all__"


class userMessageFileSerializer(serializers.ModelSerializer):

    def __str__(self):
        return self.txtURL

    class Meta:
        model = userMessageFile
        fields = "__all__"

class LsituserMessageFileSerializer(serializers.Serializer):
    messageFiles = serializers.ListField(
        child=serializers.FileField(max_length=100000, allow_empty_file=False, use_url=True),
        write_only=True )
    userMessage = serializers.PrimaryKeyRelatedField(required=True, write_only=True,queryset=userMessage.objects.all())

    def create(self, validated_data):
        messageFiles = validated_data.get('messageFiles')
        userMessage = validated_data.get('userMessage')
        result = []
        for index, url in enumerate(messageFiles):
            messageFile = userMessageFile.objects.create(txtURL=url,userMessage = userMessage)
            messageFile.save()
        return {}

class userMessageDetailSerializer(serializers.ModelSerializer):
    sendUser = UserDetailSerializer()
    receiveUser = UserDetailSerializer()
    # 这么设置sendDate不会随着调用Serializer而更新，且会限制格式
    handleUer = UserDetailSerializer()
    sendDate = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    MessageFiles = userMessageFileSerializer(many=True)

    class Meta:
        model = userMessage
        fields = ("sendUser","receiveUser","title","message","exploEviId","devEviId","hasRead","hasHandle","handleUser","sendDate","MessageFiles")



# class userMessageTestSerializer(serializers.ModelSerializer):
#     sendUser = UserDetailSerializer()
#     receiveUser = UserDetailSerializer()
#     # 这么设置sendDate不会随着调用Serializer而更新，且会限制格式
#     handleUser = UserDetailSerializer()
#     sendDate = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
#     # MessageFiles = userMessageFileSerializer(many=True)
#
#     MessageFiles = serializers.SerializerMethodField(read_only=True, )
#
#     def get_MessageFiles(self, obj):
#         # self就一堆了。。。
#         park = userProfile.objects.all()
#         return UserDetailSerializer(park, many=True).data
#     class Meta:
#         model = userMessage
#         fields = ("sendUser","receiveUser","title","message","exploEviId","devEviId","hasRead","hasHandle","handleUser","sendDate","MessageFiles")