from django.urls import path
from . import views


urlpatterns = [
    path('Signup/', views.Signup, name='Signup'),
    path('Signin/', views.Signin, name='Signin'),
    path('change-password/', views.change_password, name='change_password'),

    
]

