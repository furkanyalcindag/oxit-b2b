from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms

from inoks.models.GuestUser import GuestUser


class GuestCheckoutForm(ModelForm):
    # confirm_password = forms.CharField( widget=forms.PasswordInput(
    #   attrs={'class': 'form-control', 'placeholder': 'Şifre Tekrarı'}))

    class Meta:
        model = GuestUser
        fields = ('firstName', 'lastName', 'email', 'mobilePhone', 'city', 'district', 'address', 'tc',)
        widgets = {
            'firstName': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '', 'required': 'required',
                       'readonly': 'readonly',
                       }),
            'lastName': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required',
                       'readonly': 'readonly'
                       }),

            'email': forms.EmailInput(
                attrs={'class': 'form-control ', 'readonly': 'readonly'
                       }),
            'mobilePhone': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '',
                       'readonly': 'readonly', }),
            'city': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '',
                       'readonly': 'readonly', }),

            'district': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '',
                       'readonly': 'readonly', }),
            'address': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '',
                       'readonly': 'readonly', }),
            'tc': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '',
                       'readonly': 'readonly', }),

        }
