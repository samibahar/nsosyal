# -*- coding: utf-8 -*-
"""Prototip teknik özeti PDF'i üretir (arkadaşa gönderilecek).

19.08.2026 gece güncellemesi: Gemini API entegrasyonu, "korku"->"sinirli"
kategori değişikliği + StandardScaler düzeltmesi, doygunluk azaltma formül
güçlendirmesi, ve terapiste götürülebilir rapor varyantı eklendi -- bu script
CLAUDE.md'deki güncel duruma göre yeniden yazıldı."""
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
def sayfa(): story.append(PageBreak())

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
    "Teknik özet (güncellenmiş sürüm) — TEKNOFEST NSosyal İnovasyon Yarışması "
    "(Sosyal Yapay Zekâ teması) · 19 Ağustos 2026", stil_alt))
cizgi()

# ============================================================ 1. NEDEN
h1("1. Ne yapıyoruz ve neden")
p("NSosyal (T3 Vakfı + Baykar yapımı, ~700 bin+ kullanıcılı, reklamsız mikroblog platformu) "
  "için duygu-duyarlı, açıklanabilir ve koruyucu bir sıralama/şeffaflık katmanı geliştiriyoruz. "
  "Sorun: sosyal medya akışları genelde \"en yüksek etkileşim\" için optimize edilir ve bu, "
  "duygusal olarak yoğun/olumsuz içeriği ödüllendirme eğilimindedir (Facebook'un kendi iç "
  "araştırmasında \"öfke = en yüksek etkileşim\" bulgusu gibi). Biz bunun yerine: kullanıcının "
  "ilgi alanından HİÇ SAPMADAN, sadece o an olumsuz bir davranışsal örüntüye (\"spiral\") girip "
  "girmediğini fark eden ve buna göre içeriğin dozunu nazikçe ayarlayan bir sistem kurduk. "
  "İçerik elenmiyor, sadece yumuşatılıyor -- ve her karar açıklanabilir olmak zorunda (kara "
  "kutu bir sinir ağı değil, denetlenebilir modeller). Bu, projenin şeffaflık tezinin temeli.")
h2("Neden bu kadar 'dürüstlük' vurgusu var?")
p("Çünkü bu bir ruh sağlığı bağlamına yakın bir araç ve yanlış/abartılı bir iddia hem etik hem "
  "de itibar açısından riskli. Bu yüzden proje boyunca tekrarlanan bir disiplin var: vendor "
  "iddialarını sorgulamadan kabul etmemek, kendi ölçtüğümüz her sayıyı (iyi ya da kötü) olduğu "
  "gibi raporlamak, ve bir şey bozulduğunda/beklenenden kötü çıktığında saklamak yerine kök "
  "nedenini bulup düzeltmek. Bu belgede birkaç yerde \"beklenenden kötü çıktı, sebebi X, düzeltme Y\" "
  "şeklinde bölümler göreceksin -- bunlar kusur değil, metodolojik dürüstlüğün kanıtı olarak bilinçli "
  "şekilde saklandı.")

h2("Mimari — verinin izlediği yol (uçtan uca)")
madde([
    "<b>1. Gönderi metni</b> → BERT modeli duygu skoru üretir (-1 ile +1 arası)",
    "<b>2. Kullanıcı etkileşimi</b> → tarayıcıda Intersection Observer dwell-time'ı ölçer, "
    "tıklama/roket/yorum backend'e bildirilir",
    "<b>3. İKİ AYRI, birbirinden habersiz model</b> bu sinyalleri yorumlar: "
    "(a) <b>spiral tespiti</b> (ikili, sıralamayı etkiler) ve (b) <b>psikolojik durum tahmini</b> "
    "(5 kategori, SADECE görüntüleme amaçlı — bkz. §6, bu ayrım kritik)",
    "<b>4. İki katmanlı sıralama motoru</b> (motor.py) → ilgi skoru + refah katmanı "
    "(spiral seviyesine göre negatif içerik elenmez, sadece yumuşatılır)",
    "<b>5. Şeffaflık paneli</b> → her karar (\"neden bunu görüyorsun\") kullanıcıya açık "
    "biçimde gösterilir",
    "<b>6. Haftalık/isteğe bağlı rapor</b> → oturum verisi bir LLM'e (Gemini) özetletilip "
    "okunabilir bir metne çevrilir (bkz. §7)",
])

# ============================================================ 2. PARAMETRELER TABLOSU
h1("2. Parametreler — Neden Bu Değerler, Neye Etki Ediyorlar")
p("Sistemde ayarlanabilir her sabit rastgele seçilmedi; hepsinin somut bir gerekçesi var. "
  "Aşağıdaki tablo hepsini tek yerde topluyor (her biri kendi bölümünde de tekrar geçiyor):")
tablo(
    ["Parametre", "Değer", "Neden", "Neye etki eder"],
    [
        ["TAM_GUVEN_ESIGI", "8", "Az örneklemli oran istatistiksel güvenilmez (kolayca %0/%100'e savrulur)",
         "\"Tespit edilen durum\" göstergesinin ilk birkaç etkileşimde ne kadar bastırılacağı"],
        ["DOGRULAMA_ARALIGI", "8", "Çok sık sorulursa rahatsız eder, çok seyrek sorulursa veri birikmez (EMA literatürüyle uyumlu)",
         "Kaç etkileşimde bir onay kartı çıkacağı"],
        ["KISISEL_ETA0", "0.12", "Gerçekte çok daha küçük olurdu (~0.0005); demo'da TEK oturumda görünür olsun diye büyütüldü",
         "Kişiselleştirilmiş modelin her onaydan sonra ne kadar kayacağı"],
        ["saturate() tavanı", "%75 (eskiden %45)", "%45, seviye=1'de bile gözle zor fark ediliyordu — canlı testte yakalandı",
         "Doygunluk azaltmanın maksimum görsel gücü"],
        ["saturate() eğrisi", "seviye^0.7", "Doğrusal eğri orta seviyelerde neredeyse görünmezdi",
         "Efekt ne kadar erken/belirgin fark edilir"],
        ["refah_cezasi çarpanı", "0.8", "Tam çarpan (1.0) içeriği aşırı bastırabilirdi; 0.8 belirgin ama tam eleme değil",
         "Sıralamada negatif içeriğin ne kadar aşağı düşeceği"],
        ["_katki_agirligi aralığı", "0.15 – 1.0", "Hızlı kaydırma barları tek başına domine etmesin (tavan), kısa bakış da sıfır sayılmasın (taban)",
         "Bir etkileşimin oturum ortalamasına katkı ağırlığı"],
        ["StandardScaler", "sabit/dondurulmuş", "dwell_saniye (0-15+) ile duygu (-1..1) ölçek farkı lineer modeli çarpıtıyordu",
         "Hangi sinyalin tahminde ne kadar ağırlık taşıyacağı (F1: 0.686→0.704)"],
        ["Gemini max_output_tokens", "2048 (eskiden 600)", "600'de model 'thinking' token'larını da aynı bütçeden harcayıp metni yarıda kesiyordu",
         "Rapor metninin tam üretilip üretilemeyeceği"],
    ],
    genislikler=[3.3*cm, 2.6*cm, 6.2*cm, 4.4*cm],
)

sayfa()

# ============================================================ 3. DUYGU MODELİ
h1("3. Duygu Analizi Modeli (BERT)")
p("Temel model: <b>savasy/bert-base-turkish-sentiment-cased</b> (hazır Türkçe BERT, ikili "
  "pozitif/negatif sınıflandırma, nötr sınıfı yok).")

h2("Bağımsız doğrulama — vendor iddiasına güvenmedik, kendimiz ölçtük")
p("winvoker/turkish-sentiment-analysis-dataset'ten rastgele 1000 örnek ile bağımsız test yapıldı "
  "(veri sızıntısı olmasın diye fine-tuning ve doğrulama TAMAMEN ayrık split'lerden geldi):")
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
  "bölümünden (doğrulama setinden tamamen ayrık) dengeli ~15.000 örnekle 2 epoch devam eğitimi. "
  "CPU'da (GPU yok) 2 saat 6 dakika sürdü.")
kucuk("Ek bulgu: modelin NSosyal-tarzı kısa/resmi haber-bülteni cümlelerinde (20 örnek elle test) "
      "orijinal ve ince-ayarlı model EŞİT çıktı (%65=%65) — fine-tuning bu alt-türde ne kazandırdı "
      "ne kaybettirdi, genel Türkçe metinde büyük kazanç sağladı. İnce ayarlı model üretimde kullanılıyor.")

# ============================================================ 4. SPIRAL MODEL
h1("4. Spiral Tespiti (Lojistik Regresyon) — SIRALAMAYI ETKİLEYEN model")
p("Kullanıcının son 20 farklı gönderiyle etkileşiminden 6 özellik çıkarılıp (motor.py), "
  "senaryo-bazlı sentetik veriyle eğitilmiş bir lojistik regresyon modeline verilir "
  "(spiral_model.py). <b>Doğruluk: 0.714, F1: 0.748.</b> Bu modelin çıktısı (spiral_seviyesi) "
  "hem sıralamayı hem renk doygunluğunu etkileyen TEK sinyal (bkz. §6).")

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

h2("Küçük örneklem güven düzeltmesi (TAM_GUVEN_ESIGI)")
p("Az sayıda farklı gönderiyle (2-3 gibi) hesaplanan bir ORAN istatistiksel olarak güvenilmez — "
  "kolayca %0 ya da %100'e savrulur. Yeterli veri (8 farklı gönderi) birikene kadar gösterilen "
  "değer kademeli olarak yumuşatılıyor (guven_carpani = min(1, gonderi_sayisi/8)).")
p("<b>Sıralamaya etkisi (motor.py, sirala()):</b> <font face='Arial'>refah_cezasi = "
  "spiral_seviyesi × max(0, -duygu) × 0.8 ; final_skor = ilgi_skoru − refah_cezasi</font>. "
  "Yani spiral seviyesi yükseldikçe, negatif duygulu gönderiler puan kaybedip sıradaki sayfada "
  "aşağı düşüyor (elenmiyor, \"yumuşatıldı\" rozetiyle işaretleniyor).")

sayfa()

# ============================================================ 5. PSİKOLOJİK MODEL
h1("5. Psikolojik Durum Sınıflandırıcısı (5 Kategori)")
p("Tek bir \"spiral var/yok\" yerine, her etkileşim için 5 sinyalden (duygu, dwell-time, "
  "tıklama, roket, yorum) 5 kategoriden birine olasılık dağılımı üretiliyor: "
  "<b>sakin, mutluluk, umut, sinirli, anksiyete.</b> Model: SGDClassifier (log_loss), "
  "StandardScaler ile — F1 makro ≈ 0.70.")

h2("'Korku' neden 'sinirli' oldu (19.08.2026)")
p("Orijinal tasarımda kategori \"korku\"ydu: negatif duygu + uzun donup-izleme + hiç etkileşim "
  "yok. Ama modülün kendi dosya-başı dürüstlük notu zaten şunu itiraf ediyordu: \"korku ile "
  "anksiyete'yi ayırt etmenin bilimsel bir üst sınırı var\" — çünkü ikisi de davranışsal olarak "
  "neredeyse AYNI imzayı taşıyordu (\"negatif + pasif\"). \"Sinirli\" (negatif duygu + roket/yorum "
  "VAR, aktif tepkisel katılım) davranışsal olarak GERÇEKTEN ayırt edilebilir bir örüntü — "
  "\"korku\"nun donup-pasif-izlemesinin tam tersi.")

h2("Sentetik senaryo tasarımı (güncel)")
tablo(
    ["Kategori", "Tasarım mantığı"],
    [
        ["sakin", "Nötre yakın duygu, kısa dwell, neredeyse hiç etkileşim yok"],
        ["mutluluk", "Pozitif duygu + aktif katılım (roket/yorum sık)"],
        ["umut", "Pozitif duygu + uzun sessiz takip, roket/yorum nadir"],
        ["sinirli", "Negatif duygu + roket/yorum VAR (aktif, tepkisel katılım), kısa-orta dwell"],
        ["anksiyete", "Negatif duygu + kısa-tekrarlı dwell, huzursuz düşük etkileşim"],
    ],
    genislikler=[2.8*cm, 13.7*cm],
)

h2("Yan bulgu: kategori değişince F1 düştü, kök nedeni bulup düzelttik")
p("Kategori değişip model yeniden eğitilince F1 makro 0.78'den <b>0.686</b>'ya düştü. Kök neden "
  "araştırıldı: <font face='Arial'>dwell_saniye</font> (0-15+ saniye) ile <font face='Arial'>duygu</font> "
  "(-1..1) ve roket/yorum/tıklama (0/1) arasında BÜYÜK ölçek farkı var; lineer modelde "
  "ölçeklenmemiş büyük-skala özellik küçük olanları gölgeliyor. Eskiden bu gizliydi çünkü "
  "\"korku\"nun ayrımı neredeyse tamamen dev dwell büyüklüğüyle yapılıyordu; \"sinirli\" küçük "
  "skala olan duygu işaretine dayandığı için sorun görünür oldu. <b>StandardScaler</b> eklendi "
  "(eğitim + tahmin + kişiselleştirme güncellemesi — üçü de aynı dondurulmuş ölçekleyiciyi "
  "kullanıyor). Sonuç: F1 makro <b>0.704</b>'e çıktı, kategoriler arası denge de düzeldi "
  "(\"umut\" precision 0.55→0.72).")
tablo(
    ["Kategori", "Precision", "Recall", "F1"],
    [
        ["anksiyete", "0.57", "0.73", "0.64"],
        ["mutluluk", "0.81", "0.70", "0.75"],
        ["sakin", "0.68", "0.79", "0.73"],
        ["sinirli", "0.84", "0.55", "0.67"],
        ["umut", "0.72", "0.76", "0.74"],
    ],
    genislikler=[KULLANILABILIR_GENISLIK/4]*4,
)
kucuk("0.70, eski 0.78'in altında ama bu dürüst, gerçek bir sayı — daha zor (ve daha savunulabilir) "
      "bir ayrım görevinin sonucu, uydurulmadı.")

h2("Neden hazır bir 'duygu kategorisi' modeli kullanılmadı")
p("Araştırılan alternatifler (örn. maymuni/bert-base-turkish-cased-emotion-analysis) belgesiz "
  "eğitim verisi ve doğrulanmamış \"%99.5 doğruluk\" gibi şüpheli iddialar taşıyordu. Kendi "
  "açıklanabilir modelimiz tercih edildi.")

h2("Arayüz düzeltmeleri (kullanıcı testi sırasında bulunan hatalar)")
madde([
    "<b>Sinyal birleştirme:</b> aynı gönderiye roket atıp sonra kaydırıp uzaklaşmak, önceden "
    "roket sinyalini sessizce eziyordu. Artık en uzun süre + tüm eylemlerin OR'u birleştiriliyor.",
    "<b>Ağırlıklı ortalama:</b> kısa/edilgen bir görünme (0.4sn) artık tam bir gözlem gibi "
    "sayılmıyor (ağırlık = dwell/4, roket/yorum/tıklama varsa = 1.0).",
    "<b>Oturum boyunca kademeli birikme:</b> tek bir olay artık barları %90+'a savurmuyor, "
    "tüm oturumun ağırlıklı ortalaması alınıyor.",
])

sayfa()

# ============================================================ 6. BARLAR NEYİ ETKİLİYOR
h1("6. Duygu/Spiral Barları — Hangisi Neyi Etkiliyor?")
p("Bu ayrım kritik ve kolayca karıştırılabiliyor, o yüzden ayrı bir bölüm hak ediyor: sayfada "
  "İKİ AYRI gösterge var, ve sadece BİRİ sıradaki gönderileri etkiliyor.")

h2("A) 'Tespit edilen durum' göstergesi (üstteki tekil bar) → SIRALAMAYI ETKİLER")
p("Bu, spiral_model.py'nin ikili çıktısı (spiral_seviyesi). motor.py'deki sirala() fonksiyonuna "
  "doğrudan parametre olarak giriyor ve refah_cezasi'nı belirliyor (bkz. §4) — yani bu seviye "
  "yükseldikçe negatif gönderiler sıradaki sayfada gerçekten aşağı düşüyor. Aynı zamanda renk "
  "doygunluğu azaltmayı da bu değer tetikliyor (bkz. §7) — tek bir sinyal, iki görsel etki, "
  "tutarlılık için.")

h2("B) 5 kategorili 'olası izlenim' barları (mutluluk/umut/sakin/sinirli/anksiyete) → SADECE GÖRÜNTÜLEME")
p("Bu tamamen AYRI bir model (psikolojik_durum.py), ayrı bir günlük (PSIKOLOJIK_GUNLUK) "
  "kullanıyor ve çıktısı sadece arayüzde gösteriliyor — motor.py'deki sirala() fonksiyonuna HİÇ "
  "geçmiyor. \"%40 anksiyete\" görsen bile bu, sıradaki gönderileri değiştirmiyor; sadece "
  "kullanıcıya kendi örüntüsünü gösteren bir ayna.")
p("<b>Bu bilinçli bir tasarım kararı:</b> sıralamaya giren TEK sinyal spiral seviyesi olsun ki "
  "sistem açıklanabilir kalsın (\"refah_cezası X çünkü spiral seviyesi Y\" — tek, izlenebilir "
  "neden). 5 kategorili katman saf öz-farkındalık amaçlı; sıralamaya karışırsa hem açıklanabilirlik "
  "karmaşıklaşır hem de \"duygu kategorimize göre içerik seçiyoruz\" gibi bilinçli olarak "
  "reddettiğimiz bir yaklaşıma kayma riski doğar (bkz. §9).")

h2("Ekranda kalma süresi (dwell) barları nasıl etkiliyor?")
p("İki farklı şekilde: (1) <b>Doğrudan özellik olarak</b> — dwell_saniye, sınıflandırıcının "
  "kullandığı 5 sinyalden biri, hangi kategorinin tahmin edileceğini belirliyor. "
  "(2) <b>Ağırlık olarak</b> — eğer o gönderide açık bir eylem (roket/yorum/tıklama) varsa süre "
  "ne olursa olsun tam ağırlık (1.0); sadece pasif dwell varsa ağırlık dwell_saniye/4'e "
  "endekslenip 0.15-1.0 arasına sıkıştırılıyor. Bu, sırf hızlı kaydırmanın barları tek başına "
  "domine etmesini önlemek için eklendi.")

# ============================================================ 7. DOYGUNLUK
h1("7. Renk Doygunluğu Azaltma")
p("Spiral seviyesi yükseldikçe akışın CSS <font face='Arial'>saturate()</font> filtresi kademeli "
  "azalıyor — kesin bir engel değil, fark ettirmeye yönelik nazik bir görsel sinyal. Kullanıcı "
  "isteğiyle bir açma/kapama tuşu da eklendi. Ayrı bir ağırlıklı formül icat etmek yerine zaten "
  "eğitilmiş tek bileşik sinyal (spiral_seviyesi) tekrar kullanıldı — tutarlılık için.")

h2("Bulunan hata: teknik olarak çalışıyordu ama gözle görülmüyordu")
p("Kullanıcı canlı testte fark etmediğini bildirdi. Tarayıcıda doğrulandı: mekanizma TEKNİK "
  "olarak doğru çalışıyordu (filter doğru uygulanıyordu), ama etki gözle görülemeyecek kadar "
  "küçüktü — iki sebep: (1) güven-çarpanı ilk birkaç etkileşimde spiral seviyesini kasıtlı "
  "bastırıyor (örn. %9'da doygunluk sadece %96 — fark edilmez), (2) eski formülün tavanı "
  "seviye=1'de bile sadece %45 azalmaydı. Güven bastırmasını korumayı seçtik (istatistiksel "
  "gerekçesi hâlâ geçerli), ama görünürlük eğrisini güçlendirdik:")
tablo(
    ["Spiral seviyesi", "Eski formül", "Yeni formül"],
    [
        ["0.09 (ilk birkaç etkileşim)", "saturate(~96%) — fark edilmez", "saturate(~89%) — hâlâ hafif ama daha belirgin"],
        ["0.33 (orta)", "saturate(~85%)", "saturate(66%)"],
        ["1.00 (maksimum)", "saturate(55%)", "saturate(25%)"],
    ],
    genislikler=[KULLANILABILIR_GENISLIK/3]*3,
)
kucuk("Formül: doygunluk% = 100 − (seviye^0.7) × 75. Üstel<1 eğri orta seviyelerde de belirginlik "
      "sağlıyor, sadece seviye=1'e çok yaklaşınca değil.")

sayfa()

# ============================================================ 8. DOĞRULAMA
h1("8. Aktif Öğrenme / Kendi Kendini Doğrulama Döngüsü")
p("Davranış→psikoloji eşlemesi sentetik senaryolara dayanıyor, gerçek insan verisine değil. "
  "Bunu \"doğrulanmış\" gibi sunmak yerine, kullanıcıya her ~8 etkileşimde bir hafif bir onay "
  "sorusu soruyoruz (\"şu an gerçekte nasıl hissediyorsun?\") ve cevabı modelin O ANKİ "
  "tahminiyle karşılaştırıyoruz. Model tahmini, taraflılık olmasın diye kullanıcı cevap "
  "vermeden ÖNCE hiç gösterilmiyor. Eşleşme oranı şeffafça raporlanıyor.")
kucuk("Literatür notu: bu mekanizma, psikolojideki \"Ecological Momentary Assessment (EMA)\" / "
      "\"micro-EMA\" yönteminin bağımsız bir yeniden keşfi (JMIR 2024;26:e50275; PMC7991987). "
      "Az soru + sık sorma prensibi literatürle örtüşüyor.")

# ============================================================ 9. KİŞİSELLEŞTİRME
h1("9. Kişiselleştirme (Online Learning)")
p("Doğrulama cevapları modeli GERÇEKTEN güncelleyebilir mi? Evet — SGDClassifier'ın "
  "partial_fit özelliği kullanılarak, her doğrulama cevabından sonra modelde TEK küçük bir "
  "SGD adımı atılıyor. Varsayılan model (_VARSAYILAN_MODEL) hiç değişmiyor; ayrı bir kopya "
  "(_KISISEL) zamanla kayabiliyor.")
p("<b>Demo sorunu ve çözümü:</b> gerçek kişiselleştirmeyi (çok kullanıcı, uzun vade) tek bir "
  "oturumda gösteremeyiz. Arayüze bir anahtar eklendi: \"Varsayılan / Kişiselleştirilmiş\" — "
  "aynı oturumun geçmişini seçilen modelle anında yeniden skorlayıp iki hâli karşılaştırıyor.")
madde([
    "Test sonucu: tek bir onay neredeyse etkisiz kalıyor (~3 puanlık kayma)",
    "Birkaç tutarlı onaydan sonra model gerçekten yön değiştiriyor (kişiselleştirilmiş kopyada "
    "gözlemlenebilir bir kayma)",
    "<b>Dürüstlük notu:</b> adım büyüklüğü (KISISEL_ETA0=0.12) demo'da görünür olması için "
    "kasıtlı büyütüldü — gerçek üretimde (binlerce kullanıcı, aylarca veri) çok daha küçük "
    "olurdu (~0.0005). Bu bir \"gerçek kişiselleştirme kalibrasyonu\" iddiası değil, "
    "mekanizmanın kanıt-of-konseptidir.",
    "İstikrar riski: az veriyle düzenlileştirme olmadan online güncelleme modeli yanlış yöne "
    "kaydırabilir. Şu anki koruma: küçük adım + değişmeyen varsayılan model referans olarak "
    "kalıyor. Gerçek üründe düzenlileştirme/sınır (clipping) eklenmeli.",
])

sayfa()

# ============================================================ 10. RAPOR
h1("10. Haftalık Rapor: Statik Örnekten Gerçek Zamanlı LLM'e")
p("Rapor önce statik/sabit metinli bir örnek olarak gösterildi (formatı kanıtlamak için). "
  "19.08.2026 gecesi gerçek LLM üretimine geçirildi: oturumda kaydedilen gerçek veri (kategori "
  "dağılımı, konu/saat örüntüleri, doğrulama eşleşme oranı) bir dil modeline özetletilip "
  "okunabilir bir rapor metnine çevriliyor.")

h2("Sağlayıcı seçimi: Claude değil, Gemini")
p("İlk tasarım Anthropic/Claude API'siydi. Kullanıcının bütçe kısıtı sorması üzerine "
  "<b>Google Gemini</b>'ye geçildi (gemini-3.6-flash, google-genai kütüphanesi) — Gemini'nin "
  "kart istemeyen gerçek bir ücretsiz katmanı var, Claude API tamamen kullanım-bazlı ücretli. "
  "Mantık/prompt/sistem talimatı sağlayıcıdan bağımsız tasarlandı — tek bir fonksiyonu "
  "(uret()) değiştirmek başka bir sağlayıcıya geçmek için yeterli.")

h2("Canlı entegrasyonda çıkan iki gerçek sorun (saklanmadı, çözüldü)")
madde([
    "<b>Model emekliye ayrılmış:</b> gemini-2.5-flash artık yeni kullanıcılara kapalı; API'nin "
    "kendi hata mesajının önerdiği gemini-3.6-flash'a geçildi.",
    "<b>Çıktı yarıda kesiliyordu:</b> modelin \"thinking\" (iç muhakeme) token'ları da aynı "
    "max_output_tokens bütçesinden düşüyor. thinking_budget=0 ile tamamen kapatmak bu modelde "
    "reddedildi (400 hata) — çözüm thinking_level=\"low\" + bütçeyi 2048'e çıkarmak oldu.",
])
p("Gerçek üretimle doğrulanan örnek çıktı üç doğru bölümde geldi (\"Gözlemlenen olası örüntü / "
  "İyi gidenler / Nazik bir not\"), teşhis dili yok, temkinli ton korunuyor. API anahtarı yoksa "
  "(GEMINI_API_KEY tanımlı değilse) arayüz zaten var olan statik örneğe düşüyor — sahte bir LLM "
  "çıktısı asla uydurulmuyor.")

h2("Yeni: bir uzmana götürülebilecek veri özeti")
p("Aynı LLM, kullanıcının isteğiyle, bir ruh sağlığı uzmanına götürebileceği YORUMSUZ bir ham "
  "veri özeti de hazırlayabiliyor. Kişisel rapordan (sıcak, \"Nazik bir not\" içeren) kasıtlı "
  "olarak FARKLI bir sistem talimatıyla çalışıyor: tavsiye/yorum/sonuç çıkarma YASAK, üçüncü "
  "şahıs+nötr dil, sadece \"Veri Özeti / Gözlemlenen Davranışsal Örüntüler / Sınırlılıklar\" "
  "başlıklarıyla ham sayıları sunuyor. \"Sınırlılıklar\" bölümünde modelin sentetik veriyle "
  "eğitildiğini, klinik doğrulaması olmadığını ve TEK BAŞINA hiçbir karar için yeterli "
  "olmadığını tekrar etmesi ZORUNLU kılındı. Otomatik yüklenmiyor — talep üzerine (bir buton "
  "ile) üretiliyor. Canlı test edildi; çıktı açılış cümlesinde \"klinik bir belge değildir, "
  "nihai değerlendirme uzmana aittir\" diyor ve hiç yorum/tavsiye içermiyor.")

# ============================================================ 11. DİĞER
h1("11. Diğer Teknik Düzeltmeler ve Araçlar")
madde([
    "<b>Sayfalama (infinite scroll):</b> 150 örnek gönderi (10 kategori × 15), gerçek sayfa "
    "sayfa (12'şer) yükleme, skor motoruna göre sıralı, tekrarsız",
    "<b>Doğal çeşitlilik:</b> final_skor'a küçük rastgele gürültü — her oturum sıfırlamasında "
    "birebir aynı sıra gelmiyor",
    "<b>Roket/yorum spam koruması:</b> aynı gönderiye art arda etkileşim artık günlüğü domine "
    "etmiyor, tek kayıtta birleştiriliyor",
    "<b>Tarayıcı önbellek yönetimi:</b> statik dosyalar (?v=N) sürüm numarasıyla işaretleniyor, "
    "değişiklik yapıldığında bilinen bir tarayıcı önbellek hatasını önlemek için artırılıyor",
])

# ============================================================ 12. LİTERATÜR
h1("12. Literatür Desteği (Gerçek Kaynaklarla)")
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

sayfa()

# ============================================================ 13. KORKULARIMIZ
h1("13. Önlemeye Çalıştığımız Şeyler / Olası Korkularımız")
p("Bu projede teknik hatalardan çok, ETİK/İTİBAR riskleri konusunda temkinli davrandık. "
  "Bilinçli olarak reddedilen yaklaşımlar:")
madde([
    "<b>Cohort-bazlı öneri</b> (\"kaygılı hissedenlerin izlediğini göster\") — Facebook'un "
    "\"öfke=en yüksek etkileşim\" tuzağına düşürme riski; anksiyeteli kullanıcılara \"diğer "
    "anksiyeteli kullanıcıların izlediğini\" göstermek doomscroll döngüsünü pekiştirebilir.",
    "<b>Reklamı duygu durumuna göre hedeflemek</b> — 2017'de sızan bir Facebook belgesi "
    "\"worthless/insecure\" hisseden gençleri reklam hedeflemesi için kullanmayı önermişti. "
    "Biz TAM TERSİNİ yapıyoruz: kırılgan durumda reklamı bastırıyoruz, hedeflemiyoruz.",
    "<b>İçerik kategorisine (siyasi/dini vb.) göre filtreleme</b> — sistem KONU-NÖTR, sadece "
    "duygusal yoğunluğa bakıyor. Bu hem etik açıdan hem de bu platform (yerli/milli "
    "konumlandırılmış) için stratejik olarak riskli olurdu.",
    "<b>Teşhis aracı gibi konuşmak</b> — her metinde (kişisel rapor, terapist özeti, arayüz "
    "metinleri) \"tespit ettik\" değil \"gözlemledik\", \"kesin\" değil \"olası\" dili zorunlu "
    "kılındı; \"tanı/hasta/bozukluk\" kelimeleri hiçbir LLM promptunda kullanılmıyor.",
    "<b>Sahte/abartılı teknik iddia</b> — vendor'ın %95.4 doğruluk iddiasını sorgulamadan kabul "
    "etmek yerine bağımsız ölçtük (%69.8 çıktı), F1 düşüşünü (0.78→0.686) gizlemek yerine kök "
    "nedenini bulup düzelttik ve dürüstçe raporladık. Bu belgenin kendisi de bu disiplinin bir "
    "ürünü.",
    "<b>Gerçek olmayan entegrasyon iddiası</b> — NSosyal veya T3 AI'a gerçek bir API erişimimiz "
    "YOK. Bunu raporda \"önerilen entegrasyon konsepti\" olarak açıkça belirtiyoruz, gerçek bir "
    "entegrasyon varmış gibi sunmuyoruz.",
])

# ============================================================ 14. SINIRLILIKLAR
h1("14. Dürüstçe Belirtilmesi Gereken Sınırlılıklar")
madde([
    "BERT modeli hâlâ ikili (nötr sınıfı yok) — nötr metin zorla bir tarafa yuvarlanıyor",
    "Davranış→psikoloji eşlemesi sentetik senaryolara dayanıyor, klinik bir ölçüm değil",
    "\"Sinirli\" ile \"anksiyete\" ikisi de negatif duygu içerir ve gerçek dünyada iç içe "
    "geçebilir; F1≈0.70 bunun dürüst bir yansıması",
    "Kişiselleştirme mekanizması bir kanıt-of-konsept; gerçek üretimde düzenlileştirme/sınır "
    "eklenmeli",
    "Terapiste götürülebilir özet de dahil, hiçbir çıktı bir teşhis veya klinik değerlendirme "
    "aracı DEĞİL — yalnızca olası davranışsal örüntüleri gösterir, nihai değerlendirme her "
    "zaman uzmana aittir",
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
print(f"Olusturuldu: {DOSYA}")
