"""
Spiral sınıflandırıcı — gerçek eğitilmiş model (scikit-learn), spike_poc.py'deki
kaba "15 saniyeden fazla negatif içerikte kalma = spiral" kuralının yerini alır.

Gerçek kullanıcı davranış verisi yok (platform henüz bize API erişimi vermiyor),
bu yüzden CLAUDE.md'de kararlaştırıldığı gibi küçük, senaryo-bazlı SENTETİK bir
veri seti kullanıyoruz. Etiketler kural-tabanlı ama doğrusal olmayan bir üretici
fonksiyondan + %8 etiket gürültüsünden geliyor, ki model gerçek sinyali gürültüden
ayırt etmeyi öğrensin ve F1/doğruluk metrikleri gerçekçi (mükemmel değil) çıksın.

Bu, raporda "önerilen bir yöntem kanıtı" olarak sunulmalı — gerçek kullanıcı
verisiyle yeniden eğitilmesi gerektiği açıkça belirtilmeli.
"""
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report

RASTGELE_TOHUM = 42
rng = np.random.default_rng(RASTGELE_TOHUM)

# ---------------------------------------------------------------------------
# 1) Sentetik senaryo üretimi
# ---------------------------------------------------------------------------
# Her örnek, kullanıcının son ~10-15 dakikalık davranış penceresini temsil eden
# özet özellikler:
#   negatif_dwell_toplam   -> negatif içerikte (duygu < -0.2) geçirilen toplam sn
#   negatif_dwell_orani    -> negatif dwell / toplam dwell
#   negatif_tekrar_sayisi  -> art arda/tekrar negatif içeriğe dönme sayısı
#   ortalama_duygu         -> görüntülenen içeriklerin ortalama duygu skoru
#   tiklama_orani          -> tıklama sayısı / görüntülenen gönderi sayısı
#   kaydirma_hizi          -> dakikada görüntülenen gönderi sayısı (hızlı geçiş)
OZELLIK_ADLARI = [
    "negatif_dwell_toplam", "negatif_dwell_orani", "negatif_tekrar_sayisi",
    "ortalama_duygu", "tiklama_orani", "kaydirma_hizi",
]


def _senaryo_uret(n: int):
    negatif_dwell_toplam = rng.gamma(shape=2.0, scale=8.0, size=n)          # sn
    negatif_dwell_orani = np.clip(rng.beta(2, 3, size=n), 0, 1)
    negatif_tekrar_sayisi = rng.poisson(lam=1.5, size=n).astype(float)
    ortalama_duygu = rng.normal(loc=-0.1, scale=0.4, size=n)
    ortalama_duygu = np.clip(ortalama_duygu, -1, 1)
    tiklama_orani = np.clip(rng.beta(2, 5, size=n), 0, 1)
    kaydirma_hizi = rng.gamma(shape=3.0, scale=4.0, size=n)                  # gönderi/dk

    X = np.column_stack([
        negatif_dwell_toplam, negatif_dwell_orani, negatif_tekrar_sayisi,
        ortalama_duygu, tiklama_orani, kaydirma_hizi,
    ])

    # Doğrusal olmayan, gerçekçi bir "gerçek spiral" üretici fonksiyon:
    # yüksek negatif dwell + yüksek tekrar + düşük tıklama (pasif tüketim) +
    # yüksek kaydırma hızı (doomscroll) -> spiral olasılığı artar.
    logit = (
        0.09 * negatif_dwell_toplam
        + 2.2 * negatif_dwell_orani
        + 0.55 * negatif_tekrar_sayisi
        - 1.8 * ortalama_duygu
        - 1.4 * tiklama_orani
        + 0.05 * kaydirma_hizi
        - 3.2
    )
    olasilik = 1 / (1 + np.exp(-logit))
    y = (rng.random(n) < olasilik).astype(int)

    # %8 etiket gürültüsü: gerçek dünyada dwell-time/tıklama gibi dolaylı
    # sinyaller her zaman gerçek duygu durumunu yansıtmaz.
    gurultu_maskesi = rng.random(n) < 0.08
    y[gurultu_maskesi] = 1 - y[gurultu_maskesi]

    return X, y


def veri_seti_olustur(n: int = 2000):
    X, y = _senaryo_uret(n)
    return X, y


# ---------------------------------------------------------------------------
# 2) Eğitim + değerlendirme
# ---------------------------------------------------------------------------
def egit_ve_degerlendir():
    X, y = veri_seti_olustur(2000)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=RASTGELE_TOHUM, stratify=y
    )

    modeller = {
        "Lojistik Regresyon": LogisticRegression(max_iter=1000),
        "Gradient Boosting": GradientBoostingClassifier(random_state=RASTGELE_TOHUM),
    }

    sonuclar = {}
    for ad, model in modeller.items():
        model.fit(X_train, y_train)
        tahmin = model.predict(X_test)
        sonuclar[ad] = {
            "model": model,
            "dogruluk": accuracy_score(y_test, tahmin),
            "f1": f1_score(y_test, tahmin),
            "precision": precision_score(y_test, tahmin),
            "recall": recall_score(y_test, tahmin),
            "rapor": classification_report(y_test, tahmin, target_names=["spiral_degil", "spiral"]),
        }
    return sonuclar, (X_train, X_test, y_train, y_test)


if __name__ == "__main__":
    sonuclar, _ = egit_ve_degerlendir()
    print(f"Eğitim verisi: 2000 sentetik senaryo, özellikler: {OZELLIK_ADLARI}\n")
    for ad, s in sonuclar.items():
        print(f"=== {ad} ===")
        print(f"  Doğruluk : {s['dogruluk']:.3f}")
        print(f"  F1       : {s['f1']:.3f}")
        print(f"  Precision: {s['precision']:.3f}")
        print(f"  Recall   : {s['recall']:.3f}")
        print(s["rapor"])
