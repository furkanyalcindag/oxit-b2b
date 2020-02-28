from django import forms
from django.forms import ModelForm

from inoks.models import ProductCategory


class ProductCategoryForm(ModelForm):

    class Meta:
        model = ProductCategory
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Ürün Kategori Adı', 'required': 'required'}),



        }
