# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from sorl.thumbnail import get_thumbnail
from datetime import datetime
from django.utils import timezone
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

# Create your models here.




class Producto(models.Model):
    tipo_choice = (
        ('Vacuna','Vacuna'),
        ('Medicamento','Medicamento'),
        ('Otro Producto','Otro Producto')
    )
    nombre = models.CharField('Producto',max_length=50)
    referencia = models.CharField('ID de Referencia', max_length=10,blank=True,null=True)
    tipo = models.CharField('Categoria',choices=tipo_choice,max_length=25)
    proxima_aplicacion = models.IntegerField('Proxima aplicacion en dias',blank=True,null=True)

    def __str__(self):
        return ''+str(self.nombre)


class Cliente(models.Model):
    nombre_texto = models.CharField('Nombre y Apellido',max_length=200)
    direccion_texto = models.CharField('Domicilio', max_length=200)
    codigopostal_texto = models.IntegerField('Codigo Postal',blank=True,null=True)
    tel_texto = models.CharField('Telefono',max_length=40,blank=True,null=True)
    celular_texto = models.CharField('Celular',max_length=40,blank=True,null=True)
    mail_texto = models.CharField('Email',max_length=200,blank=True,null=True)
    inscripcion_date = models.DateField('Fecha de inscripcion',default=timezone.now)

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

    owner = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name='Responsable')
    nombre_texto = models.CharField('Mascota',max_length=200)
    chip = models.CharField('Chip', max_length=200,blank=True,null=True)
    esterilizado = models.BooleanField('Esterilizado?',default=False)
    raza_texto = models.CharField('Raza',max_length=30, default='Sin completar')
    color_texto = models.CharField('Color',max_length=30,default= 'Sin completar')
    sexo_texto = models.CharField('Sexo',choices=sexo_choice,max_length=15, default='Macho')
    #edad_texto = models.IntegerField('Edad', default='0')
    birthday_date = models.DateField('Nacimiento', default=timezone.now, blank=True, null=True)
    deceso_date = models.DateField('Deceso',blank=True, null=True)
    causa_deceso = models.CharField('Causa del deceso',blank=True,null=True,max_length=50)
    ambiente = models.CharField('Ambiente', choices=ambiente_choice,default='Departamento',max_length=30)
    alimentacion = models.CharField('Alimentacion',choices=alimentacion_choice,default='Balanceado',max_length=15)
    medicado_observacion = models.CharField('Observacion',blank=True,null=True,max_length=100)
    alimentacion_frecuencia = models.IntegerField('Frecuencia de alimento por dia',default=0)
    foto = models.ImageField(upload_to="images",blank=True, null=True)

    def image_tag(self):
        imagen = get_thumbnail(self.foto, "80x80", crop='center', quality=95)
        if imagen is not None:
            imagen = imagen.url
            return u'<a href="%s" target="_blank"><img src="%s" /></a>' % (self.foto.url,imagen)
        else:
            notexistpath = 'images/notexist.png'
            notexistthumb = get_thumbnail(notexistpath,"80x80", crop='center', quality=95)
            notexistthumb = notexistthumb.url
            return u'<img src="%s" />' % (notexistthumb)

    image_tag.short_description = 'Foto'
    image_tag.allow_tags = True

    def save(self,*args,**kwargs):
        super(Mascota, self).save(*args, **kwargs)

        if self.id is not None:
            if self.foto:
                image = Image.open(self.foto.path)
                image = image.resize((640,360),Image.ANTIALIAS)
                image.save(self.foto.path)

    def __str__(self):
        return self.nombre_texto


class Turno(models.Model):
    razon_choice = (
        ('Observacion','Observacion'),
        ('Vacuna','Vacuna'),
        ('Peluqueria','Peluqueria'),
        ('Cirugía','Cirugía'),
        ('Consulta','Consulta'),
        ('Especialidad','Especialidad'),
        ('Ecografia/Rayos','Ecografia/Rayos'),
    )

    fecha = models.DateTimeField('Proxima visita')
    razon = models.CharField('Razon',choices=razon_choice,max_length=30,default='Observacion')
    se_atiende = models.ForeignKey(Mascota,on_delete=models.CASCADE,verbose_name='Mascota')
    nota = models.TextField('Nota',blank=True,null=True)

    def __str__(self):
        return 'Turno para: ' + '%s' % self.razon + ' el dia ' + str(self.fecha.strftime("%d-%m-%Y"))

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
    fecha_realizada = models.DateTimeField('Fecha y Hora', default=timezone.now)
    peso_texto = models.FloatField('Peso',blank=True,null=True)
    temperatura_texto = models.FloatField('Temperatura',blank=True,null=True)
    frecuencia_respiratoria_texto = models.FloatField('Frecuencia Respiratoria',blank=True,null=True)
    linfonodulos_texto = models.CharField('LFN',max_length=50,blank=True,null=True)
    #Sistema Circulatorio
    frecuencia_cardiaca = models.IntegerField('Frecuencia Cardiaca',blank=True,null=True)
    auscultacion_text = models.CharField('Auscultacion',choices=auscultacion_choice,max_length=20,blank=True,null=True)
    auscultacion_ritmo_text = models.CharField('Auscultacion Ritmo',choices=auscultacion_ritmo_choice,max_length=20,blank=True,null=True)
    auscultacion_sonidos_text = models.CharField('Auscultacion Sonidos',choices=auscultacion_sonidos_choice,max_length=20,blank=True,null=True)
    soplo_text = models.CharField('Dimension',choices=soplo_choice,max_length=20,blank=True,null=True)
    enObservasion_bool = models.BooleanField('En Observación')
    ficha = models.TextField('Ficha')
    atendido_por = models.CharField('idvet',max_length=30,blank=True,null=True)
    aplicacion_text = models.ManyToManyField(Producto, verbose_name='Aplicaciones', blank=True)
    turno = models.ManyToManyField(Turno,verbose_name='Turnos')

    def get_fecha(self):
        return self.fecha_realizada.strftime("%d/%m/%Y  %H:%M")
    get_fecha.short_description = "Fecha"

    def __str__(self):
        return str(self.fecha_realizada.strftime("%d-%m-%Y"))

    #def save(self, *args, **kwargs):
       # turnito = Turno(
        #    fecha=timezone.now,
         #   nota='ok, agregamos turno a: ' + str(self.nombre_mascota)
        #)
        #turnito.save()
        #super(HistorialTarjeta, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Visita'
        verbose_name_plural = 'Visitas'


class EstudiosComplementarios(models.Model):

    razon_choice = (
        ('Radiografia','Radiografia'),
        ('Ecografia','Ecografia'),
        ('Electrocardiograma','Electrocardiograma'),
        ('Estudios de laboratorio','Estudios de laboratorio')
    )

    fecha = models.DateTimeField('Fecha y hora', default=timezone.now)
    razon = models.CharField('Razon',choices=razon_choice,max_length=30,default='Complementario')
    mascota = models.ForeignKey(Mascota, verbose_name="Mascota", on_delete=models.CASCADE)
    radiografia = models.ImageField(verbose_name="Imagen",upload_to="images", blank=True)
    pdf = models.FileField(verbose_name="Archivo adjunto",upload_to="pdf", blank=True, null=True)
    nota = models.TextField('Informe', blank=True, null=True)

    def image_tag(self):
        imagen = get_thumbnail(self.radiografia, "256x144", crop='center', quality=75)
        imagenEntera = self.radiografia.url
        if imagen is not None:
            imagen = imagen.url
            return u'<a href="%s" target="_blank"> <img src="%s"/><a/>' % (imagenEntera,imagen)
        else:
            notexistpath = 'images/notexist.png'
            notexistthumb = get_thumbnail(notexistpath,"50x50", crop='center', quality=50)
            notexistthumb = notexistthumb.url
            return u'<img src="%s" />' % (notexistthumb)

    image_tag.short_description = 'Imagen cargada'
    image_tag.allow_tags = True

    def save(self,*args,**kwargs):
        super(EstudiosComplementarios, self).save(*args, **kwargs)

        if self.id is not None:
            if self.radiografia:
                image = Image.open(self.radiografia.path)
                image = image.resize((1280,720),Image.ANTIALIAS)
                image.save(self.radiografia.path)



    def __str__(self):
        return str(self.fecha.strftime("%d-%m-%Y"))

    class Meta:
        verbose_name = 'Estudios Complementarios'
        verbose_name_plural = 'Estudios Complementarios'