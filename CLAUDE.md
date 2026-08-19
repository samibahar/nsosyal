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
