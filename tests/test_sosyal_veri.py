from sosyal_veri import SosyalDepo
from topluluk_veri import TOPLULUK_GONDERILERI


def test_topluluk_havuzu_profile_bazli_ve_benzersiz():
    assert len(TOPLULUK_GONDERILERI) == 80
    assert len({post["id"] for post in TOPLULUK_GONDERILERI}) == 80
    assert {post["yazar"] for post in TOPLULUK_GONDERILERI} == {
        "denizcetin", "eceyilmaz", "ardaatlas", "selinkaya", "mertdemir"
    }


def test_sosyal_depo_follow_reaction_comment_ve_hikaye_kalici(tmp_path):
    depo = SosyalDepo(tmp_path / "demo.sqlite3")
    depo.hazirla([{"id": 1, "konu": "bilim", "metin": "Kısa bir demo postu.", "yazar": "denizcetin"}])

    assert len(depo.gonderileri_yukle()) == 1
    assert depo.takip_degistir("emiryusuf", "denizcetin") is True
    assert depo.kullanici_ozeti("denizcetin")["following_by_viewer"] is True
    assert depo.roket_degistir("emiryusuf", 1) is True
    assert depo.post_ozellikleri(1)["roket_sayisi"] == 1
    depo.yorum_ekle("emiryusuf", 1, "Güzel bir fikir.")
    assert depo.post_ozellikleri(1)["yorum_sayisi"] == 1
    assert len(depo.yorumlar(1)) == 1
    assert len(depo.hikayeler()) >= 5
