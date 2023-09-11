import datetime
from django.db import models
from django.utils import timezone

class Pergunta(models.Model):
    texto = models.CharField(max_length = 150)
    data_pub = models.DateTimeField('Data de publicação')
    def __str__(self):
        return '({}) - {}'.format(self.id, self.texto)
    def foi_publicada_recentemente(self):
        agora = timezone.now()
        return agora-datetime.timedelta(days=1) <= self.data_pub <= agora
    foi_publicada_recentemente.admin_order_field = 'data_pub'
    foi_publicada_recentemente.boolean = True
    foi_publicada_recentemente.short_description = 'É Recente?'


class Alternativa(models.Model):
    texto = models.CharField(max_length = 80)
    quant_votos = models.IntegerField('Quantidade de votos', default = 0)
    pergunta = models.ForeignKey(Pergunta, on_delete = models.CASCADE)
    def __str__(self):
        return '({}) - {}'.format(self.id, self.texto)