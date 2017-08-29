"""league URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from league_tracker import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^add_user/', views.create_user),
    url(r'^add_league/', views.create_league),
    url(r'^add_deck/', views.create_deck),
    url(r'^add_record/', views.create_record),
    url(r'^thanks/', views.thanks),
    url(r'^records/(?P<id>\d+)/$',
        views.records),
    url(r'^$', views.index),
]
