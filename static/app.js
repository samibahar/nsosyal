// NSosyal duygu-duyarlı akış — timeline arayüzü.
// Intersection Observer ile her gönderinin görünürlük süresini (dwell-time)
// ölçer, backend'e bildirir; backend spiral olasılığını günceller ve akış
// bir sonraki yenilemede buna göre yeniden sıralanır.

const akisEl = document.getElementById("akis");
const spiralDolgu = document.getElementById("spiral-dolgu");
const spiralMetin = document.getElementById("spiral-metin");
const spiralIkon = document.getElementById("spiral-ikon");

const gorunurlukBaslangic = new Map(); // gonderi_id -> performance.now() zamanı

const KONU_RENK = {
  spor: { bg: "var(--konu-spor-soft)", fg: "var(--konu-spor)" },
  gundem: { bg: "var(--konu-gundem-soft)", fg: "var(--konu-gundem)" },
  teknoloji: { bg: "var(--konu-teknoloji-soft)", fg: "var(--konu-teknoloji)" },
};

function konuRenk(konu) {
  return KONU_RENK[konu] || { bg: "var(--konu-varsayilan-soft)", fg: "var(--konu-varsayilan)" };
}

function duyguRengi(d) {
  if (d > 0.15) return "var(--good)";
  if (d < -0.15) return "var(--danger)";
  return "var(--faint)";
}

function seviyeRengi(seviye) {
  if (seviye > 0.6) return "var(--danger)";
  if (seviye > 0.3) return "var(--warn)";
  return "var(--accent)";
}

function seviyeEtiketi(seviye) {
  if (seviye > 0.6) return "Yüksek";
  if (seviye > 0.3) return "Orta";
  return "Sakin";
}

function spiralGostergesiGuncelle(seviye) {
  const yuzde = Math.round(seviye * 100);
  const renk = seviyeRengi(seviye);
  spiralDolgu.style.width = yuzde + "%";
  spiralDolgu.style.background = renk;
  spiralMetin.textContent = `${seviyeEtiketi(seviye)} · %${yuzde}`;
  spiralIkon.style.color = renk;
  spiralIkon.style.background = seviye > 0.6
    ? "var(--danger-soft)"
    : seviye > 0.3
    ? "var(--warn-soft)"
    : "var(--accent-soft)";
}

async function gonderileriGetir() {
  const yanit = await fetch("/api/gonderiler");
  const veri = await yanit.json();
  spiralGostergesiGuncelle(veri.spiral_seviyesi);
  akisiCiz(veri.gonderiler);
}

async function etkilesimGonder(gonderi_id, dwell_saniye, tiklama = false) {
  if (dwell_saniye < 0.3) return; // gürültü filtrele
  const yanit = await fetch("/api/etkilesim", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ gonderi_id, dwell_saniye, tiklama }),
  });
  const veri = await yanit.json();
  spiralGostergesiGuncelle(veri.spiral_seviyesi);
}

function olcumSatiriOlustur(baslik, gosterilenMetin, barDeger, maxDeger, renk) {
  const yuzde = Math.max(0, Math.min(100, (barDeger / maxDeger) * 100));
  const satir = document.createElement("div");
  satir.className = "olcum-satiri";
  satir.innerHTML = `
    <div class="olcum-baslik"><span>${baslik}</span><b>${gosterilenMetin}</b></div>
    <div class="olcum-cubuk-arka"><div class="olcum-cubuk-dolgu" style="width:${yuzde}%;background:${renk}"></div></div>
  `;
  return satir;
}

function akisiCiz(gonderiler) {
  akisEl.innerHTML = "";

  if (!gonderiler.length) {
    akisEl.innerHTML = '<div class="durum-mesaji">Gösterilecek gönderi yok.</div>';
    return;
  }

  const observer = new IntersectionObserver(
    (girdiler) => {
      girdiler.forEach((girdi) => {
        const id = Number(girdi.target.dataset.id);
        if (girdi.isIntersecting) {
          gorunurlukBaslangic.set(id, performance.now());
        } else if (gorunurlukBaslangic.has(id)) {
          const gecenSaniye = (performance.now() - gorunurlukBaslangic.get(id)) / 1000;
          gorunurlukBaslangic.delete(id);
          etkilesimGonder(id, gecenSaniye);
        }
      });
    },
    { threshold: 0.6 } // gönderinin en az %60'ı görünür olmalı
  );

  gonderiler.forEach((g) => {
    const renk = konuRenk(g.konu);
    const dRenk = duyguRengi(g.duygu);

    const kart = document.createElement("article");
    kart.className = "gonderi" + (g.refah_cezasi > 0 ? " yumusatildi" : "");
    kart.dataset.id = g.id;

    kart.innerHTML = `
      <div class="avatar" style="background:${renk.fg}">${g.konu.charAt(0)}</div>
      <div class="govde">
        <div class="ust-satir">
          <span class="konu-etiket" style="background:${renk.bg};color:${renk.fg}">${g.konu}</span>
          ${g.refah_cezasi > 0 ? `<span class="yumusatma-rozeti">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 9v4M12 17h.01M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0Z"/></svg>
            yumuşatıldı
          </span>` : ""}
        </div>
        <div class="metin"></div>
        <div class="alt-satir">
          <button class="neden-buton">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>
            Neden bunu görüyorsun?
          </button>
          <span class="duygu-rozeti"><span class="duygu-nokta" style="background:${dRenk}"></span>duygu ${g.duygu.toFixed(2)}</span>
        </div>
        <div class="aciklama-paneli"></div>
      </div>
    `;
    // metni güvenli biçimde ekle (XSS'ten kaçınmak için textContent kullan)
    kart.querySelector(".metin").textContent = g.metin;

    const panel = kart.querySelector(".aciklama-paneli");
    panel.appendChild(olcumSatiriOlustur("İlgi skoru", g.ilgi_skoru, g.ilgi_skoru, 1, "var(--accent)"));
    if (g.refah_cezasi > 0) {
      panel.appendChild(olcumSatiriOlustur("Refah yumuşatması", "-" + g.refah_cezasi, g.refah_cezasi, 1, "var(--warn)"));
    }
    panel.appendChild(olcumSatiriOlustur("Final skor", g.final_skor, g.final_skor, 1, "var(--good)"));
    const not = document.createElement("div");
    not.className = "aciklama-notu";
    not.textContent = g.aciklama;
    panel.appendChild(not);

    const nedenButon = kart.querySelector(".neden-buton");
    nedenButon.addEventListener("click", (e) => {
      e.stopPropagation();
      panel.classList.toggle("acik");
      nedenButon.classList.toggle("acik");
    });

    kart.addEventListener("click", () => {
      etkilesimGonder(g.id, 1.0, true);
    });

    akisEl.appendChild(kart);
    observer.observe(kart);
  });
}

document.getElementById("yenile-buton").addEventListener("click", gonderileriGetir);
document.getElementById("sifirla-buton").addEventListener("click", async () => {
  await fetch("/api/sifirla", { method: "POST" });
  gonderileriGetir();
});

gonderileriGetir();
