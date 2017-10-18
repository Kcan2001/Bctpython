from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext

def about(request):
    return render(request, 'frontpages/about.html')

def home(request):
    return render(request, 'frontpages/index.html')

def gallery(request):
    return render(request, 'frontpages/gallery.html')

def loginview(request):
    if  request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST['next'])
            return redirect('accounts:myaccount')
        else:
            return render(request, 'frontpages/login.html', {'error': 'The Username and Password did not match.'})
    else:
        return render(request, 'frontpages/login.html')

def logoutview(request):
    if  request.method == 'POST':
        logout(request)
        return redirect('home')

def signup(request):
    if  request.method == 'POST':
        if request.POST['password'] == request.POST['password2']:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'frontpages/signup.html', {'error': 'Username already in use, Please try another.'})
            except User.DoesNotExist:
                user = User.objects.create_user(first_name=request.POST['firstname'], last_name=request.POST['lastname'], email=request.POST['email'], username=request.POST['username'], password=request.POST['password'])
                login(request, user)
                return render(request, 'accounts/myaccount.html')
        else:
            return render(request, 'frontpages/signup.html', {'error': 'Passwords did not match.'})
    else:
        return render(request, 'frontpages/signup.html')

def yourtrips(request):
    return render(request, 'frontpages/your-trips.html')

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
    return render(request, 'frontpages/thank-you.html')

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
