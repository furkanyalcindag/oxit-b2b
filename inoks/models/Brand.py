from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=256, blank=True, null=True, verbose_name='Ürün Markası')

    def __str__(self):
        return '%s ' % self.name

