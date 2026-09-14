"""Yoğun içerik sözlüğü: ton modelinin haber üslubunda kaçırdığı açık olumsuz olayları yakalar.

Gerçek veri testinde (14.09.2026) uygulamadaki ton modeli (v3), gerçek haber
başlıklarındaki güçlü olumsuz haberlerin yalnızca %6–8'ini yoğun sayıyordu
("…işçi öldü" → +0,91): model üslubu okuyor, olayı okumuyor. Bu liste ölüm,
şiddet, afet ve istismar gibi açık olayları adıyla yakalar; eşleşen metnin
tonu en fazla SOZLUK_TONU olur (yalnızca aşağı çekilir, hiç yukarı çekilmez).

Ölçüm: liste yazılırken hiç bakılmamış, elle etiketlenmiş 100 gerçek başlıkta
güçlü olumsuz yakalama %6 → %83; işaretlenenlerin %97'si gerçekten olumsuz.
Eğitim gerektirmez ve açıklanabilirdir: "Neden bu?" eşleşen sözcüğü gösterir.
Bu oranlar ilk sözlüğün tarihsel sonucudur; güncel karaktersiz yazım
değerlendirmesi docs/gorunurluk_ve_final_dogrulamasi.md içindedir.

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
SOZCUKLER = [
    r"öl(dü|ü|dür|en)", r"hayatını kaybet", r"can kayb", r"can verdi", r"yaral",
    r"hastanelik", r"cinayet", r"katled", r"katliam", r"katil(?![ıi]m)", r"vurul", r"bıçak",
    r"saldır", r"terör", r"şehit", r"yangın", r"kaza(\b|da|sı(?!z)|ya|lar)",
    r"çarp(ış|tı|an|ma)", r"devril", r"taciz", r"istismar", r"tecavüz", r"şiddet(?!li|le mücadele)",
    r"dehşet", r"vahşet", r"facia", r"enkaz", r"ceset", r"intihar", r"patla", r"çöktü",
    r"yıkıl", r"kavga", r"silahlı", r"rehin", r"linç", r"savaş", r"bombal", r"yaktı\b",
    r"yakıl", r"yakarak", r"sabotaj",
]
_DESEN = re.compile(r"\b(?:" + "|".join(SOZCUKLER) + ")")
_KATLA = str.maketrans("çğıöşüâîû", "cgiosuaiu")
_KATLANMAZ = {r"öl(dü|ü|dür|en)", r"katil(?![ıi]m)", r"çöktü"}
_ASCII_DESEN = re.compile(r"\b(?:" + "|".join(s.translate(_KATLA) for s in SOZCUKLER if s not in _KATLANMAZ) + ")")

# Açıkça eğitim, araç ya da mecaz bildiren ifadeler olay kanıtı değildir.
# Yalnızca eşleşen ifade atlanır; cümledeki başka bir olay hâlâ yakalanır.
_OLAY_DISI = re.compile(
    r"\b(?:yangın\s+(?:tatbikat\w*|eğitim\w*|söndürme\s+(?:tüp\w*|cihaz\w*))|"
    r"bıçak\s+(?:set\w*|bileme\w*)|"
    r"(?:satış\w*|talep\w*|ihracat\w*|kahkaha\w*)\s+patla\w*)"
)
_ASCII_OLAY_DISI = re.compile(_OLAY_DISI.pattern.translate(_KATLA))


def _kucuk(metin: str) -> str:
    """Türkçe küçük harf: str.lower() "İ"yi noktalı iki karaktere, "I"yı "i"ye çeviriyor."""
    return metin.replace("I", "ı").replace("İ", "i").lower()


def yogun_sozcuk(metin: str) -> str | None:
    """Metinde açık bir olumsuz olay sözcüğü varsa onu, yoksa None döndürür."""
    metin = _kucuk(metin or "")
    katli = metin.translate(_KATLA)
    olay_disi = [m.span() for m in _OLAY_DISI.finditer(metin)] + [m.span() for m in _ASCII_OLAY_DISI.finditer(katli)]
    for eslesme in _DESEN.finditer(metin):
        if not any(bas <= eslesme.start() < son for bas, son in olay_disi):
            return eslesme.group(0)
    for eslesme in _ASCII_DESEN.finditer(katli):
        if not any(bas <= eslesme.start() < son for bas, son in olay_disi):
            return metin[eslesme.start():eslesme.end()]
    return None


def sistem_tonu(model_tonu: float, metin: str) -> tuple[float, str | None]:
    """Uygulamanın kullandığı ton: model tonu, açık olay sözcüğü varsa en fazla SOZLUK_TONU."""
    sozcuk = yogun_sozcuk(metin)
    return (min(model_tonu, SOZLUK_TONU), sozcuk) if sozcuk else (model_tonu, None)
