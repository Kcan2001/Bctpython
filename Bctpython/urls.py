"""Bctpython URL Configuration

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
from django.conf.urls import include, url
from django.contrib import admin
from frontpages import views
from django.http import HttpResponse

import accounts.views
from django.contrib.sitemaps.views import sitemap
from django.contrib.auth import views as auth_views
from django.conf.urls import (
handler400, handler403, handler404, handler500
)

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home,  name='home'),
    url(r'^about/', views.about, name='about'),
    url(r'^gallery/', views.gallery,  name='gallery'),
    url(r'^your-trips/', views.yourtrips, name='your-trips'),
    url(r'^login/', views.loginview,  name='login'),
    url(r'^logout/', views.logoutview,  name='logout'),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^guides/', views.guides,  name='guides'),
    url(r'^accommodations/', views.accommodations, name='accommodations'),
    url(r'^included/', views.included,  name='included'),
    url(r'^packing/', views.packing, name='packing'),
    url(r'^westeuro/', views.westeuro,  name='westeuro'),
    url(r'^easteuro/', views.easteuro, name='easteuro'),
    url(r'^scandinavia/', views.scandinavia,  name='scandinavia'),
    url(r'^kilimanjaro/', views.kilimanjaro, name='kilimanjaro'),
    url(r'^reviews/', views.reviews,  name='reviews'),
    url(r'^contact/', views.contact, name='contact'),
    url(r'^faqs/', views.faqs, name='faqs'),
    url(r'^terms/', views.terms, name='terms'),
    url(r'^privacy/', views.privacy, name='privacy'),
    url(r'^404/', views.handler404, name='404'),
    url(r'^500/', views.handler500, name='500'),
    url(r'^thank-you/', views.thankyou, name='thank-you'),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^robots\.txt$', lambda r: HttpResponse("User-Agent: *\nDisallow:", content_type="text/plain")),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
