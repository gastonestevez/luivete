# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-15 20:09
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evet', '0042_auto_20180615_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historialtarjeta',
            name='aplicacion_text',
            field=models.ManyToManyField(blank=True, null=True, to='evet.Producto', verbose_name='Aplicaciones'),
        ),
        migrations.AlterField(
            model_name='historialtarjeta',
            name='fecha_realizada',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 15, 17, 9, 56, 107658), verbose_name='Fecha y Hora'),
        ),
        migrations.AlterField(
            model_name='mascota',
            name='birthday_date',
            field=models.DateField(blank=True, default=datetime.datetime(2018, 6, 15, 17, 9, 56, 103302), null=True, verbose_name='Nacimiento'),
        ),
        migrations.RemoveField(
            model_name='producto',
            name='proxima_aplicacion'
        )
        migrations.AddField(
            model_name='producto',
            name='proxima_aplicacion',
            field=models.IntegerField(blank=True, null=True, verbose_name='Proxima aplicaci\xf3n en dias'),
        ),
    ]
