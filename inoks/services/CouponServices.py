from inoks.models.Coupon import Coupon


def active_passive_coupon(pk):
    coupon = Coupon.objects.get(pk=pk)

    if coupon.isActive:
        coupon.isActive = False
    else:
        coupon.isActive = True

    coupon.save()

    return coupon
