# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Turno
import datetime
from datetime import timedelta
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
  return render(request, 'evet/index.html')

def output(request):
    return render(request, 'evet/backexport.html', {'output': 'OK! 200'})