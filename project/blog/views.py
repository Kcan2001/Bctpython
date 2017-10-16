from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.conf import settings

from .models import Post


class BlogHomePageView(ListView):
    model = Post
    template_name = 'blog/home.html'
    paginate_by = 2
    queryset = Post.objects.all().exclude(is_draft=True)


class BlogPostPageView(DetailView):
    model = Post
    template_name = 'blog/blog_post.html'

    def get_context_data(self, **kwargs):
        context = super(BlogPostPageView, self).get_context_data(**kwargs)
        context['disqus_embed_url'] = settings.DISQUS_EMBED_URL
        context['disqus_page_url'] = self.request.path
        context['disqus_page_identifier'] = self.object.pk

        return context
