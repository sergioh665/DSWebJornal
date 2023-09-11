from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Edicao, EdicaoForm, Noticia, Comentario, Usuario
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import login


'''testa o usuário conectado'''
def testar_usuario(user):
    if hasattr(user, 'usuario'):
        return True
    return False

class IndexView(View):
    def get(self, request, *args, **kwargs):
        edicoes = Edicao.objects.all()
        contexto = {'edicoes': edicoes}
        return render(request, 'jornal/index.html', contexto)

class EdicaoView(View):
    def get(self, request, *args, **kwargs):
        edicao = get_object_or_404(Edicao, pk = kwargs['pk'])
        testaUser = hasattr(request.user, 'usuario')
        contexto = {'edicao': edicao, 'testaUser': testaUser}
        return render(request, 'jornal/edicao.html', contexto)

@method_decorator(user_passes_test(testar_usuario), name='dispatch')
class NovaEdicaoView(View):
    def get(self, request, *args, **kwargs):
        form = EdicaoForm()
        return render(request, 'jornal/nova_edicao.html', {'form' : form})
    def post(self, request, *args, **kwargs):
        form = EdicaoForm(request.POST)
        if form.is_valid():
            nome = request.user.usuario
            autor = form.save(commit = False)
            autor.usuario = nome
            autor.save()
            return HttpResponseRedirect(reverse('jornal:index'))
        else:
            return render(request, 'jornal/nova_edicao.html', {'form' : form})

@method_decorator(user_passes_test(testar_usuario), name='dispatch')
class NovaNoticiaView(View):
    def post(self, request, *args, **kwargs):
        edicao = get_object_or_404(Edicao, pk = kwargs['pk'])
        texto = request.POST.get('texto')
        if texto:
            nome = request.user.usuario
            nova = Noticia(texto = texto, edicao = edicao, usuario=nome)
            nova.save()
            return HttpResponseRedirect(reverse('jornal:edicao', args=(edicao.id,)))
        else:
            contexto = {
                'edicao': edicao,
                'erro': '⚠️ Preencha o texto da notícia corretamente.'
            }
            return render(request, 'jornal/edicao.html', contexto)

@method_decorator(user_passes_test(testar_usuario), name='dispatch')
class AdicionarComentarioView(View):
    def post(self, request, *args, **kwargs):
        nota = get_object_or_404(Noticia, pk=kwargs['pk'])
        txt = request.POST['texto']
        if txt:
            usr = request.user.usuario
            comentario = Comentario(
                texto = txt, noticia = nota, usuario = usr
            )
            comentario.save()
            return HttpResponseRedirect(reverse(
                'jornal:edicao', args=(nota.edicao.id,)
            ))
        else:
            contexto = {
                'edicao': nota.edicao,
                'erro': '⚠️ Escreva um comentário válido.'
            }
            return render(request, 'jornal/edicao.html', contexto)

class CadastrarUsuarioView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'jornal/novo_usuario.html')
    def post(self, request, *args, **kwargs):
        user = request.POST.get('user')
        senha1 = request.POST.get('senha1')
        senha2 = request.POST.get('senha2')
        email = request.POST.get('email')
        nome = request.POST.get('nome')
        if user and senha1 and email and nome and senha1 == senha2:
            user = User.objects.create_user(user, email, senha1)
            usuario = Usuario(user=user, nome=nome)
            usuario.save()
            login(request, user)
            return HttpResponseRedirect(reverse('jornal:index'))
        else:
            contexto = {
                'erro': '⚠️ Preencha o cadastro corretamente.'
            }
            return render(request, 'jornal/novo_usuario.html', contexto)


class ApagarEdicaoView(View):
    def get(self, request, *args, **kwargs):
        edicao = get_object_or_404(Edicao, pk=kwargs['pk'])
        edicao.delete()
        return HttpResponseRedirect(reverse('jornal:index'))

class PesquisarView(View):
    def post(self, request, *args, **kwargs):
        pesquisa = request.POST.get('pesquisa')
        texto = request.POST.get('texto')
        if pesquisa and texto:
            if pesquisa == 'titulo':
                filtro = "“%s”" % texto
                retorno = Edicao.objects.filter(titulo__icontains = texto)
            else:
                filtro = "“%s”" % texto
                retorno = Edicao.objects.filter(termo__icontains = texto).distinct()
            contexto = {'edicoes': retorno, 'pesquisa': True, 'filtro': filtro}
            return render(request, 'jornal/index.html', contexto)
        else:
            return HttpResponseRedirect(reverse('jornal:index'))




