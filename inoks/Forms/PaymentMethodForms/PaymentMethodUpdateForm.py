from django.forms import ModelForm
from django import forms

from inoks.models.PaymentMethod import PaymentType


class PaymentTypeForm(ModelForm):
    isActive = forms.BooleanField(required=True)

    class Meta:
        model = PaymentType
        fields = ('name', 'isActive')
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Yöntem', 'value': '', 'required': 'required'}),

        }
