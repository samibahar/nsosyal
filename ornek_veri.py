"""
Demo akışı için örnek gönderi havuzu — 10 konu, konu başına 5 gönderi (50 toplam),
karışık duygu tonlarıyla (pozitif/negatif/nötr). Gerçek kullanıcı/olay adı
geçmiyor; tüm metinler betimsel/anonim örnek içerik (CLAUDE.md kuralına uygun).
"""

ORNEK_GONDERILER = [
    # --- spor ---
    {"id": 1, "konu": "spor", "metin": "Takımımız bu hafta harika bir galibiyet aldı, çok sevindim!"},
    {"id": 2, "konu": "spor", "metin": "Antrenman sonrası oyuncular keyifli bir sohbet yaptı."},
    {"id": 3, "konu": "spor", "metin": "Transfer draması yüzünden taraftarlar arasında büyük öfke var."},
    {"id": 4, "konu": "spor", "metin": "Yarın akşamki maçın bilet satışları bugün başladı."},
    {"id": 5, "konu": "spor", "metin": "Sakatlık haberi sonrası taraftarlar endişeli bekleyişte."},

    # --- gundem ---
    {"id": 6, "konu": "gundem", "metin": "Mahkeme, savaş suçlarından idam cezasına mahkum etti."},
    {"id": 7, "konu": "gundem", "metin": "Yeni bir toplantı yarın saat 14.00'te başlayacak."},
    {"id": 8, "konu": "gundem", "metin": "Tutuklama haberi sonrası sosyal medyada büyük kaygı oluştu."},
    {"id": 9, "konu": "gundem", "metin": "Deprem sonrası bölgede büyük yıkım ve can kaybı yaşandı."},
    {"id": 10, "konu": "gundem", "metin": "Yeni düzenleme meclis gündemine alındı."},

    # --- teknoloji ---
    {"id": 11, "konu": "teknoloji", "metin": "Yeni yapay zekâ modeli beklentilerin çok üzerinde başarı gösterdi."},
    {"id": 12, "konu": "teknoloji", "metin": "Şirketin yeni telefonu bugün tanıtıldı."},
    {"id": 13, "konu": "teknoloji", "metin": "Büyük bir veri sızıntısı milyonlarca kullanıcıyı etkiledi."},
    {"id": 14, "konu": "teknoloji", "metin": "Açık kaynak topluluğu yeni bir iş birliğiyle heyecanlandı."},
    {"id": 15, "konu": "teknoloji", "metin": "Sunucu çökmesi nedeniyle uygulama saatlerce erişilemez oldu."},

    # --- bilim ---
    {"id": 16, "konu": "bilim", "metin": "Araştırmacılar yeni bir gezegen keşfetti, bilim dünyası heyecanlı."},
    {"id": 17, "konu": "bilim", "metin": "Aşı çalışmasında umut verici sonuçlar elde edildi."},
    {"id": 18, "konu": "bilim", "metin": "İklim raporunda endişe verici veriler paylaşıldı."},
    {"id": 19, "konu": "bilim", "metin": "Üniversitede yeni bir laboratuvarın açılışı yapıldı."},
    {"id": 20, "konu": "bilim", "metin": "Bilim insanları küresel ısınmanın hızlandığı konusunda uyardı."},

    # --- saglik ---
    {"id": 21, "konu": "saglik", "metin": "Düzenli yürüyüşün ruh sağlığına faydaları bir kez daha kanıtlandı."},
    {"id": 22, "konu": "saglik", "metin": "Hastanelerde yoğun bakım doluluk oranı endişe yaratıyor."},
    {"id": 23, "konu": "saglik", "metin": "Yeni tedavi yöntemi hastalar için umut oldu."},
    {"id": 24, "konu": "saglik", "metin": "Uzmanlar mevsimsel gribe karşı vatandaşları uyardı."},
    {"id": 25, "konu": "saglik", "metin": "Sağlıklı beslenme üzerine yeni bir rehber yayımlandı."},

    # --- ekonomi ---
    {"id": 26, "konu": "ekonomi", "metin": "Piyasalarda bugün sert bir düşüş yaşandı, yatırımcılar endişeli."},
    {"id": 27, "konu": "ekonomi", "metin": "Yeni istihdam verileri beklentilerin üzerinde geldi."},
    {"id": 28, "konu": "ekonomi", "metin": "Enflasyon rakamları açıklandı, tartışmalar sürüyor."},
    {"id": 29, "konu": "ekonomi", "metin": "Küçük işletmelere yönelik yeni bir destek paketi duyuruldu."},
    {"id": 30, "konu": "ekonomi", "metin": "Döviz kurundaki oynaklık esnafı zor durumda bırakıyor."},

    # --- sanat ---
    {"id": 31, "konu": "sanat", "metin": "Yeni sergi büyük beğeni topladı, ziyaretçi sayısı rekor kırdı."},
    {"id": 32, "konu": "sanat", "metin": "Ünlü bir eserin restorasyonu tamamlandı."},
    {"id": 33, "konu": "sanat", "metin": "Festival programı bu yıl daha da genişledi."},
    {"id": 34, "konu": "sanat", "metin": "Bir müzenin bütçe kesintisiyle kapanma riski tartışılıyor."},
    {"id": 35, "konu": "sanat", "metin": "Genç sanatçılar için yeni bir destek programı başladı."},

    # --- egitim ---
    {"id": 36, "konu": "egitim", "metin": "Yeni müfredat tartışmaları öğretmenler arasında endişe yarattı."},
    {"id": 37, "konu": "egitim", "metin": "Bir okulun robotik takımı uluslararası yarışmada derece yaptı."},
    {"id": 38, "konu": "egitim", "metin": "Sınav sonuçları açıklandı, öğrenciler heyecanla bekliyor."},
    {"id": 39, "konu": "egitim", "metin": "Kırsal bölgelerde eğitime erişim hâlâ büyük bir sorun."},
    {"id": 40, "konu": "egitim", "metin": "Üniversiteler için yeni burs programı duyuruldu."},

    # --- oyun ---
    {"id": 41, "konu": "oyun", "metin": "Beklenen oyunun çıkış tarihi nihayet açıklandı, hayranlar çok mutlu."},
    {"id": 42, "konu": "oyun", "metin": "Sunucu sorunları oyuncuları çileden çıkardı."},
    {"id": 43, "konu": "oyun", "metin": "Yeni güncelleme oynanışı baştan sona değiştirdi."},
    {"id": 44, "konu": "oyun", "metin": "E-spor turnuvasında nefes kesen bir final yaşandı."},
    {"id": 45, "konu": "oyun", "metin": "Mikro ödeme tartışmaları oyuncu topluluğunu ikiye böldü."},

    # --- seyahat ---
    {"id": 46, "konu": "seyahat", "metin": "Yeni bir doğrudan uçuş hattı tanıtıldı, seyahatseverler sevindi."},
    {"id": 47, "konu": "seyahat", "metin": "Yoğun sezon nedeniyle otel fiyatları hızla yükseliyor."},
    {"id": 48, "konu": "seyahat", "metin": "Az bilinen bir sahil kasabası bu yaz gözde rotalardan biri oldu."},
    {"id": 49, "konu": "seyahat", "metin": "Uçuş iptalleri yüzünden havalimanında yolcular mağdur oldu."},
    {"id": 50, "konu": "seyahat", "metin": "Doğa yürüyüşü rotalarına yenileri eklendi."},
]

# Örnek kullanıcının ilgi alanı profili (kayıt sırasında seçildiği varsayımıyla)
ORNEK_KULLANICI_ILGI = {
    "spor": 0.9, "oyun": 0.8, "sanat": 0.7, "teknoloji": 0.6, "seyahat": 0.6,
    "saglik": 0.5, "gundem": 0.5, "bilim": 0.4, "ekonomi": 0.4, "egitim": 0.3,
}
