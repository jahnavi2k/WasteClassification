from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileSerializer
from django.http import FileResponse
from trashAlwaysCan import findTrash
import os

class FileView(APIView):
  parser_classes = (MultiPartParser, FormParser)
  #permission_classes = (permissions.AllowAny,) 
  def post(self, request, *args, **kwargs):
    file_serializer = FileSerializer(data=request.data)
    if file_serializer.is_valid():
      file_serializer.save()
      findTrash.predict_result('specimen.jpg')
      response = FileResponse(open(os.path.join(os.getcwd(), 'annotated.jpg'), 'rb'))
      return response
      #return Response(file_serializer.data, status=status.HTTP_201_CREATED)
    else:
      return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
