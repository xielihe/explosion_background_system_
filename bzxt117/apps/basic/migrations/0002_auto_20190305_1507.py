# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-03-05 07:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='picUrl',
            field=models.ImageField(blank=True, max_length=300, null=True, upload_to='image/user/', verbose_name='头像路径'),
        ),
    ]