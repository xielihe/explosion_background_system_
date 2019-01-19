# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework.validators import UniqueTogetherValidator
import os,shutil
import numpy as np

from apps.sample.models import *
from apps.basic.models import *
from apps.basic.serializers import UserDetailSerializer
from apps.match.models import *
from apps.utils.PreProcess import *
from bzxt117.settings import MEDIA_ROOT
from utils.PreProcess import preProcess

class exploSampleSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    inputDate = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    # read_only前端写也写不进去！！！

    class Meta:
        model = exploSample
        fields = "__all__"
class exploSampleFTIRTestFileSerializer(serializers.ModelSerializer):
    handledData = serializers.SerializerMethodField()
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
        model = exploSampleFTIRTestFile
        fields = ("id","exploSampleFTIR","txtURL","handledData")
class LsitExploSampleFTIRTestFileSerializer(serializers.Serializer):
    FTIRs = serializers.ListField(
        child=serializers.FileField(max_length=100000, allow_empty_file=False, use_url=True),
        write_only=True )
    exploSampleFTIR = serializers.PrimaryKeyRelatedField(required=True,write_only=True, queryset=exploSampleFTIR.objects.all())
    #
    # return_FTIRs = serializers.ListField(
    #     child=serializers.CharField(max_length=10000,),
    #     read_only=True )

    # 增添和更新都必须是多文件，且这个更新和其他更新不同，更新会覆盖，但新建不会覆盖，每次新建上传完都会进行取平均，替换平均文件
    def create(self, validated_data):
        FTIRs = validated_data.get('FTIRs')
        exploSampleFTIR = validated_data.get('exploSampleFTIR')
        result = []
        for index, url in enumerate(FTIRs):
            FTIR = exploSampleFTIRTestFile.objects.create(txtURL=url,exploSampleFTIR = exploSampleFTIR)
            result =  preProcess('FTIR',exploSampleFTIR.id,FTIR.id,os.path.join(MEDIA_ROOT,str(FTIR.txtURL)))
            if result[0] == '0' :
                FTIR.txtHandledURL = result[1]
                FTIR.save()
            # 文件预处理，更新FTIR匹配表和综合匹配表的结果

        # 对上传的文档预处理取平均，再将取完平均的回填
        return {}
class exploSampleFTIRSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    inputDate = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    class Meta:
        model = exploSampleFTIR
        fields = ("id","exploSample","devDetect","methodDetect", "user","inputDate")
class exploSampleFTIRDetailSerializer(serializers.ModelSerializer):
    # 被指向用related_name来连接
    exploSampleFTIRTestFile = exploSampleFTIRTestFileSerializer(many = True)
    # 自身的外键直接用serializer代替即可
    user = UserDetailSerializer()

    class Meta:
        model = exploSampleFTIR
        fields = ("id","exploSample","devDetect","methodDetect", "user","inputDate","exploSampleFTIRTestFile")

class exploSampleRamanTestFileSerializer(serializers.ModelSerializer):
    handledData = serializers.SerializerMethodField()

    def get_handledData(self, obj):
        path = obj.txtHandledURL
        if os.path.exists(path) == True:
            data = np.load(path)
            return data
    def __str__(self):
        return self.txtURL

    class Meta:
        model = exploSampleRamanTestFile
        fields = ("id","exploSampleRaman","txtURL","handledData")
class LsitExploSampleRamanTestFileSerializer(serializers.Serializer):
    Ramans = serializers.ListField(
        child=serializers.FileField(max_length=100000, allow_empty_file=False, use_url=True),
        write_only=True )
    exploSampleRaman = serializers.PrimaryKeyRelatedField(required=True, write_only=True, queryset=exploSampleRaman.objects.all())

    # 增添和更新都必须是多文件，且这个更新和其他更新不同，更新会覆盖，但新建不会覆盖，每次新建上传完都会进行取平均，替换平均文件
    def create(self, validated_data):
        Ramans = validated_data.get('Ramans')
        exploSampleRaman = validated_data.get('exploSampleRaman')
        result = []
        for index, url in enumerate(Ramans):
            Raman = exploSampleRamanTestFile.objects.create(txtURL=url,exploSampleRaman = exploSampleRaman)
            result =  preProcess('RAMAN',exploSampleRaman.id,Raman.id,os.path.join(MEDIA_ROOT,str(Raman.txtURL)))
            if result[0] == '0' :
                Raman.txtHandledURL = result[1]
                Raman.save()
            # 文件预处理，更新Raman匹配表和综合匹配表的结果
        return {}
class exploSampleRamanSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    inputDate = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    class Meta:
        model = exploSampleRaman
        fields = ("id","exploSample","devDetect","methodDetect", "user","inputDate")
class exploSampleRamanDetailSerializer(serializers.ModelSerializer):
    # 被指向用related_name来连接
    exploSampleRamanTestFile = exploSampleRamanTestFileSerializer(many = True)
    # 自身的外键直接用serializer代替即可
    user = UserDetailSerializer()

    class Meta:
        model = exploSampleRaman
        fields = ("id","exploSample","devDetect","methodDetect", "user","inputDate","exploSampleRamanTestFile")

class exploSampleXRDTestFileSerializer(serializers.ModelSerializer):
    handledData = serializers.SerializerMethodField()

    def get_handledData(self, obj):
        path = obj.txtHandledURL
        if os.path.exists(path) == True:
            data = np.load(path)
            return data
    def __str__(self):
        return self.txtURL

    class Meta:
        model = exploSampleXRDTestFile
        fields = ("id","exploSampleXRD","txtURL","handledData")
class LsitExploSampleXRDTestFileSerializer(serializers.Serializer):
    XRDs = serializers.ListField(
        child=serializers.FileField(max_length=100000, allow_empty_file=False, use_url=True),
        write_only=True )
    exploSampleXRD = serializers.PrimaryKeyRelatedField(required=True,write_only=True, queryset=exploSampleXRD.objects.all())

    # 增添和更新都必须是多文件，且这个更新和其他更新不同，更新会覆盖，但新建不会覆盖，每次新建上传完都会进行取平均，替换平均文件
    def create(self, validated_data):
        XRDs = validated_data.get('XRDs')
        exploSampleXRD = validated_data.get('exploSampleXRD')
        result = []
        for index, url in enumerate(XRDs):
            XRD = exploSampleXRDTestFile.objects.create(txtURL=url,exploSampleXRD = exploSampleXRD)
            result =  preProcess('XRD',exploSampleXRD.id,XRD.id,os.path.join(MEDIA_ROOT,str(XRD.txtURL)))
            if result[0] == '0':
                XRD.txtHandledURL = result[1]
                XRD.save()
            # 文件预处理，更新XRD匹配表和综合匹配表的结果
        return {}
class exploSampleXRDSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    inputDate = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    class Meta:
        model = exploSampleXRD
        fields = ("id","exploSample","devDetect","methodDetect", "user","inputDate")
class exploSampleXRDDetailSerializer(serializers.ModelSerializer):
    # 被指向用related_name来连接
    exploSampleXRDTestFile = exploSampleXRDTestFileSerializer(many = True)
    # 自身的外键直接用serializer代替即可
    user = UserDetailSerializer()

    class Meta:
        model = exploSampleXRD
        fields = ("id","exploSample","devDetect","methodDetect", "user","inputDate","exploSampleXRDTestFile")

class exploSampleXRFTestFileSerializer(serializers.ModelSerializer):
    handledData = serializers.SerializerMethodField()

    def get_handledData(self, obj):
        path = obj.handledURL
        if os.path.exists(path) == True:
            data = np.load(path)
            return data
    def __str__(self):
        return self.excelURL

    class Meta:
        model = exploSampleXRFTestFile
        fields =("id","exploSampleXRF","excelURL","handledData")
class LsitExploSampleXRFTestFileSerializer(serializers.Serializer):
    # 用于接收多个文件
    XRFs = serializers.ListField(
        child=serializers.FileField(max_length=100000, allow_empty_file=False, use_url=True),
        write_only=True )
    #用于接收外键
    exploSampleXRF = serializers.PrimaryKeyRelatedField(required=True, write_only=True,queryset=exploSampleXRF.objects.all())
    def create(self, validated_data):
        XRFs = validated_data.get('XRFs')
        exploSampleXRF = validated_data.get('exploSampleXRF')
        # 新建重复也不可以覆盖！！否则就和修改一样了啊
        # exploSampleXRFTestFiles = exploSampleXRFTestFile.objects.filter(exploSampleXRF = exploSampleXRF)
        # for exploSampleXRFTestFileUp in exploSampleXRFTestFiles:
        #     exploSampleXRFTestFileUp.delete()
        result = []
        for index, url in enumerate(XRFs):
            # 会自动填入exploSampleId
            XRF = exploSampleXRFTestFile.objects.create(excelURL=url,exploSampleXRF = exploSampleXRF)
            result = preProcess('XRF',exploSampleXRF.id,XRF.id,os.path.join(MEDIA_ROOT,str(XRF.excelURL)))
            if result[0] == '0':
                XRF.handledURL = result[1]
                XRF.save()
        return {}
class exploSampleXRFSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    inputDate = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    class Meta:
        model = exploSampleXRF
        fields = "__all__"
        # fields = ("id","exploSample","devDetect","methodDetect", "user","inputDate","excelHandledURL")
class exploSampleXRFDetailSerializer(serializers.ModelSerializer):
    # 被指向用related_name来连接
    exploSampleXRFTestFile = exploSampleXRFTestFileSerializer(many = True)
    # 自身的外键直接用serializer代替即可
    user = UserDetailSerializer()

    class Meta:
        model = exploSampleXRF
        fields = ("id","exploSample","devDetect","methodDetect", "user","inputDate","exploSampleXRFTestFile")

class exploSampleGCMSTestFileSerializer(serializers.ModelSerializer):

    def __str__(self):
        return "%s,%s" % (self.type,self.txtURL)

    class Meta:
        model = exploSampleGCMSTestFile
        fields = "__all__"
class exploSampleGCMSFileSerializer(serializers.ModelSerializer):
    handledData = serializers.SerializerMethodField()

    def get_handledData(self, obj):
        path = obj.txtHandledURL
        if os.path.exists(path) == True:
            data = np.load(path).item()
            return data

    class Meta:
        model = exploSampleGCMSFile
        fields = ("id","exploSampleGCMS","handledData")
class LsitExploSampleGCMSTestFileSerializer(serializers.Serializer):
    # 用于接收多个文件
    GCMSs = serializers.ListField(
        child=serializers.FileField(max_length=100000, allow_empty_file=False, use_url=True),
        write_only=True )
    #用于接收外键,GCMSTestFile的外键也是GCMS，AverFile只是用来取平均的
    exploSampleGCMS = serializers.PrimaryKeyRelatedField(required=True, write_only=True,queryset=exploSampleGCMS.objects.all())

    def create(self, validated_data):
        GCMSs = validated_data.get('GCMSs')
        exploSampleGCMS = validated_data.get('exploSampleGCMS')
        # type = validated_data.get('type')
        # 新建重复也不可以覆盖！！否则就和修改一样了啊
        # exploSampleGCMSTestFiles = exploSampleGCMSTestFile.objects.filter(exploSampleGCMS = exploSampleGCMS)
        # for exploSampleGCMSTestFileUp in exploSampleGCMSTestFiles:
        #     exploSampleGCMSTestFileUp.delete()
        # 新创建的GCMS对象列表
        GCMS2s = []
        # GCMS3s = []
        filePath = ""
        TICId = 0
        result = []
        for index, url in enumerate(GCMSs):
            # 会自动填入exploSampleId
            # 从url中知道type，如果是TIC的type，那么就创建一个以此id和样本id联合的文件夹用来存放这一批的文档，
            # 先存下来，再移动
            GCMS = exploSampleGCMSTestFile.objects.create(txtURL=url, exploSampleGCMS = exploSampleGCMS)
            name = url.name
            type = os.path.splitext(name)[0]
            GCMS.type = type
            GCMS.save()
            if type == "TIC":
                filePath = os.path.join(MEDIA_ROOT,"file/exploSampleGCMSTestFile/%d_%d/" % (exploSampleGCMS.exploSample_id,GCMS.id))
                os.makedirs(filePath)
                TICId = GCMS.id
            GCMS2s.append(GCMS)
        for GCMS2 in GCMS2s:
            prePath =os.path.join(MEDIA_ROOT,str(GCMS2.txtURL))
            name = os.path.basename(prePath)
            newPath = os.path.join(filePath,name)
            shutil.move(prePath, newPath)
            GCMS2.txtURL = newPath
            GCMS2.save()
        GCMSFile = exploSampleGCMSFile.objects.create(exploSampleGCMS = exploSampleGCMS)
        result = preProcess('GCMS',exploSampleGCMS.id, GCMSFile.id, filePath)
        if result[0] == '0':
            GCMSFile.txtHandledURL = result[1]
            GCMSFile.save()
        # result = preProcess('GCMS', exploSampleGCMS.id, TICId, filePath)
        # if result[0] == '0':
        #     exploSampleGCMSFile.objects.create(exploSampleGCMS = exploSampleGCMS,txtHandledURL = result[1])
        # 预处理方法，给filePath即为所在的文件夹
        #     blog = exploSampleGCMSFileSerializer(GCMS2, context=self.context)
        #     GCMS3s.append(blog.data['handledData'])
        # 处理完一批我就删掉？
        # 对上传的文档预处理取平均，再将取完平均的回填到exploSampleGCMSAverFile
        return {}
class exploSampleGCMSSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    inputDate = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = exploSampleGCMS
        fields = "__all__"
class exploSampleGCMSDetailSerializer(serializers.ModelSerializer):
    inputDate = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    user = UserDetailSerializer()
    exploSampleGCMSFile = exploSampleGCMSFileSerializer(many=True)

    class Meta:
        model = exploSampleGCMS
        fields = ("id","exploSample","devDetect","methodDetect", "user","inputDate","exploSampleGCMSFile")

class exploSampleDetailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    inputDate = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    exploSampleFTIR = exploSampleFTIRDetailSerializer(many= True)
    exploSampleRaman = exploSampleRamanDetailSerializer(many= True)
    exploSampleXRD = exploSampleXRDDetailSerializer(many= True)
    exploSampleXRF = exploSampleXRFDetailSerializer(many= True)
    exploSampleGCMS = exploSampleGCMSDetailSerializer(many=True)

   # read_only前端写也写不进去！！！

    class Meta:
        model = exploSample
        fields =("id",'sname','snameAbbr','user','inputDate','sampleOrigin','factory','picUrl','note',
                 'exploSampleFTIR','exploSampleRaman','exploSampleXRD','exploSampleXRF','exploSampleGCMS')

class devSampleSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    inputDate = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = devSample
        fields = "__all__"
class devPartSampleSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    inputDate = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = devPartSample
        fields = "__all__"
class devSampleDetailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    inputDate = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    devPartSample = devPartSampleSerializer(many = True)

    class Meta:
        model = devSample
        fields =("id",'sname','user', 'inputDate','Type','Origin','Factory','Model','Logo','function','picUrl','note','devPartSample')


class devPartSampleFTIRTestFileSerializer(serializers.ModelSerializer):
    handledData = serializers.SerializerMethodField()

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
        model = devPartSampleFTIRTestFile
        fields = ("id","devPartSampleFTIR","txtURL","handledData")
class LsitdevPartSampleFTIRTestFileSerializer(serializers.Serializer):
    FTIRs = serializers.ListField(
        child=serializers.FileField(max_length=100000, allow_empty_file=False, use_url=True),
        write_only=True )

    devPartSampleFTIR = serializers.PrimaryKeyRelatedField(required=True, write_only=True,queryset=devPartSampleFTIR.objects.all())
    # 增添和更新都必须是多文件，且这个更新和其他更新不同，更新会覆盖，但新建不会覆盖，每次新建上传完都会进行取平均，替换平均文件
    def create(self, validated_data):
        FTIRs = validated_data.get('FTIRs')
        devPartSampleFTIR = validated_data.get('devPartSampleFTIR')
        result = []
        for index, url in enumerate(FTIRs):
            devPartSampleId = devPartSampleFTIR.devPartSample_id
            FTIR = devPartSampleFTIRTestFile.objects.create(txtURL=url,devPartSampleFTIR = devPartSampleFTIR)
            result = preProcess('FTIR',devPartSampleFTIR.id,FTIR.id,os.path.join(MEDIA_ROOT,str(FTIR.txtURL)))
            if result[0] == '0':
                FTIR.txtHandledURL = result[1]
                FTIR.save()

        # 对上传的文档预处理取平均，再将取完平均的回填
        return {}
class devPartSampleFTIRSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    inputDate = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    class Meta:
        model = devPartSampleFTIR
        fields = ("id","devPartSample","devDetect","methodDetect", "user","inputDate")
class devPartSampleFTIRDetailSerializer(serializers.ModelSerializer):
    # 被指向用related_name来连接
    devPartSampleFTIRTestFile = devPartSampleFTIRTestFileSerializer(many = True)
    # 自身的外键直接用serializer代替即可
    user = UserDetailSerializer()

    class Meta:
        model = devPartSampleFTIR
        fields = ("id","devPartSample","devDetect","methodDetect", "user","inputDate","devPartSampleFTIRTestFile")

class devPartSampleRamanTestFileSerializer(serializers.ModelSerializer):
    handledData = serializers.SerializerMethodField()

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
        model = devPartRamanTestFile
        fields = ("id","devPartSampleRaman","txtURL","handledData")
class LsitdevPartSampleRamanTestFileSerializer(serializers.Serializer):
    Ramans = serializers.ListField(
        child=serializers.FileField(max_length=100000, allow_empty_file=False, use_url=True),
        write_only=True )
    devPartSampleRaman = serializers.PrimaryKeyRelatedField(required=True, write_only=True,queryset=devPartSampleRaman.objects.all())
    # 增添和更新都必须是多文件，且这个更新和其他更新不同，更新会覆盖，但新建不会覆盖，每次新建上传完都会进行取平均，替换平均文件
    def create(self, validated_data):
        Ramans = validated_data.get('Ramans')
        devPartSampleRaman = validated_data.get('devPartSampleRaman')
        result = []
        for index, url in enumerate(Ramans):
            devPartSampleId = devPartSampleRaman.devPartSample_id
            Raman = devPartRamanTestFile.objects.create(txtURL=url,devPartSampleRaman = devPartSampleRaman)
            result = preProcess('RAMAN',devPartSampleRaman.id,Raman.id,os.path.join(MEDIA_ROOT,str(Raman.txtURL)))
            if result[0] == '0':
                Raman.txtHandledURL = result[1]
                Raman.save()
            # 文件预处理，更新Raman匹配表和综合匹配表的结果

        return {}
class devPartSampleRamanSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    inputDate = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    class Meta:
        model = devPartSampleRaman
        fields = ("id","devPartSample","devDetect","methodDetect", "user","inputDate")
class devPartSampleRamanDetailSerializer(serializers.ModelSerializer):
    # 被指向用related_name来连接
    devPartRamanTestFile = devPartSampleRamanTestFileSerializer(many = True)
    # 自身的外键直接用serializer代替即可
    user = UserDetailSerializer()

    class Meta:
        model = devPartSampleRaman
        fields = ("id","devPartSample","devDetect","methodDetect", "user","inputDate","devPartRamanTestFile")

class devPartSampleXRFTestFileSerializer(serializers.ModelSerializer):
    handledData = serializers.SerializerMethodField()

    def get_handledData(self, obj):
        path =obj.handledURL
        if os.path.exists(path) == True:
            data = np.load(path)
        # print(type(data))
        # print(data[0])

            return data
    def __str__(self):
        return self.excelURL

    class Meta:
        model = devPartSampleXRFTestFile
        fields =("id","devPartSampleXRF","excelURL","handledData")
class LsitdevPartSampleXRFTestFileSerializer(serializers.Serializer):
    XRFs = serializers.ListField(
        child=serializers.FileField(max_length=100000, allow_empty_file=False, use_url=True),
        write_only=True )

    devPartSampleXRF = serializers.PrimaryKeyRelatedField(required=True, write_only=True ,queryset=devPartSampleXRF.objects.all())
    # 增添和更新都必须是多文件，且这个更新和其他更新不同，更新会覆盖，但新建不会覆盖，每次新建上传完都会进行取平均，替换平均文件
    def create(self, validated_data):
        XRFs = validated_data.get('XRFs')
        devPartSampleXRF = validated_data.get('devPartSampleXRF')
        result = []
        for index, url in enumerate(XRFs):
            devPartSampleId = devPartSampleXRF.devPartSample_id
            XRF = devPartSampleXRFTestFile.objects.create(excelURL=url,devPartSampleXRF = devPartSampleXRF)
            result = preProcess('XRF', devPartSampleXRF.id, XRF.id, os.path.join(MEDIA_ROOT, str(XRF.excelURL)))
            if result[0] == '0':
                XRF.handledURL = result[1]
                XRF.save()
            # 文件预处理，更新XRF匹配表和综合匹配表的结果
            # 样本库更新报告都得变

        return {}
class devPartSampleXRFSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    inputDate = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    class Meta:
        model = devPartSampleXRF
        fields = "__all__"
class devPartSampleXRFDetailSerializer(serializers.ModelSerializer):
    # 被指向用related_name来连接
    devPartSampleXRFTestFile = devPartSampleXRFTestFileSerializer(many = True)
    # 自身的外键直接用serializer代替即可
    user = UserDetailSerializer()

    class Meta:
        model = devPartSampleXRF
        fields = ("id","devPartSample","devDetect","methodDetect", "user","inputDate","devPartSampleXRFTestFile")

class devShapeSampleSerializer(serializers.ModelSerializer):
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
        model = devShapeSample
        fields = "__all__"

class devPartSampleDetailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    inputDate = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    devPartSampleFTIR = devPartSampleFTIRDetailSerializer(many = True)
    devPartSampleRaman = devPartSampleRamanDetailSerializer(many= True)
    devPartSampleXRF = devPartSampleXRFDetailSerializer(many= True)
    devShapeSample = devShapeSampleSerializer(many= True)

    class Meta:
        model = devPartSample
        fields = ("id",'sname', 'devSample','user','inputDate','sampleType','Origin','Factory','Model','Logo'
                  ,'function','Color','Material','Shape','thickness','picUrl','note','devPartSampleFTIR','devPartSampleRaman',
                  'devPartSampleXRF','devShapeSample')