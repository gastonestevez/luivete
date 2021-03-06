# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-05 22:52
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evet', '0023_auto_20180605_1921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='celular_texto',
            field=models.CharField(max_length=40, verbose_name='Celular'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='tel_texto',
            field=models.CharField(max_length=40, verbose_name='Telefono'),
        ),
        migrations.AlterField(
            model_name='historialtarjeta',
            name='fecha_realizada',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 5, 19, 52, 2, 472420), verbose_name='Fecha y Hora'),
        ),
        migrations.AlterField(
            model_name='mascota',
            name='birthday_date',
            field=models.DateField(blank=True, default=datetime.datetime(2018, 6, 5, 19, 52, 2, 470130), null=True, verbose_name='Cumple'),
        ),
    ]
