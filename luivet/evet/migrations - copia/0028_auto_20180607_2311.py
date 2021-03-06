# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-08 02:11
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evet', '0027_auto_20180607_2306'),
    ]

    operations = [
        migrations.AddField(
            model_name='mascota',
            name='medicado_observacion',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Observacion'),
        ),
        migrations.AlterField(
            model_name='historialtarjeta',
            name='fecha_realizada',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 7, 23, 11, 4, 917791), verbose_name='Fecha y Hora'),
        ),
        migrations.AlterField(
            model_name='mascota',
            name='alimentacion',
            field=models.CharField(choices=[('Balanceado', 'Balanceado'), ('Casero', 'Casero'), ('Medicado', 'Medicado')], default='Balanceado', max_length=15, verbose_name='Alimentacion'),
        ),
        migrations.AlterField(
            model_name='mascota',
            name='birthday_date',
            field=models.DateField(blank=True, default=datetime.datetime(2018, 6, 7, 23, 11, 4, 915763), null=True, verbose_name='Nacimiento'),
        ),
    ]
