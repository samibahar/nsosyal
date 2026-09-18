# 20 Eylül: rakam haritası ve soru-cevap çalışma notu

Sunum `NSosyal_Final_Sunum_v18.pdf` (17 sayfa) içindir; sayfa numaraları ona göredir. Konuşma metni: `20eylul_sunum_konusma.md`.
Kural: söylediğimiz her rakam slaytta da var; rakamı söylerken o sayfadaki tabloyu, grafiği ya da dipnotu gösteriyoruz.

## 1. Rakam haritası

Her rakam için: nerede duruyor, neyi ölçüyor, neyi ölçmüyor. "Ne ölçmez" sütunu, yanlış söylenirse en çok zarar veren kısımdır.

| Rakam | Sayfa ve yeri | Ne ölçer | Ne ölçmez / dikkat |
|---|---|---|---|
| 22.743 başlık testi, olumsuz sözcük başına tıklama +%2,3 | 4, tablo | Olumsuz dilin tıklamayı artırdığı (Robertson vd. 2023, randomize) | Bizim ürünümüzü değil |
| 689 bin kişi | 4, tablo | Akıştaki duygusal içerik değişince kullanıcının yazdığı tonun kaydığı (Kramer, Guillory, Hancock 2014, PNAS) | Hissedilen duyguyu değil, yazılan dili; rızasız olduğu için eleştirildi |
| %46 daha iyi, %10 daha kötü | 4, tablo | Pasif kullanımdan sonra etkinin kişiden kişiye değiştiği (Beyens vd. 2020) | Ortalama bir zarar ya da fayda değil |
| 4.965 kişi, 7 hafta | 5, tablo | Kronolojik ve algoritmik akış arasında yaşam doyumu farkı çıkmadı (Gauthier vd. 2026, Nature) | Makalenin asıl konusu siyasi; biz yalnız iyi oluş bulgusunu kullanıyoruz |
| 22 dk, %37, g=0,25, 23 deney | 5, tablo | Süre sınırı, açılışta bekleme, bırakma ve kullanım müdahalelerinin literatürdeki sonuçları | Bizim ürünümüzü değil |
| En fazla %60 azaltma, 0,6 | 6, tablo ve dipnot | Dozun üst sınırı: hedef pay = taban × (1 − 0,6 × yoğunluk) | Optimize edilmiş ya da kişiye göre değişen bir sayı değil; seçilmiş üst sınır |
| %23 → en fazla 3; %13 → en fazla 2 | 6, dipnot | 48 adayın üçte biri yoğunsa, yoğunluk 0,5 ve 1'de 12'lik sayfada kalan yoğun gönderi | Kalanlar silinmez, sonraki sıralara aralıklanır |
| 10 gönderi kaydı | 6, tablo | Dengelemenin başlaması için oturumdaki en az kayıt sayısı | "10 roket" ya da "10 uzun bakış" değil (aşağıda B2) |
| 1,5 sn | 6, tablo | Bunun altındaki bakış okuma sayılmaz, takılma kanıtına girmez | Göz takibi değil |
| %70 / %30 | 8, tablo | Dengeleme kararı: %70 takılma modeli, %30 ruh hali modelinin sinirli + yoğun payı | Psikolojik bir sabit değil; tasarım parametresi |
| 4.000 ve 24.960 oturum | 8, tablo | Takılma modelinin eğitildiği ve sistemin sınandığı simüle oturumlar | Gerçek kullanıcı değil. 24.960 = 18.000 + 3.600 + 3.360 |
| F1 0,70 | 8, tablo | Ruh hali modelinin sentetik test setindeki başarısı | Gerçek insanda doğruluk değil |
| %20 | 8, tablo | Beş seçenekte rastgele tahminin eşleşme oranı (kıyas tabanı) | Bizim başarımız değil |
| 6 cevap | 8, tablo | Kişisel takılma kalibrasyonunun akışa bağlanması için en az cevap (ve daha düşük Brier hatası) | |
| 102 kişi; 58 çalışma, d=0,15 | 8, alt başlık ve dipnot | Kendi duygu kayıtlarından geri bildirim ve terapiste ilerleme verisi göstermenin faydası | Bizim uzman özetimizin etkisi değil; o test edilmedi |
| 48 aday, 12 gönderi | 9, tablo (6'da da) | Sunucunun gönderdiği aday sayısı ve telefonun seçtiği sayfa | |
| %95,4 → %69,8 | 9, sürüm tablosu | Hazır modelin kart iddiası ve bizim bağımsız testimizdeki sonucu | |
| %94,3 / %93,3 / %94,0 (üç sınıfta %95,7) | 9, sürüm tablosu | v1, v2, v3'ün genel Türkçe (winvoker, 630 örnek) doğruluğu | Haber başlığı ya da ruh hali doğruluğu değil |
| 0,83 / 0,91 / 0,96 / 0,00 | 9, sürüm tablosu | Nötr metinlerde ortalama ton; 0 ideal (nötre nötr diyebiliyor mu) | |
| %82 / %21 / %71 / %12 → sistem %82 | 9, sürüm tablosu | 200 gerçek başlıkta güçlü olumsuzu yakalama | Tek kişi etiketledi; küme geliştirmede görüldü |
| %50 / %43 / %47 / %16 → sistem %20 | 9, sürüm tablosu | Normal tweetlerde yanlış işaret | |
| %83, AUC 0,89, 37.249 | 10, büyük rakam | Etiketli gerçek metinlerde olumsuzluk ayrımının doğruluğu (olay sözcüğü dahil) | "Sarsıcı olay" doğruluğu değil; etiketler saldırgan / düşük puan |
| 72.495, 34.195 etiketsiz | 10, büyük rakam | Taranan gerçek metin; etiketsiz kısımda doğruluk hesaplanamaz | "72 binde doğruluk" diye bir sayı yok |
| Haber %12 / %79 / %82; tweet %82 / %7 / %83; toksik %83 / %9 / %85 | 10, grafik | Yalnız BERT / yalnız olay sözcüğü / ikisi birlikte yakalama | Tweetlerde işi model yapıyor, haberde sözlük |
| +0,41 → −0,90 | 10, örnek kutusu | "Yangında 3 işçi hayatını kaybetti": yalnız BERT ve olay sözcüğü ile ton | |
| %96 | 11, tablo | Eski "puandan ceza" yönteminin ilk sayfadaki yoğun payı ne kadar kestiği | Bugünkü yöntem değil (bugün −%35 / −%47 / −%62) |
| %62 → %0,8 | 11, tablo | Uzun okuyanda yanlış alarm, eski ve yeni takılma modeli (simülatör) | Gerçek kullanıcı değil |
| %23–34 → 0 | 11, tablo | Hızlı kaydırmanın yanlışlıkla dengelenmesi | |
| 62 → 0 ihlal, 85 test | 11, tablo ve üst satır | Otomatik erişilebilirlik denetimi, otomatik test sayısı | Erişilebilirlik sertifikası değil; "85 kişide fayda" değil |
| ≈5 ms, 14 KB, ≤4 MB, ≈140 milyon | 12, ölçtüklerimiz | Telefonda sayfa kararı süresi, model boyutu, yerel kayıt üst sınırı, tek GPU'nun günlük kapasitesi | Telefon süresi gerçek cihazda ölçülmedi (aşağıda G) |
| ~1.500 aday, 10 etkileşim olasılığı | 14, tablo | X'in Mart 2023 açık kaynak koduna göre sıralama | ~1.500 koddan değil X blogundan; "bugün de böyle" deme |
| 1.256 kişi / 9.386 kişi | 14, dipnot | Benzer iki yeniden sıralama deneyinin büyüklüğü | |
| 18.000; −%31,6 / −%5,7; −%33,0 / −%32,1; 4,80 / 8,02 | 15, tablo | Üç kollu simülasyon: uyarlanan ve sabit doz, hedef ve olağan profiller, oturum başına müdahale | Gerçek kişi değil; ölçüm sistemin kendi ton etiketiyle |
| 1,7 milyon | 16, hedef kullanıcı | NSosyal'in açıkladığı kayıtlı kullanıcı sayısı (AA, 30.12.2025) | Aktif kullanıcı değil |
| 5–10 kişi | 16 ve 17 | İlk kullanılabilirlik pilotu | Etki ya da fayda kanıtı değil |

## 2. Soru-cevap

### A. Yapay zekâ nerede, BERT ve olay sözcüğü (sayfa 9–10)

**Projede yapay zekâ nerede?** Üç öğrenen model var: BERT (derin öğrenme dil modeli, sunucuda metnin tonu), takılma modeli (lojistik regresyon, telefonda) ve ruh hali modeli (SGD sınıflandırıcı, telefonda). Olay sözcüğü desteği yapay zekâ değil, yaklaşık 45 kalıplık elle yazılmış bir kural listesi. Sistem hibrit.

**BERT nasıl çalışıyor?** Cümleyi parçalara bölüp sayıya çeviriyor; her kelime cümledeki bütün kelimelere bakarak (12 katman) anlamını güncelliyor; en sonda olumsuz, nötr, olumlu olasılıkları çıkıyor. Ton = olumlu − olumsuz, −1 ile +1 arası. Türkçeyi büyük bir metin yığınından öğrenmiş hazır bir tabanın üstüne üç tur kendi ince ayarımızı yaptık.

**"3 işçi hayatını kaybetti"ye neden +0,41?** Model duygunun ifadesini okuyor, olayın ağırlığını değil. Eğitimdeki olumsuz örnekler çoğunlukla "rezalet, berbat" gibi duygu kelimeli şikâyetler; olgusal haber dilinde duygu kelimesi yok. Aynı cümlede "öldü" dersen −0,92, "maalesef… üzgünüz" eklersen −0,98 veriyor.

**Sözlük her şeyi mi yapıyor?** Hayır. Saldırgan tweetlerin %82'sini model tek başına yakalıyor, sözlük tek başına %7'sini; sözlük eklenince %83. Sözlüğün katkısı haber başlıklarında: %12'den %82'ye.

**Neden "filtre" demiyoruz?** Sözlük gönderiyi kaldırmıyor, yalnızca tonunu −0,9'a çekiyor; doz da gönderiyi silmiyor, aralıklıyor.

### B. Takılma modeli (sayfa 8)

**B1. Birinin takıldığını nasıl anlıyorsunuz?** Son 30 dakikada, yoğun tonlu gönderilerde kişinin kendi diğer gönderilerine göre ne kadar uzun kaldığına bakıyoruz (göreli oyalanma, katsayı +1,56). Roket ve yorum riski düşürüyor (−0,85). Her şeyi yavaş okuyan birinde oyalanma sıfıra yakın çıkar: kişiyi başkasıyla değil kendisiyle kıyaslıyoruz. Beklenen okuma süresi = 1,5 sn + kelime sayısı / 3,5.

**B2. "10 gönderi kaydı" ne demek?** Ekranda tek başına odakta kalan her gönderi bir kayıt (süresiyle birlikte); tıklama, roket ve yorum da o kayda eklenir. Oturumda 10 kayıt olmadan dengeleme başlamaz. 1,5 saniyenin altındaki bakışlar kayıt sayısına girer ama takılma kanıtı sayılmaz.

**B3. Neden yorum yazan kişi daha az dengeleniyor?** Tasarım gereği: takılma "pasif" kalmayı arıyor, roket ya da yorum riski düşürüyor. 14.09'da gerçek gönderilerle kurduğumuz oturumlarda, saldırgan tweetlerde pasif takılan senaryoda dengeleme %100 başladı; aynı içerikte yorum yazan senaryoda %29. Gerekçe: aktif tartışma edilgen tüketimle aynı örüntü değil. Bu bir varsayım; gerçek kullanıcıda sınanmadı.

**B4. Sentetik veriyle kendi hipotezinizi mi öğrettiniz?** Kısmen evet, bunu saklamıyoruz: simülatör hipotezlerimizi kodluyor. Bu yüzden model kendini kullanıcıya sorarak sınıyor; kişisel kalibrasyon en az 6 cevapta varsayılandan daha iyi tutmadan akışa bağlanmıyor. Gerçek doğruluk pilotun konusu.

**B5. Eşikler neden 0,28 ve 0,58?** Tasarım parametresi: 0,28 dengeleme, 0,58 bildirim. Literatürden türetilmedi. Maliyeti: gerçek gönderilerle kurulan oturumlarda olağan okumada da %12 dengeleme başlıyor.

**Not:** "36 bin oturum" deme; belgelerimizde yok. Belgeli olan: eğitim 4.000, sınama 18.000 + 3.600 + 3.360 = 24.960.

### C. Doz (sayfa 6)

**Formülü örnekle anlat.** Sayfa 6'nın dipnotunu göster: 48 adayın üçte biri yoğunsa, yoğunluk 0,5'te hedef pay %23'e iner, 12'lik sayfada en fazla 3 yoğun gönderi kalır; yoğunluk 1'de %13, en fazla 2.

**0,6 neden?** Taradık: yoğunluk 0,6'da α 0,3 → 0,9 arası yoğun pay −%37 → −%63 azalıyor, yoğun gönderilerin ilk 3 sayfada kalması %60 → %33'e düşüyor. 0,6 ikisinin ortasında; kişiye göre değişmiyor.

**Resmî ya da acil bilgi?** Hesap listesiyle dengelemeden muaf; "Gerildim" tepkisiyle de itilmez.

### D. Veri ve KVKK (sayfa 7, 9)

**Sunucuya ne gidiyor?** Sayfa isteği (oturum kimliği ve aday sayısı), kullanıcının yazdığı gönderi ve yorum, takip. **Gitmeyen:** durma süresi, tıklama, roket, ilgi profili, takılma ve ruh hali tahminleri, "Şu an nasıl hissediyorsun?" cevapları. Tarayıcı yerel depolamaya izin vermezse kişiselleştirme kapanır, veri yine gitmez (e2e testi istek sayısını kontrol ediyor).

**KVKK?** Çıkarılan ruh hali sağlık verisi gibi özel nitelikli sayılabilir (KVKK md. 6; 7499 sayılı kanunla 1.6.2024'te değişti). Başka bir işleme şartı olmadığı için açık rıza alıyoruz: ilk açılışta eşit ağırlıklı Açık / Kapalı. Kayıt telefonda 12 hafta (en fazla 20.000 olay), tek tuşla silinir. Kurumun Özel Nitelikli Kişisel Veriler Rehberi (26.02.2025) karşısında en temkinli yolu seçtik. Gerçek entegrasyonda veri sorumlusu platform olur.

### E. Ruh hali modeli ve kendini sınama (sayfa 8)

**Ne yapıyor?** Son 30 dakikadaki ton, durma, tıklama, roket ve yorumdan beş olası ruh hali: sakin, mutluluk, umut, sinirli, yoğun. Tek gönderiden değil pencereden hesaplanıyor (en az 3 kayıt). Sinirli + yoğun payı dengeleme kararının %30'u.

**Nasıl sınanıyor?** "Şu an nasıl hissediyorsun?" en az 12 kayıttan sonra, 8 kayıtta bir ve en az 20 dakika arayla soruluyor; "Geç" var. Önce tahmin kaydediliyor, sonra cevap alınıyor, sonra model öğreniyor. Eşleşme İçgörü ekranında rastgele (%20) ve "hep en sık cevap" tabanıyla yan yana.

**Brier hatası nedir?** Tahmin edilen olasılık ile gerçek cevap (0 ya da 1) arasındaki farkın karesi; küçük olan daha iyi.

**Kişisel model sıralamayı değiştiriyor mu?** Kişisel ruh hali modeli yalnızca etiketleri değiştiriyor. Akışı yalnızca kişisel takılma kalibrasyonu etkileyebilir; o da en az 6 cevapta daha düşük Brier hatası göstermeden bağlanmıyor.

**Zayıf yanı?** Kendi simülasyonumuzda ruh hali katkısı olağan forum okumada dozu %20 artırıyordu. Kaldırmadık, çünkü bunu yalnız simülasyonla değil gerçek cevaplarla karar vermek gerekiyor; pilotun konusu.

### F. Uzman özeti (sayfa 8)

İçerik sırası: kişinin kendi bildirimleri (tarih, saat, gün dilimi), 12 haftaya kadar haftalık seyir, gönüllü tepkiler, "olası" diye işaretli model tahmini, sınırlılıklar. Yapay zekâ ile metin yazılmıyor; cihazdaki sayılar düzenleniyor, kullanıcı kopyalayıp kendisi götürüyor. Dayanak: kendi duygu kayıtlarından geri bildirim (I. Kramer vd. 2014), terapiste ilerleme verisi (de Jong vd. 2021), klinisyen görüşü (Yoo vd. 2021). Davranıştan tahmin edilen ruh halinin tedaviye katkısı test edilmedi. Bu Kramer, 4. sayfadaki duygusal bulaşma çalışmasının Kramer'i değil.

### G. Entegrasyon, hız ve yer (sayfa 12)

**Platforma nasıl takılır?** Platform 48 adayı ve tonu verir (API), sıralama modülü uygulamanın içine girer. Prototip web; mobil uygulamaya taşınması gerekiyor. NSosyal API erişimimiz yok.

**Telefonda ne kadar yer, ne kadar hız?** Modeller 14 KB. Yerel kayıt olay başına ~205 bayt, en fazla 20.000 olay: ~4 MB. Sayfa kararı (yerel kaydı okuma + takılma + ruh hali + 48 adayın dozlu sıralaması) bizim bilgisayarda 1,6 ms; işlemci 4 kat yavaşlatılınca 4,4 ms, 6 kat yavaşlatılınca 6,3 ms. Geekbench tek çekirdek puanına göre (bizim işlemci Ryzen 9 7940HS 2.130, Samsung Galaxy A15 / Helio G99 628, oran 3,4) Galaxy A15'te ≈5 ms. Gerçek cihazda ölçmedik; bunu "canlı için gereken" sütununda yazıyoruz.

**Telefonun GPU'su kullanılıyor mu?** Hayır; telefondaki hesap işlemcide. GPU yalnızca sunucuda, BERT için.

**Sunucu maliyeti?** Ton her gönderi yayımlanınca bir kez hesaplanır; okuyan kişi sayısı maliyeti artırmaz. Dizüstü RTX 4060'ta saniyede 1.619 gönderi (günde ~140 milyon), işlemcide saniyede 60 (günde 5,2 milyon). NSosyal'in günlük gönderi sayısını bilmiyoruz; tahmin etme.

### H. Rapordan bu yana ne değişti (jürinin elinde rapor var)

| Raporda | Şimdi | Neden |
|---|---|---|
| İlgi skoru + refah cezası ("puandan ceza") | Doz: yoğun payı hedefe indirilir, gönderi aralıklanır | Ceza yöntemi yoğunluk 0,85'te ilk sayfadaki yoğun payı %96 kesiyordu: yoğun gönderiler neredeyse tamamen ilk sayfadan düşüyor, sayfada nötr ve olumlu içerik kalıyordu. Filtre gibi çalışıyordu, biz doz istiyorduk (bugün −%35 / −%47 / −%62) |
| Model v2, %93,3 | Model v3, %94,0 (üç sınıfta %95,7) | v2 nötr metne de kesin karar veriyordu; normal tweetlerin %47'sini işaretliyordu |
| Olay sözcüğü desteği yok | Var | Gerçek haber başlıklarında güçlü olumsuzun yalnız %6–12'si yakalanıyordu |
| Takılma modeli v1 | v2: kişiyi kendi okuma hızıyla kıyaslıyor | Uzun okuyanda %62 yanlış alarm → %0,8 |
| Hızlı kaydırma kanıt sayılıyordu | 1,5 sn altı kanıt sayılmıyor | Hızlı kaydırmaların %23–34'ü yanlışlıkla dengeleniyordu |
| İsteğe bağlı LLM destekli haftalık rapor anlatılıyordu (arayüze bağlı değildi) | Sunumda yok; yalnızca yapay zekâsız, yorumsuz uzman özeti | Davranış verisi dış bir servise gitmesin |
| "Veri cihazdan çıkmaz" diyordu, ama depolama kapalıyken yedek yol veriyi sunucuya gönderiyordu (11.09'da bulundu) | Yedek yolda kişiselleştirme yok, veri gitmiyor; test ediliyor | Raporun iddiasını kodda da doğru kılmak |

Raporda olup prototipte olmayanlar: üretici paneli, koruyucu reklam ilkesi (NSosyal'de reklam yok, ilke olarak söyleniyor).

### I. Simülasyon (sayfa 15)

Kullanıcıları biz tanımladık; bu yüzden sonuç "sistem tasarladığımız gibi davranıyor" demek, "insanlara iyi geliyor" demek değil. Ölçüm sistemin kendi ton etiketiyle. Gerçek etki pilotta ve kontrollü çalışmada ölçülecek. Sistem sabit değil: kişiyi kendi okuma hızıyla kıyaslıyor ve onun cevaplarıyla kalibre oluyor.

### J. "İyi geliyor mu?" ve pilot (sayfa 16–17)

İddiamız "daha kontrol edilebilir akış", iyi oluş değil. Sıranın ve olumsuz içeriğin duyguyu etkilediğine literatürde kanıt var; en zayıf halka dozun etkisi. Benzer müdahalelerde etkiler küçük (d ≈ 0,02 ile g = 0,25 arası). İlk pilot 5–10 yetişkin, 2–3 gün: "Neden bu?"yu anlama, kapatma, gereksiz müdahale hissi, bilgiye erişim; kişi başı en az 5, toplam 40+ cevap. Sonraki etki araştırması: etik değerlendirme, güç analizi, kontrol grubu. Durdurma koşulu: bilgiye erişim ya da kullanıcı kontrolünde kritik sorun.

### K. Siyasi ya da dini içerik (sayfa 7)

Konuya bakmıyoruz; nötr tonlu siyasi ya da dini içerik hiç dozlanmaz. Yalnızca yoğun tonlu gönderiler (ton < −0,15) aralıklanır, konusu ne olursa olsun: öfkeli bir spor tweeti de aynı muameleyi görür. Dürüst not: yoğun olay haberleri gündemde daha sık. TTC4900 haber kümesinde yoğun sayılan pay: gündem (siyaset + dünya) %33, sağlık %16, teknoloji %14, sanat %12, ekonomi %10, spor %8. Nedeni konu değil, ölüm, saldırı, savaş gibi olay sözcükleri; bu gönderiler de silinmiyor, yalnızca aralıklanıyor.

### L. Haberler sekmesi (sayfa 7)

Prototipte "Kızdım" ya da "Gerildim" deyince aynı gelişmenin daha yapıcı anlatımı öne geliyor; ama bu içerikler demo için elle hazırlandı. Gerçek üründe aynı olayı farklı kaynaklarda eşleştirmek gerekiyor; bu henüz yapılmadı, gelecek iş. Doz dengeleme Haberler'de değil Ana Sayfa akışında çalışıyor.

### M. Yerlilik (sayfa 14)

"Sıfırdan yerli model" iddiamız yok. Yerli yönümüz:
- Türkçe haber diline özgü geliştirme: haber üslubu verisi, üç tur ince ayar, Türkçe olay sözlüğü. Hazır modeller Türkçe haber dilinde kör (sürüm tablosu).
- Dışa bağımlılık yok: model platformun kendi sunucusunda çalışıyor, yabancı bir yapay zekâ servisine (API) veri gitmiyor; davranış verisi telefonda kalıyor.
- Yerli bir platform (NSosyal) için tasarlandı; T3 AI'ya önerilen bir uzantı.
- Hazır olan: BERTurk tabanı ve üstündeki açık Türkçe duygu modeli. Lisans uygunluğu üretim öncesi denetlenecek.

### N. İş modeli (sayfa 13)

Müşteri platform, kullanıcı değil: ücretli pilot, kurulum, yıllık bakım. Kullanıcıya ücret ve veri satışı yok. Fiyat yok; entegrasyon emeği, içerik analizi maliyeti (sayfa 12'de ölçtük) ve destek kapsamından hesaplanacak.

## 3. Konuşma metnindeki soru ve dikkat notları

### Sayfa 3: Proje özeti

**Dikkat:** Tablodaki her satırı okuma; "neden, amaç, nasıl, katkı" sırasıyla anlat. Ayrıntılar sonraki sayfalarda geliyor. T3 AI sorulursa: platformun spam ve bot mücadelesinde kullandığı yapay zekâ; erişimimiz yok, bizimki önerilen bir uzantı.

### Sayfa 5: Problemin tanımı - mevcut araçlar

**Soru gelirse (slaytta yok, basın kaynağı):** Sızdırılan iç belgelere göre Facebook 2017-18'de öfke tepkisini beğeniden beş kat ağırlıklı saymıştı (WSJ, The Facebook Files, 2021). Platform tarafındaki teşviki göstermek için kullanılabilir, ama hakemli bir çalışma değil.

### Sayfa 8: Çözüm önerisi - davranış modelleri ve uzman özeti

**Soru gelirse:** Kişisel uyarlama ancak kişinin kendi cevaplarında (en az 6) varsayılandan daha iyi tuttuğu görülürse akışa bağlanır; kişisel ruh hali modeli yalnızca etiketleri değiştirir. Terapiste ilerleme verisi göstermek küçük ama anlamlı fayda sağlıyor (de Jong vd. 2021, d=0,15). Özet önce kişinin kendi bildirimlerini, sonra olası tahminleri ve sınırlılıkları verir.

**Dikkat:** "Tespit ediyoruz" deme, "olası" de; teşhis aracı değil. Kramer 2014 burada World Psychiatry'deki depresyon deneyi (I. Kramer vd.), 4. sayfadaki duygusal bulaşma çalışmasıyla karıştırma. Özet yapay zekâ yorumu içermez, cihazdan gönderilmez.

### Sayfa 9: Teknik mimari ve model sürümleri

**Soru gelirse:** v2 neden kullanılmadı? Haber başlığında %71 yakalıyor ama normal tweetlerin %47'sini işaretliyor; akışın yarısını dengelerdi. v1'in %94,3'ü neden v3'ün %94,0'ından yüksek? İkisi de yalnız olumlu/olumsuz ayrımı; v1 haber başlığında %21 yakalıyor, normal tweette %43 yanlış işaret veriyor, nötr metne de kesin karar veriyor. Tablo 18.09.2026'da aynı testlerle ölçüldü, eğitim yapılmadı. Ham davranış kaydı cihazda 12 hafta tutulur.

### Sayfa 10: Model ve veri kapsamı

**Soru gelirse:** Olay sözcüğü yapay zekâ değil, yaklaşık 45 kalıplık elle yazılmış bir kural listesi; sistem, öğrenen model ile kuralın birleşimi (hibrit). "Filtre" deme: gönderi kaldırılmaz, yalnızca tonu −0,9'a çekilir. Bedeli: normal tweetlerde yanlış işaret %16'dan %20'ye çıkıyor (film, dizi, mecaz). %83 sonucu sözlük dahil hesaplandı; tweetlerde sözlüğün katkısı çok küçük (%82 → %83). Doz dengeleme Ana Sayfa akışında çalışıyor; sözlük, akışa düşen haber hesabı gönderileri için gerekli. Haberler sekmesi ayrı bir özellik.

### Sayfa 11: Prototip

**Dikkat:** Tabloyu okuma; her satırı bir cümlelik hikâye olarak anlat. %0,8 ve hızlı kaydırma sonuçları simülasyondan; "hiç yanlış yapmıyor" deme.

### Sayfa 14: Özgünlük ve yerlilik

**Dikkat:** "Dünyada ilk" deme; "taradığımız literatürde rastlamadık" de. Benzer deneylerin siyasi yönünü öne çıkarma, farkı yöntemde anlat: neye bakıyor, kime uygulanıyor. Piccardi vd. 2025 (Science) ölçeği duygu durumu değil, karşı gruba tutum. X sütunu Mart 2023'te açık kaynak yapılan koda dayanıyor, bin beş yüz aday rakamı mühendislik blogundan. "Bugün de aynen böyle çalışıyor" deme; "açık kaynak koddaki adımlar" de. Rakip kötülemesi yapma, tasarım hedefi farkını anlat.

### Sayfa 16: Hedef kitle ve etki

**Dikkat:** 1,7 milyon kayıtlı kullanıcı: AA, 30.12.2025, platformun açıklaması. "Aktif" deme, kaynağı yok.

## 4. Ölçüm notları (10. sayfa için)

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

## 5. Jürinin sorabileceği kritik sorular

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
