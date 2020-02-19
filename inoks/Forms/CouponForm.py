from django import forms
from django.forms import ModelForm

from inoks.models.Coupon import Coupon


class CouponForm(ModelForm):
    class Meta:
        model = Coupon
        fields = ('name', 'code', 'creationDate', 'finishDate', 'discountAmount')
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Kupon Adı', 'required': 'required'}),

            'code': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Kupon Kodu', 'required': 'required'}),

            'creationDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'type': 'date', 'autocomplete': 'off',
                       }),

            'finishDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'type': 'date', 'autocomplete': 'off'}),

            'discountAmount': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'İndirim Miktarı', 'required': 'required'})

        }
