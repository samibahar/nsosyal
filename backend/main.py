"""
FastAPI backend — motor.py'deki gerçek skor motorunu (BERT duygu analizi +
eğitilmiş spiral sınıflandırıcı) bir web arayüzüne bağlar. Tek demo kullanıcı
için bellek-içi durum tutar (gerçek üretimde bu veritabanına/oturuma taşınır).
"""
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))  # motor.py, duygu_modeli.py, spiral_model.py kök dizinde

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from motor import gonderileri_puanla, sirala, spiral_olasiligi

app = FastAPI(title="NSosyal Duygu-Duyarlı Katman — Kanıt-of-Konsept")

GONDERILER = [
    {"id": 1, "konu": "spor", "metin": "Takımımız bu hafta harika bir galibiyet aldı, çok sevindim!"},
    {"id": 2, "konu": "spor", "metin": "Transfer draması yüzünden taraftarlar arasında büyük öfke var."},
    {"id": 3, "konu": "gundem", "metin": "Mahkeme, savaş suçlarından idam cezasına mahkum etti."},
    {"id": 4, "konu": "gundem", "metin": "Yeni bir toplantı yarın saat 14.00'te başlayacak."},
    {"id": 5, "konu": "spor", "metin": "Antrenman sonrası oyuncular keyifli bir sohbet yaptı."},
    {"id": 6, "konu": "gundem", "metin": "Tutuklama haberi sonrası sosyal medyada büyük kaygı oluştu."},
    {"id": 7, "konu": "teknoloji", "metin": "Yeni yapay zekâ modeli beklentilerin çok üzerinde başarı gösterdi."},
    {"id": 8, "konu": "gundem", "metin": "Deprem sonrası bölgede büyük yıkım ve can kaybı yaşandı."},
]
gonderileri_puanla(GONDERILER)

KULLANICI_ILGI = {"spor": 0.9, "gundem": 0.5, "teknoloji": 0.6}

DAVRANIS_GUNLUGU: list[dict] = []


class Etkilesim(BaseModel):
    gonderi_id: int
    dwell_saniye: float
    tiklama: bool = False


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
    return {"spiral_seviyesi": round(spiral, 3)}


@app.post("/api/sifirla")
def api_sifirla():
    DAVRANIS_GUNLUGU.clear()
    return {"ok": True}


app.mount("/", StaticFiles(directory=BASE_DIR / "static", html=True), name="static")
