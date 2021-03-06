# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2019-06-06 14:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('evet', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistroStock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(verbose_name='Fecha')),
                ('cantidad', models.IntegerField(verbose_name='Cantidad')),
                ('comentario', models.TextField(verbose_name='Comentario')),
            ],
        ),
        migrations.AddField(
            model_name='producto',
            name='stock',
            field=models.IntegerField(default=0, verbose_name='Stock'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='registrostock',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evet.Producto', verbose_name='Producto'),
        ),
    ]
