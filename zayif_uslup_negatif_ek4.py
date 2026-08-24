# -*- coding: utf-8 -*-
"""Dorduncu tur negatif ornekler."""
import json
from pathlib import Path

NEGATIF_ORNEKLER = [
    "Kentteki toplu taşıma filosuna eklenen yeni araçların teslimatı, tedarikçi sorunları nedeniyle ertelendi.",
    "Yerel süt üreticilerinin kooperatif borcu, düşen fiyatlar nedeniyle katlanarak arttı.",
    "Şehir merkezindeki bisiklet park alanlarının sayısı, artan talebe yetişemiyor.",
    "Kentteki eski tramvay hattının restorasyonu, bütçe yetersizliği nedeniyle askıya alındı.",
    "Havayolu şirketinin check-in sistemindeki güncelleme, saatlerce hizmet aksamasına yol açtı.",
    "Bölgedeki narenciye bahçeleri, beklenmedik don olayı nedeniyle ciddi zarar gördü.",
    "Kentteki toplu konut projelerinin teslim tarihleri, malzeme tedarik sorunları nedeniyle ötelendi.",
    "Yerel spor salonlarının üyelik ücretlerine yapılan zam, kullanıcı sayısını azalttı.",
    "Şirketin çağrı merkezindeki bekleme süreleri, yoğun şikayet dönemlerinde saatleri buldu.",
    "Kentteki nehir üzerindeki köprünün bakım çalışması, ulaşımı aylarca aksattı.",
    "Bölgedeki kümes hayvancılığı işletmeleri, yem fiyatlarındaki artıştan olumsuz etkilendi.",
    "Yerel sinema salonu, düşen izleyici sayısı nedeniyle kapanma kararı aldı.",
    "Kentteki toplu taşıma güzergah değişikliği, bazı mahallelerin erişimini zorlaştırdı.",
    "Şirketin lojistik ağındaki aksaklık, teslimat sürelerini beklenenin iki katına çıkardı.",
    "Bölgedeki bağcılık üreticileri, dolu yağışı nedeniyle önemli ürün kaybı yaşadı.",
    "Kentteki toplu konut yönetiminin asansör bakım ihmali, sakinlerden şikayet aldı.",
    "Yerel gazetenin dijital dönüşüm süreci, personel azaltımıyla birlikte yürütülmek zorunda kaldı.",
    "Şehir merkezindeki otopark ücretlerine yapılan zam, esnaf tarafından protesto edildi.",
    "Kentteki içme suyu şebekesindeki eskimiş borular, sık su kesintilerine neden oluyor.",
    "Bölgedeki tekstil fabrikalarının ihracat siparişleri, kur dalgalanmaları nedeniyle azaldı.",
    "Yerel belediyenin geri dönüşüm kampanyasına katılım oranı, beklentinin altında kaldı.",
    "Kentteki toplu ulaşım araçlarının klima arızaları, yaz aylarında yolcu şikayetlerini artırdı.",
    "Şirketin depo kirası, bölgedeki emlak fiyatlarındaki artışla birlikte ciddi yükseldi.",
    "Bölgedeki balık çiftlikleri, su sıcaklığındaki değişim nedeniyle verim kaybı yaşadı.",
    "Kentteki eski pazar yerinin yenileme projesi, esnafın geçici taşınmasına neden oldu.",
    "Yerel taksi durağındaki araç sayısı, artan talebi karşılayamaz duruma geldi.",
    "Şehir stadyumunun aydınlatma sistemi arızası, gece maçının ertelenmesine yol açtı.",
    "Kentteki toplu taşıma kartı otomatlarının sık arızalanması yolcu yoğunluğuna neden oldu.",
    "Bölgedeki fındık üreticileri, düşen dünya fiyatları nedeniyle gelir kaybı yaşadı.",
    "Yerel itfaiye teşkilatının araç filosu, bakım eksikliği nedeniyle sık arıza veriyor.",
    "Kentteki toplu konut alanındaki güvenlik kamerası sistemi, aylardır devre dışı durumda.",
    "Şirketin üretim tesisindeki hammadde stoku, tedarik gecikmesi nedeniyle tükendi.",
    "Bölgedeki seracılık üreticileri, elektrik kesintileri nedeniyle ürün kaybı bildirdi.",
    "Kentteki eski su kemerinin çevresindeki yapılaşma, tarihi dokuya zarar verdi.",
    "Yerel esnafın kredi kartı komisyon oranları, bu yıl belirgin biçimde yükseldi.",
    "Şehir merkezindeki yaya geçitlerinin aydınlatma eksikliği, kaza riskini artırdı.",
    "Kentteki toplu taşıma seferlerinin gece saatlerinde sıklığı, talebi karşılayamıyor.",
    "Bölgedeki mandıra işletmeleri, soğuk hava deposu maliyetleri nedeniyle zarar etti.",
    "Yerel kültür merkezinin etkinlik takvimi, bütçe kesintisi nedeniyle daraltıldı.",
    "Şirketin ihracat gümrük süreçlerindeki gecikme, teslim tarihlerini olumsuz etkiledi.",
]

DOSYA = Path(__file__).resolve().parent / "zayif_uslup_veri.jsonl"

with open(DOSYA, "a", encoding="utf-8") as f:
    for metin in NEGATIF_ORNEKLER:
        f.write(json.dumps({"text": metin, "label": "negative"}, ensure_ascii=False) + "\n")

print(f"{len(NEGATIF_ORNEKLER)} negatif ornek eklendi.")
