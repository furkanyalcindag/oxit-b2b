from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms


class UserCheckoutForm(ModelForm):
    # confirm_password = forms.CharField( widget=forms.PasswordInput(
    #   attrs={'class': 'form-control', 'placeholder': 'Şifre Tekrarı'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Adınız', 'value': '', 'required': 'required', 'readonly': 'readonly'
                       }),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': ' Soyadınız', 'required': 'required',
                       'readonly': 'readonly'
                       }),

            'email': forms.EmailInput(
                attrs={'class': 'form-control ', 'placeholder': ' Email', 'required': 'required', 'readonly': 'readonly'
                       }),

        }
