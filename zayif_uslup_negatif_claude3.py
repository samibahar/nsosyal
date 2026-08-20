# -*- coding: utf-8 -*-
"""Ucuncu tur negatif ornekler."""
import json
from pathlib import Path

NEGATIF_ORNEKLER = [
    "Kentteki müze girişlerindeki ücretlendirme değişikliği, ziyaretçi sayısını azalttı.",
    "Yerel imalatçının ihracat pazarı, rakip ülkelerin fiyat avantajı nedeniyle daraldı.",
    "Şehir merkezindeki yaya bölgesi düzenlemesi, çevredeki dükkanların cirosunu düşürdü.",
    "Kentteki kreş kapasitesi, artan başvuru sayısını karşılayamaz duruma geldi.",
    "Havayolu şirketinin uçak bakım süreleri, yedek parça tedarikinde yaşanan gecikmeyle uzadı.",
    "Bölgedeki zeytin üreticileri, bu yılki don olayı nedeniyle rekolte kaybı yaşadı.",
    "Kentteki toplu taşıma durak tabelalarının bakımsızlığı yolculardan şikayet aldı.",
    "Şirketin sosyal medya reklam harcamaları artmasına rağmen satış rakamları gerilemeye devam etti.",
    "İlçedeki su kuyularının tuzlanma oranı, tarım arazilerinin verimini düşürdü.",
    "Kentteki eski sanayi bölgesinin dönüşüm projesi, finansman sorunları nedeniyle durduruldu.",
    "Yerel spor kulübünün sponsorluk geliri, geçen sezona göre belirgin biçimde azaldı.",
    "Şehirlerarası tren seferlerindeki gecikme oranı, bu çeyrekte rekor seviyeye ulaştı.",
    "Kentteki toplu konut sitesinin ortak alan aidatları, bakım ihmali nedeniyle tartışma konusu oldu.",
    "Fabrikanın ihracat sevkiyatı, liman işçilerinin grevi nedeniyle günlerce bekletildi.",
    "Yerel kütüphanenin dijital abonelik sistemi, teknik sorunlar nedeniyle sık sık kesintiye uğruyor.",
    "Kentteki içme suyu depolarının bakım çalışması, geniş bir bölgede kesintiye yol açtı.",
    "Şirketin müşteri veri tabanı sisteminde yaşanan arıza, sipariş süreçlerini aksattı.",
    "Bölgedeki tarım kooperatifinin gübre maliyetleri, üreticilerin kar marjını daralttı.",
    "Kentteki toplu ulaşım hatlarının sıklığı, akşam saatlerinde talebi karşılayamıyor.",
    "Havalimanı pisti bakım çalışması, art arda uçuş rötarlarına neden oldu.",
    "Yerel tekstil atölyelerinin sipariş hacmi, ithal ürünlerin rekabeti nedeniyle geriledi.",
    "Kentteki toplu spor müsabakalarına seyirci ilgisi, bilet fiyatlarındaki artışla azaldı.",
    "Şirketin depo otomasyon sistemi, yazılım güncellemesi sonrası günlerce devre dışı kaldı.",
    "Bölgedeki arıcılık işletmeleri, iklim değişikliğinin etkisiyle bal üretiminde azalma yaşadı.",
    "Kentteki toplu taşıma kart bakiye yükleme noktalarının azlığı yolculardan tepki topladı.",
    "Yerel gazete dağıtım ağı, personel eksikliği nedeniyle bazı bölgelere ulaşamıyor.",
    "Şehir hastanesinin ameliyat bekleme listesi, cihaz eksikliği nedeniyle uzadı.",
    "Kentteki sanayi sitesindeki elektrik altyapısı, artan talebi karşılamakta zorlanıyor.",
    "Bölgedeki seracılık işletmeleri, doğalgaz fiyatlarındaki artış nedeniyle üretimi kıstı.",
    "Yerel belediyenin dijital vatandaş uygulaması, sık yaşanan çökmeler nedeniyle eleştirildi.",
]

DOSYA = Path(__file__).resolve().parent / "zayif_uslup_veri.jsonl"

with open(DOSYA, "a", encoding="utf-8") as f:
    for metin in NEGATIF_ORNEKLER:
        f.write(json.dumps({"text": metin, "label": "negative"}, ensure_ascii=False) + "\n")

print(f"{len(NEGATIF_ORNEKLER)} negatif ornek eklendi.")
