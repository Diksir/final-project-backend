from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.models import AuthToken
from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate

from .serializers import RegisterSerializer, LoginSerializer

# Create your views here.
# Registration API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        if first_name and last_name:
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            
        _, token = AuthToken.objects.create(user)
        return Response({
            "user": RegisterSerializer(user, context=self.get_serializer_context()).data,
            "token": token
        })

# Login API
class LoginAPI(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        _, token = AuthToken.objects.create(user)
        return Response({
            "user": RegisterSerializer(user).data,
            "token": token
        })
