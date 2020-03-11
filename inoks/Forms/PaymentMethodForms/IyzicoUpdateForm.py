
from django.forms import ModelForm
from django import forms

from inoks.models import PaymentMethodIyzico


class IyzicoUpdateForm(ModelForm):

    class Meta:
        model = PaymentMethodIyzico
        fields = ('apiKey', 'secretKey','payment_type')
        widgets = {
            'apiKey': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Api Anahtarı', 'value': '', 'required': 'required'}),
            'secretKey': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': ' Güvenlik Anahtarı', 'required': 'required'}),

        }
