# NSosyal Duygu Katmanı

TEKNOFEST NSosyal İnovasyon Yarışması (2026) için geliştirilen, NSosyal için
duygu-duyarlı, açıklanabilir ve koruyucu bir sıralama/şeffaflık katmanı
prototipi. Detaylı teknik anlatım için `NSosyal_Teknik_Rapor_Guncel.docx`
dosyasına bakınız.

## Gereksinimler

- Python 3.11 veya üzeri (3.13 ile test edildi)
- İnternet bağlantısı (ilk çalıştırmada BERT modelini indirmek için)

## Kurulum

```bash
pip install -r requirements.txt
```

Bu, torch/transformers gibi büyük kütüphaneleri de indirdiği için birkaç
dakika sürebilir (bağlantıya göre ~1-2 GB civarı indirme).

## Çalıştırma

```bash
python -m uvicorn backend.main:app --port 8000
```

Terminalde "Uvicorn running on http://127.0.0.1:8000" yazısını görünce
tarayıcıdan `http://localhost:8000` adresine gidin.

İlk çalıştırmada BERT duygu modeli (savasy/bert-base-turkish-sentiment-cased)
HuggingFace'ten otomatik iner; bu birkaç dakika sürebilir. Sonraki
çalıştırmalarda bu adım atlanır (model bilgisayara önbelleğe alınır).

## Notlar

- **İnce ayarlı (fine-tuned) BERT modeli** boyutu (~420MB) nedeniyle depoya
  dahil edilmemiştir; `ince_ayar.py` ve `ince_ayar_v2.py` ile yeniden
  üretilebilir. Model yoksa kod otomatik olarak orijinal (ince ayarsız)
  modele düşer; çalışmaya devam eder, yalnızca duygu skorları biraz farklı
  çıkabilir (bağımsız testte ince ayarsız model %69,8, ince ayarlı %94,3
  doğruluk — detaylar teknik raporda).
- **Opsiyonel LLM API anahtarı**: haftalık öz-farkındalık raporundaki
  gerçek zamanlı yapay zekâ yorumu ve "uzmana götürmek istersen" özeti,
  bir API anahtarı gerektirir. Anahtar yoksa bu iki bölüm sabit örnek
  metne düşer, uygulamanın geri kalanı normal çalışır. Aktif etmek için
  proje klasöründe `.env` dosyası oluşturup içine `GEMINI_API_KEY=...`
  satırını ekleyin.

## Proje Yapısı (özet)

- `backend/` — FastAPI sunucusu ve REST uç noktaları
- `static/` — mobil-öncelikli frontend (HTML/CSS/JS), cihaz-içi
  kişiselleştirme ajanı (`local-agent.js`)
- `duygu_modeli.py`, `spiral_model.py`, `psikolojik_durum.py` — eğitilmiş
  modeller
- `ince_ayar.py`, `ince_ayar_v2.py` — BERT ince ayar scriptleri
- `dogrulama.py`, `dogrulama_v2.py` — bağımsız model doğrulama scriptleri
- `tests/` — otomatik testler

## Sorun Giderme

- **"ModuleNotFoundError" hatası**: `pip install -r requirements.txt`
  komutunu tekrar çalıştırın.
- **Port 8000 meşgul hatası**: `--port 8001` gibi başka bir numara deneyin.
- **Model indirme çok yavaş/takılıyor**: internet bağlantınızı kontrol
  edin, ~1-2 GB'lık bir indirme var (BERT modeli).
