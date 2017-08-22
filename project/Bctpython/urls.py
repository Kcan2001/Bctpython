from django.conf.urls import include, url
from django.contrib import admin
from frontpages import views
import accounts.views
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
    url(r'^yourtrips/', views.yourtrips, name='yourtrips'),
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
    url(r'^thankyou/', views.thankyou, name='thankyou'),
    url(r'^accounts/', include('accounts.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
