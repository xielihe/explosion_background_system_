from rest_framework import serializers

from .models import *
from apps.sample.serializers import  *
from apps.evi.serializers import *
from apps.basic.serializers import *
from apps.user_operation.models import *

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
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=exploMatchFTIR.objects.all(),
        #         fields=('exploSampleFTIR', 'exploEviFTIR'),
        #         message="已经匹配过"
        #     )
        # ]
        #返回id是为了方便删除
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

class exploMatchXRDSerializer(serializers.ModelSerializer):
    exploSampleName = serializers.SerializerMethodField(read_only=True, )

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
        fields =("id","exploEviXRFTestFile","exploSampleXRFTestFile","miningScore",
                 "pnpScore","ppScore","gmScore","soilScore","tagScore","averScore","exploSampleName")

class exploMatchGCMSSerializer(serializers.ModelSerializer):
    exploSampleName = serializers.SerializerMethodField(read_only=True,)

    def get_exploSampleName(self, obj):
        exploSampleName = obj.exploSampleGCMSFile.exploSampleGCMS.exploSample.sname
        return exploSampleName
    class Meta:
        model = exploMatchGCMS
        #返回id是为了方便删除
        fields =("id","exploEviGCMSFile","exploSampleGCMSFile","Score","exploSampleName")

class exploSynMatchDetailSerializer(serializers.ModelSerializer):
    exploEvi = exploEviSerializer()
    exploSample = exploSampleSerializer()
    # 如果允许外键为空，也可以进行序列化
    checkHandle = UserDetailSerializer()
    expertHandle = UserDetailSerializer()

    class Meta:
        model = exploSynMatch
        #返回id是为了方便删除
        fields = ("id","exploEvi","exploSample","Score","isCheck","isExpertCheck","checkHandle","expertHandle" )
#        ,"exploSynMatchexpertHandle"

# 仅用于测试时添加方便，最后要删除
class exploSynMatchCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = exploSynMatch
        #返回id是为了方便删除
        fields = "__all__"

# 核准会返回200OK的响应
class exploSynMatchSerializer(serializers.Serializer):
    Check = serializers.BooleanField(required=True,write_only=True)
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    # 如果isCheck ==2 ，则表示有普通用户核准了，那么剩余的其他匹配结果的匹配状态应该全都置为3
    # 如果isExpertCheck == 2,则表示有专家核准了，那么不仅剩余的其他匹配结果的匹配状态置为3，还要找到如果有请求的消息的hasHandle置为True
    # 既然申请update，那么肯定会带着id，如果isCheck在请求字段中且为2，则表示核准
    # 核准同时记得维护报告表
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
                matchs = exploSynMatch.objects.exclude(id=instance.id)
                # 其余记录置为未核准
                for match in matchs:
                    match.isCheck = 3
                    match.checkHandle = user
                    match.save()
                #报告表中不一定有记录，有则找出来，没有则按照物证创建
                # 只能按照物证找，因为样本不一定和核准的样本是一个样本
                reportMatch = exploReportMatch.objects.get_or_create(exploEvi=instance.exploEvi)
                # 只有在没有专家核准的情况下才会用普通用户的核准结果去填报告表中的
                # for reportMatch in reportMatchs:
                if reportMatch.isExpertCheck == 1:
                    reportMatch.exploSample = instance.exploSample
                    reportMatch.Score = instance.Score
                    reportMatch.isCheck = 2
                    reportMatch.checkHandle = user
                    reportMatch.save()
            else:
                instance.isExpertCheck = 2
                instance.expertHandle = user
                matchs = exploSynMatch.objects.exclude(id=instance.id)
                for match in matchs:
                    match.isExpertCheck = 3
                    match.expertHandle = user
                    match.save()
                #     消息置为已处理
                messages = userMessage.objects.filter(receiveUser= user,
                                                      exploEviId=instance.exploEvi_id)
                for message in messages:
                    message.hasHandle = True
                    message.save()
                reportMatch = exploReportMatch.objects.get_or_create(exploEvi=instance.exploEvi)
                reportMatch.exploSample = instance.exploSample
                reportMatch.Score = instance.Score
                reportMatch.isExpertCheck = 2
                reportMatch.expertHandle = user
                reportMatch.isCheck = 1
                reportMatch.checkHandle = None
                reportMatch.save()
        instance.save()
        return instance

class exploReportMatchSerializer(serializers.ModelSerializer):
    exploEvi = exploEviSerializer()
    exploSample = exploSampleSerializer()
    # 如果允许外键为空，也可以进行序列化
    checkHandle = UserDetailSerializer()
    expertHandle = UserDetailSerializer()

    class Meta:
        model = exploReportMatch
        #返回id是为了方便删除
        fields = ("id","exploEvi","exploSample","Score","isCheck","isExpertCheck","checkHandle","expertHandle" )
#        ,"exploSynMatchexpertHandle"

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

class devMatchRamanSerializer(serializers.ModelSerializer):
    devSampleName = serializers.SerializerMethodField(read_only=True,)

    def get_devSampleName(self, obj):
        devSampleName = obj.devPartRamanTestFile.devPartSampleRaman.devPartSample.sname
        return devSampleName
    class Meta:
        model = devMatchRaman
        #返回id是为了方便删除
        fields =("id","devEviRamanTestFile","devPartRamanTestFile","Score","devSampleName")

class devMatchXRFSerializer(serializers.ModelSerializer):
    devSampleName = serializers.SerializerMethodField(read_only=True,)

    def get_devSampleName(self, obj):
        devSampleName = obj.devPartSampleXRFTestFile.devPartSampleXRF.devPartSample.sname
        return devSampleName
    class Meta:
        model = devMatchXRF
        #返回id是为了方便删除
        fields =("id","devEviXRFTestFile","devPartSampleXRFTestFile","miningScore",
                 "pnpScore","ppScore","gmScore","soilScore","tagScore","averScore","devSampleName")


class devShapeMatchDetailSerializer(serializers.ModelSerializer):
    devShapeSample = devShapeSampleSerializer()
    devShapeEvi = devShapeEviSerializer()
    # 如果允许外键为空，也可以进行序列化
    checkHandle = UserDetailSerializer()
    expertHandle = UserDetailSerializer()
    class Meta:
        model = devShapeMatch
        #返回id是为了方便删除
        fields = "__all__"

# 形态核准
class devShapeMatchSerializer(serializers.Serializer):
    Check = serializers.BooleanField(required=True,write_only=True)
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    # 如果isCheck ==2 ，则表示有普通用户核准了，那么剩余的其他匹配结果的匹配状态应该全都置为3
    # 如果isExpertCheck == 2,则表示有专家核准了，那么不仅剩余的其他匹配结果的匹配状态置为3，还要找到如果有请求的消息的hasHandle置为True
    # 既然申请update，那么肯定会带着id，如果isCheck在请求字段中且为2，则表示核准
    # 核准同时记得维护报告表
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
                matchs = devShapeMatch.objects.exclude(id=instance.id)
                # 其余记录置为未核准
                for match in matchs:
                    match.isCheck = 3
                    match.checkHandle = user
                    match.save()
                #报告表中一定有记录，因为默认是存的最高得分的，这里核准只是根据优先级替换而已
                # 只能按照物证找，因为样本不一定和核准的样本是一个样本
                reportMatch = devSynMatch.objects.get_or_create(devEviShape=instance.devShapeEvi)
                # 只有在没有专家核准的情况下才会用普通用户的核准结果去填报告表中的
                # for reportMatch in reportMatchs:
                if reportMatch.isExpertCheckShape== 1:
                    reportMatch.devPartSampleShape = instance.devShapeSample.devPartSample
                    reportMatch.ScoreShape = instance.matchScore
                    reportMatch.similarRect = instance.matchSampleCoordi
                    reportMatch.isCheckShape = 2
                    reportMatch.checkHandleShape = user
                    reportMatch.save()
            else:
                instance.isExpertCheck = 2
                instance.expertHandle = user
                matchs = devShapeMatch.objects.exclude(id=instance.id)
                for match in matchs:
                    match.isExpertCheck = 3
                    match.expertHandle = user
                    match.save()
                #     消息置为已处理
                messages = userMessage.objects.filter(receiveUser= user,
                                                      devEviId=instance.devShapeEvi.devEvi_id)
                for message in messages:
                    message.hasHandle = True
                    message.save()
                reportMatch = devSynMatch.objects.get_or_create(devEviShape=instance.devShapeEvi.devEvi)
                reportMatch.devPartSampleShape = instance.devShapeSample.devPartSample
                reportMatch.ScoreShape = instance.matchScore
                reportMatch.similarRect = instance.matchSampleCoordi
                reportMatch.isExpertCheckShape = 2
                reportMatch.expertHandleShape = user
                reportMatch.isCheckShape = 1
                reportMatch.checkHandleShape = None
                reportMatch.save()
        instance.save()
        return instance
# 仅用于测试时添加方便，最后要删除
class devCompMatchCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = devCompMatch
        #返回id是为了方便删除
        fields = "__all__"

# 成分匹配详情展示
class devCompMatchDetailSerializer(serializers.ModelSerializer):
    devEvi = devEviSerializer()
    devPartSample = devPartSampleSerializer()
    # 如果允许外键为空，也可以进行序列化
    checkHandle = UserDetailSerializer()
    expertHandle = UserDetailSerializer()
    class Meta:
        model = devCompMatch
        #返回id是为了方便删除
        fields = ("id","devEvi","devPartSample","Score","isCheck","isExpertCheck","checkHandle","expertHandle" )

# 成分核准
class devCompMatchSerializer(serializers.Serializer):
    Check = serializers.BooleanField(required=True,write_only=True)
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    # 如果isCheck ==2 ，则表示有普通用户核准了，那么剩余的其他匹配结果的匹配状态应该全都置为3
    # 如果isExpertCheck == 2,则表示有专家核准了，那么不仅剩余的其他匹配结果的匹配状态置为3，还要找到如果有请求的消息的hasHandle置为True
    # 既然申请update，那么肯定会带着id，如果isCheck在请求字段中且为2，则表示核准
    # 核准同时记得维护报告表
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
                    match.isCheck = 3
                    match.checkHandle = user
                    match.save()
                #报告表中一定有记录，因为默认是存的最高得分的，这里核准只是根据优先级替换而已
                # 只能按照物证找，因为样本不一定和核准的样本是一个样本
                reportMatch = devSynMatch.objects.get_or_create(devEviComp=instance.devEvi)
                # 只有在没有专家核准的情况下才会用普通用户的核准结果去填报告表中的
                # for reportMatch in reportMatchs:
                if reportMatch.isExpertCheckComp == 1:
                    reportMatch.devPartSampleComp = instance.devPartSample
                    reportMatch.ScoreComp = instance.Score
                    reportMatch.isCheckComp = 2
                    reportMatch.checkHandleComp = user
                    reportMatch.save()
            else:
                instance.isExpertCheck = 2
                instance.expertHandle = user
                matchs = devCompMatch.objects.exclude(id=instance.id)
                for match in matchs:
                    match.isExpertCheck = 3
                    match.expertHandle = user
                    match.save()
                #     消息置为已处理
                messages = userMessage.objects.filter(receiveUser= user,
                                                      devEviId=instance.devEvi_id)
                for message in messages:
                    message.hasHandle = True
                    message.save()
                # 不管普通用户是否核准都将对应样本替换并将普通用户核准那里置为空
                reportMatch = devSynMatch.objects.get_or_create(devEviComp=instance.devEvi)
                reportMatch.devPartSampleComp = instance.devPartSample
                reportMatch.ScoreComp = instance.Score
                reportMatch.isExpertCheckComp = 2
                reportMatch.expertHandleComp = user
                reportMatch.isCheckComp = 1
                reportMatch.checkHandleComp = None
                reportMatch.save()
        instance.save()
        return instance

# 综合报告表
class devSynMatchSerializer(serializers.ModelSerializer):
    devEviComp = devEviSerializer()
    devPartSampleComp = devPartSampleSerializer()
    # 如果允许外键为空，也可以进行序列化
    checkHandleComp = UserDetailSerializer()
    expertHandleComp = UserDetailSerializer()
    devEviShape = devShapeEviSerializer()
    devPartSampleShape = devShapeSampleSerializer()
    # 如果允许外键为空，也可以进行序列化
    checkHandleShape = UserDetailSerializer()
    expertHandleShape = UserDetailSerializer()

    class Meta:
        model = devSynMatch
        #返回id是为了方便删除
        fields = ("id","devEviComp","devPartSampleComp","ScoreComp","isCheckComp","checkHandleComp",
                  "isExpertCheckComp","expertHandleComp","devEviShape","devPartSampleShape","ScoreShape",
                  "similarRect","isCheckShape","checkHandleShape","isExpertCheckShape","expertHandleShape")
#        ,"exploSynMatchexpertHandle"

