from django.db import models
from django.contrib.auth.models import User

# Create your models here.
super_path = "storage/"
def user_directory_path(instance, filename):
    return f'{super_path}{instance.user_id}/{instance.folder}/{filename}'


class MyStorageModel(models.Model):

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False)
    folder = models.CharField(max_length=200, blank=True)
    file = models.FileField(upload_to=user_directory_path)
    

    def __str__(self):
        return self.name
