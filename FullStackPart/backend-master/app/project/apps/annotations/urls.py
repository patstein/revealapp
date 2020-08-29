from django.urls import path

from project.apps.annotations.views import AnnotateText

urlpatterns = [
    path('', AnnotateText.as_view(), name='annotated-text'),
]
