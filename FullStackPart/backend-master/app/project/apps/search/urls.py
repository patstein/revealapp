from django.urls import path
from .views import SearchText

urlpatterns = [
    path('query/', SearchText.as_view(), name='search'),
]
