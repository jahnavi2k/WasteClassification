from rest_framework import serializers
from .models import Filee

class FileSerializer(serializers.ModelSerializer):
  class Meta():
    model = Filee
    fields = ('photo', 'remark', 'timestamp')
