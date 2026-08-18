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
from ornek_veri import ORNEK_GONDERILER, ORNEK_KULLANICI_ILGI

app = FastAPI(title="NSosyal Duygu-Duyarlı Katman — Kanıt-of-Konsept")

GONDERILER = ORNEK_GONDERILER
gonderileri_puanla(GONDERILER)

KULLANICI_ILGI = ORNEK_KULLANICI_ILGI

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
