from django.urls import re_path
from .views import FileView

urlpatterns = [
    re_path(r'^upload/$', FileView.as_view(), name='file-upload'),
]
