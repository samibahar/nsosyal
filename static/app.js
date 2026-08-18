// NSosyal duygu-duyarlı akış — timeline arayüzü.
// Intersection Observer ile her gönderinin görünürlük süresini (dwell-time)
// ölçer, backend'e bildirir; backend spiral olasılığını günceller ve akış
// bir sonraki yenilemede buna göre yeniden sıralanır.

const akisEl = document.getElementById("akis");
const spiralDolgu = document.getElementById("spiral-dolgu");
const spiralMetin = document.getElementById("spiral-metin");

const gorunurlukBaslangic = new Map(); // gonderi_id -> performance.now() zamanı

function spiralGostergesiGuncelle(seviye) {
  const yuzde = Math.round(seviye * 100);
  spiralDolgu.style.width = yuzde + "%";
  spiralDolgu.style.background = seviye > 0.6 ? "#f4212e" : seviye > 0.3 ? "#ffad1f" : "#1d9bf0";
  spiralMetin.textContent = `${yuzde}% (0=yok, 100=yüksek)`;
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

function akisiCiz(gonderiler) {
  akisEl.innerHTML = "";
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
    const kart = document.createElement("article");
    kart.className = "gonderi" + (g.refah_cezasi > 0 ? " yumusatildi" : "");
    kart.dataset.id = g.id;
    kart.innerHTML = `
      <span class="konu-etiket">${g.konu}</span>
      <div class="metin"></div>
      <div class="alt-satir">
        <button class="neden-buton">Neden bunu görüyorsun? ▾</button>
        <span style="font-size:11px;color:var(--muted)">duygu: ${g.duygu.toFixed(2)}</span>
      </div>
      <div class="aciklama-paneli">
        <div class="satir"><span>İlgi skoru</span><b>${g.ilgi_skoru}</b></div>
        <div class="satir"><span>Refah yumuşatması</span><b>${g.refah_cezasi > 0 ? "-" + g.refah_cezasi : "yok"}</b></div>
        <div class="satir"><span>Final skor</span><b>${g.final_skor}</b></div>
        <div class="satir" style="display:block;margin-top:6px;color:var(--text)">${g.aciklama}</div>
      </div>
    `;
    // metni güvenli biçimde ekle (XSS'ten kaçınmak için textContent kullan)
    kart.querySelector(".metin").textContent = g.metin;

    const nedenButon = kart.querySelector(".neden-buton");
    const panel = kart.querySelector(".aciklama-paneli");
    nedenButon.addEventListener("click", () => {
      panel.classList.toggle("acik");
      nedenButon.textContent = panel.classList.contains("acik")
        ? "Neden bunu görüyorsun? ▴"
        : "Neden bunu görüyorsun? ▾";
    });

    kart.addEventListener("click", (e) => {
      if (e.target === nedenButon) return;
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
