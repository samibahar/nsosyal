"""
Gerçek Türkçe duygu analizi modeli — savasy/bert-base-turkish-sentiment-cased.
spike_poc.py'deki sözlük-tabanlı duygu_skoru() fonksiyonunun yerini alır, aynı
arayüzü (-1 ile +1 arası float) korur ki geri kalan mimari (skor motoru, refah
katmanı, spiral tespiti) değişmeden çalışsın.

Model ikili (pozitif/negatif) sınıflandırma yapıyor, nötr sınıfı yok — bu yüzden
nötr/duygu içermeyen cümlelerde bile model bir yöne (zayıf bir güven skoruyla)
karar veriyor. Bu, gerçek sürümde raporda dürüstçe belirtilmesi gereken bir
sınırlılık (savasy modelinin kendi kart bilgisine göre %95.4 doğruluk; bizim
dogrulama.py ile ölçtüğümüz bağımsız doğruluk %69.8 -- bkz. CLAUDE.md).

İNCE AYARLI MODEL: ince_ayar.py, alan kayması sorununu azaltmak için bu modeli
winvoker veri setiyle devam ederek eğitip models/bert-turkish-sentiment-ince-ayarli/
klasörüne kaydediyor. Bu modül önce o yerel klasörü dener, yoksa (henüz eğitim
bitmediyse ya da hiç çalıştırılmadıysa) orijinal HF Hub modeline düşer -- yani
fine-tuning bitmeden de, bittikten sonra da kod değişikliği gerekmeden çalışır.
"""
from pathlib import Path

from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

_MODEL_ADI_ORIJINAL = "savasy/bert-base-turkish-sentiment-cased"
_INCE_AYARLI_DIZIN = Path(__file__).resolve().parent / "models" / "bert-turkish-sentiment-ince-ayarli"
_INCE_AYARLI_V2_DIZIN = Path(__file__).resolve().parent / "models" / "bert-turkish-sentiment-ince-ayarli-v2"
_pipeline = None
_kullanilan_model = None


def _yukle():
    global _pipeline, _kullanilan_model
    if _pipeline is None:
        # v2 (ince_ayar_v2.py), zayıf alt-türe (kısa/resmi/haber-bülteni) hedefli
        # ikinci tur ince ayarın çıktısı -- bağımsız doğrulamada (dogrulama_v2.py,
        # 20.08.2026) winvoker genel test setinde küçük bir gerileme (%94,3->%93,3)
        # karşılığında hedef alt-türde büyük bir düzelme gösterdi (26 değişen
        # tahminin ~22'si, v1'in "negatif haberi pozitif sanma" hatasını düzeltti).
        # NSosyal içeriği winvoker'ın genel dağılımından çok bu alt-türe yakın
        # olduğundan v2 tercih edilir.
        if _INCE_AYARLI_V2_DIZIN.exists():
            kaynak = str(_INCE_AYARLI_V2_DIZIN)
        elif _INCE_AYARLI_DIZIN.exists():
            kaynak = str(_INCE_AYARLI_DIZIN)
        else:
            kaynak = _MODEL_ADI_ORIJINAL
        model = AutoModelForSequenceClassification.from_pretrained(kaynak)
        tokenizer = AutoTokenizer.from_pretrained(kaynak)
        _pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
        _kullanilan_model = kaynak
    return _pipeline


def duygu_skoru(metin: str) -> float:
    """-1 (çok negatif) ile +1 (çok pozitif) arasında bir skor döndürür.
    Etiket adı transformers sürümüne göre "positive"/"LABEL_1" gibi değişebildiği
    için içeriğe göre (alt string eşleşmesi) esnek biçimde yorumlanır."""
    sa = _yukle()
    sonuc = sa(metin, truncation=True)[0]
    etiket = sonuc["label"].lower()
    isaret = 1.0 if ("pos" in etiket or etiket in ("1", "label_1")) else -1.0
    return isaret * sonuc["score"]


if __name__ == "__main__":
    ornekler = [
        "Takımımız bu hafta harika bir galibiyet aldı, çok sevindim!",
        "Transfer draması yüzünden taraftarlar arasında büyük öfke var.",
        "Mahkeme, savaş suçlarından idam cezasına mahkum etti.",
        "Yeni bir toplantı yarın saat 14.00'te başlayacak.",
        "Antrenman sonrası oyuncular keyifli bir sohbet yaptı.",
        "Tutuklama haberi sonrası sosyal medyada büyük kaygı oluştu.",
    ]
    duygu_skoru("ısınma")  # _yukle() tetiklenip _kullanilan_model doldurulsun
    print(f"Kullanılan model: {_kullanilan_model}\n")
    for m in ornekler:
        print(f"{duygu_skoru(m):+.3f}  <- {m}")
