# Model Kartı — NSosyal Duygu Katmanı

Son güncelleme: 14.09.2026. Bu belge sistemdeki üç modeli ve sıralama
kuralını; veri kaynaklarını, ölçümleri, sınırlılıkları ve etik kararları
özetler. Rakamların kaynağı depodaki `*_sonuc.txt` dosyalarıdır ve ilgili
betikle yeniden üretilebilir.

| Bileşen | Nerede çalışır | Ne üretir | Ayrıntı |
|---|---|---|---|
| Duygu modeli (BERT v3) + olay sözcüğü desteği | Sunucu, gönderi başına bir kez | Gönderi metninin tonu (−1…+1) | §1 |
| Spiral modeli v2 | Kullanıcının tarayıcısı | Son 30 dk'da yoğun içerikte pasif oyalanma olasılığı | §2 |
| Ruh hali modeli | Kullanıcının tarayıcısı | Son 30 dk'daki etkileşimlerden 5 kategorili olası ruh hali | §3 |
| Sıralama + doz dengelemesi | Kullanıcının tarayıcısı | Akışın sırası | §4 |

## 1. Duygu modeli (BERT v3)

**Son sözlük güncellemesi (14.09 akşamı):** Karaktersiz yazım ve "kazasız" düzeltmeleri sonrasında
normal yazımlı 450 başlığın sonuçları değişmedi. Karaktersiz varyantlarda güçlü
olumsuz yakalama %53,3'ten %77,8'e; olumsuz olmayanda işaret %3,8'den %5,9'a
çıktı. Bunlar geliştirmede görülmüş örneklerdir. Görünürlük takibi, model rolü,
bileşen karşılaştırması ve sınırlar için [son doğrulama notu](gorunurluk_ve_final_dogrulamasi.md).

**Amaç ve kullanım.** Herkese açık gönderi metninin duygusal tonunu tahmin
eder: ton = P(pozitif) − P(negatif). Sıralamada yalnızca "yoğun tonlu" (ton <
−0,15) işareti olarak kullanılır. Kullanıcı hakkında bir çıkarım değildir;
gönderinin özelliğidir.

**Soy ağacı.** `savasy/bert-base-turkish-sentiment-cased` → v1 (winvoker,
~15 bin ikili örnek) → v2 (haber üslubu, ikili) → **v3 (üç sınıf: negatif /
nötr / pozitif)**. v3'ün sınıflandırıcı katmanı rastgele değil, v2'nin
negatif ve pozitif satırlarından başlatıldı.

**Neden v3.** v2 ikili olduğu için ton = işaret × güven idi ve uygulamadaki
gönderilerin %94'ünde |ton| > 0,9 çıkıyordu; olgusal bir duyuru da "çok
olumsuz" sayılabiliyordu.

**v3 eğitim verisi** (`ince_ayar_v3.py`):

| Kaynak | Adet | Not |
|---|---|---|
| winvoker `split="test"` negatif | 5.600 | Kaynaklara göre dengeli |
| winvoker `split="test"` nötr | 6.000 | Neredeyse tamamı Vikipedi cümlesi; olay/değerlik kelimesi içeren ~2.080 nötr ayıklandı |
| winvoker `split="test"` pozitif | 6.000 | Kaynaklara göre dengeli (ürün yorumu baskın olmasın) |
| `zayif_uslup_veri.jsonl` | 712 (×2) | Kısa, resmi haber üslubu; kısmen bir dil modeliyle, kısmen ekip tarafından üretildi |
| `haber_uslubu_uc_sinif.jsonl` | 337 (×5) | Bu proje için yazılmış üç sınıflı haber ve paylaşım cümleleri (137 nötr, 106 negatif, 94 pozitif) |

Test ve doğrulama metinleri, uygulamadaki gönderi ve haber metinleri eğitimden
açıkça çıkarıldı.

**Eğitim.** Öğrenme oranı 3e-5, 2 epoch, parti 32, %6 ısınma, fp16, en fazla
128 belirteç; tek RTX 4060'ta ~4 dakika. Ayarlar 6 aday arasından **yalnızca
doğrulama setiyle** seçildi (winvoker'dan test örnekleriyle kesişmeyen 1.500
örnek + 60 cümlelik haber doğrulama seti): `v3_arama_sonuc.txt`.

**Test sonuçları** (`dogrulama_v3_sonuc.txt`; hiçbiri eğitimde ya da seçimde
kullanılmadı):

| Test | v2 | v3 |
|---|---|---|
| winvoker 1.000 örnek, ikili doğruluk (630 pozitif/negatif) | %93,3 | **%94,0** (F1 0,963) |
| winvoker üç sınıf doğruluğu | — | **%95,7** (F1 makro 0,929) |
| Nötr etiketli örneklerde ortalama \|ton\| | 0,961 | 0,005 |
| Elle etiketlenmiş 40 haber üslubu cümle | %92,5 | %92,5 |
| Ekibin önceden puanladığı 22 haber, yön uyumu | %77 | %82 (Spearman ρ 0,65) |
| Jüri demosundaki 14 gönderi, yön uyumu | %93 | %93 |
| Uygulamadaki 250 gönderide \|ton\| > 0,9 | %94 | %54 |

**Sınırlılıklar.**
- Nötr sınıfı büyük ölçüde Vikipedi cümlelerinden öğrenildi.
- Duygu kelimesi içermeyen bazı birinci şahıs cümleleri yanlış okunabiliyor
  (örnek: "Kütüphanede herkesin aynı anda sayfa çevirmesi garip biçimde motive
  edici" olumsuz okunuyor).
- Ton, sınıflandırıcı olasılıkları arasındaki farktır; psikolojik bir duygu
  yoğunluğu ölçümü değildir.
- Eğitim verisinin bir kısmı sentetiktir (yukarıdaki tablo).

**Gerçek haber başlıklarında sınır ve olay sözcüğü desteği (14.09.2026).**
Bu bölümdeki %83/%97, sözlüğün ilk sürümünün (commit `f203a7d`) iç
değerlendirmesidir; ayrılmış 100 başlık, sözlüğün son küçük düzeltmelerinden
önce de görülmüştü. Aynı sürüm daha sonra hiç görülmemiş dört kaynaktan 200 yeni
başlıkta güçlü olumsuzların %82'sini yakaladı (isabet %90). Sonraki eklemelerle
(karaktersiz yazım, "kazasız", dar bağlam istisnaları) 450 başlığın normal
yazımındaki sonuç değişmedi, ama bu başlıkların hepsi artık geliştirmede
görülmüştür. Bağımsız son değerlendirme için kurallar dondurulduktan sonra yeni
örneklem ve ikinci etiketleyici gerekir.

Yukarıdaki testler winvoker ve bizim yazdığımız cümlelerdir. Herkese açık
gerçek Türkçe haber başlıklarından elle etiketlediğimiz 250 başlıkta v3, açık
olumsuz bir olay bildiren başlıkların (ölüm, yaralanma, saldırı, yangın,
kaza…) yalnızca %6–8'ini yoğun okudu: haber üslubundaki olgusal anlatımı nötr
sayıyor. Model yeniden eğitilmeden açık olay sözcükleri için bir sözlük
eklendi (`yogun_sozluk.py`): başlıkta böyle bir sözcük varsa ton en fazla
−0,9 olur. Sözlük tonu yalnızca aşağı çeker, olumluya çeviremez. Sözlük 150
başlıklık geliştirme setiyle yazıldı, sonra hiç bakılmamış 100 başlıkla
ölçüldü:

| Ayrılmış 100 başlık | v3 | v3 + sözlük |
|---|---|---|
| Güçlü olumsuz başlıkları yakalama | %6 | **%83** |
| Herhangi bir olumsuz başlık (tutuklama, dava dahil) | %9 | %43 |
| İşaretlenenlerin gerçekten olumsuz olması (isabet) | %100 (çok az işaret) | %97 |
| Olumsuz olmayan başlığı işaretleme | %0 | %3 |
| Gerçek tweetler: saldırgan / normal işaretleme | %82 / %16 | %83 / %20 |

Hafif olumsuz haberlerin (tutuklama, dava) çoğu bilerek işaretlenmez: doz,
sarsıcı içeriğin tekrarını azaltmayı hedefler. Tek başına "deprem", "sel",
"şiddetli" ya da "kazan-" gibi yanlış alarm üreten sözcükler sözlüğe
alınmadı. Denenen alternatifler: v2 haberlerde daha çok yakalıyor ama normal
tweetlerin %47'sini işaretliyor; hazır bir çıkarım (NLI) modeli ancak test
etiketlerine bakılarak seçilen bir hipotez cümlesiyle iyi sonuç verdiği için
güvenilir bulunmadı. "Neden bu?" açıklaması tonu sözcüğün belirlediğini ve
modelin kendi tonunu gösterir.

**Atıf ve lisans.** Temel model `savasy/bert-base-turkish-sentiment-cased`,
veri seti `winvoker/turkish-sentiment-analysis-dataset` (HuggingFace). Temel
modelin sayfasında lisans belirtilmemiştir; ince ayarlı model araştırma ve
yarışma amaçlıdır.

## 2. Spiral modeli v2

**Amaç.** Son 30 dakikadaki davranıştan "yoğun tonlu içerikte, kendi okuma
hızına göre belirgin biçimde uzun ve pasif kalma" olasılığını tahmin eder.
Teşhis değildir; yalnızca akışın dozunu ayarlamak için kullanılır.

**Girdi (cihazda).** Gönderi başına birleştirilmiş olay: durma süresi, ton,
kelime sayısı, roket/yorum. Yakın olaylar daha ağırdır (10 dk yarı ömür).
Beklenen okuma süresi = 1,5 sn + kelime / 3,5.

**Model.** İşaret kısıtlı lojistik regresyon: her özelliğin riski hangi yönde
etkilediği hipotezle sabitlenir, büyüklüğü veriden öğrenilir. Kısıtsız
denemede özellikler birbirini dengelemek için ters işaret alıyor ve hep olumlu
içerik okuyan kullanıcıyı riskli sayıyordu.

| Özellik | Standartlaştırılmış katsayı |
|---|---|
| Göreli oyalanma (yoğunlarda kendi hızına göre) | +1,56 |
| Aktif katılım (roket, yorum) | −0,85 |
| Yoğun pay, okuma üstü kalma | 0 (kısıt nedeniyle kullanılmadı) |

**Eğitim verisi.** Davranış düzeyinde simülatör: 4.000 oturum, 7 kullanıcı
türü (olağan, spiral, uzun okuyan, olumsuz haberleri aktif tartışan, hızlı göz
atan, spirale geçen, saatler önce yoğun oturum geçirmiş), akıştaki yoğun
içerik payı %5–%90, %8 etiket gürültüsü. Etiket simülasyondaki gizli durumdur,
özelliklerin bir formülü değildir.

**Ölçüm** (`spiral_v2_sonuc.txt`, simülatörün ayrılmış %25'i):

| | v1 (eski) | v2 |
|---|---|---|
| ROC-AUC | 0,632 | 0,856 |
| F1 | 0,517 | 0,728 |
| Kalibrasyon hatası (ECE) | 0,299 | 0,041 |
| Yanlış alarm: uzun okuyan / hızlı göz atan / eski oturum | %62 / %29 / %56 | %0,8 / %1,2 / %0 |
| Spiral oturumu yakalama | %71 | %88 |

**Hızlı kaydırma düzeltmesi (14.09.2026).** Gerçek gönderilerle kurulan
oturumlarda 0,4–1 sn'lik rastgele durma farkları hızlı kaydırmayı "oyalanma"
gibi gösteriyor ve oturumların %23–34'ünde dengelemeyi başlatıyordu. Okuma
tabanının (1,5 sn) altındaki durmalar artık göreli oyalanmaya girmez; model
aynı simülatörde bu tanımla yeniden eğitildi (katsayılar ve ölçümler yukarıda
günceldir). Aynı kural ruh hali penceresine de uygulandı (§3). Gerçek
gönderilerle (haber başlıkları, tweetler; tonlar §1'deki gibi) 200'er oturumda
son durum:

| Davranış | Dengeleme başlar | Bildirim |
|---|---|---|
| Suç/şiddet haberlerinde pasif takılma | %100 | %66 |
| Deprem haberlerinde pasif takılma | %91 | %16 |
| Saldırgan tweetlerde pasif takılma | %100 | %84 |
| Aynısı, yorum yazarak (aktif) | %29 | %0 |
| Olağan okuma | %12 | %0 |
| Hızlı kaydırma (0,4–1 sn) | %0 | %0 |
| Uzun olumlu okuma | %0 | %0 |

**Sınırlılıklar.** Simülatör hipotezlerimizi kodlar ve karşılaştırma v2'nin
lehinedir; gerçek dünya doğruluğu değildir. Sakin oturumlar 0,26 civarında
kalır (simülasyondaki %35 spiral payından gelen önsel). Gerçek kullanıcı
onaylarıyla yeniden eğitilmelidir. Python ve tarayıcı özellik hesabı birebir
aynıdır (otomatik eşitlik testi); 11 senaryo testi `tests/test_spiral_model.py`.

**Cihazda kişisel kalibrasyon (12.09.2026).** Kontrol sorusunda "yoğun" ya da
"sinirli" cevabı spiral için 1, "sakin/mutluluk/umut" 0 sayılır (zayıf etiket).
Model çıktısı kişiye özel iki parametreyle yeniden ölçeklenir (Platt: eğim ×
logit(p) + kayma). Eğim en az 0,25 tutulduğu için özelliklerin riski etkileme
yönü hiçbir zaman tersine dönmez. Kalibrasyon akışa ancak en az 6 cevapta, her
cevap önce tahmin edilip sonra öğrenilerek, varsayılandan düşük Brier hatası
verirse bağlanır; jüri demosu kalibrasyonsuz çalışır. Gönüllü pilot için dışa
aktarma ve analiz: `docs/pilot_protokolu.md`, `pilot_analizi.py`.

## 3. Ruh hali modeli

**Amaç.** Son 30 dakikanın olası ruh halini beş kategoride tahmin eder:
sakin, mutluluk, umut, sinirli, yoğun (anksiyete). Klinik bir ölçüm değildir.

**Pencere (12.09.2026).** Ruh hali tek bir gönderiyle değişmez; tek gönderinin
sinyali de zayıftır. Sınıflandırıcı her etkileşimi ayrı tahmin eder, sonra son
30 dakikadaki tahminler zamanla azalan ağırlıkla (10 dk yarı ömür, spiral ile
aynı) ortalanır. Ortalama alınır, çarpılmaz: ardışık gönderiler bağımsız kanıt
değildir, çarpım modeli gereksiz yere kesinleştirirdi. En az 3 etkileşim yoksa
tahmin yapılmaz. Okuma tabanından (1,5 sn) kısa durulan gönderi okunmamış
sayılır ve kanıta girmez; 15 sn'den uzun durma 15 sn sayılır (sentetik eğitim
verisi bu aralığın dışını görmedi, olumsuz içerikte 30 sn durma "umut"
okunuyordu; 14.09.2026). Raporlarda (İçgörü ısı haritası, uzman özeti) her an, o sırada
geçen süreyle ağırlıklandırılır: gönderi sayısı değil süre sayılır.

**Model.** Girdi: ton, durma süresi, tıklama, roket, yorum. Standart ölçekleme
+ lojistik kayıplı SGD (bire-karşı-diğerleri). Sentetik veri: kategori başına
500 örnek, %10 etiket gürültüsü. Sentetik test setinde doğruluk ve F1 makro
0,704. Tarayıcıdaki olasılıklar sklearn ile birebir aynıdır (önceden softmax
kullanıldığı için 0,17'ye kadar sapıyordu; düzeltildi).

**Cihazda kişisel uyarlama.** Kullanıcı "Şu an nasıl hissediyorsun?" sorusunu
cevapladığında kişisel modelde tek küçük bir adım atılır (η 0,15; varsayılan
modele doğru λ 0,05 düzenlileştirme). Cevap o anki pencereye aittir: adım
penceredeki etkileşimlere ağırlıkları oranında paylaştırılır (pencerenin
ortalama kaybı için bir SGD adımı). Önce tahmin edilir, sonra öğrenilir;
eşleşme oranı hiç görülmemiş cevaplarla ölçülür. Kişisel model yalnızca
etiketleri etkiler, sıralamayı kaydırmaz.

**Doğrulama.** İçgörü ekranı eşleşme oranını iki taban çizgisiyle yan yana
gösterir: rastgele (%20) ve "hep en sık cevabı söyle". Model bu tabanı
geçmiyorsa ekran bunu açıkça yazar.

## 4. Sıralama ve doz dengelemesi

- **Çekirdek puan:** 0,48 × sunucunun ilgi puanı + 0,34 × cihazdaki konu
  ilgisi (+ kullanıcının son açık tepkisi).
- **Çeşitlilik:** açgözlü seçim; bir konudan ilk gönderi +0,07, sonrakiler
  −0,09 × n. Bonus seçilmiş listeye göre verilir.
- **Akış yoğunluğu:** 0,7 × spiral + 0,3 × (sinirli + yoğun olasılığı);
  dengeleme en az 10 etkileşim ve yoğunluk > 0,28 iken çalışır.
- **Doz:** sayfadaki yoğun tonlu içerik payı hedefe iner: hedef = taban pay ×
  (1 − 0,6 × yoğunluk). Yoğun gönderiler silinmez, aralıklanır. Resmi/acil
  bilgi hesapları muaftır. Yaklaşım "kalibre edilmiş öneri" fikrinin (Steck,
  RecSys 2018) maruziyet payına uygulanmasıdır.

**Etki** (`etki_analizi_sonuc.txt`; 600 senaryo, ilk sayfa; tonlar olay
sözcüğü desteğiyle):

| Akış yoğunluğu | Yoğun içerik payı | Korunan ilgi | Yoğunların ilk 3 sayfada kalması |
|---|---|---|---|
| 0,35 | −%35 | %100 | %58 |
| 0,6 | −%47 | %99 | %48 |
| 0,85 | −%62 | %99 | %36 |

Yoğun gönderiler ortalama 6,8 sıra arayla gelir (art arda gelme %3); resmi
gönderi 146 durumun hiçbirinde aşağı inmedi. Önceki "puandan ceza" sürümü
yoğunluk 0,85'te payı %96 azaltıyordu (fiilen filtre); bu yüzden değiştirildi.
Gerçek haber başlıklarından kurulan akışta (300 senaryo) aynı yöntem payı
−%33 / −%48 / −%59 azalttı, ilgi %99,9+ korundu. Bu bir maruziyet ölçümüdür,
iyi-oluş etkisi değildir.

## 5. Etik ve gizlilik kararları

- **Açık rıza:** ilk açılışta ne tutulduğu, nerede saklandığı ve teşhis
  olmadığı anlatılır; açık/kapalı iki eşit seçenek.
- **Veri cihazda:** ham davranış ve gün başına toplamlar yalnızca tarayıcıda,
  12 hafta; daha eskisi kendiliğinden silinir, kullanıcı tek tuşla hepsini siler. Sunucu davranış verisi kabul eden hiçbir uç nokta
  sunmaz; tarayıcı depolamaya izin vermezse kişiselleştirme yapılmaz.
- **Dış servis yok:** hiçbir davranış verisi üçüncü taraf bir yapay zekâ
  servisine gönderilmez.
- **Konu-nötr:** siyasi/dini kategori yoktur; yalnızca duygusal ton.
- **Reklam hedefleme yok:** kırılganlık hiçbir zaman hedefleme sinyali olarak
  kullanılmaz.
- **Kontrol:** dengeleme kalıcı olarak (Ayarlar) ya da yalnızca bu oturum için
  kapatılabilir; tüm yerel veriler iki adımlı onayla silinebilir.
- **Bilgiye erişim:** resmi/acil bilgilendirme dengelenmez; ilke "haberi
  saklamak değil, tekrarını azaltmak".
- **Dil:** "tespit ettik" değil "olası örüntü"; hiçbir ekran teşhis iddia
  etmez.
- **Açık kalan:** gerçek kullanıcılarla iyi-oluş etkisi ölçülmedi; bu, pilot
  çalışma gerektirir.

## 6. Performans (`olcek_olcumu_sonuc.txt`)

- Duygu modeli: tek RTX 4060'ta saniyede 1.619 gönderi (günde ~140 milyon),
  8 çekirdek CPU'da saniyede 60 (günde ~5,2 milyon). Ton gönderi başına bir kez
  hesaplanır; maliyet okuyucu sayısıyla değil gönderi sayısıyla büyür.
- Cihazda: spiral 1,7 ms, ruh hali 0,3 ms (Python referansı); 48 adayın
  sıralaması tarayıcıda ortanca 0,1 ms.
- 48 adaylık liste gzip ile ~2–3,5 KB; fotoğraflar yalnızca gösterilen
  gönderiler için iner.
