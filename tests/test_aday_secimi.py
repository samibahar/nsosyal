from collections import Counter

from aday_secimi import aday_listesi

KONULAR = ["spor", "gundem", "teknoloji", "bilim", "saglik", "ekonomi", "sanat", "egitim", "oyun", "seyahat"]


def havuz():
    # Konu başına 25 gönderi; ilk konular sunucunun sabit profilinde daha yüksek skorlu.
    return [{"id": k * 100 + i, "konu": konu, "final_skor": 1 - k * 0.05 - i * 0.001}
            for k, konu in enumerate(KONULAR) for i in range(25)]


def sirali():
    return sorted(havuz(), key=lambda g: -g["final_skor"])


def test_genis_aday_listesi_her_konuya_kesif_payi_ayirir():
    sayim = Counter(g["konu"] for g in aday_listesi(sirali(), set(), 48))
    assert sum(sayim.values()) == 48
    assert set(sayim) == set(KONULAR)
    assert min(sayim.values()) >= 2 and max(sayim.values()) <= 8


def test_klasik_sayfa_degismedi():
    sayfa = aday_listesi(sirali(), set(), 12)
    sayim = Counter(g["konu"] for g in sayfa)
    assert len(sayfa) == 12 and max(sayim.values()) <= 3
    assert set(sayim) == {"spor", "gundem", "teknoloji", "bilim"}


def test_gosterilenler_tekrar_aday_olmaz():
    ilk = aday_listesi(sirali(), set(), 48)
    ikinci = aday_listesi(sirali(), {g["id"] for g in ilk}, 48)
    assert not {g["id"] for g in ilk} & {g["id"] for g in ikinci}
