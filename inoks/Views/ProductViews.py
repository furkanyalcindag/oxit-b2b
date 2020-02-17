from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.forms import modelformset_factory
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework.decorators import api_view

from inoks.Forms.BrandForm import BrandForm
from inoks.Forms.ImageForm import ImageForm
from inoks.Forms.ProductCategoryForm import ProductCategoryForm
from inoks.Forms.ProductForm import ProductForm
from inoks.models import Product, ProductCategory, ProductGroup
from inoks.models.Brand import Brand
from inoks.models.ProductImage import ProductImage
from inoks.serializers.product_serializers import ProductSerializer
from inoks.services import general_methods


@login_required
def return_add_products(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    product_form = ProductForm()

    # image_form = modelformset_factory(ProductImage,
    #                                 form=ImageForm, extra=4)
    durum = "EKLE"

    if request.method == 'POST':

        product_form = ProductForm(request.POST, request.FILES)

        # image_form = image_form(request.POST, request.FILES,
        # queryset=ProductImage.objects.none())

        if product_form.is_valid():

            product = Product(
                name=product_form.cleaned_data['name'],
                price=product_form.cleaned_data['price'],
                listPrice=product_form.cleaned_data['listPrice'],
                code=product_form.cleaned_data['code'],
                brand=product_form.cleaned_data['brand'],
                baseWidth=product_form.cleaned_data['baseWidth'],
                speedIndex=product_form.cleaned_data['speedIndex'],
                rimDiameter=product_form.cleaned_data['rimDiameter'],
                sectionRate=product_form.cleaned_data['sectionRate'],
                vehicleType=product_form.cleaned_data['vehicleType'],
                stock=product_form.cleaned_data['stock'],
                info=product_form.cleaned_data['info'])

            product.save()

            for f in request.FILES.getlist('input2[]'):
                productImages = ProductImage(productImage=f)
                productImages.save()
                product.productImage.add(productImages)

            product.save()

            for category in product_form.cleaned_data['category']:
                product.category.add(category)

            product.save()

            messages.success(request, 'Ürün Kaydedildi.')

            return redirect('inoks:urunler')

        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'urunler/urun-ekle.html',
                  {'product_form': product_form, 'durum': durum})


@login_required
def product_delete(request, pk):
    if request.method == 'POST' and request.is_ajax():
        try:
            obj = Product.objects.get(pk=pk)
            obj.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except Product.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def productCategory_delete(request, pk):
    if request.method == 'POST' and request.is_ajax():
        try:
            obj = ProductCategory.objects.get(pk=pk)
            obj.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except Product.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def productCategory_update(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    productCategory = ProductCategory.objects.get(id=pk)
    product_category_form = ProductCategoryForm(request.POST or None, instance=productCategory)

    if product_category_form.is_valid():
        product_category_form.save()
        messages.success(request, 'Başarıyla Güncellendi')
        return redirect('inoks:urun-kategori-ekle')
    else:
        messages.warning(request, 'Alanları Kontrol Ediniz')
    categories = ProductCategory.objects.all()
    return render(request, 'urunler/urun-kategori-ekle.html',
                  {'product_category_form': product_category_form, 'categories': categories})


@login_required
def product_update(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    product = Product.objects.get(id=pk)
    product_form = ProductForm(request.POST or None, instance=product)
    durum = "GUNCELLE"
    images = product.productImage.all()

    if request.method == 'POST':
        if product_form.is_valid():
            product.category.clear()
            for category in product_form.cleaned_data['category']:
                product.category.add(category)

            product.save()

            for f in request.FILES.getlist('input2[]'):
                productImages = ProductImage(productImage=f)
                productImages.save()
                product.productImage.add(productImages)

            product.save()

            messages.success(request, 'Başarıyla Güncellendi')

            return redirect('inoks:urun-listesi')

        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'urunler/urun-ekle.html',
                  {'product_form': product_form, 'durum': durum, 'images': images, 'product': product.pk})


@api_view()
def getProduct(request, pk):
    product = Product.objects.filter(pk=pk)

    data = ProductSerializer(product, many=True)

    responseData = {}
    responseData['product'] = data.data
    responseData['product'][0]
    return JsonResponse(responseData, safe=True)


@api_view()
def getProducts(request, pk):
    product = Product.objects.filter(pk=pk)

    data = ProductSerializer(product, many=True)

    responseData = {}
    responseData['product'] = data.data
    responseData['product'][0]
    return JsonResponse(responseData, safe=True)


@login_required
def return_product_list(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    product_list = Product.objects.all()

    return render(request, 'urunler/urun-listesi.html', {'product_list': product_list})


@login_required
def return_products(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    categories = ProductCategory.objects.all()
    urunler = Product.objects.all()

    return render(request, 'urunler/urunler.html',
                  {'kategoriler': categories, 'urunler': urunler})


@login_required
def product_image_delete(request):
    if request.POST:
        try:
            image_id = request.POST.get('image_id')
            product_id = request.POST.get('product_id')

            product = Product.objects.get(pk=product_id)
            image = ProductImage.objects.get(pk=image_id)

            product.productImage.remove(image)
            product.save()
            image.delete()

            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


@login_required
def return_add_product_category(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    product_category_form = ProductCategoryForm()

    if request.method == 'POST':

        product_category_form = ProductCategoryForm(request.POST)

        if product_category_form.is_valid():

            productCategory = ProductCategory(name=product_category_form.cleaned_data['name'])

            productCategory.save()

            return redirect('inoks:urun-kategori-ekle')

        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')
    categories = ProductCategory.objects.all()
    return render(request, 'urunler/urun-kategori-ekle.html',
                  {'product_category_form': product_category_form, 'categories': categories})


@login_required
def return_add_brand(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    brand_form = BrandForm(request.POST)
    brands = Brand.objects.all()

    if request.method == 'POST':

        if brand_form.is_valid():

            brand = Brand(name=brand_form.cleaned_data['name'])

            brand.save()

            return redirect('inoks:marka-ekle')

        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'urunler/urun-marka-ekle.html',
                  {'brand_form': brand_form, 'brands': brands})


@login_required
def brand_delete(request, pk):
    if request.method == 'POST':
        try:
            obj = Brand.objects.get(pk=pk)
            obj.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except Brand.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def add_products_to_group(request, group_id):
    group = ProductGroup.objects.get(pk=group_id)

    exist_products = Product.objects.filter(id__in=group.products.all().values('pk'))

    products = Product.objects.filter(~Q(id__in=group.products.all().values('pk')))

    if request.method == 'POST':
        for check in request.POST.getlist('check_list[]'):
            product = Product.objects.get(pk=int(check))
            group.products.add(product)
            group.save()

        messages.success(request, 'özellikler eklendi.')

        return redirect('inoks:urun-grupla', group_id)

    return render(request, 'urunler/urun-grup.html',
                  {'group': group, 'exist_products': exist_products, 'products': products})


@login_required
def delete_product_from_group(request, product_id, group_id):
    product = Product.objects.get(pk=product_id)
    group = ProductGroup.objects.get(pk=group_id)
    group.products.remove(product)
    group.save()
    messages.success(request, 'Ürün başarıyla çıkarıldı.')
    return redirect('inoks:urun-grupla', group_id)
