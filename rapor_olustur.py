# -*- coding: utf-8 -*-
"""NSosyal Duygu Katmanı - TEKNOFEST Teknik Rapor üretici.
Resmi şablona (NSosyal_Inovasyon_2026_-_Proje_Teknik_Raporu_1_u6IVb) uyar:
Arial 12pt gövde, Arial Black 14pt başlık, 1.15 satır aralığı, iki yana yaslı,
2.5cm kenar boşluğu, kapak+içindekiler+kaynakça ayrı sayfa, <=30 sayfa."""
import docx
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

DOSYA = "NSosyal_Teknik_Rapor.docx"

doc = Document()

# ---------- Sayfa / stil kurulumu ----------
for section in doc.sections:
    section.left_margin = Cm(2.5)
    section.right_margin = Cm(2.5)
    section.top_margin = Cm(2.5)
    section.bottom_margin = Cm(2.5)


def _font_ayarla(style, ad, kalin=None):
    style.font.name = ad
    rpr = style.element.get_or_add_rPr()
    rFonts = rpr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rpr.append(rFonts)
    rFonts.set(qn('w:ascii'), ad)
    rFonts.set(qn('w:hAnsi'), ad)
    rFonts.set(qn('w:cs'), ad)
    if kalin is not None:
        style.font.bold = kalin


normal = doc.styles['Normal']
normal.font.size = Pt(12)
normal.paragraph_format.line_spacing = 1.15
normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
normal.paragraph_format.space_after = Pt(6)
_font_ayarla(normal, 'Arial')

h1 = doc.styles['Heading 1']
h1.font.size = Pt(14)
h1.font.color.rgb = RGBColor(0, 0, 0)
h1.paragraph_format.space_before = Pt(20)
h1.paragraph_format.space_after = Pt(10)
h1.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
h1.paragraph_format.line_spacing = 1.15
_font_ayarla(h1, 'Arial Black', kalin=True)

# ---------- Yardımcı fonksiyonlar ----------

def baslik(metin):
    doc.add_heading(metin, level=1)


def altbaslik(metin):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run(metin)
    r.bold = True
    r.font.name = 'Arial'
    r.font.size = Pt(12.5)
    rpr = r._element.get_or_add_rPr()
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:ascii'), 'Arial')
    rFonts.set(qn('w:hAnsi'), 'Arial')
    rpr.append(rFonts)


def govde(metin):
    doc.add_paragraph(metin)


def madde(satirlar):
    for s in satirlar:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(s)
        r.font.name = 'Arial'
        r.font.size = Pt(12)


def sayfa_sonu():
    doc.add_page_break()


def notv(metin):
    p = doc.add_paragraph()
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_after = Pt(8)
    r = p.add_run(metin)
    r.italic = True
    r.font.size = Pt(10.5)
    r.font.name = 'Arial'


def tablo(basliklar, satirlar):
    t = doc.add_table(rows=1, cols=len(basliklar))
    t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = t.rows[0].cells
    for i, h in enumerate(basliklar):
        hdr[i].text = ''
        p = hdr[i].paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.name = 'Arial'
        r.font.size = Pt(10.5)
    for satir in satirlar:
        cells = t.add_row().cells
        for i, deger in enumerate(satir):
            cells[i].text = ''
            p = cells[i].paragraphs[0]
            r = p.add_run(str(deger))
            r.font.name = 'Arial'
            r.font.size = Pt(10.5)
    doc.add_paragraph()
    return t


def toc_ekle():
    paragraph = doc.add_paragraph()
    run = paragraph.add_run()
    fld1 = OxmlElement('w:fldChar')
    fld1.set(qn('w:fldCharType'), 'begin')
    instr = OxmlElement('w:instrText')
    instr.set(qn('xml:space'), 'preserve')
    instr.text = 'TOC \\o "1-1" \\h \\z \\u'
    fld2 = OxmlElement('w:fldChar')
    fld2.set(qn('w:fldCharType'), 'separate')
    metin = OxmlElement('w:t')
    metin.text = "İçindekiler listesi görünmüyorsa: sağ tık > Alanı Güncelle (veya F9)."
    fld3 = OxmlElement('w:fldChar')
    fld3.set(qn('w:fldCharType'), 'end')
    r_el = run._r
    r_el.append(fld1)
    r_el.append(instr)
    r_el.append(fld2)
    r_el.append(metin)
    r_el.append(fld3)


# ============================================================ KAPAK
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(140)
r = p.add_run("NSosyal Duygu Katmanı")
r.bold = True
r.font.size = Pt(26)
r.font.name = 'Arial Black'

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(10)
r = p.add_run("Duygu-Duyarlı, Açıklanabilir ve Koruyucu Bir Sıralama Katmanı")
r.font.size = Pt(15)
r.italic = True

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(60)
r = p.add_run("TEKNOFEST NSosyal İnovasyon Yarışması 2026")
r.font.size = Pt(13)
p2 = doc.add_paragraph()
p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
r2 = p2.add_run("Tema: Sosyal Yapay Zekâ")
r2.font.size = Pt(13)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(150)
r = p.add_run("Teknik Rapor")
r.font.size = Pt(13)
r.bold = True
p2 = doc.add_paragraph()
p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
r2 = p2.add_run("24 Ağustos 2026")
r2.font.size = Pt(12)

sayfa_sonu()

# ============================================================ İÇİNDEKİLER
baslik("İÇİNDEKİLER")
toc_ekle()
sayfa_sonu()

# ============================================================ 1. PROJE ÖZETİ
baslik("PROJE ÖZETİ")

altbaslik("1.1. Proje Konusu ve Amacı")
govde(
    "Bu proje, NSosyal (T3 Vakfı ve Baykar Teknoloji iş birliğiyle geliştirilen, "
    "~700 bin'i aşkın aktif kullanıcısı bulunan, reklamsız bir yerli mikroblog platformu) "
    "için duygu-duyarlı, açıklanabilir ve koruyucu bir sıralama ve şeffaflık katmanı "
    "geliştirmeyi konu alır. Sosyal medya akışlarının çoğu \"en yüksek etkileşim\" hedefiyle "
    "optimize edilir; bu durum olumsuz ve kutuplaştırıcı içeriğin yapısal olarak "
    "ödüllendirilmesine yol açabilir. Bu soyut bir varsayım değildir: Facebook'un kendi iç "
    "araştırması, \"öfke\" tepkisi taşıyan gönderilerin çok daha fazla etkileşim aldığını "
    "ortaya koymuştur [13]; bağımsız, hakemli bir çalışma ise haber başlıklarındaki her ek "
    "negatif kelimenin tıklama oranını %2,3 artırdığını nedensel olarak göstermiştir [10]; "
    "kırılgan duygu durumlarının reklamcılık amacıyla hedeflenmesinin de belgelenmiş bir "
    "emsali bulunmaktadır [14] (ayrıntılar için bkz. Bölüm 2.1). Projenin amacı, kullanıcının ilgi "
    "alanından hiç sapmadan, yalnızca o an olumsuz bir davranışsal örüntüye (\"olası "
    "spiral\") girip girmediğini fark eden ve buna göre içerik dozunu nazikçe ayarlayan, "
    "kararlarının tamamı denetlenebilir/açıklanabilir bir sistem sunmaktır. Proje, birincil "
    "olarak Sosyal Yapay Zekâ temasına hitap eder; açıklanabilir sıralama motoru ve "
    "şeffaflık paneli üzerinden Kullanıcı Katılımı ve Arayüz/Kullanıcı Deneyimi (UI/UX) "
    "temasına, üretici paneli önerisiyle de İçerik Ekonomisi temasına organik olarak "
    "dokunur."
)

altbaslik("1.2. Proje Kapsamı ve Yöntemi")
govde(
    "Projenin kapsamı, NSosyal'in ana akışına eklenen üç bileşenden oluşur: (i) gönderi "
    "metninden gerçek zamanlı duygu skoru çıkaran, bağımsız olarak doğrulanmış ve "
    "ince ayarlı bir Türkçe BERT modeli; (ii) kullanıcının davranışsal sinyallerinden "
    "(durma süresi, tıklama, roket, yorum) olası bir \"spiral\" durumu ve olası bir "
    "psikolojik izlenim kategorisi tahmin eden, sentetik senaryo verisiyle eğitilmiş "
    "açıklanabilir sınıflandırıcılar; (iii) bu sinyalleri ilgi skoruyla birleştirip "
    "içeriği yeniden sıralayan iki katmanlı bir motor. Yöntem olarak; önce mimari "
    "sözlük-tabanlı basit bir ilk prototiple (spike) uçtan uca doğrulanmış, ardından "
    "her bileşen gerçek modellerle (BERT, lojistik regresyon/SGD) değiştirilip bağımsız "
    "olarak ölçülmüştür. Fikir yalnızca tasarım düzeyinde kalmamış; FastAPI tabanlı bir "
    "backend, gerçek zamanlı bir web arayüzü, ve isteğe bağlı bir LLM destekli haftalık "
    "öz-farkındalık raporu içeren, uçtan uca çalışan bir prototiple desteklenmiştir "
    "(bkz. Bölüm 3-4). NSosyal veya T3 AI'a gerçek bir API erişimi bulunmamaktadır; "
    "sistem bağımsız bir prototip olarak çalışır ve \"önerilen entegrasyon "
    "konsepti\" olarak sunulur; bu durum, projenin dürüstlük ilkesi gereği açıkça belirtilir."
)

sayfa_sonu()

# ============================================================ 2. KATMA DEĞER VE YENİLİKÇİLİK
baslik("KATMA DEĞER VE YENİLİKÇİLİK")

altbaslik("2.1. Problem Tanımı ve Mevcut Çözümler")
govde(
    "Bölüm 1.1'de değinilen örüntünün arkasında belgelenmiş, kamuya mal olmuş kanıtlar "
    "vardır. Wall Street Journal'ın 2021'de yayımladığı \"The Facebook Files\" dizisi, "
    "şirketin \"öfke\" tepkisini 2017-2018'de algoritmada beğeniden 5 kat ağırlıklandırdığını, "
    "iç araştırmacıların bunun kutuplaştırıcı/yanlış bilgi içeren içeriği ödüllendirdiğini "
    "fark edip bu ağırlığı sonradan düşürdüğünü ortaya koymuştur [13]. Akademik tarafta, "
    "yaklaşık 105.000 haber başlığı varyasyonunun ~5,7 milyon tıklama üzerinden analiz "
    "edildiği randomize kontrollü bir çalışma, bu etkinin (%2,3'lük tıklama artışı) "
    "yalnızca bir korelasyon değil, NEDENSEL bir ilişki olduğunu göstermiştir [10]; "
    "olumsuz haberlerin sosyal medyada daha fazla paylaşıldığı da "
    "ayrıca doğrulanmıştır [11][12]. Pasif/olumsuz içerik tüketiminin kaygı ve stresle "
    "ilişkisi de literatürde tutarlı biçimde destekleniyor: 141 çalışmayı kapsayan bir "
    "meta-analiz bu ilişkiyi orta güçte doğrularken [4], doomscrolling'e odaklanan bir "
    "başka çalışma bu davranışı kaygı, stres ve kontrol kaybı hissiyle "
    "ilişkilendirmektedir [5]. "
    "Kırılganlık durumunun ticari olarak istismar edilmesinin de gerçek bir emsali "
    "vardır: 2017'de The Australian gazetesi, Facebook'un iç bir belgesinin, gençlerin "
    "ne zaman \"değersiz\" veya \"güvensiz\" hissettiğini tespit edip bunu reklam "
    "hedeflemesi için bir fırsat olarak sunduğunu haberleştirmiştir [14]. Piyasadaki "
    "mevcut çözümler ise büyük ölçüde iki eksende yetersiz kalmaktadır: (a) şeffaflık "
    "eksikliği: kullanıcı neden belirli bir içeriği gördüğünü genellikle bilmez; "
    "(b) refah-körü tasarım: sıralama yalnızca etkileşimi optimize eder, kullanıcının "
    "o anki duygusal kırılganlığını hiç hesaba katmaz."
)

altbaslik("2.2. Çözüm Fikri, Özgünlük ve Yerlilik")
govde(
    "Geliştirilen çözüm, iki katmanlı açıklanabilir bir sıralama motorudur: ilgi skoru "
    "(kullanıcının beyan ettiği ilgi alanları) ile refah skoru (olası spiral tespit "
    "edildiğinde AYNI ilgi alanı içinde kalarak daha az tetikleyici içeriğe kayma) "
    "birleştirilir. Motorun akademik bir emsali vardır: \"Collective Well-Being aware "
    "Recommendation Systems (CWB-RS)\" kavramı, etkileşim optimizasyonu yerine uzun "
    "vadeli kümülatif refahı maksimize etmeyi önerir [7]; endüstri/politika düzeyinde de "
    "benzer \"insan-öncelikli\" sıralama ilkeleri savunulmaktadır [8]. Özgünlüğün temel "
    "kaynağı KARA KUTU olmayan bir tasarımdır: sinir ağı tabanlı gizli bir puanlama yerine, "
    "her karar (spiral seviyesi, refah cezası, final skor) denetlenebilir, açıklanabilir "
    "modellerle (lojistik regresyon/SGD) üretilir ve şeffaflık panelinde kullanıcıya "
    "gösterilir. Sistem kasıtlı olarak KONU-NÖTR tasarlanmıştır: siyasi/dini içerik "
    "kategorisine göre karar vermez, yalnızca duygusal yoğunluğa bakar; bu, hem etik "
    "açıdan hem de yerli/milli konumlandırılmış bir platform için stratejik olarak önemli "
    "bir tasarım kararıdır. Yerlilik bileşenleri somuttur: (i) NSosyal'in kendisi T3 Vakfı "
    "ve Baykar Teknoloji tarafından geliştirilen yerli bir platformdur; (ii) duygu analizi "
    "için kullanılan temel model Türkçeye özel eğitilmiştir ve bu model, bağımsız "
    "doğrulamada bulunan bir zayıflık (bkz. Bölüm 3.2) üzerine ekibimiz tarafından "
    "yeniden eğitilerek (fine-tuning) doğruluğu %69,8'den %94,3'e çıkarılmıştır; yani "
    "kullanılan yapay zekâ bileşeni yalnızca tüketilen değil, yerel olarak geliştirilen "
    "bir teknik varlıktır; (iii) NSosyal'in mevcut T3 AI bileşeni (otomatik yanıt, çok "
    "dilli yorumlama, filtreleme/moderasyon), duygu-analizi katmanımızın önerilen bir "
    "uzantısı olarak konumlandırılmıştır."
)

sayfa_sonu()

# ============================================================ 3. TEKNOLOJİ KULLANIMI
baslik("TEKNOLOJİ KULLANIMI")

altbaslik("3.1. İzlenecek Yöntem, Altyapı ve Sürüm Kontrolü")
govde(
    "Backend Python/FastAPI ile geliştirilmiştir; duygu analizi için HuggingFace "
    "Transformers (savasy/bert-base-turkish-sentiment-cased tabanlı, ince ayarlı), "
    "sınıflandırıcılar için scikit-learn (LogisticRegression / SGDClassifier), veri "
    "işleme için NumPy/Pandas kullanılmıştır. Frontend, dwell-time takibi için tarayıcının "
    "yerel Intersection Observer API'sini kullanan sade bir JavaScript/HTML/CSS "
    "arayüzüdür. Haftalık öz-farkındalık raporu, oturum verisini okunabilir bir metne "
    "çeviren Google Gemini API'si (gemini-3.6-flash) ile üretilir; sağlayıcı seçimi "
    "bilinçlidir: Gemini'nin kart istemeyen gerçek bir ücretsiz katmanı, açıklanabilirlik "
    "ilkesiyle çelişmeyen, sağlayıcıdan bağımsız tasarlanmış bir prompt mimarisiyle "
    "kullanılmaktadır. Proje sürüm kontrolü altında geliştirilmiş, düzenli ve anlamlı "
    "commit'lerle ilerletilmiştir; kaynak kod GitHub üzerinde açık bir depoda "
    "saklanmaktadır: https://github.com/samibahar/nsosyal. Depo, commit geçmişiyle "
    "geliştirme sürecinin tamamını (ilk prototip aşamasından güncel sürüme kadar) "
    "takip edilebilir kılar."
)

altbaslik("3.2. Model ve Veri Doğrulama")
govde(
    "Proje, vendor/ilk-varsayım iddialarını sorgulamadan kabul etmek yerine her bileşeni "
    "bağımsız olarak ölçme disiplinini benimser. Duygu modeli için: temel modelin kendi "
    "iddia ettiği doğruluk (%95,4) yerine, winvoker/turkish-sentiment-analysis-dataset "
    "üzerinden bağımsız 1000 örneklik bir test setiyle gerçek doğruluk ölçülmüş (%69,8, "
    "F1 0,778) ve alan kayması (domain shift) kaynaklı bu zayıflık, aynı veri setinin "
    "AYRIK bir bölümüyle (veri sızıntısı önlenerek) ~15.000 örnekle yapılan hedefli bir "
    "ince ayarla düzeltilmiştir (%94,3 doğruluk, F1 0,964; bağımsız olarak yeniden "
    "ölçülmüştür). Spiral tespiti (olası doomscrolling örüntüsü, ikili sınıflandırma), "
    "senaryo-bazlı sentetik veriyle eğitilmiş bir lojistik regresyon modelidir "
    "(doğruluk 0,714, F1 0,748); altı açıklanabilir özellik (negatif dwell oranı, "
    "ortalama duygu, tıklama oranı vb.) kullanır ve öğrenilen katsayılar denetlenebilir "
    "durumdadır. Beş kategorili psikolojik izlenim sınıflandırıcısı (sakin/mutluluk/"
    "umut/sinirli/anksiyete) StandardScaler ile ölçeklenmiş bir SGDClassifier'dır "
    "(F1 makro 0,704). Aşırı öğrenmeyi (overfitting) önlemek için: tüm modellerde "
    "stratified train/test ayrımı, fine-tuning ve bağımsız doğrulama için birbirinden "
    "TAMAMEN ayrık veri bölümleri, ve %10 kasıtlı etiket gürültüsü (gerçek dünyada "
    "sınırların asla net olmadığını modellemek için) kullanılmıştır. Modelin gerçek "
    "performansını iddia etmek yerine SÜREKLİ ölçmek için, kullanıcıya ara sıra hafif "
    "bir onay sorusu (\"şu an gerçekte nasıl hissediyorsun?\") sorulur ve cevap modelin "
    "O ANKİ tahminiyle karşılaştırılır; bu mekanizma psikolojideki Ecological Momentary "
    "Assessment (EMA) yönteminin bağımsız bir uygulamasıdır [1][2]; literatür bu tür "
    "tekrarlı öz-bildirim sorgularının kullanıcı yorgunluğuna (fatigue) yol açabileceğini "
    "de not eder [3], bu yüzden soru sıklığı bilinçli olarak düşük (her ~8 etkileşimde "
    "bir) tutulmuştur."
)

t_ozet = tablo(
    ["Bileşen", "Ölçülen sonuç", "Doğrulama yöntemi"],
    [
        ["Duygu modeli (BERT)", "%94,3 doğruluk (ince ayar sonrası, %69,8'den)",
         "Bağımsız 1000 örnek, vendor iddiasından ayrı ölçüldü"],
        ["Spiral tespiti", "Doğruluk 0,714 / F1 0,748", "Stratified train/test, senaryo verisi"],
        ["Psikolojik izlenim (5 kategori)", "F1 makro 0,704",
         "Ölçek düzeltmesi (StandardScaler) ile 0,686'dan iyileştirildi"],
        ["Kendi kendini doğrulama döngüsü", "Canlı test edildi, çalışır durumda",
         "Gerçek etkileşimde model tahmini ile kullanıcı onayı eşleşti"],
    ],
)

altbaslik("3.3. Kullanıcı Deneyimi (UI/UX) Tasarımı")
govde(
    "Arayüz, NSosyal'in mevcut zaman akışı (timeline) mantığına sadık kalacak şekilde "
    "tasarlanmıştır: her gönderi kartında \"Neden bunu görüyorsun?\" butonuyla açılan bir "
    "şeffaflık paneli, ilgi skoru/refah cezası/final skoru gösterir. \"Tespit edilen "
    "durum\" göstergesi yükseldikçe akışın renk doygunluğu kademeli olarak (kullanıcı "
    "isteğiyle açılıp kapatılabilir bir anahtarla) azalır; bu, engelleyici değil, fark "
    "ettirici bir sinyal olarak tasarlanmıştır. Kullanılabilirlik testleri sırasında "
    "(gerçek kullanım denemeleriyle) birden fazla somut sorun tespit edilip düzeltilmiştir: "
    "aynı gönderiye art arda etkileşim (roket sonra kaydırıp uzaklaşma) önceden sinyali "
    "sessizce eziyordu, sinyal birleştirme mantığıyla giderildi; çok kısa/edilgen bir "
    "görünme (<0,6sn) tam bir gözlem gibi sayılıp barları saptırıyordu, etkileşim-ağırlıklı "
    "ortalamayla düzeltildi; ilk sürümde sayfalama sığ kalıyordu, gerçek sonsuz-kaydırma "
    "(infinite scroll) ile 150 örnek gönderiye genişletildi. Erişilebilirlik açısından: "
    "tüm renk kodlu göstergeler (spiral seviyesi, kategori barları) aynı zamanda metinsel "
    "etiket taşır (yalnızca renge dayanmaz), ve şeffaflık paneli literatürdeki \"az ama "
    "net\" ilkesine uygun kısa/öz tutulmuştur; aşırı detaylı açıklamaların kullanıcı "
    "güvenini azaltabileceği (\"algorithmic aversion\") bulgusuyla uyumludur [9]."
)

sayfa_sonu()

# ============================================================ 4. UYGULANABİLİRLİK
baslik("UYGULANABİLİRLİK")

altbaslik("4.1. Verimlilik ve Etkinlik")
govde(
    "Sistemin sıralama/tespit katmanı bilinçli olarak hafif ve açıklanabilir modeller "
    "(lojistik regresyon, SGD) üzerine kurulmuştur; büyük dil modelleri düzeyinde "
    "hesaplama maliyeti taşımaz; yalnızca isteğe bağlı haftalık rapor üretiminde bir LLM "
    "çağrısı kullanılır. Bu, platforma milyonlarca etkileşimde dahi düşük işletme "
    "maliyetiyle ölçeklenebilirlik sağlar. Etkinlik açısından, refah katmanının "
    "içeriği ELEMEDEN yalnızca yumuşattığı somut olarak gösterilmiştir: kullanıcı testinde "
    "spiral seviyesi yükseldiğinde negatif içerik final skorunda ölçülebilir bir ceza "
    "alıp sırada geriye düşerken, kullanıcının ilgi alanı hiç terk edilmemiştir."
)

altbaslik("4.2. Hedef Kitle")
govde(
    "Doğrudan hedef kitle, NSosyal'in ~700 bin'i aşkın aktif kullanıcısıdır; özellikle "
    "gündem/haber içeriğiyle yoğun etkileşime giren, uzun oturumlar geçiren kullanıcı "
    "segmenti. Dolaylı olarak, sistemin ürettiği şeffaflık ve refah verileri içerik "
    "üreticileri (üretici paneli önerisi) ve platform yöneticileri için de değer taşır. "
    "Genel olarak çözüm, tasarımı gereği herhangi bir sosyal medya platformuna "
    "uyarlanabilir bir mimari sunduğundan hedef kitle NSosyal ile sınırlı kalmayan bir "
    "büyüme potansiyeline sahiptir."
)

altbaslik("4.3. Teknolojik Yenilik ve Uygulanabilirlik")
govde(
    "Ürün, fikir düzeyinde kalmayıp uçtan uca çalışan bir prototiple desteklenmiştir: "
    "gerçek bir BERT modeli, eğitilmiş sınıflandırıcılar, çalışan bir backend/API, "
    "gerçek zamanlı bir arayüz ve canlı test edilmiş bir LLM entegrasyonu içerir. "
    "Teknolojik yenilik düzeyi, tek bir modelin doğruluğunda değil, İKİ AYRI davranış "
    "modelinin (spiral tespiti ve psikolojik izlenim) birbirinden bağımsız çalışıp yalnızca "
    "biri sıralamayı etkileyecek şekilde tasarlanmasında, ve kendi kendini doğrulama "
    "döngüsüyle modelin gerçek performansının sürekli ölçülmesinde yatar. Mimari, yeni "
    "sinyaller (örn. ek etkileşim türleri) veya yeni kategoriler eklemeye açık, "
    "ölçeklenebilir bir yapıya sahiptir; kişiselleştirme mekanizması (online öğrenme, "
    "bkz. Bölüm 6.2) bu ölçeklenebilirliğin somut bir kanıtıdır."
)

sayfa_sonu()

# ============================================================ 5. YAYGIN ETKİ
baslik("YAYGIN ETKİ")

altbaslik("5.1. Toplumsal Fayda ve Erişim Potansiyeli")
govde(
    "Proje, sosyal medya kullanımının olası olumsuz duygusal etkilerini azaltmaya "
    "yönelik somut, ölçülebilir bir katkı sunar. Toplumsal fayda üç düzeyde "
    "değerlendirilebilir: (i) bireysel düzeyde, haftalık öz-farkındalık raporu "
    "kullanıcıya kendi dijital alışkanlıkları hakkında olası örüntüleri (teşhis değil) "
    "gösterir ve isteğe bağlı olarak bir ruh sağlığı uzmanına götürülebilecek, yorumsuz "
    "bir ham veri özeti üretebilir; (ii) platform düzeyinde, refah-farkında sıralama "
    "yaklaşımının akademik emsali [7][8] literatürde giderek daha fazla destek "
    "bulmaktadır; (iii) toplumsal düzeyde, konu-nötr ve reklam-manipülasyonuna kapalı "
    "tasarım ilkesi (bkz. Bölüm 2.2), yerli bir platformun kullanıcı refahını önceleyen "
    "bir marka değeri inşa etmesine katkı sağlayabilir. Erişim potansiyeli, sistemin "
    "NSosyal'in mevcut kullanıcı tabanının tamamına (herhangi bir ek donanım veya "
    "kullanıcı eğitimi gerektirmeden, arka planda çalışan bir katman olarak) doğrudan "
    "ulaşabilecek şekilde tasarlanmış olmasından kaynaklanır."
)

sayfa_sonu()

# ============================================================ 6. SÜRDÜRÜLEBİLİRLİK
baslik("SÜRDÜRÜLEBİLİRLİK")

altbaslik("6.1. Ticarileştirme Potansiyeli ve İş Modeli")
govde(
    "NSosyal vakıf tabanlı ve reklamsız bir platform olduğundan klasik reklam gelirine "
    "dayalı bir model zorlanmamıştır; bunun yerine dört tamamlayıcı yön önerilmektedir: "
    "(i) düşük işletme maliyeti: hafif/açıklanabilir modeller büyük dil modelleri kadar "
    "pahalı değildir, bu doğrudan bir maliyet avantajına dönüşür; (ii) anonim/toplu "
    "\"dijital refah eğilimleri\" verisiyle üniversite, TÜBİTAK veya ruh sağlığı sivil "
    "toplum kuruluşlarıyla araştırma ortaklığı (kişisel veri paylaşılmadan, yalnızca "
    "toplu istatistik düzeyinde); (iii) \"dijital-refah-öncelikli platform\" marka "
    "değeri üzerinden kurumsal sponsorluk; (iv) mevcut roket sistemine benzer, "
    "gönüllülük esaslı opsiyonel destek/bağış mekanizması. Bu model, ürünün mevcut pazar "
    "şartlarında (vakıf-destekli, reklamsız yerli platform bağlamında) üretilebilir "
    "olmasını gerçekçi bir temele oturtur."
)

altbaslik("6.2. Finansal, Teknik ve Sosyal Sürdürülebilirlik")
govde(
    "Finansal sürdürülebilirlik, düşük işletme maliyetli mimari tercihinden "
    "(büyük/pahalı modeller yerine açıklanabilir, hafif sınıflandırıcılar) doğrudan "
    "gelir. Teknik sürdürülebilirlik için, sistemin kişiselleştirme mekanizması "
    "(SGDClassifier'ın partial_fit özelliğiyle çevrimiçi öğrenme) örnek bir prototip "
    "olarak uygulanmış ve dürüstçe sınırları belirtilmiştir. Literatür, davranıştan "
    "duygu-durumu çıkarımının meşru ama kişiye-özgü kalibrasyon olmadan sınırlı kaldığını "
    "göstermektedir [6]; kişiselleştirme mekanizması tam olarak bu ihtiyaca yönelik bir "
    "ilk adımdır. Demo ortamında "
    "öğrenme adımı görünür olması için kasıtlı büyütülmüştür, gerçek üretimde çok daha "
    "küçük bir adım büyüklüğü ve düzenlileştirme/sınır (clipping) eklenmesi gerektiği "
    "açıkça not edilmiştir; bu, değişen kullanıcı ihtiyaçlarına zamanla uyum "
    "sağlayabilecek bir temel sunar. Sosyal sürdürülebilirlik açısından, modelin "
    "sınırlılıkları (sentetik eğitim verisi, klinik doğrulama eksikliği) raporun her "
    "aşamasında dürüstçe belirtilmiş, kendi kendini doğrulama döngüsüyle sistemin "
    "zamanla gerçek kullanıcı geri bildirimiyle kalibre edilebilecek bir altyapı "
    "kurulmuştur; bu, kullanıcı güveninin uzun vadede korunmasını destekler."
)

sayfa_sonu()

# ============================================================ 7. PROJE TAKVİMİ
baslik("PROJE TAKVİMİ")

altbaslik("7.1. İş Paketleri ve Zamanlama")
govde(
    "Aşağıdaki takvim, yarışma takvimiyle (Teknik Rapor Teslimi: 24 Ağustos 2026; "
    "Mentörlük Süreci: 2-7 Eylül 2026; Final Sunumları: 14 Eylül 2026) çelişmeyecek "
    "şekilde planlanmıştır. Tamamlanan iş paketleri, bu raporun dayandığı çalışan "
    "prototipi kapsar; ilerleyen iş paketleri mentörlük ve final aşamasına "
    "hazırlığı hedefler."
)

t_takvim = tablo(
    ["İş Paketi", "Kapsam", "Dönem", "Durum"],
    [
        ["İP1: Mimari ve ilk prototip",
         "İki katmanlı sıralama motoru, spiral/psikolojik model tasarımı, sözlük-tabanlı ilk doğrulama",
         "Ağustos (1. hafta)", "Tamamlandı"],
        ["İP2: Gerçek model entegrasyonu",
         "BERT entegrasyonu, bağımsız doğrulama, ince ayar, sınıflandırıcı eğitimi",
         "Ağustos (2. hafta)", "Tamamlandı"],
        ["İP3: Backend/arayüz ve kullanıcı testi",
         "FastAPI backend, web arayüzü, kullanılabilirlik testleri ve düzeltmeler",
         "Ağustos (2-3. hafta)", "Tamamlandı"],
        ["İP4: Şeffaflık, rapor ve doğrulama döngüsü",
         "LLM destekli haftalık rapor, kendi kendini doğrulama döngüsü, kişiselleştirme",
         "Ağustos (3. hafta)", "Tamamlandı"],
        ["İP5: Teknik rapor ve sürüm kontrolü",
         "Teknik rapor yazımı, GitHub deposunun düzenlenmesi ve teslimi",
         "24 Ağustos 2026'ya kadar", "Tamamlandı"],
        ["İP6: Mentörlük geri bildirimlerinin uygulanması",
         "Mentör önerileri doğrultusunda model/mimari iyileştirmeleri",
         "2-7 Eylül 2026", "Planlandı"],
        ["İP7: Kişiye-özgü kalibrasyon ve genişletme",
         "Kişiselleştirme mekanizmasının düzenlileştirme ile güçlendirilmesi, gelecek-"
         "vizyonu özelliklerinin (Perspektif Köprüsü vb.) fizibilite çalışması",
         "Eylül (1-2. hafta)", "Planlandı"],
        ["İP8: Final sunum ve canlı demo hazırlığı",
         "Sunum dosyası, kullanıcı senaryoları, canlı demo akışının hazırlanması",
         "14 Eylül 2026'ya kadar", "Planlandı"],
    ],
)

sayfa_sonu()

# ============================================================ 8. TAKIM YAPISI
baslik("TAKIM YAPISI")

altbaslik("8.1. Takım Organizasyonu ve Roller")
govde(
    "Değerlendirme esasları gereği takım üyelerinin isim ve fotoğraf gibi kişisel "
    "bilgilerine bu bölümde yer verilmemiştir. Takım, yarışma kayıt şartına uygun "
    "olarak 2-5 kişi ve bir takım kaptanından oluşmaktadır; görev dağılımı aşağıda "
    "disiplin/rol bazında özetlenmiştir."
)

t_takim = tablo(
    ["Rol", "Katkı Alanı"],
    [
        ["Takım Kaptanı / Proje Yönetimi", "Genel koordinasyon, yarışma süreç takibi, teslim yönetimi"],
        ["Yazılım Geliştirme (Backend)", "FastAPI backend, API tasarımı, sürüm kontrolü"],
        ["Yapay Zekâ / Veri Bilimi", "Model eğitimi, bağımsız doğrulama, ince ayar, performans ölçümü"],
        ["Ürün / UI-UX Tasarımı", "Arayüz tasarımı, kullanıcı akışları, kullanılabilirlik testleri"],
        ["Araştırma ve Dokümantasyon", "Literatür taraması, teknik rapor, kaynakça"],
    ],
)
notv(
    "Not: Tablo, projede yürütülen disiplin bazlı katkı alanlarını göstermektedir; "
    "ekip büyüklüğü ve isimlendirme yarışma kayıt sistemindeki resmi bilgilerle "
    "tutarlıdır."
)

sayfa_sonu()

# ============================================================ KAYNAKÇA
baslik("KAYNAKÇA")

kaynaklar = [
    "[1] Investigating Best Practices for Ecological Momentary Assessment, JMIR, "
    "26:e50275, 2024. Erişim: https://www.jmir.org/2024/1/e50275",
    "[2] Measuring Criterion Validity of Microinteraction Ecological Momentary "
    "Assessment (Micro-EMA), PMC7991987. Erişim: "
    "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7991987/",
    "[3] Modeling Behaviour to Predict User State: Self-Reports as Ground Truth, "
    "arXiv:2007.14461. Erişim: https://arxiv.org/pdf/2007.14461",
    "[4] Are active and passive social media use related to mental health, wellbeing, "
    "and social support outcomes? A meta-analysis, Journal of Computer-Mediated "
    "Communication, 29(1), zmad055, 2024. Erişim: "
    "https://academic.oup.com/jcmc/article/29/1/zmad055/7595758",
    "[5] Beyond the Scroll: Intolerance of Uncertainty and Doomscrolling, "
    "ScienceDirect, 2024. Erişim: "
    "https://www.sciencedirect.com/science/article/abs/pii/S0191886924003799",
    "[6] Passive Sensing for Mental Health Monitoring Using Machine Learning with "
    "Wearables and Smartphones: A Scoping Review, JMIR, 2025. Erişim: "
    "https://www.jmir.org/2025/1/e77066",
    "[7] Challenging Social Media Threats using Collective Well-being Aware "
    "Recommendation Algorithms and Multi-objective Optimization, arXiv:2102.04211. "
    "Erişim: https://arxiv.org/pdf/2102.04211",
    "[8] Better Feeds: Algorithms That Put People First, Georgetown University "
    "Knight-Georgetown Institute, Mart 2025, Erişim Tarihi: 19.08.2026, Erişim: "
    "https://kgi.georgetown.edu/wp-content/uploads/2025/02/Better-Feeds_-Algorithms-That-Put-People-First.pdf",
    "[9] Explainable recommendation: when design meets trust calibration, World Wide "
    "Web (Springer), 2021. Erişim: "
    "https://link.springer.com/article/10.1007/s11280-021-00916-0",
    "[10] Robertson, C.E., Pröllochs, N., Schwarzenegger, K., Pärnamets, P., Van "
    "Bavel, J.J., Feuerriegel, S., (2023) Negativity drives online news consumption, "
    "Nature Human Behaviour, 7, 812-822. Erişim: "
    "https://www.nature.com/articles/s41562-023-01538-4",
    "[11] Negative online news articles are shared more to social media, Scientific "
    "Reports (Nature), 2024. Erişim: https://www.nature.com/articles/s41598-024-71263-z",
    "[12] Negativity Spreads More than Positivity on Twitter After Both Positive and "
    "Negative Political Situations, PMC9383030. Erişim: "
    "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9383030/",
    "[13] The Facebook Files, The Wall Street Journal, 2021, Erişim Tarihi: "
    "19.08.2026, Erişim: https://www.wsj.com/articles/the-facebook-files-11631713039",
    "[14] Confidential Facebook document reveals leverage over vulnerable teens, "
    "The Australian, 2017 (haber kaynağı; ABD Kongresi'ne sunulan iç belgelerle "
    "ilişkilendirilmiştir).",
    "[15] savasy/bert-base-turkish-sentiment-cased, HuggingFace model kartı, Erişim "
    "Tarihi: 19.08.2026, Erişim: https://huggingface.co/savasy/bert-base-turkish-sentiment-cased",
    "[16] winvoker/turkish-sentiment-analysis-dataset, HuggingFace veri seti, Erişim "
    "Tarihi: 19.08.2026, Erişim: https://huggingface.co/datasets/winvoker/turkish-sentiment-analysis-dataset",
]
for k in kaynaklar:
    p = doc.add_paragraph(k)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15

doc.save(DOSYA)
print(f"Olusturuldu: {DOSYA}")
