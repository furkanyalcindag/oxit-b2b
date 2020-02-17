from django.conf.urls import url

from inoks.Views import ProductViews, UserViews, OrderViews, ReportViews, EarningsViews, DashboardViews, SettingViews, \
    TreeViews, RefundViews, CityViews, APIViews, HomeViews, CouponViews

app_name = 'inoks'

urlpatterns = [
    # HOME

    url(r'home/customer-home/$', HomeViews.get_home_product, name='kullanici-urun-sayfasi'),
    url(r'home/category-product/(?P<pk>\d+)$', HomeViews.get_category_products, name='kategori-urunleri'),
    url(r'home/brand-product/(?P<pk>\d+)$', HomeViews.get_brand_products, name='markanin-urunleri'),
    url(r'home/product-detail/(?P<pk>\d+)$', HomeViews.get_product_detail, name='urun-detay'),

    # Dashboard
    url(r'dashboard/admin-dashboard/$', DashboardViews.return_admin_dashboard, name='admin-dashboard'),
    url(r'dashboard/user-dashboard/$', DashboardViews.return_user_dashboard, name='user-dashboard'),
    url(r'dashboard/admin-dashboard/sil/(?P<pk>\d+)$', DashboardViews.pending_profile_delete,
        name='bekleyen-kullanicilar-sil'),
    url(r'dashboard/admin-dashboard/(?P<pk>\d+)$', DashboardViews.getPendingProfile, name='getPendingProfile'),
    url(r'kullanici-onayla/$', DashboardViews.profile_active_passive, name="kullanici-onayla"),
    url(r'dashboard/admin-dashboard/bekleyen-siparis-sil/(?P<pk>\d+)$', DashboardViews.pending_order_delete,
        name='bekleyen-siparisler-sil'),
    url(r'dashboard/admin-dashboard/pending-order/(?P<pk>\d+)$', DashboardViews.getPendingOrder,
        name='getPendingOrder'),
    url(r'siparis-onayla/$', DashboardViews.pendingOrderActive, name="siparis-onayla"),
    url(r'dashboard/user-dashboard/(?P<pk>\d+)$', DashboardViews.getMyOrder, name='getMyOrder'),

    # Kullanıcılar
    url(r'kullanici/kullanici-ekle/$', UserViews.return_add_users, name='kullanici-ekle'),
    url(r'kullanici/kullanicilar/$', UserViews.return_users, name='kullanicilar'),
    url(r'kullanici/uyelerim/$', UserViews.return_my_users, name='uyelerim'),
    url(r'kullanici/bekleyen-kullanicilar/$', UserViews.return_pending_users, name='bekleyen-kullanicilar'),
    url(r'kullanici/iptal-edilen-kullanicilar/$', UserViews.return_deactive_users, name='iptal-edilen-kullanicilar'),
    url(r'kullanici/bekleyen-kullanicilar/sil/(?P<pk>\d+)$', UserViews.pending_profile_delete,
        name='bekleyen-kullanicilar-sil'),
    url(r'kullanici-onayla/$', UserViews.profile_active_passive, name="kullanici-onayla"),
    url(r'kullanici-iptal-et/$', UserViews.profile_passive, name="kullanici-iptal-et"),
    url(r'kullanici/bekleyen-kullanicilar/(?P<pk>\d+)$', UserViews.getPendingProfile, name='getPendingProfile'),
    url(r'kullanici/kullanicilar/(?P<pk>\d+)$', UserViews.getAllProfile, name='getAllProfile'),
    url(r'kullanici/iptal-edilen-kullanicilar/(?P<pk>\d+)$', UserViews.getDeactiveProfile, name='getDeactiveProfile'),
    url(r'kullanici-aktif-et/$', UserViews.profile_reactive, name="kullanici-aktif-et"),
    url(r'kullanici/kullanici-ekle/duzenle/(?P<pk>\d+)$', UserViews.users_update, name='kullanici-duzenle'),
    url(r'kullanici/kullanici-ekle/kullanici-bilgileri/(?P<pk>\d+)$', UserViews.users_information,
        name='kullanici-bilgileri-getir'),
    url(r'kullanici/kullanici-bilgi-gonder/(?P<pk>\d+)$', UserViews.send_information, name='kullanici-bilgi-gonder'),
    url(r'kullanici/kullanici-kart-ekle/(?P<pk>\d+)$', UserViews.return_add_user_creditcart,
        name='kullanici-kart-ekle'),
    url(r'kullanici/kullanici-kart-guncelle/(?P<pk>\d+)$', UserViews.credit_card_update,
        name='kullanici-kart-guncelle'),
    url(r'kullanici/kullanici-kart-sil/(?P<pk>\d+)$', UserViews.credit_card_delete,
        name='kullanici-kart-sil'),

    # Urunler
    url(r'urunler/urun-ekle/$', ProductViews.return_add_products, name='urun-ekle'),
    url(r'urunler/urunler/$', ProductViews.return_products, name='urunler'),
    url(r'urunler/urun-kategori-ekle/$', ProductViews.return_add_product_category, name='urun-kategori-ekle'),
    url(r'urunler/urun-listesi/$', ProductViews.return_product_list, name='urun-listesi'),
    url(r'urunler/urun-listesi/sil/(?P<pk>\d+)$', ProductViews.product_delete, name='product-sil'),
    url(r'urunler/urunler/delete-image/$', ProductViews.product_image_delete, name='imageDelete'),
    url(r'urunler/urun-ekle/duzenle/(?P<pk>\d+)$', ProductViews.product_update, name='urun-duzenle'),
    url(r'urunler/urun-kategori-ekle/sil/(?P<pk>\d+)$', ProductViews.productCategory_delete,
        name='productCategory-sil'),
    url(r'urunler/urun-kategori-ekle/duzenle/(?P<pk>\d+)$', ProductViews.productCategory_update,
        name='urun-kategori-ekle-duzenle'),
    url(r'urunler/urun-listesi/(?P<pk>\d+)$', ProductViews.getProduct, name='getProduct'),
    url(r'urunler/urunler/(?P<pk>\d+)$', ProductViews.getProducts, name='getProducts'),
    url(r'urunler/marka-ekle/$', ProductViews.return_add_brand, name='marka-ekle'),
    url(r'urunler/marka-sil/(?P<pk>\d+)$', ProductViews.brand_delete, name='marka-sil'),
    url(r'urunler/grupla/(?P<group_id>\d+)$', ProductViews.add_products_to_group, name='urun-grupla'),
    url(r'urunler/grup-urun-sil/(?P<group_id>\d+)/(?P<product_id>\d+)$', ProductViews.delete_product_from_group,
        name='urun-grup-sil'),

    # Siparisler
    url(r'siparisler/siparis-ekle/$', OrderViews.return_add_orders, name='siparis-ekle'),
    url(r'siparisler/admin-siparis-ekle/$', OrderViews.return_add_orders_admin, name='admin-siparis-ekle'),
    url(r'siparisler/bekleyen-siparisler/$', OrderViews.return_pending_orders, name='bekleyen-siparisler'),
    url(r'siparisler/siparislerim/$', OrderViews.return_my_orders, name='siparislerim'),
    url(r'siparisler/siparislerim/(?P<pk>\d+)$', OrderViews.getMyOrder, name='getMyOrder'),
    url(r'siparisler/siparisler/$', OrderViews.return_orders, name='siparisler'),
    url(r'siparisler/siparis-durumlari/$', OrderViews.return_order_situations, name='siparis-durumlari'),
    url(r'siparisler/bekleyen-siparisler/sil/(?P<pk>\d+)$', OrderViews.pending_order_delete,
        name='bekleyen-siparisler-sil'),
    url(r'siparisler/bekleyen-siparisler/(?P<pk>\d+)$', OrderViews.getPendingOrder, name='getPendingOrder'),
    url(r'siparis-onayla/$', OrderViews.pendingOrderActive, name="siparis-onayla"),
    url(r'siparisler/siparisler/sil/(?P<pk>\d+)$', OrderViews.orders_delete,
        name='siparislersil'),
    url(r'siparisler/siparisler/uye-siparis-sil/(?P<pk>\d+)$', OrderViews.orders_delete_member,
        name='uye-siparis-sil'),
    url(r'siparisler/siparisler/(?P<pk>\d+)$', OrderViews.getOrder, name='getOrder'),
    url(r'siparisler/sepet-siparis-ekle/$', OrderViews.return_add_orders_from_cart, name='kart-siparis-ekle'),
    url(r'siparis-durumu-guncelle/$', OrderViews.siparis_durumu_guncelle, name="siparis-durumu-guncelle"),
    url(r'kargo-bilgi/(?P<pk>\d+)$', OrderViews.kargoBilgi, name='kargo-bilgi'),

    # İadeler
    url(r'iadeler/iade-olustur/$', RefundViews.return_add_refund, name='iade-olustur'),
    url(r'iadeler/iadeler/$', RefundViews.return_refunds, name='iadeler'),
    url(r'iadeler/iadelerim/$', RefundViews.return_my_refunds, name='iadelerim'),
    url(r'iadeler/iade-durumlari/$', RefundViews.return_refund_situations, name='iade-durumlari'),
    url(r'iadeler/iade-durumlari/sil/(?P<pk>\d+)$', RefundViews.refund_situations_delete, name='iade-durum-sil'),
    url(r'iadeler/iade-durumlari/duzenle/(?P<pk>\d+)$', RefundViews.refund_situations_update,
        name='iade-durum-duzenle'),
    url(r'iade-onayla/$', RefundViews.pendingRefundActive, name="iade-onayla"),
    url(r'iade-reddet/$', RefundViews.pendingRefundPassive, name="iade-reddet"),
    url(r'iadeler/bekleyen-iadeler/$', RefundViews.return_pendings_refunds, name='bekleyen-iadeler'),

    # Raporlar
    url(r'raporlar/rapor-olustur/$', ReportViews.return_create_report, name='rapor-olustur'),

    # Kazançlar
    url(r'kazanclar/kazanclar/$', EarningsViews.return_all_earnings_report, name='kazanclar'),
    url(r'kazanclar/kazanclarim/$', EarningsViews.return_my_earnings_report, name='kazanclarim'),
    url(r'kazanclar/odenecekler/$', EarningsViews.return_odenecekler, name='odenecekler'),
    url(r'kazanclar/odenenler/$', EarningsViews.return_odenenler, name='odenenler'),
    url(r'odeme-yap/$', EarningsViews.make_pay, name="odeme-yap"),

    # Ayarlar
    url(r'ayarlar/profil-ayarlari/$', SettingViews.return_profil_settings, name='profil-ayarlari'),
    url(r'ayarlar/sistem-ayarlari/$', SettingViews.return_system_settings, name='sistem-ayarlari'),
    url(r'sponsor-dogrula/$', SettingViews.sponsor_isexist, name="sponsor-dogrula"),

    # SoyAgacı
    url(r'soyagaci/soy-agacim/$', TreeViews.return_my_tree, name='soy-agacim'),
    url(r'soyagaci/soy-agaclari/$', TreeViews.return_all_tree, name='soy-agaclari'),

    # api
    url(r'ilce-getir/$', CityViews.get_districts, name="ilce-getir"),
    url(r'adres-bilgi/$', APIViews.get_address_info, name="adres-bilgi"),
    url(r'siparis/urun-bilgi-getir/$', APIViews.get_order_products.as_view(), name="siparis-urun-getir"),

    # odeme
    url(r'odeme-modul/(?P<siparis>\d+)$', OrderViews.odemeYap, name='odeme-yap'),
    url(r'odeme-bildirim/$', OrderViews.odeme_sonuc, name='odeme-sonuc'),
    url(r'odeme-basarili/$', OrderViews.basarili_odeme, name='odeme-basarili'),
    url(r'odeme-basarisiz/$', OrderViews.basarisiz_odeme, name='basarisiz-odeme'),
    url(r'havale-eft-bilgi/(?P<siparis>\d+)$', OrderViews.havale_eft, name='havale-eft-bilgi'),

    # kupon
    url(r'kupon-bilgileri/$', CouponViews.coupon_create, name='kupon'),
    url(r'ödeme-bilgileri/$', CouponViews.review_payments, name='odeme'),
    url(r'kupon-aktifligi/(?P<pk>\d+)$', CouponViews.coupon_activity, name='kupon-aktiflestir'),
    url(r'kupon-sil/(?P<pk>\d+)$', CouponViews.coupon_delete, name='kupon-sil'),
    url(r'kupon-guncelle/(?P<pk>\d+)$', CouponViews.coupon_update, name='kupon-guncelle'),

]
