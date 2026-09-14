"""Yoğun içerik sözlüğü: ton modelinin haber üslubunda kaçırdığı açık olumsuz olayları yakalar.

Gerçek veri testinde (14.09.2026) uygulamadaki ton modeli (v3), gerçek haber
başlıklarındaki güçlü olumsuz haberlerin yalnızca %6–8'ini yoğun sayıyordu
("…işçi öldü" → +0,91): model üslubu okuyor, olayı okumuyor. Bu liste ölüm,
şiddet, afet ve istismar gibi açık olayları adıyla yakalar; eşleşen metnin
tonu en fazla SOZLUK_TONU olur (yalnızca aşağı çekilir, hiç yukarı çekilmez).

Ölçüm: liste yazılırken hiç bakılmamış, elle etiketlenmiş 100 gerçek başlıkta
güçlü olumsuz yakalama %6 → %83; işaretlenenlerin %97'si gerçekten olumsuz.
Eğitim gerektirmez ve açıklanabilirdir: "Neden bu?" eşleşen sözcüğü gösterir.

Bilerek dışarıda bırakılanlar: çıplak "deprem", "sel", "felaket" (yeniden
yapılanma ve yardım haberlerini işaretliyordu; ölüm ve yaralanma zaten ayrıca
yakalanır), "şiddetli" (hava durumu), "şiddetle mücadele", "kazan-" (kaza ile
karışmasın), "çarpıcı" ve "gölü" (ölü ile karışmasın).

Her sözcük kelime başında aranır: Türkçede kök başta, ekler sonda olduğu için
kelime içi eşleşme hep yanlış alarmdı ("bilinçli" → linç, "başvuru" → vurul,
"ispatlanmış" → patla; gerçek havuzlarda 81 metin).
"""
import re

SOZLUK_TONU = -0.9
_DESEN = re.compile(
    r"\b(?:öl(dü|ü|dür|en)|hayatını kaybet|can kayb|can verdi|yaral|hastanelik|cinayet|katled|katliam|katil|vurul|bıçak|"
    r"saldır|terör|şehit|yangın|kaza(\b|da|sı|ya|lar)|çarp(ış|tı|an|ma)|devril|taciz|istismar|tecavüz|şiddet(?!li|le mücadele)|"
    r"dehşet|vahşet|facia|enkaz|ceset|intihar|patla|çöktü|yıkıl|kavga|silahlı|rehin|linç|savaş|bombal|yaktı\b|yakıl|yakarak|sabotaj)"
)


def _kucuk(metin: str) -> str:
    """Türkçe küçük harf: str.lower() "İ"yi noktalı iki karaktere, "I"yı "i"ye çeviriyor."""
    return metin.replace("I", "ı").replace("İ", "i").lower()


def yogun_sozcuk(metin: str) -> str | None:
    """Metinde açık bir olumsuz olay sözcüğü varsa onu, yoksa None döndürür."""
    eslesme = _DESEN.search(_kucuk(metin or ""))
    return eslesme.group(0) if eslesme else None


def sistem_tonu(model_tonu: float, metin: str) -> tuple[float, str | None]:
    """Uygulamanın kullandığı ton: model tonu, açık olay sözcüğü varsa en fazla SOZLUK_TONU."""
    sozcuk = yogun_sozcuk(metin)
    return (min(model_tonu, SOZLUK_TONU), sozcuk) if sozcuk else (model_tonu, None)
