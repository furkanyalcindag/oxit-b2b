from django import forms
from django.forms import ModelForm

from inoks.models import Order, Product, OrderSituations


class OrderForm(ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.all(),
                                     to_field_name='name',
                                     empty_label="Seçiniz",
                                     widget=forms.Select(
                                         attrs={'class': 'form-control select2 select2-hidden-accessible',
                                                'style': 'width: 100%; '}))

    order_situations = forms.ModelChoiceField(queryset=OrderSituations.objects.all(),
                                              to_field_name='name',
                                              empty_label="Seçiniz",
                                              widget=forms.Select(
                                                  attrs={'class': 'form-control select2 select2-hidden-accessible',
                                                         'style': 'width: 100%; '}))

    class Meta:
        model = Order
        fields = (
            'profile', 'product', 'quantity', 'city', 'district', 'address', 'sponsor',
            'payment_type',
            'isContract',)
        widgets = {
            'profile': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                           'style': 'width: 100%; '}),

            'quantity': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Miktar', 'required': 'required'}),

            'city': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%; '}),

            'district': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                            'style': 'width: 100%; '}),

            'address': forms.Textarea(
                attrs={'class': 'form-control ', 'placeholder': 'Adres', 'rows': '2', 'required': 'required'}),

            'sponsor': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Sponsor', 'required': 'required'}),

            'payment_type': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                                'style': 'width: 100%;'})

        }

        def __init__(self, *args, **kwargs):
            # Only in case we build the form from an instance
            # (otherwise, 'toppings' list should be empty)

            if not kwargs.get('instance'):
                # We get the 'initial' keyword argument or initialize it
                # as a dict if it didn't exist.
                initial = kwargs.setdefault('initial', {})
                # The widget for a ModelMultipleChoiceField expects
                # a list of primary key for the selected data.
                initial['category'] = [t.pk for t in kwargs['instance'].category.all()]
