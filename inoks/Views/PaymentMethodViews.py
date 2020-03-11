from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from inoks.Forms.PaymentMethodForms.BakiyemUpdateForm import BakiyemUpdateForm
from inoks.Forms.PaymentMethodForms.IyzicoUpdateForm import IyzicoUpdateForm
from inoks.Forms.PaymentMethodForms.PayTRUpdateForm import PayTRUpdateForm
from inoks.models import PaymentMethodBakiyem, PaymentMethodIyzico
from inoks.models.PaymentMethod import PaymentMethod
from inoks.models.PaymentMethodPayTR import PaymentMethodPayTR
from inoks.services import general_methods, PaymentMethodSevices


def UpdatePaytr(request, pk):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    payment_method = PaymentMethod.objects.get(pk=pk)
    payTr = PaymentMethodPayTR.objects.get(payment_type=payment_method)
    payTr_form = PayTRUpdateForm(request.POST or None, instance=payTr)
    if request.method == 'POST':
        if payTr_form.is_valid():
            payTr.merchantId = payTr_form.cleaned_data['merchantId']
            payTr.merchantKey = payTr_form.cleaned_data['merchantKey']
            payTr.merchantSalt = payTr_form.cleaned_data['merchantSalt']
            payTr_form.payment_type = payment_method.name
            payTr_form.save()

        messages.success(request, 'PayTr Güncellendi')

        return redirect('inoks:payTr', payment_method.pk)

    return render(request, 'OdemeYontemi/PaytrUpdate.html', {'payTr_form': payTr_form})


def UpdateBakiyem(request, pk):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    payment_method = PaymentMethod.objects.get(pk=pk)
    bakiyem = PaymentMethodBakiyem.objects.get(payment_type=payment_method)
    bakiyem_form = BakiyemUpdateForm(request.POST or None, instance=bakiyem)
    if request.method == 'POST':
        if bakiyem_form.is_valid():
            bakiyem_form.username = bakiyem_form.cleaned_data['username']
            bakiyem_form.password = bakiyem_form.cleaned_data['password']
            bakiyem_form.dealerCode = bakiyem_form.cleaned_data['dealerCode']
            bakiyem_form.payment_type = payment_method.name
            bakiyem_form.save()

        messages.success(request, 'Bakiyem Yöntemi Güncellendi')

        return redirect('inoks:bakiyem', payment_method.pk)

    return render(request, 'OdemeYontemi/bakiyemUpdate.html', {'bakiyem_form': bakiyem_form})


def UpdateIyzico(request, pk):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    payment_method = PaymentMethod.objects.get(pk=pk)
    iyzico = PaymentMethodIyzico.objects.get(payment_type=payment_method)
    iyzico_form = IyzicoUpdateForm(request.POST or None, instance=iyzico)
    if request.method == 'POST':
        if iyzico_form.is_valid():
            iyzico_form.apiKey = iyzico_form.cleaned_data['apiKey']
            iyzico_form.secretKey = iyzico_form.cleaned_data['secretKey']
            iyzico_form.payment_type = payment_method.name
            iyzico_form.save()

        messages.success(request, 'İyzico Güncellendi')

        return redirect('inoks:iyzico', payment_method.pk)

    return render(request, 'OdemeYontemi/iyzicoUpdate.html', {'iyzico_form': iyzico_form})


def paymentMethod(request):
    paymentMethod = PaymentMethod.objects.all()
    return render(request, 'OdemeYontemi/paymentMethod.html', {'paymentMethod': paymentMethod})


@login_required
def paymentMethod_activity(request, pk):
    if PaymentMethodSevices.active_passive_paymentMethod(pk).isActive:
        messages.success(request, 'Yöntem Aktifleştirildi')
    else:
        messages.success(request, 'Yöntem Pasifleştirildi')

    return redirect('inoks:payment-method')

