# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.serializers import *
import os,shutil
import numpy as np

from apps.evi.models import *
from apps.basic.models import *
from apps.basic.serializers import UserDetailSerializer
from apps.match.models import *
from bzxt117.settings import MEDIA_ROOT
from utils.PreProcess import preProcess



class exploEviSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    inputDate = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = exploEvi
        fields = "__all__"


class exploEviFTIRTestFileSerializer(serializers.ModelSerializer):
    handledData = serializers.SerializerMethodField()
    exploEviId = serializers.IntegerField(read_only= True)

    def get_handledData(self, obj):
        path =obj.txtHandledURL
        if os.path.exists(path) == True:
            data = np.load(path)
        # print(type(data))
        # print(data[0])

            return data
    def __str__(self):
        return self.txtURL

    class Meta:
        model = exploEviFTIRTestFile
        fields = ("id","exploEviFTIR","exploEviId","txtURL","handledData")
class LsitExploEviFTIRTestFileSerializer(serializers.Serializer):
    # 用于接收多个文件
    FTIRs = serializers.ListField(
        child=serializers.FileField(max_length=100000, allow_empty_file=False, use_url=True),
        write_only=True )
    #用于接收外键
    exploEviFTIR = serializers.PrimaryKeyRelatedField(required=True, write_only=True,queryset=exploEviFTIR.objects.all())
    # 保证Id只是我们内部维护的
    exploEviId = serializers.IntegerField(read_only=True,)

    def create(self, validated_data):
        FTIRs = validated_data.get('FTIRs')
        exploEviFTIR = validated_data.get('exploEviFTIR')
        # 新建重复也不可以覆盖！！否则就和修改一样了啊
        # exploEviFTIRTestFiles = exploEviFTIRTestFile.objects.filter(exploEviFTIR = exploEviFTIR)
        # for exploEviFTIRTestFileUp in exploEviFTIRTestFiles:
        #     exploEviFTIRTestFileUp.delete()
        result = []
        for index, url in enumerate(FTIRs):
            # 会自动填入exploEviId
            exploEviId = exploEviFTIR.exploEvi_id
            FTIR = exploEviFTIRTestFile.objects.create(txtURL=url,exploEviFTIR = exploEviFTIR,exploEviId =exploEviId )
            handledURL = ""
            result =  preProcess('FTIR',exploEviFTIR.id,FTIR.id,os.path.join(MEDIA_ROOT,str(FTIR.txtURL)))
            if result[0] == '0' :
                FTIR.txtHandledURL = result[1]
                FTIR.save()
            # 文件预处理
            # 新增一个物证文件时，该FTIR表中此物证的匹配结果必然是空的，此外因为更新走的也是补录的路径
            # 因此如果新增物证文件，要将综合表和报告表中的此物证的删去来提示用户进行重新匹配
            # synMatchs = exploSynMatch.objects.filter(exploEvi_id= exploEviId)
            # for synMatch in synMatchs:
            #     synMatch.delete()
        return {}
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
    handledData = serializers.SerializerMethodField()
    exploEviId = serializers.IntegerField(read_only= True)

    def get_handledData(self, obj):
        path = obj.txtHandledURL
        if os.path.exists(path) == True:
            data = np.load(path)
        # print(type(data))
        # print(data[0])

            return data
    def __str__(self):
        return self.txtURL

    class Meta:
        model = exploEviRamanTestFile
        fields = ("id","exploEviRaman","exploEviId","txtURL","handledData")
class LsitExploEviRamanTestFileSerializer(serializers.Serializer):
    # 用于接收多个文件
    Ramans = serializers.ListField(
        child=serializers.FileField(max_length=100000, allow_empty_file=False, use_url=True),
        write_only=True)
    # 用于接收外键
    exploEviRaman = serializers.PrimaryKeyRelatedField(required=True, write_only=True,queryset=exploEviRaman.objects.all())
    # 保证Id只是我们内部维护的
    exploEviId = serializers.IntegerField(read_only=True, )
    def create(self, validated_data):
        Ramans = validated_data.get('Ramans')
        exploEviRaman = validated_data.get('exploEviRaman')
        # 新建重复也不可以覆盖！！否则就和修改一样了啊
        result = []
        for index, url in enumerate(Ramans):
            # 会自动填入exploEviId
            Raman = exploEviRamanTestFile.objects.create(txtURL=url, exploEviRaman=exploEviRaman,
                                                       exploEviId=exploEviRaman.exploEvi_id)
            result =  preProcess('RAMAN',exploEviRaman.id,Raman.id,os.path.join(MEDIA_ROOT,str(Raman.txtURL)))
            if result[0] == '0':
                Raman.txtHandledURL = result[1]
                Raman.save()
        return {}
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
    handledData = serializers.SerializerMethodField()
    exploEviId = serializers.IntegerField(read_only= True)

    def get_handledData(self, obj):
        path =obj.txtHandledURL
        if os.path.exists(path) == True:
            data = np.load(path)
        # print(type(data))
        # print(data[0])

            return data
    def __str__(self):
        return self.txtURL

    class Meta:
        model = exploEviXRDTestFile
        fields = ("id","exploEviXRD","exploEviId","txtURL","handledData")
class LsitExploEviXRDTestFileSerializer(serializers.Serializer):
    # 用于接收多个文件
    XRDs = serializers.ListField(
        child=serializers.FileField(max_length=100000, allow_empty_file=False, use_url=True),
        write_only=True)
    # 用于接收外键
    exploEviXRD = serializers.PrimaryKeyRelatedField(required=True, write_only=True,queryset=exploEviXRD.objects.all())
    # 保证Id只是我们内部维护的
    exploEviId = serializers.IntegerField(read_only=True, )

    def create(self, validated_data):
        XRDs = validated_data.get('XRDs')
        exploEviXRD = validated_data.get('exploEviXRD')
        # 新建重复也不可以覆盖！！否则就和修改一样了啊
        # exploEviXRDTestFiles = exploEviXRDTestFile.objects.filter(exploEviXRD = exploEviXRD)
        # for exploEviXRDTestFileUp in exploEviXRDTestFiles:
        #     exploEviXRDTestFileUp.delete()
        result = []
        for index, url in enumerate(XRDs):
            # 会自动填入exploEviId
            XRD = exploEviXRDTestFile.objects.create(txtURL=url, exploEviXRD=exploEviXRD,
                                                       exploEviId=exploEviXRD.exploEvi_id)
            result =  preProcess('XRD',exploEviXRD.id,XRD.id,os.path.join(MEDIA_ROOT,str(XRD.txtURL)))
            if result[0] == '0':
                XRD.txtHandledURL = result[1]
                XRD.save()
        return {}
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
    handledData = serializers.SerializerMethodField()
    exploEviId = serializers.IntegerField(read_only= True)

    def get_handledData(self, obj):
        path = obj.handledURL
        if os.path.exists(path) == True:
            data = np.load(path)
        # print(type(data))
        # print(data[0])

            return data
    def __str__(self):
        return self.excelURL

    class Meta:
        model = exploEviXRFTestFile
        fields = ("id","exploEviXRF","exploEviId","excelURL","handledData")
class LsitExploEviXRFTestFileSerializer(serializers.Serializer):
    # 用于接收多个文件
    XRFs = serializers.ListField(
        child=serializers.FileField(max_length=100000, allow_empty_file=False, use_url=True),
        write_only=True )
    #用于接收外键
    exploEviXRF = serializers.PrimaryKeyRelatedField(required=True, write_only=True,queryset=exploEviXRF.objects.all())
    # 保证Id只是我们内部维护的
    exploEviId = serializers.IntegerField(read_only=True,)

    def create(self, validated_data):
        XRFs = validated_data.get('XRFs')
        exploEviXRF = validated_data.get('exploEviXRF')
        # 新建重复也不可以覆盖！！否则就和修改一样了啊
        # exploEviXRFTestFiles = exploEviXRFTestFile.objects.filter(exploEviXRF = exploEviXRF)
        # for exploEviXRFTestFileUp in exploEviXRFTestFiles:
        #     exploEviXRFTestFileUp.delete()
        result = []
        for index, url in enumerate(XRFs):
            # 会自动填入exploEviId
            XRF = exploEviXRFTestFile.objects.create(excelURL=url,exploEviXRF = exploEviXRF,exploEviId = exploEviXRF.exploEvi_id)
            result =  preProcess('XRF',exploEviXRF.id,XRF.id,os.path.join(MEDIA_ROOT,str(XRF.excelURL)))
            if result[0] == '0':
                XRF.handledURL = result[1]
                XRF.save()
        return {}
class exploEviXRFSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    inputDate = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
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
    def __str__(self):
        return "%s,%s" % (self.type,self.txtURL)
    class Meta:
        model = exploEviGCMSTestFile
        fields = "__all__"
class exploEviGCMSFileSerializer(serializers.ModelSerializer):
    handledData = serializers.SerializerMethodField()
    exploEviId = serializers.IntegerField(read_only= True)

    def get_handledData(self, obj):
        path = obj.txtHandledURL
        if os.path.exists(path) == True:
            data = np.load(path)
        # print(type(data))
        # print(data[0])

            return data

    class Meta:
        model = exploEviGCMSFile
        fields = ("id","exploEviGCMS","exploEviId","handledData")
class LsitExploEviGCMSTestFileSerializer(serializers.Serializer):
    # 用于接收多个文件
    GCMSs = serializers.ListField(
        child=serializers.FileField(max_length=100000, allow_empty_file=False, use_url=True),
        write_only=True )
    #用于接收外键,GCMSTestFile的外键也是GCMS，AverFile只是用来取平均的
    exploEviGCMS = serializers.PrimaryKeyRelatedField(required=True, queryset=exploEviGCMS.objects.all() ,write_only=True)
    # 保证Id只是我们内部维护的
    exploEviId = serializers.IntegerField(read_only=True,)
    # type = serializers.CharField(read_only= True,max_length=20,)

    def create(self, validated_data):
        GCMSs = validated_data.get('GCMSs')
        exploEviGCMS = validated_data.get('exploEviGCMS')
        # type = validated_data.get('type')
        GCMS2s = []
        result = []
        filePath = ""
        TICId = 0
        for index, url in enumerate(GCMSs):
            # 会自动填入exploSampleId
            # 从url中知道type，如果是TIC的type，那么就创建一个以此id和样本id联合的文件夹用来存放这一批的文档，
            # 先存下来，再移动
            GCMS = exploEviGCMSTestFile.objects.create(txtURL=url,exploEviGCMS = exploEviGCMS,exploEviId = exploEviGCMS.exploEvi_id)
            name = url.name
            type = os.path.splitext(name)[0]
            GCMS.type = type
            GCMS.save()
            if type == "TIC":
                filePath = os.path.join(MEDIA_ROOT, "file/exploEviGCMSTestFile/%d_%d/" % (GCMS.exploEviId, GCMS.id))
                os.makedirs(filePath)
                TICId = GCMS.id
            GCMS2s.append(GCMS)
        for GCMS2 in GCMS2s:
            prePath = os.path.join(MEDIA_ROOT, str(GCMS2.txtURL))
            name = os.path.basename(prePath)
            newPath = os.path.join(filePath, name)
            shutil.move(prePath, newPath)
            GCMS2.txtURL = newPath
            GCMS2.save()
        # 预处理方法，给filePath即为所在的文件夹
        #     blog = exploSampleGCMSFileSerializer(GCMS2, context=self.context)
        #     GCMS3s.append(blog.data['handledData'])
        # 处理完一批我就删掉？
        # 对上传的文档预处理取平均，再将取完平均的回填到exploSampleGCMSAverFile
        GCMSFile = exploEviGCMSFile.objects.create(exploEviGCMS = exploEviGCMS,exploEviId =exploEviGCMS.exploEvi_id)
        result = preProcess('GCMS', exploEviGCMS.id, GCMSFile.id, filePath)
        if result[0] == '0':
            GCMSFile.txtHandledURL = result[1]
            GCMSFile.save()
        # result = preProcess('GCMS', exploEviGCMS.id, TICId, filePath)
        # if result[0] == '0':
        #     exploEviGCMSFile.objects.create(exploEviGCMS = exploEviGCMS,exploEviId =exploEviGCMS.exploEvi_id, txtHandledURL = result[1])
        return {}
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

class exploEviDetailSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()
    inputDate = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    exploEviFTIR = exploEviFTIRDetailSerializer(many= True)
    exploEviRaman = exploEviRamanDetailSerializer(many= True)
    exploEviXRD = exploEviXRDDetailSerializer(many= True)
    exploEviXRF = exploEviXRFDetailSerializer(many= True)
    exploEviGCMS = exploEviGCMSDetailSerializer(many= True)

    class Meta:
        model = exploEvi
        fields = ('id','evidenceName','caseName','user','inputDate','picUrl','note','exploEviFTIR',
                  'exploEviRaman','exploEviXRD','exploEviXRF','exploEviGCMS')

class devEviSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    inputDate = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = devEvi
        fields = "__all__"

class devEviFTIRTestFileSerializer(serializers.ModelSerializer):
    handledData = serializers.SerializerMethodField()
    devEviId = serializers.IntegerField(read_only=True)

    def get_handledData(self, obj):
        path = obj.txtHandledURL
        if os.path.exists(path) == True:
            data = np.load(path)
        # print(type(data))
        # print(data[0])

            return data
    def __str__(self):
        return self.txtURL

    class Meta:
        model = devEviFTIRTestFile
        fields = ("id","devEviFTIR","devEviId","txtURL","handledData")
class LsitdevEviFTIRTestFileSerializer(serializers.Serializer):
    # 用于接收多个文件
    FTIRs = serializers.ListField(
        child=serializers.FileField(max_length=100000, allow_empty_file=False, use_url=True),
        write_only=True )
    #用于接收外键
    devEviFTIR = serializers.PrimaryKeyRelatedField(required=True, write_only=True,queryset=devEviFTIR.objects.all())
    # 保证Id只是我们内部维护的
    devEviId = serializers.IntegerField(read_only=True,)

    def create(self, validated_data):
        FTIRs = validated_data.get('FTIRs')
        devEviFTIR = validated_data.get('devEviFTIR')
        # 新建重复也不可以覆盖！！否则就和修改一样了啊
        # devEviFTIRTestFiles = devEviFTIRTestFile.objects.filter(devEviFTIR = devEviFTIR)
        # for devEviFTIRTestFileUp in devEviFTIRTestFiles:
        #     devEviFTIRTestFileUp.delete()
        result = []
        for index, url in enumerate(FTIRs):
            # 会自动填入devEviId
            devEviId = devEviFTIR.devEvi_id
            FTIR = devEviFTIRTestFile.objects.create(txtURL=url,devEviFTIR = devEviFTIR,devEviId =devEviId )
            # 文件预处理
            # 新增一个物证文件时，该FTIR表中此物证的匹配结果必然是空的，此外因为更新走的也是补录的路径
            # 因此如果新增物证文件，要将综合表和报告表中的此物证的删去来提示用户进行重新匹配
            result = preProcess('FTIR', devEviFTIR.id, FTIR.id, os.path.join(MEDIA_ROOT, str(FTIR.txtURL)),)
            if result[0] == '0':
                FTIR.txtHandledURL = result[1]
                FTIR.save()
        return {}
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
    handledData = serializers.SerializerMethodField()
    devEviId = serializers.IntegerField(read_only=True)

    def get_handledData(self, obj):
        path = obj.txtHandledURL
        if os.path.exists(path) == True:
            data = np.load(path)
        # print(type(data))
        # print(data[0])

            return data
    def __str__(self):
        return self.txtURL

    class Meta:
        model = devEviRamanTestFile
        fields = ("id","devEviRaman","devEviId","txtURL","handledData")
class LsitdevEviRamanTestFileSerializer(serializers.Serializer):
    # 用于接收多个文件
    Ramans = serializers.ListField(
        child=serializers.FileField(max_length=100000, allow_empty_file=False, use_url=True),
        write_only=True )
    #用于接收外键
    devEviRaman = serializers.PrimaryKeyRelatedField(required=True, write_only=True,queryset=devEviRaman.objects.all())
    # 保证Id只是我们内部维护的
    devEviId = serializers.IntegerField(read_only=True,)

    def create(self, validated_data):
        Ramans = validated_data.get('Ramans')
        devEviRaman = validated_data.get('devEviRaman')
        # 新建重复也不可以覆盖！！否则就和修改一样了啊
        # devEviRamanTestFiles = devEviRamanTestFile.objects.filter(devEviRaman = devEviRaman)
        # for devEviRamanTestFileUp in devEviRamanTestFiles:
        #     devEviRamanTestFileUp.delete()
        result = []
        for index, url in enumerate(Ramans):
            # 会自动填入devEviId
            devEviId = devEviRaman.devEvi_id
            Raman = devEviRamanTestFile.objects.create(txtURL=url,devEviRaman = devEviRaman,devEviId =devEviId )
            # 文件预处理
            # 新增一个物证文件时，该Raman表中此物证的匹配结果必然是空的，此外因为更新走的也是补录的路径
            # 因此如果新增物证文件，要将综合表和报告表中的此物证的删去来提示用户进行重新匹配
            result = preProcess('RAMAN', devEviRaman.id, Raman.id, os.path.join(MEDIA_ROOT, str(Raman.txtURL)))
            if result[0] == '0':
                Raman.txtHandledURL = result[1]
                Raman.save()
        return {}
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
    handledData = serializers.SerializerMethodField()
    devEviId = serializers.IntegerField(read_only=True)

    def get_handledData(self, obj):
        path = obj.handledURL
        if os.path.exists(path) == True:
            data = np.load(path)
        # print(type(data))
        # print(data[0])

            return data
    def __str__(self):
        return self.excelURL

    class Meta:
        model = devEviXRFTestFile
        fields = ("id","devEviXRF","devEviId","excelURL","handledData")
class LsitdevEviXRFTestFileSerializer(serializers.Serializer):
    # 用于接收多个文件
    XRFs = serializers.ListField(
        child=serializers.FileField(max_length=100000, allow_empty_file=False, use_url=True),
        write_only=True )
    #用于接收外键
    devEviXRF = serializers.PrimaryKeyRelatedField(required=True, write_only=True,queryset=devEviXRF.objects.all())
    # 保证Id只是我们内部维护的
    devEviId = serializers.IntegerField(read_only=True,)
    def create(self, validated_data):
        XRFs = validated_data.get('XRFs')
        devEviXRF = validated_data.get('devEviXRF')
        # 新建重复也不可以覆盖！！否则就和修改一样了啊
        # devEviXRFTestFiles = devEviXRFTestFile.objects.filter(devEviXRF = devEviXRF)
        # for devEviXRFTestFileUp in devEviXRFTestFiles:
        #     devEviXRFTestFileUp.delete()
        result = []
        for index, url in enumerate(XRFs):
            # 会自动填入devEviId
            XRF = devEviXRFTestFile.objects.create(excelURL=url,devEviXRF = devEviXRF,devEviId = devEviXRF.devEvi_id)
            result = preProcess('XRF', devEviXRF.id, XRF.id, os.path.join(MEDIA_ROOT, str(XRF.excelURL)))
            if result[0] == '0':
                XRF.handledURL = result[1]
                XRF.save()
        return {}
class devEviXRFSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    inputDate = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
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

class devEviDetailSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()
    inputDate = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    devEviFTIR = devEviFTIRDetailSerializer(many= True)
    devEviRaman = devEviRamanDetailSerializer(many= True)
    devEviXRF = devEviXRFDetailSerializer(many= True)
    devShapeEvi = devShapeEviSerializer(many=True)

    class Meta:
        model = devEvi
        fields = ('id','evidenceName','caseName','user','inputDate','eviType','picUrl','Factory','Model','Logo',
                  'Color','Material','Shape','thickness','note','devEviFTIR','devEviRaman','devEviXRF','devShapeEvi')
# 物证形态详情表
class devEviShapeDetailSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()
    inputDate = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    devShapeEvi = devShapeEviSerializer(many=True)

    class Meta:
        model = devEvi
        fields = ('id','evidenceName','caseName','user','inputDate','eviType','picUrl','Factory','Model','Logo',
                  'Color','Material','Shape','thickness','note','devShapeEvi')