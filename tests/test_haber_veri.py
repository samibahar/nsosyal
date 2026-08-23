from haber_veri import HABERLER


def test_her_haber_olayinin_iki_kaynagi_var():
    olaylar = {}
    for haber in HABERLER:
        olaylar.setdefault(haber["olay_id"], []).append(haber)

    assert len(olaylar) == 11
    assert all(len(kaynaklar) == 2 for kaynaklar in olaylar.values())
    assert all({haber["birincil"] for haber in kaynaklar} == {True, False} for kaynaklar in olaylar.values())


def test_alternatif_kaynak_ayni_olguyu_korur_ve_cift_yonlu_baglanir():
    haberler = {haber["id"]: haber for haber in HABERLER}
    for haber in HABERLER:
        alternatif = haberler[haber["alternatif_id"]]
        assert alternatif["alternatif_id"] == haber["id"]
        assert alternatif["olay_id"] == haber["olay_id"]
        assert alternatif["olgu_kodu"] == haber["olgu_kodu"]
        assert alternatif["kaynak"] != haber["kaynak"]


def test_yapici_kaynak_yogun_kaynaktan_daha_dengeli_etiketlenir():
    olaylar = {haber["olay_id"] for haber in HABERLER}
    for olay_id in olaylar:
        birincil = next(haber for haber in HABERLER if haber["olay_id"] == olay_id and haber["birincil"])
        alternatif = next(haber for haber in HABERLER if haber["olay_id"] == olay_id and not haber["birincil"])
        assert alternatif["duygu"] > birincil["duygu"]
