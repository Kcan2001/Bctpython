from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext


def about(request):
    return render(request, 'frontpages/about.html')


def home(request):
    return render(request, 'frontpages/index.html')


def gallery(request):
    return render(request, 'frontpages/gallery.html')


def yourtrips(request):
    return render(request, 'frontpages/yourtrips.html')


def accommodations(request):
    return render(request, 'frontpages/accommodations.html')


def guides(request):
    return render(request, 'frontpages/guides.html')


def included(request):
    return render(request, 'frontpages/included.html')


def terms(request):
    return render(request, 'frontpages/terms.html')


def privacy(request):
    return render(request, 'frontpages/privacy.html')


def packing(request):
    return render(request, 'frontpages/packing.html')


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
    return render(request, 'frontpages/reviews.html')


def contact(request):
    return render(request, 'frontpages/contact.html')


def handler404(request):
    response = render_to_response('frontpages/404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('frontpages/500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response

# Create your views here.
