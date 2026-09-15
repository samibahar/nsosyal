# Final yaklaşımı ve iş modeli

15.09.2026. Final sunumunun dayandığı ölçüm çerçevesinin ve iş modeli önerisinin kısa özeti. Sunum, yarışmanın resmî şablonunda 16 sayfa olarak hazırlandı. Teslim edilmiş teknik rapor değiştirilmedi; iş modeli, raporun sürdürülebilirlik bölümünün somutlaştırılmış önerisidir.

## Ölçümler ayrı ayrı anlatılır

Aşağıdaki sonuçlar kendi tarihleri ve kapsamlarıyla aktarılır. Bu özet hazırlanırken yeni bir ölçüm yapılmadı.

| Ölçüm | Neyi gösterir | Neyi göstermez | Kaynak |
|---|---|---|---|
| winvoker test seti, ikili doğruluk %94,0 (üç sınıfta %95,7) | Genel Türkçe metinde tonun doğruluğu | Haber üslubunda ya da ruh hali tahmininde doğruluk | [model kartı](model_karti.md) §1 |
| 72.495 gerçek metinlik tarama (14.09.2026) | Sistemin farklı içerik türlerinde nasıl işaretleme yaptığı | Bu metinlerin hepsinde doğruluk; çoğu elle etiketli değil | [son doğrulama notu](gorunurluk_ve_final_dogrulamasi.md) |
| 200 haber başlığı, tek etiketleyici: güçlü olumsuz yakalama v3 %12, sözlük %79, birlikte %82 (34 örnek) | Haber başlıklarında olay sözcüğü desteğinin katkısı | Bağımsız son test; set, sözlüğün sonraki düzeltmelerinde görüldü | [model kartı](model_karti.md) §1 |
| Etiketli tweetler: saldırganı işaretleme model %82, yalnız sözlük %7 | Sosyal metinde işi modelin yaptığı | Karma yöntemin her veri türünde üstün olduğu | [model kartı](model_karti.md) §1 |
| Üç kollu kapalı döngü simülasyonu, 18.000 oturum (15.09.2026) | Uyarlanan dozun müdahaleyi takılan örüntülere yoğunlaştırması | İnsanların daha iyi hissettiği; davranışlar simülasyondur | [ölçüm sınırları](olcum_sinirlari.md) |
| Otomatik testler: son tam kayıtta 85 test (14.09.2026) | Kuralların tasarlandığı gibi çalıştığı | Kullanıcı faydası; erişilebilirlik taramasında sıfır ihlal tam WCAG uygunluğu demek değildir | Depodaki `tests/` |

Simülasyonda sonradan eklenen, toplam müdahalesi eşitlenmiş rastgele karşılaştırma keşifsel olarak işaretlenir. Herkese sabit dozun uyarlanan dozdan daha fazla toplam müdahale ettiği gizlenmez. Kullanıcıya faydası ölçülmedi; bilimsel dayanak ve sınırlar için [bilimsel dayanak](bilimsel_dayanak.md).

## İş modeli önerisi

- **Ödeyen:** Sosyal platformun ürün ve teknoloji ekibi. İlk aday NSosyal. Prototipin NSosyal'a API erişimi ya da mevcut bir ortaklığı yoktur; platform izni ve entegrasyon ayrı bir bağımlılıktır.
- **Gelir kalemleri:**
  - dar kapsamlı ücretli pilot;
  - üretim entegrasyonu;
  - yıllık bakım ve destek.
- **Kullanıcı:** Ücretsiz ve gönüllü katılır; katman her an kapatılabilir.
- **Gelir kalemi olmayanlar:** Davranış ya da duygu verisi satışı yok. Duygu durumuna göre reklam hedefleme yok.
- **Başlangıç finansmanı:** Hibe ve sponsorluk başlangıç finansmanıdır, düzenli gelir dayanağı değildir.
- **Doğrulanmamış varsayımlar:** Mevcut müşteri, anlaşma ya da gelir yoktur. Fiyat ve müşteri kazanımı henüz sınanmadı. Pilot bedeli entegrasyon iş günü, test ve raporlama emeği ile içerik analizi maliyetinden hesaplanmalıdır. Tek bir performans mikro ölçümü, gerçek yük testi olmadan ölçek ya da hizmet düzeyi taahhüdüne çevrilmez.
- **Pilotun yazılı kapsamı:**
  - platformun aday akışına erişim ve cihaz içi sıralama arayüzü;
  - kontrol grubunun tanımı;
  - bilgiye erişim güvenceleri;
  - kapatma akışı.
- **Genişlemeden önce başarı kapıları:**
  - açıklama ve kapatmanın anlaşılması;
  - kritik bilgiye erişimde sorun olmaması;
  - olağan kullanımda gereksiz müdahalenin ölçülmesi;
  - model hata oranlarının bağımsız etiketlerle kontrol edilmesi.

  Bu kapılar sağlanmadan "insanlara iyi geliyor" iddiasıyla genişlenmez.
- **Araştırma:** Üniversite iş birliği olası bir sonraki adımdır, kurulmuş bir ortaklık değildir. Sağlık etkisi araştırması etik değerlendirme ve örneklem planı gerektirir. 5–10 kişilik bir kullanılabilirlik pilotu arayüz sorunlarını ortaya çıkarabilir, etkinlik kanıtı üretmez.
