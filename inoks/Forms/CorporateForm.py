from django import forms
from django.forms import ModelForm

from inoks.models.Settings import Settings


class CorporateForm(ModelForm):
    class Meta:
        model = Settings
        fields = ('value',)
        widgets = {

            'value': forms.Textarea(
                attrs={'class': 'form-control ', 'required': 'required'}),
        }
