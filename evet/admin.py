# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Cliente
from .models import Mascota
from .models import HistorialTarjeta
from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
import csv
from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template.loader import render_to_string


#Clases


class HistorialInline(admin.StackedInline):
    model = HistorialTarjeta
    fields = [
                'fecha_realizada',
                'peso_texto',
                'temperatura_texto',
                'frecuencia_respiratoria_texto',
                'ficha',
                'linfonodulos_texto',
                'frecuencia_cardiaca',
                'auscultacion_text',
                'auscultacion_ritmo_text',
                'auscultacion_sonidos_text',
                'presencia_soplo_text',
                'soplo_text',
    ]
    extra = 0

class MascotaListadoInline(admin.TabularInline):
    model = Mascota
    fields = ['nombre_texto']
    extra = 0


class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre_texto','direccion_texto','celular_texto','id')
    readonly_fields = ('id',)
    search_fields = ('nombre_texto','direccion_texto','celular_texto','tel_texto')
    inline = [MascotaListadoInline]

class HistorialAdmin(admin.ModelAdmin):
    list_display = ('nombre_mascota','ficha','fecha_realizada',)
    search_fields = ('nombre_mascota__nombre_texto','nombre_mascota__owner__nombre_texto')


class MascotaAdmin(admin.ModelAdmin):
    list_display = ('nombre_texto','owner','image_tag','id')
    search_fields = ('nombre_texto','owner__nombre_texto','id')
    readonly_fields = ('image_tag',)
    raw_id_fields = ('owner',)
    inline = [HistorialInline]

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
        html = render_to_string('admin/exportacion.html', contexto)
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")),result)

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


# Register your models here.
admin.site.register(Cliente, ClienteAdmin, inlines=[MascotaListadoInline])
admin.site.register(Mascota, MascotaAdmin, inlines=[HistorialInline])
admin.site.register(HistorialTarjeta, HistorialAdmin)

