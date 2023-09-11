import datetime
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Pergunta

def cria_pergunta(texto, dias):
    """
    cria um objeto Pergunta com: um texto e um delta de dias positivo ou negativo
    """
    data = timezone.now() + datetime.timedelta(days = dias)
    return Pergunta.objects.create(texto = texto, data_pub = data)

class DetalhesViewTest(TestCase):
    def test_com_pergunta_no_futuro(self):
        """
        quando a pergunta tiver data no futuro deve retornar um 404
        """
        p1 = cria_pergunta(texto = 'Pergunta futuro', dias = 1)
        resposta = self.client.get(
            reverse('enquetes:detalhes', args=(p1.id,))
            )
        self.assertEqual(resposta.status_code, 404)

    def test_com_pergunta_no_passado(self):
        """
        DEVE exibir normalmente perguntas com data no passado
        """
        p1 = cria_pergunta(texto = 'Pergunta 1', dias = -1)
        resposta = self.client.get(
            reverse('enquetes:detalhes', args=(p1.id,))
            )
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, p1.texto)
        self.assertEqual(
            resposta.context['pergunta'], p1
        )

class IndexViewTest(TestCase):
    def test_sem_perguntas_cadastradas(self):
        """
        DEVE ser exibida uma mensagem indicando que nao há enquete cadastradas
        """
        resposta = self.client.get(reverse('enquetes:index'))
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, 'Não existem enquetes cadastradas até o momento.')
        self.assertQuerysetEqual(resposta.context['lista_enquetes'], [])

    def test_com_pergunta_no_passado(self):
        """
        deve exibir normalmente perguntas com data no passado
        """
        cria_pergunta(texto = 'Pergunta 1', dias = -1)
        resposta = self.client.get(reverse('enquetes:index'))
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, 'Pergunta 1')
        self.assertQuerysetEqual(
            resposta.context['lista_enquetes'], ['<Pergunta: (1) - Pergunta 1>']
        )

    def test_com_pergunta_no_futuro(self):
        """
        NÂO PODE exibir perguntas com data no futuro
        """
        cria_pergunta(texto = 'Pergunta futuro', dias = 1)
        resposta = self.client.get(reverse('enquetes:index'))
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, 'Não existem enquetes cadastradas até o momento.')
        self.assertQuerysetEqual(
            resposta.context['lista_enquetes'], []
        )

    def test_com_pergunta_no_futuro_e_outra_no_futuro(self):
        """
        DEVE exibir perguntas com data no futuro
        """
        cria_pergunta(texto = 'Pergunta no futuro', dias = 1)
        cria_pergunta(texto = 'Pergunta no passado', dias = -1)
        resposta = self.client.get(reverse('enquetes:index'))
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, 'Pergunta no passado')
        self.assertQuerysetEqual(
            resposta.context['lista_enquetes'],
            ['<Pergunta: (2) - Pergunta no passado>']
        )

    def test_duas_perguntas_no_passado(self):
        """
        DEVE exibi-las ordenadas decrescentemente por data de publicacao
        """
        cria_pergunta(texto = 'Pergunta no passado 1', dias = -30)
        cria_pergunta(texto = 'Pergunta no passado 2', dias = -5)
        resposta = self.client.get(reverse('enquetes:index'))
        self.assertEqual(resposta.status_code, 200)
        self.assertQuerysetEqual(
            resposta.context['lista_enquetes'],
            ['<Pergunta: (2) - Pergunta no passado 2>',
            '<Pergunta: (1) - Pergunta no passado 1>']
        )

class PerguntaModelTest(TestCase):
    def test_pergunta_recentemente_com_pergunta_no_futuro(self):
        """
        Foi publicada_recentemente() DEVE retornar FALSE para pergunta no futuro
        """
        data = timezone.now() + datetime.timedelta(days=1)
        obj_pergunta = Pergunta(data_pub = data)
        self.assertIs(obj_pergunta.foi_publicada_recentemente(), False)

    def test_publicada_recentemente_com_pergunta_no_passado(self):
        """
        Foi publicada_recentemente() DEVE retornar FALSE para datas anteriores
        às últimas 24hrs.
        """
        data = timezone.now() - datetime.timedelta(days=1, seconds=1)
        obj_pergunta = Pergunta(data_pub = data)
        self.assertIs(obj_pergunta.foi_publicada_recentemente(), False)

    def test_publicada_recentemente_com_pergunta_nas_ultimas_24hrs(self):
        """
        Foi publicada_recentemente() DEVE retornar TRUE para datas dentro
        do intervalo das últimas 24hrs
        """
        data = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        obj_pergunta = Pergunta(data_pub = data)
        self.assertIs(obj_pergunta.foi_publicada_recentemente(), True)

    def test_publicada_recentemente_agora(self):
        """
        Foi publicada_recentemente() DEVE retornar TRUE para datas em exatos 24hrs
        """
        data = timezone.now()
        obj_pergunta = Pergunta(data_pub = data)
        self.assertIs(obj_pergunta.foi_publicada_recentemente(), True)
