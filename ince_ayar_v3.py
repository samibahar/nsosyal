# -*- coding: utf-8 -*-
"""Üçüncü tur ince ayar: NÖTR sınıfı ekleme (aşırı kesinlik düzeltmesi).

SORUN (11.09.2026 ölçümü): v2 ikili (pozitif/negatif) bir sınıflandırıcı ve
duygu skoru = işaret × sınıflandırıcı güveni. 250 demo gönderinin %94'ünde
|ton| > 0,9 çıktı, nötre yakın (|ton| ≤ 0,3) hiç gönderi yoktu. Dengeleme
cezası |ton| ile orantılı olduğu için pratikte açık/kapalı çalışıyor, olgusal
bir duyuru da "çok olumsuz" sayılabiliyordu. Sınıflandırıcının kendinden
emin olması, metnin duygusal olarak YOĞUN olduğu anlamına gelmez.

ÇÖZÜM: v2'yi üç sınıfa (negatif / nötr / pozitif) genişletip winvoker'ın
"Notr" etiketli örnekleriyle devam ederek eğitmek. Ton artık
P(pozitif) − P(negatif): nötr bir metinde iki olasılık da küçük kalır ve ton
sıfıra yaklaşır; karışık bir metin ara bir değer alır.

BAŞLANGIÇ: yeni 3'lü sınıflandırıcı katmanı rastgele başlatılmaz. v2'nin
negatif ve pozitif satırları aynen kopyalanır, nötr satırı ikisinin
ortalamasıyla başlar. Böylece model v2'nin bildiklerini kaybetmeden başlar.

VERİ:
  - winvoker split="test" (bağımsız doğrulama split="train" üzerinden
    yapılıyor, v1 ince ayarı da split="test" kullanmıştı). Değerlendirmede
    kullanılan 1000 örnekle aynı metne sahip satırlar ayrıca çıkarılır.
  - Pozitifler kaynaklara göre dengelenir (winvoker pozitiflerinin çoğu ürün
    yorumu; tek bir alanın baskın olmaması için).
  - zayif_uslup_veri.jsonl (kısa/resmi/haber bülteni tarzı, v2'nin eğitim
    verisi) de eklenir.

İKİNCİ DENEME (11.09.2026): ilk v3 ölçümde sayısal olarak v2'yi geçti ama
elle kontrolde "Aşı karşıtlığı salgın riskini artırıyor" gibi açıkça olumsuz
haber cümlelerini NÖTR okudu. Sebep: winvoker'ın nötr örnekleri Vikipedi
cümleleri ve aralarında "Taylor tarafından öldürülür" gibi olumsuz olay
anlatanlar da "Notr" etiketli; model "resmi üçüncü şahıs anlatım = nötr"
kısayolunu öğrendi. Bizim ölçmek istediğimiz şey içeriğin duygusal tonu.
Düzeltme:
  - Vikipedi nötrlerinden değerlik kelimesi (öldür, savaş, kaza, başarı,
    ödül vb.) içerenler çıkarılır (17 bin örneğin ~2 bini).
  - haber_uslubu_uc_sinif.jsonl: haber ve gündelik paylaşım üslubunda,
    üç sınıflı, bu amaçla yazılmış hedefli veri. Nötr cümleler
    duyuru/takvim/prosedür bilgisidir; böylece model üslubu değil içeriği
    öğrenir.
  - Uygulamadaki gönderiler ve haberler eğitimden açıkça hariç tutulur.

ÜÇÜNCÜ AŞAMA (11.09.2026 akşam): kısa, duygu kelimesi içermeyen başlıklar
("işten çıkardı", "iptal edildi") nötr okunuyordu. Hedefli veriye bu tür
başlıklar eklendi; öğrenme oranı, epoch ve hedefli veri ağırlığı
ince_ayar_v3_arama.py ile GPU'da arandı. Seçim yalnızca DOĞRULAMA setiyle
yapıldı (winvoker'dan ayrı 1500 örnek + haber_uslubu_dogrulama.jsonl);
dogrulama_v3.py'nin test setleri seçimde hiç kullanılmadı. Aşağıdaki
varsayılanlar aramanın seçtiği değerlerdir.

SINIRLILIK (raporda/sunumda söylenmeli): winvoker'daki nötr örneklerin
neredeyse tamamı Vikipedi cümleleri; hedefli veri bunu dengelemek için
eklendi ama küçük (≈380 cümle).

Sonuç ayrı klasöre (bert-turkish-sentiment-ince-ayarli-v3) kaydedilir; v2'nin
üzerine yazılmaz. dogrulama_v3.py ile ölçülmeden duygu_modeli.py onu
kullanmaya başlamaz.
"""
import ast
import json
import random
import re
from pathlib import Path

import numpy as np
import torch
from datasets import Dataset, load_dataset
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    DataCollatorWithPadding,
    Trainer,
    TrainingArguments,
)

KOK = Path(__file__).resolve().parent
TABAN_MODEL_DIZINI = KOK / "models" / "bert-turkish-sentiment-ince-ayarli-v2"
ZAYIF_USLUP = KOK / "zayif_uslup_veri.jsonl"
ZAYIF_TEST = KOK / "zayif_uslup_dogrulama_etiketli.py"
HABER_USLUBU = KOK / "haber_uslubu_uc_sinif.jsonl"
HABER_DOGRULAMA = KOK / "haber_uslubu_dogrulama.jsonl"
CIKTI_DIZINI = KOK / "models" / "bert-turkish-sentiment-ince-ayarli-v3"
RASTGELE_TOHUM = 42

# ince_ayar_v3_arama.py'nin doğrulama setinde seçtiği değerler
OGRENME_ORANI = 3e-5
EPOCH = 2
HEDEFLI_KAT = 5

# Vikipedi "nötr"lerinde olumsuz/olumlu olay anlatan cümleleri ayıklamak için.
DEGERLIK = re.compile(
    r"(öl[dmüu]|öldür|savaş|işgal|katliam|yenil|başarısız|kaza|yaral|yangın|deprem|felaket|"
    r"hastal|kriz|çatışma|saldır|hapis|idam|iflas|kayb|yık|zarar|tehdit|korku|endişe|ölüm|"
    r"intihar|suç|terör|sürgün|kıtlık|salgın|zafer|başarı|kazan|ödül|şampiyon|mutlu|sevin|"
    r"harika|muhteşem|övgü|rekor|üstün)"
)

ETIKETLER = ["negative", "neutral", "positive"]
LABEL2ID = {etiket: i for i, etiket in enumerate(ETIKETLER)}
WINVOKER_ETIKET = {"negative": "negative", "notr": "neutral", "positive": "positive"}

NEGATIF_SAYISI = 5600
NOTR_SAYISI = 6000
POZITIF_SAYISI = 6000


def _test_indeksleri(veri) -> set[int]:
    """dogrulama.py / dogrulama_v3.py'nin 1000 test örneği (split=train, seed=42)."""
    random.seed(RASTGELE_TOHUM)
    return set(random.sample(range(len(veri)), 1000))


def _degerlendirme_metinleri() -> set[str]:
    veri = load_dataset("winvoker/turkish-sentiment-analysis-dataset", split="train")
    return {str(veri[i]["text"]).strip() for i in _test_indeksleri(veri)}


def winvoker_dogrulama(adet: int = 1500) -> list[tuple[str, str]]:
    """Model SEÇİMİ için winvoker split=train'den 1500 örnek (tohum 7).
    Test için ayrılan 1000 örnekle kesişmez."""
    veri = load_dataset("winvoker/turkish-sentiment-analysis-dataset", split="train")
    test = _test_indeksleri(veri)
    secilen = []
    for i in random.Random(7).sample(range(len(veri)), 6000):
        etiket = WINVOKER_ETIKET.get(str(veri[i]["label"]).strip().lower())
        if i in test or not etiket:
            continue
        secilen.append((str(veri[i]["text"]).strip()[:512], etiket))
        if len(secilen) >= adet:
            break
    return secilen


def haber_dogrulama() -> list[tuple[str, str]]:
    with open(HABER_DOGRULAMA, encoding="utf-8") as f:
        return [(k["text"].strip(), k["label"]) for k in map(json.loads, filter(str.strip, f))]


def _zayif_test_metinleri() -> set[str]:
    """Elle etiketlenmiş 40 örneklik test setini modülü çalıştırmadan okur."""
    agac = ast.parse(ZAYIF_TEST.read_text(encoding="utf-8"))
    for dugum in agac.body:
        if isinstance(dugum, ast.Assign) and any(getattr(h, "id", "") == "VERI" for h in dugum.targets):
            return {metin.strip() for metin, _ in ast.literal_eval(dugum.value)}
    return set()


def _uygulama_metinleri() -> set[str]:
    """Uygulamada görünen gönderi ve haber metinleri: ölçüm için ayrılır."""
    from demo_paketi import DEMO_POSTS, DEMO_PROFILE_POSTS
    from haber_veri import HABERLER
    from ornek_veri import ORNEK_GONDERILER
    from topluluk_veri import TOPLULUK_GONDERILERI
    metinler = {g["metin"].strip() for g in [*ORNEK_GONDERILER, *TOPLULUK_GONDERILERI, *DEMO_POSTS, *DEMO_PROFILE_POSTS]}
    for haber in HABERLER:
        metinler |= {haber["baslik"].strip(), haber["ozet"].strip()}
    return metinler


def veri_hazirla(hedefli_kat: int = HEDEFLI_KAT) -> Dataset:
    rng = random.Random(RASTGELE_TOHUM)
    dogrulama = {m for m, _ in winvoker_dogrulama()} | {m for m, _ in haber_dogrulama()}
    haric = _degerlendirme_metinleri() | _zayif_test_metinleri() | _uygulama_metinleri() | dogrulama

    test = load_dataset("winvoker/turkish-sentiment-analysis-dataset", split="test")
    gruplar: dict[str, dict[str, list[str]]] = {"negative": {}, "neutral": {}, "positive": {}}
    ayiklanan = 0
    for satir in test:
        metin = str(satir["text"]).strip()
        etiket = WINVOKER_ETIKET.get(str(satir["label"]).strip().lower())
        if not etiket or not metin or metin in haric:
            continue
        if etiket == "neutral" and DEGERLIK.search(metin.lower()):
            ayiklanan += 1
            continue
        gruplar[etiket].setdefault(satir["dataset"], []).append(metin)
    print(f"  değerlik kelimesi içerdiği için ayıklanan Vikipedi nötrü: {ayiklanan}")

    def kaynak_dengeli(kaynaklar: dict[str, list[str]], hedef: int) -> list[str]:
        """Her kaynaktan eşit pay almaya çalışır; küçük kaynak bitince kalan
        pay büyük kaynaklardan tamamlanır."""
        for liste in kaynaklar.values():
            rng.shuffle(liste)
        secilen, kalan = [], dict(kaynaklar)
        while len(secilen) < hedef and kalan:
            pay = max(1, (hedef - len(secilen)) // len(kalan))
            for ad in list(kalan):
                al, kalan[ad] = kalan[ad][:pay], kalan[ad][pay:]
                secilen.extend(al)
                if not kalan[ad]:
                    del kalan[ad]
                if len(secilen) >= hedef:
                    break
        return secilen[:hedef]

    kayitlar = []
    for etiket, hedef in (("negative", NEGATIF_SAYISI), ("neutral", NOTR_SAYISI), ("positive", POZITIF_SAYISI)):
        secilen = kaynak_dengeli(gruplar[etiket], hedef)
        print(f"  winvoker {etiket}: {len(secilen)}  (kaynaklar: {sorted(gruplar[etiket])})")
        kayitlar += [{"text": metin, "label": LABEL2ID[etiket]} for metin in secilen]

    zayif = []
    with open(ZAYIF_USLUP, encoding="utf-8") as f:
        for satir in f:
            satir = satir.strip()
            if not satir:
                continue
            kayit = json.loads(satir)
            if kayit.get("label") in ("negative", "positive") and kayit.get("text", "").strip() not in haric:
                zayif.append({"text": kayit["text"].strip(), "label": LABEL2ID[kayit["label"]]})
    # Haber üslubu az örnekle temsil ediliyor; iki kez eklenerek ağırlığı artırılır.
    print(f"  zayif_uslup (x2): {len(zayif)}")
    kayitlar += zayif + zayif

    hedefli = []
    with open(HABER_USLUBU, encoding="utf-8") as f:
        for satir in f:
            satir = satir.strip()
            if satir:
                kayit = json.loads(satir)
                if kayit["text"].strip() not in haric:
                    hedefli.append({"text": kayit["text"].strip(), "label": LABEL2ID[kayit["label"]]})
    print(f"  haber_uslubu_uc_sinif (x{hedefli_kat}): {len(hedefli)}")
    kayitlar += hedefli * hedefli_kat

    rng.shuffle(kayitlar)
    return Dataset.from_list(kayitlar)


def model_hazirla():
    taban = AutoModelForSequenceClassification.from_pretrained(str(TABAN_MODEL_DIZINI))
    etiketler = {int(k): str(v).lower() for k, v in taban.config.id2label.items()}
    poz = next(i for i, e in etiketler.items() if "pos" in e or e == "label_1")
    neg = next(i for i in etiketler if i != poz)

    model = AutoModelForSequenceClassification.from_pretrained(
        str(TABAN_MODEL_DIZINI),
        num_labels=3,
        id2label=dict(enumerate(ETIKETLER)),
        label2id=LABEL2ID,
        ignore_mismatched_sizes=True,
    )
    with torch.no_grad():
        agirlik, sapma = taban.classifier.weight, taban.classifier.bias
        model.classifier.weight[LABEL2ID["negative"]] = agirlik[neg]
        model.classifier.weight[LABEL2ID["positive"]] = agirlik[poz]
        model.classifier.weight[LABEL2ID["neutral"]] = (agirlik[neg] + agirlik[poz]) / 2
        model.classifier.bias[LABEL2ID["negative"]] = sapma[neg]
        model.classifier.bias[LABEL2ID["positive"]] = sapma[poz]
        model.classifier.bias[LABEL2ID["neutral"]] = (sapma[neg] + sapma[poz]) / 2
    del taban
    return model


def egit(veri: Dataset, tokenizer, ogrenme_orani: float = OGRENME_ORANI, epoch: int = EPOCH,
         gecici_dizin: Path = CIKTI_DIZINI / "_checkpoint_gecici"):
    """Veriyi %92/%8 böler, v2'den başlayarak eğitir ve modeli döndürür."""
    torch.manual_seed(RASTGELE_TOHUM)
    bolum = veri.train_test_split(test_size=0.08, seed=RASTGELE_TOHUM)
    bolum = bolum.map(lambda o: tokenizer(o["text"], truncation=True, max_length=128), batched=True, remove_columns=["text"])
    model = model_hazirla()

    def compute_metrics(eval_pred):
        from sklearn.metrics import accuracy_score, f1_score
        logits, labels = eval_pred
        tahmin = np.argmax(logits, axis=-1)
        return {"dogruluk": accuracy_score(labels, tahmin), "f1_makro": f1_score(labels, tahmin, average="macro")}

    parti = 32
    toplam_adim = -(-len(bolum["train"]) // parti) * epoch
    args = TrainingArguments(
        output_dir=str(gecici_dizin),
        num_train_epochs=epoch,
        per_device_train_batch_size=parti,
        per_device_eval_batch_size=64,
        learning_rate=ogrenme_orani,
        warmup_steps=int(toplam_adim * 0.06),
        weight_decay=0.01,
        fp16=torch.cuda.is_available(),
        eval_strategy="epoch",
        save_strategy="no",
        logging_steps=50,
        report_to=[],
        seed=RASTGELE_TOHUM,
    )
    egitici = Trainer(
        model=model,
        args=args,
        train_dataset=bolum["train"],
        eval_dataset=bolum["test"],
        compute_metrics=compute_metrics,
        data_collator=DataCollatorWithPadding(tokenizer),
    )
    egitici.train()
    print("Ayrılmış %8'lik bölümde sonuç:", egitici.evaluate())
    return model


def main():
    if not TABAN_MODEL_DIZINI.exists():
        print(f"HATA: {TABAN_MODEL_DIZINI} bulunamadı.")
        return
    print("Veri hazırlanıyor...")
    veri = veri_hazirla()
    print(f"Toplam örnek: {len(veri)}")
    tokenizer = AutoTokenizer.from_pretrained(str(TABAN_MODEL_DIZINI))
    print(f"\nÜçüncü tur ince ayar başlıyor (cihaz: {'GPU' if torch.cuda.is_available() else 'CPU'}, "
          f"öğrenme oranı {OGRENME_ORANI}, {EPOCH} epoch, hedefli veri x{HEDEFLI_KAT})...\n")
    model = egit(veri, tokenizer)
    CIKTI_DIZINI.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(CIKTI_DIZINI)
    tokenizer.save_pretrained(CIKTI_DIZINI)
    print(f"Kaydedildi: {CIKTI_DIZINI}")
    print("Şimdi dogrulama_v3.py çalıştırılmalı; ölçülmeden duygu_modeli.py bu modeli kullanmamalı.")


if __name__ == "__main__":
    main()
