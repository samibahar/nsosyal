/* Egitilmis spiral (lojistik regresyon) ve psikolojik durum (SGDClassifier)
   modellerinin JS'te calisan cikarim (inference) mantigi. Katsayilar
   trained-weights.js'ten geliyor (disa_aktar_modeller.py ile uretildi).
   Hicbir ham veri disari cikmiyor. */
(function () {
  const W = window.TrainedModelWeights;

  function sigmoid(z) { return 1 / (1 + Math.exp(-z)); }

  function spiralOlasiligi(ozellikler) {
    const { coef, intercept, ozellik_sirasi } = W.spiral;
    let z = intercept;
    ozellik_sirasi.forEach((ad, i) => { z += coef[i] * (ozellikler[ad] || 0); });
    return sigmoid(z);
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

  window.TrainedModels = { spiralOlasiligi, psikolojikTahmin, varsayilanPsikolojik, psikolojikGuncelle };
})();
