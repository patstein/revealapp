from django.urls import path

from .views import RegistrationView, ValidationView, GetUserInfo

urlpatterns = [
    path('', RegistrationView.as_view(), name='registration'),
    path('validation/', ValidationView.as_view(), name='registration_validation'),
    path('info/', GetUserInfo.as_view(), name='info')
]
