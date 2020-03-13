from django.db import models

from inoks.models.PaymentMethod import PaymentMethod


class PaymentMethodIyzico(models.Model):
    payment_type = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, null=True, blank=True)
    apiKey = models.CharField(max_length=100, blank=True, null=True, verbose_name='API Anahtarı')
    secretKey = models.CharField(max_length=100, null=True, blank=True, verbose_name='Güvenlik Anahtarı')

    def __str__(self):
        return '%s ' % self.apiKey
