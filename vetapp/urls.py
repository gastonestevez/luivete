"""vetapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.conf import settings
from django.contrib import admin
from django.views.static import serve
from django.views.generic import TemplateView
from evet import views


urlpatterns = [
    url(r'^', admin.site.urls),
    url(r'^admin/dynamic_raw_id/', include('dynamic_raw_id.urls')),
    url(r'^backexport/',views.output,name='output'),
    url(r'^synchro/', include('synchro.urls', 'synchro', 'synchro')),

  #  url(r'^evet/turno/(?P<pk>[0-9]+)/change/',views.modificarTurno,name='modificar')
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),

    ]