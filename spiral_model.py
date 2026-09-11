"""
Spiral sınıflandırıcı (v2, 11.09.2026).

Gerçek kullanıcı davranış verisi yok (platform API erişimi vermiyor), bu yüzden
model SENTETİK veriyle eğitiliyor. Bu, "önerilen yöntemin kanıtı"dır; gerçek
kullanıcı onaylarıyla (kontrol soruları) yeniden eğitilmesi gerekir.

v1'DE ÖLÇÜLEN SORUNLAR (11.09.2026, python spiral_model.py çıktısında da var):
  1) Ölçek uyuşmazlığı: sentetik eğitimde "negatif_dwell_toplam" ortalaması
     16 sn; gerçek 20 gönderilik pencerede 50-100 sn. Olağan bir akışta birkaç
     olumsuz gönderiye bakmak 0,8'in üstünde spiral çıkıyordu; olumsuz
     haberlere 2'şer saniye göz atmak 0,98.
  2) "negatif_tekrar_sayisi" üretimde hep 0'dı (eğitimde ortalama 1,5).
  3) Döngüsellik: etiketler modelin kendi özelliklerinin lojistik bir
     formülüydü; model üreticiyi geri öğreniyordu.
  4) Zaman yoktu: dünkü oturum bugünkü riski etkiliyor, boş günlük bile 0,09
     veriyordu.
  5) Uzun metni okumak ile olumsuz içerikte oyalanmak ayırt edilemiyordu.

v2 YAKLAŞIMI:
  - Özellikler spiral_ozellik.py'de: 30 dk oturum penceresi, 10 dk yarı ömür,
    okuma süresine göre normalize edilmiş durma, yoğun içerikte diğerlerine
    göre oyalanma, aktif/pasif katılım ayrımı. Sunucu, tarayıcı ve eğitim aynı
    fonksiyonu kullanır.
  - Katsayı yönleri hipotezle karşılaştırılır (tests/test_spiral_model.py).
    İlk denemede "ortalama_ton" ters yönde çıkıp olumlu içerik okuyanı riskli
    saydığı için özellik setinden çıkarıldı.
  - Eğitim verisi DAVRANIŞ düzeyinde simülasyon: her oturum tek tek gönderi
    görüntülemelerinden oluşur, özellikler üretimdeki fonksiyonla bu
    olaylardan hesaplanır. Etiket simülasyondaki gizli durumdur (spiral /
    değil), özelliklerin bir formülü değildir.
  - Zor örnekler bilerek eklendi: uzun metin okuyan, olumsuz haberleri aktif
    tartışan, hızlı göz atan ve saatler önce yoğun bir oturum geçirmiş
    kullanıcılar spiral DEĞİLDİR.
  - Model standartlaştırılmış özelliklerle lojistik regresyon: her katsayı
    okunabilir, karar açıklanabilir kalır.

DAYANAK (yön, parametre değil): olumsuz içerikte pasif oyalanmanın olumsuz
duygulanımla, aktif katılımın daha iyi iyi-oluşla ilişkili olduğu hipotezi
(Verduyn vd., 2017 derlemesi). Sonraki çalışmalar bu etkinin kişiden kişiye
değiştiğini gösteriyor; buradaki parametreler varsayımdır.
"""
import numpy as np
from scipy.optimize import minimize
from scipy.special import expit
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, brier_score_loss, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

import spiral_ozellik as so

RASTGELE_TOHUM = 42
KONULAR = ["spor", "gundem", "teknoloji", "bilim", "saglik", "ekonomi", "sanat", "egitim", "oyun", "seyahat"]
OZELLIK_ADLARI = so.OZELLIK_ADLARI

# tür: (etiket, olasılık)
TURLER = {
    "olagan": (0, 0.30),
    "spiral": (1, 0.25),
    "uzun_okuyan": (0, 0.12),
    "aktif_tartisan": (0, 0.12),
    "hizli_gozatan": (0, 0.08),
    "spirale_gecis": (1, 0.08),
    "eski_oturum": (0, 0.05),
}
ETIKET_GURULTUSU = 0.08


# ---------------------------------------------------------------------------
# 1) Davranış simülatörü
# ---------------------------------------------------------------------------
def _ton(rng, olumsuz_pay: float) -> float:
    r = rng.random()
    if r < olumsuz_pay:
        return -rng.uniform(0.6, 1.0) if rng.random() < 0.75 else -rng.uniform(0.2, 0.6)
    if r < olumsuz_pay + 0.40:
        return rng.uniform(-0.15, 0.3)
    return rng.uniform(0.3, 1.0)


def _davranis(faz: str, yogun: bool, rng) -> tuple[float, bool]:
    """(durma / okuma süresi oranı, aktif katılım var mı)."""
    if faz == "spiral":
        return (rng.lognormal(np.log(2.1), 0.5), rng.random() < 0.03) if yogun else (rng.lognormal(np.log(0.55), 0.45), rng.random() < 0.05)
    if faz == "uzun_okuyan":
        return rng.lognormal(np.log(1.9), 0.4), rng.random() < 0.12
    if faz == "aktif_tartisan":
        return (rng.lognormal(np.log(1.7), 0.45), rng.random() < 0.5) if yogun else (rng.lognormal(np.log(0.8), 0.45), rng.random() < 0.2)
    if faz == "hizli_gozatan":
        return rng.lognormal(np.log(0.35), 0.4), rng.random() < 0.03
    return rng.lognormal(np.log(0.8), 0.45), rng.random() < 0.12  # olağan


def _oturum_olaylari(tur: str, rng, baslangic: float = 0.0, kimlik_ofset: int = 0) -> tuple[list[dict], float]:
    n = int(rng.integers(10, 26))
    # çok olumlu akış / sakin gün / olağan gün / kriz günü / ağır kriz: akıştaki
    # yoğun içerik payı. Uç akışlar da bulunsun ki model onlarda uydurmasın.
    olumsuz_pay = float(rng.choice([0.05, 0.15, 0.25, 0.45, 0.65, 0.9], p=[0.14, 0.24, 0.29, 0.19, 0.09, 0.05]))
    odak = list(rng.choice(KONULAR, 2, replace=False))
    t, olaylar = baslangic, []
    for i in range(n):
        faz = tur
        if tur == "spirale_gecis":
            faz = "olagan" if i < n // 2 else "spiral"
        ton = _ton(rng, olumsuz_pay)
        yogun = ton < so.YOGUN_TON
        kelime = int(rng.integers(6, 29))
        konu = str(rng.choice(odak)) if (faz == "spiral" and yogun and rng.random() < 0.7) else str(rng.choice(KONULAR))
        oran, aktif = _davranis(faz, yogun, rng)
        dwell = max(0.3, oran * so.beklenen_okuma(kelime))
        t += dwell + rng.uniform(0.4, 2.0)
        roket = aktif and rng.random() < 0.7
        olaylar.append({
            "gonderi": kimlik_ofset + i, "zaman": t, "dwell": dwell, "ton": ton, "kelime": kelime, "konu": konu,
            "roket": roket, "yorum": aktif and not roket, "tiklama": aktif or rng.random() < 0.15,
        })
    return olaylar, t


def oturum_uret(tur: str, rng) -> tuple[list[dict], float]:
    if tur == "eski_oturum":
        eski, _ = _oturum_olaylari("spiral", rng, baslangic=0.0, kimlik_ofset=1000)
        simdiki_baslangic = eski[-1]["zaman"] + rng.uniform(2, 6) * 3600
        yeni, son = _oturum_olaylari("olagan", rng, baslangic=simdiki_baslangic)
        return eski + yeni, son + rng.uniform(0, 60)
    olaylar, son = _oturum_olaylari(tur, rng)
    return olaylar, son + rng.uniform(0, 60)


def veri_seti_olustur(n: int = 4000, tohum: int = RASTGELE_TOHUM):
    rng = np.random.default_rng(tohum)
    adlar = list(TURLER)
    olasiliklar = np.array([TURLER[ad][1] for ad in adlar])
    X, y, turler, oturumlar = [], [], [], []
    while len(X) < n:
        tur = str(rng.choice(adlar, p=olasiliklar / olasiliklar.sum()))
        olaylar, simdi = oturum_uret(tur, rng)
        ozellik = so.ozellikler(olaylar, simdi)
        if ozellik is None:
            continue
        etiket = TURLER[tur][0]
        if rng.random() < ETIKET_GURULTUSU:
            etiket = 1 - etiket
        X.append([ozellik[ad] for ad in OZELLIK_ADLARI])
        y.append(etiket)
        turler.append(tur)
        oturumlar.append((olaylar, simdi))
    return np.array(X), np.array(y), np.array(turler), oturumlar


# ---------------------------------------------------------------------------
# 2) Eğitim: işaret kısıtlı lojistik regresyon
# ---------------------------------------------------------------------------
# Her özelliğin riski hangi YÖNDE etkilediği hipotezle sabitlenir; veri yalnızca
# büyüklüğü belirler. Kısıtsız lojistik regresyonda birbirine yakın ölçen
# özellikler (göreli oyalanma / okuma üstü kalma / yoğun pay) birbirini
# dengelemek için ters işaret alıyordu (baskılayıcı etki): yoğun içerik hiç
# yokken bile risk 0,32 çıkıyordu. Kısıtın gereksiz kıldığı özelliğin katsayısı
# sıfıra iner; bu, kendiliğinden bir özellik seçimidir.
YONLER = {"yogun_pay": 1, "goreli_oyalanma": 1, "yogun_fazla_kalma": 1, "aktif_oran": -1}


class IsaretKisitliLojistik:
    """sklearn LogisticRegression ile aynı kayıp (log kaybı + L2, C=1), L-BFGS-B
    sınırlarıyla katsayı işareti kısıtlı. predict_proba/coef_/intercept_ aynı
    biçimde döner."""

    def __init__(self, yonler: list[int], C: float = 1.0):
        self.yonler, self.C = yonler, C

    def fit(self, X, y):
        n, d = X.shape
        y = np.asarray(y, dtype=float)

        def kayip(w):
            z = X @ w[:d] + w[d]
            return float(np.sum(np.logaddexp(0, z) - y * z) + 0.5 / self.C * w[:d] @ w[:d])

        def gradyan(w):
            fark = expit(X @ w[:d] + w[d]) - y
            return np.append(X.T @ fark + w[:d] / self.C, fark.sum())

        sinirlar = [(0, None) if yon > 0 else (None, 0) for yon in self.yonler] + [(None, None)]
        w = minimize(kayip, np.zeros(d + 1), jac=gradyan, method="L-BFGS-B", bounds=sinirlar).x
        self.coef_, self.intercept_ = np.array([w[:d]]), np.array([w[d]])
        return self

    def predict_proba(self, X):
        p = expit(X @ self.coef_[0] + self.intercept_[0])
        return np.column_stack([1 - p, p])


def egit(n: int = 4000) -> dict:
    X, y, turler, oturumlar = veri_seti_olustur(n)
    indeks = np.arange(len(y))
    egitim_i, test_i = train_test_split(indeks, test_size=0.25, random_state=RASTGELE_TOHUM, stratify=y)
    olcekleyici = StandardScaler().fit(X[egitim_i])
    model = IsaretKisitliLojistik([YONLER[ad] for ad in OZELLIK_ADLARI]).fit(olcekleyici.transform(X[egitim_i]), y[egitim_i])
    return {"model": model, "olcekleyici": olcekleyici, "X": X, "y": y, "turler": turler,
            "oturumlar": oturumlar, "egitim_i": egitim_i, "test_i": test_i}


_EGITIM = None


def egitilmis() -> dict:
    global _EGITIM
    if _EGITIM is None:
        _EGITIM = egit()
    return _EGITIM


def olasilik(ozellik: dict | None) -> float:
    """Özellik yoksa (yeterli güncel gönderi yok) risk 0 kabul edilir."""
    if ozellik is None:
        return 0.0
    e = egitilmis()
    x = e["olcekleyici"].transform(np.array([[ozellik[ad] for ad in OZELLIK_ADLARI]]))
    return float(e["model"].predict_proba(x)[0, 1])


# ---------------------------------------------------------------------------
# 3) v1 (yalnızca karşılaştırma için; eski üretici ve eski özellikler)
# ---------------------------------------------------------------------------
def _v1_model():
    rng = np.random.default_rng(RASTGELE_TOHUM)
    n = 2000
    X = np.column_stack([
        rng.gamma(2.0, 8.0, n), np.clip(rng.beta(2, 3, n), 0, 1), rng.poisson(1.5, n).astype(float),
        np.clip(rng.normal(-0.1, 0.4, n), -1, 1), np.clip(rng.beta(2, 5, n), 0, 1), rng.gamma(3.0, 4.0, n),
    ])
    logit = 0.09 * X[:, 0] + 2.2 * X[:, 1] + 0.55 * X[:, 2] - 1.8 * X[:, 3] - 1.4 * X[:, 4] + 0.05 * X[:, 5] - 3.2
    y = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int)
    maske = rng.random(n) < 0.08
    y[maske] = 1 - y[maske]
    X_egitim, _, y_egitim, _ = train_test_split(X, y, test_size=0.25, random_state=RASTGELE_TOHUM, stratify=y)
    return LogisticRegression(max_iter=1000).fit(X_egitim, y_egitim)


def _v1_ozellikler(olaylar: list[dict]) -> list[float] | None:
    """Eski local-agent.js / motor.py tanımı: zaman penceresi yok, gönderi başına
    son kayıt, son 20 gönderi, tekrar sayısı hep 0."""
    son = {}
    for olay in olaylar:
        son[olay["gonderi"]] = olay
    gunluk = list(son.values())[-20:]
    if not gunluk:
        return None
    toplam = sum(o["dwell"] for o in gunluk) or 1e-9
    negatif = sum(o["dwell"] for o in gunluk if o["ton"] < -0.2)
    return [negatif, negatif / toplam, 0.0, float(np.mean([o["ton"] for o in gunluk])),
            float(np.mean([1.0 if o.get("tiklama") else 0.0 for o in gunluk])), len(gunluk) / max(toplam / 60, 0.1)]


def _v1_olasilik(model, olaylar) -> float:
    ozellik = _v1_ozellikler(olaylar)
    return float(model.predict_proba([ozellik])[0, 1]) if ozellik is not None else float(model.predict_proba([[0] * 6])[0, 1])


# ---------------------------------------------------------------------------
# 4) Değerlendirme
# ---------------------------------------------------------------------------
def _ece(y, p, kutu: int = 10) -> float:
    kenarlar = np.linspace(0, 1, kutu + 1)
    toplam = 0.0
    for alt, ust in zip(kenarlar[:-1], kenarlar[1:]):
        maske = (p >= alt) & ((p < ust) if ust < 1 else (p <= ust))
        if maske.any():
            toplam += maske.mean() * abs(y[maske].mean() - p[maske].mean())
    return float(toplam)


def _metrikler(y, p) -> str:
    tahmin = (p >= 0.5).astype(int)
    return (f"doğruluk {accuracy_score(y, tahmin):.3f} · F1 {f1_score(y, tahmin):.3f} · "
            f"ROC-AUC {roc_auc_score(y, p):.3f} · Brier {brier_score_loss(y, p):.3f} · kalibrasyon hatası (ECE) {_ece(y, p):.3f}")


def _senaryo(ad: str, olaylar: list[dict], simdi: float) -> tuple[str, list[dict], float]:
    return ad, olaylar, simdi


def ornek_senaryolar() -> list[tuple[str, list[dict], float]]:
    """Elle kurulmuş, rastgelelik içermeyen günlükler (README/sunum için)."""
    def olay(i, t, dwell, ton, kelime=14, konu="gundem", roket=False, yorum=False):
        return {"gonderi": i, "zaman": t, "dwell": dwell, "ton": ton, "kelime": kelime, "konu": konu,
                "roket": roket, "yorum": yorum, "tiklama": roket or yorum}

    okuma = so.beklenen_okuma(14)  # ≈ 5,5 sn
    senaryolar = []
    t, g = 0.0, []
    for i in range(20):
        g.append(olay(i, t, okuma * 0.9, -0.8 if i % 4 == 0 else 0.4, konu=KONULAR[i % 10])); t += okuma + 1
    senaryolar.append(_senaryo("Olağan karışık akış: 20 gönderi, 5'i yoğun tonlu, hepsine okuma süresi kadar", g, t))
    t, g = 0.0, []
    for i in range(20):
        g.append(olay(i, t, 2.0, -0.85, konu=KONULAR[i % 10])); t += 3
    senaryolar.append(_senaryo("Yoğun haberlere hızlı göz atma: 20 gönderi, 2'şer sn", g, t))
    t, g = 0.0, []
    for i in range(20):
        yogun = i % 5 < 2
        g.append(olay(i, t, 12.0 if yogun else 3.0, -0.9 if yogun else 0.3, konu="gundem" if yogun else KONULAR[i % 10])); t += (12 if yogun else 3) + 1
    senaryolar.append(_senaryo("Yoğun içerikte pasif oyalanma: 8 yoğun gönderide 12'şer sn, diğerleri 3 sn", g, t))
    t, g = 0.0, []
    for i in range(20):
        yogun = i % 5 < 2
        g.append(olay(i, t, 12.0 if yogun else 3.0, -0.9 if yogun else 0.3, konu="gundem" if yogun else KONULAR[i % 10], yorum=yogun)); t += (12 if yogun else 3) + 1
    senaryolar.append(_senaryo("Aynısı, ama yoğun gönderilere yorum yazılıyor (aktif katılım)", g, t))
    t, g = 0.0, []
    for i in range(20):
        g.append(olay(i, t, 12.0, 0.8, kelime=30, konu=KONULAR[i % 10])); t += 13
    senaryolar.append(_senaryo("Uzun metinleri okuyan, hep olumlu içerik", g, t))
    t, g = 0.0, []
    for i in range(12):
        g.append(olay(100 + i, t, 12.0, -0.9)); t += 13
    t += 3 * 3600
    for i in range(10):
        g.append(olay(i, t, 4.0, 0.2, konu=KONULAR[i])); t += 5
    senaryolar.append(_senaryo("3 saat önce yoğun oturum, şimdi 10 sakin gönderi", g, t))
    return senaryolar


def rapor() -> str:
    e = egitilmis()
    X, y, turler, test_i = e["X"], e["y"], e["turler"], e["test_i"]
    model, olcek = e["model"], e["olcekleyici"]
    p_yeni = model.predict_proba(olcek.transform(X[test_i]))[:, 1]
    v1 = _v1_model()
    p_eski = np.array([_v1_olasilik(v1, e["oturumlar"][i][0]) for i in test_i])
    yt = y[test_i]
    satirlar = [
        "SPİRAL MODELİ v2 · değerlendirme (python spiral_model.py)",
        "=" * 72,
        f"Simüle oturum: {len(y)} (eğitim {len(e['egitim_i'])}, test {len(test_i)}), spiral payı %{100 * y.mean():.0f}, etiket gürültüsü %{100 * ETIKET_GURULTUSU:.0f}",
        "",
        "Test oturumlarında (aynı simülatör, ayrılmış %25):",
        f"  v2: {_metrikler(yt, p_yeni)}",
        f"  v1: {_metrikler(yt, p_eski)}",
        "  DİKKAT: iki model de yeni simülatörde ölçülüyor; bu karşılaştırma v2'nin",
        "  lehine. Gösterdiği şey, eski özelliklerin bu ayrımları (okuma süresi,",
        "  aktif/pasif, zaman) TEMSİL EDEMEDİĞİ; gerçek dünya doğruluğu değil.",
        "",
        "Türe göre 'spiral' deme oranı (eşik 0,5; ilk dört satır aslında spiral DEĞİL):",
    ]
    for tur in ["uzun_okuyan", "aktif_tartisan", "hizli_gozatan", "eski_oturum", "olagan", "spiral", "spirale_gecis"]:
        maske = turler[test_i] == tur
        if maske.any():
            satirlar.append(f"  {tur:15s} n={maske.sum():4d} · v2 %{100 * (p_yeni[maske] >= 0.5).mean():5.1f} · v1 %{100 * (p_eski[maske] >= 0.5).mean():5.1f}")
    satirlar += ["", "Standartlaştırılmış katsayılar (pozitif = riski artırır):"]
    for ad, katsayi in sorted(zip(OZELLIK_ADLARI, model.coef_[0]), key=lambda c: -abs(c[1])):
        satirlar.append(f"  {ad:18s} {katsayi:+.2f}")
    satirlar += ["", "Elle kurulmuş örnek günlükler (v1 → v2):"]
    for ad, olaylar, simdi in ornek_senaryolar():
        satirlar.append(f"  {_v1_olasilik(v1, olaylar):.2f} → {olasilik(so.ozellikler(olaylar, simdi)):.2f}  {ad}")
    satirlar.append(f"  {_v1_olasilik(v1, []):.2f} → {olasilik(None):.2f}  Boş günlük")
    return "\n".join(satirlar)


if __name__ == "__main__":
    metin = rapor()
    print(metin)
    with open("spiral_v2_sonuc.txt", "w", encoding="utf-8") as f:
        f.write(metin + "\n")
