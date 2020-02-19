from django import forms
from django.forms import ModelForm

from inoks.models.Settings import Settings


class CommunicationForm(ModelForm):
    class Meta:
        model = Settings
        fields = ('value',)
        widgets = {

            'value': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required'}),
        }
