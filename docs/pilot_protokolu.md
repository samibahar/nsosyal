# Gönüllü pilot protokolü

## Neden

Spiral ve ruh hali modelleri sentetik (simüle edilmiş) davranış verisiyle eğitildi.
Bir modelin gerçek insanlarda ne kadar tuttuğunu yalnızca gerçek insanların
cevapları gösterebilir. Uygulama bu cevapları zaten topluyor: ara sıra çıkan
"Şu an nasıl hissediyorsun?" sorusu. Pilot, bu cevapları birkaç gönüllüden
toplayıp modelleri **ilk kez gerçek öz-bildirimle** ölçmek içindir.

Bu bir ruh sağlığı değerlendirmesi değildir; kimseye tanı konmaz.

## Katılımcı ve onam

- 5–10 gönüllü, 18 yaş üstü. Katılım gönüllüdür, istenen an bırakılabilir.
- İsim, telefon, e-posta toplanmaz. Dosyadaki katılımcı kodu cihazda rastgele üretilir.
- Katılımcıya önceden söylenir: ne kaydedildiği (aşağıda), dosyayı yalnızca
  kendisinin gönderebileceği, göndermeden önce içeriğini Ayarlar'da görebileceği.
- Zor bir dönemden geçen biri için bu uygulama bir destek aracı değildir;
  profesyonel destek önerilir.

## Uygulama

1. Sunucu ekipten birinin bilgisayarında çalışır, gönüllüler aynı Wi-Fi'dan bağlanır:
   `python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000`, adres
   `http://<bilgisayarın-yerel-ip-adresi>:8000`.
2. **Her gönüllü kendi telefonunu ya da tarayıcısını kullanır.** Aynı tarayıcıyı
   paylaşmak iki kişinin cevaplarını tek dosyada karıştırır.
3. İlk açılışta "Açık" seçilir. Ayarlar'da "Kısa kontrol soruları" ve
   "Kişisel uyarlama" açık kalır.
4. 2–3 gün, günde 1–2 oturum, oturum başına 10–15 dakika akışta **her zamanki gibi**
   gezinilir. Kontrol sorusu en fazla 20 dakikada bir çıkar; dürüst cevap
   verilir, istenmezse "Geç" seçilir.
5. Jüri demosu çalıştırılmaz. Çalıştırılırsa sonraki cevaplar zaten
   "demo" olarak işaretlenir ve analizden çıkarılır.
6. Bitişte: Ayarlar > Gönüllü pilot > "Pilot dosyasını indir". Gönüllü dosyayı
   ekibe kendisi gönderir. Ekip dosyaları `pilot_verisi/` klasörüne koyar
   (klasör repoya girmez).

Hedef: kişi başı en az 5 cevap, toplamda 40+ cevap.

## Dosyada ne var, ne yok

Her kontrol sorusu anı için:

- Verilen cevap ve o anki model tahminleri (varsayılan ve kişisel).
- Spiral tahminine giren 4 özet sayı: son 30 dakikada yoğun tonlu içerikte
  geçen sürenin payı, bu içerikte diğerlerine göre oyalanma, okuma süresinin
  üstünde kalma, aktif katılım (roket/yorum) oranı.
- Ruh hali tahminine giren 5 sayı: son gönderinin tonu, durma süresi,
  tıklama/roket/yorum.
- Kaçıncı gün olduğu (tarih ya da saat değil).

Gönderi metni, gönderi kimliği, konu, yazar, saat ve kimlik bilgisi **yoktur**
(tests/e2e/test_akis.py bunu her çalıştırmada denetler).

## Analiz

```
python pilot_analizi.py pilot_verisi/
```

Çıktı `pilot_sonuc.txt` dosyasına da yazılır:

1. **Uygulamanın o anki tahminleri:** her cevap önce tahmin edildi, sonra
   öğrenildi. Uyum oranı Wilson %95 güven aralığıyla, "hep en sık cevabı söyle"
   ve rastgele tahmin tabanlarıyla birlikte verilir.
2. **Gerçek veriyle yeniden eğitim:** her turda bir katılımcının bütün cevapları
   test, kalanlar eğitim olarak ayrılır. Pilot verisiyle eğitilen spiral modeli
   (aynı işaret kısıtlarıyla) sentetik modelle ve taban oranıyla, hiç görmediği
   kişilerde karşılaştırılır. En az 3 katılımcı gerekir.

Yeni katsayılar uygulamaya otomatik yazılmaz; karar sonuca bakılarak verilir.
Sonuç ne çıkarsa, sentetik modelden kötü çıksa da, olduğu gibi raporlanır.

## Sınırlılıklar

- Küçük ve gönüllü örneklem; güven aralıkları geniştir, genelleme yapılamaz.
- Öz-bildirim klinik bir ölçüm değildir. "Yoğun" ya da "sinirli" cevabı spiral
  için yalnızca zayıf bir etikettir.
- Soru sorulması davranışı etkileyebilir (ölçüm etkisi).
