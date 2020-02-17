from django.db import models

from inoks.models import Profile
from inoks.models.CreditCard import CreditCard


class ProfileCreditCard(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    creditCard = models.ForeignKey(CreditCard, on_delete=models.CASCADE)
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi')
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')
