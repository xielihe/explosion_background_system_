# -*- coding: utf-8 -*-
import re
from rest_framework import serializers
from datetime import datetime
from datetime import timedelta
from rest_framework.validators import UniqueValidator

from apps.user_operation.models import *
from apps.basic.serializers import *

class userMessageDetailSerializer(serializers.ModelSerializer):
    sendUser = UserDetailSerializer()
    receiveUser = UserDetailSerializer()
    # 这么设置sendDate不会随着调用Serializer而更新，且会限制格式
    sendDate = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = userMessage
        fields = "__all__"


class userMessageSerializer(serializers.ModelSerializer):
    sendUser = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    sendDate = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = userMessage
        fields = "__all__"

class allowUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = allowUpdate
        fields = "__all__"