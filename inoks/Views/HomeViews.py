from django.contrib import messages
from django.db.models import Count, Q
from django.shortcuts import render

from inoks.models import ProductCategory, Product, ProductGroup
from inoks.models.Brand import Brand


def get_home_product(request):
    products = Product.objects.order_by('-creationDate')[:20]
    brands = Brand.objects.all()
    categories = ProductCategory.objects.all()

    return render(request, 'home/home.html',
                  {'products': products, 'brands': brands, 'categories': categories})





def get_category_products(request, pk):
    category = ProductCategory.objects.get(pk=pk)
    products = category.product_set.all()
    cat = ProductCategory.objects.all()
    brands = Brand.objects.all()

    return render(request, 'home/get-category-products.html',
                  {'products': products, 'categories': cat, 'brands': brands})


def get_brand_products(request, pk):
    brand = Brand.objects.get(pk=pk)
    products = brand.product_set.all()
    brands = Brand.objects.all()

    cat = ProductCategory.objects.all()
    return render(request, 'home/get-brand-products.html',
                  {'products': products, 'categories': cat, 'brands': brands})


def get_product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    group = ProductGroup.objects.get(name="Önerilen Ürünler")
    return render(request, 'home/product-detail.html',
                  {'product': product, 'group': group})


def search_category(request):
    categories = ProductCategory.objects.all()
    brands = Brand.objects.all()
    products = ''
    if request.method == 'POST':
        # category = ProductCategory.objects.filter(pk=int(request.POST['cat']))
        products = Product.objects.filter(category__in=[ProductCategory.objects.get(pk=int(request.POST['cat']))],
                                          name__icontains=request.POST['name'])

        messages.warning(request, 'Kayıt Bulunamadı')

    return render(request, 'home/get-category-products.html',
                  {'products': products, 'categories': categories, 'brands': brands})
