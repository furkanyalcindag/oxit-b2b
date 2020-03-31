from datetime import datetime

import pytz
from django.contrib import messages
from django.db.models import Count, Q
from django.shortcuts import render

from inoks.filters.ProductFilter import ProductFilter
from inoks.models import ProductCategory, Product, ProductGroup, Settings, Rating, OptionProduct, Option
from inoks.models.Brand import Brand
from inoks.models.Discount import Discount
from inoks.models.Enum import OPTION_CHOICES


def get_home_product(request):
    products = Product.objects.filter(isActive=True).order_by('-creationDate')[:21]

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
    options = Option.objects.all()
    option_dict = dict()
    option_products = []
    for option in options:
        optionProducts = OptionProduct.objects.filter(product=product).filter(option_value__option_id=option.pk)
        if optionProducts.count() > 0:
            option_products.append(optionProducts)

            if len(option_products) > 0:
                option_dict[option.type_name] = optionProducts

    ratings = Rating.objects.filter(product=product)
    group = ProductGroup.objects.get(name="Önerilen Ürünler")
    point = 0
    count = 0
    if ratings.count() > 0:
        for rating in ratings:
            point = point + rating.point
            count = count + 1
        point = point / count
        point = point * 20

    if request.method == 'POST':
        selected = request.POST['option']
        return render(request, 'home/product-detail.html',
                      {'product': product, 'group': group, 'ratings': ratings, 'point': int(point),
                       'options': option_dict, 'selected': selected})

    return render(request, 'home/product-detail.html',
                  {'product': product, 'group': group, 'ratings': ratings, 'point': int(point),
                   'options': option_dict})


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


def get_corporate(request):
    corporate = Settings.objects.get(name='Kurumsal')
    return render(request, 'home/Corporate.html', {'corporate': corporate})
