# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Turno
import datetime
from datetime import timedelta
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    startdate = datetime.datetime.now().date()
    enddate = startdate + timedelta(days=365)
    turnos = Turno.objects.filter(fecha__range=[startdate, enddate])
    return render(request,'evet/turnos.html', {'turnos':turnos})

def modificarTurno(request):
    pass
