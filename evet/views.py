# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import Turno

from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    turnos = Turno.objects.all()
    return render(request,'evet/turnos.html', {'turnos':turnos})

def modificarTurno(request):
    pass
