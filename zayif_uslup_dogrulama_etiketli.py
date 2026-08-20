# -*- coding: utf-8 -*-
"""
Hedef zayif alt-tur (kisa/resmi/haber-bulteni tarzi, dolayli duygu ifadesi)
icin ELLE ETIKETLENMIS dogrulama seti.

ONEMLI -- BIRINCI DENEME REDDEDILDI (21.08.2026): ilk yazilan 40 ornek,
Claude tarafindan v1_v2_farklari.txt (dogrulama_v2.py'nin ciktisi, bu
oturumda az once okunmustu) okunduktan HEMEN SONRA yazildi -- konu secimi
(deprem/tutuklama/siber saldiri/sel) o dosyayla belirgin ortusuyordu, hatta
bir pozitif ornek ("Kutuphanenin calisma saatleri...") o dosyadaki tek
regresyon ornegiyle neredeyse birebir ayniydi. Kullanicinin sordugu "bu
testi kod/veriyi gormeden mi hazirladin?" sorusu haklı cikti -- test kirliydi,
%97,5 sayisi guvenilir degildi. Ayrica ilk deneme "deprem/tutuklama/mahkeme"
gibi DRAMATIK kriz kelimeleri kullaniyordu, ama zayif_uslup_veri.jsonl'deki
GERCEK egitim verisi (asagida dogrulandi) cok daha SESSIZ bir kurumsal/
ekonomik gerileme tarzinda ("su kesintisi uzadi", "butce kisildi", "kapasite
yetersiz kaldi") -- yani ilk test hem kirli hem de yanlis tarzdaydi.

BU IKINCI SURUM: (1) zayif_uslup_veri.jsonl'deki 192 negatif + 520 pozitif
ornegin TAMAMI/bir kismi taranip konu/kalip cakismasi olmadigi dogrulandi,
(2) v1_v2_farklari.txt'teki 26 konudan HICBIRI (deprem, tutuklama, sel,
siber saldiri, mahkeme, catisma, iklim raporu, deniz seviyesi, yan etki,
antibiyotik, asi karsitligi, doviz, kira, muze butce, egitime erisim, sinav
itiraz, kutuphane saatleri, mikro odeme, isten cikarma/oyun studyosu, oyun
karakteri, doga parki, istifa, sakatlik) kullanilmadi, (3) egitim verisiyle
AYNI sessiz-gerileme/sessiz-iyilesme tarzinda ama FARKLI kurum/sektorlerde
(itfaiye, veteriner, feribot, PTT, denetim, yuzme havuzu, gece otobusu,
turizm ofisi, sanat galerisi vb.) yeni cumleler yazildi.
"""

VERI = [
    # -- NEGATIF (etiket=negative), sessiz kurumsal/ekonomik gerileme tarzinda --
    ("İtfaiye ekiplerinin olay yerine ulaşma süresi bu yıl belirgin biçimde uzadı.", "negative"),
    ("Veteriner kliniklerindeki randevu bekleme süresi, personel eksikliği nedeniyle arttı.", "negative"),
    ("Feribot seferlerinin sıklığı, yakıt maliyetleri gerekçesiyle azaltıldı.", "negative"),
    ("PTT şubelerindeki kargo teslim süreleri, yoğun dönemde günler seviyesine uzadı.", "negative"),
    ("Gıda denetim ekiplerinin yıllık teftiş sayısı, kadro eksikliği nedeniyle düştü.", "negative"),
    ("Halk plajındaki cankurtaran sayısı, bütçe kısıtı nedeniyle geçen yıla göre azaldı.", "negative"),
    ("Gece otobüs seferlerinin güzergahı, düşük doluluk gerekçesiyle daraltıldı.", "negative"),
    ("Turizm danışma ofislerinin çalışma saatleri, personel yetersizliği nedeniyle kısaltıldı.", "negative"),
    ("Sanat galerisinin sergi takvimi, sponsorluk desteğinin azalmasıyla seyrekleşti.", "negative"),
    ("Belediye otobüs filosundaki arıza oranı, bakım bütçesi kısıntısıyla yükseldi.", "negative"),
    ("Semt pazarındaki denetim sıklığı, ekip sayısının azalmasıyla düştü.", "negative"),
    ("Halk kütüphanesinin süreli yayın aboneliği, bütçe kesintisiyle azaltıldı.", "negative"),
    ("İlçedeki çocuk oyun alanlarının bakım periyodu, kaynak yetersizliği nedeniyle uzadı.", "negative"),
    ("Meteoroloji istasyonlarının bakım aralığı, personel azlığı nedeniyle gecikmeye uğradı.", "negative"),
    ("Belediye fen işlerinin yol yama talebi karşılama oranı bu yıl geriledi.", "negative"),
    ("Kamu spor tesislerindeki soyunma odalarının sayısı, artan üye talebini karşılayamıyor.", "negative"),
    ("Şehir içi tramvay hattının bakım kesintisi, öngörülenden uzun sürdü.", "negative"),
    ("Belediyenin sokak aydınlatma arıza giderme süresi, ekip azlığı nedeniyle uzadı.", "negative"),
    ("Kamu otoparklarındaki güvenlik kamerası sayısı, bakım ihmali nedeniyle azaldı.", "negative"),
    ("Halk sağlığı taramalarına katılım oranı, bu yıl beklenenin altında kaldı.", "negative"),
    # -- POZITIF (etiket=positive), sessiz kurumsal/ekonomik iyilesme tarzinda --
    ("İtfaiye teşkilatına eklenen yeni araçlarla olay yerine ulaşma süresi kısaldı.", "positive"),
    ("Veteriner kliniklerinin nöbet sistemi genişletilerek acil vaka bekleme süresi azaltıldı.", "positive"),
    ("Feribot hattına eklenen yeni sefer, yolcu bekleme süresini belirgin biçimde kısalttı.", "positive"),
    ("PTT'nin dijital takip sistemi sayesinde kargo teslim süreleri kısaldı.", "positive"),
    ("Gıda denetim ekiplerinin sayısı artırılarak yıllık teftiş oranı yükseltildi.", "positive"),
    ("Halk plajlarına eklenen ek cankurtaran kadrosu güvenlik standardını yükseltti.", "positive"),
    ("Gece otobüs seferlerinin sıklığı, artan talep üzerine yükseltildi.", "positive"),
    ("Turizm danışma ofislerinin çalışma saatleri, ziyaretçi talebiyle uzatıldı.", "positive"),
    ("Sanat galerisinin yeni sponsorluk anlaşmasıyla sergi takvimi genişledi.", "positive"),
    ("Belediye otobüs filosuna eklenen yeni araçlarla arıza oranı düştü.", "positive"),
    ("Semt pazarındaki denetim ekibi büyütülerek kontrol sıklığı artırıldı.", "positive"),
    ("Halk kütüphanesinin süreli yayın koleksiyonu yeni bağışlarla genişletildi.", "positive"),
    ("İlçedeki çocuk oyun alanlarının bakım periyodu yeni ekiple kısaltıldı.", "positive"),
    ("Meteoroloji istasyonlarının bakım programı hızlandırılarak veri kalitesi yükseltildi.", "positive"),
    ("Belediye fen işlerinin yol yama talebine yanıt süresi bu yıl kısaldı.", "positive"),
    ("Kamu spor tesislerine eklenen yeni soyunma odalarıyla kapasite artırıldı.", "positive"),
    ("Şehir içi tramvay hattının bakımı planlanandan erken tamamlandı.", "positive"),
    ("Belediyenin sokak aydınlatma arıza giderme süresi yeni ekiple kısaldı.", "positive"),
    ("Kamu otoparklarına eklenen yeni kameralarla güvenlik seviyesi yükseltildi.", "positive"),
    ("Halk sağlığı taramalarına katılım, yeni bilgilendirme kampanyasıyla arttı.", "positive"),
]

if __name__ == "__main__":
    from sklearn.metrics import accuracy_score, f1_score

    from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

    def yukle(dizin):
        tok = AutoTokenizer.from_pretrained(dizin)
        mod = AutoModelForSequenceClassification.from_pretrained(dizin)
        return pipeline("sentiment-analysis", model=mod, tokenizer=tok)

    def skor(pipe, metin):
        s = pipe(metin, truncation=True)[0]
        etiket = s["label"].lower()
        return "positive" if ("pos" in etiket or etiket in ("1", "label_1")) else "negative"

    gercekler = [g for _, g in VERI]
    metinler = [m for m, _ in VERI]

    cikti = []
    for ad, dizin in [
        ("v1 (models/bert-turkish-sentiment-ince-ayarli)", "models/bert-turkish-sentiment-ince-ayarli"),
        ("v2 (models/bert-turkish-sentiment-ince-ayarli-v2)", "models/bert-turkish-sentiment-ince-ayarli-v2"),
    ]:
        pipe = yukle(dizin)
        tahminler = [skor(pipe, m) for m in metinler]
        dogruluk = accuracy_score(gercekler, tahminler)
        f1 = f1_score(gercekler, tahminler, pos_label="positive")
        yanlislar = [(m, g, t) for m, g, t in zip(metinler, gercekler, tahminler) if g != t]
        cikti.append(f"\n=== {ad} ===")
        cikti.append(f"Dogruluk: {dogruluk:.3f} ({sum(1 for g,t in zip(gercekler,tahminler) if g==t)}/{len(VERI)})")
        cikti.append(f"F1: {f1:.3f}")
        cikti.append(f"Yanlis tahminler ({len(yanlislar)}):")
        for m, g, t in yanlislar:
            cikti.append(f"  [gercek:{g:>8} tahmin:{t:>8}] {m}")

    with open("zayif_uslup_dogrulama_sonuc.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(cikti))
    print("Sonuc zayif_uslup_dogrulama_sonuc.txt dosyasina yazildi.")
