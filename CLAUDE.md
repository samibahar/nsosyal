# Proje Bağlamı — NSosyal İnovasyon Yarışması (TEKNOFEST)

Bu dosya, Claude Code'un bu projeye başlarken hiçbir şeyi baştan sormasına gerek kalmadan
tüm bağlamı okuması için hazırlandı. Cowork'te (bulut ortamı) uzun bir araştırma/planlama
sürecinden geçtik — burada varılan tüm kararlar özetleniyor. Lütfen bu kararları
sorgulamadan kabul et, aksini gerektiren yeni bir bilgi çıkmadıkça.

## Yarışma ve Teslim

- Yarışma: NSosyal İnovasyon Yarışması (TEKNOFEST, düzenleyen: 2N Medya + T3 Vakfı).
- Resmi şartname okundu: `2026_NSOSYAL_YARISMASI_SARTNAMESI_TR_2026_07_24_v9_1.pdf` (V3, 17.08.2026).
- Son başvuru tarihi: **20 Ağustos 2026** (şartnamede sadece tarih var, saat belirtilmemiş).
  **GÜNCEL DURUM (19.08.2026 gece):** başvuru/takım kaydı gerçekten TAMAMLANDI —
  kullanıcı "Ön Başvuru Formu"nu (Proje Başlığı: "NSosyal Duygu Katmanı", takım adı:
  "Duygu Katmanı") doldurup gönderdi ve az önce "başvuru bitti" diye onayladı. (Not: bu
  konuda bir kere karışıklık yaşandı — kullanıcı daha önce "yaptım" sanıp aslında
  göndermemişti, o yanlış kaydı düzeltmiştik; bu sefer gerçekten tamamlandı, artık risk
  yok.)
- Teknik Rapor teslimi: **24 Ağustos 2026, saat 17.00 (TSİ)** — KYS üzerinden. Şablona uygun
  olmayan/eksik/geç yüklenen raporlar değerlendirmeye alınmaz, takım elenir.
- Ardından: 2 Eylül sonuç ilanı, 2-7 Eylül mentörlük süreci, 14 Eylül final sunum teslimi,
  20 Eylül canlı sunum, 30 Eylül-4 Ekim TEKNOFEST Şanlıurfa.
- Şartnamenin genel kapsam metni "çalışan bir prototip ile desteklemeli" diyor — 24 Ağustos
  raporu için net bir gate kriteri olarak yazılmamış ama final aşamasında canlı demo açıkça
  isteniyor. Yine de olabildiğince güçlü bir kanıt-of-konsept hedefle, "zorunlu değil" diye
  gevşek davranma.
- Format: rapor en fazla 30 sayfa (kapak/içindekiler/kaynakça dahil), Arial 12pt, Arial Black
  14pt başlık, 1.15 satır aralığı, 2.5cm kenar boşluğu.
- **Puanlama (GÜNCEL — 19.08.2026 gece resmi rapor şablonundan, eski %35/%0 rakamları
  ARTIK GEÇERSİZ, bkz. altındaki not):** Sosyal Yapay Zekâ teması için Teknik Yeterlilik
  ve Uygulanabilirlik %30, Yenilikçilik ve Özgünlük %20, Problemi Çözme Başarısı %20,
  Sunum ve Prototip Kalitesi %15, Kullanıcı Deneyimi (UI/UX) %10, İş Modeli ve
  Sürdürülebilirlik **%5** (eskiden %0'dı, şablonda "yeşil vurgulu hücreler: orijinal
  şartnamede %0 olan, bu düzeltmede asgari %5'e çekilen alanlar" notuyla düzeltilmiş —
  yani bu bölümü artık TAMAMEN atlama, kısa da olsa gerçek içerik olsun).
## Resmi Rapor Şablonu (19.08.2026 gece, kullanıcının Downloads'tan paylaştığı .docx'ten)

Dosya: `NSosyal_Inovasyon_2026_-_Proje_Teknik_Raporu_1_u6IVb (1).docx`. Bu, önceki
şartname özetinden DAHA GÜNCEL ve DAHA DETAYLI — rapor yazarken bunu esas al.

**Zorunlu başlık sırası (Word "Heading 1" stili, aynen kullan):**
1. İÇİNDEKİLER (ayrı sayfa)
2. PROJE ÖZETİ — 1.1. Proje Konusu ve amacı (0-7p) / 1.2. Proje Kapsamı ve Yöntemi (0-8p)
3. KATMA DEĞER VE YENİLİKÇİLİK — 2.1. Problem Tanımı ve Mevcut Çözümler (0-7p) /
   2.2. Çözüm Fikri, Özgünlük ve Yerlilik (0-8p)
4. TEKNOLOJİ KULLANIMI — 3.1. İzlenecek Yöntem, altyapı ve Sürüm Kontrolü (0-7p) /
   3.2. Model ve Veri Doğrulama (0-6p) / 3.3. Kullanıcı Deneyimi (UI/UX) Tasarımı (0-7p)
5. UYGULANABİLİRLİK — 4.1. Verimlilik ve Etkinlik (0-5p) / 4.2. Hedef Kitle (0-5p) /
   4.3. Teknolojik Yenilik ve Uygulanabilirlik (0-5p)
6. YAYGIN ETKİ — 5.1. Toplumsal Fayda ve Erişim Potansiyeli (0-10p)
7. SÜRDÜRÜLEBİLİRLİK — 6.1. Ticarileştirme Potansiyeli ve İş Modeli (0-5p) /
   6.2. Finansal, Teknik ve Sosyal Sürdürülebilirlik (0-5p)
8. PROJE TAKVİMİ — 7.1. İş Paketleri ve Zamanlama (0-5p, görsel tablo/şema iste,
   24 Ağu/2-7 Eyl/14 Eyl tarihleriyle çelişmesin)
9. TAKIM YAPISI — 8.1. Takım Organizasyonu ve Roller (0-5p, TABLOLAŞTIR — ama İSİM/FOTOĞRAF
   gibi kişisel bilgi KESİNLİKLE KONMAYACAK, değerlendirme kuralı bunu yasaklıyor)
10. KAYNAKÇA (ayrı sayfa, 0-5p, köşeli parantez atıf [1], [4,7,21], [5-11]; web kaynak:
    "Soyad, Adın Baş Harfi., Başlık, Tarih, Erişim Tarihi, Erişim adresi"; akademik:
    "Soyad, Adın Baş Harfi., (Yıl) Başlık, (varsa) Dergi, Sayı, Sayfa, DOI")

Alt madde toplamı tam 100 puan (7+8+7+8+7+6+7+5+5+5+10+5+5+5+5+5=100), her alt madde
kendi içinde kontrol-maddesi bazlı kısmi puanlanıyor (şablonun "PUANLAMA VE DEĞERLENDİRME
ESASLARI" sayfasındaki 16 tabloda tek tek yazılı — bu sayfa RAPORA KONMAYACAK, sadece bizim
neyin puanlandığını bilmemiz için).

**Kritik, gözden kaçmaması gereken puanlı maddeler:**
- 3.1'de **GitHub/Bitbucket repo bağlantısı paylaşılmış** (0-1p) ve **commit geçmişiyle
  takip edilebilir geliştirme** (0-1p) AYRI AYRI puanlanıyor — yani rapor GitHub linki
  istiyor. Kullanıcı daha önce (19.08.2026 gece) zip+README ile paylaşmayı tercih edip
  GitHub'ı reddetmişti ("ikisini de istemem") -- ama o zaman bu puanlı madde bilinmiyordu,
  YENİDEN SORULMALI.
- 3.2 not: "Projede yapay zeka/veri bileşeni yoksa bu alt kriter değerlendirme dışı
  bırakılır" -- bizim projede güçlü bir YZ bileşeni var, bu madde tam uygulanır, atlanamaz.
- 8.1: takım 2-5 kişi olmalı, kişisel bilgi (isim/fotoğraf) YASAK.

**Format kuralları (raporun kendisinde bu sayfa/not YOK, sadece uyulacak):**
- En fazla 30 sayfa (kapak+içindekiler+kaynakça+ekler dahil), kapak/içindekiler/kaynakça
  için 3 AYRI sayfa ayrılmalı.
- Arial 12pt gövde, Arial Black 14pt başlık, 1.15 satır aralığı, iki yana yaslı,
  2.5cm kenar boşluğu (üst-alt-sağ-sol).
- Cümleler birbirinin tekrarı olmamalı.
- Bu aşamada demo videosu İSTENMİYOR (final sunumuna ait).
- KYS üzerinden 24 Ağustos 2026 17.00 TSİ'ye kadar; şablona uymayan/eksik/geç = değerlendirme
  dışı.

**Beklenen teslimatlar (tüm yarışma boyunca, sadece 24 Ağustos değil):** teknik rapor,
sunum dosyası, kullanıcı senaryoları, çalışan prototip, kaynak kod, proje/demo videosu,
iş modeli ve gelir modeli dokümanı, yapay zekâ mimarisi dokümanı, veri/model/etik/performans
dokümanı, UI/UX tasarımları, kullanıcı akışları, kullanıcı araştırması özeti, kullanılabilirlik
testi sonuçları, erişilebilirlik değerlendirmesi.

## Ürün Konsepti (Kesinleşti)

**Tema:** Sosyal Yapay Zekâ (birincil), Kullanıcı Katılımı/UX ve İçerik Ekonomisi'ne de organik dokunuyor.

NSosyal (gerçek bir platform — T3 Vakfı + Baykar Teknoloji yapımı, Twitter/X tarzı bir
mikroblog, Reels değil) için duygu-duyarlı, açıklanabilir ve koruyucu bir katman:

1. **İki katmanlı, açıklanabilir sıralama motoru:** İlgi/alaka skoru (kullanıcının ilgi
   alanları) + refah skoru (negatif spiral tespit edilince aynı ilgi alanı İÇİNDE kalarak
   daha az tetikleyici içeriğe kayma). Kara kutu bir sinir ağı DEĞİL — her karar
   açıklanabilir olmalı (şeffaflık iddiamızın temeli).
2. **Şeffaflık paneli:** Kullanıcıya "neden bunu görüyorsun" açıklamasını gerçek zamanlı
   gösteren arayüz.
3. **Öz-farkındalık raporu:** Önce **haftalık** bir örnek olarak gösterilecek (aylık değil —
   raporda "aylık versiyon aynı mantığın zaman penceresi genişletilmiş hâli" diye açıklanacak,
   yeni mühendislik gerekmiyor). Teşhis/klinik aracı DEĞİL, kişisel öz-farkındalık/gözlem
   notu olarak çerçevelenmeli — aşırı iddialı dilden kaçın ("kesin duygu okuyoruz" değil,
   "olası örüntü").
4. **Üretici paneli:** İçerik üreticisine kendi içeriğinin neden öne çıkıp çıkmadığını ve
   erişim/kazanç etkisini gösteren şeffaflık.
5. **Koruyucu ekonomi/reklam katmanı:** Kırılgan duygu durumunda manipülatif/dürtüsel
   reklamlar bastırılır, yerine destekleyici içerik sunulur (NSosyal şu an reklamsız,
   bu ileriye dönük bir tasarım ilkesi olarak sunuluyor).
6. **Kendi kendini doğrulayan aktif öğrenme döngüsü:** Pasif tahminin ara sıra, hafif
   dokunuşlu bir onay sorusuyla ("şu an kaygılı mı hissediyorsun?") doğrulanması — hem
   bilimsel dürüstlük hem gerçek performans metrikleri (F1, doğruluk) için.

## Bilinçli Reddedilen Yaklaşımlar (TEKRAR ÖNERME)

- **"Kaygılı hissedenlerin izlediğini göster" (cohort-bazlı öneri):** REDDEDİLDİ. Facebook'un
  kendi iç araştırmasında "öfke = en yüksek etkileşim" bulgusuyla aynı tuzağa düşürme riski
  taşıyor — anxious kullanıcılara "diğer anxious kullanıcıların izlediğini" göstermek,
  doomscroll döngüsünü pekiştirebilir.
- **Reklamı duygu durumuna göre HEDEFLEMEK:** REDDEDİLDİ. 2017'de sızan bir Facebook
  belgesi, "worthless/insecure" hisseden gençleri reklam hedeflemesi için kullanmayı
  önermişti, büyük skandal oldu. Biz TAM TERSİNİ yapıyoruz: kırılgan durumda reklamı
  bastırıyoruz, hedeflemiyoruz.
- **İçerik kategorisine (siyasi/dini vb.) göre filtreleme:** REDDEDİLDİ. Sistem KONU-NÖTR
  olmalı — sadece duygusal yoğunluğa bakıyoruz, konuya değil. "Dini/siyasi içeriği azalt"
  gibi bir çerçeve hem etik açıdan yanlış hem de bu platform (yerli/milli konumlandırılmış)
  için stratejik olarak çok riskli.
- **T3 AI'a gerçek/API erişimi olduğu iddiası:** YANLIŞ. Gerçek erişimimiz YOK. Kanıt-of-
  konsept tamamen bağımsız çalışıyor, raporda "önerilen entegrasyon konsepti" olarak
  sunulacak — sahte bir gerçek entegrasyon iddiası kurulmamalı.

## NSosyal Hakkında Doğrulanmış Bulgular

- Gerçek platform, ~700 bin+ aktif kullanıcı (Ocak 2026 itibarıyla).
- Giriş sonrası arayüz birebir Twitter/X yapısında: Ana Sayfa/Bildirimler/Mesajlar/Keşfet/
  Topluluklar/Kaydedilenler/Beğeniler, sağda "Popüler" trend paneli.
- Trend mekanizması zayıf/kolay doldurulabiliyor (örn. 2 günde 60 gönderilik bir etiket ilk
  5'e girebiliyor).
- Ana akış kişiselleştirilmiş mi belirsiz — kayıt sırasında ilgi alanı soruluyor ama bu HENÜZ
  TEST EDİLMEDİ, varsayımla ilerlenmemeli (birden fazla test hesabıyla doğrulanmalı).
- T3 AI zaten var (otomatik yanıt, çok dilli yorumlama, filtreleme/moderasyon) — bizim
  duygu-analizi motorumuz bunun "önerilen bir uzantısı" olarak konumlandırılıyor.
- Trend içeriği ağır/duygusal yoğunluklu haber materyali (siyasi, gündem) içerebiliyor —
  bunu raporda betimsel/anonim biçimde kullan, gerçek kişilerin görsellerini/isimlerini
  doğrudan rapora koyma.

## Teknik Yaklaşım ve Kullanılacak Araçlar

- **Duygu analizi:** `savasy/bert-base-turkish-sentiment-cased` (hazır Türkçe model) veya
  `dbmdz/bert-base-turkish-cased` (fine-tuning için taban), fine-tuning verisi için
  `winvoker/turkish-sentiment-analysis-dataset` (hepsi HuggingFace'te).
- **Dwell-time takibi:** Tarayıcının standart `Intersection Observer API`'si.
- **Backend:** Python, FastAPI ya da Flask.
- **Spiral sınıflandırıcı:** scikit-learn (lojistik regresyon/gradient boosting) — küçük,
  sentetik/senaryo-bazlı veriyle eğitilebilir.
- **Rapor metni üretimi:** Bir LLM API'si (Claude API gibi) ile prompt tabanlı üretim.
- **Sürüm kontrolü:** Bu klasör bir git reposu olarak başlatılmalı, düzenli/anlamlı
  commit'lerle ilerlenmeli (rapor kontrol listesi bunu ayrı ayrı puanlıyor).

## Şu Ana Kadar Yapılanlar

- `spike_poc.py` — Cowork'teki bulut ortamında (HuggingFace'e ağ erişimi kısıtlıydı, 403)
  gerçek modeli indiremediğimiz için sözlük-tabanlı basit bir duygu skorlayıcıyla,
  mimarinin TAMAMINI (skor motoru + refah katmanı + spiral tespiti + açıklanabilirlik)
  uçtan uca test ettik. **Çalıştı ve doğru sonuç üretti** — spiral doğru tespit edildi,
  negatif içerik elenmeden aşağı kaydırıldı, her gönderi için okunabilir bir açıklama
  üretildi. Bu dosyayı incele, mantığı understand et, sonra gerçek BERT modeliyle
  değiştirmeye başla (burada normal internet erişimi olduğu için bu artık mümkün olmalı).

## Bağımsız Model Doğrulaması (19.08.2026)

`dogrulama.py` ile `savasy/bert-base-turkish-sentiment-cased` modeli, kendi kart
iddiasına (%95.4 doğruluk) güvenmek yerine BAĞIMSIZ bir veri setinde
(winvoker/turkish-sentiment-analysis-dataset, 1000 rastgele örnek) test edildi.
X/Twitter'dan canlı veri çekmek ToS ihlali + altyapı riski taşıdığı için
(X'in öneri algoritmasını kendi kullanıcı grafiğimiz olmadan yeniden üretmek
mümkün değil), bunun yerine hazır/lisanslı bu veri seti kullanıldı.

**Bulgu:** Bağımsız doğruluk %69.8, F1 0.778 (ikili karşılaştırmaya giren 630
örnekte) — modelin kendi iddiasının belirgin altında. Model "negatif" dediğinde
sık yanılıyor (precision 0.37) ama gerçek negatifleri kaçırmıyor (recall 0.93) —
yani gerçekte POZİTİF olan metinleri sıklıkla negatif sınıflandırıyor. Muhtemel
sebep: alan kayması (domain shift) — model muhtemelen dar bir alanda (ürün/film
yorumu) fine-tune edilmiş, test verimiz haber/sosyal medya karışımı. Ayrıca
1000 örneğin 370'i "Nötr" etiketli — modelin nötr sınıfı yok, bu örneklerin
hepsi zorla pozitif/negatif tarafa yuvarlanıyor (bilinen bir sınırlılık).

**Raporda nasıl kullanılacak:** Bunu saklamak yerine METODOLOJİK DÜRÜSTLÜK
kanıtı olarak sun — "vendor iddiasını sorgulamadan kabul etmedik, bağımsız
doğrulama yaptık, bir sınırlılık keşfettik ve dürüstçe raporladık". Hem %95.4
(vendor) hem %69.8 (bağımsız, bizim ölçümümüz) rakamını birlikte ver, aradaki
farkı alan kayması ile açıkla.

## Çok Kategorili Psikolojik Durum Katmanı (19.08.2026)

Kullanıcı isteği üzerine, ikili "spiral var/yok" tespitinin yanına, her etkileşim
anı için 5 kategorili bir "olası psikolojik izlenim" katmanı eklendi:
**sakin, mutluluk, umut, korku, anksiyete**. `psikolojik_durum.py` — spiral_model.py
ile AYNI yöntemle (açıklanabilir, sentetik senaryo verisiyle eğitilmiş lojistik
regresyon), 5 sinyalden (BERT duygu skoru, dwell-time, tıklama, roket, yorum)
tahmin üretiyor. F1 makro ≈0.78.

**Neden hazır bir "duygu kategorisi" BERT modeli kullanılmadı:** Araştırıldı
(`maymuni/bert-base-turkish-cased-emotion-analysis` vb.) — hepsi belgesiz eğitim
verisi ve doğrulanmamış/şüpheli doğruluk iddiaları taşıyor (savasy modelinde
yaşanan güven kırılmasından hemen sonra). Ayrıca kara kutu bir model, projenin
"her karar açıklanabilir olmalı" temel tezine aykırı olurdu.

**Kritik sınırlılık (raporda mutlaka belirtilmeli):** Bu kategoriler klinik bir
duygu okuması DEĞİL — sadece davranışsal sinyallerden (durma süresi, tıklama,
roket, yorum) türetilmiş olası bir örüntü etiketi. "korku" ve "anksiyete" gibi
yakın psikolojik durumları salt etkileşim verisinden kesin ayırt etmenin bilimsel
bir sınırı var. Aşırı iddialı dilden kaçınılmalı ("tespit ettik" değil "olası").

**X'ten veri çekme fikri reddedildi:** ToS ihlali riski + X'in öneri algoritmasını
kendi altyapımız olmadan yeniden üretemeyeceğimiz gerekçesiyle. Bkz. yukarıdaki
"Bağımsız Model Doğrulaması" bölümü — onun yerine hazır/lisanslı veri seti kullanıldı.

**Backend/arayüz:** `/api/etkilesim` artık `roket`/`yorum` alanlarını da alıyor,
her etkileşimde anlık kategori tahminini dönüyor (arayüzde canlı rozet olarak
gösteriliyor). `/api/psikolojik-ozet`, bu OTURUMDA gerçekten kaydedilen
etkileşimlerden (sabit örnek metin değil) konu/saat bazlı gerçek bir özet
üretiyor — `rapor.html`'de "Bu oturumda gerçekten gözlemlenen" bölümü olarak
canlı gösteriliyor.

## Duygu Analizi Optimizasyonu + Kendi Kendini Doğrulama (19.08.2026, gece)

Kullanıcı sordu: "BERT fine-tuning arka planda çalışıyor ama o sadece gönderi
METNİNİ yorumluyor — barları dolduran davranış→psikoloji eşlemesini neye
dayandıracağız?" Çok haklı bir soru, üç parçalı cevap uygulandı:

1. **Aktif öğrenme / kendi kendini doğrulama döngüsü (kodlandı):** Kullanıcıya
   her ~8 etkileşimde bir hafif bir onay sorusu çıkıyor ("şu an gerçekte nasıl
   hissediyorsun?" — mutluluk/umut/sakin/korku/anksiyete, "Geç" seçeneği de
   var). Cevap, modelin O ANKİ tahminiyle karşılaştırılıp `/api/dogrulama`
   ile kaydediliyor; taraflılık olmasın diye model tahmini kullanıcıya ÖNCE
   gösterilmiyor. `/api/dogrulama-ozet` eşleşme oranını döndürüyor,
   `rapor.html`'de "Model doğrulama" bölümü olarak şeffafça gösteriliyor.
   Bu, CLAUDE.md'nin başındaki orijinal üründe zaten planlanmış ama hiç
   kodlanmamış "Kendi kendini doğrulayan aktif öğrenme döngüsü" maddesinin
   ilk gerçek uygulaması.
2. **Literatüre gevşek dayandırma:** `psikolojik_durum.py`'nin docstring'i
   güncellendi — sentetik senaryoların tasarımının rastgele olmadığı,
   genel kabul gören dijital davranış kavramlarıyla (edilgen tüketim ~
   rumination, aktif katılım ~ olumlu duygulanım, tekrarlı kontrol ~
   huzursuzluk) kabaca uyumlu olduğu belirtildi. Bu KESİN akademik kaynak
   iddiası DEĞİL — "rastgele uydurma değil" seviyesinde bir gerekçe.
3. **Kapsamı dürüstçe küçültme:** Arayüz metinleri (ruh-hali-paneli başlığı,
   rapor.html footer'ı) "doğrulanmış tespit sistemi" değil "önerilen yöntem +
   sürekli doğrulama mekanizması" olarak güncellendi.

**Raporda kullanılacak çerçeve:** "Modelimiz mükemmel değil, bunu biliyoruz ve
saklamıyoruz — bu yüzden hem bağımsız veri setiyle doğruluk ölçtük (duygu
modeli) hem de kullanıcı onayıyla sürekli kendini sınayan bir mekanizma
kurduk (psikolojik kategori modeli)." Bu, ham doğruluk iddiasından çok daha
güçlü bir "teknik yeterlilik" argümanı.

## Duygu Analizi Optimizasyonu — BERT Fine-Tuning (19.08.2026)

`ince_ayar.py`: savasy modeli, winvoker veri setinin **split="test"** bölümünden
(dogrulama.py'nin kullandığı split="train" 1000 örneğiyle ÇAKIŞMIYOR, veri
sızıntısı yok) dengeli ~15.000 örnekle (7500 pozitif + 7500 negatif) 2 epoch
devam ederek ince ayar yapılıyor. Amaç: dogrulama.py'de bulunan alan kayması
sorununu (gerçek doğruluk %69.8, modelin negatif tahmin yanlılığı) azaltmak.

CPU'da (GPU yok) eğitim tahmin edilenden çok daha yavaş çıktı: ~5.1sn/adım,
1480 adım toplam → gerçek süre 2 saat 6 dakika sürdü (ilk tahmin 45-90 dk
yanlıştı). Fine-tuned model `models/bert-turkish-sentiment-ince-ayarli/`
klasörüne kaydedildi; `duygu_modeli.py` artık bu klasörü önce dener, yoksa
HF Hub'daki orijinal modele düşer (kod değişikliği gerekmeden çalışır).

**SONUÇ (19.08.2026, ~gece yarısı) — AYNI 1000 örneklik bağımsız test
setinde (dogrulama.py, split="train", fine-tuning'in kullandığı split="test"
ile tamamen ayrık, veri sızıntısı yok):**

| | Doğruluk | F1 | negatif precision |
|---|---|---|---|
| Önce (orijinal savasy) | %69.8 | 0.778 | 0.372 |
| Sonra (ince ayarlı)    | **%94.3** | **0.964** | **0.803** |

24.5 puanlık gerçek, bağımsız ölçülmüş bir iyileşme. En büyük düzelme:
model artık "negatif" dediğinde çoğunlukla haklı (önceden pozitif metni
sık sık yanlışlıkla negatif sanıyordu). Yan not/sınırlılık: nötr etiketli
örneklerin pozitife yuvarlanma oranı arttı (%52 → %91) -- model hâlâ ikili,
nötr sınıfı yok, ve şimdi belirsiz/nötr metni daha güçlü biçimde pozitife
okuyor gibi görünüyor; raporda bu dürüstçe belirtilmeli.

**Raporda kullanılacak çerçeve:** "Vendor'ın iddiasını (%95.4) sorgulamadan
kabul etmek yerine bağımsız ölçtük, gerçek zayıflık bulduk (%69.8), bunu
hedefli bir fine-tuning ile ölçülebilir biçimde düzelttik (%94.3), ve
sürecin her adımını (veri sızıntısı koruması dahil) şeffafça belgeledik."
Bu, tek başına "%95 doğruluk" demekten çok daha güçlü bir teknik yeterlilik
anlatısı.

**EK BULGU / KISA ALARM (aynı gece, hemen sonrasında test edildi):** İnce
ayarlı modeli `ornek_veri.py`'deki 150 demo gönderisinde (kısa, resmi,
üçüncü-şahıs "haber bülteni" tarzı cümleler -- winvoker'ın daha çok birinci
şahıs/günlük-dil ağırlıklı tarzından farklı bir alt-tür) test ederken, ilk
8 örneklik hızlı testte ince ayarlı model şaşırtıcı biçimde KÖTÜ çıktı
(idam/tutuklama gibi net negatif haberleri pozitif sanıyordu). 20 örneğe
genişletilince endişe geçti: **orijinal ve ince ayarlı model bu ÖZEL alt-türde
eşit performans gösteriyor (%65 = %65)** -- yani fine-tuning bizim demo
içeriğimizde ne iyileştirme ne kötüleştirme yaptı, GENEL Türkçe metinde
(bağımsız 1000 örnek) ise büyük iyileştirme yaptı (%69.8→%94.3).

**Karar:** İnce ayarlı modeli kullanmaya devam (duygu_modeli.py zaten
otomatik seçiyor) -- genel performansı kesin olarak daha iyi, kendi demo
tarzımızda da geriletmiyor. **Raporda dürüstçe belirtilmesi gereken ek
sınırlılık:** kısa/resmi/dolaylı-duygu-ifadeli Türkçe cümleler (örn. "X
tepki topladı" gibi çıkarımsal duygu, doğrudan "harika/kötü" gibi açık
duygu kelimesi yok) HER İKİ modelin de zorlandığı bir alt-tür (%65
civarı) -- bu, modelin genel bir sınırlılığı, fine-tuning ile çözülmedi.

## Literatür Taraması (19.08.2026, gece)

`literatur_bulgulari.md` — gerçek kaynaklarla (uydurma yok) bir tarama
yapıldı. En önemli bulgu: bizim "kendi kendini doğrulama döngümüz" aslında
psikolojideki **EMA (Ecological Momentary Assessment)** yönteminin bağımsız
bir yeniden keşfi — bu literatürle isimlendirilip raporda güçlendirilebilir.
Diğer bulgular: pasif dwell-time/olumsuz duygu ilişkisi literatürde ORTA
güçte (abartma), davranıştan duygu çıkarımı meşru ama kişiye-özgü kalibrasyon
olmadan sınırlı (bilinen sınırlılık olarak yaz), refah-farkında sıralama
konseptimizin akademik emsali var (CWB-RS, arXiv:2102.04211), şeffaflık
panelinde "az ama net" ilkesi literatürce destekleniyor. Detaylar ve tam
atıflar dosyada.

## Kişiselleştirme (Online Learning) Mekanizması (19.08.2026, gece)

Kullanıcının fikri: "3.yi (aktif öğrenme) yaparsak, katsayılarla küçük adımlarla
oynayarak uzun vadede oto-optimizasyon yapmış olmaz mıyız?" — evet, bu gerçek
bir ML kavramı (online/incremental learning, SGD). Uygulandı:

- `psikolojik_durum.py`: model artık `SGDClassifier(loss="log_loss")` —
  `partial_fit` destekli. `_VARSAYILAN_MODEL` hiç değişmez, `KISISEL_MODEL`
  her doğrulama cevabından sonra küçük bir adımla güncellenir.
- **Demo sorunu ve çözümü:** gerçek kişiselleştirmeyi (çok kullanıcı, uzun
  vade) tek bir demo oturumunda gösteremeyiz. Kullanıcının önerisi: bir
  anahtarla ("Varsayılan" / "Kişiselleştirilmiş") aynı oturum içinde iki
  modeli karşılaştırılabilir hale getirdik — `/api/kisisel-mod` geçmişi
  seçilen modelle yeniden skorluyor.
- **Dürüstlük notu (raporda mutlaka belirt):** `KISISEL_ETA0` (öğrenme oranı)
  demo'da mekanizmanın birkaç onayda görünür olması için KASITLI olarak
  büyütüldü. Gerçek üretimde (binlerce kullanıcı, aylarca veri) çok daha
  küçük olurdu. Bu "gerçek kişiselleştirme kalibrasyonu" iddiası değil,
  mekanizmanın kanıt-of-konseptidir.
- **İstikrar riski (kullanıcı da fark etti, doğru):** az veriyle/düzenlileştirme
  olmadan online güncelleme modeli yanlış yöne kaydırabilir. Şu anki tasarımda
  koruma: küçük adım boyu (tek gürültülü cevap ≈ etkisiz) + varsayılan model
  hiç dokunulmadan referans olarak kalıyor (istenirse anahtar her an "Varsayılan"a
  dönüp güvenli tarafa geçilebilir). Gerçek üründe düzenlileştirme/sınır
  (clipping) eklenmeli -- rapor bunu "gelecek iş" olarak not etmeli.

## Renk Doygunluğu Azaltma + Gerçek LLM Haftalık Rapor (19.08.2026, gece)

Spiral seviyesine bağlı renk doygunluğu azaltma eklendi (`app.js`/`index.html`/
`style.css`): `spiral_seviyesi` arttıkça akışın CSS `saturate()` filtresi
kademeli azalıyor (seviye 0.7'de %69 doygunluk gibi), kullanıcı isteğiyle bir
açma/kapama tuşu da eklendi. Ayrı bir ağırlıklı formül icat etmek yerine zaten
eğitilmiş tek bileşik sinyali (spiral_seviyesi) tekrar kullanmak tercih edildi
— tutarlılık için.

**Gerçek LLM destekli haftalık rapor** (`haftalik_rapor.py`) eklendi —
sabit örnek metnin yanına, bu oturumda gerçekten kaydedilen veriye bakarak
anlık üretilen bir versiyon. **Sağlayıcı: Anthropic/Claude DEĞİL, Google
Gemini** (`gemini-2.5-flash`, `google-genai` kütüphanesi) — kullanıcı bütçe
kısıtı nedeniyle sordu, Gemini'nin kart istemeyen gerçek bir ücretsiz katmanı
olduğu için ona geçildi (Claude API tamamen kullanım-bazlı ücretli, ücretsiz
kota yok). Mantık/prompt/sistem talimatı sağlayıcıdan bağımsız tasarlandı —
`uret()` fonksiyonunu değiştirmek başka bir sağlayıcıya geçmek için yeterli.
`GEMINI_API_KEY` ortam değişkeni `.env`'de yoksa `mevcut()` False döner,
arayüz zaten var olan statik örnek rapora düşer — sahte bir LLM çıktısı asla
uydurulmaz.

**Uçtan uca canlı test edildi (19.08.2026, gece) — çalışıyor.** İki küçük
sorun çözüldü: (1) `gemini-2.5-flash` artık yeni kullanıcılara kapalı, API'nin
kendi hata mesajının önerdiği `gemini-3.6-flash`'a geçildi; (2) ilk denemede
çıktı yarıda kesiliyordu -- sebebi modelin "thinking" (iç muhakeme) token'larının
`max_output_tokens` bütçesinden düşmesiydi (`thoughts_token_count` günlükte
görüldü). `thinking_budget=0` ile tamamen kapatmak bu modelde reddedildi (400
hata) -- çözüm `thinking_level="low"` + `max_output_tokens=2048`'e çıkarmak
oldu. Gerçek bir örnek üretimle doğrulandı: üç bölüm de doğru formatta
("## Gözlemlenen olası örüntü" / "İyi gidenler" / "Nazik bir not"), teşhis
dili yok, temkinli ton korunuyor.

## "Korku" → "Sinirli" Kategori Değişikliği + Ölçeklendirme Düzeltmesi (19.08.2026, gece)

Kullanıcının gözlemi: "korku" davranışsal olarak gerçekçi hissettirmiyordu,
"sinirli" gibi bir kategori daha gerçekçi olur mu? Haklı bir gözlem --
`psikolojik_durum.py`'nin kendi dosya-başı dürüstlük notu zaten "korku ile
anksiyete'yi ayırt etmenin bilimsel bir üst sınırı var" diyordu, çünkü ikisi
de "negatif duygu + pasif" örüntüsüydü, davranışsal olarak neredeyse aynı
imzayı taşıyorlardı. **"sinirli" (negatif duygu + roket/yorum VAR, aktif
tepkisel katılım) davranışsal olarak GERÇEKTEN AYRIT EDİLEBİLİR bir imza** --
"korku"nun donup-pasif-izleme'sinin tam tersi. 5 kategori: sakin, mutluluk,
umut, sinirli, anksiyete. Arayüz (renk, etiket, doğrulama kartı emojisi) ve
`rapor.js` buna göre güncellendi.

**Yan bulgu (kod incelenirken ortaya çıktı, saklanmadı):** kategori değişip
model yeniden eğitilince F1 makro 0.78'den 0.686'ya düştü. Kök neden
araştırıldı: `dwell_saniye` (0-15+ saniye) ile `duygu` (-1..1) ve
roket/yorum/tıklama (0/1) arasında BÜYÜK ölçek farkı var, lineer modelde
(SGDClassifier/lojistik regresyon) ölçeklenmemiş büyük-skala özellik küçük
olanları gölgeliyor. Eskiden bu sorun gizliydi çünkü "korku"nun ayrımı
neredeyse tamamen dev dwell büyüklüğüyle yapılıyordu; "sinirli" ise küçük
skala olan duygu işaretine (negatif/pozitif) dayandığı için sorun görünür
oldu. `StandardScaler` eklendi (eğitim + `psikolojik_durum_tahmini` +
`kisisel_guncelle` -- üçü de AYNI dondurulmuş `_OLCEKLEYICI`'yi kullanıyor,
tutarsızlık olmasın diye). Sonuç: F1 makro 0.686 → **0.704**, kategoriler
arası denge de düzeltildi (örn. "umut" precision 0.55 → 0.72). Eski 0.78'in
altında ama bu, gerçek ve daha zor bir ayrım görevinin dürüst sonucu --
uydurma bir sayı değil. `rapor.html` altbilgisindeki eski/yanlış F1≈0.78 ve
"ince ayar sürüyor" ifadeleri de güncel gerçek değerlere düzeltildi.

**Doygunluk azaltma "çalışmıyor gibi" sorunu (aynı gece) — kök neden bulundu
ve düzeltildi.** Kullanıcı canlı testte fark etmediğini bildirdi. Tarayıcıda
`getComputedStyle` ile doğrulandı: mekanizma TEKNİK olarak çalışıyordu
(`#akis` üzerinde `filter: saturate(...)` doğru uygulanıyordu), ama etki
gözle görülemeyecek kadar küçüktü -- iki sebep: (1) `_guven_carpani` (az
etkileşimde spiral_seviyesi'ni kasıtlı bastıran güven mekanizması) ilk
birkaç etkileşimde seviyeyi çok düşük tutuyor (örn. %9'da doygunluk sadece
%96 -- fark edilmez), (2) eski formülün maksimum azalması bile sadece %45'ti
(seviye=1'de saturate(55%)). Güven bastırmasını KORUDUK (istatistiksel
gerekçesi hâlâ geçerli, spiral_seviyesi ile tutarlılık ilkesi bozulmasın
diye) ama görünürlük eğrisini güçlendirdik: maksimum azalma %45→%75, eğri
de `seviye^0.7` ile öne yüklendi (orta seviyelerde de belirgin olsun, sadece
seviye=1'e çok yaklaşınca değil). Test: seviye=0.33 → saturate(66%) (öncesi
~saturate(85%) olurdu), seviye=1.0 → saturate(25%) (öncesi saturate(55%)).

## Rapor Sayfası Metin Düzeltmesi + "Terapiste Götürülebilir Veri Özeti" (19.08.2026, gece)

`rapor.html` başındaki uyarı kutusu artık yanlıştı -- "gerçek sürümde bir LLM
tarafından üretilir" diye GELECEK ZAMANDA yazıyordu ama bu artık şu anda
oluyor (canlı LLM raporu çalışıyor). Metin, hangi bölümlerin gerçekten canlı
(gözlemlenen/doğrulama/AI yorumu) hangi bölümün hâlâ sabit format örneği
(10-16 Ağustos) olduğunu netleştirecek şekilde güncellendi. "Teşhis/klinik
değerlendirme değildir" uyarısı AYNEN korundu.

**Yeni özellik: "Bir uzmana götürmek istersen" bölümü.** Kullanıcının önerisi
-- LLM, isteğe bağlı olarak, kullanıcının bir ruh sağlığı uzmanına götürebileceği
YORUMSUZ bir ham veri özeti de hazırlayabilsin. Kişisel rapordan (sıcak,
"Nazik bir not" içeren) kasıtlı olarak FARKLI bir sistem talimatıyla
(`SISTEM_TALIMATI_TERAPIST`, `haftalik_rapor.py`) çalışıyor: tavsiye/yorum/
sonuç çıkarma YASAK, üçüncü şahıs+nötr dil, sadece "Veri Özeti / Gözlemlenen
Davranışsal Örüntüler / Sınırlılıklar" başlıklarıyla ham sayıları sunuyor,
"Sınırlılıklar" bölümünde modelin sentetik veriyle eğitildiğini, klinik
doğrulaması olmadığını ve TEK BAŞINA yeterli olmadığını tekrar etmesi
ZORUNLU. Otomatik yüklenmiyor -- talep üzerine (buton) üretiliyor, her sayfa
açılışında gereksiz LLM çağrısı olmasın diye. `uret()` fonksiyonuna
`hedef="kisisel"|"terapist"` parametresi eklendi, yeni endpoint:
`GET /api/terapist-raporu`. Canlı test edildi -- çıktı beklenen çerçeveye
tam uyuyor, açılış cümlesi "klinik bir belge değildir, nihai değerlendirme
uzmana aittir" diyor.

## Sırada Ne Var (güncel, 19.08.2026 gece — eski liste tamamen tamamlanmıştı, yenilendi)

1. **[ÖNEMLİ] GitHub reposundaki eski `README.md`'yi düzelt/kaldır** — hâlâ Claude Code
   kurulumunu/Cowork iş bölümünü anlatıyor (projenin en başından kalma), jüri repoyu
   açtığında bunu görmemeli. `README.txt` (kurulum rehberi) zaten var, onunla
   değiştirilmeli veya birleştirilmeli. Kullanıcı "projeyi bitirdikten sonra" yapalım dedi
   — ŞİMDİ YAPILMAYACAK, teslimden önce mutlaka hatırlat.
2. ~~Başvuru/takım kaydını KYS'de tamamla~~ — **BİTTİ** (19.08.2026 gece, kullanıcı onayladı).
3. Teknik rapor Bölüm 8.1'deki (Takım Yapısı) placeholder rol tablosunu gerçek ekibe göre
   güncelle (isim/fotoğraf KONMAYACAK, sadece roller).
4. Rapor hâlâ 15/30 sayfa — istenirse Teknik Yeterlilik veya Yaygın Etki derinleştirilebilir,
   ama kullanıcı şu an "böyle kalsın" dedi.
5. Perspektif Köprüsü / Dijital Refah Ağacı / Dinamik Sürtünme gibi gelecek-vizyon fikirleri
   şu an sadece `NSosyal_Rapor_Icerigi.pdf`'te var — resmi rapora (`rapor_olustur.py`) kısaca
   değinilmesi istenirse eklenmeli, şu an eklenmedi.

## İş Modeli / Sürdürülebilirlik Fikirleri (rapor 6.1-6.2 için)

NSosyal vakıf tabanlı olduğu için klasik reklam modeli ZORLAMA — bunun yerine: (1) düşük
işletme maliyeti (hafif/açıklanabilir model), (2) anonim/toplu "dijital refah eğilimleri"
verisiyle üniversite/TÜBİTAK/ruh sağlığı STK ortaklığı, (3) "dijital-refah-öncelikli
platform" marka değeri üzerinden kurumsal sponsorluk, (4) opsiyonel gönüllü destek/bağış
mekanizması (roket sistemine benzer).

## Genel Ton/Disiplin Kuralları

- Her teknik iddiada dürüst ol — "kesin" yerine "olası", "kanıtladık" yerine "gözlemledik"
  gibi temkinli bir dil kullan.
- Sağlık/ruh sağlığı bağlamında ASLA teşhis aracı gibi konuşma.
- Siyasi/dini içerik kategorisi üzerinden konuşma, sadece duygusal yoğunluk.
