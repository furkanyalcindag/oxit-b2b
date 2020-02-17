from django.db import models


class Cargo(models.Model):
    name = models.CharField(max_length=256, blank=True, null=True, verbose_name='Kargo Adı')
    lower_limit = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Kargo Limiti')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Kargo Ücreti')
    status = models.BooleanField(default=False, verbose_name='Kargo Durumu')

    def __str__(self):
        return '%s ' % self.name
