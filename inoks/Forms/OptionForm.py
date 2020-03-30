from django import forms
from django.forms import ModelForm

from inoks.models import Option


class OptionForm(ModelForm):
    class Meta:
        model = Option
        fields = ('type_name', 'type',)
        widgets = {
            'type_name': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Seçenek Adı', 'required': 'required'}),
            'type': forms.Select(
                attrs={'class': 'form-control select2 select2-hidden-accessible',
                       'style': 'width: 100%;', 'required': 'required', 'id': 'option_type'}),


        }
