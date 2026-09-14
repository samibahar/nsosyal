"""Tarayıcıdaki trained-models.js ile Python aynı hesabı yapar: spiral özellikleri
(spiral_ozellik.py, hızlı kaydırma düzeltmesi dahil) ve ruh hali modelinin durma
sınırı (psikolojik_durum.DWELL_UST)."""
import os
import random

import spiral_ozellik as so
from psikolojik_durum import DWELL_UST

ADRES = os.environ.get("NSOSYAL_URL", "http://localhost:8000")


def _oturumlar(n=150):
    rng = random.Random(3)
    sonuc = []
    for _ in range(n):
        t, olaylar = 1000.0, []
        for _ in range(rng.randint(2, 22)):
            dwell = rng.choice([0.4, 0.8, 1.2, 1.5, 3.0, 9.0, rng.uniform(0, 30)])
            olaylar.append({"gonderi": rng.randint(0, 25), "zaman": t, "dwell": dwell, "ton": rng.uniform(-1, 1), "kelime": rng.randint(3, 50),
                            "konu": "gundem", "roket": rng.random() < .1, "yorum": rng.random() < .06})
            t += dwell + rng.uniform(0.5, 60)
        sonuc.append({"olaylar": olaylar, "simdi": t + rng.uniform(0, 300)})
    return sonuc


def test_spiral_ozellikleri_ve_ruh_hali_siniri_tarayiciyla_ayni(masaustu):
    masaustu.goto(f"{ADRES}/index.html")
    masaustu.wait_for_function("!!window.TrainedModels")
    oturumlar = _oturumlar()
    js = masaustu.evaluate("(o) => o.map(x => window.TrainedModels.spiralOzellikleri(x.olaylar, x.simdi))", oturumlar)
    for oturum, j in zip(oturumlar, js):
        py = so.ozellikler(oturum["olaylar"], oturum["simdi"])
        assert (py is None) == (j is None)
        if py:
            assert all(abs(py[ad] - j[ad]) < 1e-9 for ad in so.OZELLIK_ADLARI)
    uzun, sinir = masaustu.evaluate("""(ust) => [30, ust].map(d => window.TrainedModels.psikolojikTahmin(
        {duygu: -0.9, dwell_saniye: d, tiklama: 0, roket: 0, yorum: 0}).olasiliklar)""", DWELL_UST)
    assert uzun == sinir  # 15 sn'den uzun durma ek kanıt sayılmaz
    assert max(uzun, key=uzun.get) == "anksiyete"  # önceden olumsuzda 30 sn "umut" okunuyordu
    # Hızlı kaydırmada geçilen (1,5 sn altı) gönderiler ruh haline kanıt sayılmaz.
    hizli, karisik = masaustu.evaluate("""() => {
        const T = window.TrainedModels, simdi = 5000;
        const olay = (i, dwell, duygu) => ({zaman: simdi - 200 + i * 10, ozellik: {duygu, dwell_saniye: dwell, tiklama: 0, roket: 0, yorum: 0}});
        const hizli = Array.from({length: 12}, (_, i) => olay(i, 0.6, -0.8));
        return [T.ruhHaliPenceresi(hizli, simdi), T.ruhHaliPenceresi([...hizli, ...[0, 1, 2].map(i => olay(12 + i, 4, 0.5))], simdi)];
    }""")
    assert hizli is None
    assert karisik["kanit"] == 3 and karisik["olasiliklar"]["anksiyete"] < 0.1
