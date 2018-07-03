# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Cliente
from .models import Mascota
from .models import HistorialTarjeta
from .models import Producto
from .models import Turno
from .models import EstudiosComplementarios
from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime, date
import csv
from io import BytesIO
from tabbed_admin import TabbedModelAdmin
from django.template.loader import get_template
from dynamic_raw_id.admin import DynamicRawIDMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import timedelta


#Filtros
class FiltrarPorFechaDeHoy(admin.SimpleListFilter):
    title = _('Hoy')
    parameter_name = 'fecha'

    def next_weekday(self,d, weekday):
        days_ahead = weekday - d.weekday()
        if days_ahead <= 0:  # Target day already happened this week
            days_ahead += 7
        return d + timedelta(days_ahead)

    def lookups(self, request, model_admin):
        return (
            ('man', ('Mañana')),
            ('tarde', _('Tarde')),
            ('noche', _('Noche')),
            ('proxsem',_('Semana Siguiente')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'man':
            return queryset.filter(fecha__gte=date(datetime.now().year,datetime.now().month,datetime.now().day),
                                   fecha__lte=datetime(datetime.now().year,datetime.now().month,datetime.now().day,12,59))
        if self.value() == 'tarde':
            return queryset.filter(fecha__gte=datetime(datetime.now().year, datetime.now().month, datetime.now().day,
                                                       13, 00),
                                   fecha__lte=datetime(datetime.now().year, datetime.now().month, datetime.now().day,
                                                       17, 59))
        if self.value() == 'noche':
            return queryset.filter(fecha__gte=datetime(datetime.now().year, datetime.now().month, datetime.now().day,
                                                       18, 00),
                                   fecha__lte=datetime(datetime.now().year, datetime.now().month, datetime.now().day,
                                                       23, 59))
        if self.value() == 'proxsem':
            proxsemana = self.next_weekday(datetime.now(),0)
            proxsemana = self.next_weekday(proxsemana,0)
            return queryset.filter(fecha__gte=self.next_weekday(datetime.now(),0),
                                   fecha__lte=proxsemana)

        if self.value() is None:
            return queryset.filter(fecha__gte=date(datetime.now().year, datetime.now().month, datetime.now().day),
                                   fecha__lte=datetime(datetime.now().year, datetime.now().month, datetime.now().day,
                                                       23, 59))


#Clases
class NuevoEstudioInline(admin.StackedInline):
    model = EstudiosComplementarios
    extra = 0
    readonly_fields = ('image_tag',)
    show_change_link = True
    fields = ['fecha','razon','radiografia','image_tag','pdf','nota']

    def get_queryset(self, request):
        # get the existing query set, then empty it.
        qs = super(NuevoEstudioInline, self).get_queryset(request)
        return qs.none()


class EstudiosRadiografiaInline(admin.StackedInline):
    model = EstudiosComplementarios
    readonly_fields = ('image_tag',)
    fields = ['fecha','razon','radiografia','image_tag','pdf','nota']
    show_change_link = True
    extra = 0
    ordering = ('-fecha',)
    classes = ['collapse']
    verbose_name_plural = "Radiografias"
    verbose_name = "Radiografia"

    def get_queryset(self, request):
        # get the existing query set, then empty it.
        radios = EstudiosComplementarios.objects.filter(razon='Radiografia').order_by('-fecha')
        return radios


class EstudiosEcografiasInline(admin.StackedInline):
    model = EstudiosComplementarios
    readonly_fields = ('image_tag',)
    fields = ['fecha','razon','radiografia','image_tag','pdf','nota']
    show_change_link = True
    extra = 0
    ordering = ('-fecha',)
    classes = ['collapse']
    verbose_name_plural = "Ecografias"
    verbose_name = "Ecografia"

    def get_queryset(self, request):
        # get the existing query set, then empty it.
        radios = EstudiosComplementarios.objects.filter(razon='Ecografia').order_by('-fecha')
        return radios


class EstudiosElectroInline(admin.StackedInline):
    model = EstudiosComplementarios
    readonly_fields = ('image_tag',)
    fields = ['fecha','razon','radiografia','image_tag','pdf','nota']
    show_change_link = True
    extra = 0
    ordering = ('-fecha',)
    classes = ['collapse']
    verbose_name_plural = "Electrocardiogramas"
    verbose_name = "Electrocardiograma"

    def get_queryset(self, request):
        # get the existing query set, then empty it.
        radios = EstudiosComplementarios.objects.filter(razon='Electrocardiograma').order_by('-fecha')
        return radios


class EstudiosLaboratorioInline(admin.StackedInline):
    model = EstudiosComplementarios
    readonly_fields = ('image_tag',)
    fields = ['fecha','razon','radiografia','image_tag','pdf','nota']
    show_change_link = True
    extra = 0
    ordering = ('-fecha',)
    classes = ['collapse']
    verbose_name_plural = "Laboratorio"
    verbose_name = "Laboratorio"

    def get_queryset(self, request):
        # get the existing query set, then empty it.
        radios = EstudiosComplementarios.objects.filter(razon='Estudios de laboratorio').order_by('-fecha')
        return radios


class HistorialInline(DynamicRawIDMixin,admin.StackedInline):
    save_on_top = True
    model = HistorialTarjeta
    dynamic_raw_id_fields = ('aplicacion_text',)
    #readonly_fields = ('aplicacion_text',)
    fieldsets = (
        ('EOG',{
            'classes': ('collapse', 'open'),
            'fields': ('fecha_realizada',
                       ('peso_texto','temperatura_texto','frecuencia_respiratoria_texto','linfonodulos_texto'),
                       )
        }),
        ('Sistema Circulatorio', {
            'classes': ('collapse', 'open'),
            'fields': (('frecuencia_cardiaca',
                       'auscultacion_text',
                       'auscultacion_ritmo_text',
                       'auscultacion_sonidos_text',
                       'soplo_text',
                       'enObservasion_bool',),)
        }),
        ('Ficha', {
            'fields': ('ficha','atendido_por','aplicacion_text',)
        }),
    )
    extra = 0
    ordering = ('-fecha_realizada',)
    classes = ['collapse']
    verbose_name = "Visita anterior"
    verbose_name_plural = "Visitas anteriores"

class NuevoHistorialInline(DynamicRawIDMixin,admin.StackedInline):
    save_on_top = True
    model = HistorialTarjeta
    extra = 0
    dynamic_raw_id_fields = ('aplicacion_text','estudios_complementarios')

    def get_queryset(self, request):
        # get the existing query set, then empty it.
        qs = super(NuevoHistorialInline, self).get_queryset(request)
        return qs.none()

    fieldsets = (
        ('EOG', {
            'classes': ('collapse', 'open'),
            'fields': ('fecha_realizada',
                       ('peso_texto', 'temperatura_texto', 'frecuencia_respiratoria_texto', 'linfonodulos_texto'),
                       )
        }),
        ('Sistema Circulatorio', {
            'classes': ('collapse', 'open'),
            'fields': (('frecuencia_cardiaca',
                        'auscultacion_text',
                        'auscultacion_ritmo_text',
                        'auscultacion_sonidos_text',
                        'soplo_text',
                        'enObservasion_bool',),)
        }),
        ('Ficha', {
            'fields': ('ficha','atendido_por','aplicacion_text',)
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

    list_display = ('nombre_mascota','get_fecha','ficha',)
    ordering = ('-fecha_realizada',)
    search_fields = ('nombre_mascota__nombre_texto','nombre_mascota__owner__nombre_texto')
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
            'fields': ('ficha','atendido_por','aplicacion_text',),
        })
    )


class MascotaAdmin(DynamicRawIDMixin,TabbedModelAdmin):
    list_display = ('owner','nombre_texto','image_tag','id')
    search_fields = ('owner__nombre_texto','owner__tel_texto','owner__celular_texto','id')
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

    tab_estudios_complementarios = (
        NuevoEstudioInline,
        EstudiosRadiografiaInline,
        EstudiosEcografiasInline,
        EstudiosElectroInline,
        EstudiosLaboratorioInline,
    )

    tabs = [
        ('Informacion',tab_mascota),
        ('Historial Clinico',tab_historial),
        ('Estudios Complementarios',tab_estudios_complementarios)
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
#TODO IMPLEMENTAR BIEN ESTE METODO !!
    def exportar_pdf(self,request,queryset):
        historiales = HistorialTarjeta.objects.filter(nombre_mascota__nombre_texto=queryset[0])
        contexto = {'Mascotas': queryset,
                   'Historiales': historiales,
                   'FECHA_DE_HOY': datetime.now(),
                   }
        template = get_template('admin/exportacion.html')
        html = template.render(contexto)
        result = BytesIO
        #pdf = pisa.pisaDocument(BytesIO(.encode("UTF-8")),result)

        #if not pdf.err:
         #   return HttpResponse(result.getvalue(),content_type='application/pdf')
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

class TurnoAdmin(DynamicRawIDMixin,admin.ModelAdmin):
    extra = 0
    dynamic_raw_id_fields = ('se_atiende',)
    list_display = ('get_dia','get_hora','se_atiende','razon','nota')
    #list_filter = ('fecha','razon',)
    list_filter = (FiltrarPorFechaDeHoy,)
    ordering = ('fecha',)

    def get_dia(self,obj):
        return obj.fecha.date()
    get_dia.short_description = 'Fecha'

    def get_hora(self,obj):
        return obj.fecha.time()
    get_hora.short_description = 'Hora'



class EstudiosComplementariosAdmin(admin.ModelAdmin):
    list_display = ('fecha','nota')
    ordering = ('fecha',)
    fieldsets = (
        ('Imagenes',{
            'fields':(('fecha','mascota','radiografia','pdf','nota'),)
        }),
    )
    list_filter = ('fecha','razon')


# Register your models here.
admin.site.register(Cliente, ClienteAdmin, inlines=[MascotaListadoInline])
admin.site.register(Mascota, MascotaAdmin, inlines=[NuevoHistorialInline, HistorialInline,EstudiosElectroInline,EstudiosEcografiasInline,EstudiosLaboratorioInline,EstudiosRadiografiaInline,NuevoEstudioInline])
admin.site.register(HistorialTarjeta, HistorialAdmin,)
admin.site.register(Producto,ProductoAdmin)
admin.site.register(Turno,TurnoAdmin)
admin.site.register(EstudiosComplementarios,EstudiosComplementariosAdmin)