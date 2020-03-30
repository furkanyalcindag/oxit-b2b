from django import forms
from django.forms import ModelForm

from inoks.models.Discount import Discount


class DiscountForm(ModelForm):
    isDiscountReseller = forms.BooleanField(required=False)
    isDiscountCustomer = forms.BooleanField(required=False)

    class Meta:
        model = Discount
        fields = (
            'isDiscountReseller', 'isDiscountCustomer', 'discountPriceCustomer', 'discountPriceReseller',
            'creationDate',
            'finishDate',)
        widgets = {

            'creationDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right',  'id': 'datepicker2', 'name': 'creationDate',
                       }),

            'finishDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right',  'id': 'datepicker',
                       'name': 'finishDate', }),

            'discountPriceReseller': forms.NumberInput(
                attrs={'class': 'form-control ', 'placeholder': 'İndirimli Ürün Fiyatı', }),

            'discountPriceCustomer': forms.NumberInput(
                attrs={'class': 'form-control ', 'placeholder': 'İndirimli Ürün Fiyatı', }),

        }
