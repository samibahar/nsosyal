"""
FastAPI backend — motor.py'deki gerçek skor motorunu (BERT duygu analizi +
eğitilmiş spiral sınıflandırıcı) ve psikolojik_durum.py'deki çok kategorili
anlık yorum sınıflandırıcısını bir web arayüzüne bağlar. Tek demo kullanıcı
için bellek-içi durum tutar (gerçek üretimde bu veritabanına/oturuma taşınır).
"""
import random
import sys
import time
from collections import Counter
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))  # motor.py, duygu_modeli.py, spiral_model.py kök dizinde

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from motor import gonderileri_puanla, sirala, spiral_olasiligi
from ornek_veri import ORNEK_GONDERILER, ORNEK_KULLANICI_ILGI
from topluluk_veri import TOPLULUK_GONDERILERI
from sosyal_veri import SosyalDepo
from duygu_katmani import analiz_et
from psikolojik_durum import (
    psikolojik_durum_tahmini, KATEGORILER, kisisel_model_olustur, kisisel_guncelle,
)
import haftalik_rapor

app = FastAPI(title="NSosyal Duygu-Duyarlı Katman — Kanıt-of-Konsept")

DEPO = SosyalDepo(BASE_DIR / "data" / "nsosyal_demo.sqlite3")
DEPO.hazirla([*ORNEK_GONDERILER, *TOPLULUK_GONDERILERI])
GONDERILER = DEPO.gonderileri_yukle()
gonderileri_puanla(GONDERILER)
GONDERI_BY_ID = {g["id"]: g for g in GONDERILER}

KULLANICI_ILGI = ORNEK_KULLANICI_ILGI

SAYFA_BOYU = 12

DAVRANIS_GUNLUGU: list[dict] = []  # spiral modeli için kayan pencere (son 20, gönderi başına 1 kayıt)
PSIKOLOJIK_GUNLUK: list[dict] = []  # oturum özeti için (gönderi başına 1 kayıt)
GOSTERILEN_ID_SETI: set[int] = set()  # sayfalama: bu oturumda zaten sunulan gönderiler
SON_ETKILESIMLER: dict[int, dict] = {}  # gonderi_id -> o gönderiye dair BİRLEŞTİRİLMİŞ ham sinyal

TAM_GUVEN_ESIGI = 8  # spiral oranı bu kadar farklı gönderi görülmeden tam güvenilir sayılmaz

# --- Kendi kendini doğrulama / aktif öğrenme döngüsü ---
# psikolojik_durum.py'nin davranış->kategori eşlemesi (örn. "negatif duygu +
# yoğun roket/yorum = sinirli") sentetik senaryolara dayanıyor, gerçek insan
# verisine değil. Bunu
# "doğrulanmış" gibi sunmak yerine, kullanıcıya ara sıra hafif bir onay sorusu
# sorup CEVABINI modelin tahminiyle karşılaştırıyoruz -- gerçek bir dayanak
# ancak böyle oluşur. Bkz. CLAUDE.md "Kendi Kendini Doğrulayan Aktif Öğrenme".
DOGRULAMA_GUNLUGU: list[dict] = []
DOGRULAMA_ARALIGI = 20  # daha az invaziv: yaklaşık her 20 anlamlı etkileşimde bir
SAYAC = {"son_dogrulamadan_beri": 0}
MUDAHALE_DURUMU = {"son_gosterim": 0.0, "sessize_alindi": 0.0}
MUDAHALE_SOGUMA_SURESI = 20 * 60

# --- Kişiselleştirme (çevrimiçi/online öğrenme) ---
# _VARSAYILAN_MODEL (psikolojik_durum.py içinde) hiç değişmez. KISISEL_MODEL,
# her doğrulama cevabından sonra küçük bir SGD adımıyla güncellenen bağımsız
# bir kopya. Arayüzdeki anahtar, hangisinin akışa yansıdığını seçer.
KISISEL_MODEL = kisisel_model_olustur()
KISISEL_MOD = {"aktif": False}
KISISEL_GUNCELLEME_SAYISI = {"deger": 0}
SON_HAM_OZELLIK = {"deger": None}  # en son etkileşimin [duygu, dwell, tiklama, roket, yorum] hâli


class Etkilesim(BaseModel):
    gonderi_id: int
    dwell_saniye: float
    tiklama: bool = False
    roket: bool = False
    yorum: bool = False
    cikis: bool = False


class DogrulamaCevabi(BaseModel):
    kullanici_cevabi: str


class YeniGonderi(BaseModel):
    metin: str
    konu: str = "gundem"


class YorumYeni(BaseModel):
    metin: str


def _gonderi_bazinda_yerine_koy(gunluk: list[dict], gonderi_id: int, yeni_kayit: dict):
    """Aynı gönderiye ait önceki kaydı kaldırıp yenisini sona ekler -- her
    gönderinin günlükte en fazla bir kaydı olur, kaç kez etkileşim gelirse gelsin."""
    gunluk[:] = [k for k in gunluk if k.get("gonderi_id") != gonderi_id]
    gunluk.append(yeni_kayit)


def _sinyalleri_birlestir(gonderi_id: int, e: "Etkilesim") -> dict:
    """Aynı gönderi için art arda gelen etkileşimleri (roket sonra scroll-away
    dwell'i, ya da spam tıklama) TEK bir birleşik sinyale indirger: en uzun
    görünen süre + o ana kadarki tüm açık eylemlerin (OR) toplamı. Bu olmadan,
    örneğin bir gönderiye roket atıp sonra kaydırıp uzaklaşınca, scroll-away
    olayı roket sinyalini SESSİZCE ezip kaybediyordu."""
    onceki = SON_ETKILESIMLER.get(gonderi_id, {"dwell_saniye": 0.0, "tiklama": False, "roket": False, "yorum": False})
    birlesik = {
        "dwell_saniye": max(onceki["dwell_saniye"], e.dwell_saniye),
        "tiklama": onceki["tiklama"] or e.tiklama,
        "roket": onceki["roket"] or e.roket,
        "yorum": onceki["yorum"] or e.yorum,
    }
    SON_ETKILESIMLER[gonderi_id] = birlesik
    return birlesik


def _bolumu_kapat(gonderi_id: int, cikis: bool):
    """Bir gönderinin görünüm bölümü (episode) kapandığında (kullanıcı gerçekten
    kaydırıp uzaklaştığında) SON_ETKILESIMLER'daki kaydı temizler. Bu olmadan,
    örneğin sayfanın başındaki bir gönderiye normal hızda bakıp (uzun dwell)
    sonra hızlı aşağı kaydırıp geri hızlı yukarı çıkınca, o eski uzun dwell
    max() ile "diriliyor" ve az önceki hızlı geçişi -- gerçekte kısa süren bir
    an -- sanki uzun sürmüş gibi günlüğe yazıyordu; bu da kaydırma_hızı
    özelliğini yanlışlıkla düşürüp spiral barının geri hızlı yukarı çıkışta
    aniden düşmesine yol açıyordu (kullanıcı tarafından tespit edildi,
    21.08.2026). Roket/yorum gibi görünüm SIRASINDA gelen olaylar bölümü
    KAPATMAZ -- sadece kaydırıp-uzaklaşma (cikis=true) kapatır."""
    if cikis:
        SON_ETKILESIMLER.pop(gonderi_id, None)


def _katki_agirligi(sinyal: dict) -> float:
    """Bir etkileşimin oturum ortalamasına katkı ağırlığı. Çok kısa, edilgen
    bir görünme (örn. hızlı kaydırırken 0.4sn görünüp geçme) tam bir gözlem
    gibi sayılmamalı -- yoksa sırf çok sayıda gönderiyi hızlıca geçmek bile
    barları tek başına domine edebiliyordu ("kaç gönderi gördüm" ayrı bir
    sinyal, "tespit edilen durum" barındaki kaydırma hızı özelliği onu zaten
    ölçüyor). Roket/yorum/tıklama gibi açık bir eylem varsa süre kısa olsa
    bile niyet açıktır, tam ağırlık verilir."""
    if sinyal["tiklama"] or sinyal["roket"] or sinyal["yorum"]:
        return 1.0
    return min(1.0, max(0.15, sinyal["dwell_saniye"] / 4.0))


def _aktif_model():
    """Arayüzdeki anahtara göre hangi modelin (varsayılan/kişisel) akışa
    yansıyacağını döndürür. None -> psikolojik_durum_tahmini VARSAYILANI kullanır."""
    return KISISEL_MODEL if KISISEL_MOD["aktif"] else None


def _oturum_ortalamasi(gunluk: list[dict]) -> dict:
    """TÜM oturumdaki (gönderi başına tekil) etkileşimlerin AĞIRLIKLI olasılık
    dağılımlarını ortalar (ağırlık = _katki_agirligi). Çubuklar ilk birkaç
    etkileşimde daha oynak, oturum uzadıkça yavaş yavaş durulur/dolar."""
    if not gunluk:
        return {"kategori": None, "olasiliklar": {k: 0.0 for k in KATEGORILER}}
    toplam_agirlik = sum(k.get("agirlik", 1.0) for k in gunluk) or 1e-9
    ortalama = {k: 0.0 for k in KATEGORILER}
    for kayit in gunluk:
        agirlik = kayit.get("agirlik", 1.0)
        for kat, p in kayit["olasiliklar"].items():
            ortalama[kat] += p * agirlik / toplam_agirlik
    baskin = max(ortalama, key=ortalama.get)
    return {"kategori": baskin, "olasiliklar": {k: round(v, 3) for k, v in ortalama.items()}}


def _guven_carpani(ornek_sayisi: int) -> float:
    """Az sayıda farklı gönderiyle (örn. sadece 2-3) hesaplanan bir ORAN
    istatistiksel olarak güvenilmez -- küçük örneklemde kolayca %0 ya da
    %100'e savrulur. Yeterli veri (TAM_GUVEN_ESIGI kadar farklı gönderi)
    birikene kadar GÖSTERİLEN değeri kademeli yumuşatıyoruz; hesaplanan
    olasılığın kendisini değiştirmiyoruz, sadece ekrana yansıyan güveni."""
    return min(1.0, ornek_sayisi / TAM_GUVEN_ESIGI)


def _dogal_cesitlilik_ekle(siralanmis: list[dict], genlik: float = 0.08) -> list[dict]:
    """Aynı ilgi skoruna sahip gönderiler (örn. hepsi 'spor') her sayfa
    yüklemesinde birebir aynı sırada gelmesin diye final_skor'a küçük bir
    rastgele gürültü ekleyip yeniden sıralar. motor.py'nin kendisi kasıtlı
    olarak deterministik bırakıldı (spike_poc.py'deki örnek çıktı tekrar
    üretilebilir kalsın diye) -- gürültü sadece burada, sunum katmanında."""
    gurultulu = [(g, g["final_skor"] + random.uniform(-genlik, genlik)) for g in siralanmis]
    gurultulu.sort(key=lambda cift: -cift[1])
    return [g for g, _ in gurultulu]


def _sosyal_ile_zenginlestir(gonderiler: list[dict]) -> list[dict]:
    """Sıralama motorunun çıktısını kalıcı sosyal durumla birleştirir.
    Model skoru ve sosyal sayaçlar birbirinden bağımsız kalır."""
    sonuc = []
    for gonderi in gonderiler:
        yazar = DEPO.kullanici(gonderi.get("yazar", "emiryusuf"))
        sonuc.append({
            **gonderi,
            "yazar_bilgi": yazar,
            **DEPO.post_ozellikleri(gonderi["id"]),
        })
    return sonuc


def _kalibrasyon_guveni() -> float:
    """Kullanıcı doğrulaması arttıkça modelin davranışsal yorumuna verilen ağırlık.
    Az sayıda geri bildirimde nötr güven kullanılır; doğrulama hiçbir zaman tek
    başına müdahale kararı vermez."""
    if len(DOGRULAMA_GUNLUGU) < 3:
        return 0.5
    son = DOGRULAMA_GUNLUGU[-20:]
    eslesme = sum(1 for kayit in son if kayit["eslesme"]) / len(son)
    return round(0.3 + 0.7 * eslesme, 3)


def _duygu_durumu() -> dict:
    analiz = analiz_et(DAVRANIS_GUNLUGU, GONDERILER, _kalibrasyon_guveni())
    simdi = time.time()
    mudahale = analiz["surdurulmus_oruntu"] and simdi >= max(MUDAHALE_DURUMU["son_gosterim"] + MUDAHALE_SOGUMA_SURESI, MUDAHALE_DURUMU["sessize_alindi"])
    if mudahale:
        MUDAHALE_DURUMU["son_gosterim"] = simdi
    return {**analiz, "mudahale_uygun": mudahale, "kalibrasyon_guveni": _kalibrasyon_guveni()}


@app.get("/api/gonderiler")
def api_gonderiler(sifirdan: bool = False):
    if sifirdan:
        GOSTERILEN_ID_SETI.clear()

    spiral = spiral_olasiligi(DAVRANIS_GUNLUGU, GONDERILER)
    siralanmis = sirala(GONDERILER, KULLANICI_ILGI, spiral)
    siralanmis = _dogal_cesitlilik_ekle(siralanmis)

    kalanlar = [g for g in siralanmis if g["id"] not in GOSTERILEN_ID_SETI]
    sayfa = kalanlar[:SAYFA_BOYU]
    for g in sayfa:
        GOSTERILEN_ID_SETI.add(g["id"])

    return {
        "spiral_seviyesi": round(spiral, 3),
        "gonderiler": _sosyal_ile_zenginlestir(sayfa),
        "tukendi": len(kalanlar) <= SAYFA_BOYU,
    }


@app.post("/api/gonderiler")
def api_gonderi_olustur(yeni: YeniGonderi):
    """Demo kullanıcısının gönderisini gerçek duygu skoru ile canlı akışa ekler.
    Kalıcı kullanıcı/veritabanı katmanı olmadığı için kayıt süreç belleğiyle sınırlıdır."""
    metin = yeni.metin.strip()
    if not metin:
        return {"ok": False, "hata": "Gönderi metni boş olamaz."}
    if len(metin) > 500:
        return {"ok": False, "hata": "Gönderi en fazla 500 karakter olabilir."}

    konu = yeni.konu.strip().lower() or "gundem"
    yeni_id = max(GONDERI_BY_ID, default=0) + 1
    gonderi = {"id": yeni_id, "metin": metin, "konu": konu, "yazar": "emiryusuf"}
    gonderileri_puanla([gonderi])
    DEPO.gonderi_olustur(yeni_id, metin, konu)
    GONDERILER.insert(0, gonderi)
    GONDERI_BY_ID[yeni_id] = gonderi
    GOSTERILEN_ID_SETI.discard(yeni_id)
    return {"ok": True, "gonderi": _sosyal_ile_zenginlestir([gonderi])[0]}


@app.get("/api/kesfet")
def api_kesfet():
    """Ana akış sayfalamasından bağımsız, görsel keşfet görünümü için tüm demo içeriği."""
    return {"gonderiler": _sosyal_ile_zenginlestir(list(GONDERILER))}


@app.get("/api/kullanicilar/{kullanici_id}")
def api_kullanici(kullanici_id: str):
    kullanici = DEPO.kullanici_ozeti(kullanici_id)
    if not kullanici:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
    postlar = [g for g in GONDERILER if g.get("yazar") == kullanici_id]
    return {"kullanici": kullanici, "gonderiler": _sosyal_ile_zenginlestir(postlar)}


@app.post("/api/kullanicilar/{kullanici_id}/takip")
def api_takip_degistir(kullanici_id: str):
    if not DEPO.kullanici(kullanici_id):
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
    takipte = DEPO.takip_degistir("emiryusuf", kullanici_id)
    return {"ok": True, "takipte": takipte, "kullanici": DEPO.kullanici_ozeti(kullanici_id)}


@app.post("/api/gonderiler/{gonderi_id}/roket")
def api_roket_degistir(gonderi_id: int):
    if gonderi_id not in GONDERI_BY_ID:
        raise HTTPException(status_code=404, detail="Gönderi bulunamadı")
    roketlendi = DEPO.roket_degistir("emiryusuf", gonderi_id)
    return {"ok": True, "roketlendi": roketlendi, **DEPO.post_ozellikleri(gonderi_id)}


@app.get("/api/gonderiler/{gonderi_id}/yorumlar")
def api_yorumlar(gonderi_id: int):
    if gonderi_id not in GONDERI_BY_ID:
        raise HTTPException(status_code=404, detail="Gönderi bulunamadı")
    return {"yorumlar": DEPO.yorumlar(gonderi_id)}


@app.post("/api/gonderiler/{gonderi_id}/yorumlar")
def api_yorum_ekle(gonderi_id: int, yorum: YorumYeni):
    metin = yorum.metin.strip()
    if not metin or len(metin) > 400:
        raise HTTPException(status_code=422, detail="Yorum 1-400 karakter olmalı")
    if gonderi_id not in GONDERI_BY_ID:
        raise HTTPException(status_code=404, detail="Gönderi bulunamadı")
    yorum_id = DEPO.yorum_ekle("emiryusuf", gonderi_id, metin)
    return {"ok": True, "yorum_id": yorum_id, "yorumlar": DEPO.yorumlar(gonderi_id), **DEPO.post_ozellikleri(gonderi_id)}


@app.get("/api/etkinlikler")
def api_etkinlikler():
    return {"etkinlikler": DEPO.etkinlikler("emiryusuf")}


@app.get("/api/hikayeler")
def api_hikayeler():
    return {"hikayeler": DEPO.hikayeler()}


@app.post("/api/demo-senaryo")
def api_demo_senaryo():
    """Yarışma demosu için sabit, tekrar üretilebilir yoğun-akış senaryosu."""
    DAVRANIS_GUNLUGU.clear()
    negatifler = sorted((g for g in GONDERILER if g["duygu"] < -0.2), key=lambda g: g["id"])[:8]
    for gonderi in negatifler:
        DAVRANIS_GUNLUGU.append({"gonderi_id": gonderi["id"], "zaman": time.time(), "dwell_saniye": 18.0, "tiklama": True, "roket": False, "yorum": False})
    spiral = spiral_olasiligi(DAVRANIS_GUNLUGU, GONDERILER)
    duygu_durumu = _duygu_durumu()
    return {"ok": True, "spiral_seviyesi": round(spiral, 3), "ornek_sayisi": len(negatifler), "duygu_katmani": duygu_durumu}


@app.post("/api/mudahale/ertele")
def api_mudahale_ertele():
    MUDAHALE_DURUMU["sessize_alindi"] = time.time() + 30 * 60
    return {"ok": True, "sessize_kadar_saniye": 30 * 60}


@app.get("/api/juri-durum")
def api_juri_durum():
    """Tüketici akışından ayrı, teknik inceleme için açıklanabilir durum özeti."""
    return {"duygu_katmani": _duygu_durumu(), "spiral_seviyesi": round(spiral_olasiligi(DAVRANIS_GUNLUGU, GONDERILER), 3), "dogrulama": {"toplam": len(DOGRULAMA_GUNLUGU), "kalibrasyon_guveni": _kalibrasyon_guveni()}, "son_sinyaller": DAVRANIS_GUNLUGU[-10:]}


@app.post("/api/etkilesim")
def api_etkilesim(e: Etkilesim):
    birlesik = _sinyalleri_birlestir(e.gonderi_id, e)
    _bolumu_kapat(e.gonderi_id, e.cikis)

    _gonderi_bazinda_yerine_koy(DAVRANIS_GUNLUGU, e.gonderi_id, {"gonderi_id": e.gonderi_id, "zaman": time.time(), **birlesik})
    del DAVRANIS_GUNLUGU[:-20]  # kayan pencere: son 20 FARKLI gönderi
    ham_spiral = spiral_olasiligi(DAVRANIS_GUNLUGU, GONDERILER)
    spiral = ham_spiral * _guven_carpani(len(DAVRANIS_GUNLUGU))

    gonderi = GONDERI_BY_ID.get(e.gonderi_id)
    duygu = gonderi["duygu"] if gonderi else 0.0
    ozellik = [duygu, birlesik["dwell_saniye"], int(birlesik["tiklama"]),
               int(birlesik["roket"]), int(birlesik["yorum"])]
    SON_HAM_OZELLIK["deger"] = ozellik

    tekil_psikolojik = psikolojik_durum_tahmini(
        duygu=duygu,
        dwell_saniye=birlesik["dwell_saniye"],
        tiklama=birlesik["tiklama"],
        roket=birlesik["roket"],
        yorum=birlesik["yorum"],
        model=_aktif_model(),
    )
    _gonderi_bazinda_yerine_koy(PSIKOLOJIK_GUNLUK, e.gonderi_id, {
        "gonderi_id": e.gonderi_id,
        "saat": datetime.now().hour,
        "konu": gonderi["konu"] if gonderi else "bilinmiyor",
        "ozellik": ozellik,                              # anahtar değişince yeniden hesaplamak için
        "kategori": tekil_psikolojik["kategori"],       # özet istatistikleri için tekil olay
        "olasiliklar": tekil_psikolojik["olasiliklar"],  # oturum ortalaması için
        "agirlik": _katki_agirligi(birlesik),
    })
    psikolojik_oturum = _oturum_ortalamasi(PSIKOLOJIK_GUNLUK)

    SAYAC["son_dogrulamadan_beri"] += 1
    onay_sorulsun_mu = SAYAC["son_dogrulamadan_beri"] >= DOGRULAMA_ARALIGI
    if onay_sorulsun_mu:
        SAYAC["son_dogrulamadan_beri"] = 0

    duygu_durumu = _duygu_durumu()
    return {
        "spiral_seviyesi": round(spiral, 3),
        "psikolojik_durum": psikolojik_oturum,
        "duygu_katmani": duygu_durumu,
        "onay_sorulsun_mu": onay_sorulsun_mu,
    }


@app.post("/api/dogrulama")
def api_dogrulama_ekle(c: DogrulamaCevabi):
    """Kullanıcının kendi bildirdiği anlık durumu, modelin O ANKİ oturum
    tahminiyle karşılaştırıp günlüğe kaydeder. Kullanıcıya soru sorulmadan
    ÖNCE modelin tahmini arayüze hiç gösterilmez -- karşılaştırma taraflı
    olmasın diye."""
    if c.kullanici_cevabi not in KATEGORILER:
        return {"ok": False, "hata": "geçersiz kategori"}
    # Önceden burada TÜM oturumun ortalama baskın kategorisiyle karşılaştırma
    # yapılıyordu -- ama soru "ŞU AN nasıl hissediyorsun" diye soruyor, oturum
    # ortalaması değil. Bu, ortalama genelde "sakin"de sabitlendiği için
    # eşleşme oranını yapay biçimde neredeyse hep sıfıra çekiyordu (kullanıcı
    # tarafından fark edildi, 20.08.2026). Doğrusu: en son etkileşimin TEKİL
    # (o anki) tahminiyle karşılaştırmak.
    if SON_HAM_OZELLIK["deger"] is not None:
        duygu, dwell, tiklama, roket, yorum = SON_HAM_OZELLIK["deger"]
        model_tahmini = psikolojik_durum_tahmini(
            duygu, dwell, bool(tiklama), bool(roket), bool(yorum), model=_aktif_model()
        )["kategori"]
    else:
        model_tahmini = _oturum_ortalamasi(PSIKOLOJIK_GUNLUK)["kategori"]  # henüz etkileşim yoksa yedek
    eslesme = model_tahmini == c.kullanici_cevabi
    DOGRULAMA_GUNLUGU.append({
        "model_tahmini": model_tahmini,
        "kullanici_cevabi": c.kullanici_cevabi,
        "eslesme": eslesme,
    })

    # Kişiselleştirme: kullanıcının onayladığı GERÇEK kategoriyle, en son
    # etkileşimin özelliği üzerinden KISISEL_MODEL'de tek küçük bir adım at.
    # _VARSAYILAN_MODEL bundan hiç etkilenmez.
    if SON_HAM_OZELLIK["deger"] is not None:
        kisisel_guncelle(KISISEL_MODEL, SON_HAM_OZELLIK["deger"], c.kullanici_cevabi)
        KISISEL_GUNCELLEME_SAYISI["deger"] += 1

    return {
        "ok": True,
        "eslesme": eslesme,
        "model_tahmini": model_tahmini,
        "kisisel_guncelleme_sayisi": KISISEL_GUNCELLEME_SAYISI["deger"],
    }


@app.post("/api/kisisel-mod")
def api_kisisel_mod(aktif: bool):
    """Arayüzdeki 'Varsayılan / Kişiselleştirilmiş' anahtarı. Geçmiş oturum
    kayıtlarını SEÇİLEN modelle yeniden skorlayıp güncel ortalamayı döndürür
    -- kullanıcı iki modeli aynı oturumda karşılaştırabilsin diye."""
    KISISEL_MOD["aktif"] = aktif
    model = _aktif_model()
    for kayit in PSIKOLOJIK_GUNLUK:
        if "ozellik" not in kayit:
            continue
        duygu, dwell, tiklama, roket, yorum = kayit["ozellik"]
        yeniden = psikolojik_durum_tahmini(duygu, dwell, bool(tiklama), bool(roket), bool(yorum), model=model)
        kayit["kategori"] = yeniden["kategori"]
        kayit["olasiliklar"] = yeniden["olasiliklar"]
    return {
        "aktif": KISISEL_MOD["aktif"],
        "kisisel_guncelleme_sayisi": KISISEL_GUNCELLEME_SAYISI["deger"],
        "psikolojik_durum": _oturum_ortalamasi(PSIKOLOJIK_GUNLUK),
    }


@app.get("/api/dogrulama-ozet")
def api_dogrulama_ozet():
    toplam = len(DOGRULAMA_GUNLUGU)
    eslesen = sum(1 for k in DOGRULAMA_GUNLUGU if k["eslesme"])
    return {
        "toplam_onay": toplam,
        "eslesen": eslesen,
        "eslesme_orani": round(eslesen / toplam, 3) if toplam else None,
        "son_kayitlar": DOGRULAMA_GUNLUGU[-10:],
        "kisisel_guncelleme_sayisi": KISISEL_GUNCELLEME_SAYISI["deger"],
        "kisisel_mod_aktif": KISISEL_MOD["aktif"],
    }


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
        # Konu x kategori tam ızgarası -- ısı haritası için. Saat x konu değil
        # konu x kategori seçildi: tek oturumluk bir demoda saat neredeyse hep
        # aynı çıkar (kullanıcı tek seferde test ediyor), ama konu zaten 10
        # farklı değer alıyor, bu yüzden zengin/dolu bir ızgara veriyor.
        "konular": sorted({kayit["konu"] for kayit in PSIKOLOJIK_GUNLUK}),
        "konu_kategori_izgara": {
            konu: {kat: konu_kategori.get((konu, kat), 0) for kat in KATEGORILER}
            for konu in {kayit["konu"] for kayit in PSIKOLOJIK_GUNLUK}
        },
    }


@app.get("/api/haftalik-rapor")
def api_haftalik_rapor():
    """LLM ile gerçek oturum verisinden haftalık öz-farkındalık raporu üretir.
    GEMINI_API_KEY tanımlı değilse mevcut:False döner -- arayüz zaten var olan
    statik örnek metne düşer, sahte bir LLM çıktısı asla uydurulmaz."""
    if not haftalik_rapor.mevcut():
        return {"mevcut": False, "sebep": "GEMINI_API_KEY tanımlı değil"}
    psikolojik = api_psikolojik_ozet()
    dogrulama = api_dogrulama_ozet()
    return haftalik_rapor.uret(psikolojik, dogrulama)


@app.get("/api/terapist-raporu")
def api_terapist_raporu():
    """Kullanıcının isterse bir ruh sağlığı uzmanına götürebileceği, YORUMSUZ
    ham davranışsal veri özeti -- /api/haftalik-rapor ile aynı veriyi kullanır,
    farklı (daha nötr, tavsiye vermeyen) bir sistem talimatıyla üretir."""
    if not haftalik_rapor.mevcut():
        return {"mevcut": False, "sebep": "GEMINI_API_KEY tanımlı değil"}
    psikolojik = api_psikolojik_ozet()
    dogrulama = api_dogrulama_ozet()
    return haftalik_rapor.uret(psikolojik, dogrulama, hedef="terapist")


@app.post("/api/sifirla")
def api_sifirla():
    global KISISEL_MODEL
    DAVRANIS_GUNLUGU.clear()
    PSIKOLOJIK_GUNLUK.clear()
    GOSTERILEN_ID_SETI.clear()
    SON_ETKILESIMLER.clear()
    DOGRULAMA_GUNLUGU.clear()
    SAYAC["son_dogrulamadan_beri"] = 0
    KISISEL_MODEL = kisisel_model_olustur()
    KISISEL_MOD["aktif"] = False
    KISISEL_GUNCELLEME_SAYISI["deger"] = 0
    SON_HAM_OZELLIK["deger"] = None
    MUDAHALE_DURUMU["son_gosterim"] = 0.0
    MUDAHALE_DURUMU["sessize_alindi"] = 0.0
    return {"ok": True}


app.mount("/", StaticFiles(directory=BASE_DIR / "static", html=True), name="static")
