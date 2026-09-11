"""Resmi / acil bilgilendirme hesabı ve örnek duyuruları.

İlke: duygu dengelemesi haberi saklamaz, yalnızca yoğun içeriğin art arda
tekrarını azaltır. Afet ve acil durum bilgisi ise olumsuz tonlu olsa bile
hayati olabilir; bu hesaplardan gelen gönderiler dengelemeden MUAFTIR ve
kullanıcının "Gerildim" tepkisi de onları aşağı itmez.

Hesap kurgusaldır (gerçek bir kurumu temsil etmez); gerçek üründe muafiyet
listesi doğrulanmış resmi kurum hesaplarından oluşur.
"""

RESMI_HESAPLAR = {"kentkoordinasyon"}

RESMI_GONDERILER = [
    {"id": 9001, "konu": "gundem", "yazar": "kentkoordinasyon",
     "metin": "Yarın öğleden sonra kuvvetli fırtına bekleniyor. Kıyı yolu 14.00'ten itibaren trafiğe kapatılacak; zorunlu olmadıkça dışarı çıkmayın."},
    {"id": 9002, "konu": "gundem", "yazar": "kentkoordinasyon",
     "metin": "Sel riski nedeniyle dere yataklarına yakın mahallelerde yaşayanların dikkatli olması istendi. Toplanma alanlarının listesi belediyenin sitesinde."},
    {"id": 9003, "konu": "saglik", "yazar": "kentkoordinasyon",
     "metin": "Deprem sonrası hasar tespit başvuruları bugünden itibaren muhtarlıklardan ve çevrim içi olarak alınıyor."},
]
