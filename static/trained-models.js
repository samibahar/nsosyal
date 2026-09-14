/* Egitilmis spiral (lojistik regresyon) ve psikolojik durum (SGDClassifier)
   modellerinin JS'te calisan cikarim (inference) mantigi. Katsayilar
   trained-weights.js'ten geliyor (disa_aktar_modeller.py ile uretildi).
   Hicbir ham veri disari cikmiyor. */
(function () {
  const W = window.TrainedModelWeights;

  function sigmoid(z) { return 1 / (1 + Math.exp(-z)); }

  function spiralOlasiligi(ozellikler) {
    const { coef, intercept, ozellik_sirasi, olcekleyici_ortalama: ort, olcekleyici_olcek: olcek } = W.spiral;
    let z = intercept;
    ozellik_sirasi.forEach((ad, i) => { const x = Number(ozellikler[ad]) || 0; z += coef[i] * (ort ? (x - ort[i]) / olcek[i] : x); });
    return sigmoid(z);
  }

  // spiral_ozellik.py'nin satir satir karsiligi; sabitler trained-weights.js'e
  // Python'dan yazilir (tek kaynak). Olay: {gonderi, zaman (sn), dwell, ton,
  // kelime, konu, roket, yorum}. Yeterli guncel gonderi yoksa null.
  function spiralOzellikleri(olaylar, simdi) {
    const P = W.spiral.parametreler;
    const okuma = kelime => P.okuma_taban + Math.max(1, kelime || P.varsayilan_kelime) / P.kelime_hizi;
    const kayitlar = new Map();
    olaylar.forEach(olay => {
      if (simdi - olay.zaman > P.pencere_saniye || olay.dwell <= 0) return;
      const onceki = kayitlar.get(olay.gonderi);
      if (!onceki) { kayitlar.set(olay.gonderi, { ...olay }); return; }
      onceki.dwell = Math.max(onceki.dwell, olay.dwell); onceki.roket = !!(onceki.roket || olay.roket);
      onceki.yorum = !!(onceki.yorum || olay.yorum); onceki.zaman = Math.max(onceki.zaman, olay.zaman);
    });
    const gunluk = [...kayitlar.values()].sort((a, b) => a.zaman - b.zaman).slice(-P.maks_gonderi);
    if (gunluk.length < P.min_gonderi) return null;
    let agirlikTop = 0, oranTop = 0, aktifTop = 0, yogunOran = 0, yogunAgirlik = 0, fazlaTop = 0;
    // Goreli oyalanma yalnizca okuma tabani (1,5 sn) kadar ya da daha uzun
    // durulan gonderilerden hesaplanir; daha kisa durmalar goz gezdirmedir
    // (hizli kaydirmadaki yanlis dengelemeyi onler, spiral_ozellik.py ile ayni).
    let gAgirlik = 0, gOran = 0, gYogunOran = 0, gYogunAgirlik = 0;
    gunluk.forEach(kayit => {
      const agirlik = Math.pow(0.5, (simdi - kayit.zaman) / P.yari_omur_saniye);
      const oran = Math.min(kayit.dwell / okuma(kayit.kelime), P.oran_ust);
      const yogun = kayit.ton < P.yogun_ton;
      agirlikTop += agirlik; oranTop += agirlik * oran;
      aktifTop += agirlik * (kayit.roket || kayit.yorum ? 1 : 0);
      if (yogun) { yogunOran += agirlik * oran; yogunAgirlik += agirlik; fazlaTop += agirlik * Math.min(Math.max(0, oran - 1), P.fazla_ust); }
      if (kayit.dwell >= P.okuma_taban) { gAgirlik += agirlik; gOran += agirlik * oran; if (yogun) { gYogunOran += agirlik * oran; gYogunAgirlik += agirlik; } }
    });
    let goreli = 0;
    if (gYogunAgirlik > 0) {
      const digerAgirlik = gAgirlik - gYogunAgirlik;
      const yogunOrt = gYogunOran / gYogunAgirlik, digerOrt = digerAgirlik > 1e-9 ? (gOran - gYogunOran) / digerAgirlik : 1;
      goreli = Math.max(-P.goreli_ust, Math.min(P.goreli_ust, Math.log((yogunOrt + P.goreli_pay) / (digerOrt + P.goreli_pay))));
    }
    return {
      yogun_pay: oranTop > 0 ? yogunOran / oranTop : 0,
      goreli_oyalanma: goreli,
      yogun_fazla_kalma: yogunAgirlik > 0 ? fazlaTop / yogunAgirlik : 0,
      aktif_oran: aktifTop / agirlikTop,
    };
  }

  // Ruh hali modeli dwell_saniye'yi yalnizca egitim araliginda gordu; tek bir
  // gonderide bundan uzun durma (telefon birakilmis olabilir) ek kanit
  // tasimaz, ustu kesilir. Aksi halde olumsuz icerikte 30 sn durmak "umut"
  // okunuyordu (gercek veri testi, 14.09.2026). Sinir psikolojik_durum.py'den.
  function _olcekle(ozellikler) {
    const { ozellik_sirasi, olcekleyici_ortalama, olcekleyici_olcek, dwell_ust = Infinity } = W.psikolojik;
    return ozellik_sirasi.map((ad, i) => {
      const x = Number(ozellikler[ad]) || 0;
      return ((ad === "dwell_saniye" ? Math.min(x, dwell_ust) : x) - olcekleyici_ortalama[i]) / olcekleyici_olcek[i];
    });
  }

  // SGDClassifier(loss="log_loss") cok sinifli problemde bire-karsi-digerleri
  // (OvR) calisir: her sinif icin ayri bir sigmoid, sonra toplam 1 olacak
  // sekilde normalize edilir. Onceden burada softmax kullaniliyordu; en buyuk
  // sinif ayni kaliyordu ama olasiliklar sklearn'den 0,17'ye kadar sapiyordu
  // (11.09.2026 olcumu). Artik sklearn'in predict_proba'siyla birebir ayni.
  function _sinifSigmoidleri(olcekli, coef, intercept) {
    return coef.map((agirliklar, k) => sigmoid(intercept[k] + agirliklar.reduce((toplam, w, i) => toplam + w * olcekli[i], 0)));
  }

  function psikolojikTahmin(ozellikler, model) {
    const { kategoriler } = W.psikolojik;
    const coef = model?.coef || W.psikolojik.coef, intercept = model?.intercept || W.psikolojik.intercept;
    const s = _sinifSigmoidleri(_olcekle(ozellikler), coef, intercept);
    const toplam = s.reduce((a, b) => a + b, 0) || 1e-12;
    const olasiliklar = {};
    kategoriler.forEach((kat, i) => { olasiliklar[kat] = s[i] / toplam; });
    const baskin = kategoriler.reduce((en, kat) => olasiliklar[kat] > olasiliklar[en] ? kat : en, kategoriler[0]);
    return { kategori: baskin, olasiliklar };
  }

  // Ruh hali tek bir gonderiyle degismez, tek bir gonderinin sinyali de zayif
  // ve gurultuludur. Bu yuzden olasi ruh hali bir PENCEREDEN hesaplanir: son
  // 30 dakikadaki her etkilesim bir kanittir, 10 dakika onceki yarim agirlikta
  // sayilir (spiral ile ayni pencere ve yari omur, trained-weights.js). Kanitlar
  // olasilik vektorlerinin agirlikli ortalamasiyla birlestirilir; carpilmaz,
  // cunku ardisik gonderiler bagimsiz kanit degildir ve carpim modeli
  // gereksiz yere kesinlestirirdi. Olay: {zaman (sn), ozellik (5 sinyal)}.
  // Okuma tabanindan (1,5 sn) kisa durulan gonderi okunmamistir, kanit
  // sayilmaz (spiraldeki goreli oyalanma ile ayni kural). Gercek veri testinde
  // hizli kaydirmada gecilen olumsuz gonderiler ruh halini "anksiyete"ye
  // cekip oturumlarin %40'inda dengelemeyi baslatiyordu (14.09.2026).
  function ruhHaliPenceresiSec(olaylar, simdi) {
    const P = W.spiral.parametreler;
    const secili = olaylar.filter(o => o.zaman <= simdi && simdi - o.zaman <= P.pencere_saniye && (o.ozellik.dwell_saniye ?? P.okuma_taban) >= P.okuma_taban)
      .map(o => ({ olay: o, agirlik: Math.pow(0.5, (simdi - o.zaman) / P.yari_omur_saniye) }));
    const toplam = secili.reduce((a, s) => a + s.agirlik, 0);
    return secili.map(s => ({ ...s, agirlik: s.agirlik / toplam }));
  }
  // Yeterli kanit yoksa (varsayilan: spiral gibi en az 3 etkilesim) null.
  function ruhHaliPenceresi(olaylar, simdi, model, enAz = W.spiral.parametreler.min_gonderi) {
    const secili = ruhHaliPenceresiSec(olaylar, simdi);
    if (!secili.length || secili.length < enAz) return null;
    const { kategoriler } = W.psikolojik, olasiliklar = Object.fromEntries(kategoriler.map(k => [k, 0]));
    secili.forEach(({ olay, agirlik }) => {
      const tahmin = psikolojikTahmin(olay.ozellik, model);
      kategoriler.forEach(k => { olasiliklar[k] += agirlik * tahmin.olasiliklar[k]; });
    });
    const kategori = kategoriler.reduce((en, k) => olasiliklar[k] > olasiliklar[en] ? k : en, kategoriler[0]);
    return { kategori, olasiliklar, kanit: secili.length };
  }
  // Rapor icin: her etkilesim aninda, o ana kadarki pencereyle olasi ruh hali.
  // olaylar zamana gore sirali olmali; kanit yetersizse durum null.
  function ruhHaliSeyri(olaylar, model) {
    const P = W.spiral.parametreler;
    let bas = 0;
    return olaylar.map((olay, i) => {
      while (olay.zaman - olaylar[bas].zaman > P.pencere_saniye) bas++;
      return { olay, durum: ruhHaliPenceresi(olaylar.slice(bas, i + 1), olay.zaman, model) };
    });
  }

  function varsayilanPsikolojik() {
    return { coef: W.psikolojik.coef.map(satir => satir.slice()), intercept: W.psikolojik.intercept.slice(), guncelleme: 0 };
  }

  // Cihazda ogrenme: kullanicinin "su an nasil hissediyorsun?" cevabiyla
  // kisisel modelde TEK bir SGD adimi (her sinif icin lojistik kayip, OvR --
  // sunucudaki kisisel_guncelle ile ayni kayip). Ek olarak varsayilan modele
  // dogru yakinsal (proximal) duzenlilestirme var: kisisel model varsayilandan
  // ancak tutarli cevaplarla uzaklasir, tek bir gurultulu cevap onu savuramaz.
  function psikolojikGuncelle(model, ozellikler, gercekKategori, { eta = 0.15, lambda = 0.05 } = {}) {
    const P = W.psikolojik, hedef = P.kategoriler.indexOf(gercekKategori);
    if (hedef < 0) return model;
    const x = _olcekle(ozellikler), s = _sinifSigmoidleri(x, model.coef, model.intercept);
    const coef = model.coef.map((satir, k) => satir.map((w, i) => w - eta * ((s[k] - (k === hedef ? 1 : 0)) * x[i] + lambda * (w - P.coef[k][i]))));
    const intercept = model.intercept.map((b, k) => b - eta * ((s[k] - (k === hedef ? 1 : 0)) + lambda * (b - P.intercept[k])));
    return { coef, intercept, guncelleme: (model.guncelleme || 0) + 1 };
  }
  // Kontrol cevabi tek bir gonderiye degil, o anki pencereye aittir. Cevap
  // penceredeki etkilesimlere agirliklari oraninda paylastirilir: toplam adim
  // tek bir cevaplik adima esittir (penceredeki ortalama kayip icin bir SGD
  // adimi). Guncelleme sayaci cevap basina bir artar.
  function psikolojikPencereGuncelle(model, olaylar, simdi, gercekKategori, { eta = 0.15, lambda = 0.05 } = {}) {
    const secili = ruhHaliPenceresiSec(olaylar, simdi);
    if (!secili.length) return model;
    let guncel = model;
    secili.forEach(({ olay, agirlik }) => { guncel = psikolojikGuncelle(guncel, olay.ozellik, gercekKategori, { eta: eta * agirlik, lambda }); });
    return { ...guncel, guncelleme: (model.guncelleme || 0) + 1 };
  }

  // Kisisel spiral kalibrasyonu (Platt olcekleme): p = sigmoid(egim x logit(p0) + kayma).
  // Spiral modeli sentetik oturumlarla egitildi; taban duzeyi (sakin bir
  // oturumda ~0,26) simulatorun varsayimidir. Kontrol sorusu cevaplari bu iki
  // parametreyi kullanicinin kendi olcegine ceker. Ozellik katsayilarina
  // dokunulmaz: egim >= 0,25 oldugu surece donusum monotondur, yani
  // literature dayali isaret kisitlari (spiral_model.YONLER) hic tersine donmez.
  const _logit = p => { const q = Math.min(1 - 1e-6, Math.max(1e-6, p)); return Math.log(q / (1 - q)); };
  function varsayilanSpiralKalibrasyonu() { return { egim: 1, kayma: 0, guncelleme: 0 }; }
  function spiralKalibre(p0, kal) { return kal ? sigmoid(kal.egim * _logit(p0) + kal.kayma) : p0; }
  // Tek SGD adimi (log kaybi) + varsayilana (egim 1, kayma 0) dogru yakinsal duzenlilestirme.
  function spiralKalibrasyonGuncelle(kal, p0, etiket, { eta = 0.3, lambda = 0.1 } = {}) {
    const z = _logit(p0), fark = sigmoid(kal.egim * z + kal.kayma) - etiket;
    return {
      egim: Math.min(3, Math.max(0.25, kal.egim - eta * (fark * z + lambda * (kal.egim - 1)))),
      kayma: Math.min(3, Math.max(-3, kal.kayma - eta * (fark + lambda * kal.kayma))),
      guncelleme: (kal.guncelleme || 0) + 1,
    };
  }

  window.TrainedModels = { spiralOlasiligi, spiralOzellikleri, psikolojikTahmin, ruhHaliPenceresiSec, ruhHaliPenceresi, ruhHaliSeyri, varsayilanPsikolojik, psikolojikGuncelle, psikolojikPencereGuncelle, varsayilanSpiralKalibrasyonu, spiralKalibre, spiralKalibrasyonGuncelle };
})();
