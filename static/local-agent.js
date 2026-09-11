/* NSosyal Local Personalization Agent: raw behaviour stays in IndexedDB. */
(function () {
  const DB_NAME = "nsosyal-local-agent", DB_VERSION = 1, EVENT_LIMIT = 240, GUNLUK_SAKLAMA_GUN = 84, YOGUN_TON = -0.2;
  // Ayarlar sekmesindeki anahtarlar. Hepsi varsayilan olarak acik; kullanicinin
  // secimi yalnizca bu cihazda saklanir ve "yerel verileri sil" ile kaybolmaz.
  const VARSAYILAN_AYARLAR = { dengeleme: true, doygunluk: true, kontrolSorulari: true, kisiselUyarlama: true };
  const KATEGORI_SAYISI = 5;
  let database;
  const defaults = () => ({ version: 4, topicWeights: {}, postReactions: {}, newsCategoryWeights: {}, newsReactions: {}, lastCheckinAt: 0, checkins: 0, demoTrace: null, ayarlar: { ...VARSAYILAN_AYARLAR }, gunluk: {}, kisiselModel: null, dogrulama: null });
  function _tamamla(kayit) { const state = { ...defaults(), ...(kayit || {}) }; state.ayarlar = { ...VARSAYILAN_AYARLAR, ...(state.ayarlar || {}) }; state.gunluk = state.gunluk || {}; return state; }
  function openDatabase() {
    if (database) return Promise.resolve(database);
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(DB_NAME, DB_VERSION);
      request.onupgradeneeded = () => { const db = request.result; if (!db.objectStoreNames.contains("events")) { const events = db.createObjectStore("events", { keyPath: "id", autoIncrement: true }); events.createIndex("createdAt", "createdAt"); } if (!db.objectStoreNames.contains("state")) db.createObjectStore("state"); };
      request.onsuccess = () => { database = request.result; resolve(database); };
      request.onerror = () => reject(request.error);
    });
  }
  async function getState() { const db = await openDatabase(); return new Promise((resolve, reject) => { const request = db.transaction("state", "readonly").objectStore("state").get("profile"); request.onsuccess = () => resolve(_tamamla(request.result)); request.onerror = () => reject(request.error); }); }
  async function setState(state) { const db = await openDatabase(); return new Promise((resolve, reject) => { const tx = db.transaction("state", "readwrite"); tx.objectStore("state").put(state, "profile"); tx.oncomplete = resolve; tx.onerror = () => reject(tx.error); }); }
  async function getEvents() { const db = await openDatabase(); return new Promise((resolve, reject) => { const request = db.transaction("events", "readonly").objectStore("events").getAll(); request.onsuccess = () => resolve((request.result || []).sort((a, b) => a.createdAt - b.createdAt)); request.onerror = () => reject(request.error); }); }
  async function addEvent(event) { const db = await openDatabase(); return new Promise((resolve, reject) => { const tx = db.transaction("events", "readwrite"); tx.objectStore("events").add(event); tx.oncomplete = resolve; tx.onerror = () => reject(tx.error); }); }
  async function clearStores() { const db = await openDatabase(); await new Promise((resolve, reject) => { const tx = db.transaction(["events", "state"], "readwrite"); tx.objectStore("events").clear(); tx.objectStore("state").clear(); tx.oncomplete = resolve; tx.onerror = () => reject(tx.error); }); }
  const clamp = (value, min = 0, max = 1) => Math.max(min, Math.min(max, value));
  const safeTone = value => Number.isFinite(Number(value)) ? Number(value) : 0;

  // Uzun donem ozeti icin GUNLUK TOPLAMLAR. Ham olay kaydi 240 etkilesimle
  // sinirli (veri minimizasyonu); haftalar arasi karsilastirma icin yalnizca
  // gun basina sayilar tutulur -- hangi gonderiye bakildigi tutulmaz.
  function gunAnahtari(zaman = Date.now()) { const d = new Date(zaman); return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`; }
  const _bosGun = () => ({ etkilesim: 0, dwell: 0, yogunDwell: 0, konular: {}, tepkiler: {}, kontroller: {} });
  function _gunlugeIsle(state, degistir) {
    const anahtar = gunAnahtari(), gun = { ..._bosGun(), ...(state.gunluk[anahtar] || {}) };
    delete gun.ornek;
    degistir(gun); state.gunluk[anahtar] = gun;
    const sinir = gunAnahtari(Date.now() - GUNLUK_SAKLAMA_GUN * 86400000);
    Object.keys(state.gunluk).forEach(tarih => { if (tarih < sinir) delete state.gunluk[tarih]; });
  }

  // spiral_model.py'nin _ozellik_cikar'iyla AYNI tanim: gonderi basina tek
  // kayit (en son gorulme), en fazla 20 farkli gonderi -- eski DAVRANIS_GUNLUGU
  // penceresinin ayni matematigi, sadece IndexedDB uzerinde.
  function _dedupluGunluk(meaningful) {
    const sonKayit = new Map();
    meaningful.forEach(event => sonKayit.set(event.postId, event));
    return [...sonKayit.values()].slice(-20);
  }
  function _spiralOzellikleri(log) {
    if (!log.length) return null;
    const toplamDwell = log.reduce((t, e) => t + e.dwell, 0) || 1e-9;
    const negatifler = log.filter(e => e.tone < YOGUN_TON);
    const negatifDwellToplam = negatifler.reduce((t, e) => t + e.dwell, 0);
    return {
      negatif_dwell_toplam: negatifDwellToplam,
      negatif_dwell_orani: negatifDwellToplam / toplamDwell,
      negatif_tekrar_sayisi: 0, // sunucudaki bilinen sinirlilikla tutarli (bkz. motor.py)
      ortalama_duygu: log.reduce((t, e) => t + e.tone, 0) / log.length,
      tiklama_orani: log.reduce((t, e) => t + (e.click ? 1 : 0), 0) / log.length,
      kaydirma_hizi: log.length / Math.max(toplamDwell / 60, 0.1),
    };
  }
  const _psikolojikOzellik = event => ({ duygu: event.tone, dwell_saniye: event.dwell, tiklama: event.click ? 1 : 0, roket: event.rocket ? 1 : 0, yorum: event.comment ? 1 : 0 });
  // Egitilmis spiral (lojistik regresyon) + psikolojik durum (SGDClassifier)
  // modellerini, hicbir ham veri cihazdan cikmadan burada calistirir --
  // trained-models.js yuklu degilse (eski sayfa onbellegi vb.) eski basit
  // esik-tabanli formule geri duser. SIRALAMAYI etkileyen yogunluk her zaman
  // VARSAYILAN modelle hesaplanir: kisisel uyarlama yalnizca tahmin
  // etiketlerini degistirir, akisin kullanici basina kaymasina yol acmaz.
  function _anlikKategoriTahmini(meaningful, model) {
    if (!meaningful.length || typeof window.TrainedModels === "undefined") return null;
    return window.TrainedModels.psikolojikTahmin(_psikolojikOzellik(meaningful[meaningful.length - 1]), model);
  }
  function _egitilmisYogunluk(meaningful) {
    const log = _dedupluGunluk(meaningful);
    const ozellikler = _spiralOzellikleri(log);
    if (!ozellikler || typeof window.TrainedModels === "undefined") return null;
    const spiralOlasilik = window.TrainedModels.spiralOlasiligi(ozellikler);
    const psikolojik = _anlikKategoriTahmini(meaningful);
    const negatifRuhHaliKutlesi = (psikolojik.olasiliklar.sinirli || 0) + (psikolojik.olasiliklar.anksiyete || 0);
    return clamp(spiralOlasilik * 0.7 + negatifRuhHaliKutlesi * 0.3);
  }
  function calculate(events, state) {
    const meaningful = events.filter(event => event.type === "interaction"), recent = meaningful.slice(-12), negative = recent.filter(event => event.tone < -0.15), sustained = negative.filter(event => event.dwell >= 3.5), unique = new Set(recent.map(event => event.topic)).size;
    const yedekYogunluk = clamp((recent.length ? sustained.length / recent.length : 0) * .72 + (recent.length > 3 ? 1 - unique / recent.length : 0) * .28);
    const egitilmisYogunluk = _egitilmisYogunluk(meaningful);
    const intensity = egitilmisYogunluk === null ? yedekYogunluk : egitilmisYogunluk;
    const confidence = clamp(meaningful.length / 16), enoughData = meaningful.length >= 10;
    const preferred = Object.entries(state.topicWeights || {}).sort((a, b) => b[1] - a[1])[0]?.[0] || null;
    // Jüri demosunun betikli tepkileri (runDemoScenario) burada HARİÇ tutulur --
    // aksi halde "Son tepkin: ... sen belirttin" etiketi, kullanıcının hiç
    // tıklamadığı senaryo-içi bir tepkiyi kendisi vermiş gibi gösteriyordu
    // (kullanıcı tarafından tespit edildi, 21.08.2026).
    const latestExplicit = [...events].reverse().find(event => (event.type === "post_reaction" || event.type === "news_reaction") && !event.demo && Date.now() - event.createdAt < 30 * 60 * 1000);
    return { mode: "local", eventCount: meaningful.length, enoughData, confidence, intensity, currentMood: !enoughData ? null : intensity > .58 ? "Yoğun" : intensity > .28 ? "Dengeleniyor" : "Dengeli", lastExplicitReaction: latestExplicit?.reaction || null, repeatedNegative: sustained.length, preferredTopic: preferred, ayarlar: { ...state.ayarlar }, kisiselGuncelleme: state.kisiselModel?.guncelleme || 0, shouldCheckin: state.ayarlar.kontrolSorulari && meaningful.length >= 12 && meaningful.length % 10 === 0 && Date.now() - state.lastCheckinAt > 20 * 60 * 1000 };
  }
  async function trimEvents() { const events = await getEvents(); if (events.length <= EVENT_LIMIT) return; const db = await openDatabase(), tx = db.transaction("events", "readwrite"); events.slice(0, events.length - EVENT_LIMIT).forEach(event => tx.objectStore("events").delete(event.id)); }
  async function summary() { return calculate(await getEvents(), await getState()); }
  async function recordInteraction({ post, dwell, click, rocket, comment, exit, demo }) {
    if (!post || dwell <= 0) return summary();
    const state = await getState(), topic = post.konu || "diger", tone = safeTone(post.duygu), reward = clamp((Math.min(dwell, 18) / 18) * .42 + (click ? .22 : 0) + (rocket ? .45 : 0) + (comment ? .32 : 0) - (exit ? .04 : 0), -.1, 1), previous = Number(state.topicWeights[topic] || 0);
    state.topicWeights[topic] = clamp(previous * .88 + reward * .12, 0, 1);
    // Tek bir acik unutulmus sekme gunluk toplami domine etmesin diye sure 60 sn'de kesilir.
    if (!demo) _gunlugeIsle(state, gun => { const sure = Math.min(dwell, 60); gun.etkilesim += 1; gun.dwell += sure; if (tone < YOGUN_TON) gun.yogunDwell += sure; gun.konular[topic] = (gun.konular[topic] || 0) + 1; });
    await Promise.all([addEvent({ type: "interaction", createdAt: Date.now(), postId: post.id, topic, tone, dwell: Number(dwell.toFixed(2)), click: !!click, rocket: !!rocket, comment: !!comment, exit: !!exit, demo: !!demo }), setState(state)]);
    await trimEvents(); return summary();
  }
  // Kendi kendini dogrulama (EMA) dongusu: kullaniciya soru sorulmadan ONCE
  // modelin o anki tahmini hic gosterilmez (taraflilik olmasin diye).
  // "Once tahmin et, sonra ogren": varsayilan ve kisisel modelin tahmini cevap
  // gelmeden hesaplanir, kisisel model ANCAK ondan sonra cevapla guncellenir.
  // Boylece kisisel modelin eslesme orani, hic gormedigi cevaplar uzerinden olculur.
  // Sayaclar state'te tutulur; ham olay kaydi 240'ta kirpilsa da kaybolmaz.
  async function recordCheckin(value) {
    const state = await getState(), T = window.TrainedModels;
    const son = (await getEvents()).filter(event => event.type === "interaction").at(-1);
    const ozellik = son && T ? _psikolojikOzellik(son) : null;
    const varsayilan = ozellik ? T.psikolojikTahmin(ozellik).kategori : null;
    const kisisel = ozellik && state.kisiselModel ? T.psikolojikTahmin(ozellik, state.kisiselModel).kategori : null;
    const aktif = state.ayarlar.kisiselUyarlama && kisisel ? kisisel : varsayilan;
    if (ozellik && state.ayarlar.kisiselUyarlama) state.kisiselModel = T.psikolojikGuncelle(state.kisiselModel || T.varsayilanPsikolojik(), ozellik, value);
    if (aktif) {
      const d = state.dogrulama || { toplam: 0, eslesen: 0, varsayilanEslesen: 0, kisiselToplam: 0, kisiselEslesen: 0, cevaplar: {} };
      d.toplam += 1; d.eslesen += aktif === value ? 1 : 0; d.varsayilanEslesen += varsayilan === value ? 1 : 0;
      if (kisisel) { d.kisiselToplam += 1; d.kisiselEslesen += kisisel === value ? 1 : 0; }
      d.cevaplar[value] = (d.cevaplar[value] || 0) + 1;
      state.dogrulama = d;
    }
    state.lastCheckinAt = Date.now(); state.checkins += 1;
    _gunlugeIsle(state, gun => { gun.kontroller[value] = (gun.kontroller[value] || 0) + 1; });
    await Promise.all([
      addEvent({ type: "checkin", createdAt: Date.now(), value, tahmin: aktif, eslesme: aktif ? aktif === value : null, tahminVarsayilan: varsayilan, tahminKisisel: kisisel }),
      setState(state),
    ]);
    return summary();
  }
  // Eslesme orani tek basina anlamsiz olabilir: 5 kategoride rastgele tahmin
  // %20 tutar, "hep en sik verilen cevabi soyle" daha da yuksek tutabilir.
  // Bu yuzden iki taban cizgisi de birlikte dondurulur. Cogunluk tabani
  // cevaplarin tamamini bilerek hesaplanir (geriye donuk), yani modele karsi
  // bilincli olarak cömert bir karsilastirmadir.
  async function dogrulamaOzeti() {
    const state = await getState();
    let d = state.dogrulama;
    if (!d) {
      const eski = (await getEvents()).filter(event => event.type === "checkin" && event.eslesme !== null && event.eslesme !== undefined);
      d = { toplam: eski.length, eslesen: eski.filter(event => event.eslesme).length, varsayilanEslesen: eski.filter(event => event.eslesme).length, kisiselToplam: 0, kisiselEslesen: 0, cevaplar: {} };
      eski.forEach(event => { d.cevaplar[event.value] = (d.cevaplar[event.value] || 0) + 1; });
    }
    if (!d.toplam) return { toplam: 0, eslesmeOrani: null };
    const enSik = Math.max(...Object.values(d.cevaplar));
    return {
      toplam: d.toplam,
      eslesmeOrani: d.eslesen / d.toplam,
      varsayilanOrani: d.varsayilanEslesen / d.toplam,
      kisiselOrani: d.kisiselToplam ? d.kisiselEslesen / d.kisiselToplam : null,
      kisiselSayisi: d.kisiselToplam,
      cogunlukOrani: enSik / d.toplam,
      rastgeleOrani: 1 / KATEGORI_SAYISI,
    };
  }
  async function recordPostReaction(post, reaction, demo) {
    const allowed = ["begendim", "umutlandim", "dusundum", "kizdim", "gerildim"];
    if (!post || !allowed.includes(reaction)) return summary();
    const state = await getState(), topic = post.konu || "diger", previous = Number(state.topicWeights[topic] || 0), positiveSignal = reaction === "begendim" || reaction === "umutlandim" || reaction === "dusundum";
    state.postReactions = { ...(state.postReactions || {}), [post.id]: reaction };
    state.topicWeights[topic] = clamp(previous * .9 + (positiveSignal ? .12 : .03), 0, 1);
    if (!demo) _gunlugeIsle(state, gun => { gun.tepkiler[reaction] = (gun.tepkiler[reaction] || 0) + 1; });
    await Promise.all([addEvent({ type: "post_reaction", createdAt: Date.now(), postId: post.id, topic, tone: safeTone(post.duygu), reaction, demo: !!demo }), setState(state)]);
    await trimEvents(); return { ...(await summary()), postReactions: state.postReactions };
  }
  async function postReactionState() { return { reactions: (await getState()).postReactions || {} }; }
  async function recordNewsReaction(article, reaction) {
    const allowed = ["begendim", "umutlandim", "dusundum", "kizdim", "gerildim"];
    if (!article || !allowed.includes(reaction)) return newsState();
    const state = await getState(), category = article.kategori || "Diğer";
    state.newsReactions = { ...(state.newsReactions || {}), [article.id]: reaction };
    const positiveSignal = reaction === "begendim" || reaction === "umutlandim" || reaction === "dusundum";
    const previous = Number((state.newsCategoryWeights || {})[category] || 0);
    state.newsCategoryWeights = { ...(state.newsCategoryWeights || {}), [category]: clamp(previous * .86 + (positiveSignal ? .18 : .06), 0, 1) };
    _gunlugeIsle(state, gun => { gun.tepkiler[reaction] = (gun.tepkiler[reaction] || 0) + 1; });
    await Promise.all([addEvent({ type: "news_reaction", createdAt: Date.now(), articleId: article.id, storyId: article.olay_id, category, tone: safeTone(article.duygu), reaction }), setState(state)]);
    await trimEvents();
    return { ...(await newsState()), shouldOfferAlternative: reaction === "kizdim" || reaction === "gerildim", reaction };
  }
  async function newsState() {
    const state = await getState(), events = (await getEvents()).filter(event => event.type === "news_reaction"), last = events.at(-1);
    return { reactions: state.newsReactions || {}, eventCount: events.length, lastReaction: last?.reaction || null, preferredCategory: Object.entries(state.newsCategoryWeights || {}).sort((a, b) => b[1] - a[1])[0]?.[0] || null };
  }
  async function clearNewsData() {
    const state = await getState(); state.newsReactions = {}; state.newsCategoryWeights = {};
    const events = await getEvents(), db = await openDatabase();
    await new Promise((resolve, reject) => { const tx = db.transaction(["events", "state"], "readwrite"), store = tx.objectStore("events"); events.filter(event => event.type === "news_reaction").forEach(event => store.delete(event.id)); tx.objectStore("state").put(state, "profile"); tx.oncomplete = resolve; tx.onerror = () => reject(tx.error); });
    return newsState();
  }
  async function rankNews(articles) {
    const state = await getState(), weights = state.newsCategoryWeights || {}, maxWeight = Math.max(.2, ...Object.values(weights).map(Number)), seen = {};
    return articles.map((article, index) => {
      const interest = Number(weights[article.kategori] || 0) / maxWeight;
      const diversity = seen[article.kategori] ? -.055 * seen[article.kategori] : .08;
      seen[article.kategori] = (seen[article.kategori] || 0) + 1;
      const score = .54 + interest * .31 + diversity - Math.max(0, -safeTone(article.duygu)) * .06 - index * .001;
      return { ...article, local_news_score: score, local_news_interest: interest, local_news_diversity: diversity };
    }).sort((a, b) => b.local_news_score - a.local_news_score);
  }
  async function rank(posts) {
    const state = await getState(), events = await getEvents(), report = calculate(events, state), maxWeight = Math.max(.25, ...Object.values(state.topicWeights || {}).map(Number)), seenTopics = {};
    // A voluntary reaction is a short-lived, explainable input. It never removes content;
    // it only adjusts order within the user's current feed on this device.
    const latestReaction = [...events].reverse().find(event => event.type === "post_reaction" && Date.now() - event.createdAt < 60 * 60 * 1000);
    const positiveReaction = ["begendim", "umutlandim", "dusundum"].includes(latestReaction?.reaction);
    const intenseReaction = ["kizdim", "gerildim"].includes(latestReaction?.reaction);
    // Ayarlar'da "Duygu dengeleme" kapaliysa yogunluk yine olculur (durum
    // kartinda gosterilir) ama siralamaya HIC yansimaz: akis yalnizca ilgi,
    // cesitlilik ve kullanicinin kendi acik tepkisiyle siralanir.
    const dengelemeAcik = state.ayarlar.dengeleme;
    return posts.map((post, index) => {
      const localInterest = Number(state.topicWeights[post.konu] || 0) / maxWeight, tone = safeTone(post.duygu);
      const balancing = dengelemeAcik && report.enoughData && report.intensity > .28 && tone < -.15 ? Math.abs(tone) * report.intensity * .62 : 0;
      const reactionEffect = latestReaction?.topic === post.konu
        ? (positiveReaction ? .20 : intenseReaction && tone < -.15 ? -.28 : 0)
        : 0;
      // Ceza -.045 iken en yuksek ilgili 1-2 konu ilk sayfanin tamamini
      // kaplayabiliyordu (kullanici tarafindan tespit edildi, 21.08.2026) --
      // güçlendirildi ki ayni konu art arda birkac gonderiden sonra dogal
      // olarak geri cekilsin.
      const diversity = seenTopics[post.konu] ? -.09 * seenTopics[post.konu] : .07;
      seenTopics[post.konu] = (seenTopics[post.konu] || 0) + 1;
      const base = Number(post.ilgi_skoru || post.final_skor || .5), localScore = base * .48 + localInterest * .34 + diversity - balancing + reactionEffect - index * .0005;
      return { ...post, local_skor: localScore, local_ilgi: localInterest, local_dengeleme: balancing, local_tepki_etkisi: reactionEffect };
    }).sort((a, b) => b.local_skor - a.local_skor);
  }
  // Jüri demosu yalnizca siralama profilini sifirlar. Ayarlar, uzun donem
  // gunluk ozetleri ve kisisel model korunur; demo etkilesimleri gunluk
  // ozetlere de yazilmaz (demo:true).
  async function _demoIcinSifirla() {
    const state = await getState();
    await clearStores();
    await setState({ ...defaults(), ayarlar: state.ayarlar, gunluk: state.gunluk, kisiselModel: state.kisiselModel, dogrulama: state.dogrulama });
  }
  async function runDemoScenario(pack) {
    const posts = pack?.gonderiler || pack?.posts || [], scenario = pack?.senaryo || pack?.scenario || [];
    if (!posts.length || !scenario.length) throw new Error("Demo paketi eksik.");
    await _demoIcinSifirla();
    const before = await rank(posts), byId = new Map(posts.map(post => [Number(post.id), post]));
    for (const signal of scenario) {
      const post = byId.get(Number(signal.post_id));
      if (!post) continue;
      await recordInteraction({ post, dwell: Number(signal.dwell || 0), click: !!signal.click, rocket: false, comment: false, exit: false, demo: true });
      if (signal.reaction) await recordPostReaction(post, signal.reaction, true);
    }
    const after = await rank(posts), report = await summary(), beforeIndex = new Map(before.map((post, index) => [Number(post.id), index + 1]));
    const compact = post => ({ id: post.id, metin: post.metin, konu: post.konu, duygu: safeTone(post.duygu), yazar: post.yazar, yazar_bilgi: post.yazar_bilgi });
    const trace = {
      version: pack.surum || pack.version || "jury-replay-v1", createdAt: Date.now(), demo: true, dengelemeAcik: report.ayarlar.dengeleme,
      candidates: posts.map(compact), signals: scenario.map(signal => ({ ...signal })), summary: report,
      before: before.map((post, index) => ({ id: post.id, position: index + 1, score: post.local_skor })),
      after: after.map((post, index) => ({ id: post.id, position: index + 1, score: post.local_skor, interest: post.local_ilgi, balancing: post.local_dengeleme, reactionEffect: post.local_tepki_etkisi })),
      movedCount: after.filter((post, index) => beforeIndex.get(Number(post.id)) !== index + 1).length,
    };
    const state = await getState(); state.demoTrace = trace; await setState(state); return trace;
  }
  async function getDecisionTrace() { return (await getState()).demoTrace || null; }
  // "Yerel verileri sil": olaylar, profil, gunluk ozetler ve kisisel model
  // silinir. Yalnizca Ayarlar'daki secimler korunur -- dengelemeyi kapatmis
  // bir kullanici veri sildi diye dengeleme sessizce geri acilmasin.
  async function erase() { const state = await getState(); await clearStores(); await setState({ ...defaults(), ayarlar: state.ayarlar }); return summary(); }

  async function getAyarlar() { return { ...(await getState()).ayarlar }; }
  async function setAyar(anahtar, deger) {
    if (!(anahtar in VARSAYILAN_AYARLAR)) throw new Error(`Bilinmeyen ayar: ${anahtar}`);
    const state = await getState(); state.ayarlar[anahtar] = !!deger; await setState(state); return { ...state.ayarlar };
  }
  async function kisiselModelDurumu() { const state = await getState(); return { guncelleme: state.kisiselModel?.guncelleme || 0, aktif: state.ayarlar.kisiselUyarlama && !!state.kisiselModel }; }
  // Icgoru grafiklerinde kullanilacak model: kisisel uyarlama aciksa ve en az
  // bir kez guncellendiyse kisisel model, degilse null (= varsayilan).
  async function etiketModeli() { const state = await getState(); return state.ayarlar.kisiselUyarlama && state.kisiselModel ? state.kisiselModel : null; }
  async function kisiselModeliSifirla() { const state = await getState(); state.kisiselModel = null; await setState(state); return kisiselModelDurumu(); }
  async function uzunDonemOzeti() {
    const state = await getState();
    const gunler = Object.entries(state.gunluk).sort((a, b) => a[0].localeCompare(b[0])).map(([tarih, gun]) => ({ tarih, ...gun }));
    return { gunler, ornekVar: gunler.some(gun => gun.ornek), saklamaGun: GUNLUK_SAKLAMA_GUN, olaySiniri: EVENT_LIMIT, olaySayisi: (await getEvents()).length };
  }
  // Sunum icin ORNEK gecmis: son 4 haftanin gercek veri olmayan gunlerine
  // acikca "ornek" olarak isaretlenmis toplamlar yazar. Sabit tohumlu uretici
  // kullanildigi icin her seferinde ayni gorunur; bilincli olarak iyilesme
  // hikayesi anlatan bir egilim uretmez. Tek tusla geri alinabilir.
  async function ornekGecmisYukle() {
    const state = await getState(), bugun = gunAnahtari();
    let tohum = 20260911;
    const rastgele = () => { tohum = (tohum * 1664525 + 1013904223) % 4294967296; return tohum / 4294967296; };
    const konular = ["teknoloji", "bilim", "spor", "gundem", "sanat", "ekonomi", "oyun", "seyahat"];
    const cevaplar = ["sakin", "mutluluk", "umut", "sinirli", "anksiyete"];
    const tepkiler = ["begendim", "umutlandim", "dusundum", "kizdim", "gerildim"];
    for (let geri = 28; geri >= 1; geri--) {
      const tarih = gunAnahtari(Date.now() - geri * 86400000);
      const r = rastgele();
      if (tarih === bugun || state.gunluk[tarih] || r < 0.18) continue;
      const etkilesim = 8 + Math.floor(rastgele() * 34), dwell = etkilesim * (3 + rastgele() * 4), yogunPay = 0.18 + rastgele() * 0.34;
      const gun = { ..._bosGun(), ornek: true, etkilesim, dwell: Math.round(dwell), yogunDwell: Math.round(dwell * yogunPay) };
      for (let i = 0; i < etkilesim; i++) { const konu = konular[Math.floor(Math.pow(rastgele(), 1.6) * konular.length)]; gun.konular[konu] = (gun.konular[konu] || 0) + 1; }
      if (rastgele() < 0.5) { const tepki = tepkiler[Math.floor(rastgele() * tepkiler.length)]; gun.tepkiler[tepki] = 1 + Math.floor(rastgele() * 3); }
      if (rastgele() < 0.35) { const cevap = cevaplar[Math.floor(rastgele() * cevaplar.length)]; gun.kontroller[cevap] = 1; }
      state.gunluk[tarih] = gun;
    }
    await setState(state); return uzunDonemOzeti();
  }
  async function ornekGecmisiKaldir() {
    const state = await getState();
    Object.keys(state.gunluk).forEach(tarih => { if (state.gunluk[tarih].ornek) delete state.gunluk[tarih]; });
    await setState(state); return uzunDonemOzeti();
  }
  window.LocalPersonalization = { init: openDatabase, getLocalEvents: getEvents, recordInteraction, recordCheckin, dogrulamaOzeti, recordPostReaction, postReactionState, recordNewsReaction, newsState, clearNewsData, summary, rank, rankNews, runDemoScenario, getDecisionTrace, erase, getAyarlar, setAyar, kisiselModelDurumu, etiketModeli, kisiselModeliSifirla, uzunDonemOzeti, ornekGecmisYukle, ornekGecmisiKaldir };
})();
