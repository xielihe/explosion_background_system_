from django.db import models


from apps.sample.models import *
from apps.evi.models import *




# Create your models here.
class exploMatchFTIR(models.Model):
    """
    炸药及原材料物证FTIR匹配结果表
    """
    exploSampleFTIRTestFile = models.ForeignKey(exploSampleFTIRTestFile,verbose_name=u"对应的样本FTIR文件记录",on_delete=models.CASCADE)
    exploEviFTIRTestFile = models.ForeignKey(exploEviFTIRTestFile, verbose_name=u"对应的物证FTIR文件记录",on_delete=models.CASCADE)
    Score =models.FloatField(default=0.0,verbose_name="相似分")

    class Meta:
        verbose_name = "炸药及原材料物证FTIR匹配结果表"
        verbose_name_plural = verbose_name
        # 配置这个以后，如果进行重复提交，会出现{
        #     "non_field_errors": [
        #         "字段 exploSampleFTIR, exploEviFTIR 必须能构成唯一集合。"
        #     ]
        # }的错误，来自于数据库
        unique_together = ("exploSampleFTIRTestFile", "exploEviFTIRTestFile")
        ordering = ['-Score']


class exploMatchRaman(models.Model):
    """
    炸药及原材料物证Raman匹配结果表
    """
    exploSampleRamanTestFile = models.ForeignKey(exploSampleRamanTestFile,verbose_name=u"对应的样本Raman文件记录",on_delete=models.CASCADE)
    exploEviRamanTestFile = models.ForeignKey(exploEviRamanTestFile, verbose_name=u"对应的物证Raman文件记录",on_delete=models.CASCADE)
    Score = models.FloatField(default=0.0, verbose_name="相似分")

    class Meta:
        verbose_name = "炸药及原材料物证Raman匹配结果表"
        verbose_name_plural = verbose_name
        unique_together = ("exploSampleRamanTestFile", "exploEviRamanTestFile")
        ordering = ['-Score']

class exploMatchXRD(models.Model):
    """
    炸药及原材料物证XRD匹配结果表
    """
    exploSampleXRDTestFile = models.ForeignKey(exploSampleXRDTestFile,verbose_name=u"对应的样本XRD文件记录",on_delete=models.CASCADE)
    exploEviXRDTestFile = models.ForeignKey(exploEviXRDTestFile, verbose_name=u"对应的物证XRD文件记录",on_delete=models.CASCADE)
    Score = models.FloatField(default=0.0, verbose_name="相似分")

    class Meta:
        verbose_name = " 炸药及原材料物证XRD匹配结果表"
        verbose_name_plural = verbose_name
        unique_together = ("exploSampleXRDTestFile", "exploEviXRDTestFile")
        ordering = ['-Score']



class exploMatchXRF(models.Model):
    """
    炸药及原材料物证XRF匹配结果表
    """
    exploSampleXRFTestFile = models.ForeignKey(exploSampleXRFTestFile,verbose_name=u"对应的样本XRF文件记录",on_delete=models.CASCADE)
    exploEviXRFTestFile = models.ForeignKey(exploEviXRFTestFile, verbose_name=u"对应的物证XRF文件记录",on_delete=models.CASCADE)
    averScore = models.FloatField(default=0.0, verbose_name="平均相似分")

    class Meta:
        verbose_name = "炸药及原材料物证XRF匹配结果表"
        verbose_name_plural = verbose_name
        unique_together = ("exploSampleXRFTestFile", "exploEviXRFTestFile")
        ordering = ['-averScore']


class exploMatchGCMS(models.Model):
    """
    炸药及原材料物证GC-MS匹配结果表
    """
    exploSampleGCMSFile = models.ForeignKey(exploSampleGCMSFile,verbose_name=u"对应的样本GC-MS文件记录"
                                        , related_name="exploMatchGCMS", on_delete=models.CASCADE)
    exploEviGCMSFile = models.ForeignKey(exploEviGCMSFile, verbose_name=u"对应的物证GC-MS文件记录",
                                     related_name="exploMatchGCMS", on_delete=models.CASCADE)
    msName = models.CharField(max_length=30,null=True, blank=True, verbose_name="匹配的MS文件名称")
    Score = models.FloatField(default=0.0, verbose_name="相似分")

    class Meta:
        verbose_name = "炸药及原材料物证GC-MS匹配结果表"
        verbose_name_plural = verbose_name
        unique_together = ("exploSampleGCMSFile", "exploEviGCMSFile")
        ordering = ['-Score']


class exploSynMatch(models.Model):
    """
    炸药及原材料物证综合匹配结果表
    """
    CHECK_TYPE = (
        (1, "未核准"),
        (2, "匹配"),
        (3, "非匹配"),
    )
    exploSample = models.ForeignKey(exploSample,verbose_name=u"对应的样本"
                                        , related_name="exploSynMatch", on_delete=models.CASCADE)
    exploEvi = models.ForeignKey(exploEvi, verbose_name=u"对应的物证",
                                     related_name="exploSynMatch", on_delete=models.CASCADE)
    Score = models.FloatField(default=0.0, verbose_name="相似分")
    isCheck =models.IntegerField(choices=CHECK_TYPE, default=1,verbose_name="普通用户核准状态")
    checkHandle = models.ForeignKey(userProfile, blank=True,null=True,verbose_name=u"普通核准人员（外键）",related_name='exploSynMatchcheckHandle')
    isExpertCheck =models.IntegerField(choices=CHECK_TYPE, default=1,verbose_name="专家核准状态")
    expertHandle = models.ForeignKey(userProfile,blank=True,null=True, verbose_name=u"专家核准人员（外键）",related_name='exploSynMatchexpertHandle')
    expertOpinion = models.CharField(max_length=300,blank=True,null=True,verbose_name="专家核准意见")

    class Meta:
        verbose_name = "炸药及原材料物证综合匹配结果表"
        verbose_name_plural = verbose_name
        ordering = ['-Score']

class exploReportMatch(models.Model):
    """
    炸药及原材料物证报告结果表
    """
    CHECK_TYPE = (
        (1, "未核准"),
        (2, "匹配"),
        (3, "非匹配"),
    )
    exploEvi = models.ForeignKey(exploEvi, verbose_name=u"对应的物证",
                                     related_name="exploReportMatch", on_delete=models.CASCADE)
    exploSynMatch = models.CharField(max_length=300, blank=True, null=True, verbose_name="对应的综合匹配id数组")

    class Meta:
        verbose_name = "炸药及原材料物证报告结果表"
        verbose_name_plural = verbose_name

class exploReportMatchPDF(models.Model):
    '''
    炸药及原材料物证报告文件表
    '''
    exploEvi = models.ForeignKey(exploEvi, verbose_name=u"对应的物证",
                             related_name="exploReportMatchPDF", on_delete=models.CASCADE)
    PDFURL = models.FileField(max_length=300, upload_to="file/exploReportMatchPDF/", null=True, blank=True,
                              verbose_name="炸药及原材料物证报告文件路径")
    class Meta:
        verbose_name = "炸药及原材料物证报告文件表"
        verbose_name_plural = verbose_name

class devMatchFTIR(models.Model):
    """
    爆炸装置物证FTIR匹配结果表
    """
    devPartSampleFTIRTestFile = models.ForeignKey(devPartSampleFTIRTestFile,verbose_name=u"对应的样本FTIR文件记录"
                                        ,related_name="devMatchFTIRR",on_delete=models.CASCADE)
    devEviFTIRTestFile = models.ForeignKey(devEviFTIRTestFile, verbose_name=u"对应的物证FTIR文件记录",
                                     related_name="devMatchFTIR",on_delete=models.CASCADE)
    Score =models.FloatField(default=0.0,verbose_name="相似分")

    class Meta:
        verbose_name = "爆炸装置物证FTIR匹配结果表"
        verbose_name_plural = verbose_name
        unique_together = ("devPartSampleFTIRTestFile", "devEviFTIRTestFile")
        ordering = ['-Score']


class devMatchRaman(models.Model):
    """
    爆炸装置物证Raman匹配结果表
    """
    devPartSampleRamanTestFile = models.ForeignKey(devPartSampleRamanTestFile,verbose_name=u"对应的样本Raman文件记录"
                                        , related_name="devMatchRaman", on_delete=models.CASCADE)
    devEviRamanTestFile = models.ForeignKey(devEviRamanTestFile, verbose_name=u"对应的物证Raman文件记录",
                                     related_name="devMatchRaman", on_delete=models.CASCADE)
    Score = models.FloatField(default=0.0, verbose_name="相似分")

    class Meta:
        verbose_name = "爆炸装置物证Raman匹配结果表"
        verbose_name_plural = verbose_name
        unique_together = ("devPartSampleRamanTestFile", "devEviRamanTestFile")
        ordering = ['-Score']

class devMatchXRF(models.Model):
    """
    爆炸装置物证XRF匹配结果表
    """
    devPartSampleXRFTestFile = models.ForeignKey(devPartSampleXRFTestFile,verbose_name=u"对应的样本XRF记录"
                                        , related_name="devMatchXRF", on_delete=models.CASCADE)
    devEviXRFTestFile = models.ForeignKey(devEviXRFTestFile, verbose_name=u"对应的物证XRF文件记录",
                                     related_name="devMatchXRF", on_delete=models.CASCADE)
    averScore = models.FloatField(default=0.0, verbose_name="平均相似分")

    class Meta:
        verbose_name = "爆炸装置物证XRF匹配结果表"
        verbose_name_plural = verbose_name
        unique_together = ("devPartSampleXRFTestFile", "devEviXRFTestFile")
        ordering = ['-averScore']


class devCompMatch(models.Model):
    """
    爆炸装置物证成分综合匹配结果表
    """
    CHECK_TYPE = (
        (1, "未核准"),
        (2, "匹配"),
        (3, "非匹配"),
    )
    devPartSample = models.ForeignKey(devPartSample, verbose_name=u"对应的样本"
                                        , related_name="devCompMatch", on_delete=models.CASCADE)
    devEvi = models.ForeignKey(devEvi, verbose_name=u"对应的物证",
                                     related_name="devCompMatchh", on_delete=models.CASCADE)
    Score = models.FloatField(default=0.0, verbose_name="相似分")
    isCheck =models.IntegerField(choices=CHECK_TYPE, default=1,verbose_name="普通用户核准状态")
    checkHandle = models.ForeignKey(userProfile,  blank=True,null=True,verbose_name=u"普通核准人员（外键）",related_name='devCompMatchcheckHandle')
    isExpertCheck =models.IntegerField(choices=CHECK_TYPE, default=1,verbose_name="专家核准状态")
    expertHandle = models.ForeignKey(userProfile, blank=True,null=True, verbose_name=u"专家核准人员（外键）",related_name='devCompMatchexpertHandle')
    expertCompOpinion = models.CharField(max_length=300, blank=True, null=True, verbose_name="专家成分核准意见")
    class Meta:
        verbose_name = "爆炸装置物证成分综合匹配结果表"
        verbose_name_plural = verbose_name
        ordering = ['-Score']

class devShapeMatch(models.Model):
    """
   爆炸装置案件物证形态匹配结果表
    """
    CHECK_TYPE = (
        (1, "未核准"),
        (2, "匹配"),
        (3, "非匹配"),
    )
    devShapeSample = models.ForeignKey(devShapeSample,verbose_name=u"对应的形态样本",related_name="devShapeMatchSample",on_delete=models.CASCADE)
    devShapeEvi = models.ForeignKey(devShapeEvi, verbose_name=u"对应的形态物证",related_name="devShapeMatchEvi",on_delete=models.CASCADE)
    isCircuit = models.BooleanField(default=False, verbose_name="是否是元器件匹配")
    matchDegree =models.FloatField(default=0.0,verbose_name="得分")
    matchSampleCoordi = models.CharField(max_length=400, null=True, blank=True, verbose_name="匹配的样本位置坐标")
    matchEviCoordi = models.CharField(max_length=400, null=True, blank=True, verbose_name="匹配的物证位置坐标")
    isSure = models.BooleanField(default=False, verbose_name="是否确认")
    matchPicURL = models.ImageField(max_length=300,null=True, blank=True, upload_to="image/devShapeSample/match/",verbose_name="匹配的图片路径")
    class Meta:
        verbose_name = "爆炸装置案件物证形态匹配结果表"
        verbose_name_plural = verbose_name
        ordering = ['-matchDegree']


class PCBImgMatch(models.Model):
    """
   爆炸装置物证电路板匹配结果表
    """
    CHECK_TYPE = (
        (1, "未核准"),
        (2, "匹配"),
        (3, "非匹配"),
    )
    PCBImgSample = models.ForeignKey(PCBImgSample,verbose_name=u"对应的样本",
                                     related_name="PCBImgMatch",on_delete=models.CASCADE)
    PCBImgEvi = models.ForeignKey(PCBImgEvi, verbose_name=u"对应的物证",related_name="PCBImgMatch",on_delete=models.CASCADE)
    Score = models.FloatField(default=0.0, verbose_name="相似分")
    similarRect = models.CharField(max_length=20, null=True, blank=True, verbose_name="匹配的样本位置坐标")
    class Meta:
        verbose_name = "爆炸装置物证电路板匹配结果表"
        verbose_name_plural = verbose_name
        ordering = ['-Score']

class oPartImgMatch(models.Model):
    """
   爆炸装置物证其它零件图像（也包括组件外壳）匹配结果表
    """
    CHECK_TYPE = (
        (1, "未核准"),
        (2, "匹配"),
        (3, "非匹配"),
    )
    oPartImgSample = models.ForeignKey(oPartImgSample,verbose_name=u"对应的样本",
                                     related_name="oPartImgMatch",on_delete=models.CASCADE)
    oPartImgEvi = models.ForeignKey(oPartImgEvi, verbose_name=u"对应的物证",related_name="oPartImgMatch",
                                    on_delete=models.CASCADE)
    Score = models.FloatField(default=0.0, verbose_name="相似分")
    class Meta:
        verbose_name = " 爆炸装置物证其它零件图像（也包括组件外壳）匹配结果表"
        verbose_name_plural = verbose_name
        ordering = ['-Score']

class logoImgMatch(models.Model):
    """
   爆炸装置物证商标图像匹配结果表
    """
    CHECK_TYPE = (
        (1, "未核准"),
        (2, "匹配"),
        (3, "非匹配"),
    )
    logoImgSample = models.ForeignKey(logoImgSample,verbose_name=u"对应的样本",
                                     related_name="logoImgMatch",on_delete=models.CASCADE)
    logoImgEvi = models.ForeignKey(logoImgEvi, verbose_name=u"对应的物证",related_name="logoImgMatch",
                                    on_delete=models.CASCADE)
    Score = models.FloatField(default=0.0, verbose_name="相似分")
    class Meta:
        verbose_name = "爆炸装置物证商标图像匹配结果表"
        verbose_name_plural = verbose_name
        ordering = ['-Score']
class devShapeMultiMatch(models.Model):
    """
    爆炸装置物证形态综合匹配结果表
    """
    CHECK_TYPE = (
        (1, "未核准"),
        (2, "匹配"),
        (3, "非匹配"),
    )
    devPartSample = models.ForeignKey(devPartSample, verbose_name=u"对应的样本"
                                        , related_name="devShapeMultiMatch", on_delete=models.CASCADE)
    devEvi = models.ForeignKey(devEvi, verbose_name=u"对应的物证",
                                     related_name="devShapeMultiMatch", on_delete=models.CASCADE)
    Score = models.FloatField(default=0.0, verbose_name="相似分")
    isCheck =models.IntegerField(choices=CHECK_TYPE, default=1,verbose_name="普通用户核准状态")
    checkHandle = models.ForeignKey(userProfile,  blank=True,null=True,verbose_name=u"普通核准人员（外键）",related_name='devShapeMultiMatchcheckHandle')
    isExpertCheck =models.IntegerField(choices=CHECK_TYPE, default=1,verbose_name="专家核准状态")
    expertHandle = models.ForeignKey(userProfile, blank=True,null=True, verbose_name=u"专家核准人员（外键）",related_name='devShapeMultiMatchexpertHandle')
    expertShapeOpinion = models.CharField(max_length=300, blank=True, null=True, verbose_name="专家形态核准意见")
    class Meta:
        verbose_name = "爆炸装置物证形态综合匹配结果表"
        verbose_name_plural = verbose_name
        ordering = ['-Score']

class devSynMatch(models.Model):
    """
  爆炸装置物证综合匹配结果表（成分+形态）
    """
    devEvi = models.ForeignKey(devEvi, verbose_name=u"	对应的物证（外键）",related_name="devSynMatch",
                                    on_delete=models.CASCADE)
    devShapeMultiMatch = models.CharField(max_length=300, blank=True, null=True, verbose_name="对应的形态匹配id数组")
    devCompMatch = models.CharField(max_length=300, blank=True, null=True, verbose_name="对应的成分匹配id数组")
    class Meta:
        verbose_name = "爆炸装置物证综合匹配结果表（成分+形态）"
        verbose_name_plural = verbose_name

class devMatchPDF(models.Model):
    '''
    爆炸装置物证报告文件表
    '''
    devEvi = models.ForeignKey(devEvi, verbose_name=u"对应的物证",
                             related_name="devMatchPDF", on_delete=models.CASCADE)
    PDFURL = models.FileField(max_length=300, upload_to="file/devMatchPDF/", null=True, blank=True,
                              verbose_name="爆炸装置物证报告文件路径")
    class Meta:
        verbose_name = "爆炸装置物证报告文件表"
        verbose_name_plural = verbose_name

# miningList = models.CharField(max_length=300,null=True,blank=True,verbose_name='Mining元素列表')
# class exploSampleXRFTestFileSerializer(serializers.ModelSerializer):
# miningList = serializers.CharField(read_only=True,)