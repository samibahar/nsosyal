from demo_paketi import DEMO_POSTS, DEMO_SCENARIO


def test_juri_demo_paketi_sabit_ve_yeterli_aday_sunar():
    assert len(DEMO_POSTS) == 12
    assert len({post["id"] for post in DEMO_POSTS}) == len(DEMO_POSTS)
    assert {post["yazar"] for post in DEMO_POSTS} >= {"denizcetin", "mertdemir", "selinkaya"}


def test_juri_senaryosu_yogun_adaylara_ve_gecerli_tepkilere_baglidir():
    posts = {post["id"]: post for post in DEMO_POSTS}
    assert len(DEMO_SCENARIO) == 10
    assert all(signal["post_id"] in posts for signal in DEMO_SCENARIO)
    assert sum(1 for signal in DEMO_SCENARIO if posts[signal["post_id"]]["duygu"] < -0.15) == len(DEMO_SCENARIO)
    assert DEMO_SCENARIO[-1]["reaction"] == "gerildim"
