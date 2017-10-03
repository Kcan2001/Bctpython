from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from trips.models import TripDate, Excursion, TripFlightCost
from blog.models import Post

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def clean_email(self):
        get_email = self.cleaned_data['email']
        if User.objects.filter(email=get_email).exists():
            raise forms.ValidationError('This address already used by another user.')
        return get_email


class UpdateUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class CreateBlogPostForm(ModelForm):
    title = forms.CharField(max_length=200)
    text = forms.CharField(widget=CKEditorUploadingWidget(config_name='blog'))

    class Meta:
        model = Post
        fields = ('category', 'title', 'text')


class PaymentForm(forms.Form):
    excursions = forms.ModelMultipleChoiceField(queryset=None, required=False, to_field_name='price',
                                                widget=forms.CheckboxSelectMultiple(
                                                    attrs={'class': 'mdl-checkbox__input'}))
    flight_cost = forms.ModelChoiceField(queryset=None, required=False, empty_label='No Flights Included')

    def __init__(self, *args, **kwargs):
        self.trip = kwargs.pop('page_id', None)
        delta = kwargs.pop('delta', None)
        super(PaymentForm, self).__init__(*args, **kwargs)
        # Query for flight costs and put in to select field
        q = TripDate.objects.filter(pk=self.trip).get()
        self.fields['flight_cost'].queryset = TripFlightCost.objects.filter(trip=q.trip.pk)
        # Query for excursions
        self.fields['excursions'].queryset = Excursion.objects.filter(trip=self.trip)
        a = self.fields['excursions']
        delta_months = delta / 30
        months = int(delta_months)
        if delta >= 60:
            self.fields['subscription'] = forms.IntegerField(min_value=1, max_value=months, required=False)
            self.fields['subscription'].widget.attrs['class'] = 'bc-input-number'
