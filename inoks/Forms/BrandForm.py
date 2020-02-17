from django import forms
from django.forms import ModelForm

from inoks.models.Brand import Brand


class BrandForm(ModelForm):

    class Meta:
        model = Brand
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Ürün Markası', 'required': 'required'})


        }
