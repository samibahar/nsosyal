# -*- coding: utf-8 -*-
"""Ikinci tur negatif ornekler -- ayni kurallar, farkli konular/cumleler
(birinci turla tekrar etmeyecek sekilde)."""
import json
from pathlib import Path

NEGATIF_ORNEKLER = [
    "Belediyenin yeni otopark ücret tarifesi, çevre esnafından yoğun şikayet aldı.",
    "Şehir hastanesindeki MR cihazının arızalanması, randevuları bir aya kadar erteledi.",
    "Yerli otomobil markasının ihracat siparişleri, gümrük vergisi artışının ardından azaldı.",
    "İlçedeki spor salonunun çatısı, geçen haftaki fırtınada hasar gördü.",
    "Havayolu şirketinin yer hizmetleri personeli, ücret anlaşmazlığı nedeniyle iş bıraktı.",
    "Kentteki elektrik dağıtım şirketinin arıza giderme süresi bu yıl uzadı.",
    "Tarım ilacı kullanımındaki artış, bölgedeki arı popülasyonunu olumsuz etkiledi.",
    "Otobüs terminalindeki bilet gişelerinin sayısı, yolcu yoğunluğuna yetişemiyor.",
    "Şirketin Ar-Ge bütçesi, geçtiğimiz yıl planlanan hedefin gerisinde kaldı.",
    "Kentteki gölün su seviyesi, sanayi atıklarının etkisiyle giderek kirlendi.",
    "Üniversite kampüsündeki yurt ücretlerine yapılan zam, öğrenciler arasında tepkiyle karşılandı.",
    "Bölgedeki balıkçı teknelerinin sayısı, azalan stoklar nedeniyle her yıl düşüyor.",
    "Fabrika işçilerinin fazla mesai ücretleri, üç aydır düzenli ödenemiyor.",
    "Kentteki tarihi hamamın restorasyon süreci, öngörülen sürenin iki katına çıktı.",
    "Otoyol gişelerindeki elektronik geçiş sistemi arızası, uzun araç kuyruklarına yol açtı.",
    "Yerel çiftçilerin süt üretimi, yem fiyatlarındaki artış nedeniyle karlılığını yitirdi.",
    "Şehir merkezindeki AVM'nin ziyaretçi sayısı, art arda üçüncü çeyrekte azaldı.",
    "Kentteki toplu taşıma filosundaki araçların yaş ortalaması, bütçe kısıtı nedeniyle yükseliyor.",
    "İlçe belediyesinin park bakım ekibi, personel eksikliği nedeniyle işlerini aksatıyor.",
    "Havalimanı çevresindeki tarım arazileri, genişleme çalışmaları nedeniyle imara açıldı.",
    "Bankanın kredi başvuru onay süreleri, artan talep karşısında haftalar seviyesine uzadı.",
    "Kentteki sinema salonlarının sayısı, dijital yayın platformlarının etkisiyle azaldı.",
    "Sanayi bölgesindeki atık su arıtma tesisi, kapasite yetersizliği nedeniyle sık arızalanıyor.",
    "Yerel işletmelerin enerji verimliliği yatırımları, yüksek maliyet nedeniyle ertelendi.",
    "Kentteki bisiklet paylaşım sisteminin araç sayısı, bakımsızlık nedeniyle giderek azaldı.",
    "Okul servis araçlarının güzergah değişikliği, velilerden yoğun tepki topladı.",
    "Şirketin depo yangını, stoklarının önemli bir kısmının kullanılamaz hale gelmesine yol açtı.",
    "Kentteki içme suyu şebekesindeki kayıp oranı, denetim raporuna göre yükseldi.",
    "Tersanedeki gemi inşa siparişleri, uluslararası talep daralmasıyla azaldı.",
    "Yerel esnafın ödeme sistemine geçiş sürecinde yaşanan aksaklıklar satışları etkiledi.",
    "Kentteki toplu konut alanındaki asansör arızaları, sakinlerden şikayet aldı.",
    "Havza genelindeki yağış miktarı, son on yılın en düşük seviyesinde gerçekleşti.",
    "Şirketin çağrı merkezi personel devir oranı, bu yıl belirgin biçimde arttı.",
    "Kentteki pazar yerlerinin hijyen denetimlerinde art arda eksiklikler tespit edildi.",
    "Demiryolu hattındaki bakım çalışması, sefer sayısını geçici olarak yarıya indirdi.",
    "Yerel gazetecilik kuruluşunun reklam gelirleri, dijital rekabet nedeniyle daraldı.",
    "Kentteki toplu spor tesislerinin bakım eksikliği, kullanıcı sayısını azalttı.",
    "Fabrikadaki hammadde tedarik zincirindeki aksaklık, üretim planını geciktirdi.",
    "Şehir merkezindeki otopark kapasitesi, artan araç sayısını karşılayamıyor.",
    "Kentteki atık yönetimi sisteminin geri dönüşüm oranı, hedeflenen seviyenin altında kaldı.",
    "İlçedeki eczanelerin nöbet sistemi, personel yetersizliği nedeniyle aksadı.",
    "Yerel üreticilerin ihracat belgesi süreçlerindeki bürokrasi, teslimat sürelerini uzattı.",
    "Kentteki spor kulübünün altyapı tesisleri, bakım bütçesi kesintisiyle kullanılamaz hale geldi.",
    "Havalimanındaki check-in kuyrukları, sistem yavaşlaması nedeniyle saatlerce uzadı.",
    "Şirketin üretim hattındaki robotik sistem arızası, teslimat takvimini aksattı.",
    "Kentteki nehir kıyısındaki yürüyüş yolu, sel baskını sonrası aylarca kapalı kaldı.",
    "Yerel restoranların gıda maliyetleri, tedarik sorunları nedeniyle öngörülemez biçimde arttı.",
    "Kentteki toplu ulaşım abonman sistemine geçişte yaşanan aksaklıklar yolcuları mağdur etti.",
]

DOSYA = Path(__file__).resolve().parent / "zayif_uslup_veri.jsonl"

with open(DOSYA, "a", encoding="utf-8") as f:
    for metin in NEGATIF_ORNEKLER:
        f.write(json.dumps({"text": metin, "label": "negative"}, ensure_ascii=False) + "\n")

print(f"{len(NEGATIF_ORNEKLER)} negatif ornek eklendi.")
