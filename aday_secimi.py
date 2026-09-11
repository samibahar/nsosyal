"""Sunucunun aday gönderi seçimi (backend/main.py ve etki_analizi.py ortak kullanır)."""
import random


def dogal_cesitlilik_ekle(siralanmis: list[dict], genlik: float = 0.08, rng=random) -> list[dict]:
    """Aynı ilgi skoruna sahip gönderiler (örn. hepsi 'spor') her sayfa
    yüklemesinde birebir aynı sırada gelmesin diye final_skor'a küçük bir
    rastgele gürültü ekleyip yeniden sıralar. motor.py'nin kendisi kasıtlı
    olarak deterministik bırakıldı (spike_poc.py'deki örnek çıktı tekrar
    üretilebilir kalsın diye) -- gürültü sadece burada, sunum katmanında."""
    gurultulu = [(g, g["final_skor"] + rng.uniform(-genlik, genlik)) for g in siralanmis]
    gurultulu.sort(key=lambda cift: -cift[1])
    return [g for g, _ in gurultulu]


def sayfa_sec(siralanmis: list[dict], gosterilmis: set, sayfa_boyu: int, konu_basina_ust_sinir: int = 3,
              konu_basina_taban: int = 0) -> list[dict]:
    """Skor sırasından sayfa_boyu kadar gönderi seçer, ama aynı konudan
    art arda konu_basina_ust_sinir'den fazlasını ALMAZ -- salt ilgi-skoru
    farkına (ve rastgele gürültüye) güvenmek, en yüksek 1-2 ilgi alanının
    tüm sayfayı kaplamasına yol açıyordu (kullanıcı tarafından tespit
    edildi, 21.08.2026). Bu, ilgiye göre öne çıkarmayı korurken görünür
    çeşitliliği garanti eder.

    konu_basina_taban > 0 ise önce her konudan o kadar gönderi ayrılır
    (keşif payı), kalan yer skora göre doldurulur. Sunucunun ilgi profili
    sabit olduğu için bu pay olmadan düşük skorlu konular aday listesine hiç
    girmiyor, telefon kullanıcının gerçekten sevdiği bir konuyu öne alamıyordu."""
    kalanlar = [g for g in siralanmis if g["id"] not in gosterilmis]
    sayfa, konu_sayaci, ertelenmis = [], {}, []
    if konu_basina_taban:
        for g in kalanlar:
            if len(sayfa) >= sayfa_boyu:
                break
            if konu_sayaci.get(g["konu"], 0) < konu_basina_taban:
                sayfa.append(g)
                konu_sayaci[g["konu"]] = konu_sayaci.get(g["konu"], 0) + 1
        secilen = {g["id"] for g in sayfa}
        kalanlar = [g for g in kalanlar if g["id"] not in secilen]
    for g in kalanlar:
        if len(sayfa) >= sayfa_boyu:
            break
        konu = g["konu"]
        if konu_sayaci.get(konu, 0) >= konu_basina_ust_sinir:
            ertelenmis.append(g)
            continue
        sayfa.append(g)
        konu_sayaci[konu] = konu_sayaci.get(konu, 0) + 1
    if len(sayfa) < sayfa_boyu:
        sayfa.extend(ertelenmis[: sayfa_boyu - len(sayfa)])
    return sayfa


def aday_listesi(siralanmis: list[dict], gosterilmis: set, aday: int, sayfa_boyu: int = 12) -> list[dict]:
    """12'lik klasik sayfa eskisi gibi kalır. Geniş aday listesinde her konudan
    en az 2 gönderi keşif payı olarak ayrılır, bir konu en fazla aday/6 yer alır."""
    genis = aday > sayfa_boyu
    return sayfa_sec(siralanmis, gosterilmis, aday,
                     konu_basina_ust_sinir=max(3, aday // 6) if genis else 3,
                     konu_basina_taban=2 if genis else 0)
