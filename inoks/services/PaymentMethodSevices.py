from inoks.models import PaymentMethod


def active_passive_paymentMethod(pk):
    payment_method = PaymentMethod.objects.get(pk=pk)

    if payment_method.isActive:
        payment_method.isActive = False
    else:

        for payment in PaymentMethod.objects.all():
            payment.isActive = False
            payment.save()
        payment_method.isActive = True

    payment_method.save()

    return payment_method
