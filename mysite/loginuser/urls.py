from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

app_name = 'loginuser'
urlpatterns = [
    path('sair/', auth_views.LogoutView.as_view(), name='logout'),
    path('entrar/', views.LoginView.as_view(), name='login'),
]