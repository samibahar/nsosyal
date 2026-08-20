# -*- coding: utf-8 -*-
"""Zayıf alt-tür için hedefli sentetik eğitim verisi üretimi.

dogrulama.py/ince_ayar.py'nin bağımsız ölçümleri, hem orijinal hem ince ayarlı
modelin kısa/resmi/üçüncü-şahıs "haber bülteni" tarzı cümlelerde (doğrudan
"harika/kötü" gibi açık duygu kelimesi olmayan, dolaylı/çıkarımsal duygu
ifadeli) zorlandığını gösterdi (~%65, bkz. CLAUDE.md). winvoker veri seti
büyük ölçüde ürün/film yorumu tarzında olduğundan bu alt-türü yeterince
kapsamıyor.

Bu script, Gemini'ye tam olarak bu üslupta, dengeli (pozitif/negatif) ve
etiketli sentetik cümleler ürettirir. LLM burada CANLI sıralama kararı için
değil, offline bir veri üretim aracı olarak kullanılıyor -- bilgi damıtma
(knowledge distillation) yaklaşımı, mimariye/açıklanabilirlik ilkesine
dokunmuyor. Üretilen etiketler "gerçek" (insan) etiket kadar kesin değildir,
bu dürüstçe not edilmeli; ayrı bir bağımsız doğrulama ile sınanacak.
"""
import json
import os
import time
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ÇIKTI_DOSYASI = Path(__file__).resolve().parent / "zayif_uslup_veri.jsonl"
MODEL_ADI = "gemini-3.6-flash"
TUR_BASINA_ISTEK = 40  # her istekte kac cumle istenecek
HEDEF_TUR_BASINA_TOPLAM = 2000  # pozitif icin 2000, negatif icin 2000 -> 4000 toplam

SISTEM_TALIMATI = """Sen Türkçe doğal dil işleme için eğitim verisi üreten bir asistansın.
Görevin: KISA, RESMİ, ÜÇÜNCÜ ŞAHIS, "haber bülteni" tarzında Türkçe cümleler üretmek.

KESİN KURALLAR:
- Cümleler haber/gündem/spor/ekonomi/teknoloji/kültür gibi çeşitli konularda olsun.
- Duygu, DOLAYLI/ÇIKARIMSAL olarak anlaşılmalı -- "harika", "kötü", "berbat", "mükemmel"
  gibi AÇIK duygu kelimeleri KULLANMA. Duygu, olayın kendisinden ve sonucundan çıkarılmalı.
  Örnek pozitif (açık kelime yok): "Şirketin çeyreklik geliri beklentilerin üzerinde gerçekleşti, hisseler yükselişe geçti."
  Örnek negatif (açık kelime yok): "Fabrikada yaşanan üretim durması yüzlerce işçiyi etkiledi."
- Her cümle 1-2 cümle uzunluğunda, gerçek bir haber bülteni cümlesi gibi doğal olsun.
- Gerçek kişi/kurum ismi kullanma, uydurma/jenerik isimler kullan (örn. "yerel yönetim",
  "bir teknoloji şirketi", "ilçe belediyesi").
- Siyasi veya dini içerik ÜRETME -- nötr konular (spor, ekonomi, teknoloji, kültür, çevre,
  eğitim, sağlık, ulaşım) kullan.
- Çıktıyı SADECE geçerli bir JSON dizisi olarak ver, başka hiçbir metin ekleme:
  [{"text": "...", "label": "positive"}, {"text": "...", "label": "negative"}, ...]"""


def _istemci():
    from google import genai
    return genai.Client(api_key=os.environ["GEMINI_API_KEY"])


def _tur_uret(istemci, etiket: str, adet: int):
    from google.genai import types

    etiket_aciklama = "OLUMLU (dolaylı, açık kelime kullanmadan)" if etiket == "positive" else "OLUMSUZ (dolaylı, açık kelime kullanmadan)"
    istek = (
        f"{adet} adet {etiket_aciklama} sonuçlu, kısa/resmi/haber-bülteni tarzı "
        f"Türkçe cümle üret. Hepsinin \"label\" alanı \"{etiket}\" olsun. "
        f"Konularda çeşitlilik olsun, birbirinin tekrarı olmasın."
    )
    yanit = istemci.models.generate_content(
        model=MODEL_ADI,
        contents=istek,
        config=types.GenerateContentConfig(
            system_instruction=SISTEM_TALIMATI,
            max_output_tokens=8192,
            thinking_config=types.ThinkingConfig(thinking_level="low"),
        ),
    )
    metin = yanit.text.strip()
    if metin.startswith("```"):
        metin = metin.split("```")[1]
        if metin.startswith("json"):
            metin = metin[4:]
    try:
        veri = json.loads(metin)
    except json.JSONDecodeError:
        print(f"  [uyari] JSON parse hatasi, bu istek atlaniyor (ilk 200 karakter): {metin[:200]}")
        return []
    return [v for v in veri if v.get("text") and v.get("label") == etiket]


def main():
    if not os.environ.get("GEMINI_API_KEY"):
        print("HATA: GEMINI_API_KEY tanimli degil, veri uretilemiyor.")
        return

    istemci = _istemci()
    tum_ornekler = []

    for etiket in ["positive", "negative"]:
        toplanan = 0
        deneme = 0
        while toplanan < HEDEF_TUR_BASINA_TOPLAM and deneme < HEDEF_TUR_BASINA_TOPLAM // TUR_BASINA_ISTEK + 15:
            deneme += 1
            try:
                yeni = _tur_uret(istemci, etiket, TUR_BASINA_ISTEK)
            except Exception as e:
                print(f"  [hata] {etiket} istegi basarisiz: {e}, 5sn bekleyip tekrar denenecek")
                time.sleep(5)
                continue
            tum_ornekler.extend(yeni)
            toplanan += len(yeni)
            print(f"[{etiket}] {toplanan}/{HEDEF_TUR_BASINA_TOPLAM} (bu turda {len(yeni)} ornek geldi, deneme {deneme})")
            # kaydi her turda guncelle -- gece boyu calisirken bir yerde kesilirse veri kaybolmasin
            with open(ÇIKTI_DOSYASI, "w", encoding="utf-8") as f:
                for o in tum_ornekler:
                    f.write(json.dumps(o, ensure_ascii=False) + "\n")

    print(f"\nBitti. Toplam {len(tum_ornekler)} ornek {ÇIKTI_DOSYASI} dosyasina yazildi.")


if __name__ == "__main__":
    main()
