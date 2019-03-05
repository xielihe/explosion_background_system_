from rest_framework import serializers

from apps.match.models import *
from apps.sample.serializers import  *
from apps.evi.serializers import *
from apps.basic.serializers import *
from apps.user_operation.models import *

# 语义筛选用的分类器，因为语义筛选只有爆炸装置所以不用写炸药的
class PagerSerialiser(serializers.ModelSerializer):
    class Meta:
        model = devPartSample
        fields = "__all__"

class exploMatchFTIRSerializer(serializers.ModelSerializer):
    exploSampleName = serializers.SerializerMethodField(read_only=True,)

    def get_exploSampleName(self, obj):
        exploSampleName = obj.exploSampleFTIRTestFile.exploSampleFTIR.exploSample.sname
        return exploSampleName
    class Meta:
        model = exploMatchFTIR
        fields =("id","exploEviFTIRTestFile","exploSampleFTIRTestFile","Score","exploSampleName")
class exploMatchFTIRDetailSerializer(serializers.ModelSerializer):
    exploSampleName = serializers.SerializerMethodField(read_only=True,)
    exploEviFTIRTestFile = exploEviFTIRTestFileSerializer()
    exploSampleFTIRTestFile = exploSampleFTIRTestFileSerializer()

    def get_exploSampleName(self, obj):
        exploSampleName = obj.exploSampleFTIRTestFile.exploSampleFTIR.exploSample.sname
        return exploSampleName
    class Meta:
        model = exploMatchFTIR
        fields =("id","exploEviFTIRTestFile","exploSampleFTIRTestFile","Score","exploSampleName")

class exploMatchRamanSerializer(serializers.ModelSerializer):
    exploSampleName = serializers.SerializerMethodField(read_only=True, )

    def get_exploSampleName(self, obj):
        exploSampleName = obj.exploSampleRamanTestFile.exploSampleRaman.exploSample.sname
        return exploSampleName
    # match的详情serializer自定义一个，需要样本名称即可
    class Meta:
        model = exploMatchRaman
        #返回id是为了方便删除
        fields =("id","exploEviRamanTestFile","exploSampleRamanTestFile","Score","exploSampleName")
class exploMatchRamanDetailSerializer(serializers.ModelSerializer):
    exploSampleName = serializers.SerializerMethodField(read_only=True, )
    exploEviRamanTestFile = exploEviRamanTestFileSerializer()
    exploSampleRamanTestFile = exploSampleRamanTestFileSerializer()

    def get_exploSampleName(self, obj):
        exploSampleName = obj.exploSampleRamanTestFile.exploSampleRaman.exploSample.sname
        return exploSampleName
    # match的详情serializer自定义一个，需要样本名称即可
    class Meta:
        model = exploMatchRaman
        #返回id是为了方便删除
        fields =("id","exploEviRamanTestFile","exploSampleRamanTestFile","Score","exploSampleName")

class exploMatchXRDSerializer(serializers.ModelSerializer):
    exploSampleName = serializers.SerializerMethodField(read_only=True, )

    def get_exploSampleName(self, obj):
        exploSampleName = obj.exploSampleXRDTestFile.exploSampleXRD.exploSample.sname
        return exploSampleName
    class Meta:
        model = exploMatchXRD
        #返回id是为了方便删除
        fields =("id","exploEviXRDTestFile","exploSampleXRDTestFile","Score","exploSampleName")
class exploMatchXRDDetailSerializer(serializers.ModelSerializer):
    exploSampleName = serializers.SerializerMethodField(read_only=True, )
    exploEviXRDTestFile = exploEviXRDTestFileSerializer()
    exploSampleXRDTestFile = exploSampleXRDTestFileSerializer()

    def get_exploSampleName(self, obj):
        exploSampleName = obj.exploSampleXRDTestFile.exploSampleXRD.exploSample.sname
        return exploSampleName
    class Meta:
        model = exploMatchXRD
        #返回id是为了方便删除
        fields =("id","exploEviXRDTestFile","exploSampleXRDTestFile","Score","exploSampleName")

class exploMatchXRFSerializer(serializers.ModelSerializer):
    exploSampleName = serializers.SerializerMethodField(read_only=True,)

    def get_exploSampleName(self, obj):
        exploSampleName = obj.exploSampleXRFTestFile.exploSampleXRF.exploSample.sname
        return exploSampleName

    class Meta:
        model = exploMatchXRF
        #返回id是为了方便删除
        fields =("id","exploEviXRFTestFile","exploSampleXRFTestFile","averScore","exploSampleName")
class exploMatchXRFDetailSerializer(serializers.ModelSerializer):
    exploSampleName = serializers.SerializerMethodField(read_only=True,)
    exploEviXRFTestFile = exploEviXRFTestFileSerializer()
    exploSampleXRFTestFile =exploSampleXRFTestFileSerializer()

    def get_exploSampleName(self, obj):
        exploSampleName = obj.exploSampleXRFTestFile.exploSampleXRF.exploSample.sname
        return exploSampleName

    class Meta:
        model = exploMatchXRF
        #返回id是为了方便删除
        fields =("id","exploEviXRFTestFile","exploSampleXRFTestFile","averScore","exploSampleName")


class exploMatchGCMSSerializer(serializers.ModelSerializer):
    exploSampleName = serializers.SerializerMethodField(read_only=True,)

    def get_exploSampleName(self, obj):
        exploSampleName = obj.exploSampleGCMSFile.exploSampleGCMS.exploSample.sname
        return exploSampleName
    class Meta:
        model = exploMatchGCMS
        #返回id是为了方便删除
        fields =("id","exploEviGCMSFile","exploSampleGCMSFile","Score","exploSampleName")
class exploMatchGCMSDetailSerializer(serializers.ModelSerializer):
    exploSampleName = serializers.SerializerMethodField(read_only=True,)
    exploEviGCMSFile = exploEviGCMSFileSerializer()
    exploSampleGCMSFile = exploSampleGCMSFileSerializer()

    def get_exploSampleName(self, obj):
        exploSampleName = obj.exploSampleGCMSFile.exploSampleGCMS.exploSample.sname
        return exploSampleName
    class Meta:
        model = exploMatchGCMS
        #返回id是为了方便删除
        fields =("id","exploEviGCMSFile","exploSampleGCMSFile","Score","exploSampleName")

# 炸药的综合匹配结果的详情展示，包括这个物证的每种方法中和这个样本的得分最高的文件组合
class exploSynMatchDetailSerializer(serializers.ModelSerializer):
    exploEvi = exploEviSerializer()
    exploSample = exploSampleSerializer()
    # 如果允许外键为空，也可以进行序列化
    checkHandle = UserDetailSerializer()
    expertHandle = UserDetailSerializer()
    exploEviFTIR = serializers.SerializerMethodField(read_only=True,)
    exploEviRaman = serializers.SerializerMethodField(read_only=True,)
    exploEviXRD = serializers.SerializerMethodField(read_only=True,)
    exploEviXRF = serializers.SerializerMethodField(read_only=True,)
    exploEviGCMS = serializers.SerializerMethodField(read_only=True,)

    def get_exploEviFTIR(self, obj):
        exploEvi = obj.exploEvi
        # 把该记录的物证及样本对应的FTIR的最匹配的一对拿出来
        FTIRMatchs = exploMatchFTIR.objects.filter(exploEviFTIRTestFile__exploEviFTIR__exploEvi= exploEvi,exploSampleFTIRTestFile__exploSampleFTIR__exploSample=obj.exploSample).order_by('-Score')
        if FTIRMatchs.count() >0 :
            FTIRMatchs = FTIRMatchs[0]
        return exploMatchFTIRDetailSerializer(FTIRMatchs,).data
    def get_exploEviRaman(self, obj):
        exploEvi = obj.exploEvi
        # 把该记录的物证及样本对应的FTIR的最匹配的一对拿出来
        RamanMatchs = exploMatchRaman.objects.filter(exploEviRamanTestFile__exploEviRaman__exploEvi= exploEvi,exploSampleRamanTestFile__exploSamplevRaman__exploSample=obj.exploSample).order_by('-Score')
        if RamanMatchs.count() >0 :
            RamanMatchs = RamanMatchs[0]
        return exploMatchRamanDetailSerializer(RamanMatchs,).data
    def get_exploEviXRD(self, obj):
        exploEvi = obj.exploEvi
        # 把该记录的物证及样本对应的FTIR的最匹配的一对拿出来
        XRDMatchs = exploMatchXRD.objects.filter(exploEviXRDTestFile__exploEviXRD__exploEvi=exploEvi,
                                                 exploSampleXRDTestFile__exploSamplevXRD__exploSample=obj.exploSample).order_by(
            '-Score')
        if XRDMatchs.count() > 0:
            XRDMatchs = XRDMatchs[0]
        return exploMatchXRDDetailSerializer(XRDMatchs, ).data
    def get_exploEviXRF(self, obj):
        exploEvi = obj.exploEvi
        # 把该记录的物证及样本对应的FTIR的最匹配的一对拿出来
        XRFMatchs = exploMatchXRF.objects.filter(exploEviXRFTestFile__exploEviXRF__exploEvi=exploEvi,
                                                 exploSampleXRFTestFile__exploSamplevXRF__exploSample=obj.exploSample).order_by(
            '-averScore')
        if XRFMatchs.count() > 0:
            XRFMatchs = XRFMatchs[0]
        return exploMatchXRFDetailSerializer(XRFMatchs, ).data
    def get_exploEviGCMS(self, obj):
        exploEvi = obj.exploEvi
        # 把该记录的物证及样本对应的FTIR的最匹配的一对拿出来
        GCMSMatchs = exploMatchGCMS.objects.filter(exploEviGCMSFile__exploEviGCMS__exploEvi=exploEvi,
                                                   exploSampleGCMSFile__exploSamplevGCMS__exploSample=obj.exploSample).order_by(
            '-Score')
        if GCMSMatchs.count() > 0:
            GCMSMatchs = GCMSMatchs[0]
        return exploMatchGCMSDetailSerializer(GCMSMatchs, ).data

    class Meta:
        model = exploSynMatch
        #返回id是为了方便删除
        fields = ("id","exploEvi","exploSample","Score","isCheck","isExpertCheck","checkHandle","expertHandle","expertOpinion","exploEviFTIR","exploEviRaman","exploEviXRD","exploEviXRF","exploEviGCMS")
#        ,"exploSynMatchexpertHandle"

# 用于测试时添加方便和删除
class exploSynMatchCreateSerializer(serializers.ModelSerializer):
    exploEvi = exploEviSerializer()
    exploSample = exploSampleSerializer()
    # 如果允许外键为空，也可以进行序列化
    checkHandle = UserDetailSerializer()
    expertHandle = UserDetailSerializer()

    class Meta:
        model = exploSynMatch
        #返回id是为了方便删除
        fields = ("id","exploEvi","exploSample","Score","isCheck","isExpertCheck","checkHandle","expertHandle","expertOpinion")

# # 炸药综合核准（核准会返回200OK的响应）
# class exploSynMatchSerializer(serializers.Serializer):
#     Check = serializers.BooleanField(required=True,write_only=True)
#     user = serializers.HiddenField(
#         default=serializers.CurrentUserDefault()
#     )
#     # 如果isCheck ==2 ，则表示有普通用户核准了，那么剩余的其他匹配结果的匹配状态应该全都置为3
#     # 如果isExpertCheck == 2,则表示有专家核准了，那么不仅剩余的其他匹配结果的匹配状态置为3，还要找到如果有请求的消息的hasHandle置为True
#     # 既然申请update，那么肯定会带着id，如果isCheck在请求字段中且为2，则表示核准
#     # 核准同时记得维护报告表（现在不用了，报告表额外接口生成）
#     def update(self, instance, validated_data):
#         user = self.context["request"].user
#         # 根据PATCH的id就可以知道是哪条记录了，因为是从view过来的，view确定了queryset，所以知道是哪个
#         matchId = instance.id
#         # 如果核准了
#         if validated_data["Check"] == True:
#             # 普通用户请求
#             if user.role == 3:
#                 # 本匹配记录的核准字段更新
#                 instance.isCheck = 2
#                 instance.checkHandle = user
#                 matchs = exploSynMatch.objects.exclude(id=instance.id)
#                 # 其余记录置为未匹配（在状态为未核准的情况下）
#                 for match in matchs:
#                     if match.isCheck == 1:
#                         match.isCheck = 3
#                         match.checkHandle = user
#                         match.save()
#
#                 # 由于一个物证被核准为多个样本是可能的，因此不能进行核准更替，都要存储，所以要以物证以及核准的样本进行过滤，而不能单单过滤物证
#                 reportMatchs = exploReportMatch.objects.filter(exploEvi=instance.exploEvi,exploSample = instance.exploSample)
#                 if reportMatchs.count() >0:
#                     for reportMatch in reportMatchs:
#                         # 只有在没有专家核准的情况下才会用普通用户的核准结果去填报告表中的
#                         # for reportMatch in reportMatchs:
#                           该记录没有被专家核准
#                         if reportMatch.isExpertCheck == 1:
#                             # 如果有其余普通用户核准过，则新建
#                             if reportMatch.isCheck == 2:
#                                 reportMatchNew = exploReportMatch.objects.create(exploEvi=instance.exploEvi,exploSample = instance.exploSample,Score = instance.Score)
#                                 reportMatchNew.isCheck = 2
#                                 reportMatchNew.checkHandle = user
#                                 reportMatchNew.save()
#                             else:
#                                 # 如果没有其余普通用户核准过
#                                 reportMatch.Score = instance.Score
#                                 reportMatch.isCheck = 2
#                                 reportMatch.checkHandle = user
#                                 reportMatch.save()
#                 else:
#                     reportMatch = exploReportMatch.objects.create(exploEvi=instance.exploEvi,exploSample = instance.exploSample,Score = instance.Score)
#                     reportMatch.isCheck = 2
#                     reportMatch.checkHandle = user
#                     reportMatch.save()
#             else:
#                 # 综合表的操作
#                 instance.isExpertCheck = 2
#                 instance.expertHandle = user
#                 matchs = exploSynMatch.objects.exclude(id=instance.id)
#                 for match in matchs:
#                     if match.isExpertCheck == 1:
#                         match.isExpertCheck = 3
#                         match.expertHandle = user
#                         match.save()
#                 # 报告表的操作
#                 reportMatchs = exploReportMatch.objects.filter(exploEvi=instance.exploEvi,exploSample = instance.exploSample)
#                 if reportMatchs.count() >0:
#                   有记录可能是普通用户核准的或者其他专家核准的
#                     for reportMatch in reportMatchs:
#                         # 其余专家核准过，则新建
#                         if reportMatch.isExpertCheck == 2:
#                             reportMatchNew = exploReportMatch.objects.create(exploEvi=instance.exploEvi,
#                                                                           exploSample=instance.exploSample,
#                                                                           Score=instance.Score)
#                             reportMatchNew.isExpertCheck = 2
#                             reportMatchNew.expertHandle = user
#                             reportMatchNew.expertOpinion = instance.expertOpinion
#                             reportMatchNew.save()
#                         # 其余专家未核准，则直接赋值（普通用户核准的）
#                         else:
#                             reportMatch.Score = instance.Score
#                             reportMatch.isExpertCheck = 2
#                             reportMatch.expertHandle = user
#                             reportMatch.isCheck = instance.isCheck
#                             reportMatch.checkHandle = instance.checkHandle
#                             reportMatch.expertOpinion = instance.expertOpinion
#                             reportMatch.save()
#                 else:
#                     reportMatch = exploReportMatch.objects.create(exploEvi=instance.exploEvi,exploSample = instance.exploSample,Score = instance.Score)
#                     reportMatch.isExpertCheck = 2
#                     reportMatch.expertHandle = user
#                     reportMatch.expertOpinion = instance.expertOpinion
#                     reportMatch.save()
#         instance.save()
#         return instance
# 炸药综合核准（核准会返回200OK的响应）
class exploSynMatchCheckSerializer(serializers.Serializer):
    Check = serializers.BooleanField(required=True,write_only=True)
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    # 如果isCheck ==2 ，则表示有普通用户核准了，那么剩余的其他匹配结果的匹配状态应该全都置为3
    # 如果isExpertCheck == 2,则表示有专家核准了，那么不仅剩余的其他匹配结果的匹配状态置为3，还要找到如果有请求的消息的hasHandle置为True
    # 既然申请update，那么肯定会带着id，如果isCheck在请求字段中且为2，则表示核准
    def update(self, instance, validated_data):
        user = self.context["request"].user
        # 根据PATCH的id就可以知道是哪条记录了，因为是从view过来的，view确定了queryset，所以知道是哪个
        # 作用只是记录
        matchId = instance.id
        # 如果核准了
        if validated_data["Check"] == True:
            # 普通用户请求
            if user.role == 3:
                # 本匹配记录的核准字段更新
                instance.isCheck = 2
                instance.checkHandle = user
                matchs = exploSynMatch.objects.exclude(id=instance.id)
                # 其余记录置为未匹配（在状态为未核准的情况下）
                for match in matchs:
                    if match.isCheck == 1:
                        match.isCheck = 3
                        match.checkHandle = user
                        match.save()
                # 不去管报告表，因为报告表的记录由一个单独的接口请求生成的，不是核准后自动生成的
            else:
                # 综合表的操作
                instance.isExpertCheck = 2
                instance.expertHandle = user
                matchs = exploSynMatch.objects.exclude(id=instance.id)
                for match in matchs:
                    if match.isExpertCheck == 1:
                        match.isExpertCheck = 3
                        match.expertHandle = user
                        match.save()
        instance.save()
        return instance

# 用于列表展示或者删除的，创建不用serializer，有专门的接口去创建
class exploReportMatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = exploReportMatch
        #返回id是为了方便删除
        fields = "__all__"
#        ,"exploSynMatchexpertHandle"

# 炸药报告详情展示
class exploReportMatchDetailSerializer(serializers.ModelSerializer):
    exploEvi = exploEviSerializer()
    exploSynMatchList = serializers.SerializerMethodField(read_only=True, )

    def get_exploSynMatchList(self, obj):
        exploSynMatch1 = obj.exploSynMatch
        exploMatchList = exploSynMatch1.split()
        length = len(exploMatchList)
        if length > 0:
            if length > 1:
                # 把字符型数组转化为int形数组
                exploMatchList = [int(i) for i in exploMatchList ]
                synMatch = exploSynMatch.objects.filter(id__in=exploMatchList).order_by("-Score")
                # 返回形态综合详情展示
                return exploSynMatchDetailSerializer(synMatch, many=True).data
            else:
                synMatch = exploSynMatch.objects.get(id=int(exploMatchList[0]))
                return exploSynMatchDetailSerializer(synMatch, ).data
        else:
            return []

    class Meta:
        model = exploReportMatch
        # 返回id是为了方便删除
        fields = ("id", "exploEvi", "exploSynMatchList")


# 注意对于爆炸装置物证是不分部分不部分的，而对于样本是要区分部分Part的
class devMatchFTIRSerializer(serializers.ModelSerializer):
    devSampleName = serializers.SerializerMethodField(read_only=True,)

    def get_devSampleName(self, obj):
        devSampleName = obj.devPartSampleFTIRTestFile.devPartSampleFTIR.devPartSample.sname
        return devSampleName
    class Meta:
        model = devMatchFTIR
        #返回id是为了方便删除
        fields =("id","devEviFTIRTestFile","devPartSampleFTIRTestFile","Score","devSampleName")
#         这个serializer包含了物证文件和样本文件的详细信息（将文件的数据提取出来返回的）
class devMatchFTIRDetailSerializer(serializers.ModelSerializer):
    devSampleName = serializers.SerializerMethodField(read_only=True,)
    devEviFTIRTestFile = devEviFTIRTestFileSerializer()
    devPartSampleFTIRTestFile = devPartSampleFTIRTestFileSerializer()

    def get_devSampleName(self, obj):
        devSampleName = obj.devPartSampleFTIRTestFile.devPartSampleFTIR.devPartSample.sname
        return devSampleName
    class Meta:
        model = devMatchFTIR
        #返回id是为了方便删除
        fields =("id","devEviFTIRTestFile","devPartSampleFTIRTestFile","Score","devSampleName")

# 只返回对应的样本文件的样本名的serializer
class devMatchRamanSerializer(serializers.ModelSerializer):
    devSampleName = serializers.SerializerMethodField(read_only=True,)

    def get_devSampleName(self, obj):
        devSampleName = obj.devPartSampleRamanTestFile.devPartSampleRaman.devPartSample.sname
        return devSampleName
    class Meta:
        model = devMatchRaman
        #返回id是为了方便删除
        fields =("id","devEviRamanTestFile","devPartSampleRamanTestFile","Score","devSampleName")
# 这个serializer包含了物证文件和样本文件的详细信息（将文件的数据提取出来返回的）
class devMatchRamanDetailSerializer(serializers.ModelSerializer):
    devSampleName = serializers.SerializerMethodField(read_only=True,)
    devEviRamanTestFile  = devEviRamanTestFileSerializer()
    devPartSampleRamanTestFile = devPartSampleRamanTestFileSerializer()

    def get_devSampleName(self, obj):
        devSampleName = obj.devPartSampleRamanTestFile.devPartSampleRaman.devPartSample.sname
        return devSampleName
    class Meta:
        model = devMatchRaman
        #返回id是为了方便删除
        fields =("id","devEviRamanTestFile","devPartSampleRamanTestFile","Score","devSampleName")

class devMatchXRFSerializer(serializers.ModelSerializer):
    devSampleName = serializers.SerializerMethodField(read_only=True,)

    def get_devSampleName(self, obj):
        devSampleName = obj.devPartSampleXRFTestFile.devPartSampleXRF.devPartSample.sname
        return devSampleName
    class Meta:
        model = devMatchXRF
        #返回id是为了方便删除
        fields =("id","devEviXRFTestFile","devPartSampleXRFTestFile","averScore","devSampleName")
 # 这个serializer包含了物证文件和样本文件的详细信息（将文件的数据提取出来返回的）
class devMatchXRFDetailSerializer(serializers.ModelSerializer):
    devSampleName = serializers.SerializerMethodField(read_only=True,)
    devEviXRFTestFile = devEviXRFTestFileSerializer()
    devPartSampleXRFTestFile = devPartSampleXRFTestFileSerializer()

    def get_devSampleName(self, obj):
        devSampleName = obj.devPartSampleXRFTestFile.devPartSampleXRF.devPartSample.sname
        return devSampleName
    class Meta:
        model = devMatchXRF
        #返回id是为了方便删除
        fields =("id","devEviXRFTestFile","devPartSampleXRFTestFile","averScore","devSampleName")

# class devShapeMatchDetailSerializer(serializers.ModelSerializer):
#     devShapeSample = devShapeSampleSerializer()
#     devShapeEvi = devShapeEviSerializer()
#     # 如果允许外键为空，也可以进行序列化
#     checkHandle = UserDetailSerializer()
#     expertHandle = UserDetailSerializer()
#     class Meta:
#         model = devShapeMatch
#         #返回id是为了方便删除
#         fields = "__all__"

# # 形态核准
# class devShapeMatchCheckSerializer(serializers.Serializer):
#     Check = serializers.BooleanField(required=True,write_only=True)
#     user = serializers.HiddenField(
#         default=serializers.CurrentUserDefault()
#     )
#     # 如果isCheck ==2 ，则表示有普通用户核准了，那么剩余的其他匹配结果的匹配状态应该全都置为3
#     # 如果isExpertCheck == 2,则表示有专家核准了，那么不仅剩余的其他匹配结果的匹配状态置为3，还要找到如果有请求的消息的hasHandle置为True
#     # 既然申请update，那么肯定会带着id，如果isCheck在请求字段中且为2，则表示核准
#     # 核准同时记得维护报告表
#     def update(self, instance, validated_data):
#         user = self.context["request"].user
#         # 根据PATCH的id就可以知道是哪条记录了，因为是从view过来的，view确定了queryset，所以知道是哪个
#         matchId = instance.id
#         # 如果核准了
#         if validated_data["Check"] == True:
#             # 普通用户请求
#             if user.role == 3:
#                 # 本匹配记录的核准字段更新
#                 instance.isCheck = 2

#                 instance.checkHandle = user
#                 matchs = devShapeMatch.objects.exclude(id=instance.id)
#                 # 其余记录置为未核准
#                 for match in matchs:
#                     if match.isCheck == 1:
#                         match.isCheck = 3
#                         match.checkHandle = user
#                         match.save()
#                 #报告表中一定有记录，因为默认是存的最高得分的，这里核准只是根据优先级替换而已
#                 # 只能按照物证找，因为样本不一定和核准的样本是一个样本
#
#                 # devEviComp指的是那个对应的物证，是以devEviComp为标准的！！
#                 # 由于核准的还是根据EviShape和SampleShape核准的，因此还是得按照这两筛选，且devShapeEvi对应的话devCompEvi也一定对应
#                 reportMatchs = devSynMatch.objects.filter(devShapeEvi = instance.devShapeEvi,devShapeSample = instance.devShapeSample )
#                 # 只有在没有专家核准的情况下才会用普通用户的核准结果去填报告表中的
#                 # for reportMatch in reportMatchs:
#                 if reportMatchs.count() >0:
#                     for reportMatch in reportMatchs:
#                         # 跳转到这里的情况：只有成分核准结果的，而形态核准状态为专家未核准且其余用户也未核准
#                         # 只有爆炸装置需要考虑其余用户是否核准，因为涉及到形态和成分两种，炸药的只要存在报告表里就一定是核准过的
#                         if reportMatch.isExpertCheckShape== 1:
#                             if reportMatch.isCheckShape == 2:
#                                 reportMatchNew = devSynMatch.objects.create(devEviComp=instance.devShapeEvi.devEvi,
#                                                                             devPartSampleComp = instance.devShapeSample.devPartSample,
#                                                                             devShapeEvi=instance.devShapeEvi,
#                                                                             devShapeSample=instance.devShapeSample,
#                                                                          ScoreShape=instance.matchScore,
#                                                                          similarRect=instance.matchSampleCoordi)
#                                 reportMatchNew.isCheckShape = 2
#                                 reportMatchNew.checkHandleShape = user
#                                 reportMatchNew.save()
#                             else:
#                                 reportMatch.ScoreShape = instance.matchScore
#                                 reportMatch.similarRect = instance.matchSampleCoordi
#                                 reportMatch.isCheckShape = 2
#                                 reportMatch.checkHandleShape = user
#                                 reportMatch.save()
#                 else:
#                     reportMatch = devSynMatch.objects.create(devEviComp=instance.devShapeEvi.devEvi,devPartSampleComp=instance.devShapeSample.devPartSample,devShapeEvi=instance.devShapeEvi,
#                                                                             devShapeSample=instance.devShapeSample,ScoreShape = instance.matchScore,similarRect = instance.matchSampleCoordi)
#                     reportMatch.isCheckShape = 2
#                     reportMatch.checkHandleShape = user
#                     reportMatch.save()
#             else:
#                 # 匹配表
#                 instance.isExpertCheck = 2
#                 instance.expertHandle = user
#                 matchs = devShapeMatch.objects.exclude(id=instance.id)
#                 for match in matchs:
#                     if match.isExpertCheck == 1:
#                         match.isExpertCheck = 3
#                         match.expertHandle = user
#                         match.save()
#                 # 报告表
#                 reportMatchs = devSynMatch.objects.filter(devShapeEvi = instance.devShapeEvi,devShapeSample = instance.devShapeSample)
#                 if reportMatchs.count() >0:
#                     for reportMatch in reportMatchs:
#                         if reportMatch.isExpertCheckShape == 2:
#                             reportMatchNew = devSynMatch.objects.create(devEviComp=instance.devShapeEvi.devEvi,devPartSampleComp = instance.devShapeSample.devPartSample,devShapeEvi=instance.devShapeEvi,
#                                                                         devShapeSample=instance.devShapeSample,
#                                                                      ScoreShape=instance.matchScore,
#                                                                      similarRect=instance.matchSampleCoordi)
#                             reportMatchNew.isExpertCheckShape = 2
#                             reportMatchNew.expertHandleShape = user
#                             reportMatchNew.expertShapeOpinion = instance.expertShapeOpinion
#                             reportMatchNew.save()
#                         else:
#                             reportMatch.ScoreShape = instance.matchScore
#                             reportMatch.similarRect = instance.matchSampleCoordi
#                             reportMatch.isExpertCheckShape = 2
#                             reportMatch.expertHandleShape = user
#                             reportMatch.isCheckShape = instance.isCheckShape
#                             reportMatch.checkHandleShape = instance.checkHandleShape
#                             reportMatch.expertShapeOpinion = instance.expertShapeOpinion
#                             reportMatch.save()
#                 else:
#                     reportMatch = devSynMatch.objects.create(devEviComp=instance.devShapeEvi.devEvi,devPartSampleComp = instance.devShapeSample.devPartSample,devShapeEvi=instance.devShapeEvi,
#                                                                         devShapeSample=instance.devShapeSample,ScoreShape = instance.matchScore,similarRect = instance.matchSampleCoordi)
#                     reportMatch.isExpertCheckShape = 2
#                     reportMatch.expertHandleShape = user
#                     reportMatch.expertShapeOpinion = instance.expertShapeOpinion
#                     reportMatch.save()
#         instance.save()
#         return instance

# class devShapeMatchCheckSerializer(serializers.Serializer):
#     Check = serializers.BooleanField(required=True,write_only=True)
#     user = serializers.HiddenField(
#         default=serializers.CurrentUserDefault()
#     )
#     # 如果isCheck ==2 ，则表示有普通用户核准了，那么剩余的其他匹配结果的匹配状态应该全都置为3
#     # 如果isExpertCheck == 2,则表示有专家核准了，那么不仅剩余的其他匹配结果的匹配状态置为3，还要找到如果有请求的消息的hasHandle置为True
#     # 既然申请update，那么肯定会带着id，如果isCheck在请求字段中且为2，则表示核准
#     def update(self, instance, validated_data):
#         user = self.context["request"].user
#         # 根据PATCH的id就可以知道是哪条记录了，因为是从view过来的，view确定了queryset，所以知道是哪个
#         matchId = instance.id
#         # 如果核准了
#         if validated_data["Check"] == True:
#             # 普通用户请求
#             if user.role == 3:
#                 # 本匹配记录的核准字段更新
#                 instance.isCheck = 2
#                 instance.checkHandle = user
#                 matchs = devShapeMatch.objects.exclude(id=instance.id)
#                 # 其余记录置为未核准
#                 for match in matchs:
#                     if match.isCheck == 1:
#                         match.isCheck = 3
#                         match.checkHandle = user
#                         match.save()
#             else:
#                 # 匹配表
#                 instance.isExpertCheck = 2
#                 instance.expertHandle = user
#                 matchs = devShapeMatch.objects.exclude(id=instance.id)
#                 for match in matchs:
#                     if match.isExpertCheck == 1:
#                         match.isExpertCheck = 3
#                         match.expertHandle = user
#                         match.save()
#         instance.save()
#         return instance
# # 形态核准（在devShapeMultiMatchViewset中调用）

# 形态匹配详情展示（包含了形态匹配对应的样本和物证图片的矩形框等信息）

class devShapeMultiMatchCheckSerializer(serializers.Serializer):
    Check = serializers.BooleanField(required=True,write_only=True)
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    # 如果isCheck ==2 ，则表示有普通用户核准了，那么剩余的其他匹配结果的匹配状态应该全都置为3
    # 如果isExpertCheck == 2,则表示有专家核准了，那么不仅剩余的其他匹配结果的匹配状态置为3，还要找到如果有请求的消息的hasHandle置为True
    # 既然申请update，那么肯定会带着id，如果isCheck在请求字段中且为2，则表示核准
    def update(self, instance, validated_data):
        user = self.context["request"].user
        # 根据PATCH的id就可以知道是哪条记录了，因为是从view过来的，view确定了queryset，所以知道是哪个
        matchId = instance.id
        # 如果核准了
        if validated_data["Check"] == True:
            # 普通用户请求
            if user.role == 3:
                # 本匹配记录的核准字段更新
                instance.isCheck = 2
                instance.checkHandle = user
                matchs = devShapeMultiMatch.objects.exclude(id=instance.id)
                # 其余记录置为未核准
                for match in matchs:
                    if match.isCheck == 1:
                        match.isCheck = 3
                        match.checkHandle = user
                        match.save()
            else:
                # 匹配表
                instance.isExpertCheck = 2
                instance.expertHandle = user
                matchs = devShapeMultiMatch.objects.exclude(id=instance.id)
                for match in matchs:
                    if match.isExpertCheck == 1:
                        match.isExpertCheck = 3
                        match.expertHandle = user
                        match.save()
        instance.save()
        return instance
# 形态综合匹配核准（在devShapeMultiMatchViewset中调用）

class devShapeMatchDetailSerializer(serializers.ModelSerializer):
    devShapeSample = devShapeSampleSerializer()
    devShapeEvi = devShapeEviSerializer()
    matchPicURL = serializers.ImageField(read_only=True,)
    # #由物证图片和样本图片的id去取匹配图像
    # def get_matchPic(self, obj):
    #     eviFileId = obj.devShapeEvi.id
    #     sampleFileId = obj.devShapeSample.id
    #     matchUrl = os.path.join(MEDIA_ROOT, "image/devShapeEvi/match/" + str(eviFileId) + "/" + str(eviFileId) +"_"+ str(sampleFileId)+ ".jpg")
    #     return matchUrl

    class Meta:
        model = devShapeMatch
        #返回id是为了方便删除
        fields = ("id","devShapeSample","devShapeEvi","matchDegree","matchSampleCoordi","matchEviCoordi","matchPicURL")
# 形态匹配详情展示
class devShapeMatchSerializer(serializers.ModelSerializer):
    devSampleName = serializers.SerializerMethodField(read_only=True,)

    def get_devSampleName(self, obj):
        devSampleName = obj.devShapeSample.devPartSample.sname
        return devSampleName

    class Meta:
        model = devShapeMatch
        #返回id是为了方便删除
        fields = ("id","devShapeSample","devShapeEvi","matchDegree","matchSampleCoordi","matchEviCoordi","devSampleName")
# 形态匹配列表展示

#  形态综合匹配详情展示(把一个物证的所有图片和这个样本的图片的分别得分最高的拿出来)
class devShapeMultiMatchDetailSerializer(serializers.ModelSerializer):
    # 展示该物证所有图片
    devEvi = devEviShapeDetailSerializer()
    devPartSample = devPartSampleSerializer()
    devSample = serializers.SerializerMethodField(read_only=True,)
    # 如果允许外键为空，也可以进行序列化
    checkHandle = UserDetailSerializer()
    expertHandle = UserDetailSerializer()
    devSampleList = serializers.SerializerMethodField(read_only=True,)

    def get_devSample(self,obj):
        devSampleShow = devSample.objects.filter(id = obj.devPartSample.devSample.id)
        if devSampleShow.count() > 1:
            raise APIException("id错误无法找到对应的devSample")
        return devSampleSerializer(devSampleShow,).data

    def get_devSampleList(self, obj):
        # 思路：一张物证图片留一个此样本最匹配的图片
        #想展示这个 devShapeMatchSerializer

        # 建一个空的queryset
        finalQuery = devShapeMatch.objects.none()
        # 筛选出这个物证的所有图片
        shapeEvis = devShapeEvi.objects.filter(devEvi = obj.devEvi)
        # 这个物证的每张图片
        for shapeEvi in shapeEvis:
            shapeMatchs = devShapeMatch.objects.filter(devShapeEvi = shapeEvi,devShapeSample__devPartSample=obj.devPartSample ).order_by("-matchScore")
            if shapeMatchs.count() > 0:
                shapeMatchs = shapeMatchs[0]
            # 每次循环，即物证的每张图片，都选出一个与这张物证图片得分最高的属于这个样本的形态匹配记录
            finalQuery = shapeMatchs | finalQuery
        if finalQuery.count() >1:
            #因为要展示所以用详情的serializer
            return devShapeMatchDetailSerializer(finalQuery,many=True).data
        else:
            return devShapeMatchDetailSerializer(finalQuery,).data

    class Meta:
        model = devShapeMultiMatch
        #返回id是为了方便删除
        fields = ("id","devEvi","devPartSample","devSample","Score","isCheck","isExpertCheck","checkHandle","expertHandle","expertShapeOpinion","devSampleList")

# 形态综合匹配的测试时的添加接口和删除接口
class devShapeMultiMatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = devShapeMultiMatch
        fields = "__all__"
# 成分测试代码时的添加接口和删除接口
class devCompMatchCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = devCompMatch
        #返回id是为了方便删除
        fields = "__all__"

# 成分匹配详情展示( 把一个物证和一个样本的FTIR,Raman和XRF的分别得分最高的拿出来)
class devCompMatchDetailSerializer(serializers.ModelSerializer):
    devEvi = devEviSerializer()
    devPartSample = devPartSampleSerializer()
    devSample = serializers.SerializerMethodField(read_only=True,)
    # 如果允许外键为空，也可以进行序列化
    checkHandle = UserDetailSerializer()
    expertHandle = UserDetailSerializer()
    devEviFTIR = serializers.SerializerMethodField(read_only=True,)
    devEviRaman = serializers.SerializerMethodField(read_only=True,)
    devEviXRF = serializers.SerializerMethodField(read_only=True,)

    def get_devSample(self,obj):
        devSampleShow = devSample.objects.filter(id = obj.devPartSample.devSample.id)
        return devSampleSerializer(devSampleShow,).data

    def get_devEviFTIR(self, obj):
        devEvi = obj.devEvi
        # 把该记录的物证及样本对应的FTIR的最匹配的一对拿出来
        # 在等号左端，进行字段的链表查询时，用__来连接，在等好右端，进行链表取值时用 . 来连接
        FTIRMatchs = devMatchFTIR.objects.filter(devEviFTIRTestFile__devEviFTIR__devEvi=devEvi,
                                                 devPartSampleFTIRTestFile__devPartSampleFTIR__devPartSample=obj.devPartSample).order_by(
            '-Score')
        if FTIRMatchs.count() > 0:
            FTIRMatchs = FTIRMatchs[0]
        return devMatchFTIRDetailSerializer(FTIRMatchs,).data

    def get_devEviRaman(self, obj):
        devEvi = obj.devEvi
        # 把该记录的物证及样本对应的FTIR的最匹配的一对拿出来
        RamanMatchs = devMatchRaman.objects.filter(devEviRamanTestFile__devEviRaman__devEvi=devEvi,
                                                   devPartSampleRamanTestFile__devPartSampleRaman__devPartSample=obj.devPartSample).order_by(
            '-Score')
        if RamanMatchs.count() > 0:
            RamanMatchs = RamanMatchs[0]
        return devMatchRamanDetailSerializer(RamanMatchs,).data

    def get_devEviXRF(self, obj):
        devEvi = obj.devEvi
        # 把该记录的物证及样本对应的FTIR的最匹配的一对拿出来
        XRFMatchs = devMatchXRF.objects.filter(devEviXRFTestFile__devEviXRF__devEvi=devEvi,
                                                 devPartSampleXRFTestFile__devPartSampleXRF__devPartSample=obj.devPartSample).order_by(
            '-averScore')
        if XRFMatchs.count() > 0:
            XRFMatchs = XRFMatchs[0]
        return devMatchXRFDetailSerializer(XRFMatchs, ).data
    class Meta:
        model = devCompMatch
        #返回id是为了方便删除
        fields = ("id","devEvi","devPartSample","devSample","Score","isCheck","isExpertCheck","checkHandle","expertHandle","expertCompOpinion","devEviFTIR","devEviRaman","devEviXRF" )
# # 成分核准
# class devCompMatchSerializer(serializers.Serializer):
#     Check = serializers.BooleanField(required=True,write_only=True)
#     user = serializers.HiddenField(
#         default=serializers.CurrentUserDefault()
#     )
#     # 如果isCheck ==2 ，则表示有普通用户核准了，那么剩余的其他匹配结果的匹配状态应该全都置为3
#     # 如果isExpertCheck == 2,则表示有专家核准了，那么不仅剩余的其他匹配结果的匹配状态置为3，还要找到如果有请求的消息的hasHandle置为True
#     # 既然申请update，那么肯定会带着id，如果isCheck在请求字段中且为2，则表示核准
#     # 核准同时记得维护报告表
#     def update(self, instance, validated_data):
#         user = self.context["request"].user
#         # 根据PATCH的id就可以知道是哪条记录了，因为是从view过来的，view确定了queryset，所以知道是哪个
#         matchId = instance.id
#         # 如果核准了
#         if validated_data["Check"] == True:
#             # 普通用户请求
#             if user.role == 3:
#                 # 本匹配记录的核准字段更新
#                 instance.isCheck = 2
#                 instance.checkHandle = user
#                 matchs = devCompMatch.objects.exclude(id=instance.id)
#                 # 其余记录置为未核准
#                 for match in matchs:
#                     # 只有未核准状态才会修改成不匹配，因为核准不一定唯一
#                     if match.isCheck == 1:
#                         match.isCheck = 3
#                         match.checkHandle = user
#                         match.save()
#                 #报告表中一定有记录，因为默认是存的最高得分的，这里核准只是根据优先级替换而已
#                 # 只能按照物证找，因为样本不一定和核准的样本是一个样本
#                 reportMatchs = devSynMatch.objects.filter(devEviComp=instance.devEvi,devPartSampleComp = instance.devPartSample)
#                 if reportMatchs.count() >0:
#                     for reportMatch in reportMatchs:
#                 # 只有在没有专家核准的情况下才会用普通用户的核准结果去填报告表中的
#                 # for reportMatch in reportMatchs:
#                         if reportMatch.isExpertCheckComp == 1:
#                             if reportMatch.isCheckComp == 2:
#                                 reportMatchNew = devSynMatch.objects.create(devEviComp=instance.devEvi,
#                                                                          devPartSampleComp=instance.devPartSample,
#                                                                          ScoreComp=instance.Score)
#                                 reportMatchNew.isCheckComp = 2
#                                 reportMatchNew.checkHandleComp = user
#                                 reportMatchNew.save()
#                             else:
#                                 reportMatch.ScoreComp = instance.Score
#                                 reportMatch.isCheckComp = 2
#                                 reportMatch.checkHandleComp = user
#                                 reportMatch.save()
#                 else:
#                     reportMatch = devSynMatch.objects.create(devEviComp=instance.devEvi,devPartSampleComp = instance.devPartSample,ScoreComp = instance.Score)
#                     reportMatch.isCheckComp = 2
#                     reportMatch.checkHandleComp = user
#                     reportMatch.save()
#             else:
#                 instance.isExpertCheck = 2
#                 instance.expertHandle = user
#                 matchs = devCompMatch.objects.exclude(id=instance.id)
#                 for match in matchs:
#                     if match.isExpertCheck == 1:
#                         match.isExpertCheck = 3
#                         match.expertHandle = user
#                         match.save()
#                 # 不管普通用户是否核准都将对应样本替换并将普通用户核准那里置为空
#                 reportMatchs = devSynMatch.objects.filter(devEviComp=instance.devEvi,devPartSampleComp = instance.devPartSample)
#                 if reportMatchs.count() >0:
#                     for reportMatch in reportMatchs:
#                         if reportMatch.isExpertCheckComp == 2:
#                             reportMatchNew = devSynMatch.objects.create(devEviComp=instance.devEvi,
#                                                                      devPartSampleComp=instance.devPartSample,
#                                                                      ScoreComp=instance.Score)
#                             reportMatchNew.isExpertCheckComp = 2
#                             reportMatchNew.expertHandleComp = user
#                             reportMatchNew.expertCompOpinion = instance.expertOpinion
#                             reportMatchNew.save()
#                         else:
#                             reportMatch.ScoreComp = instance.Score
#                             reportMatch.isExpertCheckComp = 2
#                             reportMatch.expertHandleComp = user
#                             reportMatch.isCheckComp = instance.isCheckComp
#                             reportMatch.checkHandleComp = instance.checkHandleComp
#                             reportMatch.expertCompOpinion = instance.expertOpinion
#                             reportMatch.save()
#                 else:
#                     reportMatch = devSynMatch.objects.create(devEviComp=instance.devEvi,devPartSampleComp = instance.devPartSample,ScoreComp = instance.Score)
#                     reportMatch.isExpertCheckComp = 2
#                     reportMatch.expertHandleComp = user
#                     reportMatch.expertCompOpinion = instance.expertOpinion
#                     reportMatch.save()
#         instance.save()
#         return instance

# 综合报告表

class devCompMatchCheckSerializer(serializers.Serializer):
    Check = serializers.BooleanField(required=True,write_only=True)
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    # 如果isCheck ==2 ，则表示有普通用户核准了，那么剩余的其他匹配结果的匹配状态应该全都置为3
    # 如果isExpertCheck == 2,则表示有专家核准了，那么不仅剩余的其他匹配结果的匹配状态置为3，还要找到如果有请求的消息的hasHandle置为True
    # 既然申请update，那么肯定会带着id，如果isCheck在请求字段中且为2，则表示核准
    # 核准同时不维护报告表，报告表的记录由点击“报告”按钮后单独生成
    def update(self, instance, validated_data):
        user = self.context["request"].user
        # 根据PATCH的id就可以知道是哪条记录了，因为是从view过来的，view确定了queryset，所以知道是哪个
        matchId = instance.id
        # 如果核准了
        if validated_data["Check"] == True:
            # 普通用户请求
            if user.role == 3:
                # 本匹配记录的核准字段更新
                instance.isCheck = 2
                instance.checkHandle = user
                matchs = devCompMatch.objects.exclude(id=instance.id)
                # 其余记录置为未核准
                for match in matchs:
                    # 只有未核准状态才会修改成不匹配，因为核准不一定唯一
                    if match.isCheck == 1:
                        match.isCheck = 3
                        match.checkHandle = user
                        match.save()
            else:
                instance.isExpertCheck = 2
                instance.expertHandle = user
                matchs = devCompMatch.objects.exclude(id=instance.id)
                for match in matchs:
                    if match.isExpertCheck == 1:
                        match.isExpertCheck = 3
                        match.expertHandle = user
                        match.save()
        instance.save()
        return instance
# 成分核准

# 用于删除报告的serializer
class devSynMatchSerializer(serializers.ModelSerializer):
    devShapeMultiMatch = serializers.CharField(read_only=True)
    devCompMatch = serializers.CharField(read_only=True)
    class Meta:
        model = devSynMatch
        #返回id是为了方便删除
        fields = "__all__"
# #        ,"exploSynMatchexpertHandle"
#
# # class devSynMatchDetailSerializer(serializers.ModelSerializer):
# #     devEviComp = devEviSerializer()
# #     devPartSampleComp = devPartSampleSerializer()
# #     # 如果允许外键为空，也可以进行序列化
# #     checkHandleComp = UserDetailSerializer()
# #     expertHandleComp = UserDetailSerializer()
# #     devEviShape = devShapeEviSerializer()
# #     devPartSampleShape = devShapeSampleSerializer()
# #     # 如果允许外键为空，也可以进行序列化
# #     checkHandleShape = UserDetailSerializer()
# #     expertHandleShape = UserDetailSerializer()
# #     devEviFTIR = serializers.SerializerMethodField(read_only=True,)
# #     devEviRaman = serializers.SerializerMethodField(read_only=True,)
# #     devEviXRF = serializers.SerializerMethodField(read_only=True,)
# #
# #     def get_devEviFTIR(self, obj):
# #         devEviComp = obj.devEviComp
# #         # 把该记录的物证及样本对应的FTIR的最匹配的一对拿出来
# #         # 在等号左端，进行字段的链表查询时，用__来连接，在等好右端，进行链表取值时用 . 来连接
# #         FTIRMatchs = devMatchFTIR.objects.filter(devEviFTIRTestFile__devEviFTIR__devEvi=devEviComp,
# #                                                  devPartSampleFTIRTestFile__devPartSampleFTIR__devPartSample=obj.devPartSampleComp).order_by(
# #             '-Score')
# #         if FTIRMatchs.count() > 0:
# #             FTIRMatchs = FTIRMatchs[0]
# #         return devMatchFTIRDetailSerializer(FTIRMatchs,).data
# #
# #     def get_devEviRaman(self, obj):
# #         devEviComp = obj.devEviComp
# #         # 把该记录的物证及样本对应的FTIR的最匹配的一对拿出来
# #         RamanMatchs = devMatchRaman.objects.filter(devEviRamanTestFile__devEviRaman__devEvi=devEviComp,
# #                                                    devPartSampleRamanTestFile__devPartSampleRaman__devPartSample=obj.devPartSampleComp).order_by(
# #             '-Score')
# #         if RamanMatchs.count() > 0:
# #             RamanMatchs = RamanMatchs[0]
# #         return devMatchRamanDetailSerializer(RamanMatchs,).data
# #
# #     def get_devEviXRF(self, obj):
# #         devEviComp = obj.devEviComp
# #         # 把该记录的物证及样本对应的FTIR的最匹配的一对拿出来
# #         XRFMatchs = devMatchXRF.objects.filter(devEviXRFTestFile__devEviXRF__devEvi=devEviComp,
# #                                                  devPartSampleXRFTestFile__devPartSampleXRF__devPartSample=obj.devPartSampleComp).order_by(
# #             '-averScore')
# #         if XRFMatchs.count() > 0:
# #             XRFMatchs = XRFMatchs[0]
# #         return devMatchXRFDetailSerializer(XRFMatchs, ).data
# #
# #     class Meta:
# #         model = devSynMatch
# #         #返回id是为了方便删除
# #         fields = ("id","devEviComp","devPartSampleComp","ScoreComp","isCheckComp","checkHandleComp",
# #                   "isExpertCheckComp","expertHandleComp","expertCompOpinion","devEviFTIR","devEviRaman","devEviXRF","devEviShape","devPartSampleShape","ScoreShape",
# #                   "similarRect","isCheckShape","checkHandleShape","isExpertCheckShape","expertHandleShape","expertShapeOpinion")
# # #        ,"exploSynMatchexpertHandle"
# # 报告展示页面
class devSynMatchDetailSerializer(serializers.ModelSerializer):
    devEvi = devEviSerializer()
    devShapeMultiMatchList = serializers.SerializerMethodField(read_only=True,)
    devCompMatchList = serializers.SerializerMethodField(read_only=True,)

    def get_devShapeMultiMatchList(self, obj):
        devShapeMultiMatch1 = obj.devShapeMultiMatch
        multiMatchList = devShapeMultiMatch1.split()
        length = len(multiMatchList)
        if length >0:
            if length >1:
                multiMatchList = [int(i) for i in multiMatchList]
                shapeMatch = devShapeMultiMatch.objects.filter(id__in = multiMatchList).order_by("-Score")
                # 返回形态综合详情展示
                return devShapeMultiMatchDetailSerializer(shapeMatch,many = True).data
            else:
                shapeMatch = devShapeMultiMatch.objects.get(id = int(multiMatchList[0]))
                return devShapeMultiMatchDetailSerializer(shapeMatch,).data
        else:
            return []

    def get_devCompMatchList(self, obj):
        devCompMatch1 = obj.devCompMatch
        compMatchList = devCompMatch1.split()
        length = len(compMatchList)
        if length >0:
            if length >1:
                compMatchList = [int(i) for i in compMatchList]
                compMatch = devCompMatch.objects.filter(id__in = compMatchList).order_by("-Score")
                # 返回成分匹配详情展示
                return devCompMatchDetailSerializer(compMatch,many=True).data
            else:
                compMatch = devCompMatch.objects.get(id = int(compMatchList[0]))
                return devCompMatchDetailSerializer(compMatch,).data
        else:
            return []

    class Meta:
        model = devSynMatch
        #返回id是为了方便删除
        fields = ("id","devEvi","devShapeMultiMatchList","devCompMatchList")
#每个物证一个报告的详情展示（生成报告没有专门的serializer，是有一个专门生成报告的接口实现的）
