import spiral_ozellik as so
from spiral_model import egitilmis, olasilik

OKUMA = so.beklenen_okuma(14)


def olay(i, t, dwell, ton, kelime=14, konu="gundem", roket=False, yorum=False):
    return {"gonderi": i, "zaman": t, "dwell": dwell, "ton": ton, "kelime": kelime, "konu": konu, "roket": roket, "yorum": yorum}


def pasif_oyalanma(aktif=False):
    t, gunluk = 0.0, []
    for i in range(20):
        yogun = i % 5 < 2
        gunluk.append(olay(i, t, 12.0 if yogun else 3.0, -0.9 if yogun else 0.3, konu="gundem" if yogun else "spor", yorum=aktif and yogun))
        t += (12 if yogun else 3) + 1
    return gunluk, t


def test_az_gonderide_risk_hesaplanmaz():
    assert so.ozellikler([olay(1, 0, 5, -0.9), olay(2, 5, 5, -0.9)], simdi=10) is None
    assert olasilik(None) == 0.0


def test_ayni_gonderiye_donmek_tek_kayit_sayilir():
    gunluk = so.birlestir([olay(1, 0, 3, -0.9), olay(1, 10, 8, -0.9), olay(2, 12, 2, 0.2)], simdi=20)
    assert len(gunluk) == 2
    assert gunluk[0]["dwell"] == 8


def test_olumsuzda_pasif_oyalanma_yuksek_risk():
    gunluk, simdi = pasif_oyalanma()
    assert olasilik(so.ozellikler(gunluk, simdi)) > 0.6


def test_aktif_katilim_riski_azaltir():
    pasif, simdi = pasif_oyalanma()
    aktif, _ = pasif_oyalanma(aktif=True)
    assert olasilik(so.ozellikler(pasif, simdi)) - olasilik(so.ozellikler(aktif, simdi)) > 0.15


def test_uzun_metin_okumak_oyalanma_sayilmaz():
    t, gunluk = 0.0, []
    for i in range(15):
        gunluk.append(olay(i, t, 12.0, 0.8, kelime=30, konu="bilim"))
        t += 13
    assert olasilik(so.ozellikler(gunluk, t)) < 0.3


def test_yogun_habere_hizli_goz_atmak_oyalanma_sayilmaz():
    t, gunluk = 0.0, []
    for i in range(20):
        gunluk.append(olay(i, t, 2.0, -0.85, konu=str(i % 10)))
        t += 3
    ozellik = so.ozellikler(gunluk, t)
    assert ozellik["yogun_fazla_kalma"] == 0.0
    assert olasilik(ozellik) < 0.5


def test_tamami_yogun_akista_oyalanma_goz_atmaktan_ayrilir():
    """Kriz günü: akışın tamamı yoğun tonlu. Kıyaslanacak başka gönderi yok;
    okuma süresi kadar bakmak referans alınır."""
    def akis(dwell):
        return [olay(i, i * (dwell + 1), dwell, -0.9, konu=str(i % 3)) for i in range(12)], 12 * (dwell + 1)
    oyalanma, simdi_o = akis(14.0)
    goz_atma, simdi_g = akis(2.0)
    assert olasilik(so.ozellikler(oyalanma, simdi_o)) - olasilik(so.ozellikler(goz_atma, simdi_g)) > 0.3


def test_eski_oturum_bugunu_etkilemez():
    t, gunluk = 0.0, []
    for i in range(12):
        gunluk.append(olay(100 + i, t, 12.0, -0.9))
        t += 13
    t += 3 * 3600
    for i in range(10):
        gunluk.append(olay(i, t, 4.0, 0.2, konu=str(i)))
        t += 5
    assert olasilik(so.ozellikler(gunluk, t)) < 0.3


def test_katsayi_yonleri_hipotezle_uyumlu():
    """Sentetik veride bir özelliğin ters işaret alması (baskılayıcı etki),
    modelin veri dışı durumlarda saçmalamasına yol açar; ilk denemede böyle oldu."""
    beklenen = {"yogun_pay": 1, "goreli_oyalanma": 1, "yogun_fazla_kalma": 1, "aktif_oran": -1}
    katsayilar = dict(zip(so.OZELLIK_ADLARI, egitilmis()["model"].coef_[0]))
    for ad, isaret in beklenen.items():
        assert katsayilar[ad] * isaret >= 0, (ad, katsayilar[ad])
    # Kısıt her şeyi sıfıra itmiş olmasın: ana sinyaller gerçekten kullanılıyor.
    assert katsayilar["goreli_oyalanma"] > 0.5
    assert katsayilar["aktif_oran"] < -0.2


def test_okuma_suresi_normalizasyonu():
    kisa = so.ozellikler([olay(i, i * 10, 8.0, -0.9, kelime=5) for i in range(5)], simdi=50)
    uzun = so.ozellikler([olay(i, i * 10, 8.0, -0.9, kelime=40) for i in range(5)], simdi=50)
    assert kisa["yogun_fazla_kalma"] > uzun["yogun_fazla_kalma"]
