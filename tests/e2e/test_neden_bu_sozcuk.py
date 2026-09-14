"""Ton açık bir olay sözcüğüyle aşağı çekildiyse (yogun_sozluk.py) "Neden bu?" bunu
söyler: hangi sözcük ve modelin kendi tonu. Normal akış yerel sıralamayla çalışır."""
import os

ADRES = os.environ.get("NSOSYAL_URL", "http://localhost:8000")


def test_neden_bu_olay_sozcugunu_ve_model_tonunu_gosterir(masaustu):
    def sozcuklu(route):
        yanit = route.fetch()
        veri = yanit.json()
        for gonderi in veri["gonderiler"]:
            gonderi.update(duygu=-0.9, duygu_model=0.41, yogun_sozcuk="öldü")
        route.fulfill(response=yanit, json=veri)

    masaustu.route("**/api/gonderiler*", sozcuklu)
    masaustu.goto(f"{ADRES}/index.html")
    masaustu.wait_for_selector("#akis .post-card")
    if masaustu.locator("#onay-acik").count():
        masaustu.locator("#onay-acik").click()
        masaustu.wait_for_selector(".onay-arka", state="detached")
    masaustu.locator("#akis .post-card .why-button").first.click()
    teknik = masaustu.locator("#technical-details-content").text_content()
    assert "açık olay sözcüğü «öldü»" in teknik and "modelin kendi tonu 0.41" in teknik
    assert not masaustu.hatalar
