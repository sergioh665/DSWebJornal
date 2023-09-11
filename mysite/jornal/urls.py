from django.urls import path
from . import views

app_name = 'jornal'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('edicao/<int:pk>/', views.EdicaoView.as_view(), name = 'edicao'),
    path('edicao/adicionar/', views.NovaEdicaoView.as_view(), name = 'add_edicao'),
    path('edicao/<int:pk>/noticiar/', views.NovaNoticiaView.as_view(), name = 'add_nota'),
    path('noticia/<int:pk>/comentar/', views.AdicionarComentarioView.as_view(), name = 'add_coment'),
    path('edicao/<int:pk>/apagar/',views.ApagarEdicaoView.as_view(), name='remove_edicao'),
    path('edicao/pesquisar/', views.PesquisarView.as_view(), name='pesquisar'),
    path('usuario/adicionar/',views.CadastrarUsuarioView.as_view(), name='add_usuario'),
]

'''path('edicao/<int:pk>/comentar', views.AdicionarComentarioView.as_view(), name = 'add_coment'),
   path('usuario/cadastro/', views.CadastrarUsuarioView.as_view(), name = 'new_user'),'''