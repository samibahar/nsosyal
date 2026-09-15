# Bilimsel dayanak, kanıt zinciri ve ölçüm çerçevesi

*15.09.2026. İki ayrı literatür değerlendirmesinin birleşimi. Temel metin, yalnızca doğrulama turundan geçmiş kaynaklarla kurulan kanıt zinciridir; üzerine ikinci bir bağımsız değerlendirmeden ölçüm çerçevesi, karşı kanıtlar ve ölçüm sınırları eklendi ve o değerlendirmeden alınan kaynakların künyeleri ayrıca kontrol edildi. İki değerlendirmenin aynı sonuca varması yararlı bir tutarlılık kontrolüdür; ürünün etkisine iki bağımsız deney kanıtı değildir. Sunumdaki Ek 4 bu belgeye dayanır.*

---

## Kısa cevap

Evet, kurabiliriz. Ama ortaya çıkan şey bir kanıt olmaz; mekanizmaya dayanan dolaylı bir çıkarım zinciri olur. Psikoloji ve medya psikolojisi deneyleri iki şeyi destekliyor: olumsuz ya da sarsıcı içerik kısa vadede duyguyu kötüleştiriyor, ruh hali ile içerik seçimi arasında da literatürün desteklediği olası karşılıklı bir ilişki var. Bu da katmanımızın **neden** var olduğunu sağlam biçimde temellendiriyor. Buna karşılık akış içinde yoğun içerik dozunu kısmen azaltmanın duyguya etkisini doğrudan sınayan bir çalışma bulamadık. En yakın dolaylı kanıtlarda (Kramer vd. 2014; kullanım azaltma deneyleri) etkiler küçük ya da tutarsız. **Etkinin büyüklüğü ve kimlerde oluşacağı henüz bilinmiyor.** Dürüst iddiamız şu: tasarım literatürle tutarlı. Asıl gerekçesi, kullanıcının istemediği yoğunlaşmayı geri alınabilir biçimde yönetmesine destek olmak ve kontrolü ona bırakmak. Kullanıcıya sağladığı faydayı ayrı bir katılımcı çalışmasıyla sınamamız gerekiyor.

---

## Dört başarıyı karıştırmayalım

| Başarı düzeyi | Cevapladığı soru | Bizdeki kanıt | Tek başına cevaplayamadığı soru |
|---|---|---|---|
| Yazılım doğruluğu | Kural tasarlandığı gibi mi çalışıyor? | 85 otomatik test, tarayıcı ile Python hesabının eşitliği | Kural kullanıcı için faydalı mı? |
| Tahmin doğruluğu | Metin ya da davranış etiketi doğru mu? | winvoker testinde %94; 450 elle etiketli başlık; etiketli sosyal veri setleri (hepsi güncel sözlük için görülmüş) | Doğru tahmine göre müdahale etmek iyi mi? |
| Akış davranışı | Yoğun içeriğin payı ve süresi değişiyor mu? | 600 senaryo; kapalı döngü ve üç kollu simülasyon | İnsan kendini daha iyi hissediyor mu? |
| Kullanıcı etkisi | Yük, kontrol ve bilgilenme nasıl değişiyor? | **Yok**; ayrı bir katılımcı çalışması gerekiyor | Kalıcı klinik etki var mı? |

"85 test geçti" ile "85 kişide fayda gösterdik" aynı kanıt değildir. 72 bin metinde modeli çalıştırmak veri hacmini gösterir, bu metinlerin hepsinde doğruluk ölçülmüş olmaz. Simülasyondaki kullanıcı davranışını biz tanımladığımız için sistemin simülasyonda başarılı olması bağımsız bir psikolojik doğrulama değildir. Daha güçlü bir yapay zekâ kullanmak bu mantıksal bağımlılığı ortadan kaldırmaz.

---

## Zincire genel bakış

| # | Öncül | Kanıtın gücü | Sistemdeki karşılığı |
|---|---|---|---|
| 0 | Tespit sinyali anlamlı bir şey yakalıyor | **Zayıf–orta** | "Olası spiral" sinyali, kişisel okuma hızı tabanı, EMA kalibrasyonu |
| 1 | Olumsuz/sarsıcı içerik kısa vadede duyguyu kötüleştirir | **Güçlü** (kısa vadede), genellenebilirliği dar | Katmanın var olma gerekçesi; konudan bağımsız, yoğunluğa bakan ölçüm |
| 2 | Etkileşim sinyalleri yüksek uyarılmalı içeriği ödüllendirir | **Orta** (akış düzeyinde zayıf) | Doz sınırı ve dengeleme |
| 3 | Ruh hali ile içerik seçimi arasında olası karşılıklı ilişki; olumsuza takılmak ruminasyonla bağlantılı | Kısa vadede **orta–güçlü**, "döngü" iddiası **zayıf** | 30 dakikalık pencere, müdahalenin bir sonraki sayfada devreye girmesi |
| 4 | Dozu azaltmak, ikame etmek ve aralıklamak zararı hafifletir | **En zayıf halka** | En fazla %60 azaltma, aralıklama, Haberler'deki yapıcı anlatım |
| 5 | Şeffaflık, kontrol ve öz-izleme kabulü ve farkındalığı destekler | **Orta** (bağlam aktarımı dolaylı) | "Neden bu?", kapatma hakkı, İçgörü ekranı, EMA |

---

## Zincir

### Halka 0: Tespit sinyali. "Olumsuz içerikte uzun ve pasif kalmak" bir şey söylüyor mu?

**İddia:** Kişi kendi okuma hızına göre olumsuz tonlu içerikte belirgin biçimde uzun ve pasif kalıyorsa, bu o anki olumsuz ruh halinin *olası* bir işareti olabilir. Tek başına güvenilir bir gösterge sayılmaz.

**Kanıt:**
- **Soroka, Fournier ve Nir (2019):** 6 kıtada 17 ülkede yapılan bir deney. Gerçek video haberlerde olumsuz habere karşı fizyolojik uyarılma (deri iletkenliği) ülkeler arasında tutarlı biçimde daha güçlüydü ve bireyler arası fark belirgindi. Olumsuz içerikte uzun kalmak, herkeste görülebilen olağan bir olumsuzluk yanlılığı da olabilir. Bu da sinyali yanlış pozitife açık bırakıyor.
- **Godard ve Holtzman (2024):** 141 çalışmalık bir meta-analiz (N≈145.000). Aktif ya da pasif kullanım ile ruh sağlığı arasındaki ilişkilerin çoğu ihmal edilebilir düzeyde (|r|<.10). Pasif kullanım yalnızca genel sosyal medya bağlamında daha kötü duygusal sonuçlarla ilişkili. Aktif kullanım ise iyi oluşla (r=.15) olduğu gibi kaygıyla da (r=.12) pozitif ilişkili.
- **Valkenburg, van Driel ve Beyens (2022):** 40 anket çalışmasını inceleyen bir kapsam derlemesi. Çalışmaların çoğu "aktif iyi, pasif kötü" varsayımını desteklemiyor. Yazarlar içeriğin tonuna, kişinin o anki ruh haline ve bireysel duyarlılığa bakılmasını öneriyor.
- **Beyens vd. (2020):** Ergenlerle yapılan bir ESM çalışması (2.155 anlık ölçüm). Pasif kullanımdan sonra ergenlerin %46'sı daha iyi hissetti, %44'ünde değişim olmadı, %10'u daha kötü hissetti. Kişiye özgü tahminler gürültülü, bu oranlar kesin sınıflar gibi okunmamalı.
- **de Hoog ve Verboon (2020):** N=63, 10 gün boyunca günde 5 ölçüm alınan bir EMA çalışması. Haberin olumsuz algılandığı anlarda daha çok olumsuz, daha az olumlu duygu bildirildi. İlişkiyi haberin kişisel önemi düzenledi; nevrotiklik düzenlemedi. İlişki eş zamanlı ölçüldüğü için ters yön dışlanamıyor.
- **Shen vd. (2025):** Telefon ve giyilebilir cihazlarla pasif algılama üzerine 42 çalışmalık bir kapsam derlemesi. 32 çalışmada N<100, 19'unda izlem 7 günden kısa ve yalnızca birinde dış doğrulama var. Alan umut verici, ama doğrulama bakımından zayıf; başka sensörlerdeki başarılar bizim kaydırma sinyalimize aktarılamaz.
- *Davranışın anlamı belirsiz:* Uzun bekleme yavaş okuma, erişilebilirlik ihtiyacı ya da dikkat dağınıklığı olabilir; tepki vermemek ilgisizlik demek değildir. Yakınını ilgilendiren bir haberi dikkatle okuyan kişi ile istemeden aynı temaya tekrar tekrar dönen kişi benzer ekran davranışı üretebilir.

**Kanıtın gücü: Zayıf–orta.** Sinyalin parçaları (ton, kişiye özgülük, anlık bağlam) literatürde tek tek anlamlı. Ama bizim birleşik sinyalimizin duyguyu ne kadar isabetle yakaladığı hiç sınanmadı ve yanlış pozitif oranı bilinmiyor. Dikkat yanlılığı kanıtı (Bar-Haim vd. 2007: 172 çalışma, kaygılı bireylerde d=0,45) milisaniye düzeyindeki laboratuvar görevlerine dayanıyor. Bu kanıtı kaydırma sırasındaki durma süresine taşımak bir çıkarım olur.

**Sistemdeki karşılığı:** Sinyal tek başına pasifliğe dayanmıyor; olumsuz ton, yoğunluk, kişinin kendi okuma hızı ve pasiflik birlikte aranıyor. Bu yapı Godard/Valkenburg uyarısıyla ve Beyens'in bireysel farklılık bulgusuyla uyumlu. Sinyal "olası spiral" diye adlandırılıyor, teşhis dili kullanılmıyor. EMA sorusu sinyali sürekli sınıyor.

---

### Halka 1: Olumsuz ya da sarsıcı içerik kısa vadede duyguyu kötüleştirir

**İddia:** Olumsuz ya da sarsıcı medya içeriğine kısa süre maruz kalmak, hemen ardından ölçülen duyguyu kötüleştiriyor; bu etki sosyal medya biçiminde de görülüyor.

**Kanıt:**
- **Hopwood ve Schutte (2017):** Yalnızca deneysel çalışmaları kapsayan bir meta-analiz (18 çalışma, N=1.634). Felaket ve şiddet içeren medyadan sonra olumsuz psikolojik sonuçlar görüldü (Hedges g=1,61) ve etki kaygıda özellikle güçlüydü. Etki "en azından geçici"; süresi bilinmiyor. *g=1,61 alışılmadık büyüklükte ve felaket materyalinden geliyor. Buradan etkinin büyüklüğünü değil yönünü almalıyız.*
- **Buchanan, Aknin, Lotun ve Sandstrom (2021):** İki ön kayıtlı deney. Çalışma 1'de Twitter akışı kullanıldı (N=299, en az 2 dk), Çalışma 2'de YouTube videosu (N=603, 4–4,5 dk). COVID haberi, içerik görmeyen kontrol grubuna göre olumlu duyguyu düşürdü (η²=.03 ve .06, küçük–orta). Çalışma 1'de olumsuz duygu ve iyimserlik değişmedi. Çalışma 2'de iyimserlik düştü. Olumsuz duyguda koşullar arasında genel bir fark vardı, ancak bu farkın bir kısmı iyilik koşulundaki daha düşük olumsuz duygudan geliyor; haber ile kontrol arasındaki ikili fark doğrulanmadı. En güvenli okuma: **olumlu duyguda kısa süreli düşüş.**
- **Johnston ve Davey (1997):** 14 dakikalık olumlu, nötr ve olumsuz TV bültenleriyle yapılan bir laboratuvar deneyi. Olumsuz bülteni izleyenlerde kaygılı ve üzgün duygu durumu arttı, haberle ilgisi olmayan kişisel bir endişeyi felaketleştirme eğilimi de yükseldi. Çalışma eski, örneklemi küçük; N özette yok.
- **Shaikh, McGowan ve Lydon-Staley (2024):** 203 kişi, 14 gün, telefonla EMA. Günde bir kez iyi ya da kötü haber verilen deneysel bölümde olumlu haber olumlu duyguyu artırıp olumsuz duyguyu azalttı, olumsuz haber tersini yaptı; günlük yaşamdaki haber tüketiminde de aynı ilişki görüldü. İkinci değerlendirmenin aktarımına göre haberin etkisi bir sonraki EMA ölçümüne anlamlı biçimde taşınmadı ve koşul sırası herkeste aynıydı. Anlık etki için güçlü bir gerekçe, kalıcı etki için değil.
- **Ai ve von Mühlenen (2025):** N=128. Kişinin kendi gönderisine gelen olumsuz yorumlar kaygıyı artırdı, duygu durumunu düşürdü. *Uyarı: Bu, kişiyi hedef alan olumsuz geri bildirim. Başkalarının olumsuz içeriğini pasif biçimde okumakla aynı şey değil.*

**Tamamlayıcı gözlemsel kanıt:** Holman, Garfin ve Silver (2014), Boston saldırısından sonra N=4.675 kişiyle çalıştı: günde 6 saat ve üzeri maruziyet yüksek akut stresle ilişkiliydi (b=15,61). Çalışma kesitsel ve bütün medya türlerini tek bir toplam saatte birleştiriyor. Ata, Sarıtaş Arslan ve Murat Mehmed Ali (2026), Kahramanmaraş depremlerinden sonra Türkiye'de N=418 kişiyle kesitsel bir çalışma yaptı. Toplam sosyal medya süresi çoklu modelde **anlamlılığını yitirdi**, uyanır uyanmaz kontrol etme gibi kullanım örüntüleri daha belirleyiciydi. Bu çalışma basit "daha çok süre, daha çok zarar" savını destekleyen bir kanıt değil, en fazla karışık kanıt sayılır.

**Kanıtın gücü: Kısa vadede güçlü, genellenebilirliği dar.** Birden çok deney ve bir meta-analiz aynı yönü gösteriyor. Sınırlar şunlar:
- Deneylerin hepsi %100 olumsuz içeriği kontrolle karşılaştırıyor. Karışık bir akışta olumsuzun payının kısmen azalması sınanmadı.
- Uyaranlar dakikalarca süren TV ya da video. Tek tek kaydırılan kısa gönderilerle aynı şey değil.
- Etkiler hemen ölçüldü; ne kadar kalıcı olduğu bilinmiyor.

**Sistemdeki karşılığı:** Katmanın var olma gerekçesi bu halka. Katman konudan bağımsız çalışıyor ve yalnızca duygusal yoğunluğa bakıyor. Böylece bu literatürde zararın kaynağı olarak görünen tona odaklanıyor.

---

### Halka 2: Etkileşim sinyalleri yüksek uyarılmalı içeriği ödüllendirme eğiliminde

**İddia (düzeltilmiş hâli):** "Akışlar olumsuzu büyütür" demek yerine şunu söylüyoruz: tıklama ve paylaşım gibi etkileşim sinyalleri, **yüksek uyarılmalı**, çoğu zaman olumsuz tonlu içeriği ödüllendirebilir. Etkileşimi en üst düzeye çıkarmaya çalışan bir sıralayıcının bunu büyütmesi *makul bir dolaylı çıkarım*.

**Kanıt:**
- **Robertson vd. (2023):** Upworthy'de yapılmış 22.743 randomize başlık testinin analizi (370 milyonu aşkın gösterim). Her ek olumsuz kelime tıklanmayı **göreli olarak** yaklaşık %2,3 artırdı. Temel tıklanma oranı düşük olduğu için mutlak fark küçük. Test edilen şey akış sıralaması değil başlık seçimi; iyi oluş ölçülmedi.
- **Berger ve Milkman (2012):** New York Times makalelerinin e-postayla paylaşımı. Olumlu içerik genel olarak daha çok paylaşıldı, ama asıl belirleyici uyarılma düzeyiydi. Hayranlık, öfke ve kaygı paylaşımı artırdı; düşük uyarılmalı hüzün azalttı. Bu bulgu "etkileşim eşittir olumsuzluk" basitleştirmesini düzeltiyor.
- **Soroka vd. (2019):** Olumsuz habere verilen fizyolojik uyarılma ülkeler arasında daha güçlü. Ölçülen şey uyarılma, duygu değil.
- **Kramer, Guillory ve Hancock (2014):** Duygusal bulaşma üzerine N=689.003 kişilik bir saha deneyi. Akıştan olumsuz gönderiler çıkarılınca kullanıcıların yazdığı olumsuz kelime oranı d=0,02 düştü. Ölçülen şey hissedilen duygu değil, yazılan dil (LIWC). Çalışma onam alınmadığı için PNAS'ın "Editorial Expression of Concern" notunu aldı.
- *Yalnızca bağlam (siyasi, ana öncül değil):* Milli vd. (2025), ön kayıtlı bir algoritma denetiminde etkileşim temelli sıralamanın duygusal yüklü içeriği büyüttüğünü bildirdi. Çıktılar siyasi olduğu için bu çalışmayı dayanak yapmıyoruz.

**Kanıtın gücü: Orta.** Olumsuz ya da uyarılmalı içeriğin tıklama ve paylaşımı artırdığına dair nedensel kanıt var. Buna karşılık siyasi olmayan içerikte **akış sıralamasının** olumsuzu büyüttüğünü doğrudan gösteren bir kanıt yok. Bulaşma bulgusu da çok küçük.

**Sistemdeki karşılığı:** Doz sınırımız "olumsuz" içeriği değil "yoğun tonlu" içeriği hedefliyor, yani düzeltilmiş öncüle birebir uyuyor. Berger ve Milkman'ın bulgusu, hayranlık uyandıran olumlu içeriğin de etkileşim getirebildiğini gösteriyor. Buradan dozu dengelemenin etkileşimi mutlaka düşürmeyeceği *düşünülebilir*. Bu spekülatif bir çıkarım; Kramer'deki çekilme etkisi ters yönde bir işaret veriyor (bkz. Riskler).

---

### Halka 3: Ruh hali ile içerik seçimi arasında olası karşılıklı ilişki; olumsuza takılmak ruminasyonla bağlantılı

**İddia:** Olumsuz ruh hali insanı olumsuz içeriğe yöneltiyor, olumsuz içerik de ruh halini kötüleştiriyor. Kısa vadede iki yön de deneysel olarak gösterildi. Bu ilişkinin zaman içinde kendini besleyen bir döngüye dönüştüğü ise doğrudan izlenmedi.

**Kanıt:**
- **Kelly ve Sharot (2025):** Dört çalışma, n=1.145. Daha olumsuz tonlu web içeriğinde gezinmek daha kötü ruh haliyle ilişkiliydi. Gezinilen içeriği manipüle etmek ruh halini, ruh halini manipüle etmek de seçilen içeriğin tonunu değiştirdi. İçeriğin duygusal etkisini görünür kılan bir müdahale gezinme örüntüsünü değiştirdi ve ruh halini kısa vadede iyileştirdi. Sınırlar: iki nedensel bağlantı ayrı kısa deneylerde sınandı. Bağlam, algoritmik akış değil kullanıcının kendi seçtiği web gezinmesi. Etki büyüklükleri özette yok, saha ilişkileri küçük olarak nitelendiriliyor. Bağımsız bir tekrar henüz bilinmiyor.
- **Thompson, Jones, Holman ve Silver (2019):** Üç yıllık bir boylamsal çalışma (N=4.165). Saldırıyla ilgili medya maruziyeti 6 ay sonra travma sonrası stres belirtilerini, bu belirtiler 2 yıl sonra gelecek endişesini, endişe de sonraki bir saldırıda daha fazla medya tüketimini ve akut stresi öngördü. Çalışma gözlemsel, zaman ölçeği ise **yıllar**; bizim 30 dakikalık oturum ölçeğimizle örtüşmüyor. Holman 2014 ile aynı araştırma grubundan geliyor, bu yüzden bağımsız bir tekrar sayılmaz.
- **Nolen-Hoeksema (2000):** İleriye dönük bir çalışma. Ruminasyon sonraki depresif bozuklukları, yeni başlayan epizotları ve kaygı belirtilerini öngördü. Başlangıç belirtileri kontrol edildiğinde kronikliği öngörmedi.
- **Webb, Miles ve Sheeran (2012):** 306 deneysel karşılaştırmayı kapsayan bir meta-analiz. Olayın duygusal yönüne odaklanmak ("concentration") duygu düzenlemede ters etki yaptı (d+=−0,26). Bu sonuç ruminasyonla birebir aynı değil, ama "takılıp kalmanın" neden sorun olduğuna dair bir mekanizma sağlıyor.
- **Visted, Vøllestad, Nielsen ve Schanche (2018):** Mevcut ya da geçmiş depresyonda duygu düzenlemeyi inceleyen bir meta-analiz. Ruminasyon, kaçınma ve diğer düzenleme örüntülerinde grup farkları var. Kaydırma davranışından ruminasyon çıkarılamaz. Kaçınma da bir sorun olabileceği için olumsuzu sürekli uzaklaştırmak savunulamaz.
- **Yoon, Verona, Schlauch, Schneider ve Rottenberg (2020):** 38 depresyon tanılı ve 38 sağlıklı kadın. Depresyon grubu hüzünlü müziği daha çok seçti, ama gerekçesi hüznü artırmak değil, bu müziği sakinleştirici ve düşük enerjili bulmaktı. Olumsuz ton ile olumsuz etki aynı şey değil.
- **Webb, Lindquist, Jones, Avishai ve Sheeran (2018):** Ortam seçimi, duygularını düzenlemekte zorlanan kişilerde özellikle yararlı bir düzenleme stratejisi. Buradaki seçim kişinin kendisine ait; bir algoritmanın onun adına sıralamayı değiştirmesi aynı şey değil.
- *Türkiye bağlamı:*
  - **Satici, Gocet Tekin, Deniz ve Satici (2023):** Türkçe Doomscrolling Ölçeği'ni geliştirdi (üç kesitsel örneklem).
  - **Kartol, Üztemur ve Yaşar (2023):** 6 Şubat depremlerinden 3 ay sonra 402 depremzedeyle yapılan kesitsel bir çalışma. Psikolojik sıkıntı arttıkça doomscrolling de arttı; bu ilişkide gelecek kaygısı aracı değişken çıktı.
  - **Özmen (2026):** Depremden yaklaşık bir yıl sonra 255 üniversite öğrencisiyle, 6 ay arayla iki dalgalı boylamsal bir çalışma. Deprem korkusu ile belirsizliğe tahammülsüzlük arasındaki ilişkide doomscrolling ve kaygı ardışık aracı değişkenlerdi.
  - Bu çalışmaların hiçbiri "döngü kanıtı" değil; öz-bildirime dayanan ve iki yönlü ilişkiyle tutarlı bulgular. Özmen'in iki dalgalı tasarımı kesitsel çalışmalardan biraz daha güçlü, ama örneklem öğrenci ve bağlam afet sonrası.

**Kanıtın gücü:** Kısa vadeli iki yönlü ilişki için **orta–güçlü**, ama kanıt tek bir yeni çalışmaya dayanıyor. "Kendini besleyen döngü" iddiası **zayıf**. "Pasif uzun durma, ruminasyon demektir" köprüsü bizim varsayımımız; doğrudan sınanmadı. Medya psikolojisindeki "ruh hali yönetimi" yaklaşımı, kötü ruh halinin insanı onarıcı içeriğe yönelteceğini öngörür. Kelly ve Sharot'ta ise olumsuz ruh hali olumsuz içeriğe yöneltiyor. Bizim yorumumuza göre kendiliğinden onarım her zaman işlemiyor ve bu, dışarıdan yumuşak bir desteğin gerekçesi olabilir. *Bu uzlaştırma kaynaklarda doğrulanmadı.*

**Sistemdeki karşılığı:** Katman yalnızca "olası spiral" penceresinde devreye giriyor. Müdahale mevcut içeriği değiştirmiyor, bir sonraki sayfada devreye giriyor. Böyle karşılıklı bir ilişki varsa, ona maruziyet noktasında yumuşak ve geri alınabilir bir karşılık vermeyi hedefliyor.

---

### Halka 4: Dozu azaltmak, ikame etmek ve aralıklamak zararı hafifletebilir (en zayıf halka)

**İddia:** Yoğun tonlu içeriğin payını azaltmak ve araya daha sakin içerik koymak, Halka 1'deki kısa vadeli zararı *hafifletebilir*. Bu doğrudan sınanmış bir bulgu değil, bir çıkarım.

**Önce bir kategori hatası:** Bu alanda en çok atıf alan çalışmalar toplam kullanım süresini azaltıyor ya da platformu bıraktırıyor. Bizim sistemimiz ise süreyi değil, içeriğin **tonunu ve dozunu** değiştiriyor. Akıştaki olumsuz oranı parametrik olarak değiştirip (ör. %20/%50/%80) oturum içinde duyguyu ölçen bir deney doğrulanmış bulgular arasında yok.

**Bizim müdahalemize en yakın saha örneği:** Kramer vd. (2014). Akıştan olumsuz gönderi çıkarmanın etkisi d=0,02 çıktı ve yalnızca kelime düzeyinde ölçüldü. Bu çalışma aynı anda **hem destek hem uyarı**: yön doğru, ama etki çok küçük.

**Dolaylı mekanizma kanıtları:**
- **İkame (aynı konu, farklı ton):** Buchanan vd. (2021). Aynı genel konuda (COVID) iyilik içeriği olumlu duyguyu düşürmedi; Çalışma 2'de olumsuz duygu kontrol grubundan düşüktü. Olumlu duyguyu kontrolün **üstüne** çıkardığı ise gösterilmedi. Bu yüzden "iyi gelir" değil, "ilgili deneyin ölçtüğü sonuçlarda kötüleşme görülmedi, olumsuzu azaltabilir" demeliyiz.
- **Toparlanma ("undoing" etkisi):** Fredrickson, Mancuso, Branigan ve Tugade (2000), iki çalışma (n=170 ve n=185). Kaygı uyandıran bir durumdan sonra huzur ya da eğlence filmi izleyenler, nötr ya da üzücü film izleyenlere göre daha hızlı kardiyovasküler toparlanma gösterdi. Ölçülen fizyolojik toparlanma, uyaran film. Bu bulgu aralıklamanın kuramsal dayanağı olabilir.
- **Duygunun sönme süresi:** Kuijsters vd. (2016), N=30. Deneyle oluşturulan duygu logaritmik biçimde sönüyor: statik resimde yaklaşık 2 dakika, kısa filmde yaklaşık 6 dakika, uzun kaygı filminde 8 dakikaya kadar sürüyor. Gillies ve Dozois (2021), N=401: yöntemden bağımsız olarak etki 4 dakikadan uzun sürmedi. Buradan iki sonuç çıkıyor. Tek bir gönderinin etkisi dakikalar içinde sönüyor, yani gerekçemiz tek tek gönderiler değil, **birikimli maruziyet** olmalı. Aralıklama bu birikimi önlemeye yönelik makul bir yol.
- **Duygu düzenlemesi üzerinden bir benzetme:** Webb vd. (2012)'de dikkat dağıtma d+=0,27, duygusal yöne odaklanma d+=−0,26 çıktı. "Pasif takılma" odaklanmaya, "aralıklama" dışarıdan desteklenen bir dikkat dağıtmaya benzetilebilir. *Bu bir kanıt değil, benzetme.* Deneylerde stratejiyi katılımcı kendisi uyguluyor.
- **Yeniden çerçeveleme (Haberler özelliğini destekler, akıştaki doz azaltmayı değil):** McIntyre ve Lough (2023), 19 çalışmadaki 22 deneyi derledi: yapıcı haberin okur duygusunu etkilediği net, en belirgin kazanım olumlu duyguda. Overgaard (2021), N=492: olumlu ya da yapıcı başlıklar olumsuz başlıklara göre daha az öfke ve kaygı yarattı. Aynı deneyin kurum raporunda (Overgaard ve Stroud 2020) güven, tıklama isteği ve haberden uzaklaşma isteğinde fark görülmedi; grafik görseller kaygıyı ve risk algısını artırdı. Daha düşük risk algısı her zaman daha doğru algı demek değildir. Overgaard (2023), n=270: yapıcı gönderiler olumlu duyguyu ve öz-yeterliği artırdı. Karşı nüans olarak van Venrooij, Sachs ve Kleemans (2022), 9–13 yaş arası N=468 çocukla: yapıcı haber olumsuz duyguyu azalttı, ama öz-yeterlik aracı değişken çıkmadı ve bağış da azaldı.
- **Kullanım azaltma (yalnızca üst sınır emsali):**
  - May, Malouff ve Meynadier (2025): 10 RCT, N=1.491. Depresif belirtide g=0,25, yani **küçük** bir etki. Sınırlama ile bırakma arasındaki fark anlamlı değil.
  - Allcott, Gentzkow, Wittenbrink vd. (2025): 6 hafta devre dışı bırakma. Facebook'ta 0,060 SD, Instagram'da 0,041 SD; **çok küçük**. Hakemsiz bir çalışma makalesi ve seçim dönemine ait.
  - Lambert vd. (2022): N=154, 1 haftalık ara. İyi oluş (WEMWBS) +4,9. Tasarım kör değil ve izlem kısa.
  - Ferguson (2025): d=0,088, anlamlı değil. Thrul vd. (2025) aynı veriyi yeniden analiz etti: bir haftadan kısa müdahaleler d=−0,175 ile kötüleşmeyle, bir hafta ve üzeri müdahaleler d=0,156 ile iyileşmeyle ilişkili.
  - Allcott, Gentzkow ve Song (2022): sınır aracı kullanımı günde 22 dakika azalttı, ama öznel iyi oluşa etkisi +0,04 SD ile anlamlı değildi.
- **Karşı ve karışık kanıtlar:**
  - Longpré vd. (2021): 62 genç yetişkin. Olumlu haber, nötr habere göre stres tepkisi, bellek ya da duygulanımda üstünlük göstermedi. "Olumlu eklemek mutlaka iyi gelir" varsayımına karşı bir bulgu; küçük örneklemde fark bulunmaması eşdeğerlik kanıtı değil.
  - Cook, Cai ve Wohn (2022): 387 içerik moderatörü, her 20 gönderide bir mola. Molaya olumlu görsel koymak stresi azaltmadı; deneyimli moderatörlerde görselli molalarda daha çok yorgunluk ve sıkıntı görüldü. Moderasyon sıradan bir akış değil ve atama tam rastgele gerçekleşmedi, ama araya olumlu uyaran koymanın ters tepebileceğine yakın bir uyarı.
  - Plackett, Blyth ve Schartau (2023): 23 deneysel çalışmanın sistematik derlemesi. 9'u olumlu, 7'si karışık, 7'si sonuçsuz; 23 çalışmanın 22'si düşük kaliteli ve çoğu kısa süreli.
  - Wellspent deneyi (Mertens vd. 2026; Brockmeier vd. 2025): kişiselleştirilmiş uyarılarla kullanım süresi ve bazı sorunlu kullanım ölçümleri iyileşti; iyi oluş, duygu ve streste zaman × grup etkileri anlamlı değildi. Aynı deneyin iki yayını olduğu için iki bağımsız kanıt sayılmaz. Kullanımın azalması ile psikolojik yarar farklı sonuçlardır.

**Kanıtın gücü: Zayıf.** Doğrudan bir test yok ve dolaylı emsaller küçük etkiler gösteriyor. Güçlü taraf şu: ikame ve yapıcı anlatımda, ilgili deneylerin ölçtüğü sonuçlarda kısa vadede kötüleşme görülmedi ve olumsuz duygu azalabildi. Karşı taraf şu: araya olumlu içerik eklemek tek başına yarar sağlamayabilir (Longpré vd. 2021; Cook vd. 2022).

**Sistemdeki karşılığı:** Azaltma en fazla %60; hiçbir içerik silinmiyor; ilgi alanı korunuyor ve aynı ilgi alanındaki daha az yoğun içeriğe kayılıyor; yoğun gönderiler aralıklanıyor; Haberler sekmesinde aynı olayın yapıcı ya da farklı bir anlatımı öneriliyor.

---

### Halka 5: Şeffaflık, kontrol ve öz-izleme

**İddia:** Kısa ve net bir açıklama, küçük ama gerçek bir kontrol payı ve hafif bir öz-izleme, müdahalenin kabulünü ve kullanıcının farkındalığını destekleyebilir. Açıklama yapmak da etkiyi büyük olasılıkla ortadan kaldırmaz.

**Kanıt:**
- **Dietvorst, Simmons ve Massey (2018):** Üç çalışma. Katılımcılar kusurlu bir algoritmanın tahminlerini *biraz* bile değiştirebildiklerinde onu belirgin biçimde daha sık kullandı ve daha memnun kaldı.
- **Kizilcec (2016):** Bir MOOC'ta yapılan saha deneyi. Orta düzeyde şeffaflıkta beklenti ihlali ile güven arasında bir ilişki yoktu. Düşük (r=−0,59) ve yüksek (r=−0,55) şeffaflıkta ise ilişki olumsuzdu. Buradan "az ama net" ilkesi çıkıyor. Bağlam not verme, duygusal bir akış değil.
- **Bruns vd. (2018)** ve **Loewenstein, Bryce, Hagmann ve Rajpal (2015)**: Açıkça bildirilen varsayılan seçenekler etkisini korudu. Bruns'ta şeffaflık reaktansla etkileşime girmedi. İki çalışma da tek seferlik karar paradigmasına dayanıyor.
- **Carpenter (2013):** 42 çalışmalık bir meta-analiz. Kişiye reddetmekte özgür olduğunu hatırlatmak çoğu bağlamda uyumu artırdı. Yazar bunu reaktanstan çok öz-sunumla açıklıyor.
- **Barsova, Cheong, Mak ve Liu (2022):** 598 Facebook kullanıcısıyla kesitsel bir anket. Unfollow ve bildirim ayarlarını kullananlarda depresyon, kaygı ve stres puanları daha düşüktü. Snooze, Off-Facebook Activity ve süre araçları ise daha düşük belirtilerle ilişkili değildi; ikinci değerlendirmenin tam metin aktarımına göre tartışma bölümünde Snooze kullananlarda daha yüksek belirti puanları bildiriliyor. Kesitsel olduğu için araçların belirtileri artırdığı ya da azalttığı söylenemez; zorlanan insanlar belirli araçlara daha çok başvuruyor olabilir.
- **Milton, Runningen, Terveen, Kaur ve Chancellor (2026):** Ruh sağlığı sorunları bildiren 21 katılımcıyla tasarım atölyeleri (özet "tanı almış" diyor, yöntem öz-tanıyı da kabul ediyor). Katılımcılar, algoritmanın niyetlerini ve bağlamlarını yakalamadığını anlattı ve daha açık kontrol istedi. Nitel bir tasarım çalışması; tedavi ya da etkinlik deneyi değil.
- **Öz-izleme:** Kauer vd. (2012), bir RCT'nin ikincil analizi (114 genç). Duygusal öz-farkındalık üzerinden depresif belirtilerde dolaylı bir azalma bulundu (GA −6,366 ile −0,029, üst sınır sıfıra çok yakın). Hunt vd. (2018)'de kaygının iki grupta da düşmesi öz-izlemeye bağlanıyor, ancak bu yorum sınanmadı.
- **Duyguyu adlandırma:** Torre ve Lieberman (2018), duyguyu sözcüğe dökmenin örtük bir düzenleme işlevi gördüğünü öne sürüyor. Fan vd. (2019), 74.487 Twitter kullanıcısında açıkça olumsuz duygu bildiren bir tweet'ten sonra tonun hızla eski düzeyine döndüğünü gözlemledi; çalışma gözlemsel. **Karşı bulgu:** Nook, Satpute ve Ochsner (2021), N=80 ve N=60: duyguyu önce adlandırmak, ardından yapılan yeniden değerlendirmenin ve bilinçli kabulün etkisini zayıflattı. Bu bulgu Haberler akışımıza doğrudan dokunuyor, çünkü orada kullanıcı önce "Kızdım/Gerildim" diyor, sonra ona yeniden çerçevelenmiş içerik sunuluyor. Fark şurada: Nook'ta yeniden değerlendirmeyi **kişi kendisi üretiyor**, bizde ise içerik **dışarıdan sunuluyor**. Bu fark sınanmadı.

**Kanıtın gücü: Orta.** Yön tutarlı, ama bağlamlar (tahmin görevleri, not verme, varsayılan seçenekler) duygusal bir akıştan farklı. Sürekli akan bir akışta tekrar tekrar gösterilen açıklamaların etkisi sınanmadı.

**Sistemdeki karşılığı:** "Neden bu?" açıklaması kısa tutuluyor. Kullanıcı katmanı kapatabiliyor. İçgörü ekranı öz-farkındalık raporu sunuyor. EMA sorusu seyrek soruluyor, bir "Geç" seçeneği var ve modelin tahmini kullanıcıya önceden gösterilmiyor. İsteğe bağlı uzman özeti yorum içermiyor.

---

## Çıkarım: ne söyleyebiliriz, ne söyleyemeyiz

**Söyleyebileceklerimiz**
- Olumsuz ya da sarsıcı içeriğin kısa vadede duyguyu kötüleştirdiği deneysel olarak iyi destekleniyor. Katman bu bilinen riskin etrafında tasarlandı.
- Ruh hali ile içerik seçimi arasında literatürün desteklediği olası karşılıklı bir ilişki var; kısa vadede iki yön de ayrı deneylerde gösterildi. Müdahalenin "olumsuza takılma" örüntüsünde devreye girmesi bu bulguyla **tutarlı**.
- Etkileşim sinyalleri yüksek uyarılmalı içeriği ödüllendirme eğiliminde. Yoğunluğa bakan bir denge katmanı bu mekanizmaya **makul** bir karşılık.
- Aynı konuda daha az yoğun ya da yapıcı içeriğe kaymakta, ilgili deneylerin ölçtüğü sonuçlarda kısa vadede kötüleşme görülmedi. Yapıcı anlatım öfke ve kaygıyı azaltabildi. Bu yüzden ilgi alanını koruyan ikame ve Haberler özelliği **beklenen yönde**.
- Kısa bir açıklama ve küçük bir kontrol payı kabulü artırabilir. Açıklama yapmak müdahalenin etkisini büyük olasılıkla yok etmez.
- **Etkinin büyüklüğü ve kimlerde oluşacağı henüz bilinmiyor.** En yakın emsallerde etkiler küçük ya da tutarsız; bunu baştan açıkça söylüyoruz.
- Simülasyonda uyarlanan doz, müdahaleyi herkese aynı sabit kurala göre takılan kullanıcılarda daha çok yoğunlaştırıyor. Bu teknik bir ek katkıdır, insan yararı değildir.

**Söyleyemeyeceklerimiz**
- "Kullanıcılara iyi geldiğini kanıtladık."
- Akış içinde doz azaltmanın duyguyu iyileştirdiği (doğrudan bir test yok).
- Sinyalin kullanıcının ruh halini doğru "tespit ettiği" (yanlış pozitif oranı bilinmiyor; bu bir teşhis aracı değil).
- Simülasyondaki −%41'in bir iyi oluş artışı olduğu.
- Etkinin kalıcı olduğu ya da "döngünün kırıldığı."
- Hopwood (g=1,61) ya da Lambert (2022) düzeyinde büyük etkiler beklenebileceği.
- Pasif kullanımın herkes için zararlı olduğu.

---

## Simülasyonla birleştirme

**Simülasyonun söylediği:** Kapalı döngü simülasyonumuzda olumsuz içerikte takılan kullanıcının yoğun içerikte geçirdiği süre **−%41**, olağan okurunki **−%8** azalıyor; ilgi eşleşmesi korunuyor. Bu bir **maruziyet (doz)** sonucu. Duygu ölçülmedi. İki koşulda sayfa sayısı eşit tutulduğu için pay değil toplam süre ölçüldü. Serbest kullanımda oturum uzunluğu değişebilir; bu ölçülmedi. (Payın düşmesi toplamın düşmesi demek değildir: pay %30 düşerken görülen içerik %50 artarsa yoğun içerik sayısı %5 artar.)

**Sistem kendi başarısını ölçüyor:** "Yoğun içerik" müdahalenin kullandığı ton modeliyle tanımlanıyor; o içerik azalınca yoğunluk ölçüsü de kendiliğinden düşer. Bu yüzden "yoğunluk %X düştü, kaygı %X azaldı" denemez. Üç kollu simülasyona bu yüzden ikinci bir ölçüt eklendi: veri setlerinin kendi etiketine göre olumsuz içerikte (saldırgan mesaj, düşük puanlı yorum) geçen süre. Sonuçlar bu ölçütte de aynı yönde, ama bu ölçüt de insan duygusu değil.

**Neden uyarlanan doz, basit kural değil? (üç kollu simülasyon, 18.000 oturum):** Aynı kullanıcı her kolda aynı ilgi profili, aday çekilişi, sayfa sayısı ve davranış tohumuyla yaşatıldı. Takılan (4 profil) ve olağan (5 profil) gruplar, sabit düzeyler ve eşleştirme kuralı sonuçlardan önce yazıldı.

| Kol | Toplam müdahale (oturum başına kalkan yoğun gösterim) | Takılan profiller | Olağan profiller | Müdahalenin takılanlara düşen payı |
|---|---:|---:|---:|---:|
| Uyarlanan doz (uygulamadaki) | 4,8 | −%32 | −%6 | %84 |
| Herkese sabit doz, en düşük düzey (önceden belirlenen) | 8,0 | −%33 | −%32 | %49 |
| Rastgele zamanlı sabit doz, eşit toplam müdahale (sonradan eklendi, keşifsel) | 4,7 | −%20 | −%18 | %50 |

- Önceden belirlenen ölçüte göre sonuç **kısmen**. En düşük sabit düzey bile 1,7 kat fazla müdahale etti, yani "eşit toplam müdahale" koşulu sağlanamadı. Takılanlarda azalma benzer; olağan okura uyarlanan doz çok daha az dokunuyor.
- Toplam müdahale eşitlendiğinde (keşifsel) uyarlanan doz takılanlarda daha çok, olağanda daha az azaltıyor. Bağımsız etiket ölçütü de aynı yönde: takılanlarda −%28'e karşı −%17, olağanda −%6'ya karşı −%15.
- Çıkarılabilecek: simülasyon varsayımları altında uyarlanan sıralamanın **teknik** ek katkısı. Çıkarılamayacak: yapay zekânın insanları daha iyi hissettirdiği. Simülatör ile spiral modeli benzer varsayımlara dayanıyor; bu, sonucu bizim lehimize çevirebilecek bir döngüsellik.
- Ayrıntı: [ölçüm sınırları](olcum_sinirlari.md).

**Bileşen katkısı:** Haber başlıklarında açık olumsuz olayları neredeyse tamamen sözlük yakalıyor (450 başlıkta güçlü olumsuz: v3 %9, sözlük %87, ikisi birlikte %89). Sosyal içerikte işi model yapıyor; sözlük orada yakalamaya az şey ekleyip yanlış işareti artırıyor (normal tweetlerde %16 → %20, olumlu film yorumlarında %17 → %26). Etiketli setlerin hiçbiri güncel sözlük için "hiç görülmemiş test" değil. Ayrıntı: [model kartı](model_karti.md) §1.

**Öncüllerle birleşince beklenen yön:** Takılan kullanıcı daha az birikimli yoğun içerikle karşılaşır (simülasyon). Kısa süreli yoğun maruziyet olumlu duyguyu düşürür (Halka 1). Tek tek maruziyetlerin etkisi dakikalar içinde söner ama birikimi önlemek toparlanmaya alan açar (Halka 4). Buradan çıkan beklenti: oturum içinde olumlu duygu kaybında **azalma yönünde** bir etki. Yön literatürle tutarlı.

**Beklenen büyüklük:** Bilinmiyor; doğrudan bir sayı veremiyoruz. En yakın emsallerin etkileri şöyle: Kramer'de akıştan olumsuz çıkarma d≈0,02; tam devre dışı bırakmada 0,04–0,06 SD; kullanım azaltma meta-analizlerinde d=0,088 (anlamsız) ile g=0,25 arası. Bizim müdahalemiz bunlardan daha hafif (en fazla %60, silme yok). Bu yüzden büyük bir etki beklemek için gerekçe yok. Etkinin büyüklüğü ve kimlerde oluşacağı ancak katılımcı çalışmasıyla öğrenilebilir.

**Asimetri tasarımın lehine:** −%41'e karşı −%8, müdahalenin ağırlıkla hedef grupta yoğunlaştığını gösteriyor. Bu, etkilerin kişiden kişiye değiştiği bulgusuyla (Beyens vd. 2020) ve Allcott vd. (2025)'teki alt grup yoğunlaşmasıyla (keşifsel) uyumlu. Olağan okurdaki −%8 ise bir **maliyet**: yanlış pozitiflerin payı. İlgi eşleşmesi korunduğu için maliyet düşük ama sıfır değil.

**Belirsizlik kaynakları**

| Kaynak | Neden belirsiz |
|---|---|
| Sinyalin geçerliliği | Birleşik sinyal duyguyla hiç karşılaştırılmadı; yanlış pozitif oranı bilinmiyor |
| Doz-yanıt eğrisi | Tüm deneyler %100 olumsuz içeriği kontrolle karşılaştırıyor; kısmi azaltmanın etkisi bilinmiyor |
| Uyaran farkı | Kanıtlar TV, video ya da web gezinmesinden; kısa gönderi akışı değil |
| Simülasyonun varsayımları | Kullanıcı davranış kuralları bizim modelimiz; gerçek kullanıcı verisi değil |
| Zaman ölçeği | Duygu dakikalar içinde sönüyor; kalıcı etki beklemek için gerekçe yok |
| Geri tepme | Çekilme etkisi (Kramer) ve kısa müdahalede kötüleşme (Thrul) olasılığı |

**Nasıl ölçeriz (öneri; başlatılmadı):** İki ayrı değerlendirme gerekiyor.
- *Kullanılabilirlik ve anlam doğrulaması:* 5–10 yetişkinle. Amaç sağlık etkisi göstermek değil, büyük ürün yanlışlarını yakalamak. Sistem önce müdahale etmeden örüntü hesaplar, kullanıcı açıklamanın kendisine uyup uymadığını söyler. Öz-bildirim, modelin tahmini gösterilmeden önce alınır. Çok sayıda etkileşim olsa da katılımcı sayısı 5–10'dur.
- *Etki karşılaştırması:* Sabit prototiple, aynı kişide sırası dengelenmiş koşullar: olağan akış, herkese sabit kural ve uyarlanan doz. Birebir aynı gönderiler yerine konu ve yoğunluk bakımından eşleştirilmiş havuzlar kullanılır. Ana sonuç önceden seçilir (örneğin oturum sonundaki duygusal yük değişimi).
- *Ölçümler:* Türkçe geçerliği olan kısa bir duygulanım ölçeğiyle önce/sonra ölçüm; algılanan kontrol ve rahatsızlık; konuya ilgi ve kısa bilgi hatırlama; görülen yoğun içeriğin sayısı, süresi, payı ve sırası; kapatma ve geri alma. Kramer'deki çekilme etkisi için gönderi yazma ve etkileşimdeki değişim de izlenir.
- Kişi içindeki tekrarlar bağımsız sayılmaz. Anlamlı fark çıkmaması ne yararsızlık ne de eşdeğerlik kanıtıdır. Klinik iddia hedeflenirse etik kurul, uzmanlık ve daha uzun izlem gerekir.

---

## Karşı kanıtlar ve riskler; tasarımımızın cevabı

| Risk | Kanıt | Tasarımın cevabı | Açık kalan |
|---|---|---|---|
| Genel etki çok küçük | Orben ve Przybylski (2019): teknoloji kullanımı iyi oluştaki varyansın en fazla %0,4'ünü açıklıyor (kesitsel); Ferguson (2025); Allcott vd. (2025) | İddiamızı "zararı azaltma ve kontrol" düzeyinde tutuyoruz; büyük fayda vaat etmiyoruz | Gerçek etki ölçülmedi |
| Yanlış pozitif: olumsuzluk yanlılığı herkeste var | Soroka vd. (2019); Godard ve Holtzman (2024); Beyens vd. (2020) | Kişisel okuma hızı tabanı; tek sinyal yerine birleşik sinyal; EMA ile kalibrasyon; %60 üst sınır | Olağan okurda −%8 maliyet |
| Aktif kullanım da kaygıyla ilişkili | Godard ve Holtzman (2024): r=.12 | Pasiflik tek başına sinyal sayılmıyor | — |
| Haberdarlık kaybı, kasıtsız haber kaçınma | Skovsgaard ve Andersen (2020, kavramsal); Allcott vd. (2020): devre dışı bırakma haber bilgisini azalttı (siyasi bağlam) | Silme yok; resmi ve acil bilgi muaf; aynı olayın farklı anlatımı sunuluyor; katman kapatılabiliyor | Uzun vadeli bilgi düzeyi ölçülmedi |
| Olumsuz duygunun bir işlevi var | van Venrooij vd. (2022): olumsuz duygu yardım davranışına aracılık ediyor | Olumsuz içerik silinmiyor; azaltma en fazla %60 | — |
| Çekilme etkisi | Kramer vd. (2014): duygusal içerik azalınca kullanıcılar daha az yazdı | Yazma ve etkileşim metrikleri izlenmeli (öneri) | Test edilmedi |
| Kısa müdahalede geri tepme | Thrul vd. (2025): <1 hafta d=−0,175 | Müdahale bir yasak değil, doz ayarı | Kısa vadede izlenmeli |
| Etiketlemenin ters tepmesi | Bridgland, Jones ve Bellet (2024): uyarılar beklenti kaygısını artırıyor, sonraki sıkıntıyı azaltmıyor; Jones, Bellet ve McNally (2020): travmayı kimliğin merkezine taşıyabiliyor | Gönderilere "yoğun" rozeti yok, sıralama sessizce yapılıyor; "Neden bu?" yalnızca kullanıcı isteyince açılıyor; kimlik yükleyen dil kullanılmıyor ("kaygılısın" değil, "son 30 dakikada yoğun içerikte uzun kaldın") | Metinler bu ilkeye göre gözden geçirilmeli |
| Adlandırmanın duyguyu "kristalleştirmesi" | Nook vd. (2021) | Öneri: adlandırma zorunlu olmasın; etiket gerektirmeyen "Farklı bir anlatım göster" yolu da sunulsun ve iki yol karşılaştırılsın | Dışarıdan sunulan çerçeve sınanmadı |
| EMA sorusunun yan etkisi | Kivelä vd. (2024): N=82, klinik örneklem; ortalamada reaktivite yok, ama %22 ruh halinin kötüleştiğini bildirdi. Businelle vd. (2024): 411 kişi, 28 gün, 32 EMA koşulu; ölçüm sıklığı ve soru sayısı yükü değiştiriyor | Soru seyrek; "Geç" seçeneği var; modelin tahmini önce gösterilmiyor. Öneri: üst üste olumsuz yanıtlarda soru seyreltilsin | Genel kullanıcıda ölçülmedi |
| Reaktans ve paternalizm | Dietvorst vd. (2018); Bruns vd. (2018); Loewenstein vd. (2015); Carpenter (2013) | Açıklama, kapatma hakkı, "İstersen kapatabilirsin" dili. Bu dil ikna aracı olarak değil, gerçek bir çıkış hakkı olarak kullanılıyor | Sürekli tekrar eden açıklama sınanmadı |
| Onamsız manipülasyon (etik) | Kramer vd. (2014), PNAS'ın etik kaygı notu | Müdahale şeffaf, açıklamalı ve kapatılabilir | — |
| Pay azalırken toplam maruziyet artabilir | Aritmetik: pay %30 düşüp görülen içerik %50 artarsa yoğun içerik sayısı %5 artar | Simülasyonlarda sayfa sayısı eşit, toplam süre ölçüldü | Serbest kullanımda oturum uzunluğu ölçülmedi |
| Araya olumlu içerik koymak ters tepebilir | Cook, Cai ve Wohn (2022); Longpré vd. (2021) | Olumluya zorlama yok; aynı ilgi alanında daha az yoğun içerik | İkame içeriğin etkisi sınanmadı |
| Katsayılar psikolojik sabit değil | 0,7/0,3 bileşimi, 0,28/0,58 eşikleri, 30 dakikalık pencere ve %60 üst sınır literatürden türetilmedi | "Tasarım parametresi" diye anlatılıyor, öğrenilmiş katsayılardan ayrılıyor | Duyarlılık analizi yapılmadı |
| Sistem kendi başarısını ölçüyor | Yoğunluk ölçüsü müdahalenin ton modeliyle hesaplanıyor | Üç kollu simülasyonda veri setlerinin kendi etiketiyle ikinci ölçüt | İnsan duygusu ölçülmedi |
| Konuyu korumak bilgiyi korumak değil | Deprem konusunu korumak tahliye bilgisini korumakla aynı şey değil; önemli bilginin hepsi resmi hesaplardan gelmez | Resmi/acil hesap muafiyeti; içerik silinmiyor | Kritik bilgiyi kaçırma ve erişim gecikmesi ölçülmedi |
| Türkiye'ye aktarım | Kanıtların çoğu İngilizce içerik ve Batılı örneklemlerden | Türkçe veriyle teknik ölçüm; Türkiye'den üç çalışma (Satici 2023, Kartol 2023, Özmen 2026) | Türkçe gerçek kullanımda net fayda sınanmadı |

---

## Teslim edilen rapordaki ifadeler

Teknik rapor 24 Ağustos'ta teslim edildi. Teslimden sonra rapordaki bazı kaynak aktarımlarını makale özetleriyle yeniden karşılaştırdık; doğru aktarımlar aşağıda.

| Yer | Raporda | Doğru aktarım | Kontrol |
|---|---|---|---|
| s.4, Godard ve Holtzman (2024) | Meta-analiz, pasif/olumsuz tüketimin kaygı ve stresle ilişkisini "orta güçte doğruluyor" | "Kullanım türü ile iyi oluş arasındaki ilişkiler çoğunlukla çok küçük ve bağlama bağlı; bu yüzden salt pasifliğe değil, içerik ve oturum bağlamına bakıyoruz." | Cümle raporda var; meta-analizde ilişkilerin çoğu \|r\|<.10. Düzeltme gerekli. |
| s.17, Barsova vd. (2022) | Snooze ve süre araçları belirtilerle "anlamlı biçimde ilişkilendirilememiş" | Araçların ilişkileri farklı: Unfollow ve bildirim ayarları daha düşük belirtilerle ilişkili. Snooze daha düşük belirtilerle ilişkili değil; tam metnin tartışmasında Snooze kullananlarda daha yüksek belirti bildiriliyor. Kesitsel, neden-sonuç yok. | Özet raporla uyumlu. "Daha yüksek" bulgusu ikinci değerlendirmenin tam metin okumasına dayanıyor. |
| s.17, Milton vd. (2026) | "Ruh sağlığı tanısı almış 21 katılımcıyla tasarım atölyesi" | "Ruh sağlığı sorunları bildiren 21 katılımcıyla tasarım atölyeleri"; tedavi ya da etkinlik deneyi değil. | Özet "diagnosed" diyor, yöntem öz-tanıyı da kabul ediyor. İkinci ifade daha güvenli. |
| s.17–18, EMA döngüsü | Kullanıcı cevabıyla model uyumu, faydanın ölçümü gibi okunabiliyor | Tahmin doğrulaması ile müdahalenin etkisi iki ayrı değerlendirme başlığıdır. | Geçerli. |

---

## Kaynakça

- Ai, Y., & von Mühlenen, A. (2025). An experimental online study on the impact of negative social media comments on anxiety and mood. *Scientific Reports, 15*, 26642. https://doi.org/10.1038/s41598-025-10810-8
- Allcott, H., Braghieri, L., Eichmeyer, S., & Gentzkow, M. (2020). The welfare effects of social media. *American Economic Review, 110*(3), 629–676. https://doi.org/10.1257/aer.20190658 *(yalnızca risk bağlamı; siyasi çıktılar içeriyor)*
- Allcott, H., Gentzkow, M., & Song, L. (2022). Digital addiction. *American Economic Review, 112*(7), 2424–2463. https://doi.org/10.1257/aer.20210867
- Allcott, H., Gentzkow, M., Wittenbrink, B., Cisneros, J. C., Crespo-Tenorio, A., Dimmery, D., … Tucker, J. A. (2025). *The effect of deactivating Facebook and Instagram on users' emotional state* (NBER Working Paper No. 33697). https://www.nber.org/papers/w33697
- Ata, E. E., Sarıtaş Arslan, M., & Murat Mehmed Ali, M. (2026). Social media exposure to earthquake-related news and secondary traumatic stress: A cross-sectional study of social media users in Türkiye. *Archives of Psychiatric Nursing, 60*, 152043. https://doi.org/10.1016/j.apnu.2025.152043
- Bar-Haim, Y., Lamy, D., Pergamin, L., Bakermans-Kranenburg, M. J., & van IJzendoorn, M. H. (2007). Threat-related attentional bias in anxious and nonanxious individuals: A meta-analytic study. *Psychological Bulletin, 133*(1), 1–24. https://doi.org/10.1037/0033-2909.133.1.1
- Barsova, T., Cheong, Z. G., Mak, A. R., & Liu, J. C. J. (2022). Predicting psychological symptoms when Facebook's digital well-being features are used: Cross-sectional survey study. *JMIR Formative Research, 6*(8), e39387. https://doi.org/10.2196/39387
- Berger, J., & Milkman, K. L. (2012). What makes online content viral? *Journal of Marketing Research, 49*(2), 192–205. https://doi.org/10.1509/jmr.10.0353
- Beyens, I., Pouwels, J. L., van Driel, I. I., Keijsers, L., & Valkenburg, P. M. (2020). The effect of social media on well-being differs from adolescent to adolescent. *Scientific Reports, 10*, 10763. https://doi.org/10.1038/s41598-020-67727-7
- Bridgland, V. M. E., Jones, P. J., & Bellet, B. W. (2024). A meta-analysis of the efficacy of trigger warnings, content warnings, and content notes. *Clinical Psychological Science, 12*(4), 751–771. https://doi.org/10.1177/21677026231186625
- Brockmeier, L. C., Mertens, L., Roitzheim, C., Radtke, T., Dingler, T., & Keller, J. (2025). Effects of an intervention targeting social media app use on well-being outcomes: A randomized controlled trial. *Applied Psychology: Health and Well-Being, 17*(1), e12646. https://doi.org/10.1111/aphw.12646
- Bruns, H., Kantorowicz-Reznichenko, E., Klement, K., Luistro Jonsson, M., & Rahali, B. (2018). Can nudges be transparent and yet effective? *Journal of Economic Psychology, 65*, 41–59. https://doi.org/10.1016/j.joep.2018.02.002
- Buchanan, K., Aknin, L. B., Lotun, S., & Sandstrom, G. M. (2021). Brief exposure to social media during the COVID-19 pandemic: Doom-scrolling has negative emotional consequences, but kindness-scrolling does not. *PLoS ONE, 16*(10), e0257728. https://doi.org/10.1371/journal.pone.0257728
- Businelle, M. S., Hébert, E. T., Shi, D., Benson, L., Kezbers, K. M., Tonkin, S., Piper, M. E., & Qian, T. (2024). Investigating best practices for ecological momentary assessment: Nationwide factorial experiment. *Journal of Medical Internet Research, 26*, e50275. https://doi.org/10.2196/50275
- Carpenter, C. J. (2013). A meta-analysis of the effectiveness of the "but you are free" compliance-gaining technique. *Communication Studies, 64*(1), 6–17. https://doi.org/10.1080/10510974.2012.727941
- Cook, C. L., Cai, J., & Wohn, D. Y. (2022). Awe versus aww: The effectiveness of two kinds of positive emotional stimulation on stress reduction for online content moderators. *Proceedings of the ACM on Human-Computer Interaction, 6*(CSCW2), 1–19. https://doi.org/10.1145/3555168
- de Hoog, N., & Verboon, P. (2020). Is the news making us unhappy? The influence of daily news exposure on emotional states. *British Journal of Psychology, 111*(2), 157–173. https://doi.org/10.1111/bjop.12389
- Dietvorst, B. J., Simmons, J. P., & Massey, C. (2018). Overcoming algorithm aversion: People will use imperfect algorithms if they can (even slightly) modify them. *Management Science, 64*(3), 1155–1170. https://doi.org/10.1287/mnsc.2016.2643
- Fan, R., Varol, O., Varamesh, A., Barron, A., van de Leemput, I. A., Scheffer, M., & Bollen, J. (2019). The minute-scale dynamics of online emotions reveal the effects of affect labeling. *Nature Human Behaviour, 3*(1), 92–100. https://doi.org/10.1038/s41562-018-0490-5
- Ferguson, C. J. (2025). Do social media experiments prove a link with mental health: A methodological and meta-analytic review. *Psychology of Popular Media, 14*(2), 201–206. https://doi.org/10.1037/ppm0000541
- Fredrickson, B. L., Mancuso, R. A., Branigan, C., & Tugade, M. M. (2000). The undoing effect of positive emotions. *Motivation and Emotion, 24*(4), 237–258. https://doi.org/10.1023/A:1010796329158
- Gillies, J. C. P., & Dozois, D. J. A. (2021). How long do mood induction procedure (MIP) primes really last? Implications for cognitive vulnerability research. *Journal of Affective Disorders, 292*, 328–336. https://doi.org/10.1016/j.jad.2021.05.047
- Godard, R., & Holtzman, S. (2024). Are active and passive social media use related to mental health, wellbeing, and social support outcomes? A meta-analysis of 141 studies. *Journal of Computer-Mediated Communication, 29*(1), zmad055. https://doi.org/10.1093/jcmc/zmad055
- Holman, E. A., Garfin, D. R., & Silver, R. C. (2014). Media's role in broadcasting acute stress following the Boston Marathon bombings. *PNAS, 111*(1), 93–98. https://doi.org/10.1073/pnas.1316265110
- Hopwood, T. L., & Schutte, N. S. (2017). Psychological outcomes in reaction to media exposure to disasters and large-scale violence: A meta-analysis. *Psychology of Violence, 7*(2), 316–327. https://doi.org/10.1037/vio0000056
- Hunt, M. G., Marx, R., Lipson, C., & Young, J. (2018). No more FOMO: Limiting social media decreases loneliness and depression. *Journal of Social and Clinical Psychology, 37*(10), 751–768. https://doi.org/10.1521/jscp.2018.37.10.751
- Johnston, W. M., & Davey, G. C. L. (1997). The psychological impact of negative TV news bulletins: The catastrophizing of personal worries. *British Journal of Psychology, 88*(1), 85–91. https://doi.org/10.1111/j.2044-8295.1997.tb02622.x
- Jones, P. J., Bellet, B. W., & McNally, R. J. (2020). Helping or harming? The effect of trigger warnings on individuals with trauma histories. *Clinical Psychological Science, 8*(5), 905–917. https://doi.org/10.1177/2167702620921341
- Kartol, A., Üztemur, S., & Yaşar, P. (2023). 'I cannot see ahead': Psychological distress, doomscrolling and dark future among adult survivors following Mw 7.7 and 7.6 earthquakes in Türkiye. *BMC Public Health, 23*(1). https://doi.org/10.1186/s12889-023-17460-3
- Kauer, S. D., Reid, S. C., Crooke, A. H. D., Khor, A., Hearps, S. J. C., Jorm, A. F., Sanci, L., & Patton, G. (2012). Self-monitoring using mobile phones in the early stages of adolescent depression: Randomized controlled trial. *Journal of Medical Internet Research, 14*(3), e67. https://doi.org/10.2196/jmir.1858
- Kelly, C. A., & Sharot, T. (2025). Web-browsing patterns reflect and shape mood and mental health. *Nature Human Behaviour, 9*(1), 133–146. https://doi.org/10.1038/s41562-024-02065-6
- Kivelä, L. M. M., Fiß, F., van der Does, W., & Antypa, N. (2024). Examination of acceptability, feasibility, and iatrogenic effects of ecological momentary assessment (EMA) of suicidal ideation. *Assessment, 31*(6), 1292–1308. https://doi.org/10.1177/10731911231216053
- Kizilcec, R. F. (2016). How much information? Effects of transparency on trust in an algorithmic interface. In *Proceedings of the 2016 CHI Conference on Human Factors in Computing Systems* (pp. 2390–2395). https://doi.org/10.1145/2858036.2858402
- Kramer, A. D. I., Guillory, J. E., & Hancock, J. T. (2014). Experimental evidence of massive-scale emotional contagion through social networks. *PNAS, 111*(24), 8788–8790. https://doi.org/10.1073/pnas.1320040111 *(Editorial Expression of Concern: https://doi.org/10.1073/pnas.1412583111)*
- Kuijsters, A., Redi, J., de Ruyter, B., & Heynderickx, I. (2016). Inducing sadness and anxiousness through visual media: Measurement techniques and persistence. *Frontiers in Psychology, 7*, 1141. https://doi.org/10.3389/fpsyg.2016.01141
- Lambert, J., Barnstable, G., Minter, E., Cooper, J., & McEwan, D. (2022). Taking a one-week break from social media improves well-being, depression, and anxiety: A randomized controlled trial. *Cyberpsychology, Behavior, and Social Networking, 25*(5), 287–293. https://doi.org/10.1089/cyber.2021.0324
- Loewenstein, G., Bryce, C., Hagmann, D., & Rajpal, S. (2015). Warning: You are about to be nudged. *Behavioral Science & Policy, 1*(1), 35–42. https://doi.org/10.1177/237946151500100106
- Longpré, C., Sauvageau, C., Cernik, R., Journault, A.-A., Marin, M.-F., & Lupien, S. (2021). Staying informed without a cost: No effect of positive news media on stress reactivity, memory and affect in young adults. *PLOS ONE, 16*(10), e0259094. https://doi.org/10.1371/journal.pone.0259094
- May, W., Malouff, J. M., & Meynadier, J. (2025). Reducing social media use decreases depression symptoms: A meta-analysis of randomised controlled trials. *European Journal of Investigation in Health, Psychology and Education, 15*(11), 222. https://doi.org/10.3390/ejihpe15110222
- McIntyre, K., & Lough, K. (2023). Evaluating the effects of solutions and constructive journalism: A systematic review of audience-focused research. *Newspaper Research Journal, 44*(3), 276–300. https://doi.org/10.1177/07395329231187622
- Mertens, L., Brockmeier, L. C., Roitzheim, C., Radtke, T., Dingler, T., & Keller, J. (2026). Promoting self-regulated social media use on smartphones with a mobile intervention app (Wellspent): Randomized controlled trial. *JMIR mHealth and uHealth, 14*, e56824. https://doi.org/10.2196/56824
- Milli, S., Carroll, M., Wang, Y., Pandey, S., Zhao, S., & Dragan, A. D. (2025). Engagement, user satisfaction, and the amplification of divisive content on social media. *PNAS Nexus, 4*(3), pgaf062. https://doi.org/10.1093/pnasnexus/pgaf062 *(yalnızca bağlam; siyasi)*
- Milton, A., Runningen, D., Terveen, L., Kaur, H., & Chancellor, S. (2026). *Unraveling entangled feeds: Rethinking social media design to enhance user well-being* (arXiv:2602.15745). https://arxiv.org/abs/2602.15745
- Nolen-Hoeksema, S. (2000). The role of rumination in depressive disorders and mixed anxiety/depressive symptoms. *Journal of Abnormal Psychology, 109*(3), 504–511. https://doi.org/10.1037/0021-843X.109.3.504
- Nook, E. C., Satpute, A. B., & Ochsner, K. N. (2021). Emotion naming impedes both cognitive reappraisal and mindful acceptance strategies of emotion regulation. *Affective Science, 2*(2), 187–198. https://doi.org/10.1007/s42761-021-00036-y
- Orben, A., & Przybylski, A. K. (2019). The association between adolescent well-being and digital technology use. *Nature Human Behaviour, 3*(2), 173–182. https://doi.org/10.1038/s41562-018-0506-1
- Overgaard, C. S. B. (2021). Constructive journalism in the face of a crisis: The effects of social media news updates about COVID-19. *Journalism Studies, 22*(14), 1875–1893. https://doi.org/10.1080/1461670X.2021.1971107
- Overgaard, C. S. B. (2023). Mitigating the consequences of negative news: How constructive journalism enhances self-efficacy and news credibility. *Journalism, 24*(7), 1424–1441. https://doi.org/10.1177/14648849211062738
- Overgaard, C. S. B., & Stroud, N. J. (2020). *Koronavirüs başlıkları ve görselleri deneyi* [kurum raporu]. Center for Media Engagement. https://mediaengagement.org/research/coronavirus-headlines-and-images/ *(Overgaard 2021 ile aynı deney olarak sayıldı)*
- Özmen, M. (2026). Earthquake fear, doomscrolling, anxiety and intolerance of uncertainty: A longitudinal serial mediation study. *Journal of Health Psychology, 31*(3). https://doi.org/10.1177/13591053251387438
- Peckham, A. D., McHugh, R. K., & Otto, M. W. (2010). A meta-analysis of the magnitude of biased attention in depression. *Depression and Anxiety, 27*(12), 1135–1142. https://doi.org/10.1002/da.20755
- Plackett, R., Blyth, A., & Schartau, P. (2023). The impact of social media use interventions on mental well-being: Systematic review. *Journal of Medical Internet Research, 25*, e44922. https://doi.org/10.2196/44922
- Price, M., Legrand, A. C., Brier, Z. M. F., van Stolk-Cooke, K., Peck, K., Dodds, P. S., Danforth, C. M., & Adams, Z. W. (2022). Doomscrolling during COVID-19: The negative association between daily social and traditional media consumption and mental health symptoms during the COVID-19 pandemic. *Psychological Trauma: Theory, Research, Practice, and Policy, 14*(8), 1338–1346. https://doi.org/10.1037/tra0001202
- Robertson, C. E., Pröllochs, N., Schwarzenegger, K., Pärnamets, P., Van Bavel, J. J., & Feuerriegel, S. (2023). Negativity drives online news consumption. *Nature Human Behaviour, 7*(5), 812–822. https://doi.org/10.1038/s41562-023-01538-4
- Satici, S. A., Gocet Tekin, E., Deniz, M. E., & Satici, B. (2023). Doomscrolling Scale: Its association with personality traits, psychological distress, social media use, and wellbeing. *Applied Research in Quality of Life, 18*(2), 833–847. https://doi.org/10.1007/s11482-022-10110-7
- Shaikh, S. J., McGowan, A. L., & Lydon-Staley, D. M. (2024). Associations between valenced news and affect in daily life: Experimental and ecological momentary assessment approaches. *Media Psychology, 27*(3), 455–478. https://doi.org/10.1080/15213269.2023.2247320
- Shen, S., Qi, W., Zeng, J., Li, S., Liu, X., Zhu, X., Dong, C., Wang, B., Shi, Y., Yao, J., Wang, B., Lou, X., Gu, S., Li, P., Wang, J., Jiang, G., & Cao, S. (2025). Passive sensing for mental health monitoring using machine learning with wearables and smartphones: Scoping review. *Journal of Medical Internet Research, 27*, e77066. https://doi.org/10.2196/77066
- Skovsgaard, M., & Andersen, K. (2020). Conceptualizing news avoidance: Towards a shared understanding of different causes and potential solutions. *Journalism Studies, 21*(4), 459–476. https://doi.org/10.1080/1461670X.2019.1686410
- Soroka, S., Fournier, P., & Nir, L. (2019). Cross-national evidence of a negativity bias in psychophysiological reactions to news. *PNAS, 116*(38), 18888–18892. https://doi.org/10.1073/pnas.1908369116
- Thompson, R. R., Jones, N. M., Holman, E. A., & Silver, R. C. (2019). Media exposure to mass violence events can fuel a cycle of distress. *Science Advances, 5*(4), eaav3502. https://doi.org/10.1126/sciadv.aav3502
- Thrul, J., Devkota, J., AlJuboori, D., Regan, T., Alomairah, S., & Vidal, C. (2025). Social media reduction or abstinence interventions are providing mental health benefits—Reanalysis of a published meta-analysis. *Psychology of Popular Media, 14*(2), 207–209. https://doi.org/10.1037/ppm0000574
- Torre, J. B., & Lieberman, M. D. (2018). Putting feelings into words: Affect labeling as implicit emotion regulation. *Emotion Review, 10*(2), 116–124. https://doi.org/10.1177/1754073917742706
- Valkenburg, P. M., van Driel, I. I., & Beyens, I. (2022). The associations of active and passive social media use with well-being: A critical scoping review. *New Media & Society, 24*(2), 530–549. https://doi.org/10.1177/14614448211065425
- van Venrooij, I., Sachs, T., & Kleemans, M. (2022). The effects of constructive television news reporting on prosocial intentions and behavior in children: The role of negative emotions and self-efficacy. *Communications, 47*(1), 5–31. https://doi.org/10.1515/commun-2019-0151
- Visted, E., Vøllestad, J., Nielsen, M. B., & Schanche, E. (2018). Emotion regulation in current and remitted depression: A systematic review and meta-analysis. *Frontiers in Psychology, 9*, 756. https://doi.org/10.3389/fpsyg.2018.00756
- Webb, T. L., Miles, E., & Sheeran, P. (2012). Dealing with feeling: A meta-analysis of the effectiveness of strategies derived from the process model of emotion regulation. *Psychological Bulletin, 138*(4), 775–808. https://doi.org/10.1037/a0027600
- Webb, T. L., Lindquist, K. A., Jones, K., Avishai, A., & Sheeran, P. (2018). Situation selection is a particularly effective emotion regulation strategy for people who need help regulating their emotions. *Cognition and Emotion, 32*(2), 231–248. https://doi.org/10.1080/02699931.2017.1295922
- Yoon, S., Verona, E., Schlauch, R., Schneider, S., & Rottenberg, J. (2020). Why do depressed people prefer sad music? *Emotion, 20*(4), 613–624. https://doi.org/10.1037/emo0000573

*Kaynak hijyeni notları:*
- Buchanan vd. (2021) doğrulama kayıtlarında beş ayrı yerde geçiyor, ama tek çalışma olarak sayıldı. Thompson vd. (2019) ve Holman vd. (2014) aynı araştırma grubundan geliyor, bu yüzden bağımsız iki kanıt sayılmadı.
- Lemahieu (2025) doğrulanamadığı için kullanılmadı. Eleştirmenin önerdiği ama doğrulama turundan geçmemiş klasik çalışmalar da (duygu bulaşması, ruh hali yönetimi ve duygusal atalet üzerine olanlar gibi) bu dosyaya eklenmedi.
- Fan vd. (2019), Nolen-Hoeksema (2000) ve Peckham vd. (2010) künyeleri 15.09'da Crossref kayıtlarından tamamlandı.
- 402 depremzedeli çalışma (Kartol vd. 2023) ile Özmen (2026) 15.09'da Europe PMC özetlerinden ayrıca doğrulanıp eklendi.
- İkinci değerlendirmeden alınan kaynakların künyeleri 15.09'da Crossref ve Europe PMC kayıtlarından çekildi. Overgaard ve Stroud (2020) kurum raporu ile Overgaard (2021) aynı deney sayıldı. Wellspent deneyinin iki yayını (Mertens vd. 2026; Brockmeier vd. 2025) tek deney sayıldı.
- Barsova vd. (2022) özetinde Snooze için yalnızca "daha düşük belirtilerle ilişkili değil" yazıyor; "daha yüksek belirti" aktarımı ikinci değerlendirmenin tam metin okumasına dayanıyor. Shaikh vd. (2024) için etki büyüklükleri ve "sonraki ölçüme taşınmadı" bulgusu da o değerlendirmenin aktarımı; özet yalnızca yönü doğruluyor.
