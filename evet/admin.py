# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Cliente
from .models import Mascota
from .models import HistorialTarjeta
from .models import Aplicacion
from .models import Producto
from .models import Turno
from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime, date
import csv
from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import render_to_string
from tabbed_admin import TabbedModelAdmin
from django.template.loader import get_template
from cStringIO import StringIO
from dynamic_raw_id.admin import DynamicRawIDMixin
#Clases

class AplicacionInline(admin.TabularInline):
    raw_id_fields = ('nombre_aplicacion',)
    model = Aplicacion
    extra = 0

class HistorialInline(DynamicRawIDMixin,admin.StackedInline):
    save_on_top = True
    model = HistorialTarjeta
    inlines = [AplicacionInline]
    dynamic_raw_id_fields = ('aplicacion_text',)
    #readonly_fields = ('aplicacion_text',)
    fieldsets = (
        ('EOG',{
            'fields': ('fecha_realizada',
                       ('peso_texto','temperatura_texto','frecuencia_respiratoria_texto','linfonodulos_texto'),
                       )
        }),
        ('Sistema Circulatorio', {
            'fields': (('frecuencia_cardiaca',
                       'auscultacion_text',
                       'auscultacion_ritmo_text',
                       'auscultacion_sonidos_text',
                       'soplo_text',
                       'enObservasion_bool',),)
        }),
        ('Ficha', {
            'fields': ('ficha','aplicacion_text',)
        }),
    )
    extra = 0
    ordering = ('-fecha_realizada',)
    classes = ['collapse']

class NuevoHistorialInline(DynamicRawIDMixin,admin.StackedInline):
    save_on_top = True
    model = HistorialTarjeta
    extra = 0
    inlines=[AplicacionInline]
    dynamic_raw_id_fields = ('aplicacion_text',)

    def get_queryset(self, request):
        # get the existing query set, then empty it.
        qs = super(NuevoHistorialInline, self).get_queryset(request)
        return qs.none()

    fieldsets = (
        ('EOG', {
            'fields': ('fecha_realizada',
                       ('peso_texto', 'temperatura_texto', 'frecuencia_respiratoria_texto', 'linfonodulos_texto'),
                       )
        }),
        ('Sistema Circulatorio', {
            'fields': (('frecuencia_cardiaca',
                        'auscultacion_text',
                        'auscultacion_ritmo_text',
                        'auscultacion_sonidos_text',
                        'soplo_text',
                        'enObservasion_bool',),)
        }),
        ('Ficha', {
            'fields': ('ficha','aplicacion_text')
        })
    )


class MascotaListadoInline(admin.TabularInline):
    model = Mascota
    fields = ['nombre_texto',]
    show_change_link = True
    extra = 0


class ClienteAdmin(TabbedModelAdmin):
    list_display = ('nombre_texto','direccion_texto','celular_texto','id')
    readonly_fields = ('id',)
    search_fields = ('nombre_texto','direccion_texto','celular_texto','tel_texto')
    inline = [MascotaListadoInline]
    fields = (
        'nombre_texto',
        ('direccion_texto','codigopostal_texto'),
        ('tel_texto','celular_texto'),
        'mail_texto',
        'inscripcion_date',
    )
    tab_mascota = (MascotaListadoInline,)
    tab_cliente = (
    ('General',{
        'fields':('nombre_texto','inscripcion_date')
    }),
        ('Ubicación',{
            'fields':(('direccion_texto','codigopostal_texto'),)
    }),
    ('Comunicación',{
        'fields':(('tel_texto','celular_texto'),'mail_texto')
    })
    )
    tabs = [
        ('Cliente',tab_cliente),
        ('Mascotas',tab_mascota)
    ]

class HistorialAdmin(admin.ModelAdmin):
    list_display = ('nombre_mascota','ficha','fecha_realizada',)
    search_fields = ('nombre_mascota__nombre_texto','nombre_mascota__owner__nombre_texto')
    inline = [AplicacionInline]
    fieldsets = (
        ('General', {
            'fields': ('fecha_realizada',
                'peso_texto',
                'temperatura_texto',
                'frecuencia_respiratoria_texto',
                'linfonodulos_texto',)
        }),
        ('Sistema Circulatorio', {
            'fields': ('auscultacion_text',
                'auscultacion_ritmo_text',
                'auscultacion_sonidos_text',
                'soplo_text',
                'enObservasion_bool',)
        }),
        ('Ficha', {
            'fields': ('ficha','aplicacion_text'),
        })
    )

class MascotaAdmin(TabbedModelAdmin):
    list_display = ('nombre_texto','owner','image_tag','id')
    search_fields = ('nombre_texto','owner__nombre_texto','id')
    save_on_top = True
    readonly_fields = ('get_edad','image_tag',)
    raw_id_fields = ('owner',)
    inline = [HistorialInline]
    tab_mascota = (
        ('General',{
            'fields':('owner',
                      ('nombre_texto','chip'),
                      ('raza_texto','color_texto','sexo_texto','esterilizado'),
                      'birthday_date','get_edad','deceso_date','causa_deceso',
                      'ambiente',
                      ('alimentacion','alimentacion_frecuencia','medicado_observacion'),
                      ('foto','image_tag')
                      )
        }),
    )
    tab_historial = (
        NuevoHistorialInline,
        HistorialInline,
    )
    tabs = [
        ('Informacion',tab_mascota),
        ('Historial Clinico',tab_historial)
    ]
    def get_edad(self,obj): #Esta para el ogt esto TODO
        if(obj.birthday_date is not None):
            hoy = date.today()
            #edadFinal = str(edadYear) + ' años, ' + str(edadMonth) + ' meses, '+ str(edadDay) + ' dias.'
            edadYear = hoy.year - obj.birthday_date.year - ((hoy.month, hoy.day) < (obj.birthday_date.month, obj.birthday_date.day))
            edadMonth = 0

            if (obj.birthday_date.month < hoy.month):
                edadMonth = hoy.month - obj.birthday_date.month
            elif (obj.birthday_date.month > hoy.month):
                edadMonth = 12 - obj.birthday_date.month + hoy.month
            else:
                if(hoy.day > obj.birthday_date.day and hoy.year != obj.birthday_date.year):
                    edadMonth = 12
                else:
                    edadMonth = 0

            edadDay = datetime.now() - datetime(obj.birthday_date.year,obj.birthday_date.month,obj.birthday_date.day,0,0,0)
            edadDias = edadDay.days - ((datetime.now().year-obj.birthday_date.year)*365)
            return str(edadYear) + ' años ' + str(edadMonth) + ' mes(es) ' + str(edadDias) + ' dias.'
        else:
            return '0 años.'
    get_edad.short_description = "Edad"

    # Actions
    actions = ["exportar_historial","exportar_html","exportar_pdf"]

    def exportar_html(self,request,queryset):
        historiales = HistorialTarjeta.objects.filter(nombre_mascota__nombre_texto=queryset[0])
        return render(request,'admin/exportacion.html', context={'Mascotas':queryset,
                                                                 'Historiales':historiales,
                                                                 'FECHA_DE_HOY':datetime.now()})

    def exportar_pdf(self,request,queryset):
        historiales = HistorialTarjeta.objects.filter(nombre_mascota__nombre_texto=queryset[0])
        contexto = {'Mascotas': queryset,
                   'Historiales': historiales,
                   'FECHA_DE_HOY': datetime.now(),
                   }
        template = get_template('admin/exportacion.html')
        html = template.render(contexto)
        result = StringIO()
        pdf = pisa.pisaDocument(StringIO(html.encode("UTF-8")),result)

        if not pdf.err:
            return HttpResponse(result.getvalue(),content_type='application/pdf')
        return None

    #CSV <<
    def exportar_historial(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="historial.csv"'

        writer = csv.writer(response)
        mascotas = queryset.values_list('nombre_texto', 'owner', 'id')
        writer.writerow(['FICHAS'])
        for mascota in mascotas:
            writer.writerow(mascota)
            historiales = HistorialTarjeta.objects.filter(nombre_mascota__nombre_texto=mascota[0])
            for historial in historiales:
                writer.writerow([historial.fecha_realizada])
                writer.writerow([historial.ficha])

        return response

    exportar_historial.short_description = "Exportar historial clinico"
    exportar_html.short_description = "Exportar Historial a HTML"
    exportar_pdf.short_description = "Exportar Historial a PDF"

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre','referencia','tipo','proxima_aplicacion')
    search_fields = ('nombre','referencia')
    fieldsets = (
        (None,{
            'fields':(('nombre','referencia','tipo','proxima_aplicacion'),)
        }),
    )

class TurnoAdmin(admin.ModelAdmin):
    extra = 0
    list_display = ('fecha',)


# Register your models here.
admin.site.register(Cliente, ClienteAdmin, inlines=[MascotaListadoInline])
admin.site.register(Mascota, MascotaAdmin, inlines=[NuevoHistorialInline, HistorialInline])
admin.site.register(HistorialTarjeta, HistorialAdmin, inlines=[AplicacionInline])
admin.site.register(Producto,ProductoAdmin)
admin.site.register(Turno,TurnoAdmin)