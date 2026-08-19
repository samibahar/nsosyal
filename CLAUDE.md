# Proje Bağlamı — NSosyal İnovasyon Yarışması (TEKNOFEST)

Bu dosya, Claude Code'un bu projeye başlarken hiçbir şeyi baştan sormasına gerek kalmadan
tüm bağlamı okuması için hazırlandı. Cowork'te (bulut ortamı) uzun bir araştırma/planlama
sürecinden geçtik — burada varılan tüm kararlar özetleniyor. Lütfen bu kararları
sorgulamadan kabul et, aksini gerektiren yeni bir bilgi çıkmadıkça.

## Yarışma ve Teslim

- Yarışma: NSosyal İnovasyon Yarışması (TEKNOFEST, düzenleyen: 2N Medya + T3 Vakfı).
- Resmi şartname okundu: `2026_NSOSYAL_YARISMASI_SARTNAMESI_TR_2026_07_24_v9_1.pdf` (V3, 17.08.2026).
- Son başvuru tarihi 20 Ağustos 2026 idi — **başvuru/takım kaydı tamamlandı** (19.08.2026
  itibarıyla kullanıcı onayladı, 2-5 kişilik takım + takım kaptanı zorunluluğu karşılandı).
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
- **Puanlama (Sosyal Yapay Zekâ teması):** Teknik Yeterlilik ve Uygulanabilirlik %35 (en
  ağırlıklı kriter — kod/mimari kalitesine öncelik ver), Yenilikçilik ve Özgünlük %20,
  Problemi Çözme Başarısı %20, Sunum ve Prototip Kalitesi %15, Kullanıcı Deneyimi (UI/UX)
  %10, İş Modeli ve Sürdürülebilirlik %0 (bu tema için ağırlıksız — rapor şablonu muhtemelen
  yine de istiyor ama puana katkısı yok, fazla zaman harcama).
- **Beklenen teslimatlar (tüm yarışma boyunca, sadece 24 Ağustos değil):** teknik rapor,
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

## Sırada Ne Var (öncelik sırasıyla)

1. `spike_poc.py`'deki `duygu_skoru()` fonksiyonunu gerçek BERT modeliyle değiştir.
2. Spiral sınıflandırıcıyı gerçek (senaryo-bazlı sentetik) veriyle eğit, performans
   metriklerini (F1, doğruluk) çıkar.
3. Basit bir web arayüzü kur — gönderi/timeline formatında (Reels DEĞİL), şeffaflık
   paneli, örnek haftalık rapor ekranı. Dwell-time takibini Intersection Observer ile ekle.
4. LLM ile örnek haftalık rapor metni üret.
5. Git reposunu düzenli commit'lerle ilerlet.

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
