from django import forms
from django.forms import ModelForm

from inoks.models.Profile import Profile


class LoginProfilForm(ModelForm):
    isContract = forms.BooleanField(required=True)
    isNotification = forms.BooleanField(required=True)
    class Meta:
        model = Profile

        fields = ('mobilePhone',)
        widgets = {

            'mobilePhone': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Telefon Numarası', 'required': 'required', })

        }
