from django.urls import path
from . import views

app_name = 'enquetes'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('detalhes/<int:pk>/', views.DetalhesView.as_view(), name='detalhes'),
    path('resultado/<int:pk>/', views.ResultadoView.as_view(), name='resultado'),
    path('votacao/<int:pk>/', views.VotacaoView.as_view(), name='votacao'),
]