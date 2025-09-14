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


# Signin
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def Signin(request):
    serializer = SigninSerializser(data=request.data)
    if serializer.is_valid():
        username =serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(User, username=username, password=password)
        credentials = {"username":username}
        
        if AxesProxyHandler.is_locked(request,credentials):
            return Response({"message":"Your account is locked for 20 minutes."}, status=status.HTTP_403_FORBIDDEN)
        if user:
            reset(username=username)
            token = get_tokens_for_user(user)
            return Response({"access_token":token['access'], "refresh_token":token['refresh']}, status=status.HTTP_201_CREATED)
        return Response ({"message":"Inavalid username or pasword."}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# change password
@api_view(['POST'])
def change_password(request):
    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_passwoed']
        user = User.objects.get(id=request.user.id)

        if not user.check_password(old_password):
            return Response ({"message":"Your password is not correct."}, status=status.HTTP_400_BAD_REQUEST)
        if old_password == new_password:
            return Response({"message":"New password cannot be same as old passsword."}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()
        reset(username=user.username)
        RefreshToken.for_user(user)
        return Response({"message":"Password changed successfully."}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




        

