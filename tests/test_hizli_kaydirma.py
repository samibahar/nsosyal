"""Hızlı kaydırma düzeltmesi: okuma tabanının (1,5 sn) altındaki durmalar göreli
oyalanmaya girmez. Gerçek veri testinde 0,4–1 sn'lik rastgele durma farkları
hızlı kaydırmayı "oyalanma" sanıp oturumların %23'ünde dengeleme başlatıyordu."""
import spiral_ozellik as so


def olay(i, t, dwell, ton, kelime=14):
    return {"gonderi": i, "zaman": t, "dwell": dwell, "ton": ton, "kelime": kelime, "konu": "gundem", "roket": False, "yorum": False}


def test_hizli_kaydirmada_kisa_durmalar_goreli_oyalanmaya_girmez():
    # Yoğunlara 0,9 sn, diğerlerine 0,5 sn: eski hesapta göreli oyalanma belirgin pozitifti.
    olaylar = [olay(i, i * 2.0, 0.9 if i % 3 == 0 else 0.5, -0.8 if i % 3 == 0 else 0.4) for i in range(20)]
    assert so.ozellikler(olaylar, 41)["goreli_oyalanma"] == 0.0


def test_okuma_tabanini_asan_oyalanma_hala_sayilir():
    olaylar = [olay(i, i * 6.0, 12.0 if i % 3 == 0 else 3.0, -0.8 if i % 3 == 0 else 0.4) for i in range(20)]
    assert so.ozellikler(olaylar, 121)["goreli_oyalanma"] > 0.5
