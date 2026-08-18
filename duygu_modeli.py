"""
Gerçek Türkçe duygu analizi modeli — savasy/bert-base-turkish-sentiment-cased.
spike_poc.py'deki sözlük-tabanlı duygu_skoru() fonksiyonunun yerini alır, aynı
arayüzü (-1 ile +1 arası float) korur ki geri kalan mimari (skor motoru, refah
katmanı, spiral tespiti) değişmeden çalışsın.

Model ikili (pozitif/negatif) sınıflandırma yapıyor, nötr sınıfı yok — bu yüzden
nötr/duygu içermeyen cümlelerde bile model bir yöne (zayıf bir güven skoruyla)
karar veriyor. Bu, gerçek sürümde raporda dürüstçe belirtilmesi gereken bir
sınırlılık (savasy modelinin kendi kart bilgisine göre %95.4 doğruluk).
"""
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

_MODEL_ADI = "savasy/bert-base-turkish-sentiment-cased"
_pipeline = None


def _yukle():
    global _pipeline
    if _pipeline is None:
        model = AutoModelForSequenceClassification.from_pretrained(_MODEL_ADI)
        tokenizer = AutoTokenizer.from_pretrained(_MODEL_ADI)
        _pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
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
    print(f"Model yükleniyor: {_MODEL_ADI}\n")
    for m in ornekler:
        print(f"{duygu_skoru(m):+.3f}  <- {m}")
