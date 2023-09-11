from django.contrib import admin
from .models import Usuario, Edicao, Noticia, Comentario

admin.site.register(Usuario)
admin.site.register(Edicao)
admin.site.register(Noticia)
admin.site.register(Comentario)