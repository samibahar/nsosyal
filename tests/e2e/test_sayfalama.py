"""Sunucu sayfalaması tarayıcı oturumuna göre tutulur: bir kişinin akışı sıfırlaması
başka birinin sayfalamasını bozmaz (çok kişili pilot)."""
import os

ADRES = os.environ.get("NSOSYAL_URL", "http://localhost:8000")


def test_iki_oturumun_sayfalamasi_birbirini_etkilemez(masaustu):
    masaustu.goto(f"{ADRES}/index.html")
    sonuc = masaustu.evaluate("""async () => {
        const al = async (oturum, sifirdan) => (await (await fetch(`/api/gonderiler?aday=12&sifirdan=${sifirdan}&oturum=${oturum}`)).json()).gonderiler.map(g => g.id);
        const a1 = await al('pilot-a', true);
        await al('pilot-b', true);            // başka biri akışını sıfırlıyor
        const a2 = await al('pilot-a', false);
        const b2 = await al('pilot-b', false);
        return {a1, a2, b2};
    }""")
    assert len(sonuc["a1"]) == len(sonuc["a2"]) == 12
    assert not set(sonuc["a1"]) & set(sonuc["a2"])  # A'nın ikinci sayfası birincinin tekrarı değil
    assert len(sonuc["b2"]) == 12
