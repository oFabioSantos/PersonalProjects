"""Criando o padrão de Url's para o app users"""

from django.urls import path

#  Isso aqui importa as built in views funcions o Django para realizar a autenticação 
from django.contrib.auth import views as auth_views

from . import views

app_name='users'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name= 'users/login.html'), name='login'),  # Url, view com direcionamento do template tudo junto.
    path('logout/', views.logout_view, name='logout_view'),
    path('register/', views.register, name='register'),
]
