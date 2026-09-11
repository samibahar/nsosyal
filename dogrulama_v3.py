# -*- coding: utf-8 -*-
"""Duygu modellerinin bağımsız test setlerinde yan yana ölçümü.

Modeller: v2 (ikili), varsa "v3 önceki" (models/...-v3a, arama öncesi v3) ve
v3 (models/...-v3, etkin model).

Test setleri (hiçbiri eğitimde ya da ince_ayar_v3_arama.py'nin model
seçiminde kullanılmadı):
1) winvoker 1000 örnek (split="train", seed=42; dogrulama.py ile aynı
   örnekler, v3'ün eğitimde gördüğü split="test" ile ayrık):
     - ikili doğruluk: Pozitif/Negatif örneklerde tonun işareti
     - üç sınıflı modeller için 3 sınıf doğruluğu
     - Nötr etiketli örneklerde ortalama |ton| (düşük olması beklenir)
2) Elle etiketlenmiş 40 haber üslubu örnek (zayif_uslup_dogrulama_etiketli.py)
3) Uygulamadaki gönderilerin ton dağılımı: aşırı kesinlik ölçütleri
4) haber_veri.py: aynı olayın iki anlatımı, ekip tarafından önceden puanlanmış
5) demo_paketi.py: jüri demosundaki gönderiler, önceden puanlanmış

Ton tanımları uygulamadakiyle aynı:
  ikili model: işaret × sınıflandırıcı güveni   (duygu_modeli.py'nin eski formülü)
  üçlü model:  P(pozitif) − P(negatif)
Sonuçlar dogrulama_v3_sonuc.txt'e yazılır.
"""
import ast
import random
from pathlib import Path

import numpy as np
import torch
from datasets import load_dataset
from scipy.stats import spearmanr
from sklearn.metrics import accuracy_score, f1_score
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from demo_paketi import DEMO_POSTS, DEMO_PROFILE_POSTS
from haber_veri import HABERLER
from ornek_veri import ORNEK_GONDERILER
from topluluk_veri import TOPLULUK_GONDERILERI

KOK = Path(__file__).resolve().parent
V2 = KOK / "models" / "bert-turkish-sentiment-ince-ayarli-v2"
V3_ONCEKI = KOK / "models" / "bert-turkish-sentiment-ince-ayarli-v3a"
V3 = KOK / "models" / "bert-turkish-sentiment-ince-ayarli-v3"
CIKTI = KOK / "dogrulama_v3_sonuc.txt"
CIHAZ = "cuda" if torch.cuda.is_available() else "cpu"
satirlar: list[str] = []


def yaz(metin: str = ""):
    print(metin)
    satirlar.append(metin)


class Model:
    def __init__(self, dizin: Path):
        self.tok = AutoTokenizer.from_pretrained(str(dizin))
        self.model = AutoModelForSequenceClassification.from_pretrained(str(dizin)).to(CIHAZ).eval()
        self.etiket = {int(k): str(v).lower() for k, v in self.model.config.id2label.items()}
        self.uclu = len(self.etiket) == 3

    @torch.no_grad()
    def olasiliklar(self, metinler: list[str]) -> np.ndarray:
        cikti = []
        for i in range(0, len(metinler), 64):
            parti = self.tok(metinler[i:i + 64], truncation=True, max_length=128, padding=True, return_tensors="pt").to(CIHAZ)
            cikti.append(torch.softmax(self.model(**parti).logits.float(), dim=-1).cpu().numpy())
        return np.concatenate(cikti)

    def _indeks(self, parca: str) -> int | None:
        return next((i for i, e in self.etiket.items() if parca in e), None)

    def tonlar(self, metinler: list[str]) -> np.ndarray:
        p = self.olasiliklar(metinler)
        poz, neg = self._indeks("pos"), self._indeks("neg")
        if not self.uclu:
            # duygu_modeli.py'nin ikili formülü: işaret × en yüksek olasılık
            return np.where(p[:, poz] >= p[:, neg], p[:, poz], -p[:, neg])
        return p[:, poz] - p[:, neg]


def zayif_test():
    agac = ast.parse((KOK / "zayif_uslup_dogrulama_etiketli.py").read_text(encoding="utf-8"))
    for dugum in agac.body:
        if isinstance(dugum, ast.Assign) and any(getattr(h, "id", "") == "VERI" for h in dugum.targets):
            return ast.literal_eval(dugum.value)
    return []


def dagilim(tonlar: np.ndarray) -> str:
    mutlak = np.abs(tonlar)
    return (f"|ton|>0,9: %{100 * (mutlak > 0.9).mean():.1f} · |ton|≤0,3: %{100 * (mutlak <= 0.3).mean():.1f} · "
            f"ton<−0,15 (dengelemeye aday): %{100 * (tonlar < -0.15).mean():.1f} · ortalama |ton|: {mutlak.mean():.3f}")


def main():
    modeller = [("v2", Model(V2))]
    if V3_ONCEKI.exists():
        modeller.append(("v3 önceki", Model(V3_ONCEKI)))
    modeller.append(("v3", Model(V3)))

    yaz("=" * 72)
    yaz("TEST 1 · winvoker bağımsız 1000 örnek (split=train, seed=42)")
    yaz("=" * 72)
    veri = load_dataset("winvoker/turkish-sentiment-analysis-dataset", split="train")
    random.seed(42)
    ornek = veri.select(random.sample(range(len(veri)), 1000))
    metinler = [str(s["text"])[:512] for s in ornek]
    etiketler = [str(s["label"]).strip().lower() for s in ornek]
    ikili = [i for i, e in enumerate(etiketler) if e != "notr"]
    notr = [i for i, e in enumerate(etiketler) if e == "notr"]
    gercek = ["positive" if etiketler[i] == "positive" else "negative" for i in ikili]
    for ad, model in modeller:
        t = model.tonlar(metinler)
        tahmin = ["positive" if t[i] > 0 else "negative" for i in ikili]
        satir = (f"{ad:10s} ikili doğruluk ({len(ikili)} örnek): {accuracy_score(gercek, tahmin):.4f} · "
                 f"F1: {f1_score(gercek, tahmin, pos_label='positive'):.4f} · nötrlerde ort. |ton| {np.abs(t[notr]).mean():.3f}")
        if model.uclu:
            p = model.olasiliklar(metinler)
            uclu_tahmin = [model.etiket[int(k)] for k in p.argmax(1)]
            uclu_gercek = [{"notr": "neutral"}.get(e, e) for e in etiketler]
            satir += f" · 3 sınıf doğruluk {accuracy_score(uclu_gercek, uclu_tahmin):.4f} (F1 makro {f1_score(uclu_gercek, uclu_tahmin, average='macro'):.4f})"
        yaz(satir)

    yaz()
    yaz("=" * 72)
    yaz("TEST 2 · elle etiketlenmiş 40 haber üslubu örnek")
    yaz("=" * 72)
    test = zayif_test()
    zm, zg = [m for m, _ in test], [e for _, e in test]
    for ad, model in modeller:
        t = model.tonlar(zm)
        tahmin = ["positive" if x > 0 else "negative" for x in t]
        yanlis = [(m, g, round(float(x), 2)) for m, g, x in zip(zm, zg, t) if ("positive" if x > 0 else "negative") != g]
        yaz(f"{ad:10s} doğruluk: {accuracy_score(zg, tahmin):.3f} · ortalama |ton|: {np.abs(t).mean():.3f} · yanlış: {len(yanlis)}")
        for m, g, x in yanlis:
            yaz(f"    [gerçek {g}, ton {x:+.2f}] {m}")

    yaz()
    yaz("=" * 72)
    yaz("TEST 3 · uygulamadaki gönderilerin ton dağılımı (aşırı kesinlik)")
    yaz("=" * 72)
    gm = [g["metin"] for g in [*ORNEK_GONDERILER, *TOPLULUK_GONDERILERI]]
    tonlar = {ad: model.tonlar(gm) for ad, model in modeller}
    yaz(f"{len(gm)} gönderi")
    for ad in tonlar:
        yaz(f"{ad:10s} {dagilim(tonlar[ad])}")
    g2, g3 = tonlar["v2"], tonlar["v3"]
    yaz(f"v2 ile v3'ün yön (işaret) uyumu: %{100 * float(np.mean(np.sign(g2) == np.sign(g3))):.1f}")
    if "v3 önceki" in tonlar:
        yaz("Önceki v3 ile yeni v3 arasında tonu en çok değişen 12 gönderi (elle kontrol için):")
        ga = tonlar["v3 önceki"]
        for i in np.argsort(-np.abs(ga - g3))[:12]:
            yaz(f"  önceki {ga[i]:+.2f} → yeni {g3[i]:+.2f}  {gm[i]}")
    yaz("v3'e göre nötre en yakın 8 gönderi:")
    for i in np.argsort(np.abs(g3))[:8]:
        yaz(f"  {g3[i]:+.2f}  {gm[i]}")

    yaz()
    yaz("=" * 72)
    yaz("TEST 4 · haber_veri.py: aynı olayın iki anlatımı (ekip tarafından önceden puanlanmış)")
    yaz("=" * 72)
    hm = [f"{h['baslik']}. {h['ozet']}" for h in HABERLER]
    el = np.array([h["duygu"] for h in HABERLER])
    olaylar = {}
    for i, h in enumerate(HABERLER):
        olaylar.setdefault(h["olay_id"], {})["birincil" if h["birincil"] else "alternatif"] = i
    for ad, model in modeller:
        t = model.tonlar(hm)
        dogru_sira = sum(1 for o in olaylar.values() if t[o["alternatif"]] > t[o["birincil"]])
        yaz(f"{ad:10s} yapıcı anlatımı daha olumlu bulma {dogru_sira}/{len(olaylar)} · "
            f"el puanıyla yön uyumu %{100 * float(np.mean(np.sign(t) == np.sign(el))):.0f} · Spearman ρ = {spearmanr(t, el)[0]:.2f}")

    yaz()
    yaz("=" * 72)
    yaz("TEST 5 · demo_paketi.py: jüri demosundaki 14 gönderi (elle puanlanmış)")
    yaz("=" * 72)
    dp = [*DEMO_POSTS, *DEMO_PROFILE_POSTS]
    dm, de = [p["metin"] for p in dp], np.array([p["duygu"] for p in dp])
    for ad, model in modeller:
        t = model.tonlar(dm)
        yaz(f"{ad:10s} el puanıyla yön uyumu %{100 * float(np.mean(np.sign(t) == np.sign(de))):.0f} · "
            f"Spearman ρ = {spearmanr(t, de)[0]:.2f} · ortalama |ton| {np.abs(t).mean():.2f} (el puanı ort. |ton| {np.abs(de).mean():.2f})")

    CIKTI.write_text("\n".join(satirlar) + "\n", encoding="utf-8")
    print(f"\nSonuçlar {CIKTI.name} dosyasına yazıldı.")


if __name__ == "__main__":
    main()
