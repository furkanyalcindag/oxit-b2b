from django import forms
from django.forms import ModelForm

from inoks.models.Address import Address
from inoks.models.CreditCard import CreditCard

CHOICES_WITH_BLANK = (
    ('', '--------'),

)

class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = ('name', 'address', 'city', 'district',)
        widgets = {
            'name': forms.Select(
                attrs={'class': 'form-control select2 select2-hidden-accessible ', 'placeholder': 'Adress Başlığı'}),
            'address': forms.Textarea(
                attrs={'class': 'form-control ', 'style': 'width: 100%;height:50px ', 'placeholder': 'Açık Adres'}),

            'city': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%; ',  "onChange": 'ilceGetir()'}),

            'district': forms.Select(choices=CHOICES_WITH_BLANK,
                                     attrs={'class': 'form-control select2 select2-hidden-accessible',
                                            'style': 'width: 100%; ', 'id': 'ilce_id'}
                                     ),

        }
