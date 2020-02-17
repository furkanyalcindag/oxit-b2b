from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages

from inoks.Forms.CouponForm import CouponForm
from inoks.Forms.ProfileForm import ProfileForm
from inoks.Forms.UserForm import UserForm
from inoks.models import Profile
from inoks.models.Coupon import Coupon
from inoks.services import general_methods, CouponServices


@login_required
def coupon_create(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    coupon_form = CouponForm(request.POST)

    coupon = Coupon.objects.all()

    if request.method == 'POST':

        if coupon_form.is_valid():

            coupon = coupon_form.save(commit=False)
            coupon.isApprove = True
            coupon.save()

            messages.success(request, 'Bilgiler Başarı İle Eklendi')
            return redirect('inoks:kupon')

        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'kullanici/kullanici-kupon-form.html',
                  {'coupon_form': coupon_form, 'coupon': coupon})


@login_required
def coupon_update(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    coupon = Coupon.objects.get(pk=pk)
    coupon_form = CouponForm(request.POST or None, instance=coupon)

    coupon = Coupon.objects.all()

    if request.method == 'POST':

        if coupon_form.is_valid():

            coupon = coupon_form.save()

            messages.success(request, 'Kupon başarıyla güncellendi')
            return redirect('inoks:kupon')

        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'kullanici/kullanici-kupon-form.html',
                  {'coupon_form': coupon_form, 'coupon': coupon})


@login_required
def review_payments(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    coupon_form = CouponForm(request.POST)
    profile_form = ProfileForm(request.POST)
    user_form = UserForm(request.POST)

    if request.method == 'POST':

        if coupon_form.is_valid():

            coupon = coupon_form.save(commit=False)
            coupon.isApprove = True
            coupon.save()

            messages.success(request, 'Bilgiler Başarı İle Eklendi')
            return redirect('inoks:odeme')

        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'kullanici/kullanici-ödeme-kupon.html',
                  {'coupon_form': coupon_form, 'user_form': user_form, 'profile_form': profile_form})


@login_required
def coupon_activity(request, pk):
    if CouponServices.active_passive_coupon(pk).isActive:
        messages.success(request, 'Kupon Aktifleştirildi')
    else:
        messages.success(request, 'Kupon Pasifleştirildi')

    return redirect('inoks:kupon')


@login_required
def coupon_delete(request, pk):
    coupon = Coupon.objects.get(pk=pk)
    coupon.delete()
    messages.success(request, 'Kupon basarıyla silindi')

    return redirect('inoks:kupon')
