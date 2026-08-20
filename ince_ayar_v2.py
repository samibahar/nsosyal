# -*- coding: utf-8 -*-
"""İkinci tur ince ayar -- zayif_uslup_veri_uret.py'nin ürettiği, hedefli
sentetik veriyle (kısa/resmi/haber-bülteni tarzı, dolaylı duygu) mevcut
ince ayarlı modeli (ince_ayar.py'nin çıktısı) DEVAM ederek eğitir.

Neden sıfırdan değil devam: modelin winvoker'ın genel test setinde kazandığı
%94,3 doğruluğu korumak istiyoruz, sadece belgelenmiş zayıf alt-türü (haber
bülteni tarzı, ~%65) hedefliyoruz. Küçük öğrenme oranı ve az epoch, felaket
unutma (catastrophic forgetting) riskini azaltmak için.

VERİ SIZINTISI KORUMASI: bu script eğitimde SADECE zayif_uslup_veri.jsonl
(LLM üretimi, winvoker'dan tamamen bağımsız) kullanır. Bağımsız doğrulama
(dogrulama.py, winvoker split=train) ve orijinal ince ayar (split=test) ile
hiçbir örtüşmesi yok.

Sonuç ayrı bir dizine (bert-turkish-sentiment-ince-ayarli-v2) kaydedilir --
eskisinin üzerine YAZILMAZ, önce bağımsız doğrulamadan geçmeden mevcut modelin
yerini almaz.
"""
import json
import random
from pathlib import Path

import numpy as np
from datasets import Dataset
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    DataCollatorWithPadding,
    Trainer,
    TrainingArguments,
)

TABAN_MODEL_DIZINI = Path(__file__).resolve().parent / "models" / "bert-turkish-sentiment-ince-ayarli"
VERI_DOSYASI = Path(__file__).resolve().parent / "zayif_uslup_veri.jsonl"
CIKTI_DIZINI = Path(__file__).resolve().parent / "models" / "bert-turkish-sentiment-ince-ayarli-v2"
RASTGELE_TOHUM = 42

LABEL2ID = {"negative": 0, "positive": 1}


def veri_yukle():
    """JSONL'i okur ve pozitif/negatif sinifi DENGELER -- Gemini'nin gunluk
    kota siniri yuzunden pozitif tur (520) negatiften (Claude tarafindan
    dogrudan uretildi) cok daha fazla kaldi. Dengesiz veriyle egitmek modeli
    pozitife onyargili yapardi (savasy'nin zaten bilinen bir sorunu, bkz.
    CLAUDE.md) -- bu yuzden coğunluk sinifi azinliga esitlenerek altorneklenir."""
    pozitif, negatif = [], []
    with open(VERI_DOSYASI, encoding="utf-8") as f:
        for satir in f:
            satir = satir.strip()
            if not satir:
                continue
            kayit = json.loads(satir)
            if kayit.get("label") not in LABEL2ID or not kayit.get("text"):
                continue
            (pozitif if kayit["label"] == "positive" else negatif).append(kayit)

    rng = random.Random(RASTGELE_TOHUM)
    rng.shuffle(pozitif)
    rng.shuffle(negatif)
    sinif_basina = min(len(pozitif), len(negatif))
    print(f"Sinif dengesi: pozitif={len(pozitif)}, negatif={len(negatif)} "
          f"-> her ikisi de {sinif_basina}'e altorneklendi")
    kayitlar = pozitif[:sinif_basina] + negatif[:sinif_basina]
    rng.shuffle(kayitlar)
    return Dataset.from_list(kayitlar)


def main():
    if not VERI_DOSYASI.exists():
        print(f"HATA: {VERI_DOSYASI} bulunamadi. Once zayif_uslup_veri_uret.py calistirilmali.")
        return
    if not TABAN_MODEL_DIZINI.exists():
        print(f"HATA: {TABAN_MODEL_DIZINI} bulunamadi (ilk ince ayar hic yapilmamis).")
        return

    print(f"Taban model yukleniyor: {TABAN_MODEL_DIZINI}")
    tokenizer = AutoTokenizer.from_pretrained(str(TABAN_MODEL_DIZINI))
    model = AutoModelForSequenceClassification.from_pretrained(str(TABAN_MODEL_DIZINI))

    print("Hedefli veri yukleniyor...")
    veri = veri_yukle()
    print(f"Toplam ornek: {len(veri)}")
    pos_sayisi = sum(1 for x in veri["label"] if x == "positive")
    print(f"  pozitif: {pos_sayisi}  negatif: {len(veri) - pos_sayisi}")

    veri = veri.train_test_split(test_size=0.1, seed=RASTGELE_TOHUM)

    def tokenize(ornek):
        cikti = tokenizer(ornek["text"], truncation=True, max_length=96)
        cikti["labels"] = [LABEL2ID[l] for l in ornek["label"]]
        return cikti

    veri = veri.map(tokenize, batched=True, remove_columns=veri["train"].column_names)

    def compute_metrics(eval_pred):
        from sklearn.metrics import accuracy_score, f1_score
        logits, labels = eval_pred
        tahmin = np.argmax(logits, axis=-1)
        return {"dogruluk": accuracy_score(labels, tahmin), "f1": f1_score(labels, tahmin)}

    args = TrainingArguments(
        output_dir=str(CIKTI_DIZINI / "_checkpoint_gecici"),
        num_train_epochs=3,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=32,
        learning_rate=1e-5,  # ilk ince ayardan (2e-5) daha kucuk -- felaket unutmayi azalt
        eval_strategy="epoch",
        save_strategy="no",
        logging_steps=25,
        report_to=[],
    )

    egitici = Trainer(
        model=model,
        args=args,
        train_dataset=veri["train"],
        eval_dataset=veri["test"],
        compute_metrics=compute_metrics,
        data_collator=DataCollatorWithPadding(tokenizer),
    )

    print("\nIkinci tur ince ayar basliyor...\n")
    egitici.train()

    print(f"\nModel kaydediliyor: {CIKTI_DIZINI}")
    CIKTI_DIZINI.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(CIKTI_DIZINI)
    tokenizer.save_pretrained(CIKTI_DIZINI)
    print("Tamamlandi. Simdi bagimsiz dogrulama (dogrulama.py'nin v2 versiyonu) calistirilmali,")
    print("iyilesme dogrulanmadan duygu_modeli.py bu klasoru kullanmaya baslamamali.")


if __name__ == "__main__":
    main()
