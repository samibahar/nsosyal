# Ölçümler nasıl anlatılmalı?

14.09.2026 akşamı

- Gerçek gönderilerle oluşturulan davranış oturumları simülasyondur.
  “Gerçek gönderilerle simüle edilen 200 hızlı kaydırma oturumunda
  yanlış dengeleme gözlenmedi” denebilir. Gerçek kullanıcı başarısı veya
  gelecekte sıfır hata garantisi olarak anlatılmaz.
- f203a7d sürümünün ikinci 100 başlıktaki %83 yakalama ve %97 isabeti
  küçük bir iç değerlendirmedir. Test sonuçlarının son sözlük değişikliği
  öncesinde görülüp görülmediği dosyalardan kesinleşmiyor; yalnızca erişim
  imkânı, veri sızıntısının kanıtı değildir.
- Sonradan eklenen karaktersiz yazım ve dar bağlam istisnalarından sonra
  450 başlığın normal yazımındaki sonuç değişmedi; ancak bu başlıklar artık
  geliştirmede görülmüştür, bağımsız ölçüm değildir. Sonraki ölçümde sözlük
  sürümü, örneklem, sınıf adetleri ve güven aralıkları belirtilmeli.
- Önceki güncellemede BERT yeniden eğitilmedi; spiral katsayıları değişen
  özellik tanımıyla aynı simülatörde yeniden uyduruldu. “Hiçbir model
  eğitilmedi” ifadesi bu güncellemenin bütünü için doğru değildir.
- 15 saniye kırpması bir giriş sınırlamasıdır. Çıktının “umut” yerine
  “anksiyete” olması kişinin gerçek duygusunun doğrulandığını göstermez.
- Maruziyet azalması, öz-bildirimle tahmin uyumu, kullanılabilirlik ve iyi
  oluş farklı sonuçlardır. Birinin ölçümü diğerinin kanıtı yerine geçmez.
- Otomatik erişilebilirlik denetiminde sıfır ihlal, tüm erişilebilirlik
  gereksinimlerinin veya gerçek kullanıcı deneyiminin doğrulandığı anlamına gelmez.

## 15.09.2026 eklemeleri

- **Sistem kendi başarısını ölçmemeli.** Simülasyondaki "yoğun içerikte
  süre", müdahalenin kullandığı tonla ölçülür. Bu yüzden "yoğunluk %X düştü,
  kaygı %X azaldı" denemez. Üç kollu simülasyona bu yüzden ikinci bir ölçüt
  eklendi: veri setlerinin kendi etiketine göre olumsuz içerikte (saldırgan
  mesaj, düşük puanlı yorum) geçen süre. Bu ölçüt de insan duygusu değildir.
- **Pay ile toplam ayrı.** Yoğun içeriğin payı düşerken toplam görülen içerik
  artarsa toplam maruziyet artabilir. Simülasyonlarda iki koşulda sayfa sayısı
  eşit tutulduğu için toplam süre ölçüldü. Serbest kullanımda oturum
  uzunluğu değişebilir; bu ölçülmedi.
- **Uyarlanan doz ile basit kural** (üç kollu kapalı döngü simülasyonu,
  18.000 oturum). Önceden belirlenen sabit düzeylerin en düşüğü bile
  uyarlanan dozdan yaklaşık 1,7 kat fazla müdahale etti, yani "eşit toplam
  müdahale" koşulu sağlanamadı. Önceden belirlenen ölçüte göre sonuç
  "kısmen":
  - Takılan profillerde azalma benzer (−%32 ile −%33).
  - Olağan okurda uyarlanan doz çok daha az dokunuyor (−%6 ile −%32).

  Sonradan eklenen, toplam müdahalesi eşitlenmiş rastgele zamanlı sabit
  kolla karşılaştırmada (keşifsel) uyarlanan doz takılan profillerde daha
  çok (−%32 ile −%20), olağanda daha az (−%6 ile −%18) azaltıyor. Bağımsız
  etiket ölçütü aynı yönde. Davranışlar simülasyondur; simülatör ve spiral
  modeli benzer varsayımlara dayanır, bu yüzden bu sonuç teknik bir ek katkı
  gösterir, insan yararı göstermez.
- **Bileşen katkısı** (model kartı §1). Haber başlıklarında yakalamayı
  sözlük, sosyal içerikte model sağlıyor. Sosyal içerikte sözlük yanlış
  işareti artırıyor. Etiketli setlerin hiçbiri güncel sözlük için "hiç
  görülmemiş" değildir.

Sunuma uygun ifade: “Gerçek gönderilerle kurduğumuz simülasyonlarda hızlı
kaydırmaya verilen gereksiz müdahaleyi azalttık. Yeni haber başlıklarında
ve gönüllü kullanıcılarda doğrulamaya devam edeceğiz.”
