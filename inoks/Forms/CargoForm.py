from django import forms
from django.forms import ModelForm

from inoks.models.Brand import Brand
from inoks.models.Cargo import Cargo


class CargoForm(ModelForm):
    status: forms.BooleanField(required=True)
    class Meta:
        model = Cargo
        fields = ('name', 'lower_limit', 'price', 'status',)
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Ürün Markası', 'required': 'required'}),
            'lower_limit': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Minimum Sipariş Fiyatı', 'required': 'required'}),
            'price': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Kargo Ücreti', 'required': 'required'}),


        }
