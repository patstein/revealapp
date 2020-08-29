from django.urls import path
from project.apps.upload.views import FileView, GetPdfs, GetAllPdfs

urlpatterns = [
    path('upload/', FileView.as_view(), name='storing_file'),
    path('get/', GetPdfs.as_view(), name='storing_file'),
    path('get/all/', GetAllPdfs.as_view(), name='storing_file'),

]
