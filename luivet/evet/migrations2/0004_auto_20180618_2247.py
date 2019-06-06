# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-19 01:47
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evet', '0003_auto_20180618_2246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historialtarjeta',
            name='fecha_realizada',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 18, 22, 47, 1, 537268), verbose_name='Fecha y Hora'),
        ),
        migrations.AlterField(
            model_name='mascota',
            name='birthday_date',
            field=models.DateField(blank=True, default=datetime.datetime(2018, 6, 18, 22, 47, 1, 535407), null=True, verbose_name='Nacimiento'),
        ),
    ]
