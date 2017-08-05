from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def myaccount(request):
    return render(request, 'accounts/myaccount.html')

def loginview(request):
    if  request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST['next'])
            return redirect('accounts:myaccount')
        else:
            return render(request, 'accounts/login.html', {'error': 'The Username and Password did not match.'})
    else:
        return render(request, 'accounts/login.html')

def logoutview(request):
    if  request.method == 'POST':
        logout(request)
        return redirect('login')
