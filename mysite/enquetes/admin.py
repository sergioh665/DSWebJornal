from django.contrib import admin
from .models import Pergunta, Alternativa

admin.site.site_header = "Administração do Projeto DSWEB 2022.2"

class AlternativaInline(admin.TabularInline):
    model = Alternativa
    extra = 2

class PerguntaAdmin(admin.ModelAdmin):
    fieldsets = [
            ('Informações Gerais da Pergunta', {'fields': ['texto']}),
            ('Informações de Data', {'fields': ['data_pub']}),
        ]
    inlines = [AlternativaInline]
    list_display = ('texto', 'id', 'data_pub', 'foi_publicada_recentemente')
    list_filter = ['data_pub']
    search_fields = ['texto']

admin.site.register(Pergunta, PerguntaAdmin)
# admin.site.register(Alternativa)