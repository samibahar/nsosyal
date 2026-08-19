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
"sakin" kategorisi bilinçli olarak eklendi: davranışsal sinyal zayıf/nötr
olduğunda modelin zorla bir duyguya (örn. anksiyete) yönelmesini önler, "her
şey bir duygudur" gibi aşırı iddialı bir çıkarımdan kaçınmamızı sağlar.
Arayüzde tek bir "baskın" etiket yerine TÜM kategorilerin olasılık çubukları
birlikte gösterilir — bu da tek bir zayıf sinyalin kesin bir teşhis gibi
görünmesini engeller.

DAYANAK (bu bir "kanıtlanmış model" değil, iki bacaklı bir yaklaşım):
  1) Sentetik senaryoların TASARIMI keyfi değil, dijital davranış/HCI
     literatüründe sık işlenen genel kavramlarla kabaca uyumlu: edilgen/uzun
     süreli tüketimin dikkat sabitlenmesi (rumination) ile ilişkilendirilmesi,
     aktif katılımın (beğeni/yorum) olumlu duygulanımla ilişkilendirilmesi,
     hızlı-tekrarlı kontrol davranışının huzursuzluk/kompulsif kontrol
     örüntüleriyle ilişkilendirilmesi gibi genel kabul gören fikirler. Bu,
     kesin akademik parametre KAYNAĞI değil, tasarım kararlarının rastgele
     olmadığının gerekçesidir.
  2) Gerçek dayanak: backend/main.py'deki KENDİ KENDİNİ DOĞRULAMA döngüsü.
     Kullanıcıya ara sıra "şu an gerçekte nasıl hissediyorsun?" sorusu
     sorulur, cevabı modelin o anki tahminiyle karşılaştırılır ve eşleşme
     oranı /api/dogrulama-ozet üzerinden şeffafça raporlanır. Modelin gerçek
     performansı budur -- iddia değil, ölçüm.

KİŞİSELLEŞTİRME (çevrimiçi/online öğrenme, isteğe bağlı): _VARSAYILAN_MODEL
hiç değişmeyen, sabit bir kopyadır. Backend ayrıca her kullanıcı için bir
_KISISEL kopya tutabilir ve her doğrulama cevabından sonra kisisel_guncelle()
ile bu kopyada TEK KÜÇÜK bir SGD adımı atılır (eta0 çok küçük olduğu için tek
bir gürültülü/yanlış cevap modeli neredeyse hiç etkilemez, ama tutarlı bir
örüntü zamanla birikip fark yaratır). Bu, gerçek uzun-vadeli, çok-kullanıcılı
bir kişiselleştirme iddiası DEĞİL -- tek bir demo oturumunda bile MEKANİZMANIN
çalıştığını göstermek için arayüzdeki "Varsayılan / Kişiselleştirilmiş" anahtarı
ile karşılaştırılabilir hale getirildi.

Sentetik senaryo mantığı (üretici fonksiyon, spiral_model.py ile aynı ruhta):
  - sakin      : düşük dwell, düşük etkileşim, duygu nötre yakın
  - mutluluk   : pozitif duygu + roket/yorum VAR (aktif, olumlu katılım)
  - umut       : pozitif duygu + uzun dwell ama roket/yorum YOK (sessiz takip)
  - korku      : negatif duygu + uzun dwell + roket/yorum YOK, tıklama YOK (donup izleme)
  - anksiyete  : negatif duygu + KISA ama tekrar eden dwell + düşük ama sıfır
                 olmayan etkileşim (huzursuz, tekrar tekrar kontrol etme hissi)
"""
import copy

import numpy as np
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, classification_report

RASTGELE_TOHUM = 7
rng = np.random.default_rng(RASTGELE_TOHUM)

KATEGORILER = ["sakin", "mutluluk", "umut", "korku", "anksiyete"]
OZELLIK_ADLARI = ["duygu", "dwell_saniye", "tiklama", "roket", "yorum"]

# Kişiselleştirme (online SGD adımları) için öğrenme oranı. NOT: gerçek üretimde
# (binlerce kullanıcı, aylarca veri) bu çok daha küçük olurdu (örn. 0.0005) --
# burada, bir demo OTURUMUNDA az sayıda onayla bile mekanizmanın görünür şekilde
# çalıştığını gösterebilmek için kasıtlı olarak büyütüldü. Bu bir "gerçek
# kişiselleştirme kalibrasyonu" iddiası değil, mekanizmanın kanıt-of-konseptidir.
KISISEL_ETA0 = 0.12


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
    # SGDClassifier(loss="log_loss") = çevrimiçi (partial_fit destekli) lojistik
    # regresyon -- kişiselleştirme (bkz. dosya başı) bunun üzerine kuruluyor.
    # Tam-parti .fit() ile eğitildiğinde LogisticRegression'a denk sonuç verir.
    model = SGDClassifier(loss="log_loss", learning_rate="constant", eta0=KISISEL_ETA0,
                           random_state=RASTGELE_TOHUM, max_iter=1000)
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
_VARSAYILAN_MODEL = _EGITIM["model"]  # ASLA değişmez -- karşılaştırma referansı
_KATEGORI_DIZISI = np.array(KATEGORILER)


def kisisel_model_olustur():
    """Varsayılan modelin bağımsız bir kopyasını döndürür -- bu kopya
    kisisel_guncelle() ile zamanla varsayılandan sapabilir."""
    return copy.deepcopy(_VARSAYILAN_MODEL)


def kisisel_guncelle(model, ozellik: list, gercek_kategori: str):
    """Kullanıcının onayladığı GERÇEK kategoriyle modelde tek küçük bir SGD
    adımı atar. KISISEL_ETA0 çok küçük olduğu için tek bir gürültülü/yanlış
    cevap modeli neredeyse hiç etkilemez; tutarlı bir örüntü biriktikçe fark
    yaratır. `model` parametresi YERİNDE (in-place) güncellenir."""
    X = np.array([ozellik], dtype=float)
    y = np.array([gercek_kategori])
    model.partial_fit(X, y, classes=_KATEGORI_DIZISI)


def psikolojik_durum_tahmini(duygu: float, dwell_saniye: float, tiklama: bool,
                               roket: bool = False, yorum: bool = False, model=None) -> dict:
    """Tek bir etkileşim anı için kategori olasılık dağılımını döndürür.
    `model` verilmezse VARSAYILAN (hiç değişmeyen) model kullanılır."""
    model = model if model is not None else _VARSAYILAN_MODEL
    X = np.array([[duygu, dwell_saniye, int(tiklama), int(roket), int(yorum)]])
    olasiliklar = model.predict_proba(X)[0]
    dagilim = {str(kat): round(float(p), 3) for kat, p in zip(model.classes_, olasiliklar)}
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
