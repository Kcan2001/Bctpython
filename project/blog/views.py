from django.shortcuts import render
from django.contrib.auth.views import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Post


class BlogHomePageView(ListView):
    model = Post
    template_name = 'blog/home.html'
    paginate_by = 2
    queryset = Post.objects.all().exclude(is_draft=True)


class BlogPostPageView(DetailView):
    model = Post
    template_name = 'blog/blog_post.html'
