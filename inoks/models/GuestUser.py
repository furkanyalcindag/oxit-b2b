from django.db import models

from inoks.models import City


class GuestUser(models.Model):
    firstName = models.CharField(max_length=100, null=True, blank=True, verbose_name="Ad")
    lastName = models.CharField(max_length=100, null=True, blank=True, verbose_name="Soyad")
    email = models.EmailField()
    tc = models.CharField(max_length=11, null=True, blank=True, verbose_name='T.C. Kimlik Numarası')
    mobilePhone = models.CharField(max_length=11, null=True, blank=True, verbose_name='Telefon Numarası')
    address = models.TextField(blank=True, null=True, verbose_name='Adres')
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi')
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True, verbose_name='İl')
    district = models.TextField(blank=True, null=True, verbose_name='İlçe')
    isActive = models.BooleanField(default=False)
    isContract = models.BooleanField(default=False)
    isNotification = models.BooleanField(default=False, null=True, blank=True)


    def __str__(self):
        return '%d %s %s %s' % (self.id, '-', self.firstName, self.lastName)
