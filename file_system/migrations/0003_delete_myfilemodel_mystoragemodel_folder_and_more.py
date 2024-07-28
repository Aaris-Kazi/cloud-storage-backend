# Generated by Django 5.0.7 on 2024-07-28 11:47

import file_system.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_system', '0002_mystoragemodel'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MyFileModel',
        ),
        migrations.AddField(
            model_name='mystoragemodel',
            name='folder',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='mystoragemodel',
            name='file',
            field=models.FileField(upload_to=file_system.models.user_directory_path),
        ),
    ]
