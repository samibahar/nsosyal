"""
duygu_modeli.py'nin (BERT) BAĞIMSIZ bir Türkçe veri seti üzerinde doğrulanması.
Amaç: modelin kendi kart bilgisindeki %95.4 doğruluk iddiasına güvenmek yerine,
kendi bağımsız ölçümümüzü çıkarmak.

Veri kaynağı: winvoker/turkish-sentiment-analysis-dataset (HuggingFace, ~492k
etiketli Türkçe cümle — haber, ürün yorumu, sosyal medya gibi karışık kaynaklardan).
X/Twitter'dan canlı veri çekmek ToS ihlali ve altyapı riski taşıdığı için (X'in
öneri algoritmasını yeniden üretmek kendi kullanıcı grafiğimiz olmadan mümkün
değil), bunun yerine hazır/lisanslı, büyük ölçekli bir Türkçe veri setinden
rastgele 1000 cümlelik bir örneklem alınıyor.

Model ikili (pozitif/negatif) sınıflandırma yaptığı için "Notr" etiketli
cümleler ikili karşılaştırmanın dışında tutulur ama ayrı raporlanır — bu,
modelin bilinen bir sınırlılığı (nötr sınıfı yok).
"""
import random

from datasets import load_dataset
from sklearn.metrics import accuracy_score, f1_score, classification_report

from duygu_modeli import duygu_skoru

RASTGELE_TOHUM = 42
ORNEKLEM_BUYUKLUGU = 1000


def veri_orneklemi_al():
    veri = load_dataset("winvoker/turkish-sentiment-analysis-dataset", split="train")
    random.seed(RASTGELE_TOHUM)
    indeksler = random.sample(range(len(veri)), ORNEKLEM_BUYUKLUGU)
    return veri.select(indeksler)


def dogrula():
    ornek = veri_orneklemi_al()
    ikili_gercek, ikili_tahmin = [], []
    notr_sayisi = 0
    notr_dogru_yon_sayisi = 0  # bilgi amaçlı: nötr cümlelerde model hangi yöne kayıyor
    sonuclar = []

    for satir in ornek:
        metin = str(satir["text"])[:512]
        gercek_etiket = str(satir["label"]).strip().lower()
        skor = duygu_skoru(metin)
        tahmin_etiket = "positive" if skor > 0 else "negative"

        sonuclar.append({
            "metin": metin, "gercek": gercek_etiket,
            "tahmin": tahmin_etiket, "skor": round(skor, 3),
        })

        if gercek_etiket == "notr":
            notr_sayisi += 1
            if tahmin_etiket == "positive":
                notr_dogru_yon_sayisi += 1
            continue

        ikili_gercek.append(gercek_etiket)
        ikili_tahmin.append(tahmin_etiket)

    dogruluk = accuracy_score(ikili_gercek, ikili_tahmin)
    f1 = f1_score(ikili_gercek, ikili_tahmin, pos_label="positive")

    print(f"Toplam örneklem: {ORNEKLEM_BUYUKLUGU} (winvoker/turkish-sentiment-analysis-dataset, rastgele)")
    print(f"Nötr etiketli (ikili karşılaştırma dışı bırakıldı): {notr_sayisi}")
    print(f"  -> bunların {notr_dogru_yon_sayisi}'i model tarafından 'pozitif' yönüne yuvarlandı")
    print(f"İkili karşılaştırmaya giren: {len(ikili_gercek)}\n")
    print(f"Bağımsız doğruluk: {dogruluk:.3f}")
    print(f"Bağımsız F1: {f1:.3f}\n")
    print(classification_report(ikili_gercek, ikili_tahmin, digits=3))

    return sonuclar


if __name__ == "__main__":
    dogrula()
