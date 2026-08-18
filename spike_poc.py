"""
Uçtan uca demo — artık sözlük-tabanlı sahte bileşenler değil, GERÇEK bileşenler
kullanıyor: duygu_modeli.py (savasy/bert-base-turkish-sentiment-cased) ve
spiral_model.py (senaryo-bazlı sentetik veriyle eğitilmiş sınıflandırıcı, F1≈0.75).
Mimari mantığı ilk spike ile birebir aynı; tek fark artık gerçek modellerden
besleniyor olması. Motor mantığının kendisi motor.py'de, burada sadece demo akışı var.
"""
import time

from motor import gonderileri_puanla, sirala, spiral_olasiligi

t0 = time.time()

# 1) Örnek içerik havuzu (konu etiketiyle)
gonderiler = [
    {"id": 1, "konu": "spor", "metin": "Takımımız bu hafta harika bir galibiyet aldı, çok sevindim!"},
    {"id": 2, "konu": "spor", "metin": "Transfer draması yüzünden taraftarlar arasında büyük öfke var."},
    {"id": 3, "konu": "gundem", "metin": "Mahkeme, savaş suçlarından idam cezasına mahkum etti."},
    {"id": 4, "konu": "gundem", "metin": "Yeni bir toplantı yarın saat 14.00'te başlayacak."},
    {"id": 5, "konu": "spor", "metin": "Antrenman sonrası oyuncular keyifli bir sohbet yaptı."},
    {"id": 6, "konu": "gundem", "metin": "Tutuklama haberi sonrası sosyal medyada büyük kaygı oluştu."},
]
gonderileri_puanla(gonderiler)  # duygu skorlarını gerçek BERT modeliyle doldurur

# 2) Kullanıcının ilgi alanı + simüle davranış günlüğü
kullanici_ilgi = {"spor": 0.9, "gundem": 0.5}

# Simüle edilmiş son 5 dakikalık davranış: art arda negatif içerikte uzun dwell-time
davranis_gunlugu = [
    {"gonderi_id": 3, "dwell_saniye": 9.2, "tiklama": False},
    {"gonderi_id": 6, "dwell_saniye": 7.8, "tiklama": False},
    {"gonderi_id": 3, "dwell_saniye": 5.1, "tiklama": False},  # tekrar aynı türde içerikte takılma
]

spiral = spiral_olasiligi(davranis_gunlugu, gonderiler)  # eğitilmiş lojistik regresyondan

# 3) İki katmanlı, açıklanabilir skor motoru (motor.py'den, mantık değişmedi)
siralanmis = sirala(gonderiler, kullanici_ilgi, spiral)

print(f"Kurulum + çalıştırma süresi: {round(time.time()-t0, 4)} saniye (BERT modeli belleğe yüklendi)\n")
print(f"Tespit edilen spiral olasılığı: {spiral:.3f}  (0=yok, 1=yüksek)\n")
print("Sıralanmış akış (yüksekten düşüğe):")
for s in siralanmis:
    print(f"  #{s['id']} [{s['konu']}] duygu={s['duygu']:+.2f} final_skor={s['final_skor']:+.2f}")
    print(f"      -> {s['aciklama']}")
    print(f"      -> gönderi: \"{s['metin']}\"")
