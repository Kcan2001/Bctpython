from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import logout
from .views import UserLoginView, LoginView

app_name = 'accounts'

urlpatterns = [
    url(r'^$', views.myaccount, name='myaccount'),
    url(r'^login/$', UserLoginView.as_view(), name='login'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
    # url(r'^logout/', views.logoutview,  name='logout'),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^update-account/(?P<user_id>[\w-]+)/$', views.AccountUpdate.as_view(), name='update-account'),
    url(r'^update-user/(?P<pk>[\w-]+)/$', views.UserUpdate.as_view(), name='update-user')
]
