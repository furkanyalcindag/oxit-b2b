from django.contrib import messages
from django.db.models import Count, Q
from django.shortcuts import render

from inoks.filters.ProductFilter import ProductFilter
from inoks.models import ProductCategory, Product, ProductGroup
from inoks.models.Brand import Brand


def get_home_product(request):
    products = Product.objects.filter(isActive=1).order_by('-creationDate')[:20]

    brands = Brand.objects.all()
    categories = ProductCategory.objects.all()

    return render(request, 'home/home.html',
                  {'products': products, 'brands': brands, 'categories': categories})


def get_category_products(request, slug):
    category = ProductCategory.objects.get(slug=slug)
    products = category.product_set.all()
    cat = ProductCategory.objects.all()
    brands = Brand.objects.all()

    return render(request, 'home/get-category-products.html',
                  {'products': products, 'categories': cat, 'brands': brands, 'category': category})


def get_brand_products(request, slug):
    brand = Brand.objects.get(slug=slug)
    products = brand.product_set.all()
    brands = Brand.objects.all()

    cat = ProductCategory.objects.all()
    return render(request, 'home/get-brand-products.html',
                  {'products': products, 'categories': cat, 'brands': brands, 'brand': brand})


def get_product_detail(request, slug):
    product = Product.objects.get(slug=slug)
    group = ProductGroup.objects.get(name="Önerilen Ürünler")
    return render(request, 'home/product-detail.html',
                  {'product': product, 'group': group})


def search_category(request):
    categories = ProductCategory.objects.all()
    brands = Brand.objects.all()
    products = ''
    cat = ProductCategory.objects.get(pk=int(request.POST['cat']))

    if request.method == 'POST':
        # category = ProductCategory.objects.filter(pk=int(request.POST['cat']))
        products = Product.objects.filter(category__in=[cat],
                                          name__icontains=request.POST['name'])

    return render(request, 'home/get-category-products.html',
                  {'products': products, 'categories': categories, 'brands': brands, 'category': cat})
