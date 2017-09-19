from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from trips.models import TripDate, Excursion
from blog.models import Post

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class CreateBlogPostForm(ModelForm):
    title = forms.CharField(max_length=200)
    text = forms.CharField(widget=CKEditorUploadingWidget(config_name='blog'))

    class Meta:
        model = Post
        fields = ('category', 'title', 'text')


class PaymentForm(forms.Form):
    excursions = forms.ModelMultipleChoiceField(queryset=None, required=False, to_field_name='title', widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        self.trip = kwargs.pop('page_id', None)
        delta = kwargs.pop('delta', None)
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.fields['excursions'].queryset = Excursion.objects.filter(trip=self.trip)
        a = self.fields['excursions']
        # TODO count how much months normally
        delta_months = delta / 30
        months = int(delta_months)
        if delta >= 60:
            self.fields['subscription'] = forms.IntegerField(min_value=1, max_value=months, required=False)
            self.fields['subscription'].widget.attrs['class'] = 'bc-input-number'

        pass
