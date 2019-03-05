# _*_ encoding:utf-8 _*_
from datetime import datetime
import os

from django.db import models
from apps.basic.models import *

# Create your models here.
class exploSample(models.Model):
    """
    炸药及原材料常见样本表
    """

    sname =models.CharField(max_length=30,verbose_name="样本名称")
    snameAbbr =models.CharField(max_length=20,null=True, blank=True,verbose_name="样本名称缩写")
    user = models.ForeignKey(userProfile, verbose_name=u"处理人员")
    inputDate = models.DateTimeField(default=datetime.now, verbose_name=u"录入日期")
    sampleOrigin =models.CharField(max_length=100,null=True, blank=True,verbose_name="样本产地")
    factory =models.CharField(max_length=100, null=True, blank=True,verbose_name="样本厂家")
    picUrl =models.ImageField(max_length=300,upload_to="image/exploSample/",null=True,blank=True,verbose_name="炸药外观图片路径")
    note = models.CharField(max_length=200, null=True, blank=True, verbose_name="备注")
    class Meta:
        verbose_name = "炸药及原材料常见样本表"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.sname


class exploSampleFTIR(models.Model):
    """
    炸药及原材料样本FTIR检测表
    """
    exploSample = models.ForeignKey(exploSample, verbose_name=u"对应的炸药样本",related_name="exploSampleFTIR")
    devDetect = models.ForeignKey(devDetect, verbose_name=u"对应的检测设备")
    methodDetect = models.ForeignKey(methodDetect, verbose_name=u"对应的检测方法")
    user = models.ForeignKey(userProfile, verbose_name=u"处理人员")
    inputDate = models.DateTimeField(default=datetime.now, verbose_name=u"录入日期")

    class Meta:
        verbose_name = "炸药及原材料样本FTIR检测表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s,FTIR" %(self.exploSample.sname,)


class exploSampleFTIRTestFile(models.Model):
    """
   炸药及原材料样本FTIR检测实验文件表
    """
    exploSampleFTIR = models.ForeignKey(exploSampleFTIR, verbose_name=u"对应的FTIR检测",related_name="exploSampleFTIRTestFile")
    txtURL = models.FileField(max_length=300, upload_to="file/exploSampleFTIRTestFile/", null=True, blank=True,
                              verbose_name="录入TXT文档路径")
    txtHandledURL = models.CharField(max_length=300, null=True, blank=True, verbose_name="处理过的TXT文档路径")

    class Meta:
        verbose_name = "炸药及原材料样本FTIR检测表"
        verbose_name_plural = verbose_name


class exploSampleRaman(models.Model):
    """
    炸药及原材料样本Raman检测表
    """
    exploSample = models.ForeignKey(exploSample, verbose_name=u"对应的炸药样本",related_name="exploSampleRaman")
    devDetect = models.ForeignKey(devDetect, verbose_name=u"对应的检测设备")
    methodDetect = models.ForeignKey(methodDetect, verbose_name=u"对应的检测方法")
    user = models.ForeignKey(userProfile, verbose_name=u"处理人员")
    inputDate = models.DateTimeField(default=datetime.now, verbose_name=u"录入日期")

    class Meta:
        verbose_name = "炸药及原材料样本Raman检测表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s,Raman" %(self.exploSample.sname,)

class exploSampleRamanTestFile(models.Model):
    """
   炸药及原材料样本Raman检测实验文件表
    """
    exploSampleRaman = models.ForeignKey(exploSampleRaman, verbose_name=u"对应的Raman检测",related_name="exploSampleRamanTestFile")
    txtURL = models.FileField(max_length=300, upload_to="file/exploSampleRamanTestFile/", null=True, blank=True,
                              verbose_name="录入TXT文档路径")
    txtHandledURL = models.CharField(max_length=300, null=True, blank=True, verbose_name="处理过的TXT文档路径")

    class Meta:
        verbose_name = "炸药及原材料样本Raman检测实验文件表 "
        verbose_name_plural = verbose_name


class exploSampleXRD(models.Model):
    """
   炸药及原材料样本XRD检测表
    """
    exploSample = models.ForeignKey(exploSample, verbose_name=u"对应的炸药样本",related_name="exploSampleXRD")
    devDetect = models.ForeignKey(devDetect, verbose_name=u"对应的检测设备")
    methodDetect = models.ForeignKey(methodDetect, verbose_name=u"对应的检测方法")
    user = models.ForeignKey(userProfile, verbose_name=u"处理人员")
    inputDate = models.DateTimeField(default=datetime.now, verbose_name=u"录入日期")

    class Meta:
        verbose_name = "炸药及原材料样本XRD检测表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s,XRD" %(self.exploSample.sname,)

class exploSampleXRDTestFile(models.Model):
    """
   炸药及原材料样本XRD检测实验文件表
    """
    exploSampleXRD = models.ForeignKey(exploSampleXRD, verbose_name=u"对应的XRD检测",related_name="exploSampleXRDTestFile")
    txtURL = models.FileField(max_length=300, upload_to="file/exploSampleXRDTestFile/", null=True, blank=True,
                              verbose_name="录入TXT文档路径")
    txtHandledURL = models.CharField(max_length=300, null=True, blank=True, verbose_name="处理过的TXT文档路径")

    class Meta:
        verbose_name = "炸药及原材料样本XRD检测实验文件表 "
        verbose_name_plural = verbose_name


class exploSampleXRF(models.Model):
    """
   炸药及原材料样本XRF检测表
    """
    exploSample = models.ForeignKey(exploSample, verbose_name=u"对应的炸药样本",related_name="exploSampleXRF")
    devDetect = models.ForeignKey(devDetect, verbose_name=u"对应的检测设备")
    methodDetect = models.ForeignKey(methodDetect, verbose_name=u"对应的检测方法")
    user = models.ForeignKey(userProfile, verbose_name=u"处理人员")
    inputDate = models.DateTimeField(default=datetime.now, verbose_name=u"录入日期")

    class Meta:
        verbose_name = "炸药及原材料样本XRF检测表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s,XRF" %(self.exploSample.sname,)

class exploSampleXRFTestFile(models.Model):
    """
   炸药及原材料样本XRF检测实验文件表
    """
    exploSampleXRF = models.ForeignKey(exploSampleXRF, verbose_name=u"对应的XRF检测",related_name="exploSampleXRFTestFile")
    excelURL = models.FileField(max_length=300, upload_to="file/exploSampleXRFTestFile/", null=True, blank=True,
                              verbose_name="录入excel文档路径")
    handledURL = models.CharField(max_length=300,null=True, blank=True,verbose_name="有效元素列表")
    class Meta:
        verbose_name = "炸药及原材料样本XRF检测实验文件表"
        verbose_name_plural = verbose_name

class exploSampleGCMS(models.Model):
    """
   炸药及原材料样本GC-MS检测表
    """
    exploSample = models.ForeignKey(exploSample, verbose_name=u"对应的炸药样本",related_name="exploSampleGCMS")
    devDetect = models.ForeignKey(devDetect, verbose_name=u"对应的检测设备")
    methodDetect = models.ForeignKey(methodDetect, verbose_name=u"对应的检测方法")
    user = models.ForeignKey(userProfile, verbose_name=u"处理人员")
    inputDate = models.DateTimeField(default=datetime.now, verbose_name=u"录入日期")

    class Meta:
        verbose_name = "炸药及原材料样本GC-MS检测表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s,GCMS" %(self.exploSample.sname,)

class exploSampleGCMSFile(models.Model):
    """
    炸药及原材料样本GC-MS检测文件表
    """
    exploSampleGCMS = models.ForeignKey(exploSampleGCMS, verbose_name=u"对应的GC-MS检测",related_name="exploSampleGCMSFile")
    txtHandledURL = models.CharField(max_length=300, null=True, blank=True, verbose_name="处理过的TXT文档路径")

    class Meta:
        verbose_name = "炸药及原材料样本GC-MS检测文件表 "
        verbose_name_plural = verbose_name

class exploSampleGCMSTestFile(models.Model):
    """
    炸药及原材料样本GC-MS检测实验文件表
    """
    exploSampleGCMS = models.ForeignKey(exploSampleGCMS, verbose_name=u"对应的GC-MS检测",related_name="exploSampleGCMSTestFile")
    type =models.CharField(max_length=20,default="TIC",verbose_name="类型（TIC。。。）")
    txtURL = models.FileField(max_length=300, upload_to="file/exploSampleGCMSTestFile/", null=True, blank=True,
                              verbose_name="录入TXT文档路径")

    class Meta:
        verbose_name = "炸药及原材料样本GC-MS检测实验文件表 "
        verbose_name_plural = verbose_name



class devSample(models.Model):
    """
    爆炸装置常见样本成分表
    """
    DEV_TYPE = (
        (1, "能源"),
        (2, "控制系统"),
        (3, "连接系统"),
        (4,"起爆装置"),
        (5,"包装物"),
    )
    sname = models.CharField(max_length=30, verbose_name="组件名称")
    user = models.ForeignKey(userProfile, verbose_name=u"处理人员")
    inputDate = models.DateTimeField(default=datetime.now, verbose_name=u"录入日期")
    Type = models.IntegerField(choices=DEV_TYPE, default=1, verbose_name="组件类型分组（1-5，能源、控制系统、连接系统、起爆系统、包装物）", help_text="组件类型分组（1-5，能源、控制系统、连接系统、起爆系统、包装物）")
    Origin =models.CharField(max_length=100,null=True, blank=True,verbose_name="组件产地")
    Factory =models.CharField(max_length=100, null=True, blank=True,verbose_name="组件厂家")
    Model =models.CharField(max_length=30, null=True, blank=True,verbose_name="组件型号")
    Logo =models.CharField(max_length=100,null=True, blank=True, verbose_name="组件商标")
    function =models.CharField(max_length=200,null=True, blank=True, verbose_name="组件功能")
    picUrl = models.ImageField(max_length=300, upload_to="image/devSample/", null=True, blank=True, verbose_name="组件外观图像路径")
    note = models.CharField(max_length=500, null=True, blank=True, verbose_name="备注")
    #isDelete = models.BooleanField(default=False, verbose_name="是否逻辑删除")
    class Meta:
        verbose_name = "爆炸装置关键组件样本基本信息表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.sname

class devPartSample(models.Model):
    """
    爆炸装置关键组件的零件（包括电路板）样本基本信息表
    """
    SAMPLE_TYPE = (
        (1, "外壳"),
        (2, "零件"),
        (3, "电路板"),
        (4,"Logo"),
    )
    sname = models.CharField(max_length=30, verbose_name="零件名称")
    devSample = models.ForeignKey(devSample, verbose_name=u"所属组件", related_name="devPartSample",
                                      )#on_delete=models.CASCADE
    user = models.ForeignKey(userProfile, verbose_name=u"处理人员")
    inputDate = models.DateTimeField(default=datetime.now, verbose_name=u"录入日期")
    sampleType = models.IntegerField(choices=SAMPLE_TYPE, default=4, verbose_name="零件类型（1-4，外壳，零件，电路板，Logo）", help_text="零件类型（1-4，外壳，零件，电路板，Logo）")
    Origin = models.CharField(max_length=100, null=True, blank=True, verbose_name="零件产地")
    Factory =models.CharField(max_length=100, null=True, blank=True,verbose_name="零件厂家")
    Model =models.CharField(max_length=30, null=True, blank=True,verbose_name="零件型号")
    Logo =models.CharField(max_length=100,null=True, blank=True, verbose_name="零件商标")
    function =models.CharField(max_length=100,null=True, blank=True, verbose_name="零件功能")
    Color = models.CharField(max_length=10, null=True, blank=True, verbose_name="零件颜色")
    Material =models.CharField(max_length=10, null=True, blank=True,verbose_name="零件材质")
    Shape =models.CharField(max_length=10, null=True, blank=True,verbose_name="零件形状")
    thickness =models.CharField(max_length=50,null=True, blank=True, verbose_name="厚度（边角）")
    picUrl = models.ImageField(max_length=300, upload_to="image/devPartSample/", null=True, blank=True, verbose_name="零件外观图像路径")
    note = models.CharField(max_length=500, null=True, blank=True, verbose_name="备注")
    #isDelete = models.BooleanField(default=False, verbose_name="是否逻辑删除")
    class Meta:
        verbose_name = "爆炸装置关键组件的零件（包括电路板）样本基本信息表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.sname

class devPartSampleFTIR(models.Model):
    """
    爆炸装置关键组件样本零件FTIR检测表
    """
    devPartSample = models.ForeignKey(devPartSample, verbose_name=u"对应的爆炸装置零件样本",related_name="devPartSampleFTIR")
    devDetect = models.ForeignKey(devDetect, verbose_name=u"对应的检测设备")
    methodDetect = models.ForeignKey(methodDetect, verbose_name=u"对应的检测方法")
    user = models.ForeignKey(userProfile, verbose_name=u"处理人员")
    inputDate = models.DateTimeField(default=datetime.now, verbose_name=u"录入日期")

    class Meta:
        verbose_name = "爆炸装置关键组件样本零件FTIR检测表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s,FTIR" %(self.devPartSample.sname,)


class devPartSampleFTIRTestFile(models.Model):
    """
   爆炸装置关键组件样本零件FTIR检测实验文件表
    """
    devPartSampleFTIR = models.ForeignKey(devPartSampleFTIR, verbose_name=u"对应的FTIR检测",related_name="devPartSampleFTIRTestFile")
    txtURL = models.FileField(max_length=300, upload_to="file/devPartSampleFTIRTestFile/", null=True, blank=True,
                              verbose_name="录入TXT文档路径")
    txtHandledURL = models.CharField(max_length=300, null=True, blank=True, verbose_name="处理过的TXT文档路径")

    class Meta:
        verbose_name = "爆炸装置关键组件样本零件FTIR检测实验文件表"
        verbose_name_plural = verbose_name


class devPartSampleRaman(models.Model):
    """
    爆炸装置关键组件样本零件Raman检测表
    """
    devPartSample = models.ForeignKey(devPartSample, verbose_name=u"对应的爆炸装置零件样本",related_name="devPartSampleRaman")
    devDetect = models.ForeignKey(devDetect, verbose_name=u"对应的检测设备")
    methodDetect = models.ForeignKey(methodDetect, verbose_name=u"对应的检测方法")
    user = models.ForeignKey(userProfile, verbose_name=u"处理人员")
    inputDate = models.DateTimeField(default=datetime.now, verbose_name=u"录入日期")

    class Meta:
        verbose_name = "爆炸装置关键组件样本零件Raman检测表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s,Raman" %(self.devPartSample.sname,)


class devPartSampleRamanTestFile(models.Model):
    """
   爆炸装置关键组件样本零件Raman检测实验文件表
    """
    devPartSampleRaman = models.ForeignKey(devPartSampleRaman, verbose_name=u"对应的Raman检测",related_name="devPartSampleRamanTestFile")
    txtURL = models.FileField(max_length=300, upload_to="file/devPartSampleRamanTestFile/", null=True, blank=True,
                              verbose_name="录入TXT文档路径")
    txtHandledURL = models.CharField(max_length=300, null=True, blank=True, verbose_name="处理过的TXT文档路径")

    class Meta:
        verbose_name = "爆炸装置关键组件样本零件Raman检测实验文件表  "
        verbose_name_plural = verbose_name


class devPartSampleXRF(models.Model):
    """
   爆炸装置关键组件样本零件XRF检测表
    """
    devPartSample = models.ForeignKey(devPartSample, verbose_name=u"对应的爆炸装置零件样本",related_name="devPartSampleXRF")
    devDetect = models.ForeignKey(devDetect, verbose_name=u"对应的检测设备")
    methodDetect = models.ForeignKey(methodDetect, verbose_name=u"对应的检测方法")
    user = models.ForeignKey(userProfile, verbose_name=u"处理人员")
    inputDate = models.DateTimeField(default=datetime.now, verbose_name=u"录入日期")

    class Meta:
        verbose_name = "爆炸装置关键组件样本零件XRF检测表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s,XRF" %(self.devPartSample.sname,)


class devPartSampleXRFTestFile(models.Model):
    """
   爆炸装置关键组件样本零件XRF检测实验文件表
    """
    devPartSampleXRF = models.ForeignKey(devPartSampleXRF, verbose_name=u"对应的XRF检测",related_name="devPartSampleXRFTestFile")
    excelURL = models.FileField(max_length=300, upload_to="file/devPartSampleXRFTestFile/", null=True, blank=True,
                              verbose_name="录入excel文档路径")
    handledURL = models.CharField(max_length=300, null=True, blank=True, verbose_name="有效元素列表")
    class Meta:
        verbose_name = "爆炸装置关键组件样本零件XRF检测实验文件表"
        verbose_name_plural = verbose_name

class devShapeSample(models.Model):
    """
    原来的爆炸装置常见样本形态表
    """
    SIDE_TYPE = (
        (1, "正面"),
        (2, "反面"),
    )
    # isCircuit =models.BooleanField(default=False, verbose_name="是否是电路板")
    devPartSample = models.ForeignKey(devPartSample, verbose_name="所属零件",related_name="devShapeSample")
    user = models.ForeignKey(userProfile, verbose_name=u"处理人员")
    inputDate = models.DateTimeField(default=datetime.now, verbose_name=u"录入日期")
    # sampleSide = models.IntegerField(choices=SIDE_TYPE, default=1, verbose_name="电路板是哪个面（1-2；1为正面）", help_text="电路板是哪个面（1-2；1为正面）")
    # rectCoordi=models.CharField(max_length=50,null=True, blank=True, verbose_name="矩形框坐标（4个）")
    maskURL=models.ImageField(max_length=300,null=True, blank=True,upload_to="image/devShapeSample/mask/", verbose_name="PCB区域标记图像文件路径 ")#upload_to="image/devShapeSample/mask/",
    featureUrl=models.FileField(max_length=300,null=True, blank=True, verbose_name="特征文件路径", upload_to="file/devShapeSample/feature")#, upload_to="file/devShapeSample/feature"
    # componentSegURL=models.FileField(max_length=300,null=True, blank=True, verbose_name="元器件分割结果文件路径")# upload_to="file/devShapeSample/result/",
    srcImgURL =models.ImageField(max_length=300,upload_to="image/devShapeSample/original/",null=True,blank=True,verbose_name="原始图像文件路径")#
    sResolution=models.IntegerField(null=True, blank=True, verbose_name="原始图像采集分辨率")
    norImgURL=models.ImageField(max_length=300,upload_to="image/devShapeSample/correction/",null=True,blank=True,verbose_name="归一化图像文件路径")#
    nResolution=models.IntegerField(default= 135, verbose_name="归一化图像分辨率")
    note = models.CharField(max_length=500, null=True, blank=True, verbose_name="备注")
   # isDelete = models.BooleanField(default=False, verbose_name="是否逻辑删除")
    class Meta:
        verbose_name = "爆炸装置常见样本形态表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s,ShapeSample" %(self.devPartSample.sname,)


class PCBImgSample(models.Model):
    """
    爆炸装置关键组件样本电路板图像表
    """
    SIDE_TYPE = (
        (1, "正面"),
        (2, "反面"),
    )
    devPartSample =models.ForeignKey(devPartSample,verbose_name="所属零件",related_name="PCBImgSample")
    user = models.ForeignKey(userProfile, verbose_name=u"处理人员")
    inputDate = models.DateTimeField(default=datetime.now, verbose_name=u"录入日期")
    sampleSide = models.IntegerField(choices=SIDE_TYPE, default=1, verbose_name="电路板是哪个面（1-2；1为正面）", help_text="电路板是哪个面（1-2；1为正面）")
    rectCoordi=models.CharField(max_length=50,null=True, blank=True, verbose_name="矩形框坐标（4个）")
    markImgURL=models.ImageField(max_length=300,null=True, blank=True, verbose_name="PCB区域标记图像文件路径 ")#upload_to="image/devShapeSample/blackWhite/",
    featureUrl=models.FileField(max_length=300,null=True, blank=True, verbose_name="特征文件路径")#, upload_to="file/devShapeSample/feature"
    componentSegURL=models.FileField(max_length=300,null=True, blank=True, verbose_name="元器件分割结果文件路径")# upload_to="file/devShapeSample/result/",
    srcImgURL =models.ImageField(max_length=300,upload_to="image/PCBImgSample/original/",null=True,blank=True,verbose_name="原始图像文件路径")#
    sResolution=models.IntegerField(null=True, blank=True, verbose_name="原始图像采集分辨率")
    norImgURL=models.ImageField(max_length=300,upload_to="image/devShapeSample/nom/",null=True,blank=True,verbose_name="归一化图像文件路径")#
    nResolution=models.IntegerField(default= 135, verbose_name="归一化图像分辨率")
    note = models.CharField(max_length=500, null=True, blank=True, verbose_name="备注")
    class Meta:
        verbose_name = "爆炸装置关键组件样本电路板图像表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s,PCBImg" %(self.devPartSample.sname,)

class oPartImgSample(models.Model):
    """
    爆炸装置关键组件样本其它零件图像（也包括组件外壳）表
    """
    SIDE_TYPE = (
        (1, "正面"),
        (2, "反面"),
        (3, "3面" ),
        (4, "4面" ),
        (5, "5面" ),
        (6, "6面" ),
    )
    devPartSample =models.ForeignKey(devPartSample,verbose_name="所属零件",related_name="oPartImgSample")
    user = models.ForeignKey(userProfile, verbose_name=u"处理人员")
    inputDate = models.DateTimeField(default=datetime.now, verbose_name=u"录入日期")
    sampleSide = models.IntegerField(choices=SIDE_TYPE, default=1, verbose_name="零件是哪个面（1-6；1为正面，2为反面）", help_text="零件是哪个面（1-6；1为正面，2为反面）")
    rectCoordi=models.CharField(max_length=50,null=True, blank=True, verbose_name="矩形框坐标（2个）")
    srcImgURL =models.ImageField(max_length=300,upload_to="image/oPartImgSample/original/",null=True,blank=True,verbose_name="原始图像文件路径")#
    sResolution=models.IntegerField(null=True, blank=True, verbose_name="原始图像采集分辨率")
    norImgURL=models.ImageField(max_length=300,upload_to="image/oPartImgSample/nom/",null=True,blank=True,verbose_name="归一化图像文件路径")#
    nResolution=models.IntegerField(null=True, blank=True, verbose_name="归一化图像分辨率")
    note = models.CharField(max_length=500, null=True, blank=True, verbose_name="备注")
    class Meta:
        verbose_name = "爆炸装置关键组件样本其它零件图像（也包括组件外壳）表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s,oPartImg" %(self.devPartSample.sname,)


class logoImgSample(models.Model):
    """
    爆炸装置关键组件样本商标Logo图像表
    """
    devPartSample =models.ForeignKey(devPartSample,verbose_name="所属零件",related_name="logoImgSample")
    user = models.ForeignKey(userProfile, verbose_name=u"处理人员")
    inputDate = models.DateTimeField(default=datetime.now, verbose_name=u"录入日期")
    rectCoordi=models.CharField(max_length=50,null=True, blank=True, verbose_name="矩形框坐标（2个）")
    srcImgURL =models.ImageField(max_length=300,upload_to="image/logoImgSample/original/",null=True,blank=True,verbose_name="原始图像文件路径")#
    sResolution=models.IntegerField(null=True, blank=True, verbose_name="原始图像采集分辨率")
    norImgURL=models.ImageField(max_length=300,upload_to="image/logoImgSample/nom/",null=True,blank=True,verbose_name="归一化图像文件路径")#
    nResolution=models.IntegerField(null=True, blank=True, verbose_name="归一化图像分辨率")
    note = models.CharField(max_length=500, null=True, blank=True, verbose_name="备注")
    class Meta:
        verbose_name = " 爆炸装置关键组件样本商标Logo图像表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s,logoImg" %(self.devPartSample.sname,)


