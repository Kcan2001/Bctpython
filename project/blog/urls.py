from django.conf.urls import url
from . import views

app_name = 'blog'

urlpatterns = [
    url(r'^$', views.BlogHomePageView.as_view(), name='home'),
    url(r'^(?P<pk>[-\w]+)/$', views.BlogPostPageView.as_view(), name='blog_post'),
]