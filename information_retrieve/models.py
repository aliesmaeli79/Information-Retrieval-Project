from django.db import models

class FileUploadModel(models.Model):
    file_upload = models.FileField(upload_to='information_retrieve/document')