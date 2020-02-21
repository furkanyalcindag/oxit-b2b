import json

from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import render, redirect

from inoks.Forms.GuestUserForm import GuestUserForm
from inoks.Forms.OrderUpdateForm import OrderForm
from inoks.models import Product, Profile, Settings, City, Order, OrderProduct, OrderSituations
from inoks.models.UserProductObject import UserProductObject
from inoks.services import general_methods


def order_checkout(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    orders = []

    if request.method == 'POST':
        products = json.loads(request.POST['products_cart'])

        for product in products:
            obj = Product.objects.get(id=product['id'])
            order = UserProductObject(id=0, product_name=None, price=0, count=0, image=None, subtotal=0)
            order.id = product['id']
            order.product_name = product['name']
            order.price = product['price']
            order.count = product['count']
            order.image = obj.productImage
            order.subtotal = product['count'] * product['price']

            orders.append(order)

        return render(request, 'checkout/siparis-detay.html', {'orders': orders})

    return render(request, 'checkout/siparis-detay.html', {'orders': orders})


