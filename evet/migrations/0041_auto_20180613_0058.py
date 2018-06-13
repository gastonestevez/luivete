# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-13 03:58
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evet', '0040_auto_20180613_0023'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='historialtarjeta',
            options={'verbose_name': 'Visita', 'verbose_name_plural': 'Visitas'},
        ),
        migrations.AddField(
            model_name='producto',
            name='proxima_aplicacion',
            field=models.DateField(blank=True, null=True, verbose_name='Proxima aplicaci\xf3n'),
        ),
        migrations.AlterField(
            model_name='historialtarjeta',
            name='fecha_realizada',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 13, 0, 58, 24, 365499), verbose_name='Fecha y Hora'),
        ),
        migrations.AlterField(
            model_name='mascota',
            name='birthday_date',
            field=models.DateField(blank=True, default=datetime.datetime(2018, 6, 13, 0, 58, 24, 363098), null=True, verbose_name='Nacimiento'),
        ),
    ]
