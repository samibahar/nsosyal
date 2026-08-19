// Haftalık rapor sayfasının "gerçek" bölümü — bu oturumda kaydedilen
// psikolojik durum etkileşimlerinden canlı hesaplanır (sabit örnek metin değil).

const RUH_RENK = {
  sakin: { bg: "var(--ruh-sakin-soft)", fg: "var(--ruh-sakin)" },
  mutluluk: { bg: "var(--ruh-mutluluk-soft)", fg: "var(--ruh-mutluluk)" },
  umut: { bg: "var(--ruh-umut-soft)", fg: "var(--ruh-umut)" },
  korku: { bg: "var(--ruh-korku-soft)", fg: "var(--ruh-korku)" },
  anksiyete: { bg: "var(--ruh-anksiyete-soft)", fg: "var(--ruh-anksiyete)" },
};

async function canliOzetiYukle() {
  const yanit = await fetch("/api/psikolojik-ozet");
  const veri = await yanit.json();

  const bolum = document.getElementById("canli-bolum");
  if (!veri.toplam_etkilesim) {
    bolum.style.display = "none";
    return;
  }
  bolum.style.display = "block";
  document.getElementById("canli-toplam").textContent = veri.toplam_etkilesim;

  const kapsayici = document.getElementById("canli-dagilim");
  kapsayici.innerHTML = "";

  veri.kategoriler.forEach((kategori) => {
    const sayi = veri.kategori_dagilimi[kategori] || 0;
    const yuzde = Math.round((sayi / veri.toplam_etkilesim) * 100);
    const renk = RUH_RENK[kategori] || RUH_RENK.sakin;

    const satir = document.createElement("div");
    satir.className = "olcum-satiri";
    satir.innerHTML = `
      <div class="olcum-baslik"><span>${kategori}</span><b>${sayi} etkileşim (%${yuzde})</b></div>
      <div class="olcum-cubuk-arka"><div class="olcum-cubuk-dolgu" style="width:${yuzde}%;background:${renk.fg}"></div></div>
    `;
    kapsayici.appendChild(satir);
  });

  if (veri.en_belirgin_konu_kategori.length) {
    const not = document.createElement("div");
    not.className = "aciklama-notu";
    not.style.marginTop = "14px";
    const en = veri.en_belirgin_konu_kategori[0];
    not.textContent = `En belirgin örüntü: "${en.konu}" konulu içerikte ${en.sayi} kez "${en.kategori}" kategorisine giren bir tepki kaydedildi.`;
    kapsayici.appendChild(not);
  }
}

async function dogrulamaOzetiYukle() {
  const yanit = await fetch("/api/dogrulama-ozet");
  const veri = await yanit.json();

  const bolum = document.getElementById("dogrulama-ozet-bolum");
  if (!veri.toplam_onay) {
    bolum.style.display = "none";
    return;
  }
  bolum.style.display = "block";

  const icerik = document.getElementById("dogrulama-ozet-icerik");
  const yuzdeMetin = veri.eslesme_orani === null ? "—" : Math.round(veri.eslesme_orani * 100) + "%";

  icerik.innerHTML = `
    <div class="ozet-satiri" style="margin-bottom:12px">
      <div class="ozet-kutu"><div class="sayi">${veri.toplam_onay}</div><div class="etiket">onay sorusu soruldu</div></div>
      <div class="ozet-kutu"><div class="sayi">${veri.eslesen}</div><div class="etiket">tahminle eşleşti</div></div>
      <div class="ozet-kutu"><div class="sayi">${yuzdeMetin}</div><div class="etiket">eşleşme oranı</div></div>
    </div>
  `;

  if (veri.toplam_onay < 5) {
    const not = document.createElement("div");
    not.className = "aciklama-notu";
    not.textContent = "Henüz çok az onay verisi var -- bu oran istatistiksel olarak anlamlı sayılamaz, daha fazla etkileşimle güvenilirleşir.";
    icerik.appendChild(not);
  }
}

canliOzetiYukle();
dogrulamaOzetiYukle();
