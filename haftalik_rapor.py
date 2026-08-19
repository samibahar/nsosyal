"""
LLM destekli "haftalık öz-farkındalık raporu" üretimi — CLAUDE.md'de baştan beri
planlanan ama önce statik bir örnekle gösterilen özelliğin gerçek hâli.

Gerçek oturum verisinden (psikolojik_durum kategorileri, konu, saat) bir özet
çıkarılıp Gemini API'sine prompt olarak verilir; model bunu okunabilir, nazik,
TEŞHİS OLMAYAN bir rapor metnine çevirir. API anahtarı yoksa (ör. .env dosyası
eksikse) `mevcut()` False döner ve arayüz zaten var olan statik örneğe düşer --
kod hiçbir zaman "sahte" bir LLM çıktısı uydurmaz.

Gemini kullanılıyor (Claude değil) -- ücretsiz katmanı olduğu için (bkz. CLAUDE.md,
19.08.2026 notu). Mantık/prompt tasarımı sağlayıcıdan bağımsız, istenirse
Anthropic'e geri dönmek tek fonksiyonu (uret) değiştirmek kadar basit.
"""
import os

from dotenv import load_dotenv

load_dotenv()

MODEL_ADI = "gemini-3.6-flash"

SISTEM_TALIMATI_KISISEL = """Sen NSosyal platformu için "haftalık öz-farkındalık raporu" yazan bir asistansın.
Kurallar (KESİNLİKLE uy):
- Bu bir teşhis veya klinik değerlendirme DEĞİL. "Kesin", "tanı", "hasta", "bozukluk" gibi kelimeler kullanma.
- "Tespit ettik" değil "gözlemledik", "kesin" değil "olası" gibi temkinli bir dil kullan.
- Siyasi/dini içerik kategorisine değinme -- sadece duygusal yoğunluk ve davranış örüntüsünden bahset.
- Kullanıcıyı suçlayıcı ya da endişelendirici bir tonda YAZMA -- nazik, meraklı, destekleyici bir ton kullan.
- Çıktı düz metin olsun, üç kısa bölüm halinde: "Gözlemlenen olası örüntü", "İyi gidenler", "Nazik bir not".
  Her bölüm başlığını tam bu şekilde yaz (## ile başlat), altına 2-4 cümlelik bir paragraf yaz.
- Sadece verilen gerçek sayılara dayan, uydurma detay ekleme."""

# Terapiste/uzmana götürülmek üzere hazırlanan varyant -- kullanıcı isteğiyle
# eklendi (19.08.2026). Kritik fark: kişisel raporun aksine YORUM/tavsiye
# YAPMAZ, sadece ham davranışsal veriyi düzenli sunar -- nihai değerlendirme
# uzmana ait olduğu için model burada bir adım daha geri durmalı.
SISTEM_TALIMATI_TERAPIST = """Sen NSosyal platformunun kullanıcı davranış verisinden, kullanıcının kendi
isteğiyle bir ruh sağlığı uzmanına GÖTÜREBİLECEĞİ yapılandırılmış bir VERİ ÖZETİ hazırlayan bir asistansın.
Kurallar (KESİNLİKLE uy):
- Bu KESİNLİKLE bir teşhis, klinik değerlendirme veya tavsiye DEĞİL -- "tanı", "hasta", "bozukluk",
  "tedavi" gibi kelimeler kullanma. Yorum yapma, öneri verme, sonuç çıkarma -- sadece VERİYİ düzenli sun.
- İlk cümlede açıkça belirt: bu, kullanıcının kendi isteğiyle bir uzmana götürebileceği, uygulamanın
  kaydettiği DAVRANIŞSAL veri özetidir; klinik bir belge değildir, nihai değerlendirme uzmana aittir.
- Üçüncü şahıs, nötr, açıklayıcı bir dil kullan -- bir gözlem günlüğü özeti gibi, bir doktor raporu gibi DEĞİL.
- Sayısal verileri (kategori dağılımı, doğrulama/eşleşme oranı, saat/konu örüntüleri) olduğu gibi ver,
  yorumlama veya ciddiyet derecesi atama.
- Siyasi/dini içerik kategorisine değinme -- sadece duygusal yoğunluk ve davranış örüntüsünden bahset.
- Çıktı düz metin olsun, şu bölümlerle: "Veri Özeti", "Gözlemlenen Davranışsal Örüntüler", "Sınırlılıklar".
  Her başlığı tam bu şekilde yaz (## ile başlat). "Sınırlılıklar" bölümünde MUTLAKA şunu tekrar et: bu
  veriler sentetik senaryolarla eğitilmiş bir modelden geliyor, klinik doğrulaması yok, kullanıcının kendi
  onaylarıyla kısmen sınanıyor, ve TEK BAŞINA hiçbir karar/değerlendirme için yeterli değil.
- Sadece verilen gerçek sayılara dayan, uydurma detay ekleme."""


def mevcut() -> bool:
    return bool(os.environ.get("GEMINI_API_KEY"))


def _ozet_metni_olustur(psikolojik_ozet: dict, dogrulama_ozet: dict) -> str:
    toplam = psikolojik_ozet.get("toplam_etkilesim", 0)
    dagilim = psikolojik_ozet.get("kategori_dagilimi", {})
    en_konu = psikolojik_ozet.get("en_belirgin_konu_kategori", [])
    en_saat = psikolojik_ozet.get("en_belirgin_saat_kategori", [])

    satirlar = [f"Bu oturumda toplam {toplam} farklı gönderiyle etkileşim kaydedildi."]
    if dagilim:
        dagilim_str = ", ".join(f"{k}: {v}" for k, v in dagilim.items() if v)
        satirlar.append(f"Kategori dağılımı: {dagilim_str}.")
    if en_konu:
        for kayit in en_konu[:3]:
            satirlar.append(
                f"\"{kayit['konu']}\" konulu içerikte {kayit['sayi']} kez \"{kayit['kategori']}\" "
                f"kategorisine giren bir tepki kaydedildi."
            )
    if en_saat:
        for kayit in en_saat[:2]:
            satirlar.append(
                f"Saat {kayit['saat']}:00 civarında {kayit['sayi']} kez \"{kayit['kategori']}\" "
                f"kategorisine giren tepkiler görüldü."
            )
    if dogrulama_ozet.get("toplam_onay"):
        satirlar.append(
            f"Kullanıcı {dogrulama_ozet['toplam_onay']} kez kendi durumunu onayladı, "
            f"bunların {dogrulama_ozet['eslesen']} tanesi modelin tahminiyle eşleşti "
            f"(eşleşme oranı: %{round((dogrulama_ozet.get('eslesme_orani') or 0) * 100)})."
        )
    return "\n".join(satirlar)


def uret(psikolojik_ozet: dict, dogrulama_ozet: dict, hedef: str = "kisisel") -> dict:
    """API anahtarı yoksa {"mevcut": False, ...} döner -- arayüz statik örneğe düşer.
    `hedef`: "kisisel" (varsayılan, sıcak/destekleyici öz-farkındalık raporu) veya
    "terapist" (yorumsuz, ham veri özeti -- kullanıcının bir uzmana götürebileceği)."""
    if not mevcut():
        return {"mevcut": False, "sebep": "GEMINI_API_KEY tanımlı değil"}

    from google import genai
    from google.genai import types

    veri_ozeti = _ozet_metni_olustur(psikolojik_ozet, dogrulama_ozet)
    sistem_talimati = SISTEM_TALIMATI_TERAPIST if hedef == "terapist" else SISTEM_TALIMATI_KISISEL
    kullanici_istegi = (
        "Bu oturumda gerçekten kaydedilen veri özeti:\n\n{}\n\n"
        "Bu veriye dayanarak {} metnini yaz."
    ).format(
        veri_ozeti,
        "bir uzmana götürülebilecek yapılandırılmış veri özeti" if hedef == "terapist"
        else "haftalık öz-farkındalık raporu",
    )

    istemci = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    yanit = istemci.models.generate_content(
        model=MODEL_ADI,
        contents=kullanici_istegi,
        config=types.GenerateContentConfig(
            system_instruction=sistem_talimati,
            max_output_tokens=2048,
            thinking_config=types.ThinkingConfig(thinking_level="low"),
        ),
    )
    metin = yanit.text
    return {"mevcut": True, "metin": metin, "veri_ozeti": veri_ozeti, "hedef": hedef}
