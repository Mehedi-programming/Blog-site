from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from . serializers import *
from . models import *
from . utils import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from axes.handlers.proxy import AxesProxyHandler
from axes.utils import reset
from rest_framework.decorators import api_view, permission_classes, authentication_classes
# from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


# Create your views here.
def Signup(request):
    serializer = SignupSerializer(data = request.data)
    if serializer.is_valid():
        User.objects.create_user(
            username=serializer.validated_data['username'],
            first_name=serializer.validated_data['first_name'],
            last_name=serializer.validated_data['last_name'],
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )
        return Response({"message":"User created successfully."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





        

