// NSosyal duygu-duyarlı akış — timeline arayüzü.
// Intersection Observer ile her gönderinin görünürlük süresini (dwell-time)
// ölçer, backend'e bildirir; backend spiral olasılığını günceller. Akış,
// aşağı kaydırdıkça bizim skor motorumuza göre sayfa sayfa (infinite scroll)
// yüklenir -- sabit, tek seferlik bir liste değil.

const akisEl = document.getElementById("akis");
const spiralDolgu = document.getElementById("spiral-dolgu");
const spiralMetin = document.getElementById("spiral-metin");

function ruhHaliGuncelle(psikolojik) {
  if (!psikolojik) return;
  Object.entries(psikolojik.olasiliklar).forEach(([kategori, olasilik]) => {
    const satir = document.querySelector(`.ruh-hali-cubuk-satiri[data-kategori="${kategori}"]`);
    if (!satir) return;
    const yuzde = Math.round(olasilik * 100);
    satir.querySelector(".ruh-hali-cubuk-dolgu").style.width = yuzde + "%";
    satir.querySelector(".ruh-hali-cubuk-yuzde").textContent = "%" + yuzde;
  });
}

const gorunurlukBaslangic = new Map(); // gonderi_id -> performance.now() zamanı

function guncelDwell(gonderi_id) {
  // Roket/yorum/tıklama anında gönderi hâlâ görünürse gerçek geçen süreyi kullan;
  // değilse (görünürlük takip edilmiyorsa) makul bir varsayılana düş.
  if (gorunurlukBaslangic.has(gonderi_id)) {
    return Math.max(0.3, (performance.now() - gorunurlukBaslangic.get(gonderi_id)) / 1000);
  }
  return 1.5;
}

const KONU_RENK = {
  spor: { bg: "var(--konu-spor-soft)", fg: "var(--konu-spor)" },
  gundem: { bg: "var(--konu-gundem-soft)", fg: "var(--konu-gundem)" },
  teknoloji: { bg: "var(--konu-teknoloji-soft)", fg: "var(--konu-teknoloji)" },
  bilim: { bg: "var(--konu-bilim-soft)", fg: "var(--konu-bilim)" },
  saglik: { bg: "var(--konu-saglik-soft)", fg: "var(--konu-saglik)" },
  ekonomi: { bg: "var(--konu-ekonomi-soft)", fg: "var(--konu-ekonomi)" },
  sanat: { bg: "var(--konu-sanat-soft)", fg: "var(--konu-sanat)" },
  egitim: { bg: "var(--konu-egitim-soft)", fg: "var(--konu-egitim)" },
  oyun: { bg: "var(--konu-oyun-soft)", fg: "var(--konu-oyun)" },
  seyahat: { bg: "var(--konu-seyahat-soft)", fg: "var(--konu-seyahat)" },
};

function konuRenk(konu) {
  return KONU_RENK[konu] || { bg: "var(--konu-varsayilan-soft)", fg: "var(--konu-varsayilan)" };
}

// --- Sağ panel: o an ekranda yüklü gönderilerden gerçek zamanlı konu sayacı ---
const konuSayaclariEl = document.getElementById("konu-sayaclari");
const konuSayilari = {};

function konuSayaciKaydet(konu) {
  konuSayilari[konu] = (konuSayilari[konu] || 0) + 1;
}

function konuSayaciSifirla() {
  Object.keys(konuSayilari).forEach((k) => delete konuSayilari[k]);
}

function konuSayaciGoster() {
  if (!konuSayaclariEl) return;
  const siraliKonular = Object.entries(konuSayilari).sort((a, b) => b[1] - a[1]).slice(0, 8);
  if (!siraliKonular.length) {
    konuSayaclariEl.innerHTML = '<div class="durum-mesaji-kucuk">Akış yüklendikçe dolacak…</div>';
    return;
  }
  konuSayaclariEl.innerHTML = siraliKonular
    .map(([konu, sayi]) => {
      const renk = konuRenk(konu);
      return `<div class="konu-sayac-satiri">
        <span class="konu-sayac-etiket"><span class="konu-sayac-nokta" style="background:${renk.fg}"></span>${konu}</span>
        <span class="konu-sayac-sayi">${sayi}</span>
      </div>`;
    })
    .join("");
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
  doygunlukGuncelle(seviye);
}

// --- Renk doygunluğu azaltma ---
// spiral_seviyesi zaten (negatif dwell oranı + ortalama duygu + tıklama oranı +
// kaydırma hızı)'nın eğitilmiş modelle birleştirilmiş TEK hâli -- doygunluğu bu
// dört sinyali ayrı ayrı tartıp yeniden birleştirmek yerine, zaten güven-çarpanlı
// bu değere bağlıyoruz. Durum yükseldikçe akış nazikçe soluklaşır (kesin bir
// sınır/engel değil, fark ettirmeye yönelik yumuşak bir sinyal).
let doygunlukAktif = true;

function doygunlukGuncelle(seviye) {
  if (!doygunlukAktif) {
    akisEl.style.filter = "saturate(100%)";
    return;
  }
  // Düşük seviyelerde (özellikle güven-çarpanının küçük tuttuğu ilk birkaç
  // etkileşimde) %45'lik eski maksimum gözle neredeyse fark edilmiyordu --
  // %75'e çıkarıldı (19.08.2026, kullanıcı bildirdi). Eğri de hafifçe
  // öne yüklendi (seviye^0.7) ki orta seviyelerde de fark edilir olsun,
  // sadece seviye=1'e çok yaklaşınca değil.
  const doygunluk = Math.round(100 - Math.pow(seviye, 0.7) * 75);
  akisEl.style.filter = `saturate(${doygunluk}%)`;
}

document.getElementById("doygunluk-buton").addEventListener("click", (e) => {
  doygunlukAktif = !doygunlukAktif;
  const buton = e.currentTarget;
  buton.classList.toggle("aktif", doygunlukAktif);
  document.getElementById("doygunluk-buton-metin").textContent =
    "Doygunluk azaltma: " + (doygunlukAktif ? "Açık" : "Kapalı");
  if (!doygunlukAktif) akisEl.style.filter = "saturate(100%)";
});

async function etkilesimGonder(gonderi_id, dwell_saniye, tiklama = false, roket = false, yorum = false) {
  const acikEylemVar = tiklama || roket || yorum;
  if (!acikEylemVar && dwell_saniye < 0.3) return; // sadece pasif dwell'de gürültü filtrele
  const yanit = await fetch("/api/etkilesim", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ gonderi_id, dwell_saniye, tiklama, roket, yorum }),
  });
  const veri = await yanit.json();
  spiralGostergesiGuncelle(veri.spiral_seviyesi);
  ruhHaliGuncelle(veri.psikolojik_durum);
  if (veri.onay_sorulsun_mu) dogrulamaGoster();
}

// --- Kendi kendini doğrulama kartı ---
// psikolojik_durum.py'nin davranış->kategori eşlemesi sentetik senaryolara
// dayanıyor; gerçek bir dayanak için ara sıra kullanıcıya soruyoruz ve
// cevabını modelin O ANKİ tahminiyle karşılaştırıyoruz. Model tahmini,
// taraflı olmasın diye kullanıcı cevap vermeden ÖNCE hiç gösterilmiyor.
const dogrulamaKarti = document.getElementById("dogrulama-karti");

function dogrulamaGoster() {
  dogrulamaKarti.classList.remove("gizli");
}

function dogrulamaGizle() {
  dogrulamaKarti.classList.add("gizli");
}

dogrulamaKarti.querySelectorAll(".dogrulama-secenek").forEach((buton) => {
  buton.addEventListener("click", async () => {
    dogrulamaGizle();
    const yanit = await fetch("/api/dogrulama", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ kullanici_cevabi: buton.dataset.kategori }),
    });
    const veri = await yanit.json();
    const aktifButon = document.querySelector('.kisisel-secenek[data-aktif="true"]');
    const acikMi = aktifButon && aktifButon.classList.contains("aktif");
    const not = document.getElementById("kisisel-not");
    if (not) {
      not.textContent = acikMi
        ? `Kişiselleştirilmiş model, ${veri.kisisel_guncelleme_sayisi} onaya dayanıyor.`
        : `Kişiselleştirme ${veri.kisisel_guncelleme_sayisi} onay biriktirdi (şu an kapalı).`;
    }
  });
});

document.getElementById("dogrulama-gec-buton").addEventListener("click", dogrulamaGizle);

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

// --- Dwell-time takibi: tek bir paylaşılan gözlemci, akışa eklenen her yeni
// kart bu gözlemciye kaydolur (sayfalamada her seferinde yeniden yaratılmaz).
const dwellGozlemci = new IntersectionObserver(
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

function kartOlustur(g) {
  const renk = konuRenk(g.konu);
  const dRenk = duyguRengi(g.duygu);
  konuSayaciKaydet(g.konu);

  const kart = document.createElement("article");
  kart.className = "gonderi" + (g.refah_cezasi > 0 ? " yumusatildi" : "");
  kart.dataset.id = g.id;

  kart.innerHTML = `
    <div class="avatar" style="background:${renk.fg}">${g.konu.slice(0, 2)}</div>
    <div class="govde">
      <div class="ust-satir">
        <span class="konu-etiket" style="background:${renk.bg};color:${renk.fg}">${g.konu}</span>
        ${g.refah_cezasi > 0 ? `<span class="yumusatma-rozeti">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 9v4M12 17h.01M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0Z"/></svg>
          yumuşatıldı
        </span>` : ""}
      </div>
      <div class="metin"></div>
      ${g.id % 3 !== 0 ? `<div class="medya-yer-tutucu">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-5-5L5 21"/></svg>
      </div>` : ""}
      <div class="alt-satir">
        <button class="neden-buton">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>
          Neden bunu görüyorsun?
        </button>
        <span class="duygu-rozeti"><span class="duygu-nokta" style="background:${dRenk}"></span>duygu ${g.duygu.toFixed(2)}</span>
      </div>
      <div class="etkilesim-satiri">
        <div class="mini-eylemler">
          <button class="mini-eylem-buton roket" title="Roket at">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/></svg>
            Roket
          </button>
          <button class="mini-eylem-buton yorum" title="Yorum yaz">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
            Yorum
          </button>
        </div>
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

  // Roket/yorum tuşlarına spam basmak, tek bir olayı değil, backend'de aynı
  // gönderiye ait TEK bir kaydı güncelliyor (bkz. backend/main.py), bu yüzden
  // burada sadece hızlı art arda ağ isteğini önlemek için basit bir kilit var.
  let gonderiliyor = false;
  async function eylemGonder(roket, yorum, aktifButon) {
    if (gonderiliyor) return;
    gonderiliyor = true;
    aktifButon.classList.toggle("aktif");
    await etkilesimGonder(g.id, guncelDwell(g.id), false, roket, yorum);
    gonderiliyor = false;
  }

  const roketButon = kart.querySelector(".mini-eylem-buton.roket");
  roketButon.addEventListener("click", (e) => {
    e.stopPropagation();
    eylemGonder(!roketButon.classList.contains("aktif"), false, roketButon);
  });

  const yorumButon = kart.querySelector(".mini-eylem-buton.yorum");
  yorumButon.addEventListener("click", (e) => {
    e.stopPropagation();
    eylemGonder(false, !yorumButon.classList.contains("aktif"), yorumButon);
  });

  kart.addEventListener("click", () => {
    etkilesimGonder(g.id, guncelDwell(g.id), true);
  });

  dwellGozlemci.observe(kart);
  return kart;
}

// --- Sayfalama (infinite scroll) ---
const sentinel = document.createElement("div");
sentinel.id = "akis-sentinel";
sentinel.className = "durum-mesaji";

let yukleniyor = false;
let tukendi = false;

const sayfaGozlemci = new IntersectionObserver((girdiler) => {
  if (girdiler[0].isIntersecting) dahaFazlaYukle();
}, { rootMargin: "400px" }); // ekrandan 400px önce tetikle, kullanıcı beklemesin

async function sayfaGetir(sifirdan) {
  const yanit = await fetch(`/api/gonderiler?sifirdan=${sifirdan}`);
  const veri = await yanit.json();
  spiralGostergesiGuncelle(veri.spiral_seviyesi);
  tukendi = veri.tukendi;
  return veri.gonderiler;
}

async function ilkYuklemeYap() {
  yukleniyor = true;
  tukendi = false;
  akisEl.innerHTML = "";
  konuSayaciSifirla();
  const gonderiler = await sayfaGetir(true);

  if (!gonderiler.length) {
    akisEl.innerHTML = '<div class="durum-mesaji">Gösterilecek gönderi yok.</div>';
    yukleniyor = false;
    return;
  }

  gonderiler.forEach((g) => akisEl.appendChild(kartOlustur(g)));
  akisEl.appendChild(sentinel);
  sentinel.textContent = "";
  sayfaGozlemci.observe(sentinel);
  konuSayaciGoster();
  yukleniyor = false;
}

async function dahaFazlaYukle() {
  if (yukleniyor || tukendi) return;
  yukleniyor = true;
  sentinel.textContent = "Yeni gönderiler yükleniyor…";

  const gonderiler = await sayfaGetir(false);
  gonderiler.forEach((g) => akisEl.insertBefore(kartOlustur(g), sentinel));

  sentinel.textContent = tukendi ? "Akışın sonuna geldin." : "";
  if (tukendi) sayfaGozlemci.unobserve(sentinel);
  konuSayaciGoster();
  yukleniyor = false;
}

document.getElementById("yenile-buton").addEventListener("click", ilkYuklemeYap);
document.getElementById("sifirla-buton").addEventListener("click", async () => {
  await fetch("/api/sifirla", { method: "POST" });
  ilkYuklemeYap();
});

// --- Varsayılan / Kişiselleştirilmiş model anahtarı ---
// Kişiselleştirme, kullanıcının doğrulama cevaplarıyla KISISEL_MODEL'i (ayrı
// bir kopya) yavaşça günceller; varsayılan model hiç değişmez. Bu anahtar,
// aynı oturumdaki gönderi geçmişini SEÇİLEN modelle yeniden skorlatıp iki
// hâli karşılaştırmayı sağlıyor.
document.querySelectorAll(".kisisel-secenek").forEach((buton) => {
  buton.addEventListener("click", async () => {
    const aktif = buton.dataset.aktif === "true";
    document.querySelectorAll(".kisisel-secenek").forEach((b) => b.classList.toggle("aktif", b === buton));
    const yanit = await fetch(`/api/kisisel-mod?aktif=${aktif}`, { method: "POST" });
    const veri = await yanit.json();
    ruhHaliGuncelle(veri.psikolojik_durum);
    const sayi = veri.kisisel_guncelleme_sayisi;
    document.getElementById("kisisel-not").textContent = aktif
      ? `Kişiselleştirilmiş model, ${sayi} onaya dayanıyor.`
      : `Kişiselleştirme ${sayi} onay biriktirdi (şu an kapalı).`;
  });
});

// --- Karanlık mod (manuel anahtar; sistem tercihi zaten @media ile destekleniyor) ---
const karanlikButon = document.getElementById("karanlik-mod-buton");
if (karanlikButon) {
  const kayitliTercih = localStorage.getItem("karanlikMod");
  if (kayitliTercih === "acik") {
    document.documentElement.classList.add("karanlik-zorla");
    karanlikButon.classList.add("aktif");
  }
  karanlikButon.addEventListener("click", () => {
    const acik = document.documentElement.classList.toggle("karanlik-zorla");
    karanlikButon.classList.toggle("aktif", acik);
    localStorage.setItem("karanlikMod", acik ? "acik" : "kapali");
  });
}

ilkYuklemeYap();
