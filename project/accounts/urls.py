from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    url(r'^myaccount/', views.myaccount, name='myaccount'),
    url(r'^login/', views.loginview,  name='login'),
    url(r'^logout/', views.logoutview,  name='logout'),
    url(r'^signup/', views.signup, name='signup'),
]
