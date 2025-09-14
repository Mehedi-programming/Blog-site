from django.urls import path
from . import views


urlpatterns = [
    path('Signup/', views.Signup, name='Signup'),
    path('Signin/', views.Signin, name='Signin'),
    path('change-password/', views.change_password, name='change_password'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('set-password/', views.set_password, name='set_password'),


    
]

