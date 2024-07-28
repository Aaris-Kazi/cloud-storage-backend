from django.urls import include, path
from rest_framework import routers
from .views import DirectoryViewSets, FileNetworkModelViewset


router = routers.DefaultRouter()
router.register("directory", DirectoryViewSets, basename='directory')
router.register("file", FileNetworkModelViewset, basename='fileUploadDownload')

urlpatterns = [
    path('', include(router.urls)),
]
