from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed
import random, datetime
from django.utils import timezone
from django.contrib.auth.hashers import make_password

def get_tokens_for_user(user):
    if not user.is_active:
      raise AuthenticationFailed("User is not active")

    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def otp_generate()->str:
   return str(random.randint(1000,9999))

def otp_hash(otp:str)->str:
   return make_password(otp, hasher="argon2")

def expired_at(seconds=30):
   return timezone.now()+datetime.timedelta(seconds=seconds)