from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic.edit import UpdateView
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView)

from .models import Account


@login_required
def myaccount(request):
    return render(request, 'accounts/myaccount.html')


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


class UserLoginView(LoginView):
    #  TODO check if user is authenticated
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('accounts:myaccount')


class UserLogoutView(LogoutView):
    # TODO When we will deploy, need to make reverse_lazy to homepage
    next_page = '/yourtrips/'
    #template_name = 'frontpages/index.html'


# CBV for password change
class UserPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/registration/password_change.html'
    success_url = reverse_lazy('accounts:password_change_done')


class UserPasswordChangeDoneView(PasswordChangeDoneView):
    # TODO need to make fixed height for this page
    template_name = 'accounts/registration/password_change_done.html'


# Class-based password reset views
# - PasswordResetView sends the mail
# - PasswordResetDoneView shows a success message for the above
# - PasswordResetConfirmView checks the link the user clicked and
#   prompts for a new password
# - PasswordResetCompleteView shows a success message for the above
class UserPasswordResetView(PasswordResetView):
    template_name = 'accounts/registration/password_reset.html'
    email_template_name = 'accounts/registration/password_reset_email.html'
    subject_template_name = 'accounts/registration/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:password_reset_done')


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/registration/password_reset_done.html'


class UserPasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'accounts/registration/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class UserPasswordResetComplete(PasswordResetCompleteView):
    template_name = 'accounts/registration/password_reset_complete.html'


# CBV for models update
class AccountUpdate(UpdateView):
    # slug_field = 'user_id'
    # slug_url_kwarg = 'user_id'
    model = Account
    fields = ['phone', 'address', 'passport_number', 'photo', 'passport_issue_date']
    success_url = reverse_lazy('accounts:myaccount')
    template_name = 'accounts/update_account.html'

    def get_object(self):
        return Account.objects.get(user_id=self.request.user.id)


class UserUpdate(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name']
    success_url = reverse_lazy('accounts:myaccount')
    template_name = 'accounts/update_user.html'

    def get_object(self):
        return User.objects.get(username=self.request.user.username)


# Client old views
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


# def logoutview(request):
#     if request.method == 'POST':
#         logout(request)
#         # return redirect('home')
#         return HttpResponseRedirect('/')
