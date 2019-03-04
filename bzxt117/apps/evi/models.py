# _*_ encoding:utf-8 _*_
from datetime import datetime
import os

from django.db import models
from apps.basic.models import *

# Create your models here.
class exploEvi(models.Model):
    """
    炸药及原材料物证基本信息表
    """

    evidenceName =models.CharField(max_length=30,verbose_name="物证名称")
    caseName =models.CharField(max_length=30,default="未知案件",verbose_name="案件名称")
    user = models.ForeignKey(userProfile, verbose_name=u"处理人员")
    inputDate = models.DateTimeField(default=datetime.now, verbose_name=u"录入日期")
    picUrl =models.ImageField(max_length=300,upload_to="image/exploEvi/",null=True,blank=True,verbose_name="炸药物证外观图像路径")
    note = models.CharField(max_length=200, null=True, blank=True, verbose_name="备注")

    class Meta:
        verbose_name = "炸药及原材料物证基本信息表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.evidenceName



class exploEviFTIR(models.Model):
    """
    炸药及原材料物证FTIR检测表
    """
    exploEvi = models.ForeignKey(exploEvi, verbose_name=u"对应的炸药物证",related_name="exploEviFTIR")
    devDetect = models.ForeignKey(devDetect, verbose_name=u"对应的检测设备")
    methodDetect = models.ForeignKey(methodDetect, verbose_name=u"对应的检测方法")
    user = models.ForeignKey(userProfile, verbose_name=u"处理人员")
    inputDate = models.DateTimeField(default=datetime.now, verbose_name=u"录入日期")

    class Meta:
        verbose_name = "炸药及原材料物证FTIR检测表"
        verbose_name_plural = verbose_name

    # __str__只是用来当选择哪个作为外键的时候方便显示的，因此比如对于TestFile就不用设置__str__
    def __str__(self):
        return "%s,FTIR" %(self.exploEvi.evidenceName,)


class exploEviFTIRTestFile(models.Model):
    """
   炸药及原材料物证FTIR检测实验文件表
    """
    exploEviFTIR = models.ForeignKey(exploEviFTIR, verbose_name=u"对应的FTIR检测",related_name="exploEviFTIRTestFile")
    exploEviId = models.IntegerField(null=True, blank=True, verbose_name=u"所涉及的炸药物证")
    txtURL = models.FileField(max_length=300, upload_to="file/exploEviFTIRTestFile/", null=True, blank=True,
                              verbose_name="录入TXT文档路径")
    txtHandledURL = models.CharField(max_length=300, null=True, blank=True, verbose_name="处理过的TXT文档路径")

    class Meta:
        verbose_name = "炸药及原材料物证FTIR检测实验文件表"
        verbose_name_plural = verbose_name

class exploEviRaman(models.Model):
    """
    炸药及原材料物证Raman检测表
    """
    exploEvi = models.ForeignKey(exploEvi, verbose_name=u"对应的炸药物证",related_name="exploEviRaman")
    devDetect = models.ForeignKey(devDetect, verbose_name=u"对应的检测设备")
    methodDetect = models.ForeignKey(methodDetect, verbose_name=u"对应的检测方法")
    user = models.ForeignKey(userProfile, verbose_name=u"处理人员")
    inputDate = models.DateTimeField(default=datetime.now, verbose_name=u"录入日期")

    class Meta:
        verbose_name = "炸药及原材料物证Raman检测表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s,Raman" %(self.exploEvi.evidenceName,)


class exploEviRamanTestFile(models.Model):
    """
   炸药及原材料物证Raman检测实验文件表
    """
    exploEviRaman = models.ForeignKey(exploEviRaman, verbose_name=u"对应的Raman检测",related_name="exploEviRamanTestFile")
    exploEviId = models.IntegerField(null=True, blank=True, verbose_name=u"所涉及的炸药物证")
    txtURL = models.FileField(max_length=300, upload_to="file/exploEviRamanTestFile/", null=True, blank=True,
                              verbose_name="录入TXT文档路径")
    txtHandledURL = models.CharField(max_length=300, null=True, blank=True, verbose_name="处理过的TXT文档路径")

    class Meta:
        verbose_name = "炸药及原材料物证Raman检测实验文件表"
        verbose_name_plural = verbose_name


class exploEviXRD(models.Model):
    """
   炸药及原材料物证XRD检测表
    """
    exploEvi = models.ForeignKey(exploEvi, verbose_name=u"对应的炸药样本",related_name="exploEviXRD")
    devDetect = models.ForeignKey(devDetect, verbose_name=u"对应的检测设备")
    methodDetect = models.ForeignKey(methodDetect, verbose_name=u"对应的检测方法")
    user = models.ForeignKey(userProfile, verbose_name=u"处理人员")
    inputDate = models.DateTimeField(default=datetime.now, verbose_name=u"录入日期")

    class Meta:
        verbose_name = "炸药及原材料物证XRD检测表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s,XRD" %(self.exploEvi.evidenceName,)


class exploEviXRDTestFile(models.Model):
    """
   炸药及原材料物证XRD检测实验文件表
    """
    exploEviXRD = models.ForeignKey(exploEviXRD, verbose_name=u"对应的XRD检测",related_name="exploEviXRDTestFile")
    exploEviId = models.IntegerField(null=True, blank=True, verbose_name=u"所涉及的炸药物证")
    txtURL = models.FileField(max_length=300, upload_to="file/exploEviXRDTestFile/", null=True, blank=True,
                              verbose_name="录入TXT文档路径")
    txtHandledURL = models.CharField(max_length=300, null=True, blank=True, verbose_name="处理过的TXT文档路径")

    class Meta:
        verbose_name = "炸药及原材料物证XRD检测实验文件表"
        verbose_name_plural = verbose_name


class exploEviXRF(models.Model):
    """
   炸药及原材料物证XRF检测表
    """
    exploEvi = models.ForeignKey(exploEvi, verbose_name=u"对应的炸药物证",related_name="exploEviXRF")
    devDetect = models.ForeignKey(devDetect, verbose_name=u"对应的检测设备")
    methodDetect = models.ForeignKey(methodDetect, verbose_name=u"对应的检测方法")
    user = models.ForeignKey(userProfile, verbose_name=u"处理人员")
    inputDate = models.DateTimeField(default=datetime.now, verbose_name=u"录入日期")

    class Meta:
        verbose_name = "炸药及原材料物证XRF检测表"
        verbose_name_plural = verbose_name
    def __str__(self):
        return "%s,XRF" %(self.exploEvi.evidenceName,)


class exploEviXRFTestFile(models.Model):
    """
   炸药及原材料物证XRF检测实验文件表
    """
    exploEviXRF = models.ForeignKey(exploEviXRF, verbose_name=u"对应的XRF检测",related_name="exploEviXRFTestFile")
    exploEviId = models.IntegerField(null=True, blank=True, verbose_name=u"所涉及的炸药物证")
    excelURL = models.FileField(max_length=300, upload_to="file/exploEviXRFTestFile/", null=True, blank=True,
                              verbose_name="录入excel文档路径")
    handledURL = models.CharField(max_length=300, null=True, blank=True, verbose_name="有效元素列表")
    class Meta:
        verbose_name = "炸药及原材料物证XRF检测实验文件表"
        verbose_name_plural = verbose_name

class exploEviGCMS(models.Model):
    """
   炸药及原材料物证GC-MS检测表
    """
    exploEvi = models.ForeignKey(exploEvi, verbose_name=u"对应的炸药物证",related_name="exploEviGCMS")
    devDetect = models.ForeignKey(devDetect, verbose_name=u"对应的检测设备")
    methodDetect = models.ForeignKey(methodDetect, verbose_name=u"对应的检测方法")
    user = models.ForeignKey(userProfile, verbose_name=u"处理人员")
    inputDate = models.DateTimeField(default=datetime.now, verbose_name=u"录入日期")

    class Meta:
        verbose_name = "炸药及原材料物证GC-MS检测表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s,GCMS" %(self.exploEvi.evidenceName,)

class exploEviGCMSFile(models.Model):
    """
    炸药及原材料物证GC-MS检测文件表
    """
    exploEviGCMS = models.ForeignKey(exploEviGCMS, verbose_name=u"对应的GC-MS检测",related_name="exploEviGCMSFile")
    exploEviId = models.IntegerField(null=True, blank=True, verbose_name=u"所涉及的炸药物证")
    txtHandledURL = models.CharField(max_length=300, null=True, blank=True, verbose_name="处理过的TXT文档路径")

    class Meta:
        verbose_name = "炸药及原材料物证GC-MS检测文件表"
        verbose_name_plural = verbose_name

class exploEviGCMSTestFile(models.Model):
    """
    炸药及原材料物证GC-MS检测实验文件表
    """
    exploEviGCMS = models.ForeignKey(exploEviGCMS, verbose_name=u"对应的GC-MS检测",related_name="exploEviGCMSTestFile")
    exploEviId = models.IntegerField(null=True, blank=True, verbose_name=u"所涉及的炸药物证")
    type =models.CharField(max_length=20,default="TIC",verbose_name="类型（TIC。。。）")
    txtURL = models.FileField(max_length=300, upload_to="file/exploEviGCMSTestFile/", null=True, blank=True,
                              verbose_name="录入TXT文档路径")
    class Meta:
        verbose_name = "炸药及原材料物证GC-MS检测实验文件表"
        verbose_name_plural = verbose_name



class devEvi(models.Model):
    """
    爆炸装置物证基本信息表
    """
    EVI_TYPE = (
        (1, "外壳"),
        (2, "零件"),
        (3, "电路板"),
        (4,"Logo"),
    )
    evidenceName = models.CharField(max_length=30, verbose_name="物证名称")
    caseName = models.CharField(max_length=30, verbose_name="案件名称")
    user = models.ForeignKey(userProfile, verbose_name=u"处理人员")
    inputDate = models.DateTimeField(default=datetime.now, verbose_name=u"录入日期")
    eviType = models.IntegerField(choices=EVI_TYPE, default=3, verbose_name="物证类型（1-4，外壳，零件，电路板，Logo）",
                                  help_text="物证类型（1-4，外壳，零件，电路板，Logo）")
    picUrl = models.ImageField(max_length=300, upload_to="image/devSample/", null=True, blank=True, verbose_name="组件外观图像路径")
    Factory =models.CharField(max_length=100, null=True, blank=True,verbose_name="物证厂家")
    Model =models.CharField(max_length=30, null=True, blank=True,verbose_name="物证型号")
    Logo =models.CharField(max_length=100,null=True, blank=True, verbose_name="物证商标")
    Color = models.CharField(max_length=10, null=True, blank=True, verbose_name="物证颜色")
    Material =models.CharField(max_length=10, null=True, blank=True,verbose_name="物证材质")
    Shape =models.CharField(max_length=10, null=True, blank=True,verbose_name="物证形状")
    thickness =models.CharField(max_length=50,null=True, blank=True, verbose_name="厚度（边角）")
    note = models.CharField(max_length=500, null=True, blank=True, verbose_name="备注")
    #isDelete = models.BooleanField(default=False, verbose_name="是否逻辑删除")
    class Meta:
        verbose_name = "爆炸装置物证基本信息表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.evidenceName



class devEviFTIR(models.Model):
    """
    爆炸装置物证FTIR检测表
    """
    devEvi = models.ForeignKey(devEvi, verbose_name=u"对应的爆炸装置物证",related_name="devEviFTIR")
    devDetect = models.ForeignKey(devDetect, verbose_name=u"对应的检测设备")
    methodDetect = models.ForeignKey(methodDetect, verbose_name=u"对应的检测方法")
    user = models.ForeignKey(userProfile, verbose_name=u"处理人员")
    inputDate = models.DateTimeField(default=datetime.now, verbose_name=u"录入日期")

    class Meta:
        verbose_name = "爆炸装置物证FTIR检测表"
        verbose_name_plural = verbose_name
    def __str__(self):
        return "%s,FTIR" %(self.devEvi.evidenceName,)


class devEviFTIRTestFile(models.Model):
    """
    爆炸装置物证FTIR检测实验文件表
    """
    devEviFTIR = models.ForeignKey(devEviFTIR, verbose_name=u"对应的FTIR检测",related_name="devEviFTIRTestFile")
    devEviId = models.IntegerField(null=True, blank=True, verbose_name=u"所涉及的炸药物证")
    txtURL = models.FileField(max_length=300, upload_to="file/devEviFTIRTestFile/", null=True, blank=True,
                              verbose_name="录入TXT文档路径")
    txtHandledURL = models.CharField(max_length=300, null=True, blank=True, verbose_name="处理过的TXT文档路径")

    class Meta:
        verbose_name = "爆炸装置物证FTIR检测实验文件表"
        verbose_name_plural = verbose_name


class devEviRaman(models.Model):
    """
    爆炸装置物证Raman检测表
    """
    devEvi = models.ForeignKey(devEvi, verbose_name=u"对应的爆炸装置物证",related_name="devEviRaman")
    devDetect = models.ForeignKey(devDetect, verbose_name=u"对应的检测设备")
    methodDetect = models.ForeignKey(methodDetect, verbose_name=u"对应的检测方法")
    user = models.ForeignKey(userProfile, verbose_name=u"处理人员")
    inputDate = models.DateTimeField(default=datetime.now, verbose_name=u"录入日期")

    class Meta:
        verbose_name = "爆炸装置物证Raman检测表"
        verbose_name_plural = verbose_name
    def __str__(self):
        return "%s,Raman" %(self.devEvi.evidenceName,)


class devEviRamanTestFile(models.Model):
    """
   爆炸装置物证Raman检测实验文件表
    """
    devEviRaman = models.ForeignKey(devEviRaman, verbose_name=u"对应的Raman检测",related_name="devEviRamanTestFile")
    devEviId = models.IntegerField(null=True, blank=True, verbose_name=u"所涉及的炸药物证")
    txtURL = models.FileField(max_length=300, upload_to="file/devEviRamanTestFile/", null=True, blank=True,
                              verbose_name="录入TXT文档路径")
    txtHandledURL = models.CharField(max_length=300, null=True, blank=True, verbose_name="处理过的TXT文档路径")

    class Meta:
        verbose_name = "爆炸装置物证Raman检测实验文件表"
        verbose_name_plural = verbose_name


class devEviXRF(models.Model):
    """
   爆炸装置物证XRF检测表
    """
    devEvi = models.ForeignKey(devEvi, verbose_name=u"对应的爆炸装置物证",related_name="devEviXRF")
    devDetect = models.ForeignKey(devDetect, verbose_name=u"对应的检测设备")
    methodDetect = models.ForeignKey(methodDetect, verbose_name=u"对应的检测方法")
    user = models.ForeignKey(userProfile, verbose_name=u"处理人员")
    inputDate = models.DateTimeField(default=datetime.now, verbose_name=u"录入日期")

    class Meta:
        verbose_name = "爆炸装置物证XRF检测表"
        verbose_name_plural = verbose_name
    def __str__(self):
        return "%s,XRF" %(self.devEvi.evidenceName,)


class devEviXRFTestFile(models.Model):
    """
    爆炸装置物证XRF检测实验文件表
    """
    devEviXRF = models.ForeignKey(devEviXRF, verbose_name=u"对应的XRF检测",related_name="devEviXRFTestFile")
    devEviId = models.IntegerField(null=True, blank=True, verbose_name=u"所涉及的炸药物证")
    excelURL = models.FileField(max_length=300, upload_to="file/devEviXRFTestFile/", null=True, blank=True,
                              verbose_name="录入excel文档路径")
    handledURL = models.CharField(max_length=300, null=True, blank=True, verbose_name="有效元素列表")
    class Meta:
        verbose_name = "爆炸装置物证XRF检测实验文件表"
        verbose_name_plural = verbose_name

class devShapeEvi(models.Model):
    """
    爆炸装置案件物证形态表
    """
    SIDE_TYPE = (
        (1, "正面"),
        (2, "反面"),
    )
    devEvi = models.ForeignKey(devEvi, verbose_name="所属物证",related_name="devShapeEvi")
    user = models.ForeignKey(userProfile, verbose_name=u"处理人员")#,on_delete=models.CASCADE)
    inputDate = models.DateTimeField(default=datetime.now, verbose_name=u"录入日期")
    # sampleSide = models.IntegerField(choices=SIDE_TYPE, default=1, verbose_name="电路板是哪个面（1-2；1为正面）", help_text="电路板是哪个面（1-2；1为正面）")
    maskURL=models.ImageField(max_length=300,null=True, blank=True, verbose_name="PCB区域标记图像文件路径 ")#upload_to="image/devShapeSample/mask/",
    featureUrl=models.FileField(max_length=300,null=True, blank=True, verbose_name="特征文件路径")#, upload_to="file/devShapeSample/feature"
    # componentSegURL=models.FileField(max_length=300,null=True, blank=True, verbose_name="元器件分割结果文件路径")# upload_to="file/devShapeSample/result/",
    srcImgURL =models.ImageField(max_length=300,upload_to="image/devShapeEvi/original/",null=True,blank=True,verbose_name="原始图像文件路径")#
    sResolution=models.IntegerField(null=True, blank=True, verbose_name="原始图像采集分辨率")
    norImgURL=models.ImageField(max_length=300,upload_to="image/devShapeEvi/correction/",null=True,blank=True,verbose_name="归一化图像文件路径")#
    nResolution=models.IntegerField(null=True, blank=True, verbose_name="归一化图像分辨率")
    note = models.CharField(max_length=500, null=True, blank=True, verbose_name="备注")

   # isDelete = models.BooleanField(default=False, verbose_name="是否逻辑删除")
    class Meta:
        verbose_name = "爆炸装置案件物证形态表"
        verbose_name_plural = verbose_name
    def __str__(self):
        return "%s,ShapeEvi" %(self.devEvi.evidenceName,)


class PCBImgEvi(models.Model):
    """
    爆炸装置物证电路板图像表
    """
    SIDE_TYPE = (
        (1, "正面"),
        (2, "反面"),
    )
    #由于目前还是用原来的接口，所以devShapeEvi文件夹不变
    devEvi =models.ForeignKey(devEvi,verbose_name="所属物证",related_name="PCBImgEvi")
    user = models.ForeignKey(userProfile, verbose_name=u"处理人员")
    inputDate = models.DateTimeField(default=datetime.now, verbose_name=u"录入日期")
    sampleSide = models.IntegerField(choices=SIDE_TYPE, default=1, verbose_name="电路板是哪个面（1-2；1为正面）", help_text="电路板是哪个面（1-2；1为正面）")
    rectCoordi=models.CharField(max_length=50,null=True, blank=True, verbose_name="矩形框坐标（4个）")
    markImgURL=models.ImageField(max_length=300,null=True, blank=True, verbose_name="PCB区域标记图像文件路径 ")#upload_to="image/devShapeSample/blackWhite/",
    featureUrl=models.FileField(max_length=300,null=True, blank=True, verbose_name="特征文件路径")#, upload_to="file/devShapeSample/feature"
    componentSegURL=models.FileField(max_length=300,null=True, blank=True, verbose_name="元器件分割结果文件路径")# upload_to="file/devShapeSample/result/",
    srcImgURL =models.ImageField(max_length=300,upload_to="image/devShapeEvi/original/",null=True,blank=True,verbose_name="原始图像文件路径")#
    sResolution=models.IntegerField(null=True, blank=True, verbose_name="原始图像采集分辨率")
    norImgURL=models.ImageField(max_length=300,upload_to="image/devShapeEvi/nom/",null=True,blank=True,verbose_name="归一化图像文件路径")#
    nResolution=models.IntegerField(null=True, blank=True, verbose_name="归一化图像分辨率")
    note = models.CharField(max_length=500, null=True, blank=True, verbose_name="备注")
    class Meta:
        verbose_name = "爆炸装置物证电路板图像表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s,PCBImgEvi" %(self.devEvi.evidenceName,)

class oPartImgEvi(models.Model):
    """
    爆炸装置物证其它零件图像（也包括组件外壳）表
    """
    SIDE_TYPE = (
        (1, "正面"),
        (2, "反面"),
        (3, "3面"),
        (4, "4面"),
        (5, "5面"),
        (6, "6面"),
    )
    devEvi =models.ForeignKey(devEvi,verbose_name="所属物证",related_name="oPartImgEvi")
    user = models.ForeignKey(userProfile, verbose_name=u"处理人员")
    inputDate = models.DateTimeField(default=datetime.now, verbose_name=u"录入日期")
    eviSide = models.IntegerField(choices=SIDE_TYPE, default=1, verbose_name="物证是哪个面（1-6；1为正面，2为反面）", help_text="物证是哪个面（1-6；1为正面，2为反面）")
    rectCoordi=models.CharField(max_length=50,null=True, blank=True, verbose_name="矩形框坐标（2个）")
    srcImgURL =models.ImageField(max_length=300,upload_to="image/oPartImgEvi/original/",null=True,blank=True,verbose_name="原始图像文件路径")#
    sResolution=models.IntegerField(null=True, blank=True, verbose_name="原始图像采集分辨率")
    norImgURL=models.ImageField(max_length=300,upload_to="image/oPartImgEvi/nom/",null=True,blank=True,verbose_name="归一化图像文件路径")#
    nResolution=models.IntegerField(null=True, blank=True, verbose_name="归一化图像分辨率")
    note = models.CharField(max_length=500, null=True, blank=True, verbose_name="备注")
    class Meta:
        verbose_name = "爆炸装置物证其它零件图像（也包括组件外壳）表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s,oPartImgEvi" %(self.devEvi.evidenceName,)


class logoImgEvi(models.Model):
    """
    爆炸装置物证商标Logo图像表
    """
    devEvi =models.ForeignKey(devEvi,verbose_name="所属物证",related_name="logoImgEvi")
    user = models.ForeignKey(userProfile, verbose_name=u"处理人员")
    inputDate = models.DateTimeField(default=datetime.now, verbose_name=u"录入日期")
    rectCoordi=models.CharField(max_length=50,null=True, blank=True, verbose_name="矩形框坐标（2个）")
    srcImgURL =models.ImageField(max_length=300,upload_to="image/logoImgEvi/original/",null=True,blank=True,verbose_name="原始图像文件路径")#
    sResolution=models.IntegerField(null=True, blank=True, verbose_name="原始图像采集分辨率")
    norImgURL=models.ImageField(max_length=300,upload_to="image/logoImgEvi/nom/",null=True,blank=True,verbose_name="归一化图像文件路径")#
    nResolution=models.IntegerField(null=True, blank=True, verbose_name="归一化图像分辨率")
    note = models.CharField(max_length=500, null=True, blank=True, verbose_name="备注")
    class Meta:
        verbose_name = "爆炸装置物证商标Logo图像表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s,logoImgEvi" %(self.devEvi.evidenceName,)


