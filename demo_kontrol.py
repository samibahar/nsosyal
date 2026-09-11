# -*- coding: utf-8 -*-
"""Canlı demo öncesi kontrol listesi. Sunucu açıkken:

    python demo_kontrol.py                 # http://localhost:8000
    python demo_kontrol.py http://adres:port

Her maddeyi ✓ / ✗ olarak yazar; biri bile başarısızsa çıkış kodu 1'dir.
Tarayıcıda uçtan uca kontrol için ayrıca: python -m pytest tests/e2e -q
"""
import gzip
import json
import sys
import urllib.request

ADRES = (sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000").rstrip("/")
BEKLENEN_MODEL = "bert-turkish-sentiment-ince-ayarli-v3"
SAYFALAR = ["/index.html", "/haberler.html", "/rapor.html", "/ayarlar.html", "/kesfet.html", "/profil.html?u=emiryusuf", "/juri.html"]


def al(yol: str, gzipli: bool = False):
    istek = urllib.request.Request(ADRES + yol, headers={"Accept-Encoding": "gzip"} if gzipli else {})
    with urllib.request.urlopen(istek, timeout=15) as yanit:
        govde = yanit.read()
        if yanit.headers.get("Content-Encoding") == "gzip":
            govde = gzip.decompress(govde)
        return yanit.status, yanit.headers, govde  # başlık adları harf duyarsız kalsın


def json_al(yol: str):
    return json.loads(al(yol)[2].decode("utf-8"))


def main() -> int:
    sonuclar = []

    def kontrol(ad, islem):
        try:
            aciklama = islem()
            sonuclar.append((True, ad, aciklama))
        except Exception as hata:
            sonuclar.append((False, ad, str(hata)))

    def sayfalar():
        hatali = [yol for yol in SAYFALAR if al(yol)[0] != 200]
        assert not hatali, f"açılmayan: {hatali}"
        return f"{len(SAYFALAR)} sayfa açılıyor"

    def model():
        durum = json_al("/api/durum")
        assert durum["duygu_modeli"] == BEKLENEN_MODEL, (
            f"yüklü model {durum['duygu_modeli']!r}; LFS dosyası inmemiş olabilir (git lfs pull), sonra sunucuyu yeniden başlatın")
        return f"{durum['duygu_modeli']} · {durum['gonderi_sayisi']} gönderi · yoğun pay %{100 * durum['yogun_pay']:.0f}"

    def adaylar():
        veri = json_al("/api/gonderiler?sifirdan=true&aday=48")
        konular = {g["konu"] for g in veri["gonderiler"]}
        assert len(veri["gonderiler"]) == 48 and len(konular) >= 8, f"{len(veri['gonderiler'])} aday, {len(konular)} konu"
        return f"48 aday · {len(konular)} konu"

    def demo():
        paket = json_al("/api/demo-paketi")
        assert len(paket["gonderiler"]) == 12 and len(paket["senaryo"]) == 10
        return "12 aday + 10 sinyal"

    def sikistirma():
        _, basliklar, _ = al("/api/gonderiler?sifirdan=true&aday=48", gzipli=True)
        assert basliklar.get("Content-Encoding") == "gzip", "gzip yok"
        return "aday listesi gzip'li"

    kontrol("Sayfalar", sayfalar)
    kontrol("Duygu modeli (v3, LFS)", model)
    kontrol("48 aday listesi", adaylar)
    kontrol("Jüri demo paketi", demo)
    kontrol("Sıkıştırma", sikistirma)

    for basarili, ad, aciklama in sonuclar:
        print(f"{'✓' if basarili else '✗'} {ad}: {aciklama}")
    return 0 if all(basarili for basarili, _, _ in sonuclar) else 1


if __name__ == "__main__":
    sys.exit(main())
