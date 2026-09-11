"""
Spiral özellikleri: sunucu (motor.py), eğitim (spiral_model.py) ve tarayıcı
(static/trained-models.js) AYNI tanımı kullanır. Sabitler disa_aktar_modeller.py
ile trained-weights.js'e yazılır; JS tarafı bu dosyanın satır satır karşılığıdır.
Değiştirilirse ikisi birlikte değiştirilmeli (parite: tests/test_spiral_model.py
ve tarayıcıdaki karşılaştırma).

Bir olay: {"gonderi", "zaman" (sn), "dwell" (sn), "ton" (-1..1), "kelime",
"konu", "roket", "yorum"}.

Özellikler (hepsi son 30 dakikadaki gönderilerden, yakın olan daha ağır):
  yogun_pay          Dikkatin ne kadarı yoğun tonlu içerikteydi. Durma süresi
                     metnin okuma süresine bölünür; uzun metin okumak "uzun
                     kalmak" sayılmaz.
  goreli_oyalanma    Yoğun tonlu gönderilerde, diğerlerine GÖRE ne kadar uzun
                     kalındı (log oran). Akışta kaç yoğun gönderi olduğundan
                     bağımsızdır: her şeyi yavaş okuyan kullanıcıda 0'a yakındır.
                     Akışın tamamı yoğunsa okuma süresiyle kıyaslanır.
  yogun_fazla_kalma  Yoğun tonlu gönderilerde okuma süresinin ÜSTÜNDE kalma
                     (oyalanma). Hızlıca göz atmak burada sıfırdır.
  aktif_oran         Roket/yorum gibi aktif katılımın payı.

İlk denemede "ortalama_ton" da vardı; akışın bileşimini (kullanıcının
seçmediği bir şeyi) ölçtüğü için ters yönde (+) katsayı aldı ve hep olumlu
içerik okuyan kullanıcıyı riskli saydı. Çıkarıldı. "yogun_seri" ve
"konu_yogunlasma" katsayıları sıfıra yakın çıktığı için çıkarıldı.
"""
import math
PENCERE_SANIYE = 30 * 60
YARI_OMUR_SANIYE = 10 * 60
MAKS_GONDERI = 20
MIN_GONDERI = 3
YOGUN_TON = -0.2
OKUMA_TABAN = 1.5        # sn: göz gezdirme payı
KELIME_HIZI = 3.5        # kelime/sn (~210 kelime/dk)
VARSAYILAN_KELIME = 12   # kelime sayısı bilinmeyen eski kayıtlar için
ORAN_UST = 4.0
FAZLA_UST = 3.0
GORELI_PAY = 0.1         # log oranda sıfıra bölmeyi önleyen pay
GORELI_UST = 2.0

OZELLIK_ADLARI = ["yogun_pay", "goreli_oyalanma", "yogun_fazla_kalma", "aktif_oran"]

PARAMETRELER = {
    "pencere_saniye": PENCERE_SANIYE, "yari_omur_saniye": YARI_OMUR_SANIYE,
    "maks_gonderi": MAKS_GONDERI, "min_gonderi": MIN_GONDERI, "yogun_ton": YOGUN_TON,
    "okuma_taban": OKUMA_TABAN, "kelime_hizi": KELIME_HIZI, "varsayilan_kelime": VARSAYILAN_KELIME,
    "oran_ust": ORAN_UST, "fazla_ust": FAZLA_UST, "goreli_pay": GORELI_PAY, "goreli_ust": GORELI_UST,
}


def beklenen_okuma(kelime) -> float:
    return OKUMA_TABAN + max(1, kelime or VARSAYILAN_KELIME) / KELIME_HIZI


def birlestir(olaylar: list[dict], simdi: float) -> list[dict]:
    """Penceredeki olayları gönderi başına tek kayda indirger (en uzun durma,
    eylemlerin VEYA'sı, en son zaman) ve zamana göre sıralı son MAKS_GONDERI
    gönderiyi döndürür. Aynı gönderiye dönüp bakmak ayrı gönderi sayılmaz."""
    kayitlar: dict = {}
    for olay in olaylar:
        if simdi - olay["zaman"] > PENCERE_SANIYE or olay["dwell"] <= 0:
            continue
        onceki = kayitlar.get(olay["gonderi"])
        if onceki is None:
            kayitlar[olay["gonderi"]] = dict(olay)
        else:
            onceki["dwell"] = max(onceki["dwell"], olay["dwell"])
            onceki["roket"] = bool(onceki["roket"] or olay["roket"])
            onceki["yorum"] = bool(onceki["yorum"] or olay["yorum"])
            onceki["zaman"] = max(onceki["zaman"], olay["zaman"])
    return sorted(kayitlar.values(), key=lambda kayit: kayit["zaman"])[-MAKS_GONDERI:]


def ozellikler(olaylar: list[dict], simdi: float) -> dict | None:
    """Yeterli güncel gönderi yoksa None döner (risk hesaplanmaz)."""
    gunluk = birlestir(olaylar, simdi)
    if len(gunluk) < MIN_GONDERI:
        return None
    agirlik_top = oran_top = aktif_top = 0.0
    yogun_oran = yogun_agirlik = fazla_top = 0.0
    for kayit in gunluk:
        agirlik = 0.5 ** ((simdi - kayit["zaman"]) / YARI_OMUR_SANIYE)
        oran = min(kayit["dwell"] / beklenen_okuma(kayit.get("kelime")), ORAN_UST)
        agirlik_top += agirlik
        oran_top += agirlik * oran
        aktif_top += agirlik * (1.0 if (kayit["roket"] or kayit["yorum"]) else 0.0)
        if kayit["ton"] < YOGUN_TON:
            yogun_oran += agirlik * oran
            yogun_agirlik += agirlik
            fazla_top += agirlik * min(max(0.0, oran - 1.0), FAZLA_UST)
    diger_agirlik = agirlik_top - yogun_agirlik
    goreli = 0.0
    if yogun_agirlik > 0:
        yogun_ort = yogun_oran / yogun_agirlik
        # Kıyaslanacak yoğun olmayan gönderi yoksa (akışın tamamı yoğun: kriz
        # günü) referans, metni okuma süresi kadar bakmaktır (oran 1).
        diger_ort = (oran_top - yogun_oran) / diger_agirlik if diger_agirlik > 1e-9 else 1.0
        goreli = max(-GORELI_UST, min(GORELI_UST, math.log((yogun_ort + GORELI_PAY) / (diger_ort + GORELI_PAY))))
    return {
        "yogun_pay": yogun_oran / oran_top if oran_top > 0 else 0.0,
        "goreli_oyalanma": goreli,
        "yogun_fazla_kalma": fazla_top / yogun_agirlik if yogun_agirlik > 0 else 0.0,
        "aktif_oran": aktif_top / agirlik_top,
    }
