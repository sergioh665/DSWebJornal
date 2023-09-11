from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm

class Teste(models.Model):
    nome = models.CharField(max_length=50)
    data = models.DateTimeField(auto_now_add=True)

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, null = True)
    nome = models.CharField(max_length = 50)
    ultima_edicao = models.DateTimeField('Data da Ultima Edição', null=True)
    data_cadastro = models.DateTimeField('Data de Cadastro', auto_now_add=True, null=True)
    def __str__(self):
        return self.nome
    class Meta:
        ordering = ['nome']
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

class Edicao(models.Model):
    titulo = models.CharField(max_length = 200)
    termo = models.CharField(max_length = 50)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    data_postagem = models.DateField('Data da Postagem', auto_now_add=True, null=True)
    def __str__(self):
        return self.titulo
    class Meta:
        verbose_name = 'Edição'
        verbose_name_plural = 'Edições'

class EdicaoForm(ModelForm):
    class Meta:
        model = Edicao
        fields = ['titulo', 'termo']

class Noticia(models.Model):
    texto = models.CharField(max_length = 200)
    data_postagem = models.DateTimeField('Data da Postagem', auto_now_add=True, null=True)
    edicao = models.ForeignKey(Edicao, on_delete = models.CASCADE, null = True)
    usuario = models.ForeignKey(Usuario, on_delete = models.SET_NULL, null=True)
    def __str__(self):
        return self.texto
    class Meta:
        verbose_name = 'Notícia'
        verbose_name_plural = 'Notícias'

class Comentario(models.Model):
    texto = models.CharField(max_length = 1000)
    data_postagem = models.DateField('Data da Postagem', auto_now_add=True, null=True)
    noticia = models.ForeignKey(Noticia, on_delete = models.CASCADE, null = True)
    usuario = models.ForeignKey(Usuario, on_delete = models.SET_NULL, null=True)
    def __str__(self):
        return self.texto
    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'

