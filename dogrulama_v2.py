# -*- coding: utf-8 -*-
"""ince_ayar_v2.py'nin ciktisini (models/bert-turkish-sentiment-ince-ayarli-v2)
IKI bagimsiz test setinde olcer:
1) winvoker'in 1000 orneklik bagimsiz seti (dogrulama.py ile AYNI metodoloji,
   split=train, seed=42) -- v1'in %94.3 dogrulugunu kaybetmedik mi kontrolu.
2) NSosyal'in kendi 150 demo gonderisi -- zayif alt-tur (kisa/resmi/haber
   bulteni tarzi) gercekten iyilesti mi kontrolu.

Hicbiri egitim verisiyle (zayif_uslup_veri.jsonl) ortusmuyor -- veri sizintisi yok.
"""
import random

from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
from datasets import load_dataset
from sklearn.metrics import accuracy_score, f1_score

from ornek_veri import ORNEK_GONDERILER

MODEL_DIZINI = "models/bert-turkish-sentiment-ince-ayarli-v2"
V1_DIZINI = "models/bert-turkish-sentiment-ince-ayarli"
RASTGELE_TOHUM = 42
ORNEKLEM_BUYUKLUGU = 1000

print(f"Model yukleniyor: {MODEL_DIZINI}")
tokenizer = AutoTokenizer.from_pretrained(MODEL_DIZINI)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIZINI)
sa = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

print(f"V1 (kiyaslama) modeli yukleniyor: {V1_DIZINI}")
tokenizer_v1 = AutoTokenizer.from_pretrained(V1_DIZINI)
model_v1 = AutoModelForSequenceClassification.from_pretrained(V1_DIZINI)
sa_v1 = pipeline("sentiment-analysis", model=model_v1, tokenizer=tokenizer_v1)


def duygu_skoru(metin, pipe=None):
    pipe = pipe or sa
    sonuc = pipe(metin, truncation=True)[0]
    etiket = sonuc["label"].lower()
    isaret = 1.0 if ("pos" in etiket or etiket in ("1", "label_1")) else -1.0
    return isaret * sonuc["score"]


# ---------- TEST 1: winvoker bagimsiz set (v1 ile birebir ayni yontem) ----------
print("\n" + "=" * 70)
print("TEST 1: winvoker bagimsiz 1000 ornek (v1'in %94.3 sonucuyla kiyaslamak icin)")
print("=" * 70)

veri = load_dataset("winvoker/turkish-sentiment-analysis-dataset", split="train")
random.seed(RASTGELE_TOHUM)
indeksler = random.sample(range(len(veri)), ORNEKLEM_BUYUKLUGU)
ornek = veri.select(indeksler)

ikili_gercek, ikili_tahmin = [], []
for i, satir in enumerate(ornek):
    if i % 200 == 0:
        print(f"  {i}/{ORNEKLEM_BUYUKLUGU}...")
    metin = str(satir["text"])[:512]
    gercek = str(satir["label"]).strip().lower()
    if gercek == "notr":
        continue
    skor = duygu_skoru(metin)
    tahmin = "positive" if skor > 0 else "negative"
    ikili_gercek.append(gercek)
    ikili_tahmin.append(tahmin)

dogruluk1 = accuracy_score(ikili_gercek, ikili_tahmin)
f1_1 = f1_score(ikili_gercek, ikili_tahmin, pos_label="positive")
print(f"\nWINVOKER BAGIMSIZ DOGRULUK: {dogruluk1:.4f}  (v1: 0.943)")
print(f"WINVOKER BAGIMSIZ F1: {f1_1:.4f}  (v1: 0.964)")

# ---------- TEST 2: kendi 150 demo gonderimiz (zayif alt-tur) ----------
print("\n" + "=" * 70)
print("TEST 2: kendi 150 demo gonderimiz (zayif alt-tur, v1/orijinal ~%65 idi)")
print("=" * 70)
print("NOT: bu 150 gonderinin GERCEK/dogru etiketi elimizde yok (hicbir zaman")
print("elle etiketlenmedi) -- bu yuzden 'dogruluk' hesaplayamayiz, sadece")
print("modelin YON DAGILIMINI (kac tanesini pozitif/negatif tahmin ettigini)")
print("ve birkac ornegi manuel gozle kontrol icin yazdiriyoruz.")

pozitif_sayisi = 0
negatif_sayisi = 0
sonuclar = []
for g in ORNEK_GONDERILER:
    skor = duygu_skoru(g["metin"])
    tahmin = "positive" if skor > 0 else "negative"
    if tahmin == "positive":
        pozitif_sayisi += 1
    else:
        negatif_sayisi += 1
    sonuclar.append({"metin": g["metin"], "tahmin": tahmin, "skor": round(skor, 3)})

print(f"\nToplam {len(ORNEK_GONDERILER)} gonderi. Pozitif: {pozitif_sayisi}  Negatif: {negatif_sayisi}")

with open("v2_150_demo_sonuc.txt", "w", encoding="utf-8") as f:
    for s in sonuclar:
        f.write(f"[{s['tahmin']:>8} {s['skor']:+.3f}] {s['metin']}\n")
print("Detayli sonuclar v2_150_demo_sonuc.txt'e yazildi (manuel karsilastirma icin).")

# ---------- TEST 3: v1 vs v2 dogrudan karsilastirma (150 demo) ----------
print("\n" + "=" * 70)
print("TEST 3: v1 (mevcut) vs v2 (yeni) -- ayni 150 gonderide FARKLI tahmin edilenler")
print("=" * 70)

farklilar = []
for g in ORNEK_GONDERILER:
    skor_v2 = duygu_skoru(g["metin"], sa)
    skor_v1 = duygu_skoru(g["metin"], sa_v1)
    tahmin_v2 = "positive" if skor_v2 > 0 else "negative"
    tahmin_v1 = "positive" if skor_v1 > 0 else "negative"
    if tahmin_v1 != tahmin_v2:
        farklilar.append({"metin": g["metin"], "v1": tahmin_v1, "v2": tahmin_v2})

print(f"Toplam {len(farklilar)} gonderide v1 ve v2 FARKLI tahmin verdi (150 uzerinden).")
with open("v1_v2_farklari.txt", "w", encoding="utf-8") as f:
    f.write(f"Toplam {len(farklilar)} farkli tahmin\n\n")
    for i, d in enumerate(farklilar):
        f.write(f"{i+1}. [v1: {d['v1']:>8}] [v2: {d['v2']:>8}] {d['metin']}\n\n")
print("Farklar v1_v2_farklari.txt'e yazildi -- manuel okuyup hangisinin dogru oldugunu degerlendirecegiz.")
