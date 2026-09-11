"""Erişilebilirlik: axe-core ile WCAG 2.1 AA denetimi ve kapalı diyalogların
klavye odağından çıkarılması (static/erisim.js).

axe-core cdnjs'ten yüklenir; ağ yoksa denetim testi atlanır."""
import os

import pytest

ADRES = os.environ.get("NSOSYAL_URL", "http://localhost:8000")
AXE = "https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.9.1/axe.min.js"
SAYFALAR = ["/index.html", "/haberler.html", "/rapor.html", "/ayarlar.html", "/kesfet.html", "/profil.html?u=emiryusuf", "/juri.html"]


@pytest.mark.parametrize("yol", SAYFALAR)
def test_sayfada_wcag_aa_ihlali_yok(masaustu, yol):
    masaustu.goto(f"{ADRES}{yol}")
    masaustu.wait_for_load_state("networkidle")
    try:
        masaustu.add_script_tag(url=AXE)
    except Exception:
        pytest.skip("axe-core indirilemedi (ağ yok)")
    ihlaller = masaustu.evaluate(
        "async () => (await axe.run(document, {runOnly: {type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21aa']}}))"
        ".violations.map(v => `${v.id}: ${v.nodes.map(n => n.target.join(' ')).slice(0, 3).join(' | ')}`)")
    assert ihlaller == []


def test_kapali_diyalog_odaklanamaz_acilinca_kullanilabilir(masaustu):
    masaustu.goto(f"{ADRES}/index.html")
    masaustu.wait_for_selector("#akis .post-card")
    if masaustu.locator("#onay-acik").count():
        masaustu.locator("#onay-acik").click()
    sayfa = "document.getElementById('explanation-sheet')"
    assert masaustu.evaluate(f"{sayfa}.inert") is True
    masaustu.locator("#akis .why-button").first.click()
    masaustu.wait_for_function(f"{sayfa}.inert === false")
    masaustu.locator("#sheet-close").click()
    masaustu.wait_for_function(f"{sayfa}.inert === true")
