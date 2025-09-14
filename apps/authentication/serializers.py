from . models import *
from rest_framework import serializers
from django.contrib.auth.models import User


class SignupSerializer(serializers.Serializer):
    class Meta:
        models = User
        fields =['username','first_name','last_name','email','password']


class SigninSerializser(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)


class ResetpasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class VerifyOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=4)


class SetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)



