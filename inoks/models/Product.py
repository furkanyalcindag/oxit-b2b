from django.db import models
from django.template.defaultfilters import slugify

from inoks.models.ProductImage import ProductImage
from inoks.models.ProductCategory import ProductCategory
from inoks.models.Brand import Brand
from inoks.models.Enum import OLCU_CHOISES, OLCU, SPEED_CHOISES, VEHICLE_CHOISES


class Product(models.Model):
    productImage = models.ManyToManyField(ProductImage, null=True, blank=True, verbose_name='Ürün Resmi')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='Marka', null=True, blank=True)
    code = models.CharField(max_length=100, blank=True, null=True, verbose_name='Ürün Kodu')
    name = models.TextField(blank=True, null=True, verbose_name='Ürün Adı')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    listPrice = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Ürün Liste Fiyatı', null=True,
                                    blank=True)
    discountPrice = models.CharField(max_length=120, blank=True, null=True, verbose_name='İndirimli Fiyatı')
    stock = models.IntegerField(blank=True, null=True, verbose_name='Stok Adeti')

    category = models.ManyToManyField(ProductCategory, null=True, blank=True, verbose_name='Kategori')
    discountStartDate = models.DateField(blank=True, null=True, verbose_name='İndirim Başlama Tarihi')
    discountFinishDate = models.DateField(null=True, blank=True, verbose_name='İndirim Bitiş Tarihi')
    info = models.TextField(blank=True, null=True, verbose_name='Ürün Bilgileri')
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi')
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')
    product_size = models.CharField(max_length=120, null=True, blank=True, verbose_name="Ürün Ölçüsü",
                                    choices=OLCU_CHOISES,
                                    default=OLCU)

    vehicleType = models.CharField(null=True, blank=True, max_length=100, verbose_name='Araç Tipi',
                                   choices=VEHICLE_CHOISES)
    baseWidth = models.IntegerField(blank=True, null=True, verbose_name='Taban Genişliği')
    sectionRate = models.IntegerField(blank=True, null=True, verbose_name='Kesit Oranı')
    rimDiameter = models.IntegerField(blank=True, null=True, verbose_name='Jant Çapı')
    speedIndex = models.CharField(null=True, blank=True, verbose_name='Hız Endeksi', max_length=100,
                                  choices=SPEED_CHOISES)
    slug = models.SlugField(null=True, unique=True)
    isActive = models.BooleanField(default=True)


    def __str__(self):
        return '%s ' % self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
