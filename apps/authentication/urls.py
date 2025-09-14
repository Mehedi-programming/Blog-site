from django.urls import path
from . import views


urlpatterns = [
    path('Signup/', views.Signup, name='Signup'),
    path('Signin/', views.Signin, name='Signin'),
    
]

