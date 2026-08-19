"""
Çok kategorili "anlık psikolojik yorum" sınıflandırıcısı — spiral_model.py'nin
ikili (spiral var/yok) yaklaşımının, tek bir etkileşim anı için genişletilmiş hâli.

Her gönderi görüntüleme/etkileşim anı için 5 sinyalden (gönderinin BERT duygu
skoru, dwell-time, tıklama, roket atma, yorum atma) bir "olası psikolojik durum"
kategorisi tahmin ediyoruz: sakin, mutluluk, umut, korku, anksiyete.

ÖNEMLİ SINIRLILIK (raporda dürüstçe belirtilmeli): Bu kategoriler klinik ölçüm
değil — sadece davranışsal sinyallerden (ne kadar durdu, tıkladı mı, tepki
verdi mi) türetilmiş OLASI bir örüntü etiketi. "korku" ile "anksiyete" gibi
yakın durumları ayırt etmenin bilimsel bir üst sınırı var; biz bunu davranış
örüntüsü (donup pasif izleme vs. tekrarlayan huzursuz kontrol) üzerinden kaba
biçimde ayırt ediyoruz, gerçek bir duygu okuması iddiasında bulunmuyoruz.

Sentetik senaryo mantığı (üretici fonksiyon, spiral_model.py ile aynı ruhta):
  - sakin      : düşük dwell, düşük etkileşim, duygu nötre yakın
  - mutluluk   : pozitif duygu + roket/yorum VAR (aktif, olumlu katılım)
  - umut       : pozitif duygu + uzun dwell ama roket/yorum YOK (sessiz takip)
  - korku      : negatif duygu + uzun dwell + roket/yorum YOK, tıklama YOK (donup izleme)
  - anksiyete  : negatif duygu + KISA ama tekrar eden dwell + düşük ama sıfır
                 olmayan etkileşim (huzursuz, tekrar tekrar kontrol etme hissi)
"""
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, classification_report

RASTGELE_TOHUM = 7
rng = np.random.default_rng(RASTGELE_TOHUM)

KATEGORILER = ["sakin", "mutluluk", "umut", "korku", "anksiyete"]
OZELLIK_ADLARI = ["duygu", "dwell_saniye", "tiklama", "roket", "yorum"]


def _senaryo_uret(n_kategori: int):
    """Her kategoriden n_kategori adet sentetik etkileşim örneği üretir."""
    satirlar, etiketler = [], []

    def ekle(kategori, duygu, dwell, tiklama, roket, yorum):
        satirlar.append([duygu, dwell, tiklama, roket, yorum])
        etiketler.append(kategori)

    for _ in range(n_kategori):
        # sakin: nötre yakın duygu, kısa dwell, neredeyse hiç etkileşim yok
        ekle("sakin",
             duygu=np.clip(rng.normal(0, 0.15), -1, 1),
             dwell=max(0.3, rng.gamma(1.5, 1.2)),
             tiklama=int(rng.random() < 0.05),
             roket=int(rng.random() < 0.02),
             yorum=int(rng.random() < 0.01))

        # mutluluk: pozitif duygu + aktif, olumlu katılım (roket/yorum sık)
        ekle("mutluluk",
             duygu=np.clip(rng.normal(0.7, 0.2), -1, 1),
             dwell=max(0.3, rng.gamma(2.0, 2.0)),
             tiklama=int(rng.random() < 0.5),
             roket=int(rng.random() < 0.65),
             yorum=int(rng.random() < 0.35))

        # umut: pozitif duygu + uzun sessiz takip, roket/yorum nadir
        ekle("umut",
             duygu=np.clip(rng.normal(0.55, 0.2), -1, 1),
             dwell=max(0.3, rng.gamma(4.0, 2.5)),
             tiklama=int(rng.random() < 0.15),
             roket=int(rng.random() < 0.1),
             yorum=int(rng.random() < 0.05))

        # korku: negatif duygu + uzun donup-izleme, hiç etkileşim yok
        ekle("korku",
             duygu=np.clip(rng.normal(-0.75, 0.2), -1, 1),
             dwell=max(0.3, rng.gamma(5.0, 2.5)),
             tiklama=int(rng.random() < 0.03),
             roket=int(rng.random() < 0.01),
             yorum=int(rng.random() < 0.01))

        # anksiyete: negatif duygu + kısa-tekrarlı dwell, huzursuz düşük etkileşim
        ekle("anksiyete",
             duygu=np.clip(rng.normal(-0.6, 0.25), -1, 1),
             dwell=max(0.3, rng.gamma(1.3, 1.8)),
             tiklama=int(rng.random() < 0.2),
             roket=int(rng.random() < 0.03),
             yorum=int(rng.random() < 0.08))

    X = np.array(satirlar, dtype=float)
    y = np.array(etiketler)

    # %10 etiket gürültüsü: gerçek dünyada bu sınırlar asla net değil
    n = len(y)
    gurultu_idx = rng.choice(n, size=int(n * 0.10), replace=False)
    y[gurultu_idx] = rng.choice(KATEGORILER, size=len(gurultu_idx))

    return X, y


def egit_ve_degerlendir(kategori_basina: int = 500):
    X, y = _senaryo_uret(kategori_basina)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=RASTGELE_TOHUM, stratify=y
    )
    model = LogisticRegression(max_iter=2000)  # >2 sınıf + lbfgs -> otomatik multinomial (softmax)
    model.fit(X_train, y_train)
    tahmin = model.predict(X_test)

    sonuc = {
        "model": model,
        "dogruluk": accuracy_score(y_test, tahmin),
        "f1_makro": f1_score(y_test, tahmin, average="macro"),
        "rapor": classification_report(y_test, tahmin, target_names=model.classes_),
    }
    return sonuc


_EGITIM = egit_ve_degerlendir()
_MODEL = _EGITIM["model"]


def psikolojik_durum_tahmini(duygu: float, dwell_saniye: float, tiklama: bool,
                               roket: bool = False, yorum: bool = False) -> dict:
    """Tek bir etkileşim anı için kategori olasılık dağılımını döndürür."""
    X = np.array([[duygu, dwell_saniye, int(tiklama), int(roket), int(yorum)]])
    olasiliklar = _MODEL.predict_proba(X)[0]
    dagilim = {str(kat): round(float(p), 3) for kat, p in zip(_MODEL.classes_, olasiliklar)}
    baskin = max(dagilim, key=dagilim.get)
    return {"kategori": baskin, "olasiliklar": dagilim}


if __name__ == "__main__":
    print(f"Eğitim: kategori başına 500 sentetik örnek, özellikler: {OZELLIK_ADLARI}\n")
    print(f"Doğruluk: {_EGITIM['dogruluk']:.3f}")
    print(f"F1 (makro): {_EGITIM['f1_makro']:.3f}\n")
    print(_EGITIM["rapor"])

    print("Örnek tahminler:")
    ornekler = [
        dict(duygu=0.9, dwell_saniye=3, tiklama=True, roket=True, yorum=False),
        dict(duygu=-0.8, dwell_saniye=12, tiklama=False, roket=False, yorum=False),
        dict(duygu=-0.6, dwell_saniye=2, tiklama=True, roket=False, yorum=False),
        dict(duygu=0.05, dwell_saniye=0.8, tiklama=False, roket=False, yorum=False),
    ]
    for o in ornekler:
        sonuc = psikolojik_durum_tahmini(**o)
        print(f"  {o} -> {sonuc['kategori']} {sonuc['olasiliklar']}")
