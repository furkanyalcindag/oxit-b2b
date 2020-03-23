from django import forms
from django.forms import ModelForm

from inoks.models import RefundSituations, Refund, Product


class RefundForm(ModelForm):

    refundSituations = forms.ModelChoiceField(queryset=RefundSituations.objects.all(),
                                              to_field_name='name',
                                              empty_label="Seçiniz",
                                              widget=forms.Select(
                                                  attrs={'class': 'form-control select2 select2-hidden-accessible',
                                                         'style': 'width: 100%; '}))

    product = forms.ModelChoiceField(queryset=Product.objects.exclude(name__icontains="paket"),
                                     to_field_name='name',
                                     empty_label="Seçiniz",
                                     widget=forms.Select(
                                         attrs={'class': 'form-control select2 select2-hidden-accessible',
                                                'style': 'width: 100%; '}))

    class Meta:
        model = Refund
        fields = (
            'order', 'product', 'orderQuantity', 'isOpen', 'refundSituations')
        labels = {
            'isOpen': 'Ürün Kullanıldı Mı?',
            'refundSituations': 'İade Durumları?',

        }

        widgets = {
            'order': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Sipariş Numarası', 'required': 'required'}),
            'product': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                           'style': 'width: 100%; '}),

            'orderQuantity': forms.NumberInput(
                attrs={'class': 'form-control ', 'min': '1', 'placeholder': 'Ürün Miktarı', 'required': 'required'}),

            'isOpen': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%;'})

        }
