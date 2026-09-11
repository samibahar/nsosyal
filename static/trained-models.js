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
    gunluk.forEach(kayit => {
      const agirlik = Math.pow(0.5, (simdi - kayit.zaman) / P.yari_omur_saniye);
      const oran = Math.min(kayit.dwell / okuma(kayit.kelime), P.oran_ust);
      agirlikTop += agirlik; oranTop += agirlik * oran;
      aktifTop += agirlik * (kayit.roket || kayit.yorum ? 1 : 0);
      if (kayit.ton < P.yogun_ton) { yogunOran += agirlik * oran; yogunAgirlik += agirlik; fazlaTop += agirlik * Math.min(Math.max(0, oran - 1), P.fazla_ust); }
    });
    const digerAgirlik = agirlikTop - yogunAgirlik;
    let goreli = 0;
    if (yogunAgirlik > 0) {
      const yogunOrt = yogunOran / yogunAgirlik, digerOrt = digerAgirlik > 1e-9 ? (oranTop - yogunOran) / digerAgirlik : 1;
      goreli = Math.max(-P.goreli_ust, Math.min(P.goreli_ust, Math.log((yogunOrt + P.goreli_pay) / (digerOrt + P.goreli_pay))));
    }
    return {
      yogun_pay: oranTop > 0 ? yogunOran / oranTop : 0,
      goreli_oyalanma: goreli,
      yogun_fazla_kalma: yogunAgirlik > 0 ? fazlaTop / yogunAgirlik : 0,
      aktif_oran: aktifTop / agirlikTop,
    };
  }

  function _olcekle(ozellikler) {
    const { ozellik_sirasi, olcekleyici_ortalama, olcekleyici_olcek } = W.psikolojik;
    return ozellik_sirasi.map((ad, i) => ((Number(ozellikler[ad]) || 0) - olcekleyici_ortalama[i]) / olcekleyici_olcek[i]);
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

  window.TrainedModels = { spiralOlasiligi, spiralOzellikleri, psikolojikTahmin, varsayilanPsikolojik, psikolojikGuncelle };
})();
