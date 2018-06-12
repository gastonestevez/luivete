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
    tel_texto = models.CharField('Telefono',max_length=40)
    celular_texto = models.CharField('Celular',max_length=40)
    mail_texto = models.CharField('Email',max_length=200)
    inscripcion_date = models.DateField('Fecha de inscripcion')

    def __str__(self):
        return self.nombre_texto

class Mascota(models.Model):
    sexo_choice = (
        ('Macho','Macho'),
        ('Hembra','Hembra'),
    )

    ambiente_choice = (
        ('Casa','Casa'),
        ('Departamento','Departamento'),
        ('PH','PH'),
        ('Campo','Campo'),
        ('Calle','Calle'),
    )

    alimentacion_choice = (
        ('Balanceado','Balanceado'),
        ('Casero','Casero'),
        ('Medicado','Medicado')
    )

    owner = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    nombre_texto = models.CharField('Nombre',max_length=200)
    chip = models.CharField('Chip', max_length=200,blank=True,null=True)
    esterilizado = models.BooleanField('Esterilizado?')
    raza_texto = models.CharField('Raza',max_length=30, default='Sin completar')
    color_texto = models.CharField('Color',max_length=30,default= 'Sin completar')
    sexo_texto = models.CharField('Sexo',choices=sexo_choice,max_length=15, default='Macho')
    #edad_texto = models.IntegerField('Edad', default='0')
    birthday_date = models.DateField('Nacimiento', default=datetime.now(), blank=True, null=True)
    deceso_date = models.DateField('Deceso',blank=True, null=True)
    causa_deceso = models.CharField('Causa del deceso',blank=True,null=True,max_length=50)
    ambiente = models.CharField('Ambiente', choices=ambiente_choice,default='Departamento',max_length=30)
    alimentacion = models.CharField('Alimentacion',choices=alimentacion_choice,default='Balanceado',max_length=15)
    medicado_observacion = models.CharField('Observacion',blank=True,null=True,max_length=100)
    alimentacion_frecuencia = models.IntegerField('Frecuencia de alimento por dia',default=0)
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
    fecha_realizada = models.DateTimeField('Fecha y Hora', default=datetime.now())
    peso_texto = models.FloatField('Peso')
    temperatura_texto = models.FloatField('Temperatura')
    frecuencia_respiratoria_texto = models.FloatField('Frecuencia Respiratoria')
    linfonodulos_texto = models.CharField('LFN',max_length=50)
    #Sistema Circulatorio
    frecuencia_cardiaca = models.FloatField('Frecuencia Cardiaca')
    auscultacion_text = models.CharField('Auscultacion',choices=auscultacion_choice,max_length=20)
    auscultacion_ritmo_text = models.CharField('Auscultacion Ritmo',choices=auscultacion_ritmo_choice,max_length=20)
    auscultacion_sonidos_text = models.CharField('Auscultacion Sonidos',choices=auscultacion_sonidos_choice,max_length=20)
    soplo_text = models.CharField('Dimension',choices=soplo_choice,max_length=20)
    enObservasion_bool = models.BooleanField('En Observación')
    ficha = models.TextField('Ficha')

    def __str__(self):
        return 'Historia Visita'


class Producto(models.Model):
    tipo_choice = (
        ('Vacuna','Vacuna'),
        ('Medicamento','Medicamento'),
        ('Otro Producto','Otro Producto')
    )
    nombre = models.CharField('Producto',max_length=50)
    referencia = models.CharField('ID de Referencia', max_length=10)
    tipo = models.CharField('Categoria',choices=tipo_choice,max_length=25)

    def __str__(self):
        return ''+str(self.nombre)

class Aplicacion(models.Model):
    nombre_aplicacion = models.ForeignKey(Producto,on_delete=models.CASCADE)
    visita_aplicada = models.ForeignKey(HistorialTarjeta,on_delete=models.CASCADE)
    fecha_proxima_visita = models.DateField('Fecha de proxima visita', null=True,blank=True)

    def __str__(self):
        return 'Aplicacion'