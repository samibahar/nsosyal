// Haftalık rapor sayfasının "gerçek" bölümü — bu oturumda kaydedilen
// psikolojik durum etkileşimlerinden canlı hesaplanır (sabit örnek metin değil).

const RUH_RENK = {
  sakin: { bg: "var(--ruh-sakin-soft)", fg: "var(--ruh-sakin)" },
  mutluluk: { bg: "var(--ruh-mutluluk-soft)", fg: "var(--ruh-mutluluk)" },
  umut: { bg: "var(--ruh-umut-soft)", fg: "var(--ruh-umut)" },
  sinirli: { bg: "var(--ruh-sinirli-soft)", fg: "var(--ruh-sinirli)" },
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

async function llmRaporuYukle() {
  const bolum = document.getElementById("llm-rapor-bolum");
  const terapistBolum = document.getElementById("terapist-rapor-bolum");
  try {
    const yanit = await fetch("/api/haftalik-rapor");
    const veri = await yanit.json();
    if (!veri.mevcut) {
      bolum.style.display = "none"; // API anahtarı yok -- sabit örneğe düşülüyor
      terapistBolum.style.display = "none";
      return;
    }
    document.getElementById("llm-rapor-icerik").textContent = veri.metin;
    bolum.style.display = "block";
    terapistBolum.style.display = "block"; // aynı LLM erişimi varsa bu da kullanılabilir
  } catch (e) {
    bolum.style.display = "none";
    terapistBolum.style.display = "none";
  }
}

// --- Terapiste götürülebilecek veri özeti: talep üzerine üretilir (otomatik
// yüklenmez -- her sayfa açılışında ekstra bir LLM çağrısına gerek yok).
async function terapistRaporuUret() {
  const buton = document.getElementById("terapist-rapor-buton");
  const icerik = document.getElementById("terapist-rapor-icerik");
  buton.disabled = true;
  icerik.textContent = "Hazırlanıyor…";
  try {
    const yanit = await fetch("/api/terapist-raporu");
    const veri = await yanit.json();
    icerik.textContent = veri.mevcut ? veri.metin : "Şu an hazırlanamıyor.";
  } catch (e) {
    icerik.textContent = "Şu an hazırlanamıyor.";
  } finally {
    buton.disabled = false;
  }
}

document.getElementById("terapist-rapor-buton").addEventListener("click", terapistRaporuUret);

canliOzetiYukle();
dogrulamaOzetiYukle();
llmRaporuYukle();
