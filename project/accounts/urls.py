from django.conf.urls import url
from . import views

app_name = 'accounts'

urlpatterns = [
    # Account home page
    url(r'^$', views.UserHomePageView.as_view(), name='home'),
    url(r'^membership/$', views.UserMembershipView.as_view(), name='membership'),
    url(r'^membership/payment/$', views.membership_payment, name='membership_payment'),

    url(r'^trip/(?P<pk>[-\w]+)/$', views.UserTripDetailView.as_view(), name='trip'),
    url(r'^trip/$', views.usertripdetail, name='trip2'),
    # User sign up and account activation via email address
    url(r'^signup/', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^account-activation-sent/$', views.account_activation_sent, name='account_activation_sent'),

    # Login and Logout pages for account
    url(r'^login/$', views.UserLoginView.as_view(), name='login'),
    url(r'^logout/$', views.UserLogoutView.as_view(), name='logout'),

    # Update pages for User and Account models
    url(r'^update-account/$', views.AccountUpdate.as_view(), name='update_account'),
    url(r'^update-user/$', views.UserUpdate.as_view(), name='update_user'),

    # URLs for password change. password_change - page with form to input old password.
    url(r'^password-change/$', views.UserPasswordChangeView.as_view(), name='password_change'),
    url(r'^password-change-done/$', views.UserPasswordChangeDoneView.as_view(), name='password_change_done'),

    # URLs for password reset ('forgot password' functionality). _reset and _confirm - pages with forms
    url(r'^password-reset/$', views.UserPasswordResetView.as_view(), name='password_reset'),
    url(r'^password-reset-done/$', views.UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    url(r'^password-reset-confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.UserPasswordResetConfirm.as_view(), name='password_reset_confirm'),
    url(r'^password-reset-complete/$', views.UserPasswordResetComplete.as_view(), name='password_reset_complete'),

]
