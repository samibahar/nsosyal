from resmi_veri import RESMI_GONDERILER, RESMI_HESAPLAR
from sosyal_veri import DEMO_KULLANICILAR, SosyalDepo


def test_resmi_gonderiler_tanimli_resmi_hesaba_ait():
    assert RESMI_HESAPLAR <= set(DEMO_KULLANICILAR)
    assert RESMI_GONDERILER and all(g["yazar"] in RESMI_HESAPLAR for g in RESMI_GONDERILER)


def test_sonradan_eklenen_gonderiler_mevcut_veritabanina_girer(tmp_path):
    depo = SosyalDepo(tmp_path / "demo.sqlite3")
    depo.hazirla([{"id": 1, "konu": "bilim", "metin": "Kısa bir demo postu.", "yazar": "denizcetin"}])
    depo.hazirla([{"id": 1, "konu": "bilim", "metin": "Değişmemeli.", "yazar": "denizcetin"}, *RESMI_GONDERILER])
    gonderiler = {g["id"]: g for g in depo.gonderileri_yukle()}
    assert gonderiler[1]["metin"] == "Kısa bir demo postu."
    assert all(gonderiler[g["id"]]["yazar"] == "kentkoordinasyon" for g in RESMI_GONDERILER)
