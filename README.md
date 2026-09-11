# NSosyal Duygu Katmanı

TEKNOFEST NSosyal İnovasyon Yarışması (2026) için geliştirilen, NSosyal için
duygu-duyarlı, açıklanabilir ve koruyucu bir sıralama/şeffaflık katmanı
prototipi. Detaylı teknik anlatım için `NSosyal_Teknik_Rapor_Guncel.docx`
dosyasına bakınız.

## Gereksinimler

- Python 3.11 veya üzeri (3.13 ile test edildi)
- [Git LFS](https://git-lfs.com) (ince ayarlı duygu modelini indirmek için)
- İnternet bağlantısı (kurulumda kütüphaneleri indirmek için)

## Kurulum

```bash
git lfs install
git clone https://github.com/samibahar/nsosyal.git
cd nsosyal
pip install -r requirements.txt
```

İnce ayarlı duygu modeli (`models/bert-turkish-sentiment-ince-ayarli-v3/`,
~440 MB) Git LFS ile depodadır. Klonlamadan önce `git lfs install`
çalıştırılmadıysa veya depo ZIP olarak indirildiyse `model.safetensors`
birkaç yüz baytlık bir işaretçi dosya olabilir. Bu durumda depo klasöründe
`git lfs pull` çalıştırın. Model bulunamazsa kod otomatik olarak HuggingFace
Hub'daki orijinal (ince ayarsız) modele düşer ve çalışmaya devam eder; yalnızca
duygu skorları farklı çıkar.

## Çalıştırma

```bash
python -m uvicorn backend.main:app --port 8000
```

Terminalde "Uvicorn running on http://127.0.0.1:8000" yazısını görünce
tarayıcıdan `http://localhost:8000` adresine gidin. İlk açılışta duygu modeli
belleğe yüklendiği için sunucunun hazır olması yarım dakika kadar sürebilir.

Sayfalar: ana akış (`/`), Haberler, İçgörü (`/rapor.html`), Ayarlar
(`/ayarlar.html`) ve jüri için karar kanıtı (`/juri.html`). Ana akıştaki
"Jüri demosu" düğmesi hazır bir örnek senaryoyu cihaz içinde çalıştırır.

## Nasıl çalışır (özet)

- **Ham davranış cihazda kalır.** Hangi gönderiye ne kadar bakıldığı
  tarayıcının IndexedDB alanında tutulur; sunucuya gönderilmez. Sunucu sayfa
  başına 48 aday gönderi verir, telefon bunları kendi profiline göre sıralayıp
  12'sini gösterir.
- **Açık rıza:** İlk açılışta ne tutulduğu ve nerede saklandığı anlatılır;
  kullanıcı duygu katmanını açık veya kapalı başlatmayı seçer.
- **Duygu dengeleme (doz):** Kullanıcı yoğun tonlu içerikte, kendi okuma
  hızına göre belirgin biçimde uzun ve pasif kalıyorsa, yoğun tonlu içeriklerin
  sayfadaki payı akış yoğunluğuyla orantılı olarak azaltılır (en fazla %60) ve
  bu gönderiler art arda gelmek yerine aralıklanır; kartta "dengelendi"
  etiketi görünür. Hiçbir içerik silinmez; Ayarlar'dan tek dokunuşla
  kapatılabilir. Resmi/acil bilgilendirme hesaplarının gönderileri
  (`resmi_veri.py`) dengelemeden muaftır. Ölçüm: `etki_analizi_sonuc.txt`.
- **Açıklanabilirlik:** Her gönderideki "Neden bu?" düğmesi sıralamanın
  bileşenlerini gösterir.
- **Doğrulama:** Ara sıra sorulan "Şu an nasıl hissediyorsun?" sorusunun
  cevapları, model tahmini ve iki taban çizgisiyle (rastgele, "hep en sık
  cevap") karşılaştırılıp İçgörü ekranında gösterilir.

## Modeller

| Model | Dosya | Ne yapar |
|---|---|---|
| Duygu (BERT, 3 sınıf) | `duygu_modeli.py`, `ince_ayar_v3.py` | Gönderi metninin tonu: P(pozitif) − P(negatif) |
| Spiral v2 | `spiral_model.py`, `spiral_ozellik.py` | Son 30 dakikadaki davranıştan yoğun içerikte oyalanma riski |
| Psikolojik durum | `psikolojik_durum.py` | Tek etkileşim için 5 kategorili olası örüntü; cihazda kişisel uyarlama |

**Duygu modeli.** `savasy/bert-base-turkish-sentiment-cased` temel alınarak
`winvoker/turkish-sentiment-analysis-dataset` ve bu proje için yazılmış haber
üslubu verisiyle üç aşamada ince ayar yapıldı. Bağımsız test örneklerinde
(winvoker split=train, 1000 örnek; eğitim verisiyle ayrık):

| Sürüm | İkili doğruluk | Not |
|---|---|---|
| Orijinal model | %69,8 | Alan kayması |
| v1 | %94,3 | Genel Türkçe ince ayar |
| v2 | %93,3 | Haber üslubunda zayıflık düzeltildi |
| **v3** | **%94,0** | Nötr sınıfı eklendi; 3 sınıf doğruluk %95,7 |

v2 ikili bir sınıflandırıcı olduğu için gönderilerin %94'ünde |ton| > 0,9
çıkıyordu; v3'te nötr metinlerin tonu sıfıra yakın (ortalama |ton| 0,005).
Ayrıntılar: `dogrulama_v3_sonuc.txt`, `v3_arama_sonuc.txt`.

**Spiral modeli v2.** Özellikler okuma süresine göre normalize edilir;
asıl sinyal yoğun tonlu içerikte kullanıcının kendi hızına göre ne kadar
fazla kaldığı (göreli oyalanma), aktif katılım (yorum, roket) ise riski
azaltır. İşaret kısıtlı lojistik regresyon: katsayıların yönü hipotezle
sabit, büyüklüğü veriden öğrenilir. Gerçek kullanıcı verisi olmadığından
davranış düzeyinde bir simülatörle eğitildi; gerçek kullanıcı onaylarıyla
yeniden eğitilmesi gerekir. Ayrıntılar: `spiral_v2_sonuc.txt`.

## Test ve yeniden üretim

```bash
python -m pytest -q
```

Tarayıcı (uçtan uca) testleri Playwright ile çalışır ve açık bir sunucuya
bağlanır; sunucu kapalıysa atlanır. Bir kez kurulum:
`pip install playwright` ve `python -m playwright install chromium`.
Sunucu çalışırken:

```bash
python -m pytest tests/e2e -q
```

Ölçüm betikleri (çıktıları depodaki `*_sonuc.txt` dosyalarıdır):

```bash
python dogrulama_v3.py
```

```bash
python spiral_model.py
```

```bash
python etki_analizi.py
```

```bash
python olcek_olcumu.py
```

`disa_aktar_modeller.py` eğitilmiş spiral ve psikolojik durum modellerini
tarayıcıda çalışan `static/trained-weights.js` dosyasına yazar.
`ince_ayar_v3.py` duygu modelini yeniden eğitir (GPU önerilir);
`ince_ayar_v3_arama.py` hiperparametre aramasını yapar.

## Notlar

- **Lisans ve atıf:** Temel duygu modeli `savasy/bert-base-turkish-sentiment-cased`
  (HuggingFace), eğitim verisi `winvoker/turkish-sentiment-analysis-dataset`.
  Temel modelin sayfasında lisans belirtilmemiştir; ince ayarlı model yalnızca
  araştırma ve yarışma amaçlıdır.
- **Üçüncü taraf servis yok:** Arayüz hiçbir davranış verisini dış bir yapay
  zekâ servisine göndermez. Duygu modeli sunucuda yerel olarak çalışır ve
  yalnızca herkese açık gönderi metnini skorlar; İçgörü'deki "uzmana
  götürülebilir özet" tarayıcıda, dil modeli kullanılmadan üretilir.
  `backend/main.py`'deki `/api/haftalik-rapor` ve `/api/terapist-raporu` uç
  noktaları eski sunucu tarafı mimariden kalmadır ve arayüz tarafından
  çağrılmaz.

## Proje Yapısı (özet)

- `backend/` — FastAPI sunucusu ve REST uç noktaları
- `static/` — mobil-öncelikli frontend (HTML/CSS/JS), cihaz-içi
  kişiselleştirme ajanı (`local-agent.js`), tarayıcıda çalışan modeller
  (`trained-models.js`)
- `models/` — ince ayarlı duygu modeli (Git LFS)
- `duygu_modeli.py`, `spiral_model.py`, `spiral_ozellik.py`,
  `psikolojik_durum.py` — modeller
- `ince_ayar*.py`, `dogrulama*.py` — ince ayar ve bağımsız doğrulama
- `tests/` — otomatik testler

## Sorun Giderme

- **"ModuleNotFoundError" hatası**: `pip install -r requirements.txt`
  komutunu tekrar çalıştırın.
- **Port 8000 meşgul hatası**: `--port 8001` gibi başka bir numara deneyin.
- **Duygu skorları beklenenden farklı**: ince ayarlı model LFS işaretçisi
  olarak inmiş olabilir (`models/.../model.safetensors` birkaç yüz bayt). Kod bu
  durumda orijinal modele düşer; gerçek modeli almak için `git lfs pull`
  çalıştırın.
