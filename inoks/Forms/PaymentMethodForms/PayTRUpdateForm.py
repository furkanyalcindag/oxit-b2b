
from inoks.models.PaymentMethodPayTR import PaymentMethodPayTR
from django import forms
from django.forms import ModelForm

class PayTRUpdateForm(ModelForm):
    class Meta:
        model = PaymentMethodPayTR
        fields = ('merchantId', 'merchantKey', 'merchantSalt', 'payment_type',)
        widgets = {
            'merchantKey': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Merchant Key', 'value': '', 'required': 'required'}),
            'merchantId': forms.NumberInput(
                attrs={'class': 'form-control ', 'placeholder': ' Merchant Id', 'required': 'required'}),

            'merchantSalt': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Merchant Salt', 'required': 'required'}),
            'payment_type': forms.Select(
                attrs={'class': 'form-control select2 select2-hidden-accessible','style': 'width: 100%; ',
                       'required': 'required'}),


        }
