# -*- coding: utf-8 -*-
"""Karşı-olgusal etki analizi: duygu dengelemesi ne yapıyor, neye mal oluyor?

Jürinin "işe yaradığını nereden biliyorsunuz?", "neden bu katsayı?", "filtre
balonu olmaz mı?", "önemli haberi saklar mı?" sorularına ölçümle cevap vermek için.

YÖNTEM: Uygulamanın cihaz-içi sıralaması (static/local-agent.js, rank())
burada birebir yeniden yazıldı. Uygulamadaki gerçek gönderi havuzu (tonları
duygu modeliyle hesaplanır), sunucunun gerçek aday seçimi (aday_secimi.py,
48 aday) ve rastgele kullanıcı ilgi profilleriyle N senaryo üretilir; her
senaryoda aynı adaylar farklı politikalarla sıralanır.

BULGU VE TASARIM DEĞİŞİKLİĞİ (11.09.2026): İlk sürüm yoğun tonlu gönderinin
PUANINDAN ceza düşüyordu (|ton| × yoğunluk × 0,62). Ölçüm, bunun fiilen bir
filtre olduğunu gösterdi: 48 aday arasında yeterince alternatif olduğu için
12. sıradaki gönderiyle arasındaki farktan büyük her ceza yoğun gönderiyi ilk
sayfadan tamamen çıkarıyordu (yoğunluk 0,85'te ilk sayfadaki yoğun pay %97
azalıyor, yoğun gönderilerin yalnızca %25'i ilk üç sayfada kalıyordu).
Katsayıyı küçültmek "nazik" bir ara nokta vermedi (bkz. bölüm 4).
Yeni sürüm DOZ (kota) tabanlıdır: sayfadaki yoğun tonlu içerik payı akış
yoğunluğuyla orantılı bir hedefe indirilir, hedef = taban pay × (1 − α ×
yoğunluk), α = 0,6. Yoğun gönderiler silinmez ve topluca aşağı atılmaz;
aralıklanır. Yaklaşım, öneri sistemlerinde "kalibre edilmiş öneri" (Steck,
RecSys 2018) fikrinin maruziyet payına uygulanmasıdır.
Aynı ölçüm, çeşitlilik bonusunun adayların GELİŞ sırasına göre verildiğini ve
bunun ilgi kaybına yol açtığını da gösterdi; bonus artık ÇIKTI sırasına göre
(açgözlü seçim) verilir.

DİKKAT: Bu bir MARUZİYET ölçümüdür (kullanıcı neyi görüyor). Kullanıcının
iyi-oluşunun değiştiğini göstermez; o ancak gerçek kullanıcılarla ölçülebilir.
Sonuçlar etki_analizi_sonuc.txt'e yazılır.
"""
import random
from pathlib import Path

import numpy as np

from aday_secimi import aday_listesi, dogal_cesitlilik_ekle
from ornek_veri import ORNEK_GONDERILER, ORNEK_KULLANICI_ILGI
from resmi_veri import RESMI_GONDERILER, RESMI_HESAPLAR
from topluluk_veri import TOPLULUK_GONDERILERI

YOGUN = -0.15            # local-agent.js: dengelemenin uygulandığı ton eşiği
DENGE_ESIGI = 0.28       # local-agent.js: yoğunluk bu değerin üstündeyse dengeleme başlar
DOZ_ALFA = 0.6           # local-agent.js: en yoğun durumda payın en fazla %60'ı azaltılır
SAYFA = 12
ADAY = 48
SENARYO = 600
YOGUNLUKLAR = [0.35, 0.6, 0.85]
ALFALAR = [0.3, 0.45, 0.6, 0.75, 0.9]
ESKI_KATSAYILAR = [0.1, 0.2, 0.4, 0.62]
KONULAR = sorted(ORNEK_KULLANICI_ILGI)
satirlar: list[str] = []


def yaz(metin: str = ""):
    print(metin, flush=True)
    satirlar.append(metin)


def gonderi_havuzu() -> list[dict]:
    from duygu_modeli import duygu_skoru
    havuz = []
    for g in [*ORNEK_GONDERILER, *TOPLULUK_GONDERILERI, *RESMI_GONDERILER]:
        ilgi = ORNEK_KULLANICI_ILGI.get(g["konu"], 0.3)
        havuz.append({**g, "duygu": duygu_skoru(g["metin"]), "ilgi_skoru": ilgi, "final_skor": ilgi,
                      "resmi": g.get("yazar") in RESMI_HESAPLAR})
    return havuz


def _bonus(n: int) -> float:
    return -0.09 * n if n else 0.07


def _kalemler(adaylar, agirliklar):
    maks = max([0.25, *agirliklar.values()])
    return [{"g": g, "ilgi": agirliklar.get(g["konu"], 0) / maks,
             "yogun": g["duygu"] < YOGUN and not g.get("resmi"),
             "cekirdek": g["ilgi_skoru"] * 0.48 + agirliklar.get(g["konu"], 0) / maks * 0.34 - sira * 0.0005}
            for sira, g in enumerate(adaylar)]


def dozlu_sirala(adaylar, agirliklar, yogunluk, alfa=DOZ_ALFA, dengeleme=True):
    """local-agent.js rank() ile aynı (yeterli veri var, son tepki yok):
    açgözlü seçim; çeşitlilik bonusu seçilen listeye göre; yoğun tonlu
    gönderi ancak o ana kadarki yoğun sayısı kotanın altındaysa seçilebilir.
    Kota: round(hedef × sıra). Uygun başka aday kalmadıysa kota aşılır
    (hiçbir gönderi listeden çıkmaz)."""
    kalan = _kalemler(adaylar, agirliklar)
    aktif = dengeleme and yogunluk > DENGE_ESIGI
    taban = sum(k["yogun"] for k in kalan) / max(1, len(kalan))
    hedef = taban * (1 - alfa * yogunluk) if aktif else 1.0
    sonuc, gorulen, yogun_sayisi = [], {}, 0
    while kalan:
        izin = int(hedef * (len(sonuc) + 1) + 0.5)
        uygun = [k for k in kalan if not k["yogun"] or yogun_sayisi < izin] or kalan
        en_iyi = max(uygun, key=lambda k: k["cekirdek"] + _bonus(gorulen.get(k["g"]["konu"], 0)))
        en_iyi["skor"] = en_iyi["cekirdek"] + _bonus(gorulen.get(en_iyi["g"]["konu"], 0))
        gorulen[en_iyi["g"]["konu"]] = gorulen.get(en_iyi["g"]["konu"], 0) + 1
        yogun_sayisi += en_iyi["yogun"]
        sonuc.append(en_iyi)
        kalan.remove(en_iyi)
    return sonuc


def eski_sirala(adaylar, agirliklar, yogunluk, katsayi=0.62):
    """11.09.2026 öncesi local-agent.js: puandan ceza, çeşitlilik bonusu geliş sırasına göre."""
    kalemler, gorulen = _kalemler(adaylar, agirliklar), {}
    for k in kalemler:
        ton = k["g"]["duygu"]
        ceza = abs(ton) * yogunluk * katsayi if (not k["g"].get("resmi") and yogunluk > DENGE_ESIGI and ton < YOGUN) else 0.0
        n = gorulen.get(k["g"]["konu"], 0)
        k["skor"] = k["cekirdek"] - ceza + _bonus(n)
        gorulen[k["g"]["konu"]] = n + 1
    return sorted(kalemler, key=lambda k: -k["skor"])


def sert_filtre(adaylar, agirliklar, yogunluk):
    if yogunluk > DENGE_ESIGI:
        adaylar = [g for g in adaylar if g.get("resmi") or g["duygu"] >= YOGUN]
    return dozlu_sirala(adaylar, agirliklar, yogunluk, dengeleme=False)


def sunucu_sirasi(adaylar, agirliklar, yogunluk):
    return _kalemler(adaylar, agirliklar)


def olc(sirali, adaylar) -> dict:
    ilk = sirali[:SAYFA]
    yogunlar = [g["id"] for g in adaylar if g["duygu"] < YOGUN and not g.get("resmi")]
    konum = {k["g"]["id"]: i for i, k in enumerate(sirali)}
    return {"yogun": float(np.mean([k["g"]["duygu"] < YOGUN for k in ilk])),
            "ilgi": float(np.mean([k["ilgi"] for k in ilk])),
            "konu": len({k["g"]["konu"] for k in ilk}),
            "erisim": float(np.mean([konum.get(i, 10 ** 6) < 3 * SAYFA for i in yogunlar])) if yogunlar else np.nan}


def senaryolar(havuz):
    rng, prng = np.random.default_rng(11), random.Random(11)
    for s in range(SENARYO):
        agirliklar = dict(zip(KONULAR, rng.dirichlet(np.full(len(KONULAR), 0.6))))
        siralanmis = dogal_cesitlilik_ekle(sorted(havuz, key=lambda g: -g["final_skor"]), rng=prng)
        yield YOGUNLUKLAR[s % len(YOGUNLUKLAR)], agirliklar, aday_listesi(siralanmis, set(), ADAY)


def main():
    havuz = gonderi_havuzu()
    yaz("ETKİ ANALİZİ (python etki_analizi.py)")
    yaz("=" * 72)
    yaz(f"{len(havuz)} gönderilik havuz, yoğun tonlu (ton < {YOGUN}) payı %{100 * np.mean([g['duygu'] < YOGUN for g in havuz]):.1f}; "
        f"{SENARYO} senaryo (rastgele ilgi profili × {ADAY} aday × yoğunluk {YOGUNLUKLAR})")
    yaz("Ölçütler ilk sayfadaki 12 gönderi üzerinde; erişim = yoğun gönderilerin ilk 3 sayfada (36) kalma oranı.")
    yaz("Bu bir maruziyet ölçümüdür, iyi-oluş ölçümü değildir.")
    yaz()

    politikalar = {
        "A dengeleme yok": lambda a, w, y: dozlu_sirala(a, w, y, dengeleme=False),
        "B doz α=0,6 (uygulamadaki)": lambda a, w, y: dozlu_sirala(a, w, y),
        "E eski: puandan ceza 0,62": eski_sirala,
        "C sert filtre": sert_filtre,
        "D kişiselleştirmesiz": sunucu_sirasi,
    }
    sonuc = {ad: {y: [] for y in YOGUNLUKLAR} for ad in politikalar}
    alfa_sonuc = {(a, y): [] for a in ALFALAR for y in (0.6, 0.85)}
    eski_sonuc = {(k, y): [] for k in [0.0, *ESKI_KATSAYILAR] for y in (0.6, 0.85)}
    resmi_ihlal = resmi_sayisi = 0
    aralik = []
    for yogunluk, agirliklar, adaylar in senaryolar(havuz):
        for ad, politika in politikalar.items():
            sonuc[ad][yogunluk].append(olc(politika(adaylar, agirliklar, yogunluk), adaylar))
        a = {k["g"]["id"]: i for i, k in enumerate(dozlu_sirala(adaylar, agirliklar, yogunluk, dengeleme=False))}
        b_sirali = dozlu_sirala(adaylar, agirliklar, yogunluk)
        b = {k["g"]["id"]: i for i, k in enumerate(b_sirali)}
        for g in adaylar:
            if g.get("resmi"):
                resmi_sayisi += 1
                resmi_ihlal += b[g["id"]] > a[g["id"]] + 1  # çevresindekiler kayınca ±1 oynayabilir
        konumlar = [i for i, k in enumerate(b_sirali[:3 * SAYFA]) if k["yogun"]]
        aralik += list(np.diff(konumlar))
        for (alfa, y) in alfa_sonuc:
            alfa_sonuc[(alfa, y)].append(olc(dozlu_sirala(adaylar, agirliklar, y, alfa=alfa), adaylar))
        for (k, y) in eski_sonuc:
            sirali = eski_sirala(adaylar, agirliklar, y, katsayi=k) if k else eski_sirala(adaylar, agirliklar, 0.0)
            eski_sonuc[(k, y)].append(olc(sirali, adaylar))

    ort = lambda liste, anahtar: float(np.nanmean([m[anahtar] for m in liste]))
    yaz("1) Politikalar (ilk sayfa ortalamaları; ilgi = A'ya göre korunan pay)")
    for y in YOGUNLUKLAR:
        yaz(f"  Akış yoğunluğu {y}:")
        taban = sonuc["A dengeleme yok"][y]
        for ad in politikalar:
            m = sonuc[ad][y]
            yaz(f"    {ad:28s} yoğun pay %{100 * ort(m, 'yogun'):5.1f} (−%{100 * (1 - ort(m, 'yogun') / ort(taban, 'yogun')):3.0f}) · "
                f"ilgi %{100 * ort(m, 'ilgi') / ort(taban, 'ilgi'):5.1f} · konu {ort(m, 'konu'):4.1f} · erişim %{100 * ort(m, 'erisim'):3.0f}")
    yaz()
    yaz("2) Doz dengelemesinin güvenceleri")
    yaz(f"  Resmi/acil gönderinin dengeleme yüzünden aşağı indiği durum: {resmi_ihlal}/{resmi_sayisi}")
    yaz(f"  İlk 3 sayfada yoğun gönderiler arası ortalama mesafe: {np.mean(aralik):.1f} sıra (art arda gelme oranı %{100 * np.mean(np.array(aralik) == 1):.0f})")
    yaz()
    yaz("3) α duyarlılığı (doz; hedef pay = taban × (1 − α × yoğunluk))")
    for y in (0.6, 0.85):
        taban = sonuc["A dengeleme yok"][0.85] if y == 0.85 else sonuc["A dengeleme yok"][0.6]
        for alfa in ALFALAR:
            m = alfa_sonuc[(alfa, y)]
            isaret = "  ← uygulamadaki" if alfa == DOZ_ALFA else ""
            yaz(f"    yoğunluk {y} · α {alfa:<4} yoğun pay −%{100 * (1 - ort(m, 'yogun') / ort(taban, 'yogun')):3.0f} "
                f"(hedef −%{100 * alfa * y:3.0f}) · ilgi %{100 * ort(m, 'ilgi') / ort(taban, 'ilgi'):5.1f} · erişim %{100 * ort(m, 'erisim'):3.0f}{isaret}")
    yaz()
    yaz("4) Eski yaklaşım (puandan ceza, geliş sırası çeşitlilik) neden bırakıldı")
    for y in (0.6, 0.85):
        taban = eski_sonuc[(0.0, y)]
        for k in ESKI_KATSAYILAR:
            m = eski_sonuc[(k, y)]
            yaz(f"    yoğunluk {y} · katsayı {k:<4} yoğun pay −%{100 * (1 - ort(m, 'yogun') / ort(taban, 'yogun')):3.0f} · "
                f"ilgi %{100 * ort(m, 'ilgi') / ort(taban, 'ilgi'):5.1f} · erişim %{100 * ort(m, 'erisim'):3.0f}")
    yaz("  Küçük katsayı az azaltıyor, büyük katsayı içeriği sayfadan tümüyle atıyor; maruziyet payını")
    yaz("  doğrudan hedefleyen bir ayar yok. Doz yaklaşımında azaltma oranı α × yoğunluk ile doğrudan belirlenir.")
    (Path(__file__).resolve().parent / "etki_analizi_sonuc.txt").write_text("\n".join(satirlar) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
