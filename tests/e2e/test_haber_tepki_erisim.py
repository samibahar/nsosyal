"""Kapalı tepki seçenekleri odak almaz; Escape ve dış tıklama durumu eşitler."""
import os

ADRES = os.environ.get('NSOSYAL_URL', 'http://localhost:8000')


def test_haber_tepki_menusu_odagi_ve_kapanmasi(mobil):
    mobil.goto(f'{ADRES}/haberler.html')
    trigger = mobil.locator('.news-reaction-trigger').first
    wheel = mobil.locator('.news-reaction-wheel').first
    trigger.wait_for()
    assert wheel.evaluate('(e) => e.inert')
    assert mobil.get_by_role('button', name='Beğendim', exact=True).count() == 0
    trigger.click()
    assert trigger.get_attribute('aria-expanded') == 'true'
    assert not wheel.evaluate('(e) => e.inert')
    wheel.locator('button').first.focus()
    mobil.keyboard.press('Escape')
    assert trigger.evaluate('(e) => e === document.activeElement')
    assert wheel.evaluate('(e) => e.inert')
    assert trigger.get_attribute('aria-expanded') == 'false'
    trigger.click()
    mobil.locator('h1').click()
    assert trigger.get_attribute('aria-expanded') == 'false'
    assert wheel.evaluate('(e) => e.inert')
    assert not mobil.hatalar


def test_haber_aciklama_odagi_pencerede_kalir(mobil):
    mobil.goto(f'{ADRES}/haberler.html')
    why = mobil.locator('.news-why').first
    why.click()
    assert mobil.locator('#news-sheet-close').evaluate('(e) => e === document.activeElement')
    mobil.keyboard.press('Shift+Tab')
    assert mobil.locator('#news-sheet summary').evaluate('(e) => e === document.activeElement')
    mobil.keyboard.press('Tab')
    assert mobil.locator('#news-sheet-close').evaluate('(e) => e === document.activeElement')
    mobil.keyboard.press('Escape')
    assert why.evaluate('(e) => e === document.activeElement')
