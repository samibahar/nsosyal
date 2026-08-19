# -*- coding: utf-8 -*-
"""Rapor YAZARKEN kaynak olarak kullanılacak ikinci PDF -- prototip özeti
DEĞİL (bkz. pdf_olustur.py / NSosyal_Teknik_Ozet.pdf). Bu belge: literatür
savunmaları, uygulanabilirlik verileri, problem-motivasyon araştırmaları ve
prototipe EKLEMEDİĞİMİZ ama rapora yazılacak gelecek-vizyon fikirlerini
topluyor. 19.08.2026 gecesi, kullanıcı isteğiyle üretildi."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, ListFlowable,
    ListItem, HRFlowable, PageBreak,
)

_FONT_DIZIN = r"C:\Windows\Fonts"
pdfmetrics.registerFont(TTFont("Arial", f"{_FONT_DIZIN}\\arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", f"{_FONT_DIZIN}\\arialbd.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Italic", f"{_FONT_DIZIN}\\ariali.ttf"))

DOSYA = "NSosyal_Rapor_Icerigi.pdf"
KENAR_BOSLUGU = 2.2 * cm
KULLANILABILIR_GENISLIK = A4[0] - 2 * KENAR_BOSLUGU

renk_ana = colors.HexColor("#7c3aed")
renk_metin = colors.HexColor("#16211f")
renk_muted = colors.HexColor("#55625e")
renk_cizgi = colors.HexColor("#d8ddda")
renk_kutu = colors.HexColor("#f2eefc")

styles = getSampleStyleSheet()
stil_baslik = ParagraphStyle("Baslik", parent=styles["Title"], fontName="Arial-Bold",
                              fontSize=20, textColor=renk_metin, spaceAfter=4)
stil_alt = ParagraphStyle("Alt", parent=styles["Normal"], fontName="Arial",
                           fontSize=11, textColor=renk_muted, spaceAfter=18)
stil_h1 = ParagraphStyle("H1", parent=styles["Heading1"], fontName="Arial-Bold",
                          fontSize=14.5, textColor=renk_ana, spaceBefore=18, spaceAfter=8)
stil_h2 = ParagraphStyle("H2", parent=styles["Heading2"], fontName="Arial-Bold",
                          fontSize=11.5, textColor=renk_metin, spaceBefore=10, spaceAfter=4)
stil_govde = ParagraphStyle("Govde", parent=styles["Normal"], fontName="Arial",
                             fontSize=10, leading=14.5, textColor=renk_metin, spaceAfter=6,
                             alignment=TA_LEFT)
stil_kucuk = ParagraphStyle("Kucuk", parent=styles["Normal"], fontName="Arial-Italic",
                             fontSize=9, leading=13, textColor=renk_muted, spaceAfter=6)
stil_liste = ParagraphStyle("Liste", parent=stil_govde, leftIndent=12, spaceAfter=4)
stil_hucre = ParagraphStyle("Hucre", parent=stil_govde, fontSize=8.7, leading=11.5, spaceAfter=0)
stil_hucre_baslik = ParagraphStyle("HucreBaslik", parent=stil_hucre, fontName="Arial-Bold",
                                     textColor=colors.white)
stil_uyari = ParagraphStyle("Uyari", parent=stil_govde, fontName="Arial-Bold",
                             fontSize=9.5, textColor=colors.HexColor("#92400e"), spaceAfter=6)

story = []

def h1(t): story.append(Paragraph(t, stil_h1))
def h2(t): story.append(Paragraph(t, stil_h2))
def p(t): story.append(Paragraph(t, stil_govde))
def kucuk(t): story.append(Paragraph(t, stil_kucuk))
def uyari(t): story.append(Paragraph(t, stil_uyari))
def cizgi(): story.append(HRFlowable(width="100%", thickness=0.75, color=renk_cizgi, spaceBefore=6, spaceAfter=10))
def bosluk(h=6): story.append(Spacer(1, h))
def sayfa(): story.append(PageBreak())

def madde(satirlar):
    items = [ListItem(Paragraph(s, stil_liste), leftIndent=14) for s in satirlar]
    story.append(ListFlowable(items, bulletType="bullet", start="•", bulletColor=renk_ana, bulletFontSize=8))
    bosluk(4)

def tablo(basliklar, satirlar, genislikler):
    assert abs(sum(genislikler, 0 * cm) - KULLANILABILIR_GENISLIK) < 0.3 * cm, (
        f"Tablo genişliği sayfaya sığmıyor: {sum(genislikler, 0*cm)/cm:.1f}cm "
        f"(sınır {KULLANILABILIR_GENISLIK/cm:.1f}cm)"
    )
    veri = [[Paragraph(str(h), stil_hucre_baslik) for h in basliklar]]
    for satir in satirlar:
        veri.append([Paragraph(str(hucre), stil_hucre) for hucre in satir])
    t = Table(veri, colWidths=genislikler, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), renk_ana),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, renk_kutu]),
        ("GRID", (0, 0), (-1, -1), 0.5, renk_cizgi),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
    ]))
    story.append(t)
    bosluk(10)


# ============================================================ BAŞLIK
story.append(Paragraph("NSosyal — Rapor İçeriği Kaynağı", stil_baslik))
story.append(Paragraph(
    "24 Ağustos teknik rapor yazımı için kaynak belge (prototip özeti DEĞİL) · "
    "TEKNOFEST NSosyal İnovasyon Yarışması · 19 Ağustos 2026", stil_alt))
cizgi()
p("Bu belge, <b>NSosyal_Teknik_Ozet.pdf</b>'ten farklı bir amaca hizmet ediyor: o belge "
  "\"şu an gerçekten çalışan ne var\"ı anlatıyordu, bu belge ise raporu YAZARKEN ihtiyaç "
  "duyacağın malzemeyi topluyor — literatür savunmaları, uygulanabilirlik kanıtları, problem "
  "motivasyonu ve (dürüstçe işaretlenmiş) prototipe eklemediğimiz gelecek-vizyon fikirleri.")

# ============================================================ 1. LİTERATÜR SAVUNMALARI
h1("1. Literatürdeki Savunmalarımız")
p("19.08.2026 gecesi gerçek kaynaklarla yapılan taramadan (literatur_bulgulari.md) — "
  "hiçbir atıf uydurulmadı, hepsi WebSearch ile doğrulandı.")

h2("1.1 — Doğrulama döngümüz: EMA / micro-EMA'nın bağımsız bir uygulaması")
p("Kullanıcıya ara sıra \"şu an gerçekte nasıl hissediyorsun?\" sorma mekanizmamız, "
  "psikolojide <b>Ecological Momentary Assessment (EMA)</b> / <b>Experience Sampling Method "
  "(ESM)</b> olarak bilinen, yerleşik bir araştırma yönteminin bağımsız bir yeniden keşfi.")
madde([
    "<b>JMIR 2024;26:e50275</b> — \"Investigating Best Practices for Ecological Momentary "
    "Assessment\": soru SAYISININ artması uyumu (compliance) düşürüyor, ama örnekleme "
    "SIKLIĞI tek başına uyumla ilişkili değil → \"az soru, sık sorma\" prensibi bizim "
    "\"her ~8 etkileşimde tek soru\" tasarımımızla birebir uyumlu.",
    "<b>PMC7991987</b> — \"Measuring Criterion Validity of Microinteraction EMA\": "
    "tek-soruluk mikro-EMA'nın, araştırma sınıfı sürekli sensörle tutarlı kriter geçerliliği "
    "taşıdığını gösteriyor.",
    "<b>arXiv:2007.14461</b> — \"Modeling Behaviour to Predict User State: Self-Reports as "
    "Ground Truth\": ESM öz-bildirimlerinin ML modelleri için ground-truth olarak "
    "kullanıldığını belgeliyor, AMA tekrarlı sorgunun kullanıcı yorgunluğuna yol açabileceği "
    "riskini de not ediyor — biz de bunu bir sınırlılık olarak yazmalıyız.",
])
p("<b>Raporda nasıl kullanılır:</b> \"Bu mekanizma tesadüfen değil, psikolojide yerleşik bir "
  "yöntemin hafif bir uygulaması\" de. Kullanıcı yorgunluğu riskini dürüstçe bir sınırlılık "
  "olarak da yaz.")

h2("1.2 — Pasif kullanım / dwell-time / doomscrolling: kanıt ORTA güçte, abartma")
madde([
    "<b>JCMC 29(1), 2024</b> (141 çalışmalık meta-analiz): pasif kullanımın olumsuz "
    "sonuçlarla ilişkisi genelde KÜÇÜK/DEĞİŞKEN; sosyal kaygıyla ilişki sadece 3 çalışmaya "
    "dayanıyor (zayıf kanıt).",
    "<b>ScienceDirect 2024</b>, \"Beyond the Scroll: Intolerance of Uncertainty... "
    "Doomscrolling\": doomscrolling kaygı/stres/kontrol kaybıyla ilişkili (destekleyici) "
    "ama çoğu çalışma kesitsel — nedensellik kanıtlanmamış.",
])
p("<b>Raporda nasıl kullanılır:</b> \"Uzun pasif dwell-time = olumsuz spiral\" varsayımımızı "
  "KESİN değil \"olası örüntü\" diliyle sun. Abartılı nedensellik iddiası kurma.")

h2("1.3 — Davranıştan duygu-durumu çıkarımı (digital phenotyping): meşru ama sınırlı")
p("<b>JMIR 2025</b>, \"Passive Sensing for Mental Health Monitoring Using ML: Scoping "
  "Review\": GPS + telefon kullanımıyla depresyon şiddeti sınıflandırmasında %86.5 doğruluk, "
  "PHQ-9 ile r=-0.63 bildirilmiş. AMA: eksik veri ve sınırlı dış geçerlilik önemli önyargı "
  "kaynağı; kişiselleştirilmiş modellerde tahmin gücünün büyük kısmının \"kişi kimliği\" "
  "değişkeninden geldiği bulunmuş (zaman içindeki değişimden değil).")
p("<b>Raporda nasıl kullanılır:</b> Bu alan meşru bir araştırma alanı (yaklaşımımızı "
  "destekler) AMA kişiye-özgü kalibrasyon olmadan güvenilirlik sınırlı — "
  "psikolojik_durum.py'nin şu an genellenmiş (kişiye özelleşmemiş) olduğunu bilinen bir "
  "sınırlılık olarak yaz. Gelecek iş önerisi: kullanıcı bazlı kalibrasyon (doğrulama "
  "döngüsünün topladığı veriyle) — bkz. §4.")

h2("1.4 — Refah-farkında (wellbeing-aware) sıralama: akademik emsalimiz var")
madde([
    "<b>arXiv:2102.04211</b> — \"Challenging Social Media Threats using Collective "
    "Well-being Aware Recommendation Algorithms\": \"Collective Well-Being aware "
    "Recommender Systems (CWB-RS)\" kavramı — etkileşim optimizasyonu yerine uzun-vadeli "
    "kümülatif refahı maksimize etmeyi öneriyor. Bizim iki-katmanlı (ilgi+refah) motorumuzla "
    "kavramsal paralel.",
    "<b>Georgetown KGI, Mart 2025</b> — \"Better Feeds: Algorithms That Put People First\": "
    "endüstri/politika düzeyinde \"insan-öncelikli\" sıralama ilkeleri.",
])
p("<b>Raporda nasıl kullanılır:</b> \"Yenilikçilik ve Özgünlük\" / \"Problemi Çözme "
  "Başarısı\" kriterlerinde akademik emsal olarak referans ver — fikrimiz havada değil.")

h2("1.5 — Algoritmik şeffaflık: \"az ama net\" ilkesi")
p("<b>World Wide Web journal (Springer)</b>, \"Explainable recommendation: when design "
  "meets trust calibration\": açıklamalar genelde güveni/memnuniyeti artırır, AMA nüans: çok "
  "detaylı açıklama \"algorithmic aversion\"a (kullanıcı nasıl çalıştığını öğrenince "
  "güvenmemeye başlaması) yol açabilir.")
p("<b>Raporda/tasarımda nasıl kullanılır:</b> Şeffaflık panelini \"az ama net\" tut — mevcut "
  "tasarım (kısa açıklama cümlesi + birkaç çubuk) zaten bu yönde, aşırı teknik detaya "
  "kaymaktan kaçın.")

sayfa()

# ============================================================ 2. UYGULANABİLİRLİK VERİLERİ
h1("2. Uygulanabilirliğini Gösteren Veriler")
p("\"Teknik Yeterlilik ve Uygulanabilirlik\" kriteri bu temada en ağırlıklı (%35) — bu "
  "yüzden \"çalışıyor\" demek yetmiyor, ÖLÇTÜĞÜMÜZ gerçek sayıları göstermek gerekiyor:")
tablo(
    ["Bileşen", "Ölçülen sonuç", "Nasıl doğrulandı"],
    [
        ["BERT duygu modeli", "%94.3 doğruluk (fine-tuning sonrası, %69.8'den)",
         "Bağımsız 1000 örneklik test seti, vendor iddiasından (%95.4) ayrı ölçüldü, veri sızıntısı korumalı split"],
        ["Spiral tespiti (lojistik regresyon)", "Doğruluk 0.714, F1 0.748",
         "Senaryo-bazlı sentetik veri, train/test ayrımı"],
        ["Psikolojik durum (5 kategori)", "F1 makro 0.704",
         "\"Sinirli\" kategorisine geçince bulunan ölçek sorunu StandardScaler ile düzeltildi (0.686→0.704), dürüstçe raporlandı"],
        ["Kendi kendini doğrulama döngüsü", "Mekanizma canlı test edildi, çalışıyor",
         "Gerçek etkileşimde (negatif içerik + roket/yorum) model \"sinirli\" tahmin etti, kullanıcı onayıyla eşleşti"],
        ["Kişiselleştirme (online learning)", "partial_fit ile gerçek model kayması gözlemlendi",
         "\"Varsayılan/Kişiselleştirilmiş\" anahtarıyla aynı oturumda karşılaştırmalı test"],
        ["LLM haftalık rapor (Gemini)", "Uçtan uca canlı üretim doğrulandı",
         "Gerçek oturum verisiyle üç doğru bölümlü, teşhis dili içermeyen rapor üretildi"],
    ],
    genislikler=[4.2*cm, 5.7*cm, 6.7*cm],
)
p("<b>Raporda nasıl kullanılır:</b> Bu tabloyu (veya özetini) \"Teknik Yeterlilik\" bölümünün "
  "merkezine koy. Vurgu şu olmalı: HER sayı bağımsız ölçüldü, vendor/ilk-varsayım iddiasına "
  "güvenilmedi, kötü çıkan sonuçlar (F1 düşüşü gibi) saklanmadı, kök nedeni bulunup "
  "düzeltildi. Bu, tek başına yüksek bir doğruluk rakamından daha güçlü bir metodolojik "
  "olgunluk kanıtı.")

sayfa()

# ============================================================ 3. NEDEN İHTİYAÇ VAR
h1("3. Neden Böyle Bir Şeye İhtiyaç Var — Problem Motivasyonu")
p("Bunlar akademik makaleler değil, kamuya mal olmuş, geniş çapta haber yapılmış gerçek "
  "olaylar/belgeler — raporun \"Problem Tanımı\" bölümünde \"bu neden önemli\" sorusuna "
  "somut kanıt olarak kullanılabilir. Kaynak göstererek (gazetecilik kaynağı olarak) kullan, "
  "akademik atıf gibi sunma.")

h2("3.1 — Facebook'un kendi iç araştırması: öfke en yüksek etkileşimi üretiyor")
p("2021'de Wall Street Journal'ın \"The Facebook Files\" dizisi (ve ardından Frances "
  "Haugen'in ABD Kongresi'ne sunduğu iç belgeler), Facebook'un kendi veri biliminin "
  "\"öfke\" tepkisini içeren gönderilerin diğer duygulara göre çok daha fazla etkileşim "
  "aldığını bulduğunu ortaya koydu. Şirket 2017-2018'de \"öfke\" tepkisini algoritmada "
  "beğeniden 5 kat daha ağırlıklandırmış, iç araştırmacılar bunun kutuplaştırıcı/yanlış "
  "bilgi içeren içeriği ödüllendirdiğini fark edince bu ağırlık sonradan düşürülmüştü.")
p("<b>Bizim için anlamı:</b> \"en yüksek etkileşim\" hedefiyle optimize edilen sıralama "
  "sistemlerinin olumsuz/kutuplaştırıcı içeriği DOĞAL OLARAK ödüllendirme eğiliminde "
  "olduğunun somut, belgelenmiş kanıtı. Refah-katmanımızın (etkileşim değil, refah "
  "optimize eden) neden gerekli olduğunun ana motivasyonu budur.")

h2("3.2 — 2017: kırılgan gençlerin duygu durumuna göre reklam hedeflemesi")
p("2017'de The Australian gazetesi, Facebook'un Avustralya/Yeni Zelanda pazarlama "
  "ekibinin hazırladığı sızdırılmış bir iç belgeyi haberleştirdi: belge, platformun "
  "algoritmalarının gençlerin ne zaman \"değersiz\", \"güvensiz\", \"stresli\" veya "
  "\"başarısız\" hissettiğini tespit edebildiğini ve bunun reklamcılar için bir hedefleme "
  "fırsatı olarak sunulduğunu gösteriyordu. Haber büyük bir kamuoyu tepkisine yol açtı.")
p("<b>Bizim için anlamı:</b> Bu, tam olarak yapmamayı seçtiğimiz şeyin somut, gerçek bir "
  "örneği. Sistemimiz kırılgan duygusal durumda reklamı HEDEFLEMEK yerine BASTIRIYOR — "
  "bu tarihsel olayın doğrudan tersini yapan bir tasarım kararı olarak raporda çerçevelenebilir.")

h2("3.3 — Olumsuz haberler olumludan kat kat daha fazla yayılıyor")
p("Bu, \"neden bir refah katmanına ihtiyaç var\"ı destekleyen belki de en doğrudan bulgu — "
  "ve akademik olarak sağlam (WebSearch ile doğrulandı):")
madde([
    "<b>\"Negativity drives online news consumption\"</b>, Nature Human Behaviour, 2023 — "
    "https://www.nature.com/articles/s41562-023-01538-4 (PMC10202797). ~105.000 haber "
    "başlığı varyasyonu analiz edildi: ortalama uzunlukta bir başlıkta HER EK negatif "
    "kelime tıklama oranını %2.3 artırıyor, pozitif kelimeler ise tıklamayı azaltıyor.",
    "<b>\"Negative online news articles are shared more to social media\"</b>, Scientific "
    "Reports (Nature), 2024 — https://www.nature.com/articles/s41598-024-71263-z "
    "(PMC11405697). Haber kuruluşlarının resmi Twitter hesaplarından paylaşımlar analiz "
    "edildi: olumsuz ifade edilmiş haberler belirgin şekilde daha fazla retweet alıyor.",
    "<b>\"Negativity Spreads More than Positivity on Twitter...\"</b>, PMC9383030 — hem "
    "olumlu hem olumsuz siyasi olaylardan sonra olumsuzluğun Twitter'da daha fazla "
    "yayıldığını gösteriyor.",
])
p("<b>Raporda nasıl kullanılır:</b> Bu, Facebook'un kendi iç bulgusuyla (§3.1) birlikte "
  "\"etkileşim-optimize sistemler olumsuz içeriği yapısal olarak ödüllendirir\" tezinin "
  "akademik kanıdı. \"Kat kat fazla\" ifadesi yerine somut sayıyı (\"her ek negatif kelime "
  "%2.3 daha fazla tıklama\") kullanmak daha güçlü ve daha savunulabilir — abartılı "
  "genellemeden kaçının.")

h2("3.4 — Genel bağlam: doomscrolling ve pasif tüketimin yaygınlığı")
p("§1.2'deki JCMC meta-analizi ve ScienceDirect doomscrolling çalışması da burada "
  "problem-motivasyonu olarak tekrar kullanılabilir: pasif/olumsuz içerik tüketiminin "
  "kesin nedensellik kanıtlanmamış olsa da kaygı/stres ile tutarlı şekilde ilişkilendirildiği "
  "gösteriliyor — \"neden bir refah katmanına ihtiyaç var\" sorusuna literatür + gerçek olay "
  "ikilisiyle cevap verilebilir.")

sayfa()

# ============================================================ 4. GELECEK VİZYON
h1("4. Eklenebilecek Ama Prototipe Eklemediğimiz Fikirler (Gelecek Vizyonu)")
uyari("ÖNEMLİ: Bu bölümdeki HİÇBİR ÖĞE prototipte çalışmıyor. Raporda bunları \"gelecek "
      "vizyonu / önerilen genişletme\" olarak AÇIKÇA işaretle — mevcut prototipin bir "
      "parçasıymış gibi sunma. Bu, projenin baştan beri sürdürdüğü dürüstlük disiplininin "
      "devamı.")

h2("4.1 — Perspektif Köprüsü")
p("<b>Konsept:</b> kullanıcı bir konuda yoğun/tek taraflı duygusal içerik tüketirken "
  "(spiral tespit edildiğinde), aynı konuda FARKLI/dengeleyici bir bakış açısı sunan içeriği "
  "nazikçe önerme.")
p("<b>İkinci sayfa fikri — 'çözülebilir tarafı' göstermek:</b> kullanıcının takılı kaldığı "
  "konunun karşıt bir SİYASİ görüşünü değil, aynı sorunun daha olumlu/çözüme-dönük bir "
  "yönünü gösteren bir gönderi getirmek — örneğin kullanıcı bir sorunda (ekonomi, sağlık, "
  "afet vb.) olumsuz/çaresizlik hissi veren içerikte takılı kalmışsa, aynı konuda bir "
  "çözüm/iyileşme/ilerleme haberini köprü olarak sunmak. Bu, \"solutions journalism\" "
  "(çözüm gazeteciliği) yaklaşımıyla örtüşüyor ve konu-nötr ilkesini korumak daha kolay — "
  "siyasi taraf değiştirmiyor, aynı konunun umut veren tarafını gösteriyor.")
p("<b>Neden şimdi eklemedik:</b> Zaman kısıtı asıl sebep, ama teknik olarak da ciddi bir "
  "tasarım sorusu çözülmeli: \"farklı/çözüme-dönük bakış açısı\" hangi sinyalle "
  "belirlenecek? Sistemimizin temel ilkesi KONU-NÖTR olması ve siyasi/dini içerik "
  "kategorisine göre karar VERMEMESİ (bkz. §9, Teknik Özet PDF'i) — \"çözülebilir tarafı\" "
  "versiyonu bu ilkeyi (klasik \"karşıt görüş\" versiyonuna göre) daha az ihlal ediyor "
  "çünkü siyasi taraf değil duygusal ton (umutsuzluk → umut) eksenine dayanıyor, ki bu "
  "zaten mevcut sistemin ölçtüğü bir şey (duygu skoru). Raporda hem fikri hem de bu "
  "gerilimi dürüstçe yazmak, \"düşünülmemiş\" değil \"bilerek dikkatli davranılmış\" "
  "izlenimi verir.")

h2("4.2 — Dijital Refah Ağacı (avatar/görselleştirme)")
p("<b>Konsept:</b> haftalık/aylık rapor metninin yanında, kullanıcının refah eğilimini "
  "zaman içinde temsil eden gamified bir görsel metafor (örn. büyüyen/solan bir ağaç "
  "avatarı) — mevcut metin-ağırlıklı raporun tamamlayıcısı.")
p("<b>Neden şimdi eklemedik:</b> Görsel/animasyon tasarımı zaman alıcı; mevcut metin+çubuk "
  "grafik raporu (rapor.html) zaten \"az ama net\" ilkesine uygun ve şeffaflık literatürüyle "
  "(§1.5) destekleniyor. Gamification eklemek UX'i güçlendirebilir ama aynı zamanda \"az ama "
  "net\"in tam tersi bir karmaşıklaşma riski taşır — dikkatli tasarlanmalı.")

h2("4.3 — Dinamik Sürtünme")
p("<b>Konsept:</b> spiral seviyesi yükseldiğinde, sadece renk doygunluğunu azaltmak "
  "(bkz. Teknik Özet PDF'i §7) değil, kaydırma deneyimine küçük bir \"sürtünme\" eklemek "
  "(örn. hafif bir duraklama, bir onay adımı) — kompulsif kaydırmayı kırmaya yönelik.")
p("<b>Neden şimdi eklemedik:</b> Renk doygunluğu azaltma zaten uygulanan, test edilmiş ve "
  "\"engelleyici değil fark ettirici\" ilkesine sadık bir müdahale. Sürtünme eklemek daha "
  "agresif bir müdahale sayılır — kullanıcı özerkliğini kısıtlama riski, dikkatli UX "
  "araştırması gerektirir, kanıt-of-konsept aşamasında öncelik verilmedi.")

h2("4.4 — Sıfır-Veri / Uçta İşleme + Federe Öğrenme")
uyari("DİKKAT: Bu, arkadaşımızın önerisiyle geldi ve mevcut mimariyi YANLIŞ tarif ediyordu "
      "— raporda MUTLAKA \"gelecek vizyonu\" olarak çerçevelenmeli, mevcut prototipin nasıl "
      "çalıştığı gibi ASLA sunulmamalı.")
p("<b>Konsept:</b> duygu/davranış analizinin sunucuya hiç veri göndermeden, kullanıcının "
  "cihazında (uçta) çalışması; kişiselleştirme de merkezi bir sunucuda değil, federe "
  "öğrenme (federated learning) ile cihazlar arasında model güncellemesi paylaşılarak "
  "yapılması — gizlilik açısından güçlü bir gelecek yönü.")
p("<b>Gerçek durum:</b> mevcut prototip <b>%100 sunucu-taraflı</b> çalışıyor — BERT modeli, "
  "spiral/psikolojik sınıflandırıcılar, sıralama motoru, kişiselleştirme (SGD partial_fit) "
  "hepsi backend/main.py'de, FastAPI sunucusunda çalışıyor. Bunun tam tersini iddia etmek "
  "ciddi bir dürüstlük hatası olurdu. Raporda \"şu an sunucu-taraflı çalışıyor, ileride "
  "gizlilik için uçta işlemeye taşınabilir\" şeklinde açıkça yazılmalı.")

h2("4.5 — Kişiye-Özgü Kalibrasyon (literatürden gelen öneri, §1.3)")
p("<b>Konsept:</b> psikolojik_durum.py şu an TÜM kullanıcılar için aynı sentetik senaryo "
  "verisiyle eğitilmiş, genellenmiş bir model. Literatür (§1.3) kişiye-özgü kalibrasyon "
  "olmadan güvenilirliğin sınırlı olduğunu gösteriyor.")
p("<b>Kısmen var, tam değil:</b> kişiselleştirme mekanizması (online SGD, bkz. Teknik Özet "
  "§9) bunun bir kanıt-of-konsepti — ama gerçek üretim kalitesinde (binlerce kullanıcı, "
  "düzenlileştirme/sınır ile korunan, aylarca veriyle kalibre edilen) bir kişiye-özgü "
  "kalibrasyon henüz yok. Raporda bu ayrımı (kanıt-of-konsept var, üretim-hazır kalibrasyon "
  "yok) net yap.")

sayfa()

# ============================================================ 5. İŞ MODELİ
h1("5. İş Modeli / Sürdürülebilirlik Fikirleri")
p("Bu temada (Sosyal Yapay Zekâ) iş modeli/sürdürülebilirlik kriterinin puana katkısı YOK "
  "(%0 ağırlık) — ama rapor şablonu muhtemelen yine de bir bölüm istiyor. Fazla zaman "
  "harcamadan kısa tutulabilir. NSosyal vakıf tabanlı olduğu için klasik reklam modeli "
  "ZORLAMA — bunun yerine:")
madde([
    "<b>Düşük işletme maliyeti:</b> hafif/açıklanabilir modeller (lojistik regresyon, "
    "SGD) — büyük dil modelleri kadar pahalı değil, sadece rapor üretiminde LLM kullanılıyor",
    "<b>Anonim/toplu veri ortaklığı:</b> \"dijital refah eğilimleri\" verisiyle üniversite/"
    "TÜBİTAK/ruh sağlığı STK ortaklığı (kişisel veri paylaşılmadan, toplu istatistik olarak)",
    "<b>Marka değeri üzerinden kurumsal sponsorluk:</b> \"dijital-refah-öncelikli platform\" "
    "konumlandırması",
    "<b>Opsiyonel gönüllü destek/bağış mekanizması:</b> mevcut roket sistemine benzer, "
    "gönüllülük esaslı",
])

cizgi()
kucuk("Bu belge, NSosyal_Teknik_Ozet.pdf ile birlikte kullanılmak üzere hazırlandı. Rapor "
      "yazarken §4'teki gelecek-vizyon fikirlerinin prototipte ÇALIŞMADIĞINI, §3'teki "
      "gazetecilik kaynaklarının akademik atıf OLMADIĞINI, ve §1'deki literatür bulgularının "
      "TÜMÜNÜN gerçek/doğrulanmış kaynaklara dayandığını raporun kendi metninde de tutarlı "
      "biçimde yansıtmaya dikkat et.")

doc = SimpleDocTemplate(
    DOSYA, pagesize=A4,
    leftMargin=KENAR_BOSLUGU, rightMargin=KENAR_BOSLUGU, topMargin=2*cm, bottomMargin=2*cm,
    title="NSosyal — Rapor Icerigi Kaynagi",
)
doc.build(story)
print(f"Olusturuldu: {DOSYA}")
