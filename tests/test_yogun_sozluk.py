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
