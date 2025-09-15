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
def signup(request):
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
def signin(request):
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
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
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


# reset password
@api_view(['POST'])
def reset_password(request):
    serializer = ResetpasswordSerializer(data=request.data)
    if serializer.is_valid():
        email =serializer.validated_data['email']
        user = get_object_or_404(User, email=email) 
        if user:
            otp = otp_generate()
            hashed = otp_hash(otp)
            Otp.objects.create(
                user=user,
                hash_otp=hashed,
                expired_at= expired_at(),
                is_used=False
            )
            print(f"Your OTP is {otp}")
            return Response({"message":"Your OTP generated successfully."}, status=status.HTTP_200_OK)
        return Response({"message":"Your email does not exists"}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# verify otp
@api_view(['POST'])
def verify_otp(request):
    serializer = VerifyOtpSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']
        try:
            user = User.objects.get(email=email)
            otp_obj= Otp.objects.get(user, is_used=False)
        except Exception as e:
            return Response({"message":"Invalid email or otp"}, status=status.HTTP_400_BAD_REQUEST)

        if otp_obj.expired_at < timezone.now():
            return Response({"message":"Your otp is expired."}, status=status.HTTP_400_BAD_REQUEST)

        if otp_obj.hash_otp !=otp_hash(otp):
            return Response({"message":"Your otp is not valid."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message":"Otp verified."}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# set password
@api_view(['POST'])
def set_password(request):
    serializer = SetPasswordSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['passsword']
        try:
            user = User.objects.get(email=email)
            otp_obj = Otp.objects.get(user=user, is_used=False)
        except Exception as e:
            return Response({"message":"Invalid email or otp"}, status=status.HTTP_400_BAD_REQUEST) 

        if otp_obj.expired_at <timezone.now():
            return Response({"message":"Your otp is expired."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(password)
        user.save()
        otp_obj.is_used = True       
        reset(username=user.username)
        RefreshToken.for_user(user)
        return Response({"message":"Password set successfully."}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




        

