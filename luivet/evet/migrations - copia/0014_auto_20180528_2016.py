# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-28 20:16
from __future__ import unicode_literals

from django.db import migrations, models
from datetime import datetime

class Migration(migrations.Migration):

    dependencies = [
        ('evet', '0013_remove_historialtarjeta_nombre_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliente',
            name='documento_texto',
        ),
        migrations.RemoveField(
            model_name='mascota',
            name='diagnostico_texto',
        ),
        migrations.RemoveField(
            model_name='mascota',
            name='historial_texto',
        ),
        migrations.RemoveField(
            model_name='mascota',
            name='inscripcion_date',
        ),
        migrations.AddField(
            model_name='cliente',
            name='celular_texto',
            field=models.IntegerField(default=1, verbose_name='Celular'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cliente',
            name='codigopostal_texto',
            field=models.IntegerField(default=1, verbose_name='Codigo Postal'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cliente',
            name='tel_texto',
            field=models.IntegerField(default=1, verbose_name='Telefono'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historialtarjeta',
            name='circulatorio',
            field=models.CharField(choices=[('AZ', 'Azul'), ('RO', 'Rojo'), ('VE', 'Verde')], default=1, max_length=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historialtarjeta',
            name='frecuencia_respiratoria_texto',
            field=models.FloatField(default=1, verbose_name='Frecuencia Respiratoria'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historialtarjeta',
            name='linfonodulos_texto',
            field=models.CharField(default=1, max_length=50, verbose_name='Linfon\xf3dulos'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historialtarjeta',
            name='peso_texto',
            field=models.FloatField(default=1, verbose_name='Peso'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historialtarjeta',
            name='temperatura_texto',
            field=models.FloatField(default=1, verbose_name='Temperatura'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mascota',
            name='color_texto',
            field=models.CharField(default='negro', max_length=30, verbose_name='Color'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mascota',
            name='deceso_date',
            field=models.DateTimeField(default=datetime.now(), verbose_name='Deceso'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mascota',
            name='edad_texto',
            field=models.IntegerField(default=1, verbose_name='Edad'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mascota',
            name='raza_texto',
            field=models.CharField(default=1, max_length=30, verbose_name='Raza'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mascota',
            name='sexo_texto',
            field=models.CharField(default=1, max_length=10, verbose_name='Sexo'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='historialtarjeta',
            name='fecha_realizada',
            field=models.DateTimeField(verbose_name='Fecha y Hora'),
        ),
    ]
