# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from sorl.thumbnail import get_thumbnail
from datetime import datetime
from django.utils import timezone
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings
from django.contrib.auth.models import User
from datetime import timedelta
# Create your models here.



class Especie(models.Model):
    nombre = models.CharField('Especie', max_length=50)

    def __str__(self):
        return self.nombre.encode('utf-8').strip()

class Raza(models.Model):
    nombre = models.CharField('Raza', max_length=50)
    identificacion = models.CharField('Identificacion', max_length=25)

    def __str__(self):
        return self.nombre.encode('utf-8').strip()

class Producto(models.Model):
    tipo_choice = (
        ('Vacuna','Vacuna'),
        ('Medicamento','Medicamento'),
        ('Otro Producto','Otro Producto')
    )
    nombre = models.CharField('Producto',max_length=50)
    referencia = models.CharField('ID de Referencia', max_length=10,blank=True,null=True)
    tipo = models.CharField('Categoria',choices=tipo_choice,max_length=25)
    proxima_aplicacion = models.IntegerField('Proxima aplicacion en dias')
    stock = models.IntegerField('Stock',default=0)
    precio = models.FloatField('Precio',default=0)

    def __str__(self):
        return ''+str(self.nombre)

class RegistroStock(models.Model):
    fecha = models.DateTimeField('Fecha',default=timezone.now)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name='Producto')
    cantidad = models.IntegerField('Cantidad')
    comentario = models.TextField('Comentario')

    def __str__(self):
        return 'Registros de Stock'

    def save(self, *args, **kwargs):
        super(RegistroStock, self).save(*args, **kwargs)
        item = Producto.objects.get(pk=self.producto.pk)
        item.stock += self.cantidad
        item.save()

class Cliente(models.Model):
    nombre_texto = models.CharField('Nombre y Apellido',max_length=200)
    direccion_texto = models.CharField('Domicilio', max_length=200)
    codigopostal_texto = models.IntegerField('Codigo Postal',blank=True,null=True)
    tel_texto = models.CharField('Telefono',max_length=40,blank=True,null=True)
    celular_texto = models.CharField('Celular',max_length=40,blank=True,null=True)
    mail_texto = models.CharField('Email',max_length=200,blank=True,null=True)
    inscripcion_date = models.DateField('Fecha de inscripcion',default=timezone.now)

    def __str__(self):
        return self.nombre_texto.encode('utf-8').strip()

class Mascota(models.Model):
    sexo_choice = (
        ('Macho','Macho'),
        ('Hembra','Hembra'),
        ('Sin Especificar', 'Sin Especificar'),
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
    especie = models.ForeignKey(
        Especie,
        on_delete=models.CASCADE,
        verbose_name='Especie'
    )
    #raza_texto = models.CharField('Raza',max_length=30, default='Sin completar')
    raza_texto = models.ForeignKey(Raza, on_delete=models.CASCADE, verbose_name='Raza',null=True)
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
        return 'Turno para: ' + '%s' % self.razon + ' el dia ' + (self.fecha.strftime("%d-%m-%Y")).encode('utf-8').strip()

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

    mucosa_choice = (
        ('Normal','Normal'),
        ('Palidas','Palidas'),
        ('Congestivas','Congestivas'),
        ('Ictericos','Ictericos')
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
    mucosa_text = models.CharField('Mucosa',choices=mucosa_choice,max_length=20,blank=True,null=True)
    enObservasion_bool = models.BooleanField('En Observación')
    ficha = models.TextField('Ficha')
    atendido_por = models.IntegerField('Identificacion',blank=True,null=True)
    aplicacion_text = models.ManyToManyField(Producto, verbose_name='Aplicaciones', blank=True)
    turno = models.ManyToManyField(Turno,verbose_name='Turnos')

    def get_fecha(self):
        return self.fecha_realizada.strftime("%d/%m/%Y  %H:%M")
    get_fecha.short_description = "Fecha"

    def __str__(self):
        return str(self.fecha_realizada.strftime("%d-%m-%Y"))

    def save(self, *args, **kwargs):
        super(HistorialTarjeta, self).save(*args, **kwargs)
        for item in self.aplicacion_text.all():
            nuevoRegistro = RegistroStock(
                producto=item,
                cantidad=-1,
                comentario='Aplicacion de '+ (item.nombre) +' a '+str(self.nombre_mascota)+'. Se descuenta 1 unidad.'
            )
            nuevoRegistro.save()

            producto = Producto.objects.get(pk=item.pk)
            if producto.proxima_aplicacion > 5:

                turnito = Turno(
                    fecha=timezone.now()+timezone.timedelta(days=producto.proxima_aplicacion),
                    se_atiende=self.nombre_mascota,
                    nota='AVISO: RECORDATORIO POR APLICACIÓN: ' + producto.nombre
                )

                if producto.tipo == 'Vacuna':
                    turnito.razon = producto.tipo

                turnito.save()

    class Meta:
        verbose_name = 'Visita'
        verbose_name_plural = 'Visitas'


class EstudiosComplementarios(models.Model):

    razon_choice = (
        ('Radiografia','Radiografia'),
        ('Ecografia','Ecografia'),
        ('Electrocardiograma','Electrocardiograma'),
        ('Estudios de laboratorio','Estudios de laboratorio'),
		('Otros','Otros')
    )

    fecha = models.DateTimeField('Fecha y hora', default=timezone.now)
    razon = models.CharField('Razon',choices=razon_choice,max_length=30)
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
                #image = image.resize((1280,720),Image.ANTIALIAS)
                image.save(self.radiografia.path)


    def __str__(self):
        return str(self.fecha.strftime("%d-%m-%Y"))

    class Meta:
        verbose_name = 'Estudio complementario'
        verbose_name_plural = 'Estudios complementarios'