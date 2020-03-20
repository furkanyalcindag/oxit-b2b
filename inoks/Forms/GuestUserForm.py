from django import forms
from django.forms import ModelForm
from inoks.models.GuestUser import GuestUser

CHOICES_WITH_BLANK = (
    ('', '--------'),

)


class GuestUserForm(ModelForm):
    isContract = forms.BooleanField(required=True)
    isNotification = forms.BooleanField(required=False)

    class Meta:
        model = GuestUser
        fields = ('city', 'district', 'address',
                  'isContract', 'firstName', 'lastName', 'tc', 'mobilePhone', 'email')
        widgets = {
            'firstName': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Ad', 'rows': '2', 'required': 'required',
                       }),
            'lastName': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Soyad', 'rows': '2', 'required': 'required', }),

            'tc': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'T.C. Kimlik Numarası', 'required': 'required',
                       'maxlength': '11', 'minlength': '11'}),

            'city': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%;', "onChange": 'ilceGetir()'}),

            'district': forms.Select(choices=CHOICES_WITH_BLANK,
                                     attrs={'class': 'form-control select2 select2-hidden-accessible',
                                            'style': 'width: 100%; ', 'id': 'ilce_id'}
                                     ),

            'address': forms.Textarea(
                attrs={'class': 'form-control ', 'placeholder': 'Açık Adres', 'required': 'required',
                       'style': 'width: 100%;' 'height:50%', }),

            'mobilePhone': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Telefon Numarası', 'required': 'required',
                       'maxlength': '10', 'minlength': '10'}),
            'email': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'abc@abc.com', 'required': 'required',
                       }),

        }
