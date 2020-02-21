from django.db import models

from inoks.models import City, District
from inoks.models.Enum import ADDRESS_CHOISES, ADDRESS1


class Address(models.Model):
    name = models.CharField(max_length=256, blank=True, null=True, verbose_name='Adres Başlığı',
                            choices=ADDRESS_CHOISES,
                            default=ADDRESS1)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True,
                             verbose_name='İl')
    district = models.TextField(blank=True, null=True, verbose_name='İlçe')
    address = models.TextField(blank=True, null=True, verbose_name='Açık Adres')

    def __str__(self):
        return '%s ' % self.name
