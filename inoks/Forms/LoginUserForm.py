from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms


class LoginUserForm(ModelForm):
    # confirm_password = forms.CharField( widget=forms.PasswordInput(
    #   attrs={'class': 'form-control', 'placeholder': 'Şifre Tekrarı'}))
    # email = forms.CharField(help_text=("Enter the same password as before, for verification."))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')
        widgets = {
            'first_name': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Ad', 'value': '', 'required': 'required'}),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': ' Soyad', 'required': 'required'}),

            'email': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'E-mailiniz', 'required': 'required'}),
            'password': forms.PasswordInput(
                attrs={'class': 'form-control ', 'placeholder': 'Şifreniz'}),

        }

        # User._meta.get_field_by_name('email').unique = True
        User._meta.get_field('email')._unique = True

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("This email already used")
        return data
