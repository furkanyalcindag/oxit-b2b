from django import forms
from django.forms import ModelForm

from inoks.models import Order, Product, OrderSituations, City

"""CHOICES_WITH_BLANK = (
    ('', '--------'),

)"""


class OrderForm(ModelForm):
    # product = forms.ModelChoiceField(queryset=Product.objects.all(),
    #                                to_field_name='name',
    #                               empty_label="Seçiniz",
    #                              widget=forms.Select(
    #                                 attrs={'class': 'form-control select2 select2-hidden-accessible',
    #                                        'style': 'width: 100%; '}))

    """" 'district': forms.Select(choices=CHOICES_WITH_BLANK,attrs={'class': 'form-control select2 select2-hidden-accessible',
                                           'style': 'width: 100%; ', 'id':'ilce_id'}
                 ),



                   'city': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible disabled-select',
                                        'style': 'width: 100%; ', "onChange": 'ilceGetir()'}),



                 """

    droptxt = forms.CharField(widget=forms.HiddenInput())
    isContract = forms.BooleanField(required=True)
    isGuest = forms.BooleanField(required=False)

    class Meta:
        model = Order
        fields = (
            'city', 'district', 'address',
            'payment_type',
            'isContract', 'guestUser', 'isGuest')
        widgets = {

            'city': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible disabled-select',
                                        'style': 'width: 100%; ', "onChange": 'ilceGetir()'}),

            'district': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'ilçe', 'required': 'required', 'readonly': 'readonly'}),

            'address': forms.Textarea(
                attrs={'class': 'form-control ', 'placeholder': 'Adres', 'rows': '2', 'required': 'required',
                       'readonly': 'readonly'}),

            'payment_type': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                                'style': 'width: 100%;'})

        }
