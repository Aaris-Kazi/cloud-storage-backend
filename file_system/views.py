
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from django.http import JsonResponse, QueryDict
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from django.contrib.auth.models import User
from .models import MyStorageModel
from django.http import FileResponse

from file_system.serializers import  MyStorageSerializers
from utils.CreateDirectory import createDirectory, deleteFile, listDirectory, deleteDirectory
from utils.GetAuthUser import GetUser

# Create your views here.

super_path = "storage/"
class DirectoryViewSets(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]

    def create(self, request: Request):
        try:
            user_id = GetUser(request)
            user = User.objects.get(pk = user_id)
            path = request.data.get("directory", "")
            if path == "":
                path = super_path + user.username
                createDirectory(path)
            else:
                path = super_path + user.username +"/"+ path
                createDirectory(path, True)
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        
        return JsonResponse({"status": "success"})
    
    permission_classes = [IsAuthenticated]
    def delete(self, request: Request):
        try:
            user_id = GetUser(request)
            user = User.objects.get(pk = user_id)
            path = request.data.get("directory", "")
            if path == "":
                path = super_path + user.username
                deleteDirectory(path)
            else:
                path = super_path + user.username +"/"+ path
                deleteDirectory(path, True)
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        
        return JsonResponse({"status": "success"})


    def list(self, request: Request):
        try:
            user_id = GetUser(request)
            user = User.objects.get(pk = user_id)
            path = super_path + user.username
            directories:list = listDirectory(path)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        
        return JsonResponse({"direcotries": directories})


    def retrieve(self, request: Request, pk = None):
        user_id = GetUser(request)
        user = User.objects.get(pk = user_id)
        path = super_path + user.username +"/"+ pk
        directories:list = listDirectory(path)
            
        return JsonResponse({"direcotries": directories})
    

class FileNetworkModelViewset(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]
    serializer = MyStorageSerializers
    storageModel = MyStorageModel
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request: Request):
        user_id = GetUser(request)
        data: QueryDict = request.data
        data._mutable = True
        data.update({"user_id": int(user_id)})
        serializer = self.serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"status": "success"})
        else:
            return JsonResponse(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request):
        user_id = GetUser(request)
        data: QueryDict = request.data
        data._mutable = True
        data.update({"user_id": int(user_id)})
        name :str = data.get("name")
        folder :str = data.get("folder")
        user = User.objects.get(pk = user_id)
        path = f"{super_path}{user.username}/{folder}/{name}"
        instance = get_object_or_404(MyStorageModel, user_id = user_id, name = name)
        instance.delete()
        deleteFile(path)
        
        return JsonResponse({"status": "success"})
        
    
    def list(self, request: Request):
        
        user_id = GetUser(request)
        file = request.query_params.get("file")
        folder = request.query_params.get("folder")

        username = User.objects.get(pk = int(user_id))
        path = super_path + username.username +"/"+ folder +"/"+ file
        try:
            FilePointer = open(path, mode="rb")
            response = FileResponse(FilePointer, filename= FilePointer.name, as_attachment=True)
            response['Content-Disposition'] = f'attachment; filename="{file}"'
    
            return response
        except Exception as e:
            return JsonResponse({'msg': str(e)}, status=status.HTTP_404_NOT_FOUND)