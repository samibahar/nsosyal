"""Açıklanabilir, zaman-duyarlı davranışsal karar katmanı.

Bu modül duygu *teşhisi* yapmaz. Metin tonu ve etkileşimlerden, akışın bir
kullanıcı için sürdürülebilir biçimde yoğunlaşıp yoğunlaşmadığına dair güvenli
bir oturum değerlendirmesi üretir. Skorlar hem kullanıcı açıklaması hem jüri
denetimi için aynı kaynaktan gelir.
"""
from __future__ import annotations

import math
import time
from collections import Counter

MIN_ANLAMLI_ETKILESIM = 10
MIN_NEGATIF_DWELL = 45.0
MIN_NEGATIF_ORAN = 0.55
DECAY_YARI_OMUR_SANIYE = 12 * 60


def analiz_et(gunluk: list[dict], gonderiler: list[dict], kalibrasyon: float = 0.5, now: float | None = None) -> dict:
    now = now if now is not None else time.time()
    by_id = {g["id"]: g for g in gonderiler}
    anlamli = [k for k in gunluk if _anlamli(k)]
    if not anlamli:
        return _bos_sonuc()

    agirlikli = []
    for kayit in anlamli:
        post = by_id.get(kayit["gonderi_id"])
        if not post:
            continue
        yas = max(0.0, now - kayit.get("zaman", now))
        zaman_agirligi = math.pow(0.5, yas / DECAY_YARI_OMUR_SANIYE)
        eylem_agirligi = 1.0 + (0.35 if kayit.get("tiklama") else 0) + (0.45 if kayit.get("roket") or kayit.get("yorum") else 0)
        agirlik = zaman_agirligi * eylem_agirligi
        agirlikli.append((kayit, post, agirlik))

    toplam = sum(agirlik for _, _, agirlik in agirlikli) or 1e-9
    negatif = [(k, p, a) for k, p, a in agirlikli if p.get("duygu", 0.0) < -0.2]
    negatif_agirlik = sum(a for _, _, a in negatif)
    negatif_oran = negatif_agirlik / toplam
    negatif_dwell = sum(k.get("dwell_saniye", 0.0) * a for k, _, a in negatif)
    konu_sayilari = Counter(p.get("konu", "bilinmiyor") for _, p, _ in negatif)
    baskin_konu, baskin_konu_sayisi = konu_sayilari.most_common(1)[0] if konu_sayilari else (None, 0)
    tekrar = baskin_konu_sayisi / max(1, len(negatif))
    veri_guveni = min(1.0, len(anlamli) / MIN_ANLAMLI_ETKILESIM)
    kalibrasyon = max(0.15, min(1.0, kalibrasyon))
    kanit = min(1.0, 0.45 * negatif_oran + 0.35 * min(1.0, negatif_dwell / 90) + 0.20 * tekrar)
    guven = round(veri_guveni * (0.55 + 0.45 * kalibrasyon), 3)
    yogunluk = round(kanit * guven, 3)
    yeterli = len(anlamli) >= MIN_ANLAMLI_ETKILESIM
    surdurulmus = yeterli and negatif_oran >= MIN_NEGATIF_ORAN and negatif_dwell >= MIN_NEGATIF_DWELL and tekrar >= 0.35
    nedenler = []
    if negatif_oran >= MIN_NEGATIF_ORAN:
        nedenler.append("Yoğun tonlu içeriklerdeki ağırlıklı etkileşim oranı yükseldi")
    if negatif_dwell >= MIN_NEGATIF_DWELL:
        nedenler.append("Bu içeriklerde toplam durma süresi uzadı")
    if baskin_konu and tekrar >= 0.35:
        nedenler.append(f"Benzer içeriklerde tekrar eden bir örüntü oluştu ({baskin_konu})")
    return {
        "veri_yeterli": yeterli,
        "anlamli_etkilesim": len(anlamli),
        "guven": guven,
        "akıs_yogunlugu": yogunluk,
        "surdurulmus_oruntu": surdurulmus,
        "negatif_oran": round(negatif_oran, 3),
        "negatif_dwell": round(negatif_dwell, 1),
        "tekrar_orani": round(tekrar, 3),
        "baskin_konu": baskin_konu,
        "nedenler": nedenler,
    }


def _anlamli(kayit: dict) -> bool:
    return kayit.get("dwell_saniye", 0.0) >= 1.2 or bool(kayit.get("tiklama") or kayit.get("roket") or kayit.get("yorum"))


def _bos_sonuc() -> dict:
    return {"veri_yeterli": False, "anlamli_etkilesim": 0, "guven": 0.0, "akıs_yogunlugu": 0.0, "surdurulmus_oruntu": False, "negatif_oran": 0.0, "negatif_dwell": 0.0, "tekrar_orani": 0.0, "baskin_konu": None, "nedenler": []}
