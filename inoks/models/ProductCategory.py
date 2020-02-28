from django.db import models
from django.template.defaultfilters import slugify


class ProductCategory(models.Model):
    name = models.TextField(max_length=18500, blank=True, null=True, verbose_name='Ürün Kategorisi')
    slug = models.SlugField(null=True, unique=True)

    def __str__(self):
        return '%s ' % self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)