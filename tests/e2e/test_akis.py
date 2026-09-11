"""Raporun 3.3 ve 6.2 bölümlerinde anlatılan kullanıcı akışlarının tarayıcıda doğrulanması."""
import os

ADRES = os.environ.get("NSOSYAL_URL", "http://localhost:8000")
SAYFALAR = ["/index.html", "/rapor.html", "/ayarlar.html", "/haberler.html", "/kesfet.html", "/profil.html?u=emiryusuf", "/juri.html"]


def akisi_ac(sayfa, onay="acik"):
    sayfa.goto(f"{ADRES}/index.html")
    sayfa.wait_for_selector("#akis .post-card")
    sayfa.wait_for_load_state("networkidle")
    secenek = sayfa.locator(f"#onay-{onay}")
    if secenek.count():
        secenek.click()
        sayfa.wait_for_selector(".onay-arka", state="detached")


def test_ilk_acilista_acik_riza_sorulur_kapali_secince_katman_kapanir(mobil):
    mobil.goto(f"{ADRES}/index.html")
    mobil.wait_for_selector(".onay-kutu")
    assert mobil.locator("#onay-acik").is_visible() and mobil.locator("#onay-kapali").is_visible()
    for _ in range(5):  # aria-modal: Tab odağı kutunun içinde döner
        mobil.keyboard.press("Tab")
        assert mobil.evaluate("!!document.activeElement.closest('.onay-kutu')")
    mobil.locator("#onay-kapali").click()
    mobil.wait_for_selector(".onay-arka", state="detached")
    ayarlar = mobil.evaluate("() => LocalPersonalization.getAyarlar()")
    assert not any(ayarlar.values())
    mobil.reload()
    mobil.wait_for_selector("#akis .post-card")
    assert mobil.locator(".onay-kutu").count() == 0


def juri_demosu(sayfa) -> dict:
    sayfa.evaluate("async () => { const p = await (await fetch('/api/demo-paketi')).json(); await LocalPersonalization.runDemoScenario(p); }")
    return sayfa.evaluate("() => LocalPersonalization.getDecisionTrace()")


def test_ana_akis_48_aday_ister_yalniz_gosterilenlerin_fotografini_indirir(mobil):
    istekler = []
    mobil.on("request", lambda istek: istekler.append(istek.url))
    akisi_ac(mobil)
    assert mobil.locator("#akis .post-card").count() == 12
    assert sum("aday=48" in url for url in istekler) == 1
    assert len([url for url in istekler if "/assets/explore/" in url]) <= 12
    assert not mobil.hatalar


def test_yerel_depolama_engelliyse_akis_acilir_davranis_verisi_gonderilmez(depolamasiz):
    istekler = []
    depolamasiz.on("request", lambda istek: istekler.append(istek.url))
    depolamasiz.goto(f"{ADRES}/index.html")
    depolamasiz.wait_for_selector("#akis .post-card")
    assert depolamasiz.locator("#akis .post-card").count() == 12
    assert depolamasiz.locator(".onay-kutu").count() == 0
    assert depolamasiz.locator("#flow-status-title").inner_text() == "Kişiselleştirme kapalı"
    depolamasiz.locator("#akis .post-card .post-text").first.click()
    depolamasiz.mouse.wheel(0, 2500)
    depolamasiz.wait_for_timeout(800)
    assert not [url for url in istekler if "/api/etkilesim" in url or "/api/dogrulama" in url]
    assert not depolamasiz.hatalar


def test_dengeleme_bildirimi_oturum_icin_kapatilabilir(masaustu):
    akisi_ac(masaustu)
    masaustu.locator("#jury-demo-rail").click()
    masaustu.wait_for_selector("#balance-intervention:not([hidden])")
    masaustu.locator("#denge-kapat").click()
    masaustu.wait_for_function("document.getElementById('flow-status-title').textContent === 'Bu oturumda dengeleme kapalı'")
    iz = juri_demosu(masaustu)
    assert iz["dengelemeAcik"] is False
    assert max(g["balancing"] for g in iz["after"]) == 0
    assert masaustu.evaluate("() => LocalPersonalization.getAyarlar()")["dengeleme"] is True  # kalıcı ayar değişmedi


def test_mobilde_hicbir_sayfa_yatay_tasmaz_ve_hata_vermez(mobil):
    for yol in SAYFALAR:
        mobil.goto(f"{ADRES}{yol}")
        mobil.wait_for_load_state("networkidle")
        assert mobil.evaluate("document.documentElement.scrollWidth <= innerWidth"), yol
    assert not mobil.hatalar


def test_tepki_secimi_cihazda_kaydedilir(mobil):
    akisi_ac(mobil)
    tetik = mobil.locator(".post-reaction-trigger").first
    tetik.click()
    mobil.locator('[data-post-reaction="begendim"]').click()
    assert "Beğendim" in tetik.inner_text()
    olaylar = mobil.evaluate("async () => (await LocalPersonalization.getLocalEvents()).filter(e => e.type === 'post_reaction').length")
    assert olaylar == 1


def test_juri_demosu_dengeler_ayarlardan_kapatinca_dengelemez(masaustu):
    akisi_ac(masaustu)
    iz = juri_demosu(masaustu)
    assert iz["movedCount"] > 0 and max(g["balancing"] for g in iz["after"]) > 0

    masaustu.goto(f"{ADRES}/ayarlar.html")
    anahtar = masaustu.locator('[data-ayar="dengeleme"]')
    masaustu.wait_for_function("document.querySelector('[data-ayar=dengeleme]').getAttribute('aria-checked') === 'true'")
    anahtar.click()
    masaustu.wait_for_function("document.getElementById('ayar-bildirim').textContent.length > 0")
    masaustu.reload()
    masaustu.wait_for_function("document.querySelector('[data-ayar=dengeleme]').getAttribute('aria-checked') === 'false'")

    akisi_ac(masaustu)
    iz = juri_demosu(masaustu)
    assert iz["dengelemeAcik"] is False
    assert max(g["balancing"] for g in iz["after"]) == 0
    assert masaustu.locator("#flow-status-title").inner_text() in {"Dengeleme kapalı", "Bu cihazda öğreniyor"}
    assert not masaustu.hatalar


def test_resmi_bilgi_yogun_akista_da_dengelenmez(masaustu):
    akisi_ac(masaustu)
    juri_demosu(masaustu)
    sonuc = masaustu.evaluate("""async () => {
        const p = await (await fetch('/api/demo-paketi')).json();
        const resmi = {...p.gonderiler[0], id: 99001, resmi: true};
        const sirali = await LocalPersonalization.rank([...p.gonderiler, resmi]);
        return {resmi: sirali.find(g => g.id === 99001).local_dengeleme,
                enFazla: Math.max(...sirali.filter(g => g.id !== 99001).map(g => g.local_dengeleme))};
    }""")
    # local_dengeleme = dengeleme yüzünden kaç sıra aşağı kaydırıldığı
    assert sonuc["enFazla"] > 0 and sonuc["resmi"] == 0


def test_kontrol_sorusu_cevabi_kisisel_modeli_gunceller(masaustu):
    akisi_ac(masaustu)
    juri_demosu(masaustu)
    masaustu.evaluate("async () => { await LocalPersonalization.recordCheckin('anksiyete'); await LocalPersonalization.recordCheckin('sakin'); }")
    ozet = masaustu.evaluate("() => LocalPersonalization.dogrulamaOzeti()")
    durum = masaustu.evaluate("() => LocalPersonalization.kisiselModelDurumu()")
    assert ozet["toplam"] == 2 and ozet["rastgeleOrani"] == 0.2
    assert durum["guncelleme"] == 2
    masaustu.goto(f"{ADRES}/rapor.html")
    masaustu.wait_for_function("document.getElementById('dogrulama-chart').innerText.includes('tabanı')")
