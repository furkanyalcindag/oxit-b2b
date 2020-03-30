import datetime

from django.db import models
from django.template.defaultfilters import slugify


from inoks.models.ProductImage import ProductImage
from inoks.models.ProductCategory import ProductCategory
from inoks.models.Brand import Brand
from inoks.models.Enum import SPEED_CHOISES, VEHICLE_CHOISES


class Product(models.Model):
    productImage = models.ManyToManyField(ProductImage, null=True, blank=True, verbose_name='Ürün Resmi')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='Marka', null=True, blank=True)
    code = models.CharField(max_length=100, blank=True, null=True, verbose_name='Ürün Kodu')
    name = models.TextField(blank=True, null=True, verbose_name='Ürün Adı')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    listPrice = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Ürün Liste Fiyatı', null=True,
                                    blank=True)

    stock = models.IntegerField(blank=True, null=True, verbose_name='Stok Adedi')

    category = models.ManyToManyField(ProductCategory, null=True, blank=True, verbose_name='Kategori')

    info = models.TextField(blank=True, null=True, verbose_name='Ürün Bilgileri')
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi')
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')


    vehicleType = models.CharField(null=True, blank=True, max_length=100, verbose_name='Araç Tipi',
                                   choices=VEHICLE_CHOISES)
    baseWidth = models.IntegerField(blank=True, null=True, verbose_name='Taban Genişliği')
    sectionRate = models.IntegerField(blank=True, null=True, verbose_name='Kesit Oranı')
    rimDiameter = models.IntegerField(blank=True, null=True, verbose_name='Jant Çapı')
    speedIndex = models.CharField(null=True, blank=True, verbose_name='Hız Endeksi', max_length=100,
                                  choices=SPEED_CHOISES)
    slug = models.SlugField(null=True, unique=True)
    isActive = models.BooleanField(default=True)

    def getDiscountHome(self):
        datetime_current = datetime.datetime.today()
        from inoks.models.Discount import Discount
        discount_product = Discount.objects.filter(product_id=self.id).filter(
            creationDate__lte=datetime_current).filter(finishDate__gte=datetime_current).filter(isDiscountCustomer=True)
        if discount_product.count() > 0:
            return discount_product[0].discountPriceCustomer
        else:
            return 0

    def __str__(self):
        return '%s ' % self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
