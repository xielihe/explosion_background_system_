# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-03-26 10:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0002_auto_20190305_0008'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='devshapematch',
            name='matchPicURL',
        ),
        migrations.AddField(
            model_name='devshapematch',
            name='matchRadius',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='匹配的半径长度'),
        ),
    ]
