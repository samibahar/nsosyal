# -*- coding: utf-8 -*-
"""Zayif alt-tur icin NEGATIF ornekler -- Gemini kotasi bittigi icin (gunluk
20 istek siniri) bu kez Claude (ben) tarafindan dogrudan uretildi, hicbir
API'ye ihtiyac olmadan. Ayni uslup kurallari: kisa/resmi/ucuncu-sahis,
dolayli/cikarimsal olumsuz sonuc, acik "kotu/berbat" gibi kelime yok,
gercek isim yok, siyasi/dini icerik yok, cesitli konular.
"""
import json
from pathlib import Path

NEGATIF_ORNEKLER = [
    "Şirketin çeyreklik geliri beklentilerin altında kaldı, hisseler sert düşüş yaşadı.",
    "Fabrikada yaşanan üretim durması yüzlerce işçiyi etkiledi.",
    "Belediyenin su kesintisi planlanandan üç gün daha uzun sürdü.",
    "Yerel takımın deplasman serisi altıncı maçında da galibiyetsiz kapandı.",
    "Havayolu şirketi, teknik arıza nedeniyle yüzlerce seferi iptal etti.",
    "Yeni köprünün açılışı, zemin etüdü sorunları yüzünden iki yıl ertelendi.",
    "Bölgedeki kuraklık, tarım üreticilerinin rekoltesini yarı yarıya düşürdü.",
    "Hastane acil servisinde yaşanan yoğunluk, bekleme sürelerini saatlere çıkardı.",
    "Teknoloji şirketinin yeni ürünü, piyasaya çıkışının ardından geri çağrıldı.",
    "İlçedeki trafik düzenlemesi, esnafın günlük cirosunu belirgin biçimde azalttı.",
    "Okulun bilgisayar laboratuvarı, bütçe kesintisi nedeniyle kapatıldı.",
    "Limandaki grev, ihracat sevkiyatlarını iki haftadır aksatıyor.",
    "Şehir merkezindeki tarihi bina, bakımsızlık nedeniyle çökme riskiyle karşı karşıya.",
    "Yayın platformunun abone sayısı, son çeyrekte art arda üçüncü kez geriledi.",
    "Baraj seviyesindeki düşüş, kentin su kısıtlaması uygulamasına gitmesine neden oldu.",
    "Otomobil üreticisi, kalite sorunları nedeniyle on binlerce aracı geri çağırdı.",
    "İlçe pazarındaki esnaf, kira artışları nedeniyle dükkanlarını kapatmak zorunda kaldı.",
    "Spor kulübünün genç takımı, ligde küme düşme hattına gerileyerek sezonu tamamladı.",
    "Fabrika bacasından sızan kimyasal, çevredeki tarım arazilerine zarar verdi.",
    "Bankanın müşteri hizmetleri hattındaki bekleme süresi bu ay rekor kırdı.",
    "Kentteki toplu taşıma seferleri, personel eksikliği nedeniyle yüzde otuz azaltıldı.",
    "Üniversitenin araştırma bütçesi, geçen yıla göre ciddi oranda kısıldı.",
    "Sanayi bölgesindeki elektrik kesintileri, üretim hattını haftada iki gün durdurdu.",
    "Perakende zincirinin şehir merkezindeki şubesi, düşük satışlar nedeniyle kapatıldı.",
    "Yeni vergi düzenlemesi, küçük işletmelerin maliyetlerini önemli ölçüde artırdı.",
    "Kütüphanenin çatı onarımı tamamlanamadığı için bölüm aylardır hizmet veremiyor.",
    "Otoyol inşaatındaki gecikme, çevre ilçelerin ulaşımını olumsuz etkiliyor.",
    "Konser organizasyonu, teknik ekipman arızası nedeniyle yarıda kesildi.",
    "İlçedeki içme suyu şebekesinde tespit edilen kaçak, günlerce onarılamadı.",
    "Yerli üretici, ham madde fiyatlarındaki artış nedeniyle üretimi durdurmak zorunda kaldı.",
    "Havalimanındaki bagaj sistemi arızası, yüzlerce yolcunun uçuşunu aksattı.",
    "Belediye meclisi, bütçe açığı nedeniyle planlanan park projesini iptal etti.",
    "Sigorta şirketinin hasar ödemelerindeki gecikme, müşteri şikayetlerini artırdı.",
    "Madende yaşanan göçük, bölgedeki üretimi süresiz olarak durdurdu.",
    "Restoran zincirinin hijyen denetiminde tespit edilen eksiklikler kapanmasına yol açtı.",
    "Kentteki hava kirliliği ölçümleri, bu kış mevsiminin en yüksek seviyesine ulaştı.",
    "Sigorta prim artışları, küçük esnafın araç filosunu küçültmesine neden oldu.",
    "Toplu konut projesindeki inşaat gecikmesi, teslim tarihini bir yıl erteledi.",
    "Yerel gazetenin basılı tirajı, dijitalleşme sürecinde sürekli düşüş gösterdi.",
    "İlçe hastanesindeki doktor eksikliği, randevu sürelerini bir aya kadar uzattı.",
    "Tekstil fabrikasındaki siparişlerin iptali, çalışanların ücretsiz izne çıkmasına yol açtı.",
    "Kentteki bisiklet yolu projesi, bütçe yetersizliği nedeniyle yarım kaldı.",
    "Havaalanı çevresindeki gürültü şikayetleri, bu yıl belirgin biçimde arttı.",
    "Yerel esnaf birliği, online alışverişin artmasıyla ciro kaybı yaşadığını bildirdi.",
    "Şehir stadyumundaki çim bakımsızlığı, maçın ertelenmesine neden oldu.",
    "Elektrikli araç şarj istasyonlarının sık arızalanması sürücülerden tepki topladı.",
    "Turizm bölgesindeki erozyon, sahil şeridinin bir bölümünü kullanılamaz hale getirdi.",
    "Belediyenin geri dönüşüm tesisi, kapasite yetersizliği nedeniyle atık birikimine neden oldu.",
    "Bölgedeki orman varlığı, art arda yaşanan yangınlarla azalmaya devam ediyor.",
    "Kargo şirketinin teslimat süreleri, yoğun dönemde günler seviyesine uzadı.",
    "İlçe belediyesinin altyapı çalışması, yüzlerce evde su kesintisine yol açtı.",
    "Şirketin ikinci el araç satışları, faiz artışının ardından belirgin biçimde geriledi.",
    "Kentteki gölet, kuraklık nedeniyle son on yılın en düşük su seviyesine indi.",
    "Üretim tesisindeki iş kazası, bölümün geçici olarak kapatılmasına neden oldu.",
    "Yerel esnafın enerji faturaları, son düzenlemeyle iki katına çıktı.",
    "Kütüphanenin dijital arşiv projesi, teknik altyapı yetersizliği nedeniyle askıya alındı.",
    "Şehirlerarası otobüs seferlerinin sıklığı, yakıt maliyetleri gerekçesiyle azaltıldı.",
    "Fuar organizasyonuna katılımcı sayısı, geçen yıla kıyasla ciddi oranda düştü.",
    "Kentteki sokak hayvanları barınağı, kapasite doluluğu nedeniyle yeni kabul alamıyor.",
    "İlçedeki tarihi çarşının esnafı, restorasyon çalışmaları yüzünden aylardır kapalı.",
    "Havayolu şirketinin bagaj kaybı şikayetleri bu çeyrekte belirgin biçimde arttı.",
    "Şirketin ihracat rakamları, döviz kuru dalgalanmaları nedeniyle geriledi.",
    "Kentteki toplu ulaşım kartı sistemindeki arıza, saatlerce yolcu mağduriyetine yol açtı.",
    "Belediyenin çöp toplama sıklığı, ekipman eksikliği nedeniyle azaltılmak zorunda kalındı.",
    "Yerel üniversitenin yurt kapasitesi, artan öğrenci sayısını karşılayamıyor.",
    "Fabrikadaki otomasyon sistemine geçiş, yüzlerce çalışanın işine son verilmesine neden oldu.",
    "Kentteki su faturası itirazları, sayaç arızaları nedeniyle bu ay rekor seviyeye ulaştı.",
    "Sahil kesimindeki erozyon çalışmaları, öngörülen bütçeyi aşarak durduruldu.",
    "İlçe pazar yerindeki tezgah sayısı, kira artışları nedeniyle üçte bir azaldı.",
    "Otoyol güzergahındaki bakım çalışmaları, sabah saatlerinde uzun kuyruklara yol açtı.",
    "Şirketin müşteri memnuniyeti anketinde, bu çeyrekte belirgin bir düşüş kaydedildi.",
    "Kentteki içme suyu arıtma tesisinin kapasitesi, nüfus artışını karşılayamaz hale geldi.",
    "Tarım kooperatifinin depolama tesisindeki nem sorunu, ürünlerin bir kısmını kullanılamaz hale getirdi.",
    "Yerel basketbol takımının bilet satışları, art arda alınan mağlubiyetlerin ardından düştü.",
]

DOSYA = Path(__file__).resolve().parent / "zayif_uslup_veri.jsonl"

with open(DOSYA, "a", encoding="utf-8") as f:
    for metin in NEGATIF_ORNEKLER:
        f.write(json.dumps({"text": metin, "label": "negative"}, ensure_ascii=False) + "\n")

print(f"{len(NEGATIF_ORNEKLER)} negatif ornek eklendi. Toplam dosya artik guncellendi: {DOSYA}")
