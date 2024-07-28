from rest_framework import viewsets, status
from django.http import JsonResponse
from rest_framework.request import Request
from rest_framework.parsers import JSONParser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

from authentication.serializers import LoginSerializer, UserSerializer


# Create your views here.
class UserRegisterViewSet(viewsets.ViewSet):
    registerSerializer = UserSerializer

    def create(self, request: Request):
        data: dict = JSONParser().parse(request)
        serializer = self.registerSerializer(data=data)
        
        if serializer.is_valid():  
            serializer.save()
        return JsonResponse(serializer.data)
    

class UserLoginViewSet(viewsets.ViewSet):
    loginSerializer = LoginSerializer

    def create(self, request: Request):
        data: dict = JSONParser().parse(request)
        serializer = self.loginSerializer(data=data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = User.objects.filter(email = email).first()
            
            if user is None or not user.check_password(password):
                return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        
            refreshToken = RefreshToken.for_user(user=user)
            response = {
                "refresh_token": str(refreshToken),
                "access_token": str(refreshToken.access_token)
            }
            return JsonResponse(response)
        
        return JsonResponse(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    