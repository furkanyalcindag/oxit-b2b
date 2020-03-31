from decimal import Decimal

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view

from inoks.Forms.OptionForm import OptionForm
from inoks.models import Option, OptionValue, Product, OptionProduct
from inoks.serializers.OptionProductSerializer import OptionProductSerializer

from inoks.serializers.OptionValueSerializer import OptionValueSerializer


def add_option(request):  # şeçenekleri ekliyoruz
    option_form = OptionForm()
    if request.method == 'POST':
        option_form = OptionForm(request.POST)

        if option_form.is_valid():
            option = Option(type_name=option_form.cleaned_data['type_name'],
                            type=option_form.cleaned_data['type'])
            option.save()
            for value in request.POST['options'].split(","):
                option_value = OptionValue()
                option_value.option = option
                option_value.value = value
                option_value.save()

            messages.success(request, "Seçenek Başarıyla eklendi ")
        else:
            messages.warning(request, "Alanları kontrol edin.")
    return render(request, 'secenek/secenek-ekle.html', {'option_form': option_form})


def add_option_to_product(request, pk):  # ürünlere secenek ekliyoruz
    products = Product.objects.all()
    types = Option.objects.all()
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':

        stock = request.POST['stock']
        type = request.POST['type']
        type_value = request.POST['value']
        optionValue = OptionValue.objects.get(name=type_value)

        price = request.POST['price']
        list_price = request.POST['list_price']

        if price == None or " ":
            price = 0.0
        if list_price == None or " ":
            list_price = 0.0

        option_product = OptionProduct()
        option_product.product = product
        option_product.stock = stock

        option_product.price = price
        option_product.list_price = list_price
        option_product.option_value = optionValue
        option_product.save()
        messages.success(request, 'Ürün Bilgileri Kaydedildi')
    return render(request, 'secenek/urune-secenek-ekle.html', {'product': product, 'types': types})


@api_view(http_method_names=['POST'])
def get_typeValues(request):  # seçenek adına göre(option->type_name) değerlerini getiriyoruz (optionValue->name)
    if request.POST:
        try:

            type_id = request.POST.get('type_id')
            option = Option.objects.get(type_name=type_id)
            values = OptionValue.objects.filter(option=option)

            data = OptionValueSerializer(values, many=True)

            responseData = dict()
            responseData['values'] = data.data

            return JsonResponse(responseData, safe=True)

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


@api_view(http_method_names=['POST'])
def get_price_of_option(request):
    if request.POST:
        try:
            option_name = request.POST.get('option')
            option = OptionValue.objects.get(name=option_name)
            values = OptionProduct.objects.filter(option_value=option)

            data = OptionProductSerializer(values, many=True)

            responseData = dict()
            responseData['values'] = data.data

            return JsonResponse(responseData, safe=True)

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})
