/* NSosyal Local Personalization Agent: raw behaviour stays in IndexedDB. */
(function () {
  const DB_NAME = "nsosyal-local-agent", DB_VERSION = 1, EVENT_LIMIT = 240;
  let database;
  const defaults = () => ({ version: 1, topicWeights: {}, lastCheckinAt: 0, checkins: 0 });
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
  function calculate(events, state) {
    const meaningful = events.filter(event => event.type === "interaction"), recent = meaningful.slice(-12), negative = recent.filter(event => event.tone < -0.15), sustained = negative.filter(event => event.dwell >= 3.5), unique = new Set(recent.map(event => event.topic)).size;
    const intensity = clamp((recent.length ? sustained.length / recent.length : 0) * .72 + (recent.length > 3 ? 1 - unique / recent.length : 0) * .28), confidence = clamp(meaningful.length / 16), enoughData = meaningful.length >= 10;
    const preferred = Object.entries(state.topicWeights || {}).sort((a, b) => b[1] - a[1])[0]?.[0] || null;
    return { mode: "local", eventCount: meaningful.length, enoughData, confidence, intensity, currentMood: !enoughData ? null : intensity > .58 ? "Yoğun" : intensity > .28 ? "Dengeleniyor" : "Dengeli", repeatedNegative: sustained.length, preferredTopic: preferred, shouldCheckin: meaningful.length >= 12 && meaningful.length % 10 === 0 && Date.now() - state.lastCheckinAt > 20 * 60 * 1000 };
  }
  async function trimEvents() { const events = await getEvents(); if (events.length <= EVENT_LIMIT) return; const db = await openDatabase(), tx = db.transaction("events", "readwrite"); events.slice(0, events.length - EVENT_LIMIT).forEach(event => tx.objectStore("events").delete(event.id)); }
  async function summary() { return calculate(await getEvents(), await getState()); }
  async function recordInteraction({ post, dwell, click, rocket, comment, exit }) {
    if (!post || dwell <= 0) return summary();
    const state = await getState(), topic = post.konu || "diger", reward = clamp((Math.min(dwell, 18) / 18) * .42 + (click ? .22 : 0) + (rocket ? .45 : 0) + (comment ? .32 : 0) - (exit ? .04 : 0), -.1, 1), previous = Number(state.topicWeights[topic] || 0);
    state.topicWeights[topic] = clamp(previous * .88 + reward * .12, 0, 1);
    await Promise.all([addEvent({ type: "interaction", createdAt: Date.now(), postId: post.id, topic, tone: safeTone(post.duygu), dwell: Number(dwell.toFixed(2)), click: !!click, rocket: !!rocket, comment: !!comment, exit: !!exit }), setState(state)]);
    await trimEvents(); return summary();
  }
  async function recordCheckin(value) { const state = await getState(); state.lastCheckinAt = Date.now(); state.checkins += 1; await Promise.all([addEvent({ type: "checkin", createdAt: Date.now(), value }), setState(state)]); return summary(); }
  async function rank(posts) {
    const state = await getState(), report = calculate(await getEvents(), state), maxWeight = Math.max(.25, ...Object.values(state.topicWeights || {}).map(Number)), seenTopics = {};
    return posts.map((post, index) => { const localInterest = Number(state.topicWeights[post.konu] || 0) / maxWeight, tone = safeTone(post.duygu), balancing = report.enoughData && report.intensity > .28 && tone < -.15 ? Math.abs(tone) * report.intensity * .38 : 0, diversity = seenTopics[post.konu] ? -.045 * seenTopics[post.konu] : .07; seenTopics[post.konu] = (seenTopics[post.konu] || 0) + 1; const base = Number(post.ilgi_skoru || post.final_skor || .5), localScore = base * .48 + localInterest * .34 + diversity - balancing - index * .0005; return { ...post, local_skor: localScore, local_ilgi: localInterest, local_dengeleme: balancing }; }).sort((a, b) => b.local_skor - a.local_skor);
  }
  async function erase() { const db = await openDatabase(); await new Promise((resolve, reject) => { const tx = db.transaction(["events", "state"], "readwrite"); tx.objectStore("events").clear(); tx.objectStore("state").clear(); tx.oncomplete = resolve; tx.onerror = () => reject(tx.error); }); return summary(); }
  window.LocalPersonalization = { init: openDatabase, recordInteraction, recordCheckin, summary, rank, erase };
})();
