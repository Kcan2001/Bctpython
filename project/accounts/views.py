import stripe
import math

from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin, FormView
from django.views.generic.detail import SingleObjectMixin

from django.views import View
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic.detail import DetailView
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

from .models import Account, UserStripe
from trips.models import Trip, TripDate
from blog.models import Post

from .forms import SignUpForm, PaymentForm, CreateBlogPostForm
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_text
from django.template.loader import render_to_string

from .tokens import account_activation_token
from .active_campaign_api import ActiveCampaign
from django.http import HttpResponseRedirect, HttpResponseForbidden


class UserHomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/home.html'

    def get_context_data(self, **kwargs):
        context = super(UserHomePageView, self).get_context_data(**kwargs)
        context['trips'] = TripDate.objects.select_related('trip').exclude(account=self.request.user.account).order_by('arrival').all()[:5]
        # context['trips'] = Trip.objects.order_by('arrival').all()[:3]
        context['user_trips'] = TripDate.objects.filter(account=self.request.user.account, departure__gte=timezone.now())
        context['user_past_trips'] = TripDate.objects.filter(account=self.request.user.account,
                                                             departure__lt=timezone.now())[:3]
        # Will show all blog post at user profile: approved and not approved
        context['user_blog_post'] = Post.objects.filter(author=self.request.user.account)
        return context


class UserPublicView(TemplateView):
    template_name = 'accounts/public-home.html'

    def get_context_data(self, **kwargs):
        context = super(UserPublicView, self).get_context_data(**kwargs)
        # Get User Username for page kwargs
        user = get_object_or_404(User, username=self.kwargs['username'])
        # Get User Account or show 404
        context['user_profile'] = get_object_or_404(Account, id=user.account.pk)
        # Will show at public page only approved blog posts
        context['user_blog_post'] = Post.objects.filter(author=user.account.pk).exclude(is_draft=True)
        return context


class UserBlogPostCreateView(LoginRequiredMixin, CreateView):
    template_name = 'blog/create_blog_post.html'
    model = Post
    form_class = CreateBlogPostForm
    success_url = reverse_lazy('accounts:blog_post_created')

    # def get_initial(self):
    #     initial = super(UserBlogPostCreateView, self).get_initial()
    #     initial['author'] = self.request.user.account
    #     return initial
    def form_valid(self, form):
        form.instance.author = self.request.user.account
        return super().form_valid(form)


class UserBlogPostCreatedView(LoginRequiredMixin, TemplateView):
    template_name = 'blog/blog_post_created.html'


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
        # Add new user with confirmed email to Active Campaign contacts
        ActiveCampaign.sync_contact(email=user.email, first_name=user.first_name, last_name=user.last_name,
                                    tags='BC Account')
        login(request, user)
        return redirect('accounts:home')
    else:
        return render(request, 'account_activation_invalid.html')


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    # success_url = reverse_lazy('accounts:home')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse_lazy('accounts:home'))

        return super().dispatch(request, *args, **kwargs)


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


class UserMembershipView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/membership.html'

    def get_context_data(self, **kwargs):
        context = super(UserMembershipView, self).get_context_data(**kwargs)
        context['stripe_public_key'] = settings.STRIPE_PUBLIC_KEY
        return context


class UserTripDetail(View):

    def get(self, request, *args, **kwargs):
        view = UserTripDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = UserTripBookingView.as_view()
        return view(request, *args, **kwargs)


class UserTripDetailView(LoginRequiredMixin, DetailView):
    model = TripDate
    template_name = 'accounts/trip.html'
    context_object_name = 'trip'

    def get_context_data(self, **kwargs):
        context = super(UserTripDetailView, self).get_context_data(**kwargs)

        trip = TripDate.objects.get(pk=self.kwargs['pk'])
        trip_arrival_date = trip.arrival
        current_date = timezone.now().date()
        delta = (trip_arrival_date - current_date).days
        if delta < 0:
            context['time_left'] = 'expired'
        elif delta <= 60:
            context['time_left'] = 'deny'
        else:
            context['time_left'] = 'allow'

        context['form'] = PaymentForm(page_id=self.kwargs['pk'], delta=delta)
        return context


class UserTripBookingView(SingleObjectMixin, FormView):
    form_class = PaymentForm
    model = TripDate
    template_name = 'accounts/trip.html'

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            exc = form.cleaned_data['excursions']
            general_price = self.object.price
            for i in exc:
                general_price += i.price
            general_price_cents = int(general_price * 100)
            stripe.api_key = settings.STRIPE_SECRET_KEY
            # Price of website premium is 50$, amount in cents:
            # Will check if User Account already has stripe account identification:
            if hasattr(request.user.account, 'stripe_account'):
                # Get stored customer_id from previous operations:
                user_stripe_id = request.user.account.stripe_account.customer_id
                if form.cleaned_data['sub']:
                    month_payment = general_price_cents / form.cleaned_data['sub']
                    month2 = math.ceil(month_payment)
                    plan = stripe.Plan.create(name="Basic Plan", id="basic-monthly", interval="month", currency="usd", amount=month2)
                    subs = stripe.Subscription.create(customer=user_stripe_id,
                                               items=[
                                                   {
                                                       "plan": plan.stripe_id,
                                                   },
                                               ]
                                               )
                else:
                    # Making charge for amount $
                    charge = stripe.Charge.create(customer=user_stripe_id, amount=general_price_cents, currency='usd',
                                                  description='Payment for tour')
                # paid = charge.paid
                # status = charge.status
                # If charge was successful:
                if subs.status == 'active':
                    # self.object.entry_set.add(request.user.account)
                    user = request.user.account
                    trip = self.object
                    user.trips.add(trip)
                return redirect('accounts:home')
            else:
                # If request.user has not customer instance in stripe database will create it:
                customer = stripe.Customer.create(email=request.user.email, source=request.POST['stripeToken'])
                # Then will add stripe customer id to our request user (OneToOne Relation)
                UserStripe.objects.get_or_create(user_id=request.user.account.id, customer_id=customer.id)
                # After stripe_account was created will try to make a charge
                charge = stripe.Charge.create(customer=customer.id, amount=amount, currency='usd',
                                              description='Payment for premium membership')
                # paid = charge.paid
                # status = charge.status
                # If charge was successful:
                if charge.status == 'succeeded':
                    user = request.user.account
                    trip = self.object
                    user.trips.add(trip)
                return redirect('accounts:home')
            return self.form_valid(form)
        else:
            a = form.errors
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('accounts:home')

    def get_form_kwargs(self):
        kwargs = super(UserTripBookingView, self).get_form_kwargs()
        kwargs['page_id'] = self.kwargs['pk']

        trip = TripDate.objects.get(pk=self.kwargs['pk'])
        trip_arrival_date = trip.arrival
        current_date = timezone.now().date()
        delta = (trip_arrival_date - current_date).days

        kwargs['delta'] = delta
        return kwargs


# class UserTripDetailView(LoginRequiredMixin, FormMixin, DetailView):
#     model = TripDate
#     form_class = PaymentForm
#     template_name = 'accounts/trip.html'
#     context_object_name = 'trip'
#
#     def get_context_data(self, **kwargs):
#         context = super(UserTripDetailView, self).get_context_data(**kwargs)
#         trip = TripDate.objects.get(pk=self.kwargs['pk'])
#         trip_arrival_date = trip.arrival
#         current_date = timezone.now().date()
#         delta = (trip_arrival_date - current_date).days
#         if delta <= 20:
#             context['time_left'] = 'You need to pay entire sum'
#         else:
#             context['time_left'] = 'allow'
#         return context
#
#     def get_form_kwargs(self):
#         kwargs = super(UserTripDetailView, self).get_form_kwargs()
#         kwargs.update({'page_id': self.kwargs['pk']})
#         return kwargs

# def usertripdetail(request, pk):
#     if request.method == 'POST':
#         form = PaymentForm(request.POST)
#         if form.is_valid():
#             print('all is ok')
#             return redirect('accounts:home')
#     else:
#         trip_page_id = pk
#         form = PaymentForm(page_id=trip_page_id)
#         print('need to send form')
#     return render(request, 'accounts/trip2.html', {'form': form})


def membership_payment(request):
    # Will accept only post request to our view
    if request.method == 'POST':
        stripe.api_key = settings.STRIPE_SECRET_KEY
        # Price of website premium is 50$, amount in cents:
        amount = 5000
        # Will check if User Account already has stripe account identification:
        if hasattr(request.user.account, 'stripe_account'):
            # Get stored customer_id from previous operations:
            user_stripe_id = request.user.account.stripe_account.customer_id
            # Making charge for amount $
            charge = stripe.Charge.create(customer=user_stripe_id, amount=amount, currency='usd',
                                          description='Payment for premium membership for real user')
            # paid = charge.paid
            # status = charge.status
            # If charge was successful:
            if charge.status == 'succeeded':
                # Add premium access for paid user
                request.user.account.is_membership = True
                request.user.save()
                # And add new tag in Active Campaign service
                ActiveCampaign.sync_contact(email=request.user.email, first_name=request.user.first_name,
                                            last_name=request.user.last_name, tags='BC Member')
            return redirect('accounts:home')
        else:
            # If request.user has not customer instance in stripe database will create it:
            customer = stripe.Customer.create(email=request.user.email, source=request.POST['stripeToken'])
            # Then will add stripe customer id to our request user (OneToOne Relation)
            UserStripe.objects.get_or_create(user_id=request.user.account.id, customer_id=customer.id)
            # After stripe_account was created will try to make a charge
            charge = stripe.Charge.create(customer=customer.id, amount=amount, currency='usd',
                                          description='Payment for premium membership')
            # paid = charge.paid
            # status = charge.status
            # If charge was successful:
            if charge.status == 'succeeded':
                # Add premium access for paid user
                request.user.account.is_membership = True
                request.user.save()
                # And add new tag in Active Campaign service
                ActiveCampaign.sync_contact(email=request.user.email, first_name=request.user.first_name,
                                            last_name=request.user.last_name, tags='BC Member')
                return redirect('accounts:home')
        return redirect('accounts:home')


def trip_payment(request):
    # Will accept only post request to our view
    if request.method == 'POST':
        stripe.api_key = settings.STRIPE_SECRET_KEY
        # Price of website premium is 50$, amount in cents:
        amount = 5000
        # Will check if User Account already has stripe account identification:
        if hasattr(request.user.account, 'stripe_account'):
            # Get stored customer_id from previous operations:
            user_stripe_id = request.user.account.stripe_account.customer_id
            # Making charge for amount $
            charge = stripe.Charge.create(customer=user_stripe_id, amount=amount, currency='usd',
                                          description='Payment for premium membership for real user')
            # paid = charge.paid
            # status = charge.status
            # If charge was successful:
            if charge.status == 'succeeded':
                # Add premium access for paid user
                request.user.account.is_membership = True
                request.user.save()
                # And add new tag in Active Campaign service
                ActiveCampaign.sync_contact(email=request.user.email, first_name=request.user.first_name,
                                            last_name=request.user.last_name, tags='BC Member')
            return redirect('accounts:home')
        else:
            # If request.user has not customer instance in stripe database will create it:
            customer = stripe.Customer.create(email=request.user.email, source=request.POST['stripeToken'])
            # Then will add stripe customer id to our request user (OneToOne Relation)
            UserStripe.objects.get_or_create(user_id=request.user.account.id, customer_id=customer.id)
            # After stripe_account was created will try to make a charge
            charge = stripe.Charge.create(customer=customer.id, amount=amount, currency='usd',
                                          description='Payment for premium membership')
            # paid = charge.paid
            # status = charge.status
            # If charge was successful:
            if charge.status == 'succeeded':
                # Add premium access for paid user
                request.user.account.is_membership = True
                request.user.save()
                # And add new tag in Active Campaign service
                ActiveCampaign.sync_contact(email=request.user.email, first_name=request.user.first_name,
                                            last_name=request.user.last_name, tags='BC Member')
                return redirect('accounts:home')
        return redirect('accounts:home')




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
