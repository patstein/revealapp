from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import RegistrationSerializer, ValidationSerializer, UserSerializer

User = get_user_model()


class RegistrationView(APIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request, **kwargs):
        serializer = self.serializer_class(data=request.user)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save(serializer.validated_data)
            return Response({'detail': f'Registration validation email sent to {user.email}!'})


class ValidationView(APIView):
    serializer_class = ValidationSerializer
    permission_classes = [AllowAny]

    def post(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'detail': 'Account Created!'})


class GetUserInfo(APIView):
    def get(self, request):
        return Response(UserSerializer(instance=request.user).data)
