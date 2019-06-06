# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-13 02:31
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('evet', '0034_auto_20180611_1615'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aplicacion',
            name='visita_aplicada',
        ),
        migrations.AddField(
            model_name='aplicacion',
            name='pet',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='evet.Mascota'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mascota',
            name='aplicacion_texto',
            field=models.ManyToManyField(to='evet.Producto'),
        ),
        migrations.RemoveField(
            model_name='aplicacion',
            name='nombre_aplicacion',
        ),
        migrations.AddField(
            model_name='aplicacion',
            name='nombre_aplicacion',
            field=models.ManyToManyField(to='evet.Producto'),
        ),
        migrations.AlterField(
            model_name='historialtarjeta',
            name='fecha_realizada',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 12, 23, 31, 8, 191052), verbose_name='Fecha y Hora'),
        ),
        migrations.AlterField(
            model_name='mascota',
            name='birthday_date',
            field=models.DateField(blank=True, default=datetime.datetime(2018, 6, 12, 23, 31, 8, 166301), null=True, verbose_name='Nacimiento'),
        ),
    ]
