# -*- coding: utf-8 -*-
"""v3 için GPU'da hiperparametre araması.

Seçim YALNIZCA doğrulama setiyle yapılır:
  - winvoker split=train'den 1500 örnek (tohum 7); dogrulama_v3.py'nin 1000
    test örneğiyle kesişmez
  - haber_uslubu_dogrulama.jsonl: yalnızca doğrulama için yazılmış 60 haber
    ve paylaşım cümlesi (eğitimde yok)
dogrulama_v3.py'nin test setleri (winvoker 1000, elle etiketli 40 haber,
haber_veri.py, demo_paketi.py) aramada hiç kullanılmaz; seçilen model onlarda
bir kez ölçülür. Aksi halde rapora giren sayı seçim yüzünden şişerdi.

Skor = ortalama(winvoker ikili doğruluk, winvoker 3 sınıf F1 makro,
haber doğrulama 3 sınıf doğruluk). Mevcut v3 de aynı skorla ölçülür; hiçbir
aday onu geçmezse model değiştirilmez. Sonuçlar v3_arama_sonuc.txt'e yazılır.
"""
import gc
import shutil

import numpy as np
import torch
from sklearn.metrics import accuracy_score, f1_score
from transformers import AutoModelForSequenceClassification, AutoTokenizer

import ince_ayar_v3 as v3

# (öğrenme oranı, epoch, hedefli veri katı)
AYARLAR = [(2e-5, 2, 3), (3e-5, 2, 3), (2e-5, 3, 3), (3e-5, 3, 3), (2e-5, 3, 5), (3e-5, 2, 5)]
ADAY_DIZINI = v3.KOK / "models" / "_v3_arama_en_iyi"
ONCEKI_DIZIN = v3.KOK / "models" / "bert-turkish-sentiment-ince-ayarli-v3a"
CIHAZ = "cuda" if torch.cuda.is_available() else "cpu"
satirlar: list[str] = []


def yaz(metin: str = ""):
    print(metin, flush=True)
    satirlar.append(metin)


@torch.no_grad()
def olasiliklar(model, tokenizer, metinler: list[str]) -> np.ndarray:
    model.to(CIHAZ).eval()
    cikti = []
    for i in range(0, len(metinler), 64):
        parti = tokenizer(metinler[i:i + 64], truncation=True, max_length=128, padding=True, return_tensors="pt").to(CIHAZ)
        cikti.append(torch.softmax(model(**parti).logits.float(), dim=-1).cpu().numpy())
    return np.concatenate(cikti)


def olc(model, tokenizer, winvoker, haber) -> dict:
    etiket = {int(k): str(v).lower() for k, v in model.config.id2label.items()}
    ad = lambda k: "neutral" if "neu" in etiket[k] else ("positive" if "pos" in etiket[k] else "negative")
    poz = next(k for k in etiket if ad(k) == "positive")
    neg = next(k for k in etiket if ad(k) == "negative")

    p = olasiliklar(model, tokenizer, [m for m, _ in winvoker])
    gercek = [e for _, e in winvoker]
    ton = p[:, poz] - p[:, neg]
    ikili_i = [i for i, e in enumerate(gercek) if e != "neutral"]
    ikili = accuracy_score([gercek[i] for i in ikili_i], ["positive" if ton[i] > 0 else "negative" for i in ikili_i])
    uclu_f1 = f1_score(gercek, [ad(int(k)) for k in p.argmax(1)], average="macro")

    ph = olasiliklar(model, tokenizer, [m for m, _ in haber])
    haber_dogruluk = accuracy_score([e for _, e in haber], [ad(int(k)) for k in ph.argmax(1)])
    notr_i = [i for i, e in enumerate(gercek) if e == "neutral"]
    return {"skor": float(np.mean([ikili, uclu_f1, haber_dogruluk])), "ikili": ikili, "uclu_f1": uclu_f1,
            "haber": haber_dogruluk, "notr_ton": float(np.abs(ton[notr_i]).mean())}


def satir(ad: str, m: dict) -> str:
    return (f"{ad:28s} skor {m['skor']:.4f} · winvoker ikili {m['ikili']:.4f} · 3 sınıf F1 {m['uclu_f1']:.4f} · "
            f"haber {m['haber']:.3f} · nötr |ton| {m['notr_ton']:.3f}")


def main():
    winvoker, haber = v3.winvoker_dogrulama(), v3.haber_dogrulama()
    yaz("v3 HİPERPARAMETRE ARAMASI (ince_ayar_v3_arama.py)")
    yaz("=" * 72)
    yaz(f"Doğrulama: winvoker {len(winvoker)} örnek (test örnekleriyle ayrık) + haber üslubu {len(haber)} cümle")
    yaz("Test setleri aramada kullanılmadı.")
    yaz()

    tokenizer = AutoTokenizer.from_pretrained(str(v3.TABAN_MODEL_DIZINI))
    mevcut = AutoModelForSequenceClassification.from_pretrained(str(v3.CIKTI_DIZINI))
    en_iyi_ad, en_iyi = "mevcut v3", olc(mevcut, tokenizer, winvoker, haber)
    yaz(satir("mevcut v3", en_iyi))
    del mevcut
    gc.collect()
    torch.cuda.empty_cache()

    veriler = {}
    for oran, epoch, kat in AYARLAR:
        if kat not in veriler:
            veriler[kat] = v3.veri_hazirla(hedefli_kat=kat)
        ad = f"oran {oran:g} · {epoch} epoch · x{kat}"
        print(f"\n>>> {ad}", flush=True)
        model = v3.egit(veriler[kat], tokenizer, ogrenme_orani=oran, epoch=epoch,
                        gecici_dizin=v3.KOK / "models" / "_v3_arama_gecici")
        m = olc(model, tokenizer, winvoker, haber)
        yaz(satir(ad, m))
        if m["skor"] > en_iyi["skor"]:
            en_iyi_ad, en_iyi = ad, m
            shutil.rmtree(ADAY_DIZINI, ignore_errors=True)
            model.save_pretrained(ADAY_DIZINI)
            tokenizer.save_pretrained(ADAY_DIZINI)
        del model
        gc.collect()
        torch.cuda.empty_cache()

    yaz()
    yaz(f"SEÇİLEN: {en_iyi_ad}")
    if en_iyi_ad != "mevcut v3":
        shutil.rmtree(ONCEKI_DIZIN, ignore_errors=True)
        shutil.move(str(v3.CIKTI_DIZINI), str(ONCEKI_DIZIN))
        shutil.move(str(ADAY_DIZINI), str(v3.CIKTI_DIZINI))
        yaz(f"Önceki v3 {ONCEKI_DIZIN.name} klasörüne taşındı; yeni model v3 klasöründe.")
    shutil.rmtree(v3.KOK / "models" / "_v3_arama_gecici", ignore_errors=True)
    shutil.rmtree(v3.CIKTI_DIZINI / "_checkpoint_gecici", ignore_errors=True)
    (v3.KOK / "v3_arama_sonuc.txt").write_text("\n".join(satirlar) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
