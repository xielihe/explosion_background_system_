from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

# Create your models here.
class userProfile(AbstractUser):
    """
    人员信息表
    """
    ROLE_TYPE = (
        (1, "超级管理员"),
        (2, "管理员"),
        (3, "普通用户"),
        (4, "专家"),
    )
    name = models.CharField(max_length=20,verbose_name="人员姓名")
    # mobile = models.CharField(max_length=11,null=True, blank=True,verbose_name="手机（登录）")
    phone = models.CharField(max_length=20,null=True, blank=True,verbose_name="固话（查询）")
    email = models.EmailField(max_length=50, null=True, blank=True, verbose_name="邮箱")
    unit = models.EmailField(max_length=40, null=True, blank=True, verbose_name="单位")
    department = models.EmailField(max_length=40, null=True, blank=True, verbose_name="部门")
    posts = models.EmailField(max_length=40, null=True, blank=True, verbose_name="职务")
    role = models.IntegerField(choices=ROLE_TYPE,default=3, verbose_name="权限标识", help_text="权限标识")
    isDelete =models.BooleanField(default=False,verbose_name="是否逻辑删除")
    picUrl =models.ImageField(max_length=300,upload_to="image/user/",null=True,blank=True,verbose_name="头像路径")
    note =models.CharField(max_length=200,null=True,blank=True,verbose_name="备注")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"

    def __str__(self):
        return self.name


class methodDetect(models.Model):
    """
    检测方法信息表
    """
    method = models.CharField(max_length=100, null=True, blank=True, verbose_name="方法")
    txtURL = models.FileField(max_length=300, upload_to="file/methodDetect/", null=True, blank=True,
                              verbose_name="检测方法信息文档路径")

    class Meta:
        verbose_name = "检测方法信息表 "
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.method

class devDetect(models.Model):
    """
    检测设备信息表
    """
    deviceName= models.CharField(max_length=30, null=True, blank=True, verbose_name="检测设备名称")
    deviceVersion = models.CharField(max_length=30, null=True, blank=True, verbose_name="检测设备型号")
    detectMrfs = models.CharField(max_length=100, null=True, blank=True, verbose_name="仪器厂家")
    note = models.CharField(max_length=400, null=True, blank=True, verbose_name="备注")
    class Meta:
        verbose_name = "检测设备信息表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.deviceName