from django import forms
from django.forms import ModelForm

from inoks.models.Profile import Profile

CHOICES_WITH_BLANK = (
    ('', '--------'),

)


class ProfileForm(ModelForm):
    isContract = forms.BooleanField(required=True)
    isNotification = forms.BooleanField(required=False)

    class Meta:
        model = Profile

        fields = (
            'profileImage', 'mobilePhone', 'gender', 'tc', 'birthDate', 'city',
            'district', 'isContract', 'isNotification')
        widgets = {

            'mobilePhone': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Telefon Numarası', 'required': 'required',
                       'maxlength': '10', 'minlength': '10'}),
            'gender': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%;', 'required': 'required'}),
            'tc': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'T.C. Kimlik Numarası', 'required': 'required',
                       'maxlength': '11', 'minlength': '11'}),

            'birthDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'type': 'date', 'autocomplete': 'off',
                       }),

            'city': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%; ', 'required': 'required', "onChange": 'ilceGetir()'}),

            'district': forms.Select(choices=CHOICES_WITH_BLANK,
                                     attrs={'class': 'form-control select2 select2-hidden-accessible',
                                            'style': 'width: 100%; ', 'id': 'ilce_id'}
                                     ),

        }
