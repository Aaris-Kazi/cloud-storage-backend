from django.urls import include, path
from rest_framework import routers
from authentication.views import UserLoginViewSet, UserRegisterViewSet


router = routers.DefaultRouter()
router.register("register", UserRegisterViewSet, basename='register')
router.register("login", UserLoginViewSet, basename='login')

urlpatterns = [
    path('', include(router.urls)),
]
