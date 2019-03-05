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
from rest_framework.exceptions import APIException


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
        else:
            return "该预处理过的文件已被删除，无法读取"
    def __str__(self):
        return self.txtURL
    class Meta:
        model = exploSampleFTIRTestFile
        fields = ("id","exploSampleFTIR","txtURL","handledData")
class LsitExploSampleFTIRTestFileSerializer(serializers.Serializer):
    FTIRs = serializers.ListField(
        child=serializers.FileField(max_length=100000, allow_empty_file=False, use_url=True),
        write_only=True )
    exploSampleFTIR = serializers.IntegerField(required=True, write_only=True)
    #
    # return_FTIRs = serializers.ListField(
    #     child=serializers.CharField(max_length=10000,),
    #     read_only=True )

    # 增添和更新都必须是多文件，且这个更新和其他更新不同，更新会覆盖，但新建不会覆盖，每次新建上传完都会进行取平均，替换平均文件
    def create(self, validated_data):
        FTIRs = validated_data.get('FTIRs')
        exploSampleFTIRId = validated_data.get('exploSampleFTIR')

        # 差错检验
        if len(FTIRs) == 0:
            raise APIException("没有上传FTIR文件，请上传")
        if exploSampleFTIR.objects.filter(id=int(exploSampleFTIRId)).count() != 1:
            raise APIException("填入的炸药FTIR序号不存在，请重新输入")
        for index, url in enumerate(FTIRs):
            if os.path.splitext(url.name)[-1] != '.txt':
                raise APIException("有FTIR文件不是txt格式，请检查。")

        result = []
        exploSampleFTIR1 = exploSampleFTIR.objects.get(id=int(exploSampleFTIRId))

        for index, url in enumerate(FTIRs):
            FTIR = exploSampleFTIRTestFile.objects.create(txtURL=url,exploSampleFTIR = exploSampleFTIR1)
            result =  preProcess('FTIR',exploSampleFTIR1.id,FTIR.id,os.path.join(MEDIA_ROOT,str(FTIR.txtURL)))
            if result[0] == '0' :
                FTIR.txtHandledURL = result[1]
                FTIR.save()
            # 文件预处理，更新FTIR匹配表和综合匹配表的结果
            else:
                raise APIException("预处理过程出错")

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
        else:
            return "该预处理过的文件已被删除，无法读取"
    def __str__(self):
        return self.txtURL

    class Meta:
        model = exploSampleRamanTestFile
        fields = ("id","exploSampleRaman","txtURL","handledData")
class LsitExploSampleRamanTestFileSerializer(serializers.Serializer):
    Ramans = serializers.ListField(
        child=serializers.FileField(max_length=100000, allow_empty_file=False, use_url=True),
        write_only=True )
    exploSampleRaman = serializers.IntegerField(required=True, write_only=True)

    # 增添和更新都必须是多文件，且这个更新和其他更新不同，更新会覆盖，但新建不会覆盖，每次新建上传完都会进行取平均，替换平均文件
    def create(self, validated_data):
        Ramans = validated_data.get('Ramans')
        exploSampleRamanId = validated_data.get('exploSampleRaman')

        if len(Ramans) == 0:
            raise APIException("没有上传Raman文件，请上传")
        if exploSampleRaman.objects.filter(id=int(exploSampleRamanId)).count() != 1:
            raise APIException("填入的炸药Raman序号不存在，请重新输入")
        for index, url in enumerate(Ramans):
            if os.path.splitext(url.name)[-1] != '.txt':
                raise APIException("有Raman文件不是txt格式，请检查。")

        result = []
        exploSampleRaman1 = exploSampleRaman.objects.get(id=int(exploSampleRamanId))

        for index, url in enumerate(Ramans):
            Raman = exploSampleRamanTestFile.objects.create(txtURL=url,exploSampleRaman = exploSampleRaman1)
            result =  preProcess('RAMAN',exploSampleRaman1.id,Raman.id,os.path.join(MEDIA_ROOT,str(Raman.txtURL)))
            if result[0] == '0' :
                Raman.txtHandledURL = result[1]
                Raman.save()
            # 文件预处理，更新Raman匹配表和综合匹配表的结果
            else:
                raise APIException("预处理过程出错")
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
        else:
            return "该预处理过的文件已被删除，无法读取"
    def __str__(self):
        return self.txtURL

    class Meta:
        model = exploSampleXRDTestFile
        fields = ("id","exploSampleXRD","txtURL","handledData")
class LsitExploSampleXRDTestFileSerializer(serializers.Serializer):
    XRDs = serializers.ListField(
        child=serializers.FileField(max_length=100000, allow_empty_file=False, use_url=True),
        write_only=True )
    exploSampleXRD = serializers.IntegerField(required=True, write_only=True)

    # 增添和更新都必须是多文件，且这个更新和其他更新不同，更新会覆盖，但新建不会覆盖，每次新建上传完都会进行取平均，替换平均文件
    def create(self, validated_data):
        XRDs = validated_data.get('XRDs')
        exploSampleXRDId = validated_data.get('exploSampleXRD')

        # 差错检验
        if len(XRDs) == 0:
            raise APIException("没有上传XRD文件，请上传")
        if exploSampleXRD.objects.filter(id=int(exploSampleXRDId)).count() != 1:
            raise APIException("填入的炸药XRD序号不存在，请重新输入")
        for index, url in enumerate(XRDs):
            if os.path.splitext(url.name)[-1] != '.txt':
                raise APIException("有XRD文件不是txt格式，请检查。")

        result = []
        exploSampleXRD1 = exploSampleXRD.objects.get(id=int(exploSampleXRDId))

        for index, url in enumerate(XRDs):
            XRD = exploSampleXRDTestFile.objects.create(txtURL=url,exploSampleXRD = exploSampleXRD1)
            result =  preProcess('XRD',exploSampleXRD1.id,XRD.id,os.path.join(MEDIA_ROOT,str(XRD.txtURL)))
            if result[0] == '0':
                XRD.txtHandledURL = result[1]
                XRD.save()
            # 文件预处理，更新XRD匹配表和综合匹配表的结果
            else:
                raise APIException("预处理过程出错")
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
        else:
            return "该预处理过的文件已被删除，无法读取"
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
    exploSampleXRF = serializers.IntegerField(required=True, write_only=True)

    def create(self, validated_data):
        XRFs = validated_data.get('XRFs')
        exploSampleXRFId = validated_data.get('exploSampleXRF')
        # 新建重复也不可以覆盖！！否则就和修改一样了啊
        # exploSampleXRFTestFiles = exploSampleXRFTestFile.objects.filter(exploSampleXRF = exploSampleXRF)
        # for exploSampleXRFTestFileUp in exploSampleXRFTestFiles:
        #     exploSampleXRFTestFileUp.delete()
        # 差错检验
        if len(XRFs) == 0:
            raise APIException("没有上传XRF文件，请上传")
        if exploSampleXRF.objects.filter(id=int(exploSampleXRFId)).count() != 1:
            raise APIException("填入的炸药XRF序号不存在，请重新输入")
        for index, url in enumerate(XRFs):
            if os.path.splitext(url.name)[-1] != '.xlsx':
                raise APIException("有XRF文件不是excel格式，请检查。")

        result = []
        exploSampleXRF1 = exploSampleXRF.objects.get(id=int(exploSampleXRFId))

        for index, url in enumerate(XRFs):
            # 会自动填入exploSampleId
            XRF = exploSampleXRFTestFile.objects.create(excelURL=url,exploSampleXRF = exploSampleXRF1)
            result = preProcess('XRF',exploSampleXRF1.id,XRF.id,os.path.join(MEDIA_ROOT,str(XRF.excelURL)))
            if result[0] == '0':
                XRF.handledURL = result[1]
                XRF.save()
            else:
                raise APIException("预处理过程出错")
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
        else:
            return "该预处理过的文件已被删除，无法读取"

    class Meta:
        model = exploSampleGCMSFile
        fields = ("id","exploSampleGCMS","handledData")
class LsitExploSampleGCMSTestFileSerializer(serializers.Serializer):
    # 用于接收多个文件
    GCMSs = serializers.ListField(
        child=serializers.FileField(max_length=100000, allow_empty_file=False, use_url=True),
        write_only=True )
    #用于接收外键,GCMSTestFile的外键也是GCMS，AverFile只是用来取平均的
    exploSampleGCMS = serializers.IntegerField(required=True, write_only=True)

    def create(self, validated_data):
        GCMSs = validated_data.get('GCMSs')
        exploSampleGCMSId = validated_data.get('exploSampleGCMS')
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
        nameList = []

        # 差错检验
        if len(GCMSs) == 0:
            raise APIException("没有上传GC_MS文件，请上传")
        if exploSampleGCMS.objects.filter(id=int(exploSampleGCMSId)).count() != 1:
            raise APIException("填入的炸药GC_MS序号不存在，请重新输入")
        for index, url in enumerate(GCMSs):
            if os.path.splitext(url.name)[-1] != '.txt':
                raise APIException("有GCMS文件不是txt格式，请检查。")
            name = url.name
            type = os.path.splitext(name)[0]
            nameList.append(type)
        if "TIC" not in nameList:
            raise APIException("上传的GC_MS文件中没有TIC.txt文档，请重新上传")

        exploSampleGCMS1 = exploSampleGCMS.objects.get(id=int(exploSampleGCMSId))

        for index, url in enumerate(GCMSs):
            # 会自动填入exploSampleId
            # 从url中知道type，如果是TIC的type，那么就创建一个以此id和样本id联合的文件夹用来存放这一批的文档，
            # 先存下来，再移动
            GCMS = exploSampleGCMSTestFile.objects.create(txtURL=url, exploSampleGCMS = exploSampleGCMS1)
            name = url.name
            type = os.path.splitext(name)[0]
            GCMS.type = type
            GCMS.save()
            if type == "TIC":
                filePath = os.path.join(MEDIA_ROOT,"file/exploSampleGCMSTestFile/%d_%d/" % (exploSampleGCMS1.exploSample_id,GCMS.id))
                os.makedirs(filePath)
                TICId = GCMS.id
            GCMS2s.append(GCMS)
        for GCMS2 in GCMS2s:
            prePath =os.path.join(MEDIA_ROOT,str(GCMS2.txtURL))
            name = os.path.basename(prePath)
            newPath = os.path.join(filePath,name)
            if os.path.exists(prePath) == False:
                raise APIException("上传的GC_MS文件夹路径被更改，找不到文件夹，无法进行预处理")
            shutil.move(prePath, newPath)
            GCMS2.txtURL = newPath
            GCMS2.save()
        GCMSFile = exploSampleGCMSFile.objects.create(exploSampleGCMS = exploSampleGCMS1)
        result = preProcess('GCMS',exploSampleGCMS1.id, GCMSFile.id, filePath)
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
        else:
            raise APIException("预处理过程出错")
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
    user = UserDetailSerializer()
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
    user = UserDetailSerializer()
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
        else:
            return "该预处理过的文件已被删除，无法读取"
    def __str__(self):
        return self.txtURL

    class Meta:
        model = devPartSampleFTIRTestFile
        fields = ("id","devPartSampleFTIR","txtURL","handledData")
class LsitdevPartSampleFTIRTestFileSerializer(serializers.Serializer):
    FTIRs = serializers.ListField(
        child=serializers.FileField(max_length=100000, allow_empty_file=False, use_url=True),
        write_only=True )

    devPartSampleFTIR =  serializers.IntegerField(required=True, write_only=True)
    # 增添和更新都必须是多文件，且这个更新和其他更新不同，更新会覆盖，但新建不会覆盖，每次新建上传完都会进行取平均，替换平均文件
    def create(self, validated_data):
        FTIRs = validated_data.get('FTIRs')
        devPartSampleFTIRId = validated_data.get('devPartSampleFTIR')

        # 差错检验
        if len(FTIRs) == 0:
            raise APIException("没有上传FTIR文件，请上传")
        if devPartSampleFTIR.objects.filter(id=int(devPartSampleFTIRId)).count() != 1:
            raise APIException("填入的爆炸装置零件的FTIR序号不存在，请重新输入")
        for index, url in enumerate(FTIRs):
            if os.path.splitext(url.name)[-1] != '.txt':
                raise APIException("有FTIR文件不是txt格式，请检查。")
        result = []
        devPartSampleFTIR1 = devPartSampleFTIR.objects.get(id=int(devPartSampleFTIRId))

        for index, url in enumerate(FTIRs):
            devPartSampleId = devPartSampleFTIR1.devPartSample_id
            FTIR = devPartSampleFTIRTestFile.objects.create(txtURL=url,devPartSampleFTIR = devPartSampleFTIR1)
            result = preProcess('FTIR',devPartSampleFTIR1.id,FTIR.id,os.path.join(MEDIA_ROOT,str(FTIR.txtURL)))
            if result[0] == '0':
                FTIR.txtHandledURL = result[1]
                FTIR.save()
            else:
                raise APIException("预处理过程出错")
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
        else:
            return "该预处理过的文件已被删除，无法读取"
    def __str__(self):
        return self.txtURL

    class Meta:
        model = devPartSampleRamanTestFile
        fields = ("id","devPartSampleRaman","txtURL","handledData")
class LsitdevPartSampleRamanTestFileSerializer(serializers.Serializer):
    Ramans = serializers.ListField(
        child=serializers.FileField(max_length=100000, allow_empty_file=False, use_url=True),
        write_only=True )
    devPartSampleRaman = serializers.IntegerField(required=True, write_only=True)
    # 增添和更新都必须是多文件，且这个更新和其他更新不同，更新会覆盖，但新建不会覆盖，每次新建上传完都会进行取平均，替换平均文件
    def create(self, validated_data):
        Ramans = validated_data.get('Ramans')
        devPartSampleRamanId = validated_data.get('devPartSampleRaman')

        if len(Ramans) == 0:
            raise APIException("没有上传Raman文件，请上传")
        if devPartSampleRaman.objects.filter(id=int(devPartSampleRamanId)).count() != 1:
            raise APIException("填入的爆炸装置Raman序号不存在，请重新输入")
        for index, url in enumerate(Ramans):
            if os.path.splitext(url.name)[-1] != '.txt':
                raise APIException("有Raman文件不是txt格式，请检查。")

        result = []
        devPartSampleRaman1 = devPartSampleRaman.objects.get(id=int(devPartSampleRamanId))

        for index, url in enumerate(Ramans):
            devPartSampleId = devPartSampleRaman1.devPartSample_id
            Raman = devPartSampleRamanTestFile.objects.create(txtURL=url,devPartSampleRaman = devPartSampleRaman1)
            result = preProcess('RAMAN',devPartSampleRaman1.id,Raman.id,os.path.join(MEDIA_ROOT,str(Raman.txtURL)))
            if result[0] == '0':
                Raman.txtHandledURL = result[1]
                Raman.save()
            # 文件预处理，更新Raman匹配表和综合匹配表的结果
            else:
                raise APIException("预处理过程出错")

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
    devPartSampleRamanTestFile = devPartSampleRamanTestFileSerializer(many = True)
    # 自身的外键直接用serializer代替即可
    user = UserDetailSerializer()

    class Meta:
        model = devPartSampleRaman
        fields = ("id","devPartSample","devDetect","methodDetect", "user","inputDate","devPartSampleRamanTestFile")

class devPartSampleXRFTestFileSerializer(serializers.ModelSerializer):
    handledData = serializers.SerializerMethodField()

    def get_handledData(self, obj):
        path =obj.handledURL
        if os.path.exists(path) == True:
            data = np.load(path)
        # print(type(data))
        # print(data[0])

            return data
        else:
            return "该预处理过的文件已被删除，无法读取"
    def __str__(self):
        return self.excelURL

    class Meta:
        model = devPartSampleXRFTestFile
        fields =("id","devPartSampleXRF","excelURL","handledData")
class LsitdevPartSampleXRFTestFileSerializer(serializers.Serializer):
    XRFs = serializers.ListField(
        child=serializers.FileField(max_length=100000, allow_empty_file=False, use_url=True),
        write_only=True )

    devPartSampleXRF = serializers.IntegerField(required=True, write_only=True)
    # 增添和更新都必须是多文件，且这个更新和其他更新不同，更新会覆盖，但新建不会覆盖，每次新建上传完都会进行取平均，替换平均文件
    def create(self, validated_data):
        XRFs = validated_data.get('XRFs')
        devPartSampleXRFId = validated_data.get('devPartSampleXRF')

        # 差错检验
        if len(XRFs) == 0:
            raise APIException("没有上传XRF文件，请上传")
        if devPartSampleXRF.objects.filter(id=int(devPartSampleXRFId)).count() != 1:
            raise APIException("填入的爆炸装置XRF序号不存在，请重新输入")
        for index, url in enumerate(XRFs):
            if os.path.splitext(url.name)[-1] != '.xlsx':
                raise APIException("有XRF文件不是excel格式，请检查。")

        result = []
        devPartSampleXRF1 = devPartSampleXRF.objects.get(id=int(devPartSampleXRFId))

        for index, url in enumerate(XRFs):
            devPartSampleId = devPartSampleXRF1.devPartSample_id
            XRF = devPartSampleXRFTestFile.objects.create(excelURL=url,devPartSampleXRF = devPartSampleXRF1)
            result = preProcess('XRF', devPartSampleXRF1.id, XRF.id, os.path.join(MEDIA_ROOT, str(XRF.excelURL)))
            if result[0] == '0':
                XRF.handledURL = result[1]
                XRF.save()
            # 文件预处理，更新XRF匹配表和综合匹配表的结果
            # 样本库更新报告都得变
            else:
                raise APIException("预处理过程出错")

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
    featureUrl =serializers.FileField(read_only=True,)
    maskURL = serializers.ImageField(read_only=True, )
    nomUrl = serializers.FileField(read_only=True, )

    class Meta:
        model = devShapeSample
        fields = "__all__"

class devPartSampleDetailSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()
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