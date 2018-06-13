# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-13 02:48
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('evet', '0037_auto_20180612_2342'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historialtarjeta',
            name='aplicacion_text',
        ),
        migrations.AddField(
            model_name='historialtarjeta',
            name='aplicacion_text',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='evet.Producto'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='historialtarjeta',
            name='fecha_realizada',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 12, 23, 48, 35, 730890), verbose_name='Fecha y Hora'),
        ),
        migrations.AlterField(
            model_name='mascota',
            name='birthday_date',
            field=models.DateField(blank=True, default=datetime.datetime(2018, 6, 12, 23, 48, 35, 728652), null=True, verbose_name='Nacimiento'),
        ),
    ]
