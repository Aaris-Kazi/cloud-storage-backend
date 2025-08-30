
import mimetypes
import os
from wsgiref.util import FileWrapper
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from django.http import Http404, JsonResponse, QueryDict, StreamingHttpResponse
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from django.contrib.auth.models import User

from cloud_drive import settings
from .models import MyStorageModel
from django.http import FileResponse

from file_system.serializers import  MyStorageSerializers
from utils.CreateDirectory import createDirectory, deleteFile, deleteDirectory, listDirectoryV2
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
            print(user_id)
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

            dir = request.query_params.get("directory", "")
            if dir != "":
                dir = "/" + dir
            path = super_path + user.username + dir
            directories:dict = listDirectoryV2(path)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        
        return JsonResponse({"direcotries": directories})


    def retrieve(self, request: Request, pk = None):
        user_id = GetUser(request)
        user = User.objects.get(pk = user_id)
        path = super_path + user.username +"/"+ pk
        directories:dict = listDirectoryV2(path)
            
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
        instance = get_object_or_404(MyStorageModel, user_id = user_id, name = name, file = path)
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


class MediaStreamViewSet(viewsets.ViewSet):

    """
    Stream audio/video files with HTTP range support (for seeking and buffering).
    Supports any media file under MEDIA_ROOT/aaris_kazi/{videos|music}/
    """
    permission_classes = [IsAuthenticated]

    def list(self, request: Request, pk = None):
        media_type:str = request.query_params.get("media_type")
        filename:str = request.query_params.get("filename")

        if not media_type or not filename:
            return JsonResponse({"status": "Missing media_type or filename"})

        user_id = GetUser(request)

        username:str = User.objects.get(pk = int(user_id))
        file_path = os.path.join(settings.MEDIA_ROOT, "storage", str(username), media_type, filename)
        
        if not os.path.exists(file_path):
            raise Http404("Media file not found.")
        
        get_object_or_404(MyStorageModel, user_id = user_id, name = filename)
        
        file_size = os.path.getsize(file_path)
        content_type, _ = mimetypes.guess_type(file_path)
        content_type = content_type or "application/octet-stream"

        
        range_header = request.headers.get("Range", "").strip()

        if range_header:
            try:
                range_value = range_header.split("=")[-1]
                start_str, end_str = range_value.split("-")
                start = int(start_str)
                end = int(end_str) if end_str else file_size - 1
            except:
                start, end = 0, file_size - 1

            length = end - start + 1
            with open(file_path, "rb") as f:
                f.seek(start)
                data = f.read(length)

            response = StreamingHttpResponse(data, status=206, content_type=content_type)
            response["Content-Range"] = f"bytes {start}-{end}/{file_size}"
            response["Content-Length"] = str(length)
        else:
            response = StreamingHttpResponse(open(file_path, "rb"), content_type=content_type)
            response["Content-Length"] = str(file_size)

        response["Accept-Ranges"] = "bytes"
        return response
        
