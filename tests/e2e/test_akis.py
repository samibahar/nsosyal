"""Raporun 3.3 ve 6.2 bölümlerinde anlatılan kullanıcı akışlarının tarayıcıda doğrulanması."""
import json
import os

import pytest

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


def test_pwa_manifesti_gecerli_ve_bagli(masaustu):
    """'Neden mobil uygulama değil?' sorusu: site telefona uygulama gibi kurulabilir."""
    masaustu.goto(f"{ADRES}/index.html")
    manifest = masaustu.evaluate("async () => { const bag = document.querySelector('link[rel=manifest]'); return bag ? (await fetch(bag.href)).json() : null; }")
    assert manifest and manifest["display"] == "standalone" and manifest["start_url"] == "/index.html" and manifest["icons"]


def test_sunucu_davranis_verisi_kabul_etmez(masaustu):
    """Eski sunucu tarafı öğrenme uç noktaları varsayılan olarak kapalıdır."""
    masaustu.goto(f"{ADRES}/index.html")
    durumlar = masaustu.evaluate("""async () => Promise.all(
        ['/api/etkilesim', '/api/dogrulama', '/api/kisisel-mod?aktif=true'].map(yol =>
            fetch(yol, {method: 'POST', headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({gonderi_id: 1, dwell_saniye: 5, kullanici_cevabi: 'sakin'})}).then(y => y.status)))""")
    assert all(durum in (404, 405) for durum in durumlar), durumlar


def test_mobilde_hicbir_sayfa_yatay_tasmaz_ve_hata_vermez(mobil):
    for yol in SAYFALAR:
        mobil.goto(f"{ADRES}{yol}")
        mobil.wait_for_load_state("networkidle")
        assert mobil.evaluate("document.documentElement.scrollWidth <= innerWidth"), yol
    assert not mobil.hatalar


def test_mobilde_kesfet_etiketi_basliga_binmez_haber_dugmeleri_dokunulabilir(mobil):
    """Mobil incelemede bulunanlar: küçük Keşfet döşemelerinde konu etiketi başlığın
    üstüne biniyordu, görsel alt metni bozuk kodlanmıştı ("iÃ§eriÄŸi"), Haberler'deki
    "Neden bu?" düğmesi 12 px yüksekliğindeydi."""
    mobil.goto(f"{ADRES}/kesfet.html")
    mobil.wait_for_selector(".explore-card .explore-photo")
    kesfet = mobil.evaluate("""() => {
        const kes = (a, b) => Math.max(0, Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top)) * Math.max(0, Math.min(a.right, b.right) - Math.max(a.left, b.left));
        const kartlar = [...document.querySelectorAll('.explore-card')];
        return {cakisan: kartlar.filter(k => kes(k.querySelector('.explore-topic').getBoundingClientRect(), k.querySelector('.explore-card-text').getBoundingClientRect()) > 0).length,
                etiketler: kartlar.map(k => k.querySelector('.explore-topic').textContent),
                altlar: [...document.querySelectorAll('.explore-photo')].map(i => i.alt)};
    }""")
    assert kesfet["cakisan"] == 0
    assert "Gundem" not in kesfet["etiketler"] and "Gündem" in kesfet["etiketler"]
    assert all("içeriği için temsili görsel" in alt and "Ã" not in alt for alt in kesfet["altlar"])
    mobil.goto(f"{ADRES}/haberler.html")
    mobil.wait_for_selector(".news-card .news-why")
    boy = mobil.evaluate("() => [document.querySelector('.news-why'), document.getElementById('news-reset')].map(e => e.getBoundingClientRect().height)")
    assert min(boy) >= 32, boy
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


def test_spiral_kalibrasyonu_ancak_cevaplarla_kanitlaninca_akisa_baglanir(masaustu):
    """Sentetik eğitimli spiral modeli, kullanıcının 'sakinim' cevaplarıyla
    kalibre olur; ama akışı ancak 6 cevapta varsayılandan iyi tuttuğu
    görülünce etkiler. Jüri demosu kalibrasyondan etkilenmez."""
    akisi_ac(masaustu)
    once = juri_demosu(masaustu)["summary"]
    for i in range(6):
        ozet = masaustu.evaluate("async () => { await LocalPersonalization.recordCheckin('sakin'); return LocalPersonalization.spiralDogrulamaOzeti(); }")
        assert ozet["toplam"] == i + 1 and ozet["etkin"] is (i == 5)
    assert ozet["kisiselBrier"] < ozet["ayniVarsayilanBrier"] and ozet["kalibrasyon"]["egim"] >= 0.25
    sonra = masaustu.evaluate("() => LocalPersonalization.summary()")
    assert sonra["spiralKalibrasyonEtkin"] and sonra["intensity"] < once["intensity"] - 0.05
    assert juri_demosu(masaustu)["summary"]["intensity"] == pytest.approx(once["intensity"], abs=0.02)

    masaustu.goto(f"{ADRES}/rapor.html")
    masaustu.wait_for_function("document.getElementById('dogrulama-not').textContent.includes('dengelemeye bağlandı')")


def test_pilot_dosyasi_yalniz_cevap_ve_ozet_sayilari_icerir(masaustu):
    akisi_ac(masaustu)
    juri_demosu(masaustu)
    masaustu.evaluate("async () => { for (const c of ['sakin', 'anksiyete', 'umut']) await LocalPersonalization.recordCheckin(c); }")
    masaustu.goto(f"{ADRES}/ayarlar.html")
    masaustu.wait_for_function("document.getElementById('pilot-indir').textContent.includes('3 cevap')")
    with masaustu.expect_download() as bilgi:
        masaustu.locator("#pilot-indir").click()
    with open(bilgi.value.path(), encoding="utf-8") as f:
        metin = f.read()
    dosya = json.loads(metin)
    assert dosya["bicim"] == "nsosyal-pilot-1" and len(dosya["katilimci"]) == 12
    assert [k["cevap"] for k in dosya["kayitlar"]] == ["sakin", "anksiyete", "umut"]
    assert all(k["demo"] for k in dosya["kayitlar"])  # jüri demosundan sonra verildi, analizde atılır
    assert set(dosya["kayitlar"][0]["spiral"]["ozellik"]) == {"yogun_pay", "goreli_oyalanma", "yogun_fazla_kalma", "aktif_oran"}
    pencere = dosya["kayitlar"][0]["psikolojik"]["pencere"]
    assert len(pencere) >= 3 and abs(sum(p["agirlik"] for p in pencere) - 1) < 0.01
    for yasak in ["metin", "konu", "postId", "createdAt", "yazar", "topic"]:
        assert f'"{yasak}"' not in metin, yasak
    assert not masaustu.hatalar


def test_ruh_hali_tek_gonderiyle_degismez(masaustu):
    """Olası ruh hali son 30 dakikanın birleşik tahminidir: sakin bir oturumda
    tek bir 'sinirli' görünen etkileşim sonucu çevirmez; eski etkileşimler ve
    3'ten az kanıt sonuç üretmez."""
    akisi_ac(masaustu)
    sonuc = masaustu.evaluate("""() => {
        const T = TrainedModels, simdi = 100000;
        const sakin = i => ({zaman: simdi - 300 + i * 40, ozellik: {duygu: 0.05, dwell_saniye: 1.2, tiklama: 0, roket: 0, yorum: 0}});
        const olaylar = [0, 1, 2, 3, 4, 5].map(sakin);
        const sinirli = {zaman: simdi, ozellik: {duygu: -0.8, dwell_saniye: 2.5, tiklama: 1, roket: 1, yorum: 1}};
        return {tek: T.psikolojikTahmin(sinirli.ozellik).kategori, once: T.ruhHaliPenceresi(olaylar, simdi).kategori,
                sonra: T.ruhHaliPenceresi([...olaylar, sinirli], simdi).kategori,
                eski: T.ruhHaliPenceresi(olaylar, simdi + 3600), azKanit: T.ruhHaliPenceresi(olaylar.slice(0, 2), simdi)};
    }""")
    assert sonuc["tek"] == "sinirli" and sonuc["once"] == "sakin" and sonuc["sonra"] == "sakin"
    assert sonuc["eski"] is None and sonuc["azKanit"] is None


def test_ham_olaylar_12_hafta_saklanir(masaustu):
    akisi_ac(masaustu)
    gunler = masaustu.evaluate("""async () => {
        const GUN = 86400000, db = await new Promise((ok, hata) => { const r = indexedDB.open('nsosyal-local-agent'); r.onsuccess = () => ok(r.result); r.onerror = hata; });
        const olay = gun => ({type: 'interaction', createdAt: Date.now() - gun * GUN, postId: gun, topic: 'bilim', tone: 0.3, kelime: 10, dwell: 4, click: false, rocket: false, comment: false, exit: false, demo: false});
        await new Promise(ok => { const tx = db.transaction('events', 'readwrite'); tx.objectStore('events').add(olay(40)); tx.objectStore('events').add(olay(90)); tx.oncomplete = ok; });
        db.close();
        const p = await (await fetch('/api/demo-paketi')).json();
        await LocalPersonalization.recordInteraction({post: p.gonderiler[0], dwell: 3});
        return (await LocalPersonalization.getLocalEvents()).map(o => Math.round((Date.now() - o.createdAt) / GUN));
    }""")
    assert 40 in gunler and 90 not in gunler


def test_uzman_ozeti_haftalik_seyir_kendi_bildirimleri_ve_tepki_dengesi(masaustu):
    akisi_ac(masaustu)
    juri_demosu(masaustu)
    masaustu.evaluate("""async () => {
        const p = await (await fetch('/api/demo-paketi')).json();
        await LocalPersonalization.recordCheckin('sakin'); await LocalPersonalization.recordCheckin('anksiyete');
        await LocalPersonalization.recordPostReaction(p.gonderiler[0], 'gerildim');
        await LocalPersonalization.recordPostReaction(p.gonderiler[1], 'begendim');
    }""")
    masaustu.goto(f"{ADRES}/rapor.html")
    masaustu.locator("#terapist-ozet-buton").click()
    masaustu.wait_for_function("document.getElementById('terapist-ozet-metin').textContent.includes('HAFTALIK SEYİR')")
    metin = masaustu.locator("#terapist-ozet-metin").inner_text()
    for parca in ["KİŞİNİN KENDİ BİLDİRİMLERİ", "Sakin 1", "Yoğun 1", "Son 2 bildirim", "Kendi bildirimleri:",
                  "Olası ritim (süreye göre): sakin", "GÖNÜLLÜ TEPKİLER", "100 etkileşim başına", "yoğun tonlu içeriğe"]:
        assert parca in metin, parca
    assert "(2 cevap; rastgele tahmin %20)" in metin  # eşleşme, özetteki cevaplarla aynı kaynaktan
    assert "Yoğun tonlu içeriğe verilen olumsuz tepki" in masaustu.locator("#reaction-chart").inner_text()
    assert not masaustu.hatalar
