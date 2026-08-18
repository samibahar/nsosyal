"""
İki katmanlı, açıklanabilir sıralama motoru — spike_poc.py'nin mimarisini
gerçek bileşenlerle (duygu_modeli.py: BERT, spiral_model.py: eğitilmiş
sınıflandırıcı) birleştiren üretim modülü. FastAPI backend'i bunu kullanır.
"""
import numpy as np

from duygu_modeli import duygu_skoru
from spiral_model import egit_ve_degerlendir

# Spiral sınıflandırıcı, süreç başlarken bir kere eğitilir ve bellekte tutulur
# (gerçek üretimde bu, önceden eğitilip diske kaydedilmiş bir model dosyası olurdu).
_egitim_sonuclari, _ = egit_ve_degerlendir()
_SPIRAL_MODEL = _egitim_sonuclari["Lojistik Regresyon"]["model"]


def gonderileri_puanla(gonderiler: list[dict]) -> list[dict]:
    """Her gönderiye BERT ile gerçek bir duygu_skoru ekler (yoksa)."""
    for g in gonderiler:
        if "duygu" not in g:
            g["duygu"] = duygu_skoru(g["metin"])
    return gonderiler


def _ozellik_cikar(log: list[dict], gonderiler: list[dict]) -> np.ndarray:
    """Ham davranış günlüğünü (gonderi_id, dwell_saniye, tiklama), spiral
    sınıflandırıcının beklediği 6 özniteliğe indirger."""
    if not log:
        return np.zeros((1, 6))

    id_to_gonderi = {g["id"]: g for g in gonderiler}
    dwell = np.array([k["dwell_saniye"] for k in log], dtype=float)
    duygular = np.array([id_to_gonderi[k["gonderi_id"]]["duygu"] for k in log])
    tiklamalar = np.array([1.0 if k.get("tiklama") else 0.0 for k in log])

    negatif_maske = duygular < -0.2
    toplam_dwell = dwell.sum() or 1e-9

    negatif_dwell_toplam = dwell[negatif_maske].sum()
    negatif_dwell_orani = negatif_dwell_toplam / toplam_dwell

    negatif_id_listesi = [k["gonderi_id"] for i, k in enumerate(log) if negatif_maske[i]]
    negatif_tekrar_sayisi = len(negatif_id_listesi) - len(set(negatif_id_listesi))

    ortalama_duygu = duygular.mean()
    tiklama_orani = tiklamalar.mean()
    kaydirma_hizi = len(log) / max(toplam_dwell / 60.0, 0.1)

    return np.array([[
        negatif_dwell_toplam, negatif_dwell_orani, negatif_tekrar_sayisi,
        ortalama_duygu, tiklama_orani, kaydirma_hizi,
    ]])


def spiral_olasiligi(log: list[dict], gonderiler: list[dict]) -> float:
    """Eğitilmiş sınıflandırıcıdan 0-1 arası spiral olasılığı döndürür."""
    X = _ozellik_cikar(log, gonderiler)
    return float(_SPIRAL_MODEL.predict_proba(X)[0][1])


def sirala(gonderiler: list[dict], ilgi: dict, spiral_seviyesi: float) -> list[dict]:
    """spike_poc.py'deki iki katmanlı skor motoru — davranış değişmedi, girdiler
    artık gerçek modellerden geliyor."""
    sonuc = []
    for g in gonderiler:
        ilgi_skoru = ilgi.get(g["konu"], 0.3)
        refah_cezasi = spiral_seviyesi * max(0, -g["duygu"]) * 0.8
        final_skor = ilgi_skoru - refah_cezasi
        sonuc.append({
            **g,
            "ilgi_skoru": round(ilgi_skoru, 2),
            "refah_cezasi": round(refah_cezasi, 2),
            "final_skor": round(final_skor, 2),
            "aciklama": (f"İlgi alanınla eşleşiyor ({g['konu']}, skor {ilgi_skoru})"
                         + (f", ama şu an olası bir spiral tespit ettiğimiz için "
                            f"{round(refah_cezasi,2)} puan yumuşattık" if refah_cezasi > 0 else "")),
        })
    return sorted(sonuc, key=lambda x: -x["final_skor"])
