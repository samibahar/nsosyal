"""
Gönüllü pilot çalışmasının analizi (protokol: docs/pilot_protokolu.md).

Spiral ve ruh hali modelleri sentetik veriyle eğitildi. Bu betik gönüllülerin
Ayarlar > Gönüllü pilot bölümünden indirdiği dosyaları birleştirip modellerin
GERÇEK öz-bildirimle ne kadar örtüştüğünü ölçer:

  1) Uygulamanın o an verdiği tahminler: her cevap önce tahmin edildi, sonra
     öğrenildi (prequential). Uyum oranı taban çizgileri ve Wilson %95 güven
     aralığıyla verilir.
  2) Gerçek veriyle yeniden eğitim: birini dışarıda bırak çapraz doğrulaması
     (her turda bir katılımcının tüm cevapları test, kalanlar eğitim). Pilot
     verisiyle eğitilen modelin sentetik modelden iyi olup olmadığı ölçülür.
     Spiral için aynı işaret kısıtları (spiral_model.YONLER) korunur.

Yeni katsayılar uygulamaya otomatik YAZILMAZ; karar bu raporla verilir.

Kullanım:
    python pilot_analizi.py pilot_verisi/
Dosyalar kişi başına bir JSON'dur (nsosyal-pilot-<kod>.json). Klasör repoya girmez.
"""
import json
import math
import sys
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss, roc_auc_score
from sklearn.preprocessing import StandardScaler

from spiral_model import OZELLIK_ADLARI, YONLER, IsaretKisitliLojistik

BICIM = "nsosyal-pilot-1"
PSIKOLOJIK_OZELLIKLER = ["duygu", "dwell_saniye", "tiklama", "roket", "yorum"]
# local-agent.js SPIRAL_ETIKETI ile aynı: "yoğun" ya da "sinirli" cevabı 1.
SPIRAL_ETIKETI = {"anksiyete": 1, "sinirli": 1, "sakin": 0, "mutluluk": 0, "umut": 0}
MIN_KATILIMCI = 3


def yukle(klasor) -> list[dict]:
    """Geçerli dosyaları okur. Aynı katılımcı kodundan birden fazla dosya varsa
    en çok kayıt içereni alınır. Jüri demosu sırasında verilen cevaplar atılır."""
    katilimcilar = {}
    for yol in sorted(Path(klasor).glob("*.json")):
        try:
            veri = json.loads(yol.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(veri, dict) or veri.get("bicim") != BICIM or not veri.get("katilimci"):
            continue
        kayitlar = [k for k in veri.get("kayitlar", []) if not k.get("demo") and k.get("cevap") in SPIRAL_ETIKETI]
        onceki = katilimcilar.get(veri["katilimci"])
        if onceki is None or len(kayitlar) > len(onceki["kayitlar"]):
            katilimcilar[veri["katilimci"]] = {"kod": veri["katilimci"], "kayitlar": kayitlar}
    return [k for k in katilimcilar.values() if k["kayitlar"]]


def wilson(basari: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 1.0)
    p = basari / n
    merkez = (p + z * z / (2 * n)) / (1 + z * z / n)
    yari = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return (max(0.0, merkez - yari), min(1.0, merkez + yari))


def _psikolojik_ozellik(kayit) -> list[float]:
    """Ruh hali girdisi: son 30 dakikanın penceresindeki etkileşimlerin ağırlıklı
    ortalaması (oturum düzeyi). Eski biçimde (tek gönderi) o gönderinin sinyalleri."""
    psi = kayit["psikolojik"]
    if psi.get("pencere"):
        agirlik = np.array([p["agirlik"] for p in psi["pencere"]])
        X = np.array([[p["ozellik"][ad] for ad in PSIKOLOJIK_OZELLIKLER] for p in psi["pencere"]])
        return list(agirlik @ X / agirlik.sum())
    return [psi["ozellik"][ad] for ad in PSIKOLOJIK_OZELLIKLER]


def _auc(y, p):
    return float(roc_auc_score(y, p)) if len(set(y)) == 2 else None


def kayitli_tahminler(katilimcilar: list[dict]) -> dict:
    """Uygulamanın cevap anında kaydettiği tahminlerin uyumu."""
    tum = [k for kisi in katilimcilar for k in kisi["kayitlar"]]
    sonuc = {"katilimci": len(katilimcilar), "cevap": len(tum)}

    psi = [k for k in tum if k.get("psikolojik") and k["psikolojik"].get("varsayilan")]
    if psi:
        cevaplar = [k["cevap"] for k in psi]
        dogru = sum(k["psikolojik"]["varsayilan"] == k["cevap"] for k in psi)
        kisisel = [k for k in psi if k["psikolojik"].get("kisisel")]
        sonuc["psikolojik"] = {
            "n": len(psi), "uyum": dogru / len(psi), "aralik": wilson(dogru, len(psi)),
            "cogunluk": max(cevaplar.count(c) for c in set(cevaplar)) / len(psi), "rastgele": 1 / len(SPIRAL_ETIKETI),
            "kisisel_n": len(kisisel),
            "kisisel_uyum": sum(k["psikolojik"]["kisisel"] == k["cevap"] for k in kisisel) / len(kisisel) if kisisel else None,
        }

    spr = [k for k in tum if k.get("spiral")]
    if spr:
        y = np.array([SPIRAL_ETIKETI[k["cevap"]] for k in spr])
        p0 = np.array([k["spiral"]["p0"] for k in spr])
        dogru = int(((p0 >= 0.5).astype(int) == y).sum())
        sonuc["spiral"] = {
            "n": len(spr), "pozitif": float(y.mean()), "uyum": dogru / len(spr), "aralik": wilson(dogru, len(spr)),
            "cogunluk": max(y.mean(), 1 - y.mean()), "brier": float(brier_score_loss(y, p0)),
            "taban_brier": float(brier_score_loss(y, np.full(len(y), y.mean()))), "auc": _auc(y, p0),
        }
    return sonuc


def yeniden_egitim(katilimcilar: list[dict]) -> dict:
    """Birini dışarıda bırak: pilot verisiyle eğitilen model, sentetik model ve
    taban çizgisi, hiç görmedikleri katılımcıların cevaplarında karşılaştırılır."""
    if len(katilimcilar) < MIN_KATILIMCI:
        return {"yetersiz": f"en az {MIN_KATILIMCI} katılımcı gerekiyor, {len(katilimcilar)} var"}
    sonuc = {}

    # Spiral: işaret kısıtlı lojistik regresyon, sentetik modelle aynı yöntem.
    gercek, sentetik, pilot, taban = [], [], [], []
    for i, test in enumerate(katilimcilar):
        egitim = [k for j, kisi in enumerate(katilimcilar) if j != i for k in kisi["kayitlar"] if k.get("spiral")]
        deneme = [k for k in test["kayitlar"] if k.get("spiral")]
        y_egitim = np.array([SPIRAL_ETIKETI[k["cevap"]] for k in egitim])
        if not deneme or len(set(y_egitim)) < 2:
            continue
        X = lambda kayitlar: np.array([[k["spiral"]["ozellik"][ad] for ad in OZELLIK_ADLARI] for k in kayitlar])
        olcek = StandardScaler().fit(X(egitim))
        model = IsaretKisitliLojistik([YONLER[ad] for ad in OZELLIK_ADLARI]).fit(olcek.transform(X(egitim)), y_egitim)
        gercek += [SPIRAL_ETIKETI[k["cevap"]] for k in deneme]
        sentetik += [k["spiral"]["p0"] for k in deneme]
        pilot += list(model.predict_proba(olcek.transform(X(deneme)))[:, 1])
        taban += [float(y_egitim.mean())] * len(deneme)
    if gercek:
        y = np.array(gercek)
        sonuc["spiral"] = {"n": len(y), **{ad: {"brier": float(brier_score_loss(y, p)), "auc": _auc(y, np.array(p))}
                                          for ad, p in [("sentetik", sentetik), ("pilot", pilot), ("taban", taban)]}}

    # Ruh hali: çok sınıflı lojistik regresyon.
    gercek, sentetik, pilot, taban = [], [], [], []
    for i, test in enumerate(katilimcilar):
        egitim = [k for j, kisi in enumerate(katilimcilar) if j != i for k in kisi["kayitlar"] if k.get("psikolojik")]
        deneme = [k for k in test["kayitlar"] if k.get("psikolojik")]
        y_egitim = [k["cevap"] for k in egitim]
        if not deneme or len(set(y_egitim)) < 2:
            continue
        X = lambda kayitlar: np.array([_psikolojik_ozellik(k) for k in kayitlar])
        olcek = StandardScaler().fit(X(egitim))
        model = LogisticRegression(max_iter=1000).fit(olcek.transform(X(egitim)), y_egitim)
        gercek += [k["cevap"] for k in deneme]
        sentetik += [k["psikolojik"]["varsayilan"] for k in deneme]
        pilot += list(model.predict(olcek.transform(X(deneme))))
        taban += [max(set(y_egitim), key=y_egitim.count)] * len(deneme)
    if gercek:
        sonuc["psikolojik"] = {"n": len(gercek), **{ad: sum(a == b for a, b in zip(gercek, p)) / len(gercek)
                                                   for ad, p in [("sentetik", sentetik), ("pilot", pilot), ("taban", taban)]}}
    return sonuc


def _y(x) -> str:
    return f"%{100 * x:.0f}"


def _ab(aralik) -> str:
    return f"[{_y(aralik[0])}–{_y(aralik[1])}]"


def rapor(katilimcilar: list[dict]) -> str:
    kt, ye = kayitli_tahminler(katilimcilar), yeniden_egitim(katilimcilar)
    s = ["PİLOT ANALİZİ · python pilot_analizi.py", "=" * 72,
         f"{kt['katilimci']} katılımcı, {kt['cevap']} kontrol sorusu cevabı (jüri demosu cevapları hariç)", ""]
    s.append("1) Uygulamanın cevap anındaki tahminleri (önce tahmin, sonra öğrenme)")
    if "psikolojik" in kt:
        p = kt["psikolojik"]
        s.append(f"  Ruh hali (5 sınıf), n={p['n']}: uyum {_y(p['uyum'])} {_ab(p['aralik'])} · "
                 f"'hep en sık cevap' {_y(p['cogunluk'])} · rastgele {_y(p['rastgele'])}")
        if p["kisisel_uyum"] is not None:
            s.append(f"    kişisel uyarlama: {_y(p['kisisel_uyum'])} (n={p['kisisel_n']})")
    if "spiral" in kt:
        p = kt["spiral"]
        auc = f" · AUC {p['auc']:.2f}" if p["auc"] is not None else ""
        s.append(f"  Spiral ('yoğun/sinirli' cevabı), n={p['n']}, pozitif pay {_y(p['pozitif'])}: uyum {_y(p['uyum'])} "
                 f"{_ab(p['aralik'])} · 'hep en sık' {_y(p['cogunluk'])} · Brier {p['brier']:.3f} (taban {p['taban_brier']:.3f}){auc}")
    s += ["", "2) Gerçek veriyle yeniden eğitim (birini dışarıda bırak, katılımcı bazında)"]
    if "yetersiz" in ye:
        s.append(f"  Yapılmadı: {ye['yetersiz']}.")
    else:
        if "spiral" in ye:
            p = ye["spiral"]
            for ad, etiket in [("sentetik", "sentetik model"), ("pilot", "pilot verisiyle"), ("taban", "taban oranı")]:
                auc = f" · AUC {p[ad]['auc']:.2f}" if p[ad]["auc"] is not None else ""
                s.append(f"  Spiral, {etiket:16s} n={p['n']}: Brier {p[ad]['brier']:.3f}{auc}")
            iyi = p["pilot"]["brier"] < min(p["sentetik"]["brier"], p["taban"]["brier"])
            s.append("  → Pilot verisiyle eğitilen spiral modeli görmediği katılımcılarda daha az hata yapıyor; "
                     "spiral_model.py'nin eğitim verisine pilot cevapları eklenmeli." if iyi else
                     "  → Pilot verisiyle eğitim sentetik modeli ya da taban oranını geçmedi; sentetik model korunur.")
        if "psikolojik" in ye:
            p = ye["psikolojik"]
            s.append(f"  Ruh hali, n={p['n']}: sentetik {_y(p['sentetik'])} · pilot verisiyle {_y(p['pilot'])} · 'hep en sık' {_y(p['taban'])}")
    s += ["", "SINIRLILIKLAR: gönüllü ve küçük örneklem, geniş güven aralıkları; öz-bildirim klinik bir ölçüm",
          "değildir; 'yoğun/sinirli' cevabı spiral için yalnızca zayıf bir etikettir."]
    return "\n".join(s)


if __name__ == "__main__":
    klasor = sys.argv[1] if len(sys.argv) > 1 else "pilot_verisi"
    katilimcilar = yukle(klasor)
    if not katilimcilar:
        print(f"'{klasor}' klasöründe geçerli pilot dosyası yok (Ayarlar > Gönüllü pilot > indir).")
        sys.exit(1)
    metin = rapor(katilimcilar)
    print(metin)
    Path("pilot_sonuc.txt").write_text(metin + "\n", encoding="utf-8")
