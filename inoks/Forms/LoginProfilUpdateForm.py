from django import forms
from django.forms import ModelForm

from inoks.models.Profile import Profile


class LoginProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile

        fields = ('mobilePhone',)
        widgets = {

            'mobilePhone': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Telefon Numarası', 'required': 'required', })

        }
