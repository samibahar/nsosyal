/* Egitilmis spiral (lojistik regresyon) ve psikolojik durum (SGDClassifier)
   modellerinin JS'te calisan cikarim (inference) mantigi. Katsayilar
   trained-weights.js'ten geliyor (disa_aktar_modeller.py ile uretildi).
   Bu bir yaklasiklama degil -- ayni egitilmis modelin ayni matematigi,
   sadece Python yerine tarayicida calisiyor. Hicbir ham veri disari cikmiyor. */
(function () {
  const W = window.TrainedModelWeights;

  function sigmoid(z) { return 1 / (1 + Math.exp(-z)); }

  function spiralOlasiligi(ozellikler) {
    const { coef, intercept, ozellik_sirasi } = W.spiral;
    let z = intercept;
    ozellik_sirasi.forEach((ad, i) => { z += coef[i] * (ozellikler[ad] || 0); });
    return sigmoid(z);
  }

  function psikolojikTahmin(ozellikler) {
    const { coef, intercept, ozellik_sirasi, kategoriler, olcekleyici_ortalama, olcekleyici_olcek } = W.psikolojik;
    const ham = ozellik_sirasi.map(ad => Number(ozellikler[ad]) || 0);
    const olcekli = ham.map((deger, i) => (deger - olcekleyici_ortalama[i]) / olcekleyici_olcek[i]);
    const z = coef.map((agirliklar, k) => intercept[k] + agirliklar.reduce((toplam, w, i) => toplam + w * olcekli[i], 0));
    const maxZ = Math.max(...z);
    const expZ = z.map(v => Math.exp(v - maxZ));
    const toplamExp = expZ.reduce((a, b) => a + b, 0);
    const olasiliklar = {};
    kategoriler.forEach((kat, i) => { olasiliklar[kat] = expZ[i] / toplamExp; });
    const baskin = kategoriler.reduce((en, kat) => olasiliklar[kat] > olasiliklar[en] ? kat : en, kategoriler[0]);
    return { kategori: baskin, olasiliklar };
  }

  window.TrainedModels = { spiralOlasiligi, psikolojikTahmin };
})();
