from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from trips.models import TripDate, Excursion

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class PaymentForm(forms.Form):
    name = forms.CharField(required=False, help_text='for test')
    excursions = forms.ModelMultipleChoiceField(queryset=Excursion.objects.filter(), widget=forms.CheckboxSelectMultiple)
    token_igor = forms.CharField(required=False, widget=forms.HiddenInput())
