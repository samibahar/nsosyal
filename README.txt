NSosyal Duygu Katmanı — Kurulum Rehberi
========================================

Bu proje TEKNOFEST NSosyal İnovasyon Yarışması için geliştirilen bir
kanıt-of-konsept. Ne olduğunu/nasıl çalıştığını anlatan iki PDF de bu
klasörde: NSosyal_Teknik_Ozet.pdf ve NSosyal_Rapor_Icerigi.pdf.


1) GEREKSİNİMLER
-----------------
- Python 3.11 veya üzeri (3.13 ile test edildi)
- İnternet bağlantısı (ilk çalıştırmada BERT modelini indirmek için)


2) KURULUM
----------
Klasörü açtıktan sonra bir terminalde şunu çalıştır:

    pip install -r requirements.txt

NOT: Bu, torch/transformers gibi büyük kütüphaneleri de indirdiği için
birkaç dakika sürebilir (bağlantına göre ~1-2 GB civarı indirme).


3) ÇALIŞTIRMA
-------------
Kurulum bitince, proje klasöründeyken:

    python -m uvicorn backend.main:app --port 8000

Terminalde "Uvicorn running on http://127.0.0.1:8000" yazısını görünce
tarayıcıdan şu adrese git:

    http://localhost:8000

İLK ÇALIŞTIRMADA: BERT duygu modeli (savasy/bert-base-turkish-sentiment-cased)
HuggingFace'ten otomatik inecek -- bu birkaç dakika sürebilir, terminalde
indirme çubuğunu göreceksin. Sonraki çalıştırmalarda bu adım atlanır
(model bilgisayarına önbelleğe alınır).


4) GÖRECEĞİN ŞEY, BENİM GÖRDÜĞÜMDEN NEDEN BİRAZ FARKLI OLABİLİR
-----------------------------------------------------------------
İki şey bilerek bu pakete DAHİL EDİLMEDİ:

  a) İnce ayarlı (fine-tuned) BERT modeli -- 420MB olduğu için pakete
     koymadım. Kod bunu otomatik fark edip orijinal (ince ayarsız)
     modele düşüyor -- ÇÖKMEZ, çalışır, ama duygu skorları biraz farklı
     çıkabilir (bağımsız testte ince ayarsız model %69.8, ince ayarlı
     %94.3 doğruluk -- detay NSosyal_Teknik_Ozet.pdf'te).

  b) Benim kişisel Gemini API anahtarım (.env dosyası) -- güvenlik
     nedeniyle paylaşılmadı. Bunsuz da her şey çalışır, sadece "Bu
     haftanın gerçek yapay zekâ yorumu" ve "Bir uzmana götürmek
     istersen" bölümleri (rapor.html'de) görünmez, sabit örnek metne
     düşer. İstersen kendi (ücretsiz) anahtarınla bunu da aktif
     edebilirsin -- adımlar aşağıda.


5) (OPSİYONEL) GEMİNİ API ANAHTARI EKLEME
-------------------------------------------
Canlı yapay zekâ rapor özelliğini görmek istersen:

  1. https://aistudio.google.com/apikey adresine git, Google hesabınla
     giriş yap (kredi kartı istemiyor, ücretsiz katman var)
  2. "Create API key" ile bir anahtar oluştur ("Default Gemini Project"
     seçeneği yeterli)
  3. Proje klasöründe ".env" adında yeni bir dosya oluştur, içine tek
     satır yaz:

     GEMINI_API_KEY=buraya_kendi_anahtarin

  4. Sunucuyu yeniden başlat (Ctrl+C ile durdur, adım 3'teki komutu
     tekrar çalıştır)


6) SORUN YAŞARSAN
------------------
- "ModuleNotFoundError" hatası: adım 2'deki pip install komutunu tekrar
  çalıştır, terminali kapatıp yeniden açmış olabilirsin.
- Port 8000 meşgul hatası: --port 8000 yerine --port 8001 gibi başka bir
  numara dene, sonra http://localhost:8001 adresine git.
- Model indirme çok yavaş/takılıyor: internet bağlantını kontrol et,
  ~1-2 GB'lık bir indirme var (BERT modeli).
