# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-11 04:23
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evet', '0030_auto_20180611_0122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historialtarjeta',
            name='fecha_realizada',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 11, 1, 23, 33, 735101), verbose_name='Fecha y Hora'),
        ),
        migrations.AlterField(
            model_name='mascota',
            name='birthday_date',
            field=models.DateField(blank=True, default=datetime.datetime(2018, 6, 11, 1, 23, 33, 733736), null=True, verbose_name='Nacimiento'),
        ),
        migrations.AlterField(
            model_name='mascota',
            name='chip',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Chip'),
        ),
    ]
