# NSosyal Duygu Katmanı

TEKNOFEST NSosyal İnovasyon Yarışması (2026, Sosyal Yapay Zekâ) için geliştirilen,
NSosyal akışına eklenmesi önerilen açılıp kapatılabilir bir sıralama katmanı.
Kullanıcı yoğun tonlu içerikte, kendi okuma hızına göre uzun ve pasif kaldığında
sıradaki sayfada bu içeriklerin payını azaltır ve aralıklar; hiçbir gönderiyi
silmez, her kararı "Neden bu?" ile açıklar. Ham davranış kaydı cihazdan çıkmaz.

**Durum:** çalışan bağımsız prototip (tasarım, kodlama ve 85 otomatik test
tamam). NSosyal API erişimi ve canlı entegrasyon yok; gönüllü kullanıcı testi
henüz yapılmadı.

**Belgeler:** final sunumu `sunum/` klasöründe; teknik rapor
`NSosyal_Teknik_Rapor_Guncel.docx`; model kartı, ölçümler ve bilimsel dayanak
`docs/` klasöründe (`model_karti.md`, `bilimsel_dayanak.md`,
`olcum_sinirlari.md`, `final_yaklasim_ve_is_modeli.md`, `pilot_protokolu.md`).

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

Sunucu açıkken tek komutla kontrol (sayfalar, yüklü duygu modeli, aday
listesi, demo paketi, sıkıştırma):

```bash
python demo_kontrol.py
```

## Jüri için 5 dakikalık tur

1. Ana akışı açın; ilk açılışta duygu katmanının ne tuttuğunu anlatan
   bilgilendirmede "Açık başlat"ı seçin.
2. Sağ üstteki (mobilde üstteki) **Jüri demosu** düğmesine basın: hazır örnek
   sinyaller cihazda işlenir, akış yeniden sıralanır, dengelenen kartlarda
   "dengelendi" etiketi ve üstte "Akış biraz yoğunlaştı" bildirimi görünür.
3. Dengelenen bir kartta **Neden bu?** → gönderinin kaç sıra aşağı alındığı ve
   yoğun içerik payı hedefi (ör. %33 → %20).
4. **Ayarlar** → "Duygu dengeleme"yi kapatıp demoyu tekrar çalıştırın: yoğun
   gönderiler aşağı alınmaz. Uzun dönem özeti ve cihazda saklanan veriler de
   buradadır.
5. `/juri.html` → son demonun karar kanıtı (önce/sonra sıra, gerekçe).
6. Ölçümler ve belgeler: `docs/model_karti.md`, `docs/erisilebilirlik.md`,
   `docs/kullanici_akislari.md`, `*_sonuc.txt` dosyaları; testler
   `python -m pytest -q`.

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
| Olay sözcüğü desteği | `yogun_sozluk.py` | Elle yazılmış açık olay sözcükleri (ölüm, yangın, saldırı…); eşleşen metnin tonunu en fazla −0,9'a çeker. Öğrenen model değil, kural |
| Ruh hali (psikolojik durum) | `psikolojik_durum.py` | Son 30 dakikadaki etkileşimlerden 5 kategorili olası ruh hali; cihazda kişisel uyarlama |

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

**Olay sözcüğü desteği.** Model duygunun ifadesini okur, olayın ağırlığını değil: "3 işçi hayatını kaybetti" gibi olgusal haber başlıklarını yoğun saymıyordu. 200 gerçek haber başlığında güçlü olumsuzu yakalama yalnız modelle %12, olay sözcüğüyle birlikte %82; saldırgan tweetlerde ise işi model yapıyor (model %82, yalnız sözlük %7). Etiketli 37.249 gerçek metinde birleşik karar doğruluğu %83, AUC 0,89. Ayrıntılar: `docs/model_karti.md`.

**Spiral modeli v2.** Özellikler okuma süresine göre normalize edilir;
asıl sinyal yoğun tonlu içerikte kullanıcının kendi hızına göre ne kadar
fazla kaldığı (göreli oyalanma), aktif katılım (yorum, roket) ise riski
azaltır. Dengeleme kararı = 0,7 × spiral olasılığı + 0,3 × ruh hali modelinin sinirli ve yoğun payı. İşaret kısıtlı lojistik regresyon: katsayıların yönü hipotezle
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
  Sunucu davranış verisi (durma süresi, tıklama, kontrol cevabı) kabul eden
  hiçbir uç nokta sunmaz: eski sunucu tarafı öğrenme uç noktaları
  (`/api/etkilesim`, `/api/dogrulama`, haftalık rapor vb.) varsayılan olarak
  kapalıdır ve yalnızca karşılaştırma amacıyla `NSOSYAL_ESKI_SUNUCU_YOLU=1`
  ortam değişkeniyle açılır. Bu, tarayıcı testiyle ve `demo_kontrol.py` ile
  doğrulanır.

## Proje Yapısı (özet)

- `backend/` — FastAPI sunucusu ve REST uç noktaları
- `static/` — mobil-öncelikli frontend (HTML/CSS/JS), cihaz-içi
  kişiselleştirme ajanı (`local-agent.js`), tarayıcıda çalışan modeller
  (`trained-models.js`)
- `models/` — ince ayarlı duygu modeli (Git LFS)
- `duygu_modeli.py`, `spiral_model.py`, `spiral_ozellik.py`,
  `psikolojik_durum.py` — modeller
- `ince_ayar*.py`, `dogrulama*.py` — ince ayar ve bağımsız doğrulama
- `yogun_sozluk.py` — olay sözcüğü desteği
- `sunum/` — final sunumu
- `docs/` — model kartı, ölçüm sınırları, bilimsel dayanak, pilot protokolü
- `tests/` — otomatik testler

## Sorun Giderme

- **"ModuleNotFoundError" hatası**: `pip install -r requirements.txt`
  komutunu tekrar çalıştırın.
- **Port 8000 meşgul hatası**: `--port 8001` gibi başka bir numara deneyin.
- **Duygu skorları beklenenden farklı**: ince ayarlı model LFS işaretçisi
  olarak inmiş olabilir (`models/.../model.safetensors` birkaç yüz bayt). Kod bu
  durumda orijinal modele düşer; gerçek modeli almak için `git lfs pull`
  çalıştırın.
