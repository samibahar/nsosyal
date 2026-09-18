# 20 Eylül 2026 final sunumu: konuşma metni ve anlatım planı

NSosyal İnovasyon Yarışması, Duygu Katmanı takımı. Canlı sunum 20.09.2026, KÜME Vakfı: 15 dakika sunum, ardından ayrı 2 dakika demo.
Bu metin `NSosyal_Final_Sunum_v16.pdf` içindir. Her bölümde önce söylenecek metin, sonra varsa "Dikkat" ve "Soru gelirse" notları var.

## Sayfa sayfa akış

| Sayfa | Bölüm | Sayfadaki ana mesaj | Zaman |
|---|---|---|---|
| 1 | Kapak | — | 0:00–0:18 |
| 2 | Takım | İki kişilik, birlikte geliştiren ekip | 0:18–0:35 |
| 3 | Proje özeti | Akışın yoğunluğunu ilgi alanını koruyarak dengeleyen katman | 0:35–1:28 |
| 4 | Problemin tanımı - neden bir sorun var | Sorun tek gönderide değil, art arda gelen yoğunlukta | 1:28–2:42 |
| 5 | Problemin tanımı - mevcut araçlar | Mevcut araçlar süreyi yönetiyor, içeriğin dozunu değil | 2:42–3:39 |
| 6 | Çözüm önerisi - mottomuz ve çalışma prensibi | Haberi saklamıyoruz, dozunu azaltıyoruz | 3:39–4:51 |
| 7 | Çözüm önerisi - kontrol kullanıcıda | Kontrol kullanıcıda: her karar açıklanır, geri alınabilir | 4:51–5:36 |
| 8 | Çözüm önerisi - ruh hali modeli ve uzman özeti | Tahmin kullanıcıya sorularak sınanır, özet kullanıcıda kalır | 5:36–6:35 |
| 9 | Teknik mimari | İçerik analizi ortak, davranış hesabı cihazda | 6:35–7:13 |
| 10 | Model ve veri kapsamı | 72.495 metinle tarama, etiketli kümelerle doğrulama | 7:13–8:49 |
| 11 | Prototip | Geliştirirken gördük, düzelttik | 8:49–9:38 |
| 12 | Uygulanabilirlik | Üretime geçiş, ölçülebilir koşullara bağlı | 9:38–10:13 |
| 13 | İş modeli | Gelir modeli: platforma entegrasyon ve bakım | 10:13–10:55 |
| 14 | Özgünlük ve yerlilik | Benzer deneyler herkese aynı kuralı uyguladı; biz kişiye bakıyoruz | 10:55–12:10 |
| 15 | Uyarlamanın katkısı | Uyarlama, olağan okura daha az müdahale ediyor | 12:10–13:08 |
| 16 | Hedef kitle ve etki | İlk pilotta kabul ve kullanılabilirliği ölçeceğiz | 13:08–13:48 |
| 17 | Takvim ve kapanış | Finalden sonra öncelik: kontrollü pilot | 13:48–14:13 |

## Prova metni

Bu dosya jüriye yüklenecek sunuma dahil değildir. Sayfa numaraları aynı klasördeki 17 sayfalık `NSosyal_Final_Sunum_v16.pdf` ile eşleşir.

Hedef zaman planı: **14 dakika 13 saniye**, ardından ayrı **2 dakika demo**. Süreler metnin hece sayısından hesaplandı (saniyede 3,8 hece, rahat sahne hızı); kronometreli prova sonucu değildir. Kendi konuşma hızınızla en az iki prova yapın. Süre taşarsa veri kümesi ayrıntılarını kısaltın, sınırları belirten cümleleri çıkarmayın.

## 1. Kapak (0:00 - 0:18)

Merhaba, biz Duygu Katmanı takımıyız. Mottomuz tek cümle: haberi saklamıyoruz, dozunu azaltıyoruz. NSosyal için, ilgi alanından çıkmadan akışın duygusal yoğunluğunu dengeleyen bir katman geliştirdik.

## 2. Takım (0:18 - 0:35)

Takımımız İTÜ Uçak Mühendisliği öğrencileri Sami Bahar ve Emir Yusuf Uytun'dan oluşuyor. Araştırmadan çalışan prototipe kadar tüm sistemi iki kişi birlikte geliştirdik.

## 3. Proje özeti (0:35 - 1:28)

Kısaca: NSosyal akışına eklenecek, açılıp kapatılabilen bir sıralama katmanı öneriyoruz. Etkileşim odaklı akışlar yoğun ve olumsuz içeriği öne çıkarabiliyor, mevcut araçlar ise yalnızca süreye bakıyor. Amacımız kullanıcının haberden kopmadan akışı üzerinde kontrol sahibi olması. İçeriğin tonunu sunucuda, kişinin davranışını telefonunda ölçüyor; yoğunluk artınca sıradaki sayfada yoğun içeriğin payını azaltıyor ve her kararı açıklıyoruz. Bunu platformun mevcut yapay zekâ altyapısına önerilen bir uzantı olarak tasarladık.

**Dikkat:** Tablodaki her satırı okuma; "neden, amaç, nasıl, katkı" sırasıyla anlat. Ayrıntılar sonraki sayfalarda geliyor. T3 AI sorulursa: platformun spam ve bot mücadelesinde kullandığı yapay zekâ; erişimimiz yok, bizimki önerilen bir uzantı.

## 4. Problemin tanımı - neden bir sorun var (1:28 - 2:42)

Problemi "sosyal medya herkes için zararlı" diyerek kurmuyoruz. Birincisi, etkileşim olumsuzu ödüllendirebiliyor: yirmi iki bini aşkın randomize başlık testinde her ek olumsuz sözcük tıklanmayı artırmış. İkincisi, akışın kendisi duyguyu kaydırabiliyor: 689 bin kişilik bir deneyde akıştaki duygusal içerik değişince insanların kendi paylaşımlarının tonu da kaymış; çalışma rızasız yapıldığı için eleştirildi. Biz aynı mekanizmayı rıza ve açıklamayla koruma yönünde kullanıyoruz. Üçüncüsü, etki herkeste aynı değil: bir çalışmada pasif kullanımdan sonra katılımcıların yüzde 46'sı daha iyi, yüzde 10'u daha kötü hissetmiş. Türkiye'de de depremlerin ardından doomscrolling kaygıyla ilişkili bulundu. Bu yüzden herkese tek kural değil, kişiye göre doz.

## 5. Problemin tanımı - mevcut araçlar (2:42 - 3:39)

Bugün elimizde ne var ve ne işe yarıyor? Süre uyarısı veren bir uygulamayla yapılan randomize deneyde kullanım azaldı, ama iyi oluş, duygu durumu ve stres değişmedi. Akışı kronolojik yapmak da yedi haftalık bir deneyde yaşam doyumunu değiştirmedi. Tamamen bırakmanın etkisi küçük; içerik uyarıları ise beklenti kaygısını artırıyor. Hepsine bakınca şunu gördük: bu araçlar ya süreye ya konuya dokunuyor, hiçbiri içeriğin dozuna ve kişinin o anki durumuna bakmıyor. Kendimize sorduk: kullanıcıyı haberden koparmadan, sadece aynı yoğunluğun art arda gelmesini azaltabilir miyiz?

**Soru gelirse (slaytta yok, basın kaynağı):** Sızdırılan iç belgelere göre Facebook 2017-18'de öfke tepkisini beğeniden beş kat ağırlıklı saymıştı (WSJ, The Facebook Files, 2021). Platform tarafındaki teşviki göstermek için kullanılabilir, ama hakemli bir çalışma değil.

## 6. Çözüm önerisi - mottomuz ve çalışma prensibi (3:39 - 4:51)

Çıkarımımız şu oldu: süreyi kısmak da akışı kronolojiye çevirmek de yetmiyor; müdahale sıralamanın içinde ve içeriğin yoğunluğuna göre olmalı. Cevabımız, yani mottomuz: haberi saklamıyoruz, dozunu azaltıyoruz. Katman dört adımda çalışıyor. Önce ölçüyoruz: görünür kalma süresi, tepki, yorum ve tıklama; göz takibi yok. Sonra yorumluyoruz: içerik tonu, kişinin kendi okuma hızına göre oyalanması ve aktif tepkisi birlikte değerlendiriliyor, olası ruh hali de hesaba katılıyor; bu bir teşhis değil, olası bir örüntü. Üçüncüsü doz: eşik aşılırsa sıradaki sayfada yoğun içeriğin payı en fazla yüzde altmış azalıyor ve aralıklanıyor; elinizin altındaki sayfa oynamıyor. Dördüncüsü: her kartta "Neden bu?" var ve dengeleme kapatılabiliyor.

## 7. Çözüm önerisi - kontrol kullanıcıda (4:51 - 5:36)

Ne yapmadığımız da en az bu kadar önemli. İçerik silmiyor, hesap engellemiyoruz. Konuya, siyasete ya da inanca bakmıyoruz; yalnızca duygusal yoğunluğa bakıyoruz. Davranış verisi telefondan çıkmıyor. Kızdım ya da Gerildim dersen, Haberler aynı gelişmenin daha yapıcı bir anlatımını getiriyor; olayı gizlemiyoruz. Resmî ve acil duyurular muaf, kırılgan anı asla reklam için kullanmıyoruz. Sağdaki ekranda kullanıcı bir gönderinin neden ve kaç sıra aşağı indiğini görüyor.

## 8. Çözüm önerisi - ruh hali modeli ve uzman özeti (5:36 - 6:35)

Çözümün üçüncü parçası ruh hali modeli ve uzman özeti. Model son otuz dakikadaki ton, durma, tıklama ve tepkilerden beş olası ruh hali tahmin ediyor; sinirli ve yoğun payı dengeleme kararına yüzde otuz ağırlıkla giriyor. Sentetik veriyle eğitildiği için kendini sınıyor: arada bir "Şu an nasıl hissediyorsun?" diye soruyoruz, tahmini sormadan önce kaydedip cevapla karşılaştırıyoruz. Kullanıcı isterse bir uzmana götürebileceği yorumsuz bir özet oluşturuyor. Kişinin kendi duygu kayıtlarından geri bildirim almak depresyon tedavisinde belirtileri azaltmış; bizim özetimizin katkısı ise henüz test edilmedi.

**Soru gelirse:** Kişisel uyarlama ancak kişinin kendi cevaplarında (en az 6) varsayılandan daha iyi tuttuğu görülürse akışa bağlanır; kişisel ruh hali modeli yalnızca etiketleri değiştirir. Terapiste ilerleme verisi göstermek küçük ama anlamlı fayda sağlıyor (de Jong vd. 2021, d=0,15). Özet önce kişinin kendi bildirimlerini, sonra olası tahminleri ve sınırlılıkları verir.

**Dikkat:** "Tespit ediyoruz" deme, "olası" de; teşhis aracı değil. Kramer 2014 burada World Psychiatry'deki depresyon deneyi (I. Kramer vd.), 4. sayfadaki duygusal bulaşma çalışmasıyla karıştırma. Özet yapay zekâ yorumu içermez, cihazdan gönderilmez.

## 9. Teknik mimari (6:35 - 7:13)

Mimaride iki veri akışı var. Sunucu gönderi metninin tonunu bir kez hesaplıyor ve kırk sekiz aday gönderiyor. Kullanıcının görünür süreleri, tepkileri ve ilgi profili ise telefonda kalıyor; son sıralamayı cihaz yapıyor. Böylece ham davranışı merkezî bir havuza aktarmadan kişiselleştirme yapabiliyoruz. Kayıt on iki hafta tutuluyor; depolama kapalıysa sunucuya giden bir yedek yol yok.

## 10. Model ve veri kapsamı (7:13 - 8:49)

İşe hazır bir Türkçe duygu modeliyle başladık. Model kartında doğruluğu yüzde 95,4 yazıyordu. Güvenmek yerine, eğitimde görmediği bağımsız bir test setinde kendimiz ölçtük: yüzde 69,8 çıktı; model olumlu cümleleri olumsuz sanıyordu. Modeli üç tur yeniden eğittik; bugün ikili doğruluk yüzde 94, üç sınıflı yüzde 95,7, eğitim ve test verisi hiç kesişmiyor. Sonra gerçek haber başlıklarında bir kör nokta gördük. Model duygunun nasıl ifade edildiğini okuyor, olayın ağırlığını değil: "yangında üç işçi hayatını kaybetti" başlığında duygu kelimesi olmadığı için tek başına olumlu dedi. Modeli baştan eğitmek yerine ölüm, yangın, saldırı gibi açık olay sözcüklerinden bir liste ekledik; bu elle yazılmış bir kural ve tonu yalnızca aşağı çekebiliyor. Grafik iş bölümünü gösteriyor: haber başlıklarında olay sözcükleri, tweet ve yorumlarda model yakalıyor; ikisi birlikte her iki türde de en iyi sonucu veriyor. Etiketli 37 bin gerçek metinde doğruluğumuz yüzde 83.

**Soru gelirse:** Olay sözcüğü yapay zekâ değil, yaklaşık 45 kalıplık elle yazılmış bir kural listesi; sistem, öğrenen model ile kuralın birleşimi (hibrit). "Filtre" deme: gönderi kaldırılmaz, yalnızca tonu −0,9'a çekilir. Bedeli: normal tweetlerde yanlış işaret %16'dan %20'ye çıkıyor (film, dizi, mecaz). %83 sonucu sözlük dahil hesaplandı; tweetlerde sözlüğün katkısı çok küçük (%82 → %83). Doz dengeleme Ana Sayfa akışında çalışıyor; sözlük, akışa düşen haber hesabı gönderileri için gerekli. Haberler sekmesi ayrı bir özellik.

### Ölçümleri karıştırmayın (soru gelirse)

**Ton nasıl bir sayı?** Model her metin için −1 ile +1 arasında bir ton üretir: olumlu olasılığından olumsuz olasılığı çıkarılır. Akışta "yoğun" dediğimiz eşik −0,15. Doğruluk ise bu sürekli sayının değil, işaretinin ölçüsüdür: ton eksiyse olumsuz, artıysa olumlu deriz ve bunu veri setindeki etiketle karşılaştırırız.

**1. winvoker testi — %94,0.** Dışarıdan alınan, etiketleri hazır bir Türkçe duygu veri seti. Bin örnekten pozitif ya da negatif etiketli 630'unda ölçtük; eğitim verimizle kesişmiyor. Üç sınıflı doğruluk %95,7, nötr cümlelerde ortalama ton 0,005. Bu sayı metin tonunun doğruluğudur; haber başlığı ya da ruh hali doğruluğu değildir.

**2. 72.495 metinlik tarama.** On iki açık kaynaktan gerçek Türkçe metin. Modeli eğitmedik, sadece üzerinden geçirdik. Bu havuz ikiye ayrılıyor:

| Bölüm | Adet | Ne var | Ne öğreniyoruz |
|---|---:|---|---|
| Etiketli | 37.249 | Veri setinin kendi etiketi: saldırgan/normal, toksik/değil, yıldız puanı | **Doğruluk hesaplanabilir:** %83, yakalama %81, yanlış işaret %16, AUC 0,89 |
| Etiketsiz | 34.195 | Forum mesajları, RSS ve BBC haber başlıkları, TTC4900, Vikihaber | Doğruluk hesaplanamaz; yalnızca **ne sıklıkla yoğun dediğimizi** görürüz |

Etiketsiz kısım boşa değil, kör noktamızı orada bulduk: haber kaynaklarında model tek başına metinlerin yalnızca yüzde 3 ila 6'sına yoğun diyordu, oysa bu başlıkların çoğu ölüm, saldırı, yangın bildiriyordu. Olay sözcüğü desteğini bu yüzden ekledik; aynı kaynaklarda oran yüzde 18 ile 31'e çıktı. Forumda ise ikisi neredeyse aynı, yüzde 20 ve 22: orada işi model yapıyor. Yani etiketsiz havuz doğruluk ölçmez, sistemin gerçek bir akışta nerede sessiz kaldığını gösterir.

**3. 450 haber başlığı.** Haber başlıklarının doğru cevabı hiçbir veri setinde yoktu, biz elle etiketledik; sunumdaki 200 başlık bunun son bölümü. Güçlü olumsuz yakalama: yalnız model %12, yalnız sözlük %79, birlikte %82; isabet %90. Tek kişi etiketledi ve bu başlıklar sözlüğün geliştirilmesi sırasında görüldü, o yüzden bağımsız son ölçüm için yeni ve kör etiketli bir küme gerekiyor. Sonraki adımımız bu.

**Jüri "72 binde doğruluğunuz ne?" derse tek cümle:** "Doğruluk yalnızca etiketli kısımda ölçülür; 37.249 metinde yüzde 83 ve AUC 0,89. Kalan 34.195 metinde etiket yok, orada doğruluk değil işaretleme davranışı ölçülür; olay sözcüğü desteğine de zaten orada gördüğümüz açık yüzünden karar verdik."

## 11. Prototip (8:49 - 9:38)

Prototip çalışıyor: tasarım, kodlama ve testler tamam; NSosyal'e erişim olmadığı için entegrasyon yok, kullanıcı testi de henüz yapılmadı. Geliştirirken kendimizi sürekli ölçtük. İlk dengeleme yöntemimiz fiilen bir filtreydi, yoğun içeriği yüzde 96'ya kadar kesiyordu; biz sansür değil doz istiyorduk, değiştirdik. Uzun okuyanı yanlışlıkla riskli sayan modeli, kişiyi kendi hızıyla kıyaslayan modelle değiştirdik. Depolama kapalıyken verinin sunucuya gittiği yedek yolu kapattık. Hepsini 85 otomatik test koruyor.

**Dikkat:** Tabloyu okuma; her satırı bir cümlelik hikâye olarak anlat. %0,8 ve hızlı kaydırma sonuçları simülasyondan; "hiç yanlış yapmıyor" deme.

## 12. Uygulanabilirlik (9:38 - 10:13)

Üretime geçiş sunucuyu büyütmekten ibaret değil. İlk koşul platformun aday akışına erişim, ikincisi gerçek cihazlarda hız ve gizlilik denetimi. Sonra az sayıda gönüllüyle açıklamaların anlaşılıp anlaşılmadığını ölçeceğiz; başarı ölçütlerini baştan yazacağız. Bilgiye erişim ya da kullanıcı kontrolü zarar görürse büyütmek yerine düzeltmeye döneceğiz.

## 13. İş modeli (10:13 - 10:55)

İlk müşterimiz bireysel kullanıcı değil, bu özelliği akışına eklemek isteyen platform. Model üç adımdan oluşuyor: kapsamı belli ücretli bir pilot, ardından kurulum ve uyarlama, sonra yıllık bakım ve destek. Kullanıcıya ücret yok, duygu verisi satmak yok. Hibe ve sponsorluk başlangıç finansmanı; düzenli gelir hizmetten. Henüz müşterimiz yok; fiyatı uydurmak yerine entegrasyon emeği ve destek kapsamından hesaplayacağız. İlk somut teklifimiz NSosyal'da kontrollü bir pilot.

## 14. Özgünlük ve yerlilik (10:55 - 12:10)

Normalde sıralama nasıl çalışıyor? X'in açık kaynak koduna göre yaklaşık bin beş yüz aday için bir sinir ağı beğeni, yanıt, retweet gibi on etkileşim olasılığını tahmin ediyor. Hedef etkileşim; duygusal yoğunluk ayrı bir ölçüt değil. Akışı yeniden sıralayarak iyi bir etki arayan iki benzer deney bulduk. Biri karşı gruba tutumu biraz iyileştirdi; dokuz bin kişilik, altı aylık diğeri iyi oluşu değiştirmedi. İkisi de içeriğin düşmanca olup olmadığına baktı ve deney grubundaki herkese aynı kuralı uyguladı. Biz konuya değil duygusal yoğunluğa, herkese değil takılma görülen kişiye bakıyoruz; kararı da telefon veriyor. Taradığımız literatürde bunu yapan bir akış katmanına rastlamadık. Türkçe ince ayarı, olay sözlüğünü ve cihaz içi sıralamayı ekip olarak geliştirdik.

**Dikkat:** "Dünyada ilk" deme; "taradığımız literatürde rastlamadık" de. Benzer deneylerin siyasi yönünü öne çıkarma, farkı yöntemde anlat: neye bakıyor, kime uygulanıyor. Piccardi vd. 2025 (Science) ölçeği duygu durumu değil, karşı gruba tutum. X sütunu Mart 2023'te açık kaynak yapılan koda dayanıyor, bin beş yüz aday rakamı mühendislik blogundan. "Bugün de aynen böyle çalışıyor" deme; "açık kaynak koddaki adımlar" de. Rakip kötülemesi yapma, tasarım hedefi farkını anlat.

## 15. Uyarlamanın katkısı (12:10 - 13:08)

İlk aklımıza gelen çözüm herkese aynı dozdu. Bunu sınamak için on iki davranış profilinde, her birinde 150 sentetik kullanıcıyla on koşul çalıştırdık; toplam on sekiz bin simüle oturum, gerçek gönüllü değil. Sabit doz takılan kullanıcıda işe yarıyor, ama olağan okuru da yüzde 32 etkiliyor. Bizim sistem takılanlarda yoğun içerikte geçen süreyi yüzde 32 azaltırken olağan okurda yalnızca yüzde 6. Yani fark ne kadar azalttığımızda değil, ne zaman müdahale ettiğimizde. Ölçümde kendi ton etiketimizi kullandığımız için bunun bağımsız doğrulama olmadığını da söylüyoruz.

## 16. Hedef kitle ve etki (13:08 - 13:48)

Hedef kitlemiz bir tanı grubu değil; yoğun bir akışı takip ederken kontrol isteyen ve özelliği gönüllü açan yetişkinler. NSosyal, açıkladığı son rakama göre 1,7 milyonu aşkın kayıtlı kullanıcıya ulaştı. İlk pilotta beş ila on kişiyle açıklamaların anlaşılıp anlaşılmadığını ve önemli bilgiyi kaçırıp kaçırmadıklarını ölçeceğiz. Ruh sağlığına faydayı ise ancak etik onaylı, kontrollü bir çalışma gösterebilir.

**Dikkat:** 1,7 milyon kayıtlı kullanıcı: AA, 30.12.2025, platformun açıklaması. "Aktif" deme, kaynağı yok.

## 17. Takvim ve kapanış (13:48 - 14:13)

Bugün elimizde çalışan bir prototip, gerçek metin testleri ve tekrarlanabilir bir simülasyon var. Önceliğimiz modeli büyütmek değil, kullanıcıyla doğrulamak. Özetle: haberi saklamıyoruz, dozunu azaltıyoruz ve kontrolü kullanıcıya bırakıyoruz. Teşekkür ederiz.

## Ayrı 2 dakikalık demo

Demo açıkça hazırlanmış senaryo olarak tanıtılır. Canlı kullanıcının ruh halini tespit ediyormuş gibi anlatılmaz.

1. **0:00-0:20:** Akışı göster. “Bu, bağımsız NSosyal prototipimiz. Gösterim için hazırlanmış bir etkileşim senaryosu kullanıyoruz.”
2. **0:20-0:55:** Jüri demosunda dengelemeyi çalıştır. Aynı konudaki yoğun gönderilerin aralandığını göster. Normal kullanımda mevcut sayfanın değil sonraki sayfanın değiştiğini söyle.
3. **0:55-1:30:** “Neden bu?”yu aç. İlgi eşleşmesi, akış ayarı ve varsa olay sözcüğü açıklamasını göster. “Bu yüzde teşhis olasılığı değil, uygulamanın sıralama göstergesidir.”
4. **1:30-1:50:** Dengelemeyi kapat. Kontrolün kullanıcıda kaldığını göster. Gerçek kullanıcı kaydı bulunan bir cihazda “tamamen sıfırla” işlemi yapma.
5. **1:50-2:00:** “Ham davranış kaydı cihazda kalıyor. Bir sonraki aşamada bu deneyimi gönüllülerle ölçeceğiz.”

Demo açılmazsa: sunumdaki 11. sayfadaki gerçek prototip ekranları üzerinden aynı akışı anlatın. Henüz çekilmemiş videoyu hazırmış gibi söylemeyin.

## Jürinin sorabileceği kritik sorular

**İnsanlara fayda sağladığını gösterdiniz mi?**

Henüz gönüllülerde ölçmedik. Literatür tasarım gerekçesini, testler yazılımın belirli koşullardaki tutarlılığını, simülasyon ise sıralama davranışını destekliyor. Kullanıcıya etkisini kontrollü çalışmayla ölçeceğiz.

**72.495 metin varken neden 200 başlık?**

72.495 metnin tamamında model çıktısı ürettik. Bazı veri kümelerinin kendi etiketleri de var. Haber yoğunluğu için doğru cevabı ayrıca işaretlemek gerektiğinden 200 başlıkta ayrıntılı etiketli değerlendirme yaptık. Bu 200 başlığı bütün 72.495 metnin temsilcisi veya tamamının doğruluk testi saymıyoruz.

**Sadece sözlük kullanmış olmuyor musunuz?**

Haberde sözlük desteği baskın katkı sağlıyor. Etiketli tweetlerde ise yalnız sözlüğün yakalaması %7, modelin %82. Bu iki farklı içerik türünün farklı ihtiyacını birlikte karşılıyoruz. Sözlük bağlam hataları ve yanlış işaretleme getirebiliyor.

**Neden yapay zekâ, herkese aynı kural olmaz mı?**

Simülasyonda sabit doz hedef örüntüde benzer azaltma yaptı ama olağan profillere daha çok dokundu. Uyarlama, azaltmayı daha seçici zamanladı. Eş bütçeli rastgele karşılaştırma sonradan eklendi ve keşifsel. İnsanlarda üstünlük iddia etmiyoruz.

**%94 nerede geçerli?**

BERT v3 modelinin winvoker bağımsız testindeki ikili sınıflama sonucudur. Haber başlıkları, ruh hali tahmini veya kullanıcı faydası için geçerli bir doğruluk oranı değildir.

**Sistem kendi başarısını kendisi mi ölçüyor?**

Ana simülasyon ölçümü, sistemin içerik tonu etiketini kullanıyor. Bazı veri kümelerinde bağımsız saldırganlık/toksisite etiketleriyle kontrol yaptık ve benzer yön gördük. Bu etiketler de her zaman duygusal yoğunlukla aynı kavram değil. Haber ve forum içeriklerinin tümünde bağımsız etiket yok.

**Kullanıcının neye baktığını nasıl biliyorsunuz?**

Ekranda görünürlük oranı ve merkeze yakınlıkla tek kartın süresini izliyoruz. Bu göz takibi veya okunduğunun kanıtı değil. Sekme gizliyken süreyi durduruyoruz. Uzun video, dikkat dağınıklığı ve farklı okuma hızları hâlâ değerlendirilmesi gereken sınırlar.

**Ruh hali modeliniz dengelemeye katılıyor mu?**

Kişisel içgörü modeli sıralamayı yönetmiyor. Ancak mevcut varsayılan yoğunluk hesabında spiral olasılığına ek olarak varsayılan durum modelinin sinirli/anksiyete bileşenleri kullanılıyor. “Hiçbir ruh hali bileşeni yok” demiyoruz. Kişisel tahminle akış kararını birbirinden ayırıyoruz.

**Nasıl para kazanacaksınız?**

Platforma kapsamı belirli ücretli pilot, kurulum/entegrasyon ve yıllık bakım öneriyoruz. Ücret kullanıcıdan değil hizmeti alan platformdan gelecek. Henüz ödeme isteğini doğrulamadık. Fiyatı entegrasyon emeği, içerik analizi maliyeti ve destek kapsamı belirleyecek. Hibe ve sponsorluğu başlangıç finansmanı olarak görüyoruz.

**Platform bunu neden kendi yapmasın?**

Yapabilir. Değer önerimiz bir fikir satmak değil, çalışan cihaz içi modülü, test altyapısını ve pilot ölçüm paketini birlikte teslim ederek entegrasyon denemesini kolaylaştırmak. Bu değerin satın alma kararına dönüşüp dönüşmediği müşteri görüşmesi ve pilotla sınanacak.

**18.000 oturum gerçek kullanıcı mı?**

Hayır. 12 profil, profil başına 150 sentetik kullanıcı ve 10 koşul var. Aynı sentetik kullanıcı bütün koşulları yaşadığı için 18.000 bağımsız kişi yok. Duygu veya iyi oluş simüle ederek insan etkisini kanıtlamıyoruz.
