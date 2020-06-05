# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-21 22:47
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evet', '0047_auto_20180620_1829'),
    ]

    operations = [
        migrations.AddField(
            model_name='historialtarjeta',
            name='atendido_por',
            field=models.TextField(blank=True, max_length=30, null=True, verbose_name='Atendido por'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='celular_texto',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='Celular'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='codigopostal_texto',
            field=models.IntegerField(blank=True, null=True, verbose_name='Codigo Postal'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='inscripcion_date',
            field=models.DateField(default=datetime.datetime(2018, 6, 21, 19, 47, 46, 860843), verbose_name='Fecha de inscripcion'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='mail_texto',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='tel_texto',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='Telefono'),
        ),
        migrations.AlterField(
            model_name='historialtarjeta',
            name='auscultacion_ritmo_text',
            field=models.CharField(blank=True, choices=[('Normal', 'Normal'), ('Arritmico', 'Arritmico')], max_length=20, null=True, verbose_name='Auscultacion Ritmo'),
        ),
        migrations.AlterField(
            model_name='historialtarjeta',
            name='auscultacion_sonidos_text',
            field=models.CharField(blank=True, choices=[('Normal', 'Normal'), ('Disminuido', 'Disminuido'), ('Aumentado', 'Aumentado')], max_length=20, null=True, verbose_name='Auscultacion Sonidos'),
        ),
        migrations.AlterField(
            model_name='historialtarjeta',
            name='auscultacion_text',
            field=models.CharField(blank=True, choices=[('Bradicardia', 'Bradicardia'), ('Normal', 'Normal'), ('Taquicardia', 'Taquicardia')], max_length=20, null=True, verbose_name='Auscultacion'),
        ),
        migrations.AlterField(
            model_name='historialtarjeta',
            name='fecha_realizada',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 21, 19, 47, 46, 865945), verbose_name='Fecha y Hora'),
        ),
        migrations.AlterField(
            model_name='historialtarjeta',
            name='frecuencia_cardiaca',
            field=models.IntegerField(blank=True, null=True, verbose_name='Frecuencia Cardiaca'),
        ),
        migrations.AlterField(
            model_name='historialtarjeta',
            name='frecuencia_respiratoria_texto',
            field=models.FloatField(blank=True, null=True, verbose_name='Frecuencia Respiratoria'),
        ),
        migrations.AlterField(
            model_name='historialtarjeta',
            name='linfonodulos_texto',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='LFN'),
        ),
        migrations.AlterField(
            model_name='historialtarjeta',
            name='peso_texto',
            field=models.FloatField(blank=True, null=True, verbose_name='Peso'),
        ),
        migrations.AlterField(
            model_name='historialtarjeta',
            name='soplo_text',
            field=models.CharField(blank=True, choices=[('No detectado', 'No detectado'), ('1/6', '1/6'), ('2/6', '2/6'), ('3/6', '3/6'), ('4/6', '4/6'), ('5/6', '5/6'), ('6/6', '6/6')], max_length=20, null=True, verbose_name='Dimension'),
        ),
        migrations.AlterField(
            model_name='historialtarjeta',
            name='temperatura_texto',
            field=models.FloatField(blank=True, null=True, verbose_name='Temperatura'),
        ),
        migrations.AlterField(
            model_name='mascota',
            name='birthday_date',
            field=models.DateField(blank=True, default=datetime.datetime(2018, 6, 21, 19, 47, 46, 862502), null=True, verbose_name='Nacimiento'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='referencia',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='ID de Referencia'),
        ),
    ]