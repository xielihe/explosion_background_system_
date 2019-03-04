"""bzxt117 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url,include
# from django.contrib import admin
from bzxt117.settings import MEDIA_ROOT
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token


from apps.basic.views import *
from apps.sample.views import *
from apps.evi.views import *
from apps.match.views import *
from apps.user_operation.views import *
from apps.match import views


router = DefaultRouter()

router.register(r'users', UserViewset, base_name="users")

router.register(r'methodDetects', methodDetectViewset, base_name="methodDetects")

router.register(r'devDetects', devDetectViewset, base_name="devDetects")

router.register(r'exploSamples', exploSampleViewset, base_name="exploSamples")
router.register(r'exploSampleFTIRs', exploSampleFTIRViewset, base_name="exploSampleFTIRs")
router.register(r'exploSampleFTIRTestFiles', exploSampleFTIRTestFileViewset, base_name="exploSampleFTIRTestFiles")
router.register(r'exploSampleRamans', exploSampleRamanViewset, base_name="exploSampleRamans")
router.register(r'exploSampleRamanTestFiles', exploSampleRamanTestFileViewset, base_name="exploSampleRamanTestFiles")
router.register(r'exploSampleXRDs', exploSampleXRDViewset, base_name="exploSampleXRDs")
router.register(r'exploSampleXRDTestFiles', exploSampleXRDTestFileViewset, base_name="exploSampleXRDTestFiles")
router.register(r'exploSampleXRFs', exploSampleXRFViewset, base_name="exploSampleXRFs")
router.register(r'exploSampleXRFTestFiles', exploSampleXRFTestFileViewset, base_name="exploSampleXRFTestFiles")
router.register(r'exploSampleGCMSs', exploSampleGCMSViewset, base_name="exploSampleGCMSs")
router.register(r'exploSampleGCMSFiles', exploSampleGCMSFileViewset, base_name="exploSampleGCMSFiles")
router.register(r'exploSampleGCMSTestFiles', exploSampleGCMSTestFileViewset, base_name="exploSampleGCMSTestFiles")
router.register(r'devSamples', devSampleViewset, base_name="devSamples")
router.register(r'devPartSamples', devPartSampleViewset, base_name="devPartSamples")
router.register(r'devPartSampleFTIRs', devPartSampleFTIRViewset, base_name="devPartSampleFTIRs")
router.register(r'devPartSampleFTIRTestFiles', devPartSampleFTIRTestFileViewset, base_name="devPartSampleFTIRTestFiles")
router.register(r'devPartSampleRamans', devPartSampleRamanViewset, base_name="devPartSampleRamans")
router.register(r'devPartSampleRamanTestFiles', devPartSampleRamanTestFileViewset, base_name="devPartSampleRamanTestFiles")
router.register(r'devPartSampleXRFs', devPartSampleXRFViewset, base_name="devPartSampleXRFs")
router.register(r'devPartSampleXRFTestFiles', devPartSampleXRFTestFileViewset, base_name="devPartSampleXRFTestFiles")

router.register(r'devShapeSamples', devShapeSampleViewset, base_name="devShapeSamples")

router.register(r'exploEvis', exploEviViewset, base_name="exploEvis")
router.register(r'exploEviFTIRs', exploEviFTIRViewset, base_name="exploEviFTIRs")
router.register(r'exploEviFTIRTestFiles', exploEviFTIRTestFileViewset, base_name="exploEviFTIRTestFileFiles")
router.register(r'exploEviRamans', exploEviRamanViewset, base_name="exploEviRamans")
router.register(r'exploEviRamanTestFiles', exploEviRamanTestFileViewset, base_name="exploEviRamanTestFiles")
router.register(r'exploEviXRDs', exploEviXRDViewset, base_name="exploEviXRDs")
router.register(r'exploEviXRDTestFiles', exploEviXRDTestFileViewset, base_name="exploEviXRDTestFiles")
router.register(r'exploEviXRFs', exploEviXRFViewset, base_name="exploEviXRFs")
router.register(r'exploEviXRFTestFiles', exploEviXRFTestFileViewset, base_name="exploEviXRFTestFiles")
router.register(r'exploEviGCMSs', exploEviGCMSViewset, base_name="exploEviGCMSs")
router.register(r'exploEviGCMSFiles', exploEviGCMSFileViewset, base_name="exploEviGCMSFiles")
router.register(r'exploEviGCMSTestFiles', exploEviGCMSTestFileViewset, base_name="exploEviGCMSTestFiles")
router.register(r'devEvis', devEviViewset, base_name="devEvis")
router.register(r'devEviFTIRs', devEviFTIRViewset, base_name="devEviFTIRs")
router.register(r'devEviFTIRTestFiles', devEviFTIRTestFileViewset, base_name="devEviFTIRTestFiles")
router.register(r'devEviRamans', devEviRamanViewset, base_name="devEviRamans")
router.register(r'devEviRamanTestFiles', devEviRamanTestFileViewset, base_name="devEviRamanTestFiles")
router.register(r'devEviXRFs', devEviXRFViewset, base_name="devEviXRFs")
router.register(r'devEviXRFTestFiles', devEviXRFTestFileViewset, base_name="devEviXRFTestFiles")

router.register(r'devShapeEvis', devShapeEviViewset, base_name="devShapeEvis")


router.register(r'exploMatchFTIRs', exploMatchFTIRViewset, base_name="exploMatchFTIRs")
router.register(r'exploMatchRamans', exploMatchRamanViewset, base_name="exploMatchRamans")
router.register(r'exploMatchXRDs', exploMatchXRDViewset, base_name="exploMatchXRDs")
router.register(r'exploMatchXRFs', exploMatchXRFViewset, base_name="exploMatchXRFs")
router.register(r'exploMatchGCMSs', exploMatchGCMSViewset, base_name="exploMatchGCMSs")
router.register(r'exploSynMatchs', exploSynMatchViewset, base_name="exploSynMatchs")

router.register(r'exploReportMatchs', exploReportMatchViewset, base_name="exploReportMatchs")

router.register(r'devMatchFTIRs', devMatchFTIRViewset, base_name="devMatchFTIRs")
router.register(r'devMatchRamans', devMatchRamanViewset, base_name="devMatchRamans")
router.register(r'devMatchXRFs', devMatchXRFViewset, base_name="devMatchXRFs")
router.register(r'devCompMatchs', devCompMatchViewset, base_name="devCompMatchs")
router.register(r'devShapeMatchs', devShapeMatchViewset, base_name="devShapeMatchs")
router.register(r'devShapeMultiMatchs', devShapeMultiMatchViewset, base_name="devShapeMultiMatchs")

router.register(r'devSynMatchs', devSynMatchViewset, base_name="devSynMatchs")

router.register(r'userMessages', userMessageViewset, base_name="userMessages")
router.register(r'userMessageFilees', userMessageFileViewset, base_name="userMessageFiles")

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
     url(r'^media/(?P<path>.*)$',  serve, {"document_root":MEDIA_ROOT}),
     url(r'^', include(router.urls)),
     url(r'docs/', include_docs_urls(title="爆炸系统")),
     url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
     url(r'^login/', obtain_jwt_token),
     # 用POST方法请求这个接口，其中包含type和eviId的参数，若成功返回201_created的响应。
     # type对应的法则如下
     # 1：exploMatchFTIR，2：exploMatchRaman，3：exploMatchXRD，4：exploMatchXRF，5：exploMatchGCMS，
     # 6：devMatchFTIR，7:devMatchRaman,8:devMatchXRF,9:PCBImgMatch,10:oPartImgMatch,11:logoImgMatch
     # 12:devShapeMatch
     url(r'^startMatch/',startMatch.as_view(), name='startMatch'),
     url(r'^nomPicture/', nomPicture.as_view(), name='nomPicture'),
     url(r'^createDevReport/', createDevReport.as_view(), name='createDevReport'),
     url(r'^createExploReport/', createExploReport.as_view(), name='createExploReport'),
     url(r'^messageUpdate/',messageUpdate.as_view(),name='messageUpdate'),
     # 用POST方法请求这个接口，其中包含type和id的参数，id为exploSampleFTIR等级别的id，若成功返回201_created的响应。
     # type对应的法则如下
     # 1：exploSampleFTIR，2：exploSampleRaman，3：exploSampleXRD，4：exploSampleXRF，5：exploSampleGCMS，
     # 6：devPartSampleFTIR，7:devPartSampleRaman,8:devPartSampleXRF
     # 用POST方法请求这个接口，其中包含type和id的参数，id为exploEviFTIR等级别的id，若成功返回201_created的响应。
     # type对应的法则如下
     # 1：exploEviFTIR，2：exploEviRaman，3：exploEviXRD，4：exploEviXRF，5：exploEviGCMS，
     # 6：devEviFTIR，7:devEviRaman,8:devEviXRF
     url(r'^wordSelect/',wordSelect.as_view(), name='wordSelect'),
     url(r'^api-token-auth/', obtain_jwt_token),

]
