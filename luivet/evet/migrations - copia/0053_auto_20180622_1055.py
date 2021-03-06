# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-22 13:55
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evet', '0052_auto_20180621_2245'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estudioscomplementarios',
            name='cardiologia',
        ),
        migrations.RemoveField(
            model_name='estudioscomplementarios',
            name='ecografia',
        ),
        migrations.RemoveField(
            model_name='mascota',
            name='estudios_complementarios',
        ),
        migrations.AddField(
            model_name='historialtarjeta',
            name='estudios_complementarios',
            field=models.ManyToManyField(to='evet.EstudiosComplementarios', verbose_name='Estudios Complementarios'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='inscripcion_date',
            field=models.DateField(default=datetime.datetime(2018, 6, 22, 10, 55, 8, 793672), verbose_name='Fecha de inscripcion'),
        ),
        migrations.AlterField(
            model_name='estudioscomplementarios',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 22, 10, 55, 8, 710072), verbose_name='Fecha y hora'),
        ),
        migrations.AlterField(
            model_name='historialtarjeta',
            name='fecha_realizada',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 22, 10, 55, 8, 798351), verbose_name='Fecha y Hora'),
        ),
        migrations.AlterField(
            model_name='mascota',
            name='birthday_date',
            field=models.DateField(blank=True, default=datetime.datetime(2018, 6, 22, 10, 55, 8, 795139), null=True, verbose_name='Nacimiento'),
        ),
    ]
