from yogun_sozluk import SOZLUK_TONU, sistem_tonu, yogun_sozcuk


def test_acik_olumsuz_olaylar_yakalanir():
    for metin in ["Diyarbakır'da iş cinayeti: Elektrik akımına kapılan işçi öldü",
                  "İzmir'de bir kadın yakılarak öldürüldü",
                  "Endonezya'da iki tren kafa kafaya çarpıştı: çok sayıda ölü ve yaralı var",
                  "Taciz suçlamasıyla gözaltına alındı",
                  "İSTİSMAR ŞİKÂYETİ İÇİN GİTTİĞİ KARAKOLDA HAYATINI KAYBETTİ"]:
        assert yogun_sozcuk(metin), metin


def test_benzer_ama_olumsuz_olmayanlar_yakalanmaz():
    for metin in ["Takımımız maçı son dakikada kazandı",
                  "Kadına yönelik şiddetle mücadele tedbirleri değerlendirildi",
                  "Yarın şiddetli yağış bekleniyor",
                  "Depremzedelere yeni konutlar teslim edildi",
                  "Van Gölü kıyısında çarpıcı bir gün batımı",
                  "Sergide en sevdiğim fotoğraf küçük bir köşedeydi",
                  "Uluslararası film festivali başvuruları başladı",  # kelime içi: başVURULarı
                  "Bilinçli tüketim için enerji tasarrufu önerileri"]:  # kelime içi: biLİNÇli
        assert yogun_sozcuk(metin) is None, metin


def test_ton_yalnizca_asagi_cekilir():
    assert sistem_tonu(0.91, "Bir işçi öldü") == (SOZLUK_TONU, "öldü")
    assert sistem_tonu(-0.95, "Bir işçi öldü")[0] == -0.95
    assert sistem_tonu(0.4, "Güzel bir gün") == (0.4, None)


def test_olay_olmayan_arac_egitim_ve_mecaz():
    for metin in ["Okulda yangın tatbikatı yapıldı", "Yeni bıçak seti satışa çıktı",
                  "İhracatta patlama yaşandı", "Salonda kahkaha patlaması oldu",
                  "Yangın söndürme tüpleri yenilendi"]:
        assert sistem_tonu(0.4, metin) == (0.4, None), metin


def test_olay_disi_ifade_gercek_olayi_gizlemez():
    for metin in ["Yangın tatbikatında bir kişi yaralandı",
                  "Bıçak seti taşıyan araç kaza yaptı",
                  "Yangın söndürme tüpü patladı"]:
        assert sistem_tonu(0.4, metin)[0] == SOZLUK_TONU, metin


def test_karaktersiz_yazim_olaylari_ve_cakismalar():
    for metin in ["Saldiri sonucu yarali var", "Bir asker sehit oldu", "SALDIRI HABERI"]:
        assert yogun_sozcuk(metin), metin
    for metin in ["Guzel oldu", "Etkinlige katilim artti", "Bu yil coktu", "Takim kazandi",
                  "Kazasız belasız geldik", "Kazasiz belasiz geldik", "Yangin tatbikati yapildi",
                  "Bicak seti satisa cikti", "Ihracatta patlama yasandi"]:
        assert yogun_sozcuk(metin) is None, metin
    assert yogun_sozcuk("Yangin tatbikatinda yarali var")
