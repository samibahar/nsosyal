"""
İki katmanlı, açıklanabilir sıralama motoru — spike_poc.py'nin mimarisini
gerçek bileşenlerle (duygu_modeli.py: BERT, spiral_model.py: eğitilmiş
sınıflandırıcı) birleştiren üretim modülü. FastAPI backend'i bunu kullanır.
"""
import time

import spiral_model
import spiral_ozellik
from duygu_modeli import duygu_skoru
from yogun_sozluk import sistem_tonu

# Spiral sınıflandırıcı, süreç başlarken bir kere eğitilir ve bellekte tutulur
# (gerçek üretimde bu, önceden eğitilip diske kaydedilmiş bir model dosyası olurdu).
spiral_model.egitilmis()


def gonderileri_puanla(gonderiler: list[dict]) -> list[dict]:
    """Her gönderiye BERT ile gerçek bir duygu_skoru ekler (yoksa)."""
    for g in gonderiler:
        if "duygu" not in g:
            # Model tonu saklanır; açık olumsuz olay sözcüğü varsa (yogun_sozluk.py)
            # uygulamanın kullandığı ton en fazla −0,9 olur ve sözcük açıklamada gösterilir.
            g["duygu_model"] = duygu_skoru(g["metin"])
            g["duygu"], g["yogun_sozcuk"] = sistem_tonu(g["duygu_model"], g["metin"])
    return gonderiler


def _olaylara_cevir(log: list[dict], gonderiler: list[dict], simdi: float) -> list[dict]:
    """Sunucudaki davranış günlüğünü (gonderi_id, dwell_saniye, tiklama, roket,
    yorum, zaman) spiral_ozellik.py'nin olay biçimine çevirir."""
    id_to_gonderi = {g["id"]: g for g in gonderiler}
    olaylar = []
    for kayit in log:
        gonderi = id_to_gonderi.get(kayit["gonderi_id"])
        if not gonderi:
            continue
        olaylar.append({
            "gonderi": kayit["gonderi_id"], "zaman": kayit.get("zaman", simdi), "dwell": kayit["dwell_saniye"],
            "ton": gonderi["duygu"], "kelime": len(gonderi.get("metin", "").split()), "konu": gonderi.get("konu"),
            "roket": bool(kayit.get("roket")), "yorum": bool(kayit.get("yorum")),
        })
    return olaylar


def spiral_olasiligi(log: list[dict], gonderiler: list[dict]) -> float:
    """Eğitilmiş sınıflandırıcıdan 0-1 arası spiral olasılığı döndürür.
    Son 30 dakikada yeterli gönderi yoksa 0 döner (boş günlük ceza üretmez)."""
    simdi = time.time()
    ozellik = spiral_ozellik.ozellikler(_olaylara_cevir(log, gonderiler, simdi), simdi)
    return spiral_model.olasilik(ozellik)


def sirala(gonderiler: list[dict], ilgi: dict, spiral_seviyesi: float) -> list[dict]:
    """spike_poc.py'deki iki katmanlı skor motoru — davranış değişmedi, girdiler
    artık gerçek modellerden geliyor."""
    sonuc = []
    for g in gonderiler:
        ilgi_skoru = ilgi.get(g["konu"], 0.3)
        refah_cezasi = spiral_seviyesi * max(0, -g["duygu"]) * 0.8
        final_skor = ilgi_skoru - refah_cezasi
        sonuc.append({
            **g,
            "ilgi_skoru": round(ilgi_skoru, 2),
            "refah_cezasi": round(refah_cezasi, 2),
            "final_skor": round(final_skor, 2),
            "aciklama": (f"İlgi alanınla eşleşiyor ({g['konu']}, skor {ilgi_skoru})"
                         + (f", ama şu an olası bir spiral tespit ettiğimiz için "
                            f"{round(refah_cezasi,2)} puan yumuşattık" if refah_cezasi > 0 else "")),
        })
    return sorted(sonuc, key=lambda x: -x["final_skor"])
