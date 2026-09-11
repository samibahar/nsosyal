# -*- coding: utf-8 -*-
"""Ölçek ve maliyet ölçümü: "700 bin kullanıcıda çalışır mı, neye mal olur?"

Ölçülenler:
  1) Duygu modeli (BERT, v3) hızı: CPU'da ve (varsa) GPU'da saniyede kaç
     gönderi skorlanıyor. Ton gönderi başına BİR kez, yayımlanırken hesaplanır;
     kullanıcı sayısıyla değil gönderi sayısıyla büyür.
  2) Spiral + psikolojik model çıkarımı (Python referansı; tarayıcıda da aynı
     matematik çalışır, sunucuya yük bindirmez).
  3) Aday listesi yanıt boyutu (48 gönderi), gzip'li ve gzip'siz.
Sonuçlar olcek_olcumu_sonuc.txt'e yazılır. Donanım: bu makine (tek dizüstü).
"""
import gzip
import json
import platform
import time
from pathlib import Path

import numpy as np
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

import spiral_model
import spiral_ozellik
from ornek_veri import ORNEK_GONDERILER
from psikolojik_durum import psikolojik_durum_tahmini
from topluluk_veri import TOPLULUK_GONDERILERI

KOK = Path(__file__).resolve().parent
MODEL = KOK / "models" / "bert-turkish-sentiment-ince-ayarli-v3"
satirlar: list[str] = []


def yaz(metin: str = ""):
    print(metin, flush=True)
    satirlar.append(metin)


@torch.no_grad()
def bert_hizi(cihaz: str, metinler: list[str], parti: int = 32) -> float:
    tok = AutoTokenizer.from_pretrained(str(MODEL))
    model = AutoModelForSequenceClassification.from_pretrained(str(MODEL)).to(cihaz).eval()
    if cihaz == "cuda":
        model = model.half()
    def calistir(liste):
        for i in range(0, len(liste), parti):
            girdi = tok(liste[i:i + parti], truncation=True, max_length=128, padding=True, return_tensors="pt").to(cihaz)
            model(**girdi)
        if cihaz == "cuda":
            torch.cuda.synchronize()
    calistir(metinler[:64])  # ısınma
    baslangic = time.perf_counter()
    calistir(metinler)
    return len(metinler) / (time.perf_counter() - baslangic)


def main():
    metinler = [g["metin"] for g in [*ORNEK_GONDERILER, *TOPLULUK_GONDERILERI]] * 4
    yaz("ÖLÇEK VE MALİYET ÖLÇÜMÜ (python olcek_olcumu.py)")
    yaz("=" * 72)
    yaz(f"Makine: {platform.processor() or platform.machine()} · {torch.get_num_threads()} iş parçacığı"
        + (f" · GPU {torch.cuda.get_device_name(0)}" if torch.cuda.is_available() else ""))
    yaz()
    yaz(f"1) Duygu modeli (v3), {len(metinler)} gönderi, 32'lik partiler:")
    for cihaz in ["cpu"] + (["cuda"] if torch.cuda.is_available() else []):
        hiz = bert_hizi(cihaz, metinler)
        yaz(f"  {cihaz.upper():4s}: saniyede {hiz:7.0f} gönderi → günde {hiz * 86400 / 1e6:6.1f} milyon gönderi (tek cihaz)")
    yaz("  Ton gönderi yayımlanırken bir kez hesaplanır; okuyan kullanıcı sayısı bu maliyeti artırmaz.")
    yaz()

    olaylar = [{"gonderi": i, "zaman": i * 6.0, "dwell": 5.0 + (i % 4), "ton": -0.8 if i % 3 == 0 else 0.4,
                "kelime": 14, "konu": "gundem", "roket": False, "yorum": i % 7 == 0} for i in range(20)]
    tekrar = 2000
    baslangic = time.perf_counter()
    for _ in range(tekrar):
        spiral_model.olasilik(spiral_ozellik.ozellikler(olaylar, 130.0))
    spiral_ms = (time.perf_counter() - baslangic) / tekrar * 1000
    baslangic = time.perf_counter()
    for _ in range(tekrar):
        psikolojik_durum_tahmini(-0.7, 6.0, True, False, True)
    psikolojik_ms = (time.perf_counter() - baslangic) / tekrar * 1000
    yaz("2) Davranış modelleri (Python referansı, tek çağrı):")
    yaz(f"  Spiral (20 gönderilik pencere): {spiral_ms:.3f} ms · psikolojik durum: {psikolojik_ms:.3f} ms")
    yaz("  Uygulamada ikisi de kullanıcının tarayıcısında çalışır; sunucuya yük bindirmez.")
    yaz()

    aday = [{**g, "duygu": -0.5, "ilgi_skoru": 0.6, "final_skor": 0.6, "refah_cezasi": 0.0, "aciklama": "",
             "yazar_bilgi": {"id": "denizcetin", "name": "Deniz Çetin", "handle": "@denizcetin", "initials": "DÇ", "color": "#5079a2"},
             "roket_sayisi": 3, "yorum_sayisi": 1, "kullanici_roketledi": False, "resmi": False}
            for g in [*ORNEK_GONDERILER, *TOPLULUK_GONDERILERI][:48]]
    ham = json.dumps({"spiral_seviyesi": 0.0, "gonderiler": aday, "tukendi": False}, ensure_ascii=False).encode("utf-8")
    yaz("3) Aday listesi (48 gönderi, metin + meta veri):")
    yaz(f"  ham {len(ham) / 1024:.1f} KB · gzip {len(gzip.compress(ham)) / 1024:.1f} KB")
    yaz("  Fotoğraflar ayrıca ve yalnızca gösterilen gönderiler için iner.")
    (KOK / "olcek_olcumu_sonuc.txt").write_text("\n".join(satirlar) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
