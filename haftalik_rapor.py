"""
LLM destekli "haftalık öz-farkındalık raporu" üretimi — CLAUDE.md'de baştan beri
planlanan ama önce statik bir örnekle gösterilen özelliğin gerçek hâli.

Gerçek oturum verisinden (psikolojik_durum kategorileri, konu, saat) bir özet
çıkarılıp Claude API'sine prompt olarak verilir; model bunu okunabilir, nazik,
TEŞHİS OLMAYAN bir rapor metnine çevirir. API anahtarı yoksa (ör. .env dosyası
eksikse) `mevcut()` False döner ve arayüz zaten var olan statik örneğe düşer --
kod hiçbir zaman "sahte" bir LLM çıktısı uydurmaz.
"""
import os

from dotenv import load_dotenv

load_dotenv()

MODEL_ADI = "claude-sonnet-5"

SISTEM_TALIMATI = """Sen NSosyal platformu için "haftalık öz-farkındalık raporu" yazan bir asistansın.
Kurallar (KESİNLİKLE uy):
- Bu bir teşhis veya klinik değerlendirme DEĞİL. "Kesin", "tanı", "hasta", "bozukluk" gibi kelimeler kullanma.
- "Tespit ettik" değil "gözlemledik", "kesin" değil "olası" gibi temkinli bir dil kullan.
- Siyasi/dini içerik kategorisine değinme -- sadece duygusal yoğunluk ve davranış örüntüsünden bahset.
- Kullanıcıyı suçlayıcı ya da endişelendirici bir tonda YAZMA -- nazik, meraklı, destekleyici bir ton kullan.
- Çıktı düz metin olsun, üç kısa bölüm halinde: "Gözlemlenen olası örüntü", "İyi gidenler", "Nazik bir not".
  Her bölüm başlığını tam bu şekilde yaz (## ile başlat), altına 2-4 cümlelik bir paragraf yaz.
- Sadece verilen gerçek sayılara dayan, uydurma detay ekleme."""


def mevcut() -> bool:
    return bool(os.environ.get("ANTHROPIC_API_KEY"))


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


def uret(psikolojik_ozet: dict, dogrulama_ozet: dict) -> dict:
    """API anahtarı yoksa {"mevcut": False, ...} döner -- arayüz statik örneğe düşer."""
    if not mevcut():
        return {"mevcut": False, "sebep": "ANTHROPIC_API_KEY tanımlı değil"}

    from anthropic import Anthropic

    veri_ozeti = _ozet_metni_olustur(psikolojik_ozet, dogrulama_ozet)
    istemci = Anthropic()
    yanit = istemci.messages.create(
        model=MODEL_ADI,
        max_tokens=600,
        system=SISTEM_TALIMATI,
        messages=[{
            "role": "user",
            "content": f"Bu oturumda gerçekten kaydedilen veri özeti:\n\n{veri_ozeti}\n\n"
                       f"Bu veriye dayanarak haftalık öz-farkındalık raporu metnini yaz.",
        }],
    )
    metin = "".join(blok.text for blok in yanit.content if blok.type == "text")
    return {"mevcut": True, "metin": metin, "veri_ozeti": veri_ozeti}
