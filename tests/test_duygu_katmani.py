from duygu_katmani import analiz_et


POSTS = [
    {"id": 1, "konu": "gundem", "duygu": -0.8},
    {"id": 2, "konu": "bilim", "duygu": 0.7},
]


def test_az_sinyal_mudahale_uretmez():
    sonuc = analiz_et([{"gonderi_id": 1, "dwell_saniye": 30, "tiklama": True, "zaman": 100}], POSTS, now=100)
    assert sonuc["veri_yeterli"] is False
    assert sonuc["surdurulmus_oruntu"] is False


def test_surdurulen_negatif_oruntu_mudahale_icin_uygun_kanit_uretir():
    gunluk = [{"gonderi_id": 1, "dwell_saniye": 12, "tiklama": True, "zaman": 100} for _ in range(10)]
    sonuc = analiz_et(gunluk, POSTS, kalibrasyon=0.8, now=100)
    assert sonuc["veri_yeterli"] is True
    assert sonuc["surdurulmus_oruntu"] is True
    assert sonuc["guven"] > 0.5


def test_pozitif_ve_nötr_akıs_mudahale_uretmez():
    gunluk = [{"gonderi_id": 2, "dwell_saniye": 12, "tiklama": True, "zaman": 100} for _ in range(12)]
    sonuc = analiz_et(gunluk, POSTS, now=100)
    assert sonuc["surdurulmus_oruntu"] is False
    assert sonuc["negatif_oran"] == 0.0
