from rest_framework import serializers
from .models import MyStorageModel


class MyStorageSerializers(serializers.ModelSerializer):
    class Meta:
        model = MyStorageModel
        fields = ['user_id', 'name', 'folder', 'file']