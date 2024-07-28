from django.contrib import admin
from . import models
# Register your models here.

@admin.register(models.MyStorageModel)
class MyStorageAdmin(admin.ModelAdmin):
    list_display = [
        "user_id",
        "name",
        "folder",
        "file"
    ]
    search_fields = [
        "user_id",
        "name",
        "file"
    ]
    
    ordering =['id']