from django.urls import include, path
from rest_framework import routers
from .views import DirectoryViewSets, FileNetworkModelViewset, MediaStreamViewSet


router = routers.DefaultRouter()
router.register("directory", DirectoryViewSets, basename='directory')
router.register("file", FileNetworkModelViewset, basename='fileUploadDownload')
router.register(r"media", MediaStreamViewSet, basename='media')

urlpatterns = [
    path('', include(router.urls)),
]
