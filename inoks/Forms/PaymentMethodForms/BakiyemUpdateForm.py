from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms

from inoks.models import PaymentMethodBakiyem


class BakiyemUpdateForm(ModelForm):
    class Meta:
        model = PaymentMethodBakiyem
        fields = ('username', 'password', 'dealerCode','payment_type')
        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Kullanıcı Adı', 'value': '', 'required': 'required'}),

            'dealerCode': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'DealerCode', 'required': 'required'}),
            'password': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Şifreniz'}),

        }
