# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-04 18:58
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evet', '0018_auto_20180604_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historialtarjeta',
            name='fecha_realizada',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 4, 15, 58, 45, 994077), verbose_name='Fecha y Hora'),
        ),
        migrations.AlterField(
            model_name='mascota',
            name='birthday_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2018, 6, 4, 15, 58, 45, 993223), null=True, verbose_name='Cumple'),
        ),
    ]