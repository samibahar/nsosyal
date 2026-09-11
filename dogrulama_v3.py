# -*- coding: utf-8 -*-
"""ince_ayar_v3.py çıktısının bağımsız ölçümü, v2 ile yan yana.

1) winvoker 1000 örnek (split="train", seed=42; dogrulama.py ile aynı örnekler,
   v3'ün eğitimde gördüğü split="test" ile ayrık):
     - ikili doğruluk: Pozitif/Negatif örneklerde tonun işareti (v2 ile kıyas)
     - v3 için 3 sınıf doğruluğu
     - Nötr etiketli örneklerde ortalama |ton| (düşük olması beklenir)
2) Elle etiketlenmiş 40 haber üslubu örnek (zayif_uslup_dogrulama_etiketli.py)
3) Uygulamadaki gönderilerin ton dağılımı: aşırı kesinlik ölçütleri

Ton tanımları uygulamadakiyle aynı:
  v2 (ikili): işaret × sınıflandırıcı güveni   (duygu_modeli.py'nin eski formülü)
  v3 (üçlü):  P(pozitif) − P(negatif)
Sonuçlar dogrulama_v3_sonuc.txt'e yazılır.
"""
import ast
import random
from pathlib import Path

import numpy as np
import torch
from datasets import load_dataset
from sklearn.metrics import accuracy_score, f1_score
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from ornek_veri import ORNEK_GONDERILER
from topluluk_veri import TOPLULUK_GONDERILERI

KOK = Path(__file__).resolve().parent
V2 = KOK / "models" / "bert-turkish-sentiment-ince-ayarli-v2"
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
        if p.shape[1] == 2:
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
    v2, v3 = Model(V2), Model(V3)

    yaz("=" * 72)
    yaz("TEST 1 · winvoker bağımsız 1000 örnek (split=train, seed=42)")
    yaz("=" * 72)
    veri = load_dataset("winvoker/turkish-sentiment-analysis-dataset", split="train")
    random.seed(42)
    ornek = veri.select(random.sample(range(len(veri)), 1000))
    metinler = [str(s["text"])[:512] for s in ornek]
    etiketler = [str(s["label"]).strip().lower() for s in ornek]
    t2, t3 = v2.tonlar(metinler), v3.tonlar(metinler)
    ikili = [i for i, e in enumerate(etiketler) if e != "notr"]
    gercek = ["positive" if etiketler[i] == "positive" else "negative" for i in ikili]
    for ad, t in (("v2", t2), ("v3", t3)):
        tahmin = ["positive" if t[i] > 0 else "negative" for i in ikili]
        yaz(f"{ad} ikili doğruluk ({len(ikili)} örnek): {accuracy_score(gercek, tahmin):.4f} · F1: {f1_score(gercek, tahmin, pos_label='positive'):.4f}")
    notr = [i for i, e in enumerate(etiketler) if e == "notr"]
    yaz(f"Nötr etiketli {len(notr)} örnekte ortalama |ton| · v2: {np.abs(t2[notr]).mean():.3f} · v3: {np.abs(t3[notr]).mean():.3f}")
    p3 = v3.olasiliklar(metinler)
    uclu_tahmin = [v3.etiket[int(k)] for k in p3.argmax(1)]
    uclu_gercek = [{"notr": "neutral"}.get(e, e) for e in etiketler]
    yaz(f"v3 üç sınıf doğruluğu: {accuracy_score(uclu_gercek, uclu_tahmin):.4f} · F1 makro: {f1_score(uclu_gercek, uclu_tahmin, average='macro'):.4f}")

    yaz()
    yaz("=" * 72)
    yaz("TEST 2 · elle etiketlenmiş 40 haber üslubu örnek")
    yaz("=" * 72)
    test = zayif_test()
    zm = [m for m, _ in test]
    zg = [e for _, e in test]
    for ad, model in (("v2", v2), ("v3", v3)):
        t = model.tonlar(zm)
        tahmin = ["positive" if x > 0 else "negative" for x in t]
        yanlis = [(m, g, round(float(x), 2)) for m, g, x in zip(zm, zg, t) if ("positive" if x > 0 else "negative") != g]
        yaz(f"{ad} doğruluk: {accuracy_score(zg, tahmin):.3f} · ortalama |ton|: {np.abs(t).mean():.3f} · yanlış: {len(yanlis)}")
        for m, g, x in yanlis:
            yaz(f"    [gerçek {g}, ton {x:+.2f}] {m}")

    yaz()
    yaz("=" * 72)
    yaz("TEST 3 · uygulamadaki gönderilerin ton dağılımı (aşırı kesinlik)")
    yaz("=" * 72)
    gonderiler = [*ORNEK_GONDERILER, *TOPLULUK_GONDERILERI]
    gm = [g["metin"] for g in gonderiler]
    g2, g3 = v2.tonlar(gm), v3.tonlar(gm)
    yaz(f"{len(gm)} gönderi")
    yaz(f"v2: {dagilim(g2)}")
    yaz(f"v3: {dagilim(g3)}")
    isaret_uyumu = float(np.mean(np.sign(g2) == np.sign(g3)))
    yaz(f"v2 ile v3'ün yön (işaret) uyumu: %{100 * isaret_uyumu:.1f}")
    yaz()
    yaz("Tonu en çok değişen 15 gönderi (elle kontrol için):")
    for i in np.argsort(-np.abs(g2 - g3))[:15]:
        yaz(f"  v2 {g2[i]:+.2f} → v3 {g3[i]:+.2f}  {gm[i]}")
    yaz()
    yaz("v3'e göre en olumsuz 5 ve nötre en yakın 5 gönderi:")
    for i in np.argsort(g3)[:5]:
        yaz(f"  {g3[i]:+.2f}  {gm[i]}")
    for i in np.argsort(np.abs(g3))[:5]:
        yaz(f"  {g3[i]:+.2f}  {gm[i]}")

    yaz()
    yaz("=" * 72)
    yaz("TEST 4 · haber_veri.py: aynı olayın iki anlatımı (ekip tarafından önceden elle puanlanmış)")
    yaz("=" * 72)
    from haber_veri import HABERLER
    from scipy.stats import spearmanr
    hm = [f"{h['baslik']}. {h['ozet']}" for h in HABERLER]
    el = np.array([h["duygu"] for h in HABERLER])
    olaylar = {}
    for i, h in enumerate(HABERLER):
        olaylar.setdefault(h["olay_id"], {})["birincil" if h["birincil"] else "alternatif"] = i
    for ad, model in (("v2", v2), ("v3", v3)):
        t = model.tonlar(hm)
        dogru_sira = sum(1 for o in olaylar.values() if t[o["alternatif"]] > t[o["birincil"]])
        yon = float(np.mean(np.sign(t) == np.sign(el)))
        yaz(f"{ad}: yapıcı anlatımı yoğun anlatımdan daha olumlu bulma {dogru_sira}/{len(olaylar)} · "
            f"el puanıyla yön uyumu %{100 * yon:.0f} · Spearman ρ = {spearmanr(t, el)[0]:.2f}")

    yaz()
    yaz("=" * 72)
    yaz("TEST 5 · demo_paketi.py: jüri demosundaki 14 gönderi (elle puanlanmış)")
    yaz("=" * 72)
    from demo_paketi import DEMO_POSTS, DEMO_PROFILE_POSTS
    dp = [*DEMO_POSTS, *DEMO_PROFILE_POSTS]
    dm, de = [p["metin"] for p in dp], np.array([p["duygu"] for p in dp])
    for ad, model in (("v2", v2), ("v3", v3)):
        t = model.tonlar(dm)
        yaz(f"{ad}: el puanıyla yön uyumu %{100 * float(np.mean(np.sign(t) == np.sign(de))):.0f} · "
            f"Spearman ρ = {spearmanr(t, de)[0]:.2f} · ortalama |ton| {np.abs(t).mean():.2f} (el puanı ort. |ton| {np.abs(de).mean():.2f})")

    CIKTI.write_text("\n".join(satirlar) + "\n", encoding="utf-8")
    print(f"\nSonuçlar {CIKTI.name} dosyasına yazıldı.")


if __name__ == "__main__":
    main()
