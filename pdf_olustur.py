# -*- coding: utf-8 -*-
"""Prototip teknik özeti PDF'i üretir (arkadaşa gönderilecek)."""
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

# Varsayılan Helvetica, Türkçe'ye özgü ğ/ı/ş/İ karakterlerini render edemiyor
# (WinAnsiEncoding kapsamı dışında) -- Windows'taki Arial TTF'i Unicode olarak
# kaydediyoruz (şartnamenin de zaten Arial istemesiyle tutarlı).
_FONT_DIZIN = r"C:\Windows\Fonts"
pdfmetrics.registerFont(TTFont("Arial", f"{_FONT_DIZIN}\\arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", f"{_FONT_DIZIN}\\arialbd.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Italic", f"{_FONT_DIZIN}\\ariali.ttf"))

DOSYA = "NSosyal_Teknik_Ozet.pdf"
KENAR_BOSLUGU = 2.2 * cm
KULLANILABILIR_GENISLIK = A4[0] - 2 * KENAR_BOSLUGU  # tablo genişlikleri bunu aşmamalı

renk_ana = colors.HexColor("#10716b")
renk_metin = colors.HexColor("#16211f")
renk_muted = colors.HexColor("#55625e")
renk_cizgi = colors.HexColor("#d8ddda")
renk_kutu = colors.HexColor("#eef1f0")

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
stil_kod = ParagraphStyle("Kod", parent=styles["Normal"], fontName="Arial",
                           fontSize=9, leading=13, textColor=renk_metin,
                           backColor=renk_kutu, borderPadding=6, spaceAfter=8)
stil_liste = ParagraphStyle("Liste", parent=stil_govde, leftIndent=12, spaceAfter=4)
stil_hucre = ParagraphStyle("Hucre", parent=stil_govde, fontSize=8.7, leading=11.5, spaceAfter=0)
stil_hucre_baslik = ParagraphStyle("HucreBaslik", parent=stil_hucre, fontName="Arial-Bold",
                                     textColor=colors.white)

story = []

def h1(t): story.append(Paragraph(t, stil_h1))
def h2(t): story.append(Paragraph(t, stil_h2))
def p(t): story.append(Paragraph(t, stil_govde))
def kucuk(t): story.append(Paragraph(t, stil_kucuk))
def cizgi(): story.append(HRFlowable(width="100%", thickness=0.75, color=renk_cizgi, spaceBefore=6, spaceAfter=10))
def bosluk(h=6): story.append(Spacer(1, h))

def madde(satirlar):
    items = [ListItem(Paragraph(s, stil_liste), leftIndent=14) for s in satirlar]
    story.append(ListFlowable(items, bulletType="bullet", start="•", bulletColor=renk_ana, bulletFontSize=8))
    bosluk(4)

def tablo(basliklar, satirlar, genislikler):
    """Her hücreyi Paragraph'a sarar (otomatik satır kaydırma) -- sütun
    genişlikleri toplamı KULLANILABILIR_GENISLIK'i aşmamalı, yoksa hücreler
    üst üste biner/taşar."""
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
story.append(Paragraph("NSosyal Duygu Katmanı", stil_baslik))
story.append(Paragraph(
    "Teknik özet — TEKNOFEST NSosyal İnovasyon Yarışması (Sosyal Yapay Zekâ teması) · "
    "19 Ağustos 2026", stil_alt))
cizgi()

# ============================================================ 1. GENEL BAKIŞ
h1("1. Ne yapıyoruz")
p("NSosyal (T3 Vakfı + Baykar yapımı mikroblog platformu) için duygu-duyarlı, "
  "açıklanabilir ve koruyucu bir sıralama katmanı geliştiriyoruz. Fikir: kullanıcının "
  "ilgi alanından hiç sapmadan, sadece o an olumsuz bir davranışsal örüntüye (\"spiral\") "
  "girip girmediğini fark eden ve buna göre içeriğin dozunu ayarlayan bir sistem. "
  "Kara kutu değil — her karar açıklanabilir olmak zorunda; bu, projenin şeffaflık tezinin temeli.")

h2("Mimari — verinin izlediği yol")
madde([
    "<b>1. Gönderi metni</b> → BERT modeli duygu skoru üretir (-1 ile +1 arası)",
    "<b>2. Davranış günlüğü</b> → kullanıcının dwell-time, tıklama, roket, yorum sinyalleri",
    "<b>3. İki ayrı model</b> bu sinyalleri yorumlar: (a) spiral tespiti (ikili), "
    "(b) psikolojik durum tahmini (5 kategori)",
    "<b>4. İki katmanlı sıralama motoru</b> → ilgi skoru + refah katmanı (negatif içerik "
    "elenmez, sadece yumuşatılır)",
    "<b>5. Şeffaflık paneli</b> → her karar kullanıcıya açık biçimde gösterilir",
])

# ============================================================ 2. DUYGU MODELİ
h1("2. Duygu Analizi Modeli (BERT)")
p("Temel model: <b>savasy/bert-base-turkish-sentiment-cased</b> (hazır Türkçe BERT, ikili "
  "pozitif/negatif sınıflandırma, nötr sınıfı yok).")

h2("Bağımsız doğrulama — vendor iddiasına güvenmedik, kendimiz ölçtük")
p("winvoker/turkish-sentiment-analysis-dataset'ten rastgele 1000 örnek (split=\"train\") "
  "ile bağımsız test yapıldı:")
tablo(
    ["", "Doğruluk", "F1", "Negatif precision"],
    [
        ["Vendor iddiası", "%95.4", "—", "—"],
        ["Bağımsız ölçüm (fine-tuning ÖNCESİ)", "%69.8", "0.778", "0.372"],
        ["Bağımsız ölçüm (fine-tuning SONRASI)", "%94.3", "0.964", "0.803"],
    ],
    genislikler=[7*cm, 2.8*cm, 2.3*cm, 4.5*cm],
)
p("<b>Fine-tuning yöntemi (ince_ayar.py):</b> aynı modelin, winvoker'ın split=\"test\" "
  "bölümünden (doğrulama setinden tamamen ayrık — veri sızıntısı yok) dengeli ~15.000 "
  "örnekle 2 epoch devam eğitimi. CPU'da (GPU yok) 2 saat 6 dakika sürdü.")
kucuk("Ek bulgu: modelin NSosyal-tarzı kısa/resmi haber-bülteni cümlelerinde (20 örnek elle test) "
      "orijinal ve ince-ayarlı model EŞİT çıktı (%65=%65) — fine-tuning bu alt-türde ne kazandırdı "
      "ne kaybettirdi, genel Türkçe metinde büyük kazanç sağladı. İnce ayarlı model üretimde kullanılıyor.")

# ============================================================ 3. SPIRAL MODEL
h1("3. Spiral Tespiti (Lojistik Regresyon)")
p("Kullanıcının son 20 farklı gönderiyle etkileşiminden 6 özellik çıkarılıp (motor.py), "
  "senaryo-bazlı sentetik veriyle eğitilmiş bir lojistik regresyon modeline verilir "
  "(spiral_model.py). <b>Doğruluk: 0.714, F1: 0.748.</b>")

h2("Öğrenilen katsayılar (gerçek, açıklanabilir)")
tablo(
    ["Özellik", "Katsayı", "Yorum"],
    [
        ["negatif_dwell_orani", "+1.467", "En güçlü etki: negatif içerikte geçirilen sürenin oranı"],
        ["ortalama_duygu", "-1.355", "İçeriklerin genel tonu ne kadar negatifse durum o kadar artar"],
        ["negatif_tekrar_sayisi", "+0.421", "(*) bkz. not aşağıda"],
        ["tiklama_orani", "-0.479", "Tıklamadan sadece kaydırmak (pasif tüketim) durumu artırır"],
        ["negatif_dwell_toplam", "+0.061", "Zayıf etki: mutlak saniye"],
        ["kaydirma_hizi", "+0.033", "Çok zayıf etki: hızlı kaydırma (doomscroll göstergesi)"],
        ["sabit (intercept)", "-2.339", "—"],
    ],
    genislikler=[4.3*cm, 1.8*cm, 10.4*cm],
)
kucuk("(*) negatif_tekrar_sayisi: roket/yorum spam'ini önlemek için backend artık gönderi başına "
      "tek kayıt tuttuğundan bu özellik canlıda her zaman 0 dönüyor — bilinen bir sınırlılık, "
      "kodda yorum olarak belgelendi.")

h2("Küçük örneklem güven düzeltmesi")
p("Az sayıda farklı gönderiyle (2-3 gibi) hesaplanan bir ORAN istatistiksel olarak güvenilmez — "
  "kolayca %0 ya da %100'e savrulur. Yeterli veri (8 farklı gönderi) birikene kadar gösterilen "
  "değer kademeli olarak yumuşatılıyor (guven_carpani = min(1, gonderi_sayisi/8)).")

# ============================================================ 4. PSİKOLOJİK MODEL
h1("4. Psikolojik Durum Sınıflandırıcısı (5 Kategori)")
p("Tek bir \"spiral var/yok\" yerine, her etkileşim için 5 sinyalden (duygu, dwell-time, "
  "tıklama, roket, yorum) 5 kategoriden birine olasılık dağılımı üretiliyor: "
  "<b>sakin, mutluluk, umut, korku, anksiyete.</b> Model: SGDClassifier (log_loss) — F1≈0.78.")

h2("Sentetik senaryo tasarımı")
tablo(
    ["Kategori", "Tasarım mantığı"],
    [
        ["sakin", "Nötre yakın duygu, kısa dwell, neredeyse hiç etkileşim yok"],
        ["mutluluk", "Pozitif duygu + aktif katılım (roket/yorum sık)"],
        ["umut", "Pozitif duygu + uzun sessiz takip, roket/yorum nadir"],
        ["korku", "Negatif duygu + uzun donup-izleme, hiç etkileşim yok"],
        ["anksiyete", "Negatif duygu + kısa-tekrarlı dwell, huzursuz düşük etkileşim"],
    ],
    genislikler=[2.8*cm, 13.7*cm],
)
p("<b>Neden hazır bir \"duygu kategorisi\" modeli kullanılmadı:</b> araştırılan alternatifler "
  "(örn. maymuni/bert-base-turkish-cased-emotion-analysis) belgesiz eğitim verisi ve doğrulanmamış "
  "\"%99.5 doğruluk\" gibi şüpheli iddialar taşıyordu. Kendi açıklanabilir modelimiz tercih edildi.")

h2("Arayüz düzeltmeleri (kullanıcı testi sırasında bulunan hatalar)")
madde([
    "<b>Sinyal birleştirme:</b> aynı gönderiye roket atıp sonra kaydırıp uzaklaşmak, önceden "
    "roket sinyalini sessizce eziyordu. Artık en uzun süre + tüm eylemlerin OR'u birleştiriliyor.",
    "<b>Ağırlıklı ortalama:</b> kısa/edilgen bir görünme (0.4sn) artık tam bir gözlem gibi "
    "sayılmıyor (ağırlık = dwell/4, roket/yorum/tıklama varsa = 1.0).",
    "<b>Oturum boyunca kademeli birikme:</b> tek bir olay artık barları %90+'a savurmuyor, "
    "tüm oturumun ağırlıklı ortalaması alınıyor.",
])

# ============================================================ 5. DOĞRULAMA
h1("5. Aktif Öğrenme / Kendi Kendini Doğrulama Döngüsü")
p("Davranış→psikoloji eşlemesi sentetik senaryolara dayanıyor, gerçek insan verisine değil. "
  "Bunu \"doğrulanmış\" gibi sunmak yerine, kullanıcıya her ~8 etkileşimde bir hafif bir onay "
  "sorusu soruyoruz (\"şu an gerçekte nasıl hissediyorsun?\") ve cevabı modelin O ANKİ "
  "tahminiyle karşılaştırıyoruz. Model tahmini, taraflılık olmasın diye kullanıcı cevap "
  "vermeden ÖNCE hiç gösterilmiyor. Eşleşme oranı şeffafça raporlanıyor.")
kucuk("Literatür notu: bu mekanizma, psikolojideki \"Ecological Momentary Assessment (EMA)\" / "
      "\"micro-EMA\" yönteminin bağımsız bir yeniden keşfi (JMIR 2024;26:e50275; PMC7991987). "
      "Az soru + sık sorma prensibi literatürle örtüşüyor.")

# ============================================================ 6. KİŞİSELLEŞTİRME
h1("6. Kişiselleştirme (Online Learning)")
p("Doğrulama cevapları modeli GERÇEKTEN güncelleyebilir mi? Evet — SGDClassifier'ın "
  "partial_fit özelliği kullanılarak, her doğrulama cevabından sonra modelde TEK küçük bir "
  "SGD adımı atılıyor. Varsayılan model (_VARSAYILAN_MODEL) hiç değişmiyor; ayrı bir kopya "
  "(_KISISEL) zamanla kayabiliyor.")
p("<b>Demo sorunu ve çözümü:</b> gerçek kişiselleştirmeyi (çok kullanıcı, uzun vade) tek bir "
  "oturumda gösteremeyiz. Arayüze bir anahtar eklendi: \"Varsayılan / Kişiselleştirilmiş\" — "
  "aynı oturumun geçmişini seçilen modelle anında yeniden skorlayıp iki hâli karşılaştırıyor.")
madde([
    "Test sonucu: tek bir onay neredeyse etkisiz kalıyor (%89.9→%87.4, ~3 puan)",
    "8 tutarlı \"korku\" onayından sonra model gerçekten yön değiştiriyor (%89.9→%91.3 korku)",
    "<b>Dürüstlük notu:</b> adım büyüklüğü demo'da görünür olması için kasıtlı büyütüldü — "
    "gerçek üretimde (binlerce kullanıcı, aylarca veri) çok daha küçük olurdu. Bu bir \"gerçek "
    "kişiselleştirme kalibrasyonu\" iddiası değil, mekanizmanın kanıt-of-konseptidir.",
    "İstikrar riski: az veriyle düzenlileştirme olmadan online güncelleme modeli yanlış yöne "
    "kaydırabilir. Şu anki koruma: küçük adım + değişmeyen varsayılan model referans olarak kalıyor.",
])

# ============================================================ 7. DİĞER
h1("7. Diğer Teknik Düzeltmeler")
madde([
    "<b>Sayfalama (infinite scroll):</b> 50→150 örnek gönderi (10 kategori × 15), gerçek "
    "sayfa sayfa (12'şer) yükleme, skor motoruna göre sıralı, tekrarsız",
    "<b>Doğal çeşitlilik:</b> final_skor'a küçük rastgele gürültü — her oturum sıfırlamasında "
    "birebir aynı sıra gelmiyor",
    "<b>Roket/yorum spam koruması:</b> aynı gönderiye art arda etkileşim artık günlüğü "
    "domine etmiyor, tek kayıtta birleştiriliyor",
])

# ============================================================ 8. LİTERATÜR
h1("8. Literatür Desteği (Gerçek Kaynaklarla)")
tablo(
    ["Konu", "Bulgu", "Kaynak"],
    [
        ["EMA / micro-EMA", "Doğrulama döngümüzün bağımsız bir uygulaması",
         "JMIR 2024;26:e50275"],
        ["Pasif kullanım / doomscrolling", "Kaygı ilişkisi literatürde ORTA güçte (abartılmamalı)",
         "JCMC 29(1), 2024 (141 çalışma meta-analizi)"],
        ["Digital phenotyping", "Davranıştan duygu çıkarımı meşru ama kişiye-özgü kalibrasyon gerekli",
         "JMIR 2025 scoping review"],
        ["Refah-farkında sıralama", "İki-katmanlı motorumuzun akademik emsali (CWB-RS)",
         "arXiv:2102.04211"],
        ["Açıklanabilirlik", "\"Az ama net\" ilkesi — aşırı detay güveni azaltabilir",
         "Springer World Wide Web journal"],
    ],
    genislikler=[3*cm, 8.8*cm, 4.8*cm],
)

# ============================================================ 9. REDDEDİLEN
h1("9. Bilinçli Olarak Reddedilen Yaklaşımlar")
madde([
    "<b>Cohort-bazlı öneri</b> (\"kaygılı hissedenlerin izlediğini göster\") — Facebook'un "
    "\"öfke=en yüksek etkileşim\" tuzağına düşürme riski",
    "<b>Reklamı duygu durumuna göre hedeflemek</b> — 2017 Facebook skandalının tam tersini "
    "yapıyoruz: bastırıyoruz, hedeflemiyoruz",
    "<b>İçerik kategorisine göre filtreleme</b> — sistem konu-nötr, sadece duygusal yoğunluğa bakıyor",
])

# ============================================================ 10. SINIRLILIKLAR
h1("10. Dürüstçe Belirtilmesi Gereken Sınırlılıklar")
madde([
    "BERT modeli hâlâ ikili (nötr sınıfı yok) — nötr metin zorla bir tarafa yuvarlanıyor",
    "Davranış→psikoloji eşlemesi sentetik senaryolara dayanıyor, klinik bir ölçüm değil",
    "\"Korku\" ile \"anksiyete\" gibi yakın durumları ayırt etmenin bilimsel bir üst sınırı var",
    "Kişiselleştirme mekanizması bir kanıt-of-konsept; gerçek üretimde düzenlileştirme/sınır "
    "eklenmeli",
    "Bu bir teşhis veya klinik değerlendirme aracı DEĞİL — yalnızca olası örüntüleri gösterir",
])

cizgi()
kucuk("Bu belge, TEKNOFEST NSosyal İnovasyon Yarışması (Sosyal Yapay Zekâ teması) için "
      "geliştirilen kanıt-of-konseptin teknik özetidir. NSosyal veya T3 AI'a gerçek bir API "
      "erişimi yoktur; tüm bileşenler bağımsız çalışır ve \"önerilen entegrasyon konsepti\" "
      "olarak sunulmaktadır.")

doc = SimpleDocTemplate(
    DOSYA, pagesize=A4,
    leftMargin=KENAR_BOSLUGU, rightMargin=KENAR_BOSLUGU, topMargin=2*cm, bottomMargin=2*cm,
    title="NSosyal Duygu Katmanı — Teknik Özet",
)
doc.build(story)
print(f"Oluşturuldu: {DOSYA}")
