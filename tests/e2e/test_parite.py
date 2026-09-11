"""Tarayıcıdaki sıralama (local-agent.js siralaSaf) ile etki_analizi.py'deki
Python referansının AYNI sıralamayı ürettiğinin kanıtı. Etki analizindeki
sayılar ancak bu eşitlik varsa uygulamayı temsil eder."""
import os
import random

from etki_analizi import dozlu_sirala

ADRES = os.environ.get("NSOSYAL_URL", "http://localhost:8000")
KONULAR = ["spor", "gundem", "teknoloji", "bilim", "saglik", "ekonomi", "sanat", "egitim", "oyun", "seyahat"]


def test_js_siralamasi_python_referansiyla_ayni(masaustu):
    masaustu.goto(f"{ADRES}/index.html")
    masaustu.wait_for_function("typeof window.LocalPersonalization?.siralaSaf === 'function'")
    rng = random.Random(5)
    for deneme in range(6):
        adaylar = [{"id": i, "konu": rng.choice(KONULAR), "duygu": round(rng.uniform(-1, 1), 3),
                    "ilgi_skoru": round(rng.uniform(0.4, 0.75), 3), "resmi": rng.random() < 0.06} for i in range(48)]
        agirliklar = {konu: round(rng.random(), 3) for konu in KONULAR}
        for yogunluk in (0.2, 0.5, 0.9):
            python = [k["g"]["id"] for k in dozlu_sirala(adaylar, agirliklar, yogunluk)]
            js = masaustu.evaluate(
                "([a, w, y]) => LocalPersonalization.siralaSaf(a, {topicWeights: w, intensity: y, enoughData: true, dengelemeAcik: true}).map(p => p.id)",
                [adaylar, agirliklar, yogunluk])
            assert js == python, (deneme, yogunluk)
