"""Küçük ekranlarda açıklamalar ve menüler taşmaz, temel hedefler dokunulabilir."""
import os
from pathlib import Path

import pytest

ADRES = os.environ.get('NSOSYAL_URL', 'http://localhost:8000')


@pytest.mark.parametrize('width', [360, 390, 1280])
@pytest.mark.parametrize('page', ['ayarlar', 'haberler', 'rapor'])
def test_duzen_ve_dokunma(masaustu, width, page):
    masaustu.set_viewport_size({'width': width, 'height': 844})
    masaustu.goto(f'{ADRES}/{page}.html')
    masaustu.wait_for_load_state('networkidle')
    assert masaustu.evaluate('document.documentElement.scrollWidth <= innerWidth')
    if page == 'haberler':
        targets = masaustu.locator('.news-why, #news-reset, .news-reaction-trigger')
        assert all(v >= 44 for v in targets.evaluate_all('(es) => es.map(e => e.getBoundingClientRect().height)'))
    if page == 'ayarlar':
        assert masaustu.locator('.ayar-ayrinti').count() == 2
        assert masaustu.locator('#kisisel-durum').inner_text() == 'Henüz kontrol sorusu yanıtlanmadı.'
    assert not masaustu.hatalar
    if width in (390, 1280):
        target = Path('_yerel/ui_kontrol')
        target.mkdir(parents=True, exist_ok=True)
        masaustu.screenshot(path=str(target / f'{page}-{width}.png'), full_page=True)
