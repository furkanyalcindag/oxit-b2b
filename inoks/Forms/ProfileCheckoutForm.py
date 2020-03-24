from django import forms
from django.forms import ModelForm

from inoks.models.Profile import Profile


class ProfileCheckoutForm(ModelForm):
    isContract = forms.BooleanField(required=True)
    isNotification = forms.BooleanField(required=False)
    class Meta:
        model = Profile

        fields = ('mobilePhone',)
        widgets = {

            'mobilePhone': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Telefon Numarası', 'readonly': 'readonly', })

        }
