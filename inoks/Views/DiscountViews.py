from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from inoks.Forms.DiscountForm import DiscountForm
from inoks.models import Product
from inoks.models.Discount import Discount

@login_required
def discount(request, pk): #İndirim uygulama
    product = Product.objects.get(pk=pk)
    discountProduct = Discount.objects.filter(product_id=product.pk)

    discountForm = DiscountForm()
    if not discountProduct:

        discountForm = DiscountForm(request.POST)

        if request.method == 'POST':
            if discountForm.is_valid():
                discountProduct = Discount(discountPriceCustomer=discountForm.cleaned_data['discountPriceCustomer'],
                                           discountPriceReseller=discountForm.cleaned_data['discountPriceReseller'],
                                           isDiscountCustomer=discountForm.cleaned_data['isDiscountCustomer'],
                                           finishDate=discountForm.cleaned_data['finishDate'],
                                           creationDate=discountForm.cleaned_data['creationDate'])
                discountProduct.product = product
                discountProduct.save()
                discountProduct.isDiscountReseller = discountForm.cleaned_data['isDiscountReseller']
                discountProduct.save()
                messages.success(request, 'İndirim Başarıyla Uygulandı.')
            else:
                messages.warning(request, 'Alanları Kontrol Edin.')
    else:
        discountProduct = Discount.objects.get(product=product)
        discountForm = DiscountForm(request.POST or None, instance=discountProduct)
        if request.method == 'POST':

            if discountForm.is_valid():
                discountForm.save()

            messages.success(request, 'İndirim Başarıyla Güncellendi.')

        return render(request, 'urunler/urun-indirim-uygula.html', {'product': product, 'form': discountForm})

    return render(request, 'urunler/urun-indirim-uygula.html', {'product': product, 'form': discountForm})

@login_required
def getDiscount_products(request):  #indirimli ürünleri göster
    products = Discount.objects.all()
    return render(request, 'urunler/indirimli-urunler.html', {'products': products})

@login_required
def discount_product_delete(request, pk): #indirim sil
    if request.method == 'POST' and request.is_ajax():
        try:
            obj = Discount.objects.get(pk=pk)
            obj.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except Product.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})

