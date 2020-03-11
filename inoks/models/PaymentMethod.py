from django.db import models


class PaymentMethod(models.Model):
    name = models.CharField(max_length=100, verbose_name='Ödeme Yöntemi', null=True, blank=True)
    isActive = models.BooleanField(default=False)


    def __str__(self):
        return '%s ' % self.name
