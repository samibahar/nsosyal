"""
savasy/bert-base-turkish-sentiment-cased modelini, dogrulama.py'de bulduğumuz
alan kayması (domain shift) sorununu azaltmak için winvoker/turkish-sentiment-
analysis-dataset üzerinde devam ederek ince ayar (continued fine-tuning) yapar.

VERİ SIZINTISI KORUMASI: dogrulama.py'deki 1000 örneklik bağımsız test seti
winvoker'ın split="train" bölümünden geliyordu (seed=42). Bu script kasıtlı
olarak split="test" bölümünü kullanır — ikisi tamamen ayrık, "önce/sonra"
karşılaştırması veri sızıntısıyla şişirilmiş olmaz.

CPU'da eğitildiği için veri alt örneklemi (denge için ~15.000, sınıf başına
eşit) kullanılıyor, tüm 492k satır değil. Amaç mükemmel bir model değil,
mevcut modelin alan kaymasını ölçülebilir biçimde azaltmak.
"""
import random
from pathlib import Path

import numpy as np
from datasets import load_dataset
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    DataCollatorWithPadding,
    Trainer,
    TrainingArguments,
)

MODEL_ADI = "savasy/bert-base-turkish-sentiment-cased"
CIKTI_DIZINI = Path(__file__).resolve().parent / "models" / "bert-turkish-sentiment-ince-ayarli"
SINIF_BASINA_ORNEK = 7500  # dengeli ~15.000 toplam eğitim örneği
RASTGELE_TOHUM = 42

LABEL2ID = {"negative": 0, "positive": 1}


def veri_hazirla(tokenizer):
    veri = load_dataset("winvoker/turkish-sentiment-analysis-dataset", split="test")
    veri = veri.filter(lambda x: str(x["label"]).strip().lower() in ("positive", "negative"))

    rng = random.Random(RASTGELE_TOHUM)
    pos_idx = [i for i, l in enumerate(veri["label"]) if str(l).strip().lower() == "positive"]
    neg_idx = [i for i, l in enumerate(veri["label"]) if str(l).strip().lower() == "negative"]
    rng.shuffle(pos_idx)
    rng.shuffle(neg_idx)
    secili_idx = pos_idx[:SINIF_BASINA_ORNEK] + neg_idx[:SINIF_BASINA_ORNEK]
    rng.shuffle(secili_idx)

    veri = veri.select(secili_idx)
    veri = veri.train_test_split(test_size=0.1, seed=RASTGELE_TOHUM)

    def tokenize(ornek):
        # padding="max_length" DEĞİL: her cümleyi 96 token'a zorla doldurmak
        # yerine, dinamik padding (DataCollatorWithPadding) kullanılıyor --
        # her grup sadece kendi içindeki en uzun cümleye göre dolduruluyor.
        # Kısa Türkçe haber cümlelerinin çoğu 96'nın çok altında olduğu için
        # bu, SONUCU DEĞİŞTİRMEDEN (attention karesel olduğundan) hesaplamayı
        # ciddi oranda azaltır -- kalite kaybı yok, sadece hız kazancı.
        cikti = tokenizer(ornek["text"], truncation=True, max_length=96)
        cikti["labels"] = [LABEL2ID[str(l).strip().lower()] for l in ornek["label"]]
        return cikti

    veri = veri.map(tokenize, batched=True, remove_columns=veri["train"].column_names)
    return veri["train"], veri["test"]


def compute_metrics(eval_pred):
    from sklearn.metrics import accuracy_score, f1_score
    logits, labels = eval_pred
    tahmin = np.argmax(logits, axis=-1)
    return {
        "dogruluk": accuracy_score(labels, tahmin),
        "f1": f1_score(labels, tahmin),
    }


def main():
    print(f"Model yükleniyor: {MODEL_ADI}")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ADI)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_ADI)

    print("Veri hazırlanıyor (winvoker split=test, sınıf başına "
          f"{SINIF_BASINA_ORNEK} örnek)...")
    egitim_seti, dogrulama_seti = veri_hazirla(tokenizer)
    print(f"Eğitim: {len(egitim_seti)}  |  İç doğrulama: {len(dogrulama_seti)}")

    args = TrainingArguments(
        output_dir=str(CIKTI_DIZINI / "_checkpoint_gecici"),
        num_train_epochs=2,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=32,
        learning_rate=2e-5,
        eval_strategy="epoch",
        save_strategy="no",
        logging_steps=50,
        report_to=[],
    )

    egitici = Trainer(
        model=model,
        args=args,
        train_dataset=egitim_seti,
        eval_dataset=dogrulama_seti,
        compute_metrics=compute_metrics,
        data_collator=DataCollatorWithPadding(tokenizer),  # dinamik padding
    )

    print("İnce ayar başlıyor...\n")
    egitici.train()

    print(f"\nModel kaydediliyor: {CIKTI_DIZINI}")
    CIKTI_DIZINI.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(CIKTI_DIZINI)
    tokenizer.save_pretrained(CIKTI_DIZINI)
    print("Tamamlandı.")


if __name__ == "__main__":
    main()
