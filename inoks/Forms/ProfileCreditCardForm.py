from django import forms
from django.forms import ModelForm

from inoks.models.CreditCard import CreditCard


class ProfileCreditCardForm(ModelForm):
    class Meta:
        model = CreditCard
        fields = ('name', 'cvv', 'card_name_lastName', 'cartNumber',)
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Kart Adı'}),
            'cvv': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'CVV' }),
            'cartNumber': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Kart Numarası'}),
            'card_name_lastName': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Kişi Adı Soyadı'}),

        }
