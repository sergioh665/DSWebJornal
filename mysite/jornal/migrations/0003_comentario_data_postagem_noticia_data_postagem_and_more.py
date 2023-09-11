# Generated by Django 4.0.6 on 2023-02-09 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jornal', '0002_edicao_data_postagem'),
    ]

    operations = [
        migrations.AddField(
            model_name='comentario',
            name='data_postagem',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='Data da Postagem'),
        ),
        migrations.AddField(
            model_name='noticia',
            name='data_postagem',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Data da Postagem'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='data_cadastro',
            field=models.DateTimeField(null=True, verbose_name='Data de Cadastro'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='ultima_edicao',
            field=models.DateTimeField(null=True, verbose_name='Data da Ultima Edição'),
        ),
    ]
