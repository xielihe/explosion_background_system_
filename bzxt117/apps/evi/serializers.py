# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.serializers import *

from apps.evi.models import *
from apps.basic.models import *
from apps.basic.serializers import UserDetailSerializer
from utils.XRDhandle import preprocess
from apps.match.models import *

class exploEviSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    inputDate = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = exploEvi
        fields = "__all__"


class exploEviFTIRTestFileSerializer(serializers.ModelSerializer):
    txtHandledURL = serializers.FileField(read_only=True, )
    def __str__(self):
        return self.txtURL

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                field = getattr(instance, attr)
                field.set(value)
            else:
                setattr(instance, attr, value)

        #对txt进行预处理，再平均
        # exploEviFTIRTestFiles = exploEviFTIRTestFile.objects.filter(exploEviFTIR = instance.exploEviFTIR)
        instance.txtHandledURL = "file/exploEviFTIRTestFile/GM1923-扫描247_hF4jw4W.txt" #假定成功标志
        instance.save()
        return instance

    class Meta:
        model = exploEviFTIRTestFile
        fields = "__all__"

class LsitExploEviFTIRTestFileSerializer(serializers.Serializer):
    # 用于接收多个文件
    FTIRs = serializers.ListField(
        child=serializers.FileField(max_length=100000, allow_empty_file=False, use_url=True),
        write_only=True )
    #用于接收外键
    exploEviFTIR = serializers.PrimaryKeyRelatedField(required=True, queryset=exploEviFTIR.objects.all())
    # 保证Id只是我们内部维护的
    exploEviId = serializers.IntegerField(read_only=True,)
    # 返回的多个文件列表
    return_FTIRs = serializers.ListField(
        child=serializers.CharField(max_length=10000,),
        read_only=True )

    def create(self, validated_data):
        FTIRs = validated_data.get('FTIRs')
        exploEviFTIR = validated_data.get('exploEviFTIR')
        # 新建重复也不可以覆盖！！否则就和修改一样了啊
        # exploEviFTIRTestFiles = exploEviFTIRTestFile.objects.filter(exploEviFTIR = exploEviFTIR)
        # for exploEviFTIRTestFileUp in exploEviFTIRTestFiles:
        #     exploEviFTIRTestFileUp.delete()
        FTIR1s = []
        for index, url in enumerate(FTIRs):
            # 会自动填入exploEviId
            exploEviId = exploEviFTIR.exploEvi_id
            FTIR = exploEviFTIRTestFile.objects.create(txtURL=url,exploEviFTIR = exploEviFTIR,exploEviId =exploEviId )
            # 文件预处理
            # 新增一个物证文件时，该FTIR表中此物证的匹配结果必然是空的，此外因为更新走的也是补录的路径
            # 因此如果新增物证文件，要将综合表和报告表中的此物证的删去来提示用户进行重新匹配
            synMatchs = exploSynMatch.objects.filter(exploEvi_id= exploEviId)
            for synMatch in synMatchs:
                synMatch.delete()
            reportMatchs = exploReportMatch.objects.filter(exploEvi= exploEviId)
            for reportMatch in reportMatchs:
                reportMatch.delete()

            blog = exploEviFTIRTestFileSerializer(FTIR, context=self.context)
            FTIR1s.append(blog.data['txtURL'])
        return {
                'return_FTIRs':FTIR1s,
                'exploEviFTIR':exploEviFTIR}

class exploEviFTIRSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    inputDate = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    class Meta:
        model = exploEviFTIR
        fields = "__all__"
        # fields = ("id","exploSample","devDetect","methodDetect", "user","inputDate","txtHandledURL")
class exploEviFTIRDetailSerializer(serializers.ModelSerializer):
    # 被指向用related_name来连接
    exploEviFTIRTestFile = exploEviFTIRTestFileSerializer(many = True)
    # 自身的外键直接用serializer代替即可
    user = UserDetailSerializer()

    class Meta:
        model = exploEviFTIR
        fields = ("id","exploEvi","devDetect","methodDetect", "user","inputDate","exploEviFTIRTestFile")

class exploEviRamanTestFileSerializer(serializers.ModelSerializer):
    txtHandledURL = serializers.FileField(read_only=True, )
    def __str__(self):
        return self.txtURL

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                field = getattr(instance, attr)
                field.set(value)
            else:
                setattr(instance, attr, value)

        # 对txt进行预处理，再平均
        # exploEviFTIRTestFiles = exploEviFTIRTestFile.objects.filter(exploEviFTIR = instance.exploEviFTIR)
        instance.txtHandledURL = "file/exploEviFTIRTestFile/GM1923-扫描247_hF4jw4W.txt"  # 假定成功标志
        instance.save()
        return instance

    class Meta:
        model = exploEviRamanTestFile
        fields = "__all__"
class LsitExploEviRamanTestFileSerializer(serializers.Serializer):
    # 用于接收多个文件
    Ramans = serializers.ListField(
        child=serializers.FileField(max_length=100000, allow_empty_file=False, use_url=True),
        write_only=True)
    # 用于接收外键
    exploEviRaman = serializers.PrimaryKeyRelatedField(required=True, queryset=exploEviRaman.objects.all())
    # 保证Id只是我们内部维护的
    exploEviId = serializers.IntegerField(read_only=True, )
    # 返回的多个文件列表
    return_Ramans = serializers.ListField(
        child=serializers.CharField(max_length=10000, ),
        read_only=True)

    def create(self, validated_data):
        Ramans = validated_data.get('Ramans')
        exploEviRaman = validated_data.get('exploEviRaman')
        # 新建重复也不可以覆盖！！否则就和修改一样了啊
        Raman1s = []
        for index, url in enumerate(Ramans):
            # 会自动填入exploEviId
            Raman = exploEviRamanTestFile.objects.create(txtURL=url, exploEviRaman=exploEviRaman,
                                                       exploEviId=exploEviRaman.exploEvi_id)
            blog = exploEviRamanTestFileSerializer(Raman, context=self.context)
            Raman1s.append(blog.data['txtURL'])
        # 对上传的文档预处理取平均，再将取完平均的回填
        return {
            'return_Ramans': Raman1s,
            'exploEviRaman':exploEviRaman}
class exploEviRamanSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    inputDate = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = exploEviRaman
        fields = "__all__"
class exploEviRamanDetailSerializer(serializers.ModelSerializer):
    # 被指向用related_name来连接
    exploEviRamanTestFile = exploEviRamanTestFileSerializer(many = True)
    # 自身的外键直接用serializer代替即可
    user = UserDetailSerializer()

    class Meta:
        model = exploEviRaman
        fields = ("id","exploEvi","devDetect","methodDetect", "user","inputDate","exploEviRamanTestFile")


class exploEviXRDTestFileSerializer(serializers.ModelSerializer):
    txtHandledURL = serializers.FileField(read_only=True, )
    def __str__(self):
        return self.txtURL

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                field = getattr(instance, attr)
                field.set(value)
            else:
                setattr(instance, attr, value)

        # 对txt进行预处理，再平均
        # exploEviFTIRTestFiles = exploEviFTIRTestFile.objects.filter(exploEviFTIR = instance.exploEviFTIR)
        instance.txtHandledURL = "file/exploEviFTIRTestFile/GM1923-扫描247_hF4jw4W.txt"  # 假定成功标志
        instance.save()
        return instance

    class Meta:
        model = exploEviXRDTestFile
        fields = "__all__"
class LsitExploEviXRDTestFileSerializer(serializers.Serializer):
    # 用于接收多个文件
    XRDs = serializers.ListField(
        child=serializers.FileField(max_length=100000, allow_empty_file=False, use_url=True),
        write_only=True)
    # 用于接收外键
    exploEviXRD = serializers.PrimaryKeyRelatedField(required=True, queryset=exploEviXRD.objects.all())
    # 保证Id只是我们内部维护的
    exploEviId = serializers.IntegerField(read_only=True, )
    # 返回的多个文件列表
    return_XRDs = serializers.ListField(
        child=serializers.CharField(max_length=10000, ),
        read_only=True)

    def create(self, validated_data):
        XRDs = validated_data.get('XRDs')
        exploEviXRD = validated_data.get('exploEviXRD')
        # 新建重复也不可以覆盖！！否则就和修改一样了啊
        # exploEviXRDTestFiles = exploEviXRDTestFile.objects.filter(exploEviXRD = exploEviXRD)
        # for exploEviXRDTestFileUp in exploEviXRDTestFiles:
        #     exploEviXRDTestFileUp.delete()
        XRD1s = []
        for index, url in enumerate(XRDs):
            # 会自动填入exploEviId
            XRD = exploEviXRDTestFile.objects.create(txtURL=url, exploEviXRD=exploEviXRD,
                                                       exploEviId=exploEviXRD.exploEvi_id)
            blog = exploEviXRDTestFileSerializer(XRD, context=self.context)
            XRD1s.append(blog.data['txtURL'])
        # 对上传的文档预处理取平均，再将取完平均的回填
        return {
            'return_XRDs': XRD1s,
            'exploEviXRD': exploEviXRD}
class exploEviXRDSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    inputDate = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = exploEviXRD
        fields = "__all__"
        # fields = ("id","exploSample","devDetect","methodDetect", "user","inputDate","txtHandledURL")
class exploEviXRDDetailSerializer(serializers.ModelSerializer):
    # 被指向用related_name来连接
    exploEviXRDTestFile = exploEviXRDTestFileSerializer(many=True)
    # 自身的外键直接用serializer代替即可
    user = UserDetailSerializer()

    class Meta:
        model = exploEviXRD
        fields = ("id", "exploEvi", "devDetect", "methodDetect", "user", "inputDate", "exploEviXRDTestFile")

class exploEviXRFTestFileSerializer(serializers.ModelSerializer):
    miningList = serializers.CharField(read_only=True,)
    pnpList = serializers.CharField(read_only=True,)
    ppList = serializers.CharField(read_only=True, )
    gmList = serializers.CharField(read_only=True, )
    soilList = serializers.CharField(read_only=True, )
    tagList = serializers.CharField(read_only=True, )

    def __str__(self):
        return self.excelURL

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                field = getattr(instance, attr)
                field.set(value)
            else:
                setattr(instance, attr, value)

        #对excel进行预处理，填入各有效值
        # exploEviXRFTestFiles = exploEviXRFTestFile.objects.filter(exploEviXRF = instance.exploEviXRF)
        instance.save()
        return instance

    class Meta:
        model = exploEviXRFTestFile
        fields = "__all__"
class LsitExploEviXRFTestFileSerializer(serializers.Serializer):
    # 用于接收多个文件
    XRFs = serializers.ListField(
        child=serializers.FileField(max_length=100000, allow_empty_file=False, use_url=True),
        write_only=True )
    #用于接收外键
    exploEviXRF = serializers.PrimaryKeyRelatedField(required=True, queryset=exploEviXRF.objects.all())
    # 保证Id只是我们内部维护的
    exploEviId = serializers.IntegerField(read_only=True,)
    # 返回的多个文件列表
    return_XRFs = serializers.ListField(
        child=serializers.CharField(max_length=10000,),
        read_only=True )

    def create(self, validated_data):
        XRFs = validated_data.get('XRFs')
        exploEviXRF = validated_data.get('exploEviXRF')
        # 新建重复也不可以覆盖！！否则就和修改一样了啊
        # exploEviXRFTestFiles = exploEviXRFTestFile.objects.filter(exploEviXRF = exploEviXRF)
        # for exploEviXRFTestFileUp in exploEviXRFTestFiles:
        #     exploEviXRFTestFileUp.delete()
        XRF1s = []
        for index, url in enumerate(XRFs):
            # 会自动填入exploEviId
            XRF = exploEviXRFTestFile.objects.create(excelURL=url,exploEviXRF = exploEviXRF,exploEviId = exploEviXRF.exploEvi_id)
            blog = exploEviXRFTestFileSerializer(XRF, context=self.context)
            XRF1s.append(blog.data['excelURL'])
        # 对上传的文档预处理取平均，再将取完平均的回填
        return {
                'return_XRFs':XRF1s,
                'exploEviXRF':exploEviXRF}
class exploEviXRFSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    inputDate = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    miningList = serializers.CharField(read_only=True,)
    pnpList = serializers.CharField(read_only=True,)
    ppList = serializers.CharField(read_only=True, )
    gmList = serializers.CharField(read_only=True, )
    soilList = serializers.CharField(read_only=True, )
    tagList = serializers.CharField(read_only=True, )
    class Meta:
        model = exploEviXRF
        fields = "__all__"
        # fields = ("id","exploSample","devDetect","methodDetect", "user","inputDate","excelHandledURL")
class exploEviXRFDetailSerializer(serializers.ModelSerializer):
    # 被指向用related_name来连接
    exploEviXRFTestFile = exploEviXRFTestFileSerializer(many = True)
    # 自身的外键直接用serializer代替即可
    user = UserDetailSerializer()


    class Meta:
        model = exploEviXRF
        fields = ("id","exploEvi","devDetect","methodDetect", "user","inputDate","exploEviXRFTestFile")


class exploEviGCMSTestFileSerializer(serializers.ModelSerializer):
    txtHandledURL = serializers.FileField(read_only=True, )

    def __str__(self):
        return "%s,%s" % (self.type,self.txtURL)

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                field = getattr(instance, attr)
                field.set(value)
            else:
                setattr(instance, attr, value)

        #对txt进行预处理，再平均
        # exploEviGCMSTestFiles = exploEviGCMSTestFile.objects.filter(exploEviGCMS = instance.exploEviGCMS)
        instance.txtHandledURL = "file/exploEviGCMSTestFile/GM1923-扫描247_hF4jw4W.txt" #假定成功标志
        instance.save()
        return instance

    class Meta:
        model = exploEviGCMSTestFile
        fields = "__all__"
class LsitExploEviGCMSTestFileSerializer(serializers.Serializer):
    # 用于接收多个文件
    GCMSs = serializers.ListField(
        child=serializers.FileField(max_length=100000, allow_empty_file=False, use_url=True),
        write_only=True )
    #用于接收外键,GCMSTestFile的外键也是GCMS，AverFile只是用来取平均的
    exploEviGCMS = serializers.PrimaryKeyRelatedField(required=True, queryset=exploEviGCMS.objects.all())
    # 保证Id只是我们内部维护的
    exploEviId = serializers.IntegerField(read_only=True,)
    type = serializers.CharField(max_length=20,)
    # 返回的多个文件列表
    return_GCMSs = serializers.ListField(
        child=serializers.CharField(max_length=10000,),
        read_only=True )

    def create(self, validated_data):
        GCMSs = validated_data.get('GCMSs')
        exploEviGCMS = validated_data.get('exploEviGCMS')
        type = validated_data.get('type')
        # 新建重复也不可以覆盖！！否则就和修改一样了啊
        # exploEviGCMSTestFiles = exploEviGCMSTestFile.objects.filter(exploEviGCMS = exploEviGCMS)
        # for exploEviGCMSTestFileUp in exploEviGCMSTestFiles:
        #     exploEviGCMSTestFileUp.delete()
        GCMS1s = []
        for index, url in enumerate(GCMSs):
            # 会自动填入exploEviId
            GCMS = exploEviGCMSTestFile.objects.create(txtURL=url,type=type,exploEviGCMS = exploEviGCMS,exploEviId = exploEviGCMS.exploEvi_id)
            blog = exploEviGCMSTestFileSerializer(GCMS, context=self.context)
            GCMS1s.append(blog.data['txtURL'])
        # 对上传的文档预处理取平均，再将取完平均的回填到exploEviGCMSAverFile
        return {
                'return_GCMSs':GCMS1s,
                'exploEviGCMS':exploEviGCMS}
class exploEviGCMSSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    inputDate = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = exploEviGCMS
        fields = "__all__"
class exploEviGCMSDetailSerializer(serializers.ModelSerializer):
    inputDate = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    user = UserDetailSerializer()
    exploEviGCMSTestFile = exploEviGCMSTestFileSerializer(many=True)

    class Meta:
        model = exploEviGCMS
        fields = ("id","exploEvi","devDetect","methodDetect", "user","inputDate","exploEviGCMSTestFile")

class devEviSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    inputDate = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = devEvi
        fields = "__all__"

class devEviFTIRTestFileSerializer(serializers.ModelSerializer):
    txtHandledURL = serializers.FileField(read_only=True, )
    def __str__(self):
        return self.txtURL

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                field = getattr(instance, attr)
                field.set(value)
            else:
                setattr(instance, attr, value)

        #对txt进行预处理，再平均
        # devEviFTIRTestFiles = devEviFTIRTestFile.objects.filter(devEviFTIR = instance.devEviFTIR)
        instance.txtHandledURL = "file/devEviFTIRTestFile/GM1923-扫描247_hF4jw4W.txt" #假定成功标志
        instance.save()
        return instance

    class Meta:
        model = devEviFTIRTestFile
        fields = "__all__"
class LsitdevEviFTIRTestFileSerializer(serializers.Serializer):
    # 用于接收多个文件
    FTIRs = serializers.ListField(
        child=serializers.FileField(max_length=100000, allow_empty_file=False, use_url=True),
        write_only=True )
    #用于接收外键
    devEviFTIR = serializers.PrimaryKeyRelatedField(required=True, queryset=devEviFTIR.objects.all())
    # 保证Id只是我们内部维护的
    devEviId = serializers.IntegerField(read_only=True,)
    # 返回的多个文件列表
    return_FTIRs = serializers.ListField(
        child=serializers.CharField(max_length=10000,),
        read_only=True )

    def create(self, validated_data):
        FTIRs = validated_data.get('FTIRs')
        devEviFTIR = validated_data.get('devEviFTIR')
        # 新建重复也不可以覆盖！！否则就和修改一样了啊
        # devEviFTIRTestFiles = devEviFTIRTestFile.objects.filter(devEviFTIR = devEviFTIR)
        # for devEviFTIRTestFileUp in devEviFTIRTestFiles:
        #     devEviFTIRTestFileUp.delete()
        FTIR1s = []
        for index, url in enumerate(FTIRs):
            # 会自动填入devEviId
            devEviId = devEviFTIR.devEvi_id
            FTIR = devEviFTIRTestFile.objects.create(txtURL=url,devEviFTIR = devEviFTIR,devEviId =devEviId )
            # 文件预处理
            # 新增一个物证文件时，该FTIR表中此物证的匹配结果必然是空的，此外因为更新走的也是补录的路径
            # 因此如果新增物证文件，要将综合表和报告表中的此物证的删去来提示用户进行重新匹配
            compMatchs = devCompMatch.objects.filter(devEvi= devEviId)
            for compMatch in compMatchs:
                compMatch.delete()
            synMatchs = devSynMatch.objects.filter(devEvi_id= devEviId)
            for synMatch in synMatchs:
                synMatch.delete()

            blog = devEviFTIRTestFileSerializer(FTIR, context=self.context)
            FTIR1s.append(blog.data['txtURL'])
        return {
                'return_FTIRs':FTIR1s,
                'devEviFTIR':devEviFTIR}
class devEviFTIRSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    inputDate = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = devEviFTIR
        fields = "__all__"
class devEviFTIRDetailSerializer(serializers.ModelSerializer):
    # 被指向用related_name来连接
    devEviFTIRTestFile = devEviFTIRTestFileSerializer(many = True)
    # 自身的外键直接用serializer代替即可
    user = UserDetailSerializer()

    class Meta:
        model = devEviFTIR
        fields = ("id","devEvi","devDetect","methodDetect", "user","inputDate","devEviFTIRTestFile")

class devEviRamanTestFileSerializer(serializers.ModelSerializer):
    txtHandledURL = serializers.FileField(read_only=True, )
    def __str__(self):
        return self.txtURL

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                field = getattr(instance, attr)
                field.set(value)
            else:
                setattr(instance, attr, value)

        #对txt进行预处理，再平均
        # devEviRamanTestFiles = devEviRamanTestFile.objects.filter(devEviRaman = instance.devEviRaman)
        instance.txtHandledURL = "file/devEviRamanTestFile/GM1923-扫描247_hF4jw4W.txt" #假定成功标志
        instance.save()
        return instance

    class Meta:
        model = devEviRamanTestFile
        fields = "__all__"
class LsitdevEviRamanTestFileSerializer(serializers.Serializer):
    # 用于接收多个文件
    Ramans = serializers.ListField(
        child=serializers.FileField(max_length=100000, allow_empty_file=False, use_url=True),
        write_only=True )
    #用于接收外键
    devEviRaman = serializers.PrimaryKeyRelatedField(required=True, queryset=devEviRaman.objects.all())
    # 保证Id只是我们内部维护的
    devEviId = serializers.IntegerField(read_only=True,)
    # 返回的多个文件列表
    return_Ramans = serializers.ListField(
        child=serializers.CharField(max_length=10000,),
        read_only=True )

    def create(self, validated_data):
        Ramans = validated_data.get('Ramans')
        devEviRaman = validated_data.get('devEviRaman')
        # 新建重复也不可以覆盖！！否则就和修改一样了啊
        # devEviRamanTestFiles = devEviRamanTestFile.objects.filter(devEviRaman = devEviRaman)
        # for devEviRamanTestFileUp in devEviRamanTestFiles:
        #     devEviRamanTestFileUp.delete()
        Raman1s = []
        for index, url in enumerate(Ramans):
            # 会自动填入devEviId
            devEviId = devEviRaman.devEvi_id
            Raman = devEviRamanTestFile.objects.create(txtURL=url,devEviRaman = devEviRaman,devEviId =devEviId )
            # 文件预处理
            # 新增一个物证文件时，该Raman表中此物证的匹配结果必然是空的，此外因为更新走的也是补录的路径
            # 因此如果新增物证文件，要将综合表和报告表中的此物证的删去来提示用户进行重新匹配
            compMatchs = devCompMatch.objects.filter(devEvi= devEviId)
            for compMatch in compMatchs:
                compMatch.delete()
            synMatchs = devSynMatch.objects.filter(devEvi_id= devEviId)
            for synMatch in synMatchs:
                synMatch.delete()

            blog = devEviRamanTestFileSerializer(Raman, context=self.context)
            Raman1s.append(blog.data['txtURL'])
        return {
                'return_Ramans':Raman1s,
                'devEviRaman':devEviRaman}
class devEviRamanSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    inputDate = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = devEviRaman
        fields = "__all__"
class devEviRamanDetailSerializer(serializers.ModelSerializer):
    # 被指向用related_name来连接
    devEviRamanTestFile = devEviRamanTestFileSerializer(many = True)
    # 自身的外键直接用serializer代替即可
    user = UserDetailSerializer()

    class Meta:
        model = devEviRaman
        fields = ("id","devEvi","devDetect","methodDetect", "user","inputDate","devEviRamanTestFile")

class devEviXRFTestFileSerializer(serializers.ModelSerializer):
    miningList = serializers.CharField(read_only=True,)
    pnpList = serializers.CharField(read_only=True,)
    ppList = serializers.CharField(read_only=True, )
    gmList = serializers.CharField(read_only=True, )
    soilList = serializers.CharField(read_only=True, )
    tagList = serializers.CharField(read_only=True, )

    def __str__(self):
        return self.excelURL

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                field = getattr(instance, attr)
                field.set(value)
            else:
                setattr(instance, attr, value)

        #对excel进行预处理，填入各有效值
        # devEviXRFTestFiles = devEviXRFTestFile.objects.filter(devEviXRF = instance.devEviXRF)
        instance.save()
        return instance

    class Meta:
        model = devEviXRFTestFile
        fields = "__all__"
class LsitdevEviXRFTestFileSerializer(serializers.Serializer):
    # 用于接收多个文件
    XRFs = serializers.ListField(
        child=serializers.FileField(max_length=100000, allow_empty_file=False, use_url=True),
        write_only=True )
    #用于接收外键
    devEviXRF = serializers.PrimaryKeyRelatedField(required=True, queryset=devEviXRF.objects.all())
    # 保证Id只是我们内部维护的
    devEviId = serializers.IntegerField(read_only=True,)
    # 返回的多个文件列表
    return_XRFs = serializers.ListField(
        child=serializers.CharField(max_length=10000,),
        read_only=True )

    def create(self, validated_data):
        XRFs = validated_data.get('XRFs')
        devEviXRF = validated_data.get('devEviXRF')
        # 新建重复也不可以覆盖！！否则就和修改一样了啊
        # devEviXRFTestFiles = devEviXRFTestFile.objects.filter(devEviXRF = devEviXRF)
        # for devEviXRFTestFileUp in devEviXRFTestFiles:
        #     devEviXRFTestFileUp.delete()
        XRF1s = []
        for index, url in enumerate(XRFs):
            # 会自动填入devEviId
            XRF = devEviXRFTestFile.objects.create(excelURL=url,devEviXRF = devEviXRF,devEviId = devEviXRF.devEvi_id)
            blog = devEviXRFTestFileSerializer(XRF, context=self.context)
            XRF1s.append(blog.data['excelURL'])
        # 对上传的文档预处理取平均，再将取完平均的回填
        return {
                'return_XRFs':XRF1s,
                'devEviXRF':devEviXRF}
class devEviXRFSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    inputDate = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    miningList = serializers.CharField(read_only=True,)
    pnpList = serializers.CharField(read_only=True,)
    ppList = serializers.CharField(read_only=True, )
    gmList = serializers.CharField(read_only=True, )
    soilList = serializers.CharField(read_only=True, )
    tagList = serializers.CharField(read_only=True, )
    class Meta:
        model = devEviXRF
        fields = "__all__"
class devEviXRFDetailSerializer(serializers.ModelSerializer):
    # 被指向用related_name来连接
    devEviXRFTestFile = devEviXRFTestFileSerializer(many = True)
    # 自身的外键直接用serializer代替即可
    user = UserDetailSerializer()

    class Meta:
        model = devEviXRF
        fields = ("id","devEvi","devDetect","methodDetect", "user","inputDate","devEviXRFTestFile")


class devShapeEviSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    inputDate = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    blackWhiteUrl =serializers.FileField(read_only=True,)
    interColorUrl =serializers.FileField(read_only=True,)
    featureUrl =serializers.FileField(read_only=True,)
    resultPicUrl =serializers.FileField(read_only=True,)
    resultFileUrl = serializers.FileField(read_only=True, )
    nomUrl = serializers.FileField(read_only=True, )
    nomResolution = serializers.FileField(read_only=True, )

    class Meta:
        model = devShapeEvi
        fields = "__all__"