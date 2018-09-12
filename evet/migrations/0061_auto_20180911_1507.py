# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-11 18:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evet', '0060_auto_20180808_1402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turno',
            name='razon',
            field=models.CharField(choices=[('Observacion', 'Observacion'), ('Vacuna', 'Vacuna'), ('Peluqueria', 'Peluqueria'), ('Cirug\xeda', 'Cirug\xeda'), ('Consulta', 'Consulta'), ('Especialidad', 'Especialidad'), ('Ecografia/Rayos', 'Ecografia/Rayos')], default='Observacion', max_length=30, verbose_name='Razon'),
        ),
    ]