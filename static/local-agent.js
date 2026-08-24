/* NSosyal Local Personalization Agent: raw behaviour stays in IndexedDB. */
(function () {
  const DB_NAME = "nsosyal-local-agent", DB_VERSION = 1, EVENT_LIMIT = 240;
  let database;
  const defaults = () => ({ version: 3, topicWeights: {}, postReactions: {}, newsCategoryWeights: {}, newsReactions: {}, lastCheckinAt: 0, checkins: 0, demoTrace: null });
  function openDatabase() {
    if (database) return Promise.resolve(database);
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(DB_NAME, DB_VERSION);
      request.onupgradeneeded = () => { const db = request.result; if (!db.objectStoreNames.contains("events")) { const events = db.createObjectStore("events", { keyPath: "id", autoIncrement: true }); events.createIndex("createdAt", "createdAt"); } if (!db.objectStoreNames.contains("state")) db.createObjectStore("state"); };
      request.onsuccess = () => { database = request.result; resolve(database); };
      request.onerror = () => reject(request.error);
    });
  }
  async function getState() { const db = await openDatabase(); return new Promise((resolve, reject) => { const request = db.transaction("state", "readonly").objectStore("state").get("profile"); request.onsuccess = () => resolve({ ...defaults(), ...(request.result || {}) }); request.onerror = () => reject(request.error); }); }
  async function setState(state) { const db = await openDatabase(); return new Promise((resolve, reject) => { const tx = db.transaction("state", "readwrite"); tx.objectStore("state").put(state, "profile"); tx.oncomplete = resolve; tx.onerror = () => reject(tx.error); }); }
  async function getEvents() { const db = await openDatabase(); return new Promise((resolve, reject) => { const request = db.transaction("events", "readonly").objectStore("events").getAll(); request.onsuccess = () => resolve((request.result || []).sort((a, b) => a.createdAt - b.createdAt)); request.onerror = () => reject(request.error); }); }
  async function addEvent(event) { const db = await openDatabase(); return new Promise((resolve, reject) => { const tx = db.transaction("events", "readwrite"); tx.objectStore("events").add(event); tx.oncomplete = resolve; tx.onerror = () => reject(tx.error); }); }
  const clamp = (value, min = 0, max = 1) => Math.max(min, Math.min(max, value));
  const safeTone = value => Number.isFinite(Number(value)) ? Number(value) : 0;

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
    const negatifler = log.filter(e => e.tone < -0.2);
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
  // Egitilmis spiral (lojistik regresyon) + psikolojik durum (SGDClassifier)
  // modellerini, hicbir ham veri cihazdan cikmadan burada calistirir --
  // trained-models.js ile trained-weights.js yuklu degilse (eski sayfa
  // onbellegi vb.) eski basit esik-tabanli formule geri duser.
  function _egitilmisYogunluk(meaningful) {
    const log = _dedupluGunluk(meaningful);
    const ozellikler = _spiralOzellikleri(log);
    if (!ozellikler || typeof window.TrainedModels === "undefined") return null;
    const spiralOlasilik = window.TrainedModels.spiralOlasiligi(ozellikler);
    const son = meaningful[meaningful.length - 1];
    const psikolojik = window.TrainedModels.psikolojikTahmin({
      duygu: son.tone, dwell_saniye: son.dwell, tiklama: son.click ? 1 : 0,
      roket: son.rocket ? 1 : 0, yorum: son.comment ? 1 : 0,
    });
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
    return { mode: "local", eventCount: meaningful.length, enoughData, confidence, intensity, currentMood: !enoughData ? null : intensity > .58 ? "Yoğun" : intensity > .28 ? "Dengeleniyor" : "Dengeli", lastExplicitReaction: latestExplicit?.reaction || null, repeatedNegative: sustained.length, preferredTopic: preferred, shouldCheckin: meaningful.length >= 12 && meaningful.length % 10 === 0 && Date.now() - state.lastCheckinAt > 20 * 60 * 1000 };
  }
  async function trimEvents() { const events = await getEvents(); if (events.length <= EVENT_LIMIT) return; const db = await openDatabase(), tx = db.transaction("events", "readwrite"); events.slice(0, events.length - EVENT_LIMIT).forEach(event => tx.objectStore("events").delete(event.id)); }
  async function summary() { return calculate(await getEvents(), await getState()); }
  async function recordInteraction({ post, dwell, click, rocket, comment, exit, demo }) {
    if (!post || dwell <= 0) return summary();
    const state = await getState(), topic = post.konu || "diger", reward = clamp((Math.min(dwell, 18) / 18) * .42 + (click ? .22 : 0) + (rocket ? .45 : 0) + (comment ? .32 : 0) - (exit ? .04 : 0), -.1, 1), previous = Number(state.topicWeights[topic] || 0);
    state.topicWeights[topic] = clamp(previous * .88 + reward * .12, 0, 1);
    await Promise.all([addEvent({ type: "interaction", createdAt: Date.now(), postId: post.id, topic, tone: safeTone(post.duygu), dwell: Number(dwell.toFixed(2)), click: !!click, rocket: !!rocket, comment: !!comment, exit: !!exit, demo: !!demo }), setState(state)]);
    await trimEvents(); return summary();
  }
  async function recordCheckin(value) { const state = await getState(); state.lastCheckinAt = Date.now(); state.checkins += 1; await Promise.all([addEvent({ type: "checkin", createdAt: Date.now(), value }), setState(state)]); return summary(); }
  async function recordPostReaction(post, reaction, demo) {
    const allowed = ["begendim", "umutlandim", "dusundum", "kizdim", "gerildim"];
    if (!post || !allowed.includes(reaction)) return summary();
    const state = await getState(), topic = post.konu || "diger", previous = Number(state.topicWeights[topic] || 0), positiveSignal = reaction === "begendim" || reaction === "umutlandim" || reaction === "dusundum";
    state.postReactions = { ...(state.postReactions || {}), [post.id]: reaction };
    state.topicWeights[topic] = clamp(previous * .9 + (positiveSignal ? .12 : .03), 0, 1);
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
    return posts.map((post, index) => {
      const localInterest = Number(state.topicWeights[post.konu] || 0) / maxWeight, tone = safeTone(post.duygu);
      const balancing = report.enoughData && report.intensity > .28 && tone < -.15 ? Math.abs(tone) * report.intensity * .62 : 0;
      const reactionEffect = latestReaction?.topic === post.konu
        ? (positiveReaction ? .20 : intenseReaction && tone < -.15 ? -.28 : 0)
        : 0;
      const diversity = seenTopics[post.konu] ? -.045 * seenTopics[post.konu] : .07;
      seenTopics[post.konu] = (seenTopics[post.konu] || 0) + 1;
      const base = Number(post.ilgi_skoru || post.final_skor || .5), localScore = base * .48 + localInterest * .34 + diversity - balancing + reactionEffect - index * .0005;
      return { ...post, local_skor: localScore, local_ilgi: localInterest, local_dengeleme: balancing, local_tepki_etkisi: reactionEffect };
    }).sort((a, b) => b.local_skor - a.local_skor);
  }
  async function runDemoScenario(pack) {
    const posts = pack?.gonderiler || pack?.posts || [], scenario = pack?.senaryo || pack?.scenario || [];
    if (!posts.length || !scenario.length) throw new Error("Demo paketi eksik.");
    await erase();
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
      version: pack.surum || pack.version || "jury-replay-v1", createdAt: Date.now(), demo: true,
      candidates: posts.map(compact), signals: scenario.map(signal => ({ ...signal })), summary: report,
      before: before.map((post, index) => ({ id: post.id, position: index + 1, score: post.local_skor })),
      after: after.map((post, index) => ({ id: post.id, position: index + 1, score: post.local_skor, interest: post.local_ilgi, balancing: post.local_dengeleme, reactionEffect: post.local_tepki_etkisi })),
      movedCount: after.filter((post, index) => beforeIndex.get(Number(post.id)) !== index + 1).length,
    };
    const state = await getState(); state.demoTrace = trace; await setState(state); return trace;
  }
  async function getDecisionTrace() { return (await getState()).demoTrace || null; }
  async function erase() { const db = await openDatabase(); await new Promise((resolve, reject) => { const tx = db.transaction(["events", "state"], "readwrite"); tx.objectStore("events").clear(); tx.objectStore("state").clear(); tx.oncomplete = resolve; tx.onerror = () => reject(tx.error); }); return summary(); }
  window.LocalPersonalization = { init: openDatabase, getLocalEvents: getEvents, recordInteraction, recordCheckin, recordPostReaction, postReactionState, recordNewsReaction, newsState, clearNewsData, summary, rank, rankNews, runDemoScenario, getDecisionTrace, erase };
})();
