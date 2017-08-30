from django.shortcuts import render
from django.contrib.auth.views import TemplateView

from .instagram_api import GetUserMedia


class GalleryInstagramView(TemplateView):
    template_name = 'frontpages/gallery.html'

    def get_context_data(self, **kwargs):
        context = super(GalleryInstagramView, self).get_context_data(**kwargs)
        # You can set how many photos will be shown in .recent_media($how_many_photos$)
        context['photos'] = GetUserMedia.recent_media(18)
        return context


def about(request):
    return render(request, 'frontpages/about/about.html')


def home(request):
    return render(request, 'frontpages/index.html')


def yourtrips(request):
    return render(request, 'frontpages/yourtrips.html')


def accommodations(request):
    return render(request, 'frontpages/about/accommodations.html')


def guides(request):
    return render(request, 'frontpages/about/guides.html')


def included(request):
    return render(request, 'frontpages/about/included.html')


def terms(request):
    return render(request, 'frontpages/about/terms.html')


def privacy(request):
    return render(request, 'frontpages/privacy.html')


def packing(request):
    return render(request, 'frontpages/about/packing.html')


def thankyou(request):
    return render(request, 'frontpages/thankyou.html')


def faqs(request):
    return render(request, 'frontpages/faqs.html')


def easteuro(request):
    return render(request, 'frontpages/easteuro.html')


def westeuro(request):
    return render(request, 'frontpages/westeuro.html')


def scandinavia(request):
    return render(request, 'frontpages/scandinavia.html')


def kilimanjaro(request):
    return render(request, 'frontpages/kilimanjaro.html')


def reviews(request):
    return render(request, 'frontpages/about/reviews.html')


def contact(request):
    return render(request, 'frontpages/contact.html')


# Views for custom errors pages: 400, 403, 404, 500
def handler400(request):
    return render(request, 'frontpages/errors/400.html', status=400)


def handler403(request):
    return render(request, 'frontpages/errors/403.html', status=403)


def handler404(request):
    return render(request, 'frontpages/errors/404.html', status=404)


def handler500(request):
    return render(request, 'frontpages/errors/500.html', status=500)
