# Görünürlük, model rolü ve final doğrulaması

## Gönderide kalma süresi

Göz takibi yapılmaz. Görünürlük, okuma için dolaylı bir sinyaldir; kullanıcının
metni okuduğunu veya görseli incelediğini kanıtlamaz. Ton modeli yalnızca metni
inceler, görselin içeriğini değerlendirmez.

Ana akışta aynı anda bir kart seçilir. Üst çubuk ve mobil alt gezinmenin
kapattığı alan çıkarılır. Kartın ekrana sığabilecek bölümünün en az %60'ı
görünmelidir. Görünürlük oranı en yüksek kart; eşitlikte görünür alanı ekranın
merkezine en yakın kart seçilir. Uzun kartların %100 görünmesi gerekmez.
Kısa kartlara yapay görsel boşluğu eklenmez.

Kaydırma ve yeniden boyutlandırmada seçim yenilenir. Görsel yüklenmesi ve
pencere açılması için 250 ms aralıklı kontrol de yapılır. Sekme gizlenince,
onay/açıklama/yorum penceresi veya kontrol sorusu açılınca süre durur. Tıklamada
kaydedilen süre karttan çıkarken tekrar yazılmaz. Sayfadan ayrılırken son süre
kaydedilmeye çalışılır; tarayıcı kapanırken asenkron depolama garantili değildir.
1,5 saniye altındaki süreler mevcut modelde okunmuş içerik sayılmaz.

## Modelin rolü korunur

Teslim edilen raporun 7–9. sayfaları beş kategorili psikolojik izlenim modelini,
kullanıcı cevabıyla karşılaştırmayı ve cihazda doğrulamayı açıkça içerir.
Beş kategori ve İçgörü doğrulaması korunur. Ana akışın yoğunluk temelli satırı
"Dengeleme durumu" diye adlandırılır; kullanıcının kendi tepkisi ayrı belirtilir.
Varsayılan ruh hali olasılıkları birleşik yoğunluğa katkı vermeye devam eder.
Kişiselleştirilmiş ruh hali modeli sıralamayı etkilemez.

## Son sözlük değerlendirmesi

72.495 gerçek metindeki sabit BERT puanlarına güncel sözlük uygulanmıştır.
Yeni eğitim veya BERT çıkarımı yapılmamıştır. Geliştirmede görülmüş 450 etiketli
başlığın normal yazımında sonuç değişmedi: güçlü olumsuz yakalama %88,9,
olumsuz isabet %94,2. 200 başlık alt kümesinde sırasıyla %82,4 ve %90,2.
Karaktersiz 450 başlık varyantında yakalama %53,3 → %77,8; olumsuz isabet
%92,3 → %91,5; olumsuz olmayanda işaret %3,8 → %5,9.
Bu, yeni bağımsız test değildir. ASCII düzeltmesi bazı yanlış alarmları artırır.

600 senaryolu sıralama etki analizi yeniden çalıştırıldı; sonuç dosyası değişmedi.
253 gönderilik havuzda yoğun pay %22,1; ilk sayfadaki yoğun pay azalması
%35 / %47 / %62, korunan ilgi %100,1 / %99,4 / %98,8. Resmi gönderiler
0/146 durumda aşağı indi. Bunlar sabit yoğunluklarda sıralama ölçümleridir;
görünürlük takibinin gerçek kullanıcı etkisini ayrıca kanıtlamaz.

## Ruh hali katkısı için karar

Aynı simüle edilmiş oturumlar mevcut 0,7×S+0,3×R, 0,7×S ve S ile karşılaştırıldı.
Sadece R'yi çıkarmak ile S'yi yeniden 1'e ölçeklemek farklı deneylerdir.
Aynı eşikler kullanıldığı için sonuçlar eşdeğer kalibre edilmiş sistemlerin
başarı karşılaştırması değildir. Her grupta 200 oturum vardır.

Olağan forum okuma senaryosunda doz eşiği aşımı mevcutta %20, 0,7×S'de %0,
S'de %30 oldu. Toksik içerikte oyalanmada bildirim eşiği aşımı sırasıyla
%82,5, %44,5 ve %91 oldu. Hızlı kaydırmada üçünde de %0.
Oturum sonundaki eşik aşımı, oturum boyunca bildirim sayısı veya insan
tarafından doğrulanmış doğru müdahale oranı değildir.

Bu nedenle katsayılar ve eşikler değiştirilmedi. Öncelik gerçek kullanıcıyla
müdahalenin istenip istenmediğini ölçmektir. Modelin sürekli benzer kategori
üretmesi yalnızca etiketi değiştirerek çözülmüş sayılmaz.

## Sonraki insan denemesi

5–10 gönüllüye aynı görevler verilir; kişisel sağlık bilgisi istenmez.
Başlamadan çalışma ve gönüllü katılım açıklanır. Yardım etmeden gözlenir:

1. Akış değişikliğinin nedenini bul.
2. Bu oturumda dengelemeyi kapat.
3. Bir tepki ver ve sistem tahminiyle kendi bildiriminin farkını açıkla.
4. Verilerinin nerede tutulduğunu ve nasıl silinebileceğini bul (silme zorunlu değil).

Katılımcı kodu, görev başarısı, yardım ihtiyacı, süre ve "Bu müdahaleyi ister
miydin? Neden?" cevabı kaydedilir. Sıra etkisini azaltmak için açık/kapalı
gösterimin sırası katılımcılar arasında değiştirilir. Bu küçük deneme klinik
fayda veya toplum geneli etki ölçümü olarak sunulmaz. Henüz katılımcı sonucu yoktur.
