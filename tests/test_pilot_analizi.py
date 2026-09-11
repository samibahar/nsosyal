"""pilot_analizi.py: dosya okuma, güven aralığı ve birini-dışarıda-bırak yeniden eğitimi."""
import json

import numpy as np
import pytest

import pilot_analizi as pa

OLUMSUZ, OLUMLU = ["anksiyete", "sinirli"], ["sakin", "mutluluk", "umut"]


def _kayit(rng, sira, yogun, demo=False):
    """Yapay ama bilinen bir ilişki: 'yoğun' cevabı yüksek göreli oyalanmayla gelir."""
    return {
        "sira": sira, "gun": sira // 4, "cevap": str(rng.choice(OLUMSUZ if yogun else OLUMLU)), "demo": demo,
        "psikolojik": {"pencere": [
            {"ozellik": {"duygu": 0.2, "dwell_saniye": 3.0, "tiklama": 0, "roket": 0, "yorum": 0}, "agirlik": 0.3},
            {"ozellik": {"duygu": -0.7 if yogun else 0.5, "dwell_saniye": 9.0 if yogun else 4.0,
                         "tiklama": 0, "roket": 0, "yorum": 0}, "agirlik": 0.7}], "varsayilan": "sakin", "kisisel": None},
        "spiral": {"ozellik": {"yogun_pay": 0.5 if yogun else 0.1, "goreli_oyalanma": rng.normal(0.8 if yogun else -0.2, 0.3),
                               "yogun_fazla_kalma": 0.3, "aktif_oran": rng.uniform(0, 0.3)},
                   "p0": 0.26, "pk": None, "etkin": False},
    }


def _yaz(klasor, kod, kayitlar, bicim=pa.BICIM):
    (klasor / f"nsosyal-pilot-{kod}.json").write_text(json.dumps({"bicim": bicim, "katilimci": kod, "kayitlar": kayitlar}), encoding="utf-8")


@pytest.fixture
def pilot_klasoru(tmp_path):
    rng = np.random.default_rng(7)
    for kod in ["a1", "b2", "c3", "d4"]:
        _yaz(tmp_path, kod, [_kayit(rng, i, rng.random() < 0.4) for i in range(12)])
    return tmp_path


def test_demo_cevaplari_ve_gecersiz_dosyalar_alinmaz(tmp_path):
    rng = np.random.default_rng(1)
    _yaz(tmp_path, "a1", [_kayit(rng, 1, True), _kayit(rng, 2, False, demo=True)])
    _yaz(tmp_path, "yanlis", [_kayit(rng, 1, True)], bicim="baska")
    (tmp_path / "bozuk.json").write_text("{", encoding="utf-8")
    katilimcilar = pa.yukle(tmp_path)
    assert [k["kod"] for k in katilimcilar] == ["a1"] and len(katilimcilar[0]["kayitlar"]) == 1


def test_ruh_hali_girdisi_pencerenin_agirlikli_ortalamasi_eski_bicim_de_okunur():
    yeni = {"psikolojik": {"pencere": [{"ozellik": dict.fromkeys(pa.PSIKOLOJIK_OZELLIKLER, 0.0), "agirlik": 0.25},
                                       {"ozellik": dict.fromkeys(pa.PSIKOLOJIK_OZELLIKLER, 4.0), "agirlik": 0.75}]}}
    assert pa._psikolojik_ozellik(yeni) == pytest.approx([3.0] * 5)
    eski = {"psikolojik": {"ozellik": dict.fromkeys(pa.PSIKOLOJIK_OZELLIKLER, 2.0)}}
    assert pa._psikolojik_ozellik(eski) == [2.0] * 5


def test_wilson_araligi():
    alt, ust = pa.wilson(8, 10)
    assert alt < 0.8 < ust and 0.4 < alt and ust < 0.98
    assert pa.wilson(0, 0) == (0.0, 1.0)


def test_sabit_sentetik_tahmin_ayrim_yapmaz_pilot_egitimi_yapar(pilot_klasoru):
    katilimcilar = pa.yukle(pilot_klasoru)
    kt = pa.kayitli_tahminler(katilimcilar)
    assert kt["cevap"] == 48 and kt["spiral"]["auc"] == pytest.approx(0.5)
    ye = pa.yeniden_egitim(katilimcilar)
    assert ye["spiral"]["n"] == 48
    assert ye["spiral"]["pilot"]["auc"] > 0.8 and ye["spiral"]["pilot"]["brier"] < ye["spiral"]["sentetik"]["brier"]
    assert ye["psikolojik"]["pilot"] > ye["psikolojik"]["taban"]
    assert "spiral_model.py'nin eğitim verisine pilot cevapları eklenmeli" in pa.rapor(katilimcilar)


def test_az_katilimciyla_yeniden_egitim_yapilmaz(tmp_path):
    rng = np.random.default_rng(3)
    for kod in ["a1", "b2"]:
        _yaz(tmp_path, kod, [_kayit(rng, i, i % 2 == 0) for i in range(6)])
    katilimcilar = pa.yukle(tmp_path)
    assert "yetersiz" in pa.yeniden_egitim(katilimcilar)
    assert "Yapılmadı" in pa.rapor(katilimcilar)
