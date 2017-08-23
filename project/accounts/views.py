from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import login
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
    PasswordResetCompleteView,
    TemplateView)

from .models import Account

from .forms import SignUpForm
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_text
from django.template.loader import render_to_string
from .tokens import account_activation_token


class UserHomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/home.html'


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate your account - Black Crown Tours'
            message = render_to_string('accounts/registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('accounts:account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'accounts/registration/signup.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'accounts/registration/account_activation_done.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.account.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('accounts:home')
    else:
        return render(request, 'account_activation_invalid.html')


class UserLoginView(LoginView):
    #  TODO check if user is authenticated
    template_name = 'accounts/login.html'
    # success_url = reverse_lazy('accounts:home')


class UserLogoutView(LogoutView):
    # TODO When we will deploy, need to make reverse_lazy to homepage
    next_page = '/yourtrips/'
    #template_name = 'frontpages/index.html'


# CBV for password change
class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/registration/password_change.html'
    success_url = reverse_lazy('accounts:password_change_done')


class UserPasswordChangeDoneView(LoginRequiredMixin, PasswordChangeDoneView):
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
class AccountUpdate(LoginRequiredMixin, UpdateView):
    # slug_field = 'user_id'
    # slug_url_kwarg = 'user_id'
    model = Account
    fields = ['phone', 'emergency_contact', 'birth_date', 'address', 'passport_number', 'passport_nationality',
              'passport_issue_date', 'passport_expire_date', 'photo']
    success_url = reverse_lazy('accounts:home')
    template_name = 'accounts/update_account.html'

    def get_object(self):
        return Account.objects.get(user_id=self.request.user.id)


class UserUpdate(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name']
    success_url = reverse_lazy('accounts:home')
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
#             return redirect('accounts:home')
#         else:
#             return render(request, 'accounts/login.html', {'error': 'The Username or/and Password did not match.'})
#     else:
#         return render(request, 'accounts/login.html')


# def logoutview(request):
#     if request.method == 'POST':
#         logout(request)
#         # return redirect('accounts:home')
#         return HttpResponseRedirect('/')


# def signup(request):
#     if request.method == 'POST':
#         if request.POST['password'] == request.POST['password2']:
#             try:
#                 user = User.objects.get(username=request.POST['username'])
#                 return render(request, 'frontpages/signup.html', {'error': 'Username already in use, Please try another.'})
#             except User.DoesNotExist:
#                 user = User.objects.create_user(first_name=request.POST['firstname'], last_name=request.POST['lastname'], email=request.POST['email'], username=request.POST['username'], password=request.POST['password'])
#                 login(request, user)
#                 return render(request, 'accounts/home.html')
#         else:
#             return render(request, 'frontpages/signup.html', {'error': 'Passwords did not match.'})
#     else:
#         return render(request, 'frontpages/signup.html')


# @login_required
# def myaccount(request):
#     return render(request, 'accounts/home.html')
