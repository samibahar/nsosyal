"""
FastAPI backend — motor.py'deki gerçek skor motorunu (BERT duygu analizi +
eğitilmiş spiral sınıflandırıcı) ve psikolojik_durum.py'deki çok kategorili
anlık yorum sınıflandırıcısını bir web arayüzüne bağlar. Tek demo kullanıcı
için bellek-içi durum tutar (gerçek üretimde bu veritabanına/oturuma taşınır).
"""
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))  # motor.py, duygu_modeli.py, spiral_model.py kök dizinde

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from motor import gonderileri_puanla, sirala, spiral_olasiligi
from ornek_veri import ORNEK_GONDERILER, ORNEK_KULLANICI_ILGI
from psikolojik_durum import psikolojik_durum_tahmini, KATEGORILER

def _oturum_ortalamasi(gunluk: list[dict]) -> dict:
    """TÜM oturumdaki etkileşimlerin olasılık dağılımlarını ortalar (tek bir
    olaya göre değil). Her yeni etkileşim ortalamayı biraz kaydırır -- çubuklar
    ilk birkaç etkileşimde daha oynak, oturum uzadıkça yavaş yavaş durulur/dolar.
    Tek bir olayın (örn. tek bir roket tıklaması) sonucu tek başına ekrana
    %90+ gibi aşırı bir değer olarak yansımaz."""
    ortalama = {k: 0.0 for k in KATEGORILER}
    for kayit in gunluk:
        for kat, p in kayit["olasiliklar"].items():
            ortalama[kat] += p / len(gunluk)
    baskin = max(ortalama, key=ortalama.get)
    return {"kategori": baskin, "olasiliklar": {k: round(v, 3) for k, v in ortalama.items()}}

app = FastAPI(title="NSosyal Duygu-Duyarlı Katman — Kanıt-of-Konsept")

GONDERILER = ORNEK_GONDERILER
gonderileri_puanla(GONDERILER)
GONDERI_BY_ID = {g["id"]: g for g in GONDERILER}

KULLANICI_ILGI = ORNEK_KULLANICI_ILGI

DAVRANIS_GUNLUGU: list[dict] = []  # spiral modeli için kayan pencere (son 20)
PSIKOLOJIK_GUNLUK: list[dict] = []  # "haftalık" özet için tüm oturum kaydı


class Etkilesim(BaseModel):
    gonderi_id: int
    dwell_saniye: float
    tiklama: bool = False
    roket: bool = False
    yorum: bool = False


@app.get("/api/gonderiler")
def api_gonderiler():
    spiral = spiral_olasiligi(DAVRANIS_GUNLUGU, GONDERILER)
    siralanmis = sirala(GONDERILER, KULLANICI_ILGI, spiral)
    return {"spiral_seviyesi": round(spiral, 3), "gonderiler": siralanmis}


@app.post("/api/etkilesim")
def api_etkilesim(e: Etkilesim):
    DAVRANIS_GUNLUGU.append(e.model_dump())
    del DAVRANIS_GUNLUGU[:-20]  # kayan pencere: son 20 etkileşim
    spiral = spiral_olasiligi(DAVRANIS_GUNLUGU, GONDERILER)

    gonderi = GONDERI_BY_ID.get(e.gonderi_id)
    tekil_psikolojik = psikolojik_durum_tahmini(
        duygu=gonderi["duygu"] if gonderi else 0.0,
        dwell_saniye=e.dwell_saniye,
        tiklama=e.tiklama,
        roket=e.roket,
        yorum=e.yorum,
    )
    PSIKOLOJIK_GUNLUK.append({
        "saat": datetime.now().hour,
        "konu": gonderi["konu"] if gonderi else "bilinmiyor",
        "kategori": tekil_psikolojik["kategori"],       # özet istatistikleri için tekil olay
        "olasiliklar": tekil_psikolojik["olasiliklar"],  # pencere ortalaması için
    })
    psikolojik_oturum = _oturum_ortalamasi(PSIKOLOJIK_GUNLUK)

    return {"spiral_seviyesi": round(spiral, 3), "psikolojik_durum": psikolojik_oturum}


@app.get("/api/psikolojik-ozet")
def api_psikolojik_ozet():
    """Bu oturumda GERÇEKTEN kaydedilen etkileşimlerden özet — sabit örnek metin
    değil. 'Haftalık' değil (tek oturum), ama aynı mantığın küçük ölçekli, canlı
    kanıtı: hangi saatte / hangi konuda / hangi psikolojik kategoriye yönelik
    içerikte daha çok durulmuş."""
    toplam = len(PSIKOLOJIK_GUNLUK)
    kategori_sayaclari = Counter(kayit["kategori"] for kayit in PSIKOLOJIK_GUNLUK)
    konu_kategori = Counter((kayit["konu"], kayit["kategori"]) for kayit in PSIKOLOJIK_GUNLUK)
    saat_kategori = Counter((kayit["saat"], kayit["kategori"]) for kayit in PSIKOLOJIK_GUNLUK)

    en_cok_konu_kategori = konu_kategori.most_common(3)
    en_cok_saat_kategori = saat_kategori.most_common(3)

    return {
        "toplam_etkilesim": toplam,
        "kategoriler": KATEGORILER,
        "kategori_dagilimi": {k: kategori_sayaclari.get(k, 0) for k in KATEGORILER},
        "en_belirgin_konu_kategori": [
            {"konu": konu, "kategori": kat, "sayi": sayi}
            for (konu, kat), sayi in en_cok_konu_kategori
        ],
        "en_belirgin_saat_kategori": [
            {"saat": saat, "kategori": kat, "sayi": sayi}
            for (saat, kat), sayi in en_cok_saat_kategori
        ],
    }


@app.post("/api/sifirla")
def api_sifirla():
    DAVRANIS_GUNLUGU.clear()
    PSIKOLOJIK_GUNLUK.clear()
    return {"ok": True}


app.mount("/", StaticFiles(directory=BASE_DIR / "static", html=True), name="static")
