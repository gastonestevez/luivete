# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from sorl.thumbnail import get_thumbnail
from datetime import datetime

# Create your models here.
class Cliente(models.Model):
    nombre_texto = models.CharField('Nombre y Apellido',max_length=200)
    direccion_texto = models.CharField('Domicilio', max_length=200)
    codigopostal_texto = models.IntegerField('Codigo Postal')
    tel_texto = models.IntegerField('Telefono')
    celular_texto = models.IntegerField('Celular')
    mail_texto = models.CharField('Email',max_length=200)
    inscripcion_date = models.DateField('Fecha de inscripcion')

    def __str__(self):
        return self.nombre_texto

class Mascota(models.Model):
    owner = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    nombre_texto = models.CharField('Nombre',max_length=200)
    raza_texto = models.CharField('Raza',max_length=30, default='Sin completar')
    color_texto = models.CharField('Color',max_length=30,default= 'Sin completar')
    sexo_texto = models.CharField('Sexo',max_length=10, default='Sin definir') # TODO << preguntar si es combo-box
    edad_texto = models.IntegerField('Edad', default='0')
    birthday_date = models.DateTimeField('Cumple', default=datetime.now(), blank=True, null=True)
    deceso_date = models.DateTimeField('Deceso',blank=True, null=True)
    foto = models.ImageField(upload_to="images",blank=True, null=True)

    def image_tag(self):
        imagen = get_thumbnail(self.foto, "50x50", crop='center', quality=95)
        if imagen is not None:
            imagen = imagen.url
            return u'<img src="%s" />' % (imagen)
        else:
            notexistpath = 'images/notexist.png'
            notexistthumb = get_thumbnail(notexistpath,"50x50", crop='center', quality=95)
            notexistthumb = notexistthumb.url
            return u'<img src="%s" />' % (notexistthumb)

    image_tag.short_description = 'Foto'
    image_tag.allow_tags = True

    def __str__(self):
        return self.nombre_texto

class HistorialTarjeta(models.Model):
    auscultacion_choice = (
        ('Bradicardia','Bradicardia'),
        ('Normal','Normal'),
        ('Taquicardia','Taquicardia'),
    )

    auscultacion_ritmo_choice = (
        ('Normal','Normal'),
        ('Arritmico','Arritmico'),
    )

    auscultacion_sonidos_choice = (
        ('Normal','Normal'),
        ('Disminuido','Disminuido'),
        ('Aumentado','Aumentado'),
    )

    soplo_choice = (
        ('No detectado', 'No detectado'),
        ('1/6', '1/6'),
        ('2/6', '2/6'),
        ('3/6', '3/6'),
        ('4/6', '4/6'),
        ('5/6', '5/6'),
        ('6/6', '6/6'),
    )

    nombre_mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    ficha = models.TextField('Ficha')
    fecha_realizada = models.DateTimeField('Fecha y Hora')
    peso_texto = models.FloatField('Peso')
    temperatura_texto = models.FloatField('Temperatura')
    frecuencia_respiratoria_texto = models.FloatField('Frecuencia Respiratoria')
    linfonodulos_texto = models.CharField('Linfonódulos',max_length=50)
    #Sistema Circulatorio
    frecuencia_cardiaca = models.FloatField('Frecuencia Cardiaca')
    auscultacion_text = models.CharField('Auscultacion',choices=auscultacion_choice,max_length=20)
    auscultacion_ritmo_text = models.CharField('Auscultacion Ritmo',choices=auscultacion_ritmo_choice,max_length=20)
    auscultacion_sonidos_text = models.CharField('Auscultacion Sonidos',choices=auscultacion_sonidos_choice,max_length=20)
    presencia_soplo_text = models.BooleanField('Presencia de Soplo')
    soplo_text = models.CharField('Dimension',choices=soplo_choice,max_length=20)


    def __str__(self):
        return 'Historia clinica'