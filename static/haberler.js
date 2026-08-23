const newsFeed = document.getElementById("news-feed");
const newsAgent = window.LocalPersonalization;
const newsById = new Map();
let allNews = [], activeCategory = "Tümü", newsState = { reactions: {}, eventCount: 0, lastReaction: null };

const reactionOptions = [
  ["begendim", "👍", "Beğendim"], ["umutlandim", "🌤️", "Umutlandım"],
  ["dusundum", "🤔", "Düşündüm"], ["kizdim", "😠", "Kızdım"], ["gerildim", "😟", "Gerildim"],
];
const reactionLabels = Object.fromEntries(reactionOptions.map(([key, emoji, label]) => [key, `${emoji} ${label}`]));
function escapeNews(value) { const node = document.createElement("div"); node.textContent = value || ""; return node.innerHTML; }
function scoreBox(label, value) { return `<div class="score-box"><small>${label}</small><b>${value}</b></div>`; }

function updateNewsRhythm() {
  const title = document.getElementById("news-rhythm-title"), text = document.getElementById("news-rhythm-text");
  if (!newsState.lastReaction) { title.textContent = "Haber ritmin dengeli"; text.textContent = "Tepkilerin yalnızca bu cihazda kalır."; return; }
  const tense = newsState.lastReaction === "kizdim" || newsState.lastReaction === "gerildim";
  title.textContent = tense ? "Son haber sende yoğun bir tepki bıraktı" : "Tepkini sen belirttin";
  text.textContent = `${reactionLabels[newsState.lastReaction]} · ${newsState.eventCount} yerel haber tepkisi`;
}

function reactionWheel(article) {
  return `<div class="news-reaction-wrap"><button class="news-reaction-trigger" type="button" aria-expanded="false"><span>${reactionLabels[newsState.reactions?.[article.id]] || "☺ Tepki ver"}</span></button><div class="news-reaction-wheel" role="group" aria-label="Bu haber sana nasıl hissettirdi?">${reactionOptions.map(([key, emoji, label]) => `<button type="button" data-reaction="${key}" title="${label}" aria-label="${label}" class="${newsState.reactions?.[article.id] === key ? "selected" : ""}"><span>${emoji}</span><small>${label}</small></button>`).join("")}</div></div>`;
}

function articleCard(article, alternative = false) {
  const card = document.createElement("article");
  card.className = `news-card${alternative ? " alternative-news-card" : ""}`;
  card.dataset.newsId = article.id;
  card.innerHTML = `${alternative ? '<div class="alternative-ribbon">✦ AYNI GELİŞME · BAŞKA BİR KAYNAK</div>' : ""}<div class="news-media"><img src="${article.gorsel}" alt="" loading="lazy"><span>${escapeNews(article.kategori)}</span></div><div class="news-content"><div class="news-source"><span>${escapeNews(article.kaynak_kodu)}</span><div><b>${escapeNews(article.kaynak)}</b><small>${escapeNews(article.zaman)} · örnek kaynak</small></div><i>${escapeNews(article.cerceve)}</i></div><h2>${escapeNews(article.baslik)}</h2><p>${escapeNews(article.ozet)}</p>${reactionWheel(article)}<div class="news-card-footer"><button class="news-why" type="button">✦ Neden bu?</button><span>Skor ${Math.round((article.local_news_score || .5) * 100)}</span></div></div>`;
  const trigger = card.querySelector(".news-reaction-trigger"), wheel = card.querySelector(".news-reaction-wheel");
  trigger.addEventListener("click", event => { event.stopPropagation(); const open = wheel.classList.toggle("open"); trigger.setAttribute("aria-expanded", String(open)); });
  wheel.querySelectorAll("[data-reaction]").forEach(button => button.addEventListener("click", async event => {
    event.stopPropagation();
    newsState = await newsAgent.recordNewsReaction(article, button.dataset.reaction);
    updateNewsRhythm();
    wheel.classList.remove("open"); trigger.setAttribute("aria-expanded", "false");
    trigger.querySelector("span").textContent = reactionLabels[button.dataset.reaction];
    wheel.querySelectorAll("button").forEach(item => item.classList.toggle("selected", item === button));
    if (newsState.shouldOfferAlternative && !alternative) showAlternative(card, article);
  }));
  card.querySelector(".news-why").addEventListener("click", () => openNewsSheet(article));
  return card;
}

function showAlternative(card, article) {
  if (card.nextElementSibling?.classList.contains("alternative-offer")) return;
  const alternative = newsById.get(article.alternatif_id); if (!alternative) return;
  const offer = document.createElement("section"); offer.className = "alternative-offer";
  offer.innerHTML = `<div><span>✦ TEPKİNİ SEN BELİRTTİN</span><h3>Aynı gelişmeye başka bir kaynaktan bakmak ister misin?</h3><p>Bu kaynak aynı temel olguları koruyor; çözüm ve ilerleme tarafına daha fazla bağlam ekliyor.</p></div><div class="alternative-actions"><button class="show-alternative" type="button">Diğer kaynağı göster</button><button class="dismiss-alternative" type="button">Şimdi değil</button></div>`;
  card.insertAdjacentElement("afterend", offer);
  offer.querySelector(".show-alternative").addEventListener("click", () => { const altCard = articleCard(alternative, true); offer.replaceWith(altCard); altCard.scrollIntoView({ behavior: "smooth", block: "center" }); });
  offer.querySelector(".dismiss-alternative").addEventListener("click", () => offer.remove());
}

function renderNews() {
  const primary = allNews.filter(item => item.birincil && (activeCategory === "Tümü" || item.kategori === activeCategory));
  newsFeed.innerHTML = "";
  if (!primary.length) { newsFeed.innerHTML = '<div class="loading-state">Bu kategoride örnek haber yok.</div>'; return; }
  primary.forEach(article => newsFeed.appendChild(articleCard(article)));
}

function openNewsSheet(article = null) {
  const sheet = document.getElementById("news-sheet"), summary = document.getElementById("news-sheet-summary"), scores = document.getElementById("news-sheet-scores"), technical = document.getElementById("news-sheet-technical");
  if (article) {
    summary.textContent = `${article.kaynak} kaynağındaki bu haber, yerel ilgi ve konu çeşitliliği sinyalleriyle sıralandı.`;
    scores.innerHTML = scoreBox("Yerel ilgi", `${Math.round((article.local_news_interest || 0) * 100)}%`) + scoreBox("Çeşitlilik", article.local_news_diversity > 0 ? "Desteklendi" : "Dengelendi") + scoreBox("Sonuç", `${Math.round((article.local_news_score || .5) * 100)}`);
    technical.innerHTML = `<p>Yerel haber skoru: <b>${(article.local_news_score || .5).toFixed(3)}</b><br>Kamuya açık içerik tonu: <b>${Number(article.duygu).toFixed(2)}</b><br>Çerçeve etiketi: <b>${escapeNews(article.cerceve)}</b><br>Olay eşleme anahtarı: <b>${escapeNews(article.olgu_kodu)}</b><br><br>Duygusal tepkin sunucuya gönderilmez.</p>`;
  } else {
    summary.textContent = "Haber adayları sunucudan gelir; hangi haberi nasıl sıraladığımız ve verdiğin duygusal tepkiler bu tarayıcının IndexedDB alanında kalır.";
    scores.innerHTML = scoreBox("Yerel tepki", newsState.eventCount) + scoreBox("Tercih", newsState.preferredCategory || "Oluşuyor") + scoreBox("Kontrol", "Sende");
    technical.innerHTML = "<p><b>İki aşamalı sistem</b><br>1. Sunucu yalnızca örnek haber adaylarını sağlar.<br>2. Tarayıcı; kategori ilgisi, kaynak çeşitliliği ve yoğunluk ağırlığıyla yerel sıralama yapar.<br><br>Öfke veya stres, daha fazla benzer yoğun haber önermek için kullanılmaz.</p>";
  }
  sheet.classList.add("open"); sheet.setAttribute("aria-hidden", "false");
}
function closeNewsSheet() { const sheet = document.getElementById("news-sheet"); sheet.classList.remove("open"); sheet.setAttribute("aria-hidden", "true"); }

async function loadNews() {
  await newsAgent.init();
  const response = await fetch("/api/haberler"), data = await response.json();
  allNews = await newsAgent.rankNews(data.haberler || []); allNews.forEach(item => newsById.set(item.id, item));
  newsState = await newsAgent.newsState(); updateNewsRhythm();
  const categories = [...new Set(allNews.filter(item => item.birincil).map(item => item.kategori))];
  document.getElementById("news-categories").insertAdjacentHTML("beforeend", categories.map(category => `<button data-category="${escapeNews(category)}" type="button">${escapeNews(category)}</button>`).join(""));
  document.querySelectorAll("#news-categories button").forEach(button => button.addEventListener("click", () => { activeCategory = button.dataset.category; document.querySelectorAll("#news-categories button").forEach(item => item.classList.toggle("active", item === button)); renderNews(); }));
  renderNews();
}

document.getElementById("news-info-button").addEventListener("click", () => openNewsSheet());
document.getElementById("news-sheet-close").addEventListener("click", closeNewsSheet);
document.getElementById("news-sheet").addEventListener("click", event => { if (event.target.id === "news-sheet") closeNewsSheet(); });
document.getElementById("news-reset").addEventListener("click", async () => { newsState = await newsAgent.clearNewsData(); allNews = await newsAgent.rankNews(allNews); updateNewsRhythm(); renderNews(); });
document.addEventListener("click", event => { if (!event.target.closest(".news-reaction-wrap")) document.querySelectorAll(".news-reaction-wheel.open").forEach(wheel => wheel.classList.remove("open")); });
loadNews().catch(() => { newsFeed.innerHTML = '<div class="loading-state">Haberler şu an yüklenemedi.</div>'; });
