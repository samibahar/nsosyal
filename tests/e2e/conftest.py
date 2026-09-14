"""Uçtan uca (tarayıcı) testleri: Playwright + Chromium.

Çalışan bir sunucuya bağlanır; sunucu yoksa testler atlanır:
    python -m uvicorn backend.main:app --port 8000
    python -m pytest tests/e2e -q
Başka adres için NSOSYAL_URL ortam değişkeni kullanılabilir. Her test yeni
bir tarayıcı bağlamında çalışır, yani yerel (IndexedDB) veri boş başlar.
"""
import os
import urllib.request

import pytest

sync_api = pytest.importorskip("playwright.sync_api")

ADRES = os.environ.get("NSOSYAL_URL", "http://localhost:8000")


def _ayakta() -> bool:
    try:
        urllib.request.urlopen(f"{ADRES}/index.html", timeout=3)
        return True
    except Exception:
        return False


@pytest.fixture(scope="session")
def tarayici():
    if not _ayakta():
        pytest.skip(f"Sunucu çalışmıyor ({ADRES}); önce: python -m uvicorn backend.main:app --port 8000")
    with sync_api.sync_playwright() as p:
        kanal = os.environ.get("NSOSYAL_BROWSER_CHANNEL")
        tarayici = p.chromium.launch(**({"channel": kanal} if kanal else {}))
        yield tarayici
        tarayici.close()


def _sayfa(tarayici, **ayar):
    baglam = tarayici.new_context(**ayar)
    sayfa = baglam.new_page()
    sayfa.hatalar = []
    sayfa.on("pageerror", lambda hata: sayfa.hatalar.append(str(hata)))
    sayfa.on("console", lambda mesaj: mesaj.type == "error" and sayfa.hatalar.append(mesaj.text))
    return baglam, sayfa


@pytest.fixture
def mobil(tarayici):
    baglam, sayfa = _sayfa(tarayici, viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
    yield sayfa
    baglam.close()


@pytest.fixture
def depolamasiz(tarayici):
    """IndexedDB'nin engellendiği tarayıcı (bazı gizli modlar, site verisi engeli)."""
    baglam, sayfa = _sayfa(tarayici, viewport={"width": 390, "height": 844})
    baglam.add_init_script("Object.defineProperty(window, 'indexedDB', { get() { throw new Error('site verisi engelli'); } });")
    yield sayfa
    baglam.close()


@pytest.fixture
def masaustu(tarayici):
    baglam, sayfa = _sayfa(tarayici, viewport={"width": 1280, "height": 860})
    yield sayfa
    baglam.close()
