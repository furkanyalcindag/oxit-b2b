from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from rest_framework.decorators import api_view

import oxiterp
from inoks.Forms.CommunicationForm import CommunicationForm
from inoks.Forms.CorporateForm import CorporateForm
from inoks.models import Profile, Settings
from inoks.serializers.ApiSerializer import SponsorApproveSerializer
from inoks.services import general_methods
from oxiterp.settings.base import EMAIL_HOST_USER


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
    messages.success(request, 'Başarıyla kaydedilmiştir.')
    return render(request, 'ayarlar/kurumsal.html', {'form': corporate_form})


def return_contact(request):
    phone = Settings.objects.get(name='company_phone')
    email = Settings.objects.get(name='company_email')
    address = Settings.objects.get(name='company_address')
    company_name = Settings.objects.get(name='company_name')
    company_mobilePhone = Settings.objects.get(name='company_mobilePhone')

    if request.method == 'POST':
        contact_name = request.POST['contact-name']
        contact_email = request.POST['contact-email']
        contact_phone = request.POST['contact-phone']
        contact_message = request.POST['contact-message']

        invoice_data = {'contact_name': contact_name, 'contact_email': contact_email, 'contact_phone': contact_phone,
                        'contact_message': contact_message}

        subject, from_email, to = 'Oxit Bilişim Teknolojileri', 'burcu.dogan@oxityazilim.com', EMAIL_HOST_USER
        text_content = 'Müşteri Mesajı'

        html_body = render_to_string("mailTemplates/contact.html", invoice_data)

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_body, "text/html")
        msg.send()

        messages.success(request, 'Mesajınız başarıyla alınmıştır.En yakın sürede dönüş sağlanacaktır.')

    return render(request, 'home/Contact.html',
                  {'phone': phone, 'email': email, 'address': address, 'company_name': company_name,
                   'company_mobilePhone': company_mobilePhone})


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
    messages.success(request, 'Başarıyla kaydedilmiştir.')
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
        settings.name = "company_phone"
        settings.save()
    messages.success(request, 'Başarıyla kaydedilmiştir.')
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
        settings.name = "company_address"
        settings.save()
    messages.success(request, 'Başarıyla kaydedilmiştir.')
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
        settings.name = "company_email"
        settings.save()
    messages.success(request, 'Başarıyla kaydedilmiştir.')
    return render(request, 'ayarlar/iletisim.html', {'form': corporate_formMail, 'key': 'Mail Adresi:'})
