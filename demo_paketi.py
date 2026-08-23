"""Deterministic, clearly labelled data for the jury replay.

The posts are fictional first-person social posts written for this prototype.
``duygu`` is a public content-intensity label used by the transparent ranking
demo; it is not a label assigned to a person or a user emotion.
"""

DEMO_POSTS = [
    {"id": 8001, "yazar": "denizcetin", "konu": "teknoloji", "duygu": -0.88, "ilgi_skoru": 0.62, "final_skor": 0.62, "metin": "Sabahki veri kesintisi bütün ekibin planını değiştirdi. Herkes aynı anda çözüm arıyordu."},
    {"id": 8002, "yazar": "denizcetin", "konu": "teknoloji", "duygu": 0.38, "ilgi_skoru": 0.59, "final_skor": 0.59, "metin": "Dünkü kesinti için kısa bir açık kaynak kontrol listesi hazırladık. Bir sonraki sefer daha sakin ilerleriz."},
    {"id": 8003, "yazar": "mertdemir", "konu": "gundem", "duygu": -0.78, "ilgi_skoru": 0.60, "final_skor": 0.60, "metin": "Mahalledeki yol çalışması yine uzadı. İşe gidiş geliş herkes için yorucu bir hâl aldı."},
    {"id": 8004, "yazar": "mertdemir", "konu": "gundem", "duygu": 0.32, "ilgi_skoru": 0.58, "final_skor": 0.58, "metin": "Yol çalışması için yeni geçiş planını mahalle panosuna astılar. Küçük bir düzenleme bile günü kolaylaştırıyor."},
    {"id": 8005, "yazar": "selinkaya", "konu": "yasam", "duygu": 0.46, "ilgi_skoru": 0.57, "final_skor": 0.57, "metin": "Bugün yapılacaklar listesini yarıya indirdim. Kalan üç işin bitmesi beklediğimden daha iyi geldi."},
    {"id": 8006, "yazar": "ardaatlas", "konu": "spor", "duygu": 0.21, "ilgi_skoru": 0.56, "final_skor": 0.56, "metin": "Antrenmanda tempo tutmadı ama takım arkadaşımın son turdaki desteği bütün havayı değiştirdi."},
    {"id": 8007, "yazar": "eceyilmaz", "konu": "sanat", "duygu": 0.55, "ilgi_skoru": 0.55, "final_skor": 0.55, "metin": "Sergide en sevdiğim fotoğraf küçük bir köşedeydi. Kalabalık geçerken ben biraz daha kaldım."},
    {"id": 8008, "yazar": "denizcetin", "konu": "teknoloji", "duygu": -0.70, "ilgi_skoru": 0.61, "final_skor": 0.61, "metin": "Yeni güncelleme sonrası bazı telefonlar açılmadı. Destek hattındaki bekleyiş uzadıkça gerginlik arttı."},
    {"id": 8009, "yazar": "mertdemir", "konu": "gundem", "duygu": -0.67, "ilgi_skoru": 0.59, "final_skor": 0.59, "metin": "Akşam saatindeki yoğunluk yüzünden otobüsler doldu, eve dönüş herkes için daha uzun sürdü."},
    {"id": 8010, "yazar": "selinkaya", "konu": "yasam", "duygu": 0.62, "ilgi_skoru": 0.54, "final_skor": 0.54, "metin": "Bir arkadaşım çay bırakıp gitti. Günün en küçük ama en yerinde molasıydı."},
    {"id": 8011, "yazar": "ardaatlas", "konu": "spor", "duygu": 0.41, "ilgi_skoru": 0.53, "final_skor": 0.53, "metin": "Mahalle sahasında tanımadığım insanlarla takım olduk. İlk isimleri maç sonunda öğrendim."},
    {"id": 8012, "yazar": "eceyilmaz", "konu": "sanat", "duygu": 0.29, "ilgi_skoru": 0.52, "final_skor": 0.52, "metin": "Atölyede herkes kendi işiyle uğraşıyordu ama aynı masada olmak iyi geldi."},
]

# The replay is a prepared sample scenario, not inferred user behaviour. The
# repeated long dwell events are deliberately tied to the high-intensity posts.
DEMO_SCENARIO = [
    {"post_id": 8001, "dwell": 9.0, "click": True},
    {"post_id": 8003, "dwell": 8.5, "click": True},
    {"post_id": 8008, "dwell": 10.0, "click": True},
    {"post_id": 8009, "dwell": 8.0, "click": True},
    {"post_id": 8001, "dwell": 7.5, "click": True},
    {"post_id": 8003, "dwell": 7.0, "click": True},
    {"post_id": 8008, "dwell": 8.5, "click": True},
    {"post_id": 8009, "dwell": 7.5, "click": True},
    {"post_id": 8001, "dwell": 8.0, "click": True},
    {"post_id": 8008, "dwell": 8.0, "click": True, "reaction": "gerildim"},
]

DEMO_PROFILE_POSTS = [
    {"id": 8013, "yazar": "emiryusuf", "konu": "teknoloji", "duygu": 0.42, "ilgi_skoru": 0.55, "final_skor": 0.55, "metin": "Bugün küçük bir prototip akışını arkadaşlarımla denedik. En iyi geri bildirim beklemediğim bir yerden geldi."},
    {"id": 8014, "yazar": "emiryusuf", "konu": "seyahat", "duygu": 0.35, "ilgi_skoru": 0.52, "final_skor": 0.52, "metin": "Şehir içinde yeni bir yürüyüş rotası buldum. Aynı sokaklar biraz yavaşlayınca başka görünüyor."},
]
