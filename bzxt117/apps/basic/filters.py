# -*- coding: utf-8 -*-
__author__ = 'bobby'

import django_filters
from django.db.models import Q

from apps.basic.models import userProfile


class userFilter(django_filters.rest_framework.FilterSet):
    """
    过滤类
    """
    class Meta:
        model = userProfile
        fields = ['isDelete']