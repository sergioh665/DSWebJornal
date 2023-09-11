from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from .models import Pergunta, Alternativa

class IndexView(View):
    def get(self, request, *args, **kwargs):
        lista_enquetes = Pergunta.objects.filter(
            data_pub__lte = timezone.now()
        ).order_by('-data_pub')
        contexto = {'lista_enquetes': lista_enquetes}
        return render(request, 'enquetes/index.html', contexto)


class DetalhesView(View):
    def get(self, request, *args, **kwargs):
        pergunta = get_object_or_404(Pergunta, pk = kwargs['pk'])
        if pergunta.data_pub >= timezone.now():
            raise Http404('Nenhuma Enquete publicada com essa identificação')
        return render(
            request, 'enquetes/detalhes.html', {'pergunta': pergunta}
        )

class ResultadoView(View):
    def get(self, request, *args, **kwargs):
        pergunta = get_object_or_404(Pergunta, pk = kwargs['pk'])
        return render(
            request, 'enquetes/resultado.html', {'pergunta':pergunta}
        )

class VotacaoView(View):
    def post(self, request, *args, **kwargs):
        pergunta = get_object_or_404(Pergunta, pk = kwargs['pk'])
        try:
            alt_id = request.POST['alt']
            alternativa = pergunta.alternativa_set.get(pk = alt_id)

        except(KeyError, Alternativa.DoesNotExist):
            return render(request, 'enquetes/detalhes.html', {
                'pergunta': pergunta,
                'error': 'Selecione uma Alternativa válida!'
                })
        else:
            alternativa.quant_votos += 1
            alternativa.save()
            return HttpResponseRedirect(reverse(
                'enquetes:resultado', args=(pergunta.id, )
            ))




"""
--- view index
def index(request):
    lista_enquetes = Pergunta.objects.order_by('-data_pub')[:3]
    contexto = {'lista_enquetes': lista_enquetes}
    return render(request, 'enquetes/index.html', contexto)

class IndexView(generic.ListView):
    template_name = 'enquetes/index.html'
    context_object_name = 'lista_enquetes'
    def get_queryset(self):
        return Pergunta.objects.order_by('-data_pub')

--- view detalhes
def detalhes(request, enquete_id):
    pergunta = get_object_or_404(Pergunta, pk = enquete_id)
    return render(
        request, 'enquetes/detalhes.html', {'pergunta': pergunta}
    )

class DetalhesView(generic.DetailView):
    model = Pergunta
    template_name = 'enquetes/detalhes.html'
--- view resultado
def resultado(request, enquete_id):
    pergunta = get_object_or_404(Pergunta, pk=enquete_id)
    return render(
        request, 'enquetes/resultado.html', {'pergunta':pergunta}
    )
class ResultadoView(generic.DetailView):
    model = Pergunta
    template_name = 'enquetes/resultado.html'
"""