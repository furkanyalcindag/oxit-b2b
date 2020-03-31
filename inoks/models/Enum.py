MALE = 'Erkek'
FEMALE = 'Kadın'
UNKNOWN = 'Belirtmek İstemiyorum'

ilkokul = 'İlkokul'
lise = 'Lise'
lisans = 'Lisans'
master = 'Yüksek Lisans'
pre = 'Önlisans'

GENDER_CHOICES = (

    (MALE, 'Erkek'),
    (FEMALE, 'Kadın'),
    (UNKNOWN, 'Belirtmek İstemiyorum')
)

SCHOOL_CHOICES = (

    (ilkokul, 'İlkokul'),
    (lise, 'Lise'),
    (lisans, 'Lisans'),
    (master, 'Yüksek Lisans'),
    (pre, 'Önlisans'),

)

TRANSFER = 'Kredi Kartı'
EFT = 'Havale/EFT'
KAPIDA_ODEME = 'Kapıda Ödeme'
PAYMENT_CHOICES = (

    (TRANSFER, 'Kredi Kartı'),
    (EFT, 'Havale/EFT'),
    (KAPIDA_ODEME, 'Kapıda Ödeme')
)

Evet = 'Evet'
Hayir = 'Hayır'

OPEN_CHOICES = (
    (Evet, 'Evet'),
    (Hayir, 'Hayır'),

)

ARACTIP1 = 'BİNEK'
ARACTIP2 = 'TİCARİ'
ARACTIP3 = '4X4'

VEHICLE_CHOISES = (
    (ARACTIP1, 'BİNEK'),
    (ARACTIP2, 'TİCARİ'),
    (ARACTIP3, '4X4')
)

HIZ1 = 'Q=99MPH,160km/h'
HIZ2 = 'R=106 MPH, 170km/h'
HIZ3 = 'S=112 MPH, 180km/h'
HIZ4 = 'T=118 MPH, 190km/h'
HIZ5 = 'U=124 MPH, 200km/h'
HIZ6 = 'H=130 MPH, 210km/h'
HIZ7 = 'V=149 MPH, 240km/h'
HIZ8 = 'Z=149 MPH, 240km/h ve üzeri'
HIZ9 = 'W=168 MPH, 270km/h'
HIZ10 = 'Y=186 MPH, 300km/h'

SPEED_CHOISES = (
    (HIZ1, 'Q=99MPH,160km/h'),
    (HIZ2, 'R=106 MPH, 170km/h'),
    (HIZ3, 'S=112 MPH, 180km/h'),
    (HIZ4, 'T=118 MPH, 190km/h'),
    (HIZ5, 'U=124 MPH, 200km/h'),
    (HIZ6, 'H=130 MPH, 210km/h'),
    (HIZ7, 'V=149 MPH, 240km/h'),
    (HIZ8, 'Z=149 MPH, 240km/h ve üzeri'),
    (HIZ9, 'W=168 MPH, 270km/h'),
    (HIZ10, 'Y=186 MPH, 300km/h'),

)

ADDRESS1 = 'EV'
ADDRESS2 = 'İŞ'
ADDRESS3 = 'DİĞER'

ADDRESS_CHOISES = (
    (ADDRESS1, 'EV'),
    (ADDRESS2, 'İŞ'),
    (ADDRESS3, 'DİĞER')
)

OPTION1 = 'Seçenek'
OPTION2 = 'Radyo Düğmesi'
OPTION3 = 'Onay Kutusu'
OPTION4 = 'Metin'
OPTION5 = 'Dosya'
OPTION6 = 'Tarih'


OPTION_CHOICES = (
    (OPTION1, 'Seçenek'),
    (OPTION2, 'Radyo Düğmesi'),
    (OPTION3, 'Onay Kutusu'),
    (OPTION4, 'Metin'),
    (OPTION5, 'Dosya'),
    (OPTION6, 'Tarih'),

)
