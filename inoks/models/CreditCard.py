from django.db import models


class CreditCard(models.Model):
    name = models.CharField(max_length=256, blank=True, null=True, verbose_name='Kredi Kartı')
    cartNumber = models.TextField(blank=True, null=True, verbose_name='Kart Numarası')
    cvv = models.CharField(max_length=255, null=True, blank=True, verbose_name="CVV")
    card_name_lastName = models.TextField(blank=True, null=True, verbose_name='Kart ad soyad')

    def __str__(self):
        return '%s ' % self.name
