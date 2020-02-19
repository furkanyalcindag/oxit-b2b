from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view

from inoks.Forms.CommunicationForm import CommunicationForm
from inoks.Forms.CorporateForm import CorporateForm
from inoks.models import Profile, Settings
from inoks.serializers.ApiSerializer import SponsorApproveSerializer
from inoks.services import general_methods



@login_required
def return_profil_settings(request):
    return render(request, 'ayarlar/profil-ayarlari.html')


@login_required
def return_system_settings(request):
    return render(request, 'ayarlar/sistem-ayarlari.html')


@api_view(http_method_names=['POST'])
def sponsor_isexist(request):
    try:
        isExist = False
        adSoyad = ''
        sponsor = request.POST['sponsor']
        profile = Profile.objects.filter(pk=sponsor)

        if len(profile) > 0:
            isExist = True
            adSoyad = profile[0].user.first_name[0] + '****** ' + profile[0].user.last_name[0] + '******'

        situation = dict()
        situation['situation'] = isExist

        data = SponsorApproveSerializer(situation)

        responseData = dict()
        responseData['isExist'] = data.data

        if isExist:
            return JsonResponse({'status': 'Success', 'msg': 'Sponsor Doğrulandı', 'isExist': True, 'adSoyad': adSoyad})
        else:
            return JsonResponse({'status': 'Success', 'msg': 'Sponsor Bulunamadı', 'isExist': False})

    except Exception as e:

        return JsonResponse({'status': 'Fail', 'msg': 'Sponsor Bulunamadı', 'isExist': False})


@login_required
def return_corporate(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    corporate_form = CorporateForm(request.POST or None)

    if request.method == 'POST':
        settings = corporate_form.save(commit=False)
        settings.name = "Kurumsal"
        settings.save()

    return render(request, 'ayarlar/kurumsal.html', {'form': corporate_form})



@login_required
def return_contract(request):

    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    setting = Settings.objects.get
    corporate_form = CorporateForm(request.POST or None)

    if request.method == 'POST':
        settings = corporate_form.save(commit=False)
        settings.name = "Sozlesme"
        settings.save()

    return render(request, 'ayarlar/sozlesme.html', {'setting': setting, 'form': corporate_form})


@login_required
def return_phone(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    corporate_formPhone = CommunicationForm(request.POST or None)

    if request.method == 'POST':
        settings = corporate_formPhone.save(commit=False)
        settings.name = "Telefon"
        settings.save()

    return render(request, 'ayarlar/iletisim.html', {'form': corporate_formPhone, 'key': 'Telefon Numarası:'})


@login_required
def return_address(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    corporate_formAddress = CommunicationForm(request.POST or None)

    if request.method == 'POST':
        settings = corporate_formAddress.save(commit=False)
        settings.name = "Adres"
        settings.save()

    return render(request, 'ayarlar/iletisim.html', {'form': corporate_formAddress, 'key': 'Adres Bilgisi:'})

@login_required
def return_mail(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    corporate_formMail = CommunicationForm(request.POST or None)

    if request.method == 'POST':
        settings = corporate_formMail.save(commit=False)
        settings.name = "Mail"
        settings.save()

    return render(request, 'ayarlar/iletisim.html', {'form': corporate_formMail, 'key': 'Mail Adresi:'})
