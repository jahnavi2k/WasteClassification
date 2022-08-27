from django.db import models
import os

def path_and_rename(instance, filename):
    upload_to = ''
    ext = filename.split('.')[-1]
    filename = "specimen." + ext
    # return the whole path to the file
    return os.path.join(upload_to, filename)


class File(models.Model):
  photo = models.ImageField(upload_to=path_and_rename)
  remark = models.CharField(max_length=20)
  timestamp = models.DateTimeField(auto_now_add=True)
