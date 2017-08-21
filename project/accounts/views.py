from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from django.views.generic.edit import UpdateView
from .models import Account
from django.urls import reverse_lazy


@login_required
def myaccount(request):
    return render(request, 'accounts/myaccount.html')


# def loginview(request):
#     if request.method == 'POST':
#         user = authenticate(username=request.POST['username'], password=request.POST['password'])
#         if user is not None:
#             login(request, user)
#             if 'next' in request.POST:
#                 return redirect(request.POST['next'])
#             return redirect('accounts:myaccount')
#         else:
#             return render(request, 'accounts/login.html', {'error': 'The Username or/and Password did not match.'})
#     else:
#         return render(request, 'accounts/login.html')

class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('accounts:myaccount')

def logoutview(request):
    if request.method == 'POST':
        logout(request)
        # return redirect('home')
        return HttpResponseRedirect('/')


def signup(request):
    if request.method == 'POST':
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


class AccountUpdate(UpdateView):
    slug_field = 'user_id'
    slug_url_kwarg = 'user_id'
    model = Account
    fields = ['phone', 'address', 'passport_number', 'photo', 'passport_issue_date']
    success_url = reverse_lazy('accounts:myaccount')
    template_name = 'accounts/update_account.html'


class UserUpdate(UpdateView):
    model = User
    fields = ['first_name', 'last_name']
    success_url = reverse_lazy('accounts:myaccount')
    template_name = 'accounts/update_user.html'
