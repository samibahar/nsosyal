"""
Hızlı fizibilite denemesi (spike) — gerçek BERT modeli yerine hafif, sözlük-tabanlı
bir duygu skorlayıcı ile TÜM MİMARİYİ uçtan uca çalıştırıyoruz. Amaç: skor motoru +
refah katmanı + açıklanabilirlik mantığının GERÇEKTEN çalıştığını kanıtlamak.
Gerçek sürümde bu lexicon yerine savasy/bert-base-turkish-sentiment-cased kullanılacak
(normal internet erişimi olan bir geliştirme ortamında test edilmeli).
"""
import time

t0 = time.time()

# 1) Basit Türkçe duygu sözlüğü (gerçek sürümde BERT modeliyle değişecek kısım)
NEGATIVE_WORDS = {"kötü", "üzücü", "kaygı", "kaygılı", "korkunç", "öfke", "öfkelendirdi",
                   "idam", "suç", "tutuklama", "savaş", "ölüm", "dayanamıyorum", "üzdü", "endişe"}
POSITIVE_WORDS = {"harika", "mutlu", "güzel", "sevindim", "başarı", "tebrik", "keyifli", "huzur"}

def duygu_skoru(metin: str) -> float:
    """-1 (çok negatif) ile +1 (çok pozitif) arasında kaba bir skor döndürür."""
    kelimeler = metin.lower().replace(",", " ").replace(".", " ").replace("!", " ").split()
    neg = sum(1 for k in kelimeler if k in NEGATIVE_WORDS)
    pos = sum(1 for k in kelimeler if k in POSITIVE_WORDS)
    toplam = neg + pos
    if toplam == 0:
        return 0.0
    return (pos - neg) / toplam

# 2) Örnek içerik havuzu (konu etiketiyle)
gonderiler = [
    {"id": 1, "konu": "spor", "metin": "Takımımız bu hafta harika bir galibiyet aldı, çok sevindim!"},
    {"id": 2, "konu": "spor", "metin": "Transfer draması yüzünden taraftarlar arasında büyük öfke var."},
    {"id": 3, "konu": "gundem", "metin": "Mahkeme, savaş suçlarından idam cezasına mahkum etti."},
    {"id": 4, "konu": "gundem", "metin": "Yeni bir toplantı yarın saat 14.00'te başlayacak."},
    {"id": 5, "konu": "spor", "metin": "Antrenman sonrası oyuncular keyifli bir sohbet yaptı."},
    {"id": 6, "konu": "gundem", "metin": "Tutuklama haberi sonrası sosyal medyada büyük kaygı oluştu."},
]

for g in gonderiler:
    g["duygu"] = duygu_skoru(g["metin"])

# 3) Kullanıcının ilgi alanı (kayıt sırasında seçtiği varsayımıyla) + simüle davranış günlüğü
kullanici_ilgi = {"spor": 0.9, "gundem": 0.5}

# Simüle edilmiş son 5 dakikalık davranış: art arda negatif içerikte uzun dwell-time + hızlı geçişler
davranis_gunlugu = [
    {"gonderi_id": 3, "dwell_saniye": 9.2, "tiklama": False},
    {"gonderi_id": 6, "dwell_saniye": 7.8, "tiklama": False},
    {"gonderi_id": 3, "dwell_saniye": 5.1, "tiklama": False},  # tekrar aynı türde içerikte takılma
]

def spiral_skoru(log):
    """Basit ama gerçek bir kural-tabanlı sınıflandırıcı: negatif içerikte uzun/tekrarlı
    dwell-time -> spiral olasılığı. Gerçek sürümde bu bir lojistik regresyon olacak,
    burada mantığı kanıtlamak için kural tabanlı bir başlangıç kullanıyoruz."""
    neg_dwell_toplam = 0.0
    for kayit in log:
        g = next(x for x in gonderiler if x["id"] == kayit["gonderi_id"])
        if g["duygu"] < -0.2:
            neg_dwell_toplam += kayit["dwell_saniye"]
    # 15 saniyeden fazla negatif içerikte kalma -> spiral sinyali
    return min(1.0, neg_dwell_toplam / 15.0)

spiral = spiral_skoru(davranis_gunlugu)

# 4) İki katmanlı, açıklanabilir skor motoru
def sirala(gonderiler, ilgi, spiral_seviyesi):
    sonuc = []
    for g in gonderiler:
        ilgi_skoru = ilgi.get(g["konu"], 0.3)
        # Refah katmanı: spiral yüksekse, negatif duygulu içerik cezalandırılır (ama TAMAMEN elenmez)
        refah_cezasi = spiral_seviyesi * max(0, -g["duygu"]) * 0.8
        final_skor = ilgi_skoru - refah_cezasi
        sonuc.append({
            **g,
            "ilgi_skoru": round(ilgi_skoru, 2),
            "refah_cezasi": round(refah_cezasi, 2),
            "final_skor": round(final_skor, 2),
            "aciklama": (f"İlgi alanınla eşleşiyor ({g['konu']}, skor {ilgi_skoru})"
                         + (f", ama şu an olası bir spiral tespit ettiğimiz için "
                            f"{round(refah_cezasi,2)} puan yumuşattık" if refah_cezasi > 0 else ""))
        })
    return sorted(sonuc, key=lambda x: -x["final_skor"])

siralanmis = sirala(gonderiler, kullanici_ilgi, spiral)

print(f"Kurulum + çalıştırma süresi: {round(time.time()-t0, 4)} saniye (dış model indirme yok)\n")
print(f"Tespit edilen spiral seviyesi: {spiral}  (0=yok, 1=yüksek)\n")
print("Sıralanmış akış (yüksekten düşüğe):")
for s in siralanmis:
    print(f"  #{s['id']} [{s['konu']}] duygu={s['duygu']:+.2f} final_skor={s['final_skor']:+.2f}")
    print(f"      -> {s['aciklama']}")
    print(f"      -> gönderi: \"{s['metin']}\"")
