// Mobile-first feed UI. The API contract is intentionally unchanged.
const feed = document.getElementById("akis");
const topicCounts = {};
const visibleSince = new Map();
let currentSpiral = 0;
let loading = false;
let exhausted = false;
const postCache = new Map();
const localAgent = window.LocalPersonalization;
let localSummary = { eventCount: 0, enoughData: false, intensity: 0, currentMood: null, confidence: 0 };
let localPostReactions = {};
const POST_REACTIONS = [["begendim","👍","Beğendim"],["umutlandim","🌤️","Umutlandım"],["dusundum","🤔","Düşündüm"],["kizdim","😠","Kızdım"],["gerildim","😟","Gerildim"]];
const POST_REACTION_LABELS = Object.fromEntries(POST_REACTIONS.map(([key,emoji,label])=>[key,`${emoji} ${label}`]));

const TOPICS = {
  spor:{name:"Spor",author:"Ekin Spor",handle:"@ekinsporu",glyph:"⚽",bg:"linear-gradient(145deg,#8bb861,#3d7250)",shape:"#2f6948",pill:"#e9f6d7",ink:"#5d8d3a"},
  gundem:{name:"Gündem",author:"Güncel Notlar",handle:"@guncelnotlar",glyph:"◎",bg:"linear-gradient(145deg,#f0bd76,#a87346)",shape:"#75554a",pill:"#fff0da",ink:"#a86a31"},
  teknoloji:{name:"Teknoloji",author:"Teknoloji Ajandası",handle:"@tekajanda",glyph:"⌁",bg:"linear-gradient(145deg,#79c4e8,#5471a3)",shape:"#3b628f",pill:"#e4f3fb",ink:"#3c7ba4"},
  bilim:{name:"Bilim Kulübü",author:"Bilim Kulübü",handle:"@bilimkulubu",glyph:"✺",bg:"linear-gradient(145deg,#c6b0f0,#6d67a1)",shape:"#564a87",pill:"#eeeaff",ink:"#7057aa"},
  saglik:{name:"Yaşam",author:"Yaşam Notları",handle:"@yasamnotlari",glyph:"◌",bg:"linear-gradient(145deg,#9fd8c4,#4e8c7d)",shape:"#357364",pill:"#ddf7ec",ink:"#3a9074"},
  ekonomi:{name:"Ekonomi",author:"Pusula",handle:"@pusula",glyph:"↗",bg:"linear-gradient(145deg,#f0ca7a,#a98337)",shape:"#7d6439",pill:"#fff4d8",ink:"#a47b24"},
  sanat:{name:"Kültür & Sanat",author:"Kültür Ajandası",handle:"@kulturajandasi",glyph:"♫",bg:"linear-gradient(145deg,#ecaa9a,#aa6375)",shape:"#88455e",pill:"#ffe8e2",ink:"#b35f57"},
  egitim:{name:"Eğitim",author:"Kampüs",handle:"@kampus",glyph:"⌂",bg:"linear-gradient(145deg,#b7dd94,#688f50)",shape:"#53783d",pill:"#edf8df",ink:"#608d3f"},
  oyun:{name:"Oyun",author:"Oyun Dünyası",handle:"@oyundunyasi",glyph:"◈",bg:"linear-gradient(145deg,#ca9cf0,#7755a2)",shape:"#5b3b88",pill:"#f2e6ff",ink:"#8052aa"},
  seyahat:{name:"Keşif",author:"Yolda",handle:"@yoldanotlar",glyph:"⌁",bg:"linear-gradient(145deg,#79c7c6,#397e83)",shape:"#336c76",pill:"#e0f7f4",ink:"#357d7d"}
};
function topicFor(topic){ return TOPICS[topic] || {name:topic,author:"NSosyal",handle:"@nsosyal",glyph:"✦",bg:"linear-gradient(145deg,#b8d9ab,#67885d)",shape:"#56734f",pill:"#edf4e8",ink:"#587a55"}; }
function escapeText(value){ const el=document.createElement("div");el.textContent=value;return el.innerHTML; }

function statusCopy(level){
  if(level>.6)return {title:"Akış biraz yoğunlaştı",text:"Benzer yoğun içeriklerde daha uzun kaldığını fark ettik. Akışı nazikçe dengeliyoruz."};
  if(level>.3)return {title:"Akış dengeleniyor",text:"İlgi alanlarının içinde daha çeşitli içeriklere yer veriyoruz."};
  return {title:"Akış dengeli",text:"İlgi alanlarına göre taze ve çeşitli içerikler seçtik."};
}
function updateStatus(level){
  currentSpiral=level; const copy=statusCopy(level);
  document.getElementById("flow-status-title").textContent=copy.title;
  document.getElementById("flow-status-text").textContent=copy.text;
  document.getElementById("desktop-status-title").textContent=copy.title;
  document.getElementById("desktop-status-text").textContent=copy.text;
  feed.style.filter=`saturate(${Math.round(100-Math.pow(level,.7)*32)}%)`;
}
function updateMood(psikolojikDurum){
  const etiketler={mutluluk:"Keyifli",umut:"Umutlu",sakin:"Sakin",sinirli:"Yoğun",anksiyete:"Yoğun"};
  const kategori=psikolojikDurum&&psikolojikDurum.kategori;
  const metin=kategori?`Olası anlık ritim: ${etiketler[kategori]||"Dengeli"} · doğrulanmadı`:"Olası anlık ritim: Henüz yeterli sinyal yok";
  document.getElementById("flow-current-mood").textContent=metin;
  document.getElementById("desktop-current-mood").textContent=metin;
}
function updateDuyguKatmani(katman){
  if(!katman)return;
  const title=document.getElementById("flow-status-title"), text=document.getElementById("flow-status-text"), desktopTitle=document.getElementById("desktop-status-title"), desktopText=document.getElementById("desktop-status-text");
  if(!katman.veri_yeterli){title.textContent="Akışını tanıyoruz";text.textContent=`${katman.anlamli_etkilesim}/10 anlamlı etkileşim · henüz yorum yapmak için erken`;desktopTitle.textContent=title.textContent;desktopText.textContent=text.textContent;return;}
  if(katman.surdurulmus_oruntu){title.textContent="Akış biraz yoğunlaştı";text.textContent="Sürdürülebilir bir örüntü gördük; akışı nazikçe dengeleyebilirsin.";desktopTitle.textContent=title.textContent;desktopText.textContent=text.textContent;}
  if(katman.mudahale_uygun&&typeof intervention!=="undefined")intervention.hidden=false;
}
function updateTopics(){
  const list=document.getElementById("konu-sayaclari"); const rows=Object.entries(topicCounts).sort((a,b)=>b[1]-a[1]).slice(0,5);
  list.innerHTML=rows.length?rows.map(([key,count])=>`<div class="topic-row"><b>${escapeText(topicFor(key).name)}</b><span>${count} gönderi</span></div>`).join(""):'<span class="topic-loading">Akış yükleniyor…</span>';
}
function updateLocalAgent(summary){
  localSummary=summary;
  const title=document.getElementById("flow-status-title"),text=document.getElementById("flow-status-text"),desktopTitle=document.getElementById("desktop-status-title"),desktopText=document.getElementById("desktop-status-text");
  if(!summary.enoughData){title.textContent="Bu cihazda öğreniyor";text.textContent=`${summary.eventCount}/10 anlamlı etkileşim · ham davranış verisi cihazında kalır`;desktopTitle.textContent=title.textContent;desktopText.textContent=text.textContent;if(summary.lastExplicitReaction){const mood=`Son tepkin: ${POST_REACTION_LABELS[summary.lastExplicitReaction]} · sen belirttin`;document.getElementById("flow-current-mood").textContent=mood;document.getElementById("desktop-current-mood").textContent=mood;}else updateMood(null);return;}
  updateStatus(summary.intensity);
  const mood=summary.lastExplicitReaction?`Son tepkin: ${POST_REACTION_LABELS[summary.lastExplicitReaction]} · sen belirttin`:`Olası anlık ritim: ${summary.currentMood} · kullanıcı tarafından doğrulanmadı`;
  document.getElementById("flow-current-mood").textContent=mood;document.getElementById("desktop-current-mood").textContent=mood;
}
function incrementTopic(topic){topicCounts[topic]=(topicCounts[topic]||0)+1;}
function resetTopics(){Object.keys(topicCounts).forEach(key=>delete topicCounts[key]);}

async function sendInteraction(id,dwell,click=false,rocket=false,comment=false,exit=false){
  if(dwell<=0)return;
  if(localAgent){
    try{const data=await localAgent.recordInteraction({post:postCache.get(id),dwell,click,rocket,comment,exit});updateLocalAgent(data);if(data.shouldCheckin)showCheckin();}catch(error){console.warn("Local interaction could not be recorded",error);}return;
  }
  try{
    const res=await fetch("/api/etkilesim",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({gonderi_id:id,dwell_saniye:dwell,tiklama:click,roket:rocket,yorum:comment,cikis:exit})});
    const data=await res.json(); updateStatus(data.spiral_seviyesi); updateMood(data.psikolojik_durum); updateDuyguKatmani(data.duygu_katmani); if(data.onay_sorulsun_mu)showCheckin();
  }catch(error){console.warn("Interaction could not be recorded",error);}
}
function dwellFor(id){return visibleSince.has(id)?Math.max(.3,(performance.now()-visibleSince.get(id))/1000):1.5;}
const dwellObserver=new IntersectionObserver(entries=>entries.forEach(entry=>{
  const id=Number(entry.target.dataset.id);
  if(entry.isIntersecting)visibleSince.set(id,performance.now());
  else if(visibleSince.has(id)){const dwell=(performance.now()-visibleSince.get(id))/1000;visibleSince.delete(id);sendInteraction(id,dwell,false,false,false,true);}
}),{threshold:.6});

function scoreBox(label,value){return `<div class="score-box"><small>${label}</small><b>${value}</b></div>`;}
function openLocalSheet(post){
  const sheet=document.getElementById("explanation-sheet"),summary=document.getElementById("sheet-summary"),scores=document.getElementById("sheet-score-grid"),technical=document.getElementById("technical-details-content");
  if(post){
    summary.textContent="Bu post, cihazındaki ilgi profili ve akış çeşitliliği sinyalleriyle yerelde sıralandı.";
    scores.innerHTML=scoreBox("İlgi eşleşmesi",`${Math.round((post.local_ilgi||0)*100)}%`)+scoreBox("Akış ayarı",post.local_dengeleme?`−${Math.round(post.local_dengeleme*100)} puan`:"Yok")+scoreBox("Yerel sonuç",`${Math.round((post.local_skor||0)*100)}%`);
    technical.innerHTML=`<p><b>Yerel çevrim içi sıralama</b><br>İlgi ağırlığı: <b>${(post.local_ilgi||0).toFixed(2)}</b><br>Akış dengeleme: <b>${(post.local_dengeleme||0).toFixed(2)}</b><br>Yerel sıralama skoru: <b>${(post.local_skor||0).toFixed(2)}</b><br><br>Ham tıklama ve durma süresi bu hesap için sunucuya gönderilmez.</p>`;
  }else{
    summary.textContent="Kişiselleştirme profili ve ham etkileşim geçmişi bu tarayıcının IndexedDB alanında tutulur. Sunucu yalnızca herkese açık aday postları sağlar.";
    scores.innerHTML=scoreBox("Yerel sinyal",`${localSummary.eventCount} etkileşim`)+scoreBox("Güven",`${Math.round((localSummary.confidence||0)*100)}%`)+scoreBox("Kontrol","Sende");
    technical.innerHTML=`<p><b>Yerel çevrim içi öğrenme</b><br>Tercih profili: <b>${localSummary.preferredTopic||"henüz oluşmadı"}</b><br>Akış yoğunluğu: <b>${Math.round((localSummary.intensity||0)*100)}%</b><br><br><button type="button" id="erase-local-profile" class="text-button">Yerel verileri sil</button></p>`;
  }
  sheet.classList.add("open");sheet.setAttribute("aria-hidden","false");
  setTimeout(()=>{const erase=document.getElementById("erase-local-profile");if(erase)erase.addEventListener("click",eraseLocalProfile);},0);
}
function openSheet(post=null){
  if(localAgent){openLocalSheet(post);return;}
  const sheet=document.getElementById("explanation-sheet"); const summary=document.getElementById("sheet-summary"); const scores=document.getElementById("sheet-score-grid"); const technical=document.getElementById("technical-details-content");
  if(post){
    summary.textContent=post.aciklama;
    scores.innerHTML=scoreBox("İlgi eşleşmesi",`${Math.round(post.ilgi_skoru*100)}%`)+scoreBox("Akış ayarı",post.refah_cezasi?`−${Math.round(post.refah_cezasi*100)} puan`:"Yok")+scoreBox("Sonuç",`${Math.round(post.final_skor*100)}%`);
    technical.innerHTML=`<p>Duygu skoru: <b>${post.duygu.toFixed(2)}</b><br>İlgi skoru: <b>${post.ilgi_skoru.toFixed(2)}</b><br>Refah yumuşatması: <b>${post.refah_cezasi.toFixed(2)}</b><br>Final sıralama skoru: <b>${post.final_skor.toFixed(2)}</b></p>`;
  }else{
    const copy=statusCopy(currentSpiral);summary.textContent=copy.text;scores.innerHTML=scoreBox("Akış yoğunluğu",`${Math.round(currentSpiral*100)}%`)+scoreBox("Yaklaşım","Nazik dengeleme")+scoreBox("Kontrol","Sende");technical.innerHTML=`<p>Spiral seviyesi: <b>${currentSpiral.toFixed(3)}</b><br>Bu değer son etkileşim örüntülerinden hesaplanır. İçerik kaldırılmaz; yalnızca sıralamadaki ağırlığı değişebilir.</p>`;
  }
  sheet.classList.add("open");sheet.setAttribute("aria-hidden","false");
}
function closeSheet(){const sheet=document.getElementById("explanation-sheet");sheet.classList.remove("open");sheet.setAttribute("aria-hidden","true");}
document.getElementById("status-detail-button").addEventListener("click",()=>openSheet());
document.getElementById("desktop-detail-button").addEventListener("click",()=>openSheet());
document.getElementById("sheet-close").addEventListener("click",closeSheet);
document.getElementById("explanation-sheet").addEventListener("click",event=>{if(event.target.id==="explanation-sheet")closeSheet();});
document.addEventListener("click",event=>{if(!event.target.closest(".post-reaction-wrap"))document.querySelectorAll(".post-reaction-wheel.open").forEach(wheel=>{wheel.classList.remove("open");wheel.closest(".post-reaction-wrap")?.querySelector(".post-reaction-trigger")?.setAttribute("aria-expanded","false");});});

function createCard(post){
  postCache.set(post.id,post);
  const topic=topicFor(post.konu);incrementTopic(post.konu);
  const author=post.yazar_bilgi?{id:post.yazar_bilgi.id,name:post.yazar_bilgi.name,handle:post.yazar_bilgi.handle,initials:post.yazar_bilgi.initials,color:post.yazar_bilgi.color}:authorForPost(post);
  const card=document.createElement("article");card.className="post-card"+(post.refah_cezasi>0?" yumusatildi":"");card.dataset.id=post.id;
  const selectedReaction=localPostReactions[post.id];
  card.innerHTML=`<div class="post-body"><div class="post-meta"><span class="avatar" style="background:${topic.bg}">${topic.glyph}</span><div><div class="author">${escapeText(topic.author)}</div><div class="handle">${escapeText(topic.handle)} · şimdi</div></div><button class="post-menu" aria-label="Gönderi seçenekleri">•••</button></div><p class="post-text"></p></div><div class="post-visual" style="--visual-bg:${topic.bg};--visual-shape:${topic.shape}"><span class="visual-glyph">${topic.glyph}</span><span class="visual-caption">${escapeText(topic.name)} · Senin için seçildi</span></div><div class="post-actions"><div class="action-group"><div class="post-reaction-wrap"><button class="action-button post-reaction-trigger" type="button" aria-label="Duygu tepkisi ver" aria-expanded="false"><span>${selectedReaction?POST_REACTION_LABELS[selectedReaction]:"☺ Tepki"}</span></button><div class="post-reaction-wheel" role="group" aria-label="Bu gönderi sana nasıl hissettirdi?">${POST_REACTIONS.map(([key,emoji,label])=>`<button type="button" data-post-reaction="${key}" aria-label="${label}" title="${label}" class="${selectedReaction===key?"selected":""}"><span>${emoji}</span><small>${label}</small></button>`).join("")}</div></div><button class="action-button comment" type="button" aria-label="Yorum">◌ <span>Yorum</span></button></div>${post.refah_cezasi>0?'<span class="softened-pill">✦ dengelendi</span>':'<button class="why-button" type="button">✦ Neden bu?</button>'}</div>`;
  card.querySelector(".post-text").textContent=post.metin;
  card.querySelector(".post-visual").insertAdjacentHTML("afterbegin",`<img class="post-photo" src="${postImage(post)}" alt="${escapeText(topic.name)} iÃ§eriÄŸi iÃ§in temsili gÃ¶rsel" loading="lazy">`);
  const avatar=card.querySelector(".post-meta .avatar");avatar.textContent=author.initials;avatar.style.background=author.color;avatar.classList.add("profile-trigger");avatar.title=`${author.name} profilini aç`;
  const authorName=card.querySelector(".post-meta .author");authorName.innerHTML=`<a class="post-author-link" href="/profil.html?u=${encodeURIComponent(author.id)}">${escapeText(author.name)}</a>`;
  card.querySelector(".post-meta .handle").textContent=`${author.handle} · şimdi`;
  avatar.addEventListener("click",event=>{event.stopPropagation();location.href=`/profil.html?u=${encodeURIComponent(author.id)}`;});
  const why=card.querySelector(".why-button");if(why)why.addEventListener("click",event=>{event.stopPropagation();openSheet(post);});
  card.querySelector(".comment").addEventListener("click",event=>{event.stopPropagation();sendInteraction(post.id,dwellFor(post.id),false,false,true);openComments(post);});
  const reactionTrigger=card.querySelector(".post-reaction-trigger"),reactionWheel=card.querySelector(".post-reaction-wheel");
  reactionTrigger.addEventListener("click",event=>{
    event.preventDefault();event.stopPropagation();
    const willOpen=!reactionWheel.classList.contains("open");
    document.querySelectorAll(".post-reaction-wheel.open").forEach(wheel=>{wheel.classList.remove("open");wheel.closest(".post-reaction-wrap")?.querySelector(".post-reaction-trigger")?.setAttribute("aria-expanded","false");});
    reactionWheel.classList.toggle("open",willOpen);reactionTrigger.setAttribute("aria-expanded",String(willOpen));
  });
  reactionWheel.querySelectorAll("[data-post-reaction]").forEach(button=>button.addEventListener("click",async event=>{
    event.preventDefault();event.stopPropagation();
    const reaction=button.dataset.postReaction;
    localPostReactions[post.id]=reaction;reactionTrigger.querySelector("span").textContent=POST_REACTION_LABELS[reaction];
    reactionWheel.classList.remove("open");reactionTrigger.setAttribute("aria-expanded","false");
    reactionWheel.querySelectorAll("button").forEach(item=>item.classList.toggle("selected",item===button));
    if(localAgent)updateLocalAgent(await localAgent.recordPostReaction(post,reaction));
  }));
  card.addEventListener("click",event=>{if(event.target.closest(".post-author-link,.profile-trigger"))return;sendInteraction(post.id,dwellFor(post.id),true);});dwellObserver.observe(card);return card;
}

const sentinel=document.createElement("div");sentinel.className="loading-state";sentinel.id="feed-sentinel";
const pageObserver=new IntersectionObserver(entries=>{if(entries[0].isIntersecting)loadMore();},{rootMargin:"420px"});
async function getPage(reset){const response=await fetch(`/api/gonderiler?sifirdan=${reset}`);const data=await response.json();if(!localAgent)updateStatus(data.spiral_seviyesi);exhausted=data.tukendi;return localAgent?await localAgent.rank(data.gonderiler):data.gonderiler;}
async function firstLoad(){
  loading=true;exhausted=false;feed.innerHTML="";resetTopics();if(localAgent)localPostReactions=(await localAgent.postReactionState()).reactions;const posts=await getPage(true);
  if(!posts.length){feed.innerHTML='<div class="loading-state">Gösterilecek gönderi yok.</div>';loading=false;return;}
  posts.forEach(post=>feed.appendChild(createCard(post)));feed.appendChild(sentinel);sentinel.textContent="";pageObserver.observe(sentinel);updateTopics();loading=false;
}
async function loadMore(){if(loading||exhausted)return;loading=true;sentinel.textContent="Yeni gönderiler hazırlanıyor…";const posts=await getPage(false);posts.forEach(post=>feed.insertBefore(createCard(post),sentinel));sentinel.textContent=exhausted?"Akışın sonuna geldin.":"";if(exhausted)pageObserver.unobserve(sentinel);updateTopics();loading=false;}
document.getElementById("yenile-buton").addEventListener("click",firstLoad);
async function eraseLocalProfile(){
  if(localAgent){const data=await localAgent.erase();updateLocalAgent(data);closeSheet();await firstLoad();return;}
  await fetch("/api/sifirla",{method:"POST"});closeSheet();firstLoad();
}
document.getElementById("sifirla-buton").addEventListener("click",eraseLocalProfile);
function showCheckin(){const until=Number(sessionStorage.getItem("nsosyal-checkin-snooze-until")||0);if(Date.now()<until)return;document.getElementById("dogrulama-karti").classList.remove("gizli");}
function hideCheckin(){document.getElementById("dogrulama-karti").classList.add("gizli");}
document.getElementById("dogrulama-gec-buton").addEventListener("click",()=>{sessionStorage.setItem("nsosyal-checkin-snooze-until",String(Date.now()+20*60*1000));hideCheckin();});
document.querySelectorAll(".dogrulama-secenek").forEach(button=>button.addEventListener("click",async()=>{hideCheckin();if(localAgent){updateLocalAgent(await localAgent.recordCheckin(button.dataset.kategori));return;}await fetch("/api/dogrulama",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({kullanici_cevabi:button.dataset.kategori})});}));

// Navigation sheets and composer keep the social app controls usable without
// changing the ranking/interaction API used by the feed.
const appPanel=document.getElementById("app-panel");
const panelSections={explore:document.getElementById("panel-explore"),activity:document.getElementById("panel-activity"),composer:document.getElementById("panel-composer")};
function openPanel(name){
  Object.entries(panelSections).forEach(([key,section])=>section.hidden=key!==name);
  appPanel.classList.add("open");appPanel.setAttribute("aria-hidden","false");
  if(name==="activity")loadActivities();
  if(name==="composer")setTimeout(()=>document.getElementById("post-text").focus(),160);
}
function closePanel(){appPanel.classList.remove("open");appPanel.setAttribute("aria-hidden","true");}
async function loadActivities(){const list=document.querySelector("#panel-activity .activity-list");try{const response=await fetch("/api/etkinlikler");const data=await response.json();list.innerHTML=data.etkinlikler.length?data.etkinlikler.map(item=>`<article><span style="background:${item.actor_color||'#e7eee0'}">${escapeText(item.actor_initials||'✦')}</span><div><b>${escapeText(item.actor_name||'NSosyal')} ${escapeText(item.message)}</b><p>${item.post_id?"Gönderine göz atabilirsin.":"Yeni bir sosyal güncelleme var."}</p></div><time>Şimdi</time></article>`).join(""):'<p class="panel-empty">Henüz yeni bir etkinlik yok.</p>';}catch{list.innerHTML='<p class="panel-empty">Etkinlikler şu an yüklenemedi.</p>';}}
document.querySelectorAll("[data-panel]").forEach(control=>control.addEventListener("click",event=>{event.preventDefault();openPanel(control.dataset.panel);}));
document.getElementById("app-panel-close").addEventListener("click",closePanel);
appPanel.addEventListener("click",event=>{if(event.target===appPanel)closePanel();});
document.querySelectorAll(".explore-chips button").forEach(button=>button.addEventListener("click",()=>{button.classList.toggle("active");}));
document.getElementById("panel-composer").addEventListener("submit",async event=>{
  event.preventDefault();const text=document.getElementById("post-text"),topic=document.getElementById("post-topic"),message=document.getElementById("composer-message"),submit=event.currentTarget.querySelector('[type="submit"]');
  submit.disabled=true;message.textContent="Gönderin ekleniyor…";
  try{const response=await fetch("/api/gonderiler",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({metin:text.value,konu:topic.value})});const data=await response.json();if(!data.ok)throw new Error(data.hata||"Gönderi eklenemedi.");text.value="";message.textContent="Gönderin akışa eklendi.";await firstLoad();setTimeout(closePanel,500);}catch(error){message.textContent=error.message||"Gönderi şu an eklenemedi.";}finally{submit.disabled=false;}
});
let activeCommentPost=null;
function renderComments(items){const list=document.getElementById("comment-list");list.innerHTML=items.length?items.map(item=>`<article><span class="comment-avatar" style="background:${item.color}">${escapeText(item.initials)}</span><div><b>${escapeText(item.name)}</b><small>${escapeText(item.handle)}</small><p>${escapeText(item.text)}</p></div></article>`).join(""):'<p class="panel-empty">İlk yorumu sen yaz.</p>';}
async function openComments(post){activeCommentPost=post;Object.values(panelSections).forEach(section=>section.hidden=true);const comments=document.getElementById("panel-comments");comments.hidden=false;appPanel.classList.add("open");appPanel.setAttribute("aria-hidden","false");const list=document.getElementById("comment-list");list.innerHTML='<p class="panel-empty">Yorumlar yükleniyor…</p>';try{const response=await fetch(`/api/gonderiler/${post.id}/yorumlar`);renderComments((await response.json()).yorumlar||[]);}catch{list.innerHTML='<p class="panel-empty">Yorumlar şu an yüklenemedi.</p>';}}
document.getElementById("comment-form").addEventListener("submit",async event=>{event.preventDefault();if(!activeCommentPost)return;const input=document.getElementById("comment-text");const button=event.currentTarget.querySelector("button");button.disabled=true;try{const response=await fetch(`/api/gonderiler/${activeCommentPost.id}/yorumlar`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({metin:input.value})});const data=await response.json();if(!response.ok)throw new Error();input.value="";renderComments(data.yorumlar||[]);}finally{button.disabled=false;}});
let stories=[];let activeStoryIndex=0;
function renderStory(){const story=stories[activeStoryIndex];if(!story)return;document.getElementById("story-progress").innerHTML=stories.map((_,index)=>`<i class="${index<=activeStoryIndex?"active":""}"></i>`).join("");document.getElementById("story-content").innerHTML=`<img src="${story.media_path}" alt="${escapeText(story.name)} hikâyesi"><div class="story-user"><span style="background:${story.color}">${escapeText(story.initials)}</span><a href="/profil.html?u=${encodeURIComponent(story.user_id)}">${escapeText(story.name)}</a></div><p>${escapeText(story.caption)}</p>`;}
function openStory(index){if(index<0||index>=stories.length)return;activeStoryIndex=index;renderStory();const viewer=document.getElementById("story-viewer");viewer.classList.add("open");viewer.setAttribute("aria-hidden","false");}
function closeStory(){const viewer=document.getElementById("story-viewer");viewer.classList.remove("open");viewer.setAttribute("aria-hidden","true");}
async function setupStories(){try{stories=(await (await fetch("/api/hikayeler")).json()).hikayeler||[];document.querySelectorAll(".story[data-user]").forEach(button=>button.addEventListener("click",event=>{event.preventDefault();event.stopImmediatePropagation();const index=stories.findIndex(story=>story.user_id===button.dataset.user);if(index>=0)openStory(index);},true));}catch{}}
document.getElementById("story-close").addEventListener("click",closeStory);document.getElementById("story-previous").addEventListener("click",()=>openStory(Math.max(0,activeStoryIndex-1)));document.getElementById("story-next").addEventListener("click",()=>activeStoryIndex>=stories.length-1?closeStory():openStory(activeStoryIndex+1));document.getElementById("story-viewer").addEventListener("click",event=>{if(event.target.id==="story-viewer")closeStory();});
const intervention=document.createElement("aside");intervention.id="balance-intervention";intervention.hidden=true;intervention.innerHTML='<span>✦ AKIŞ DENGESİ</span><h2>Akış biraz yoğunlaştı.</h2><p>Benzer yoğun içeriklerde daha uzun kaldığını fark ettik. İstersen akışına daha çeşitli postlar ekleyelim.</p><div><button id="balance-feed" type="button">Akışı dengele</button><button id="dismiss-intervention" type="button">Boşver</button></div>';document.body.appendChild(intervention);
if(localAgent){const privacyButton=document.createElement("button");privacyButton.id="local-privacy-button";privacyButton.type="button";privacyButton.textContent="✦ Bu cihazda kişiselleştiriliyor";privacyButton.title="Yerel kişiselleştirme ayrıntıları";privacyButton.addEventListener("click",()=>openSheet());document.querySelector("#flow-status>div").appendChild(privacyButton);const localStyle=document.createElement("style");localStyle.textContent='.flow-status .local-privacy-button{display:block;width:auto;height:auto;border:0;background:transparent;color:#5d7350;font-size:10px;font-weight:800;line-height:1.25;padding:4px 0 0;text-decoration:underline;text-underline-offset:3px}.flow-status .local-privacy-button:focus-visible{outline:2px solid #719740;outline-offset:3px;border-radius:3px}';document.head.appendChild(localStyle);}
const demoButton=document.createElement("button");demoButton.type="button";demoButton.className="demo-scenario";demoButton.textContent="Demo akışını göster";demoButton.setAttribute("aria-label","Duygu katmanı demo akışını göster");demoButton.title="Demo akışını göster";document.querySelector("#flow-status>div").appendChild(demoButton);
if(localAgent)demoButton.addEventListener("click",async event=>{event.stopImmediatePropagation();demoButton.disabled=true;try{const allPosts=[...postCache.values()],negative=allPosts.filter(post=>Number(post.duygu)<-.15),posts=(negative.length?negative:allPosts).slice(0,10);for(let index=0;index<10;index+=1)await localAgent.recordInteraction({post:posts[index%Math.max(posts.length,1)],dwell:7.5,click:true,rocket:false,comment:false,exit:false});updateLocalAgent(await localAgent.summary());await firstLoad();}finally{demoButton.disabled=false;}},true);
const demoStyle=document.createElement("style");demoStyle.textContent='.demo-scenario{display:block;margin-top:8px;border:0;background:transparent;color:#56674a;padding:0;font-size:10px;font-weight:800;text-decoration:underline}.balance-intervention{position:fixed;z-index:60;left:50%;bottom:84px;width:min(560px,calc(100% - 28px));transform:translateX(-50%);border-radius:26px;background:#1a2019;color:white;padding:18px 19px;box-shadow:0 20px 60px rgba(0,0,0,.26)}.balance-intervention[hidden]{display:none}.balance-intervention>span{color:#c9ff62;font-size:9px;font-weight:850;letter-spacing:.1em}.balance-intervention h2{margin:7px 0 5px;font-size:19px}.balance-intervention p{margin:0;color:#c9d1c5;font-size:12px;line-height:1.45}.balance-intervention div{display:flex;gap:8px;margin-top:15px}.balance-intervention button{border:0;border-radius:999px;padding:9px 12px;font-size:11px;font-weight:800}.balance-intervention #balance-feed{background:#c9ff62;color:#121314}.balance-intervention #dismiss-intervention{background:transparent;color:white}';document.head.appendChild(demoStyle);
const demoCompactStyle=document.createElement("style");demoCompactStyle.textContent='.flow-status .demo-scenario{position:absolute;right:42px;top:13px;display:grid;place-items:center;width:27px;height:27px;margin:0;border-radius:50%;background:rgba(255,255,255,.75);font-size:0;text-decoration:none}.flow-status .demo-scenario::after{content:"▸";font-size:17px;line-height:1;color:#53624b}.flow-status .demo-scenario:disabled::after{content:"…";font-size:15px}';document.head.appendChild(demoCompactStyle);
const originalUpdateStatus=updateStatus;updateStatus=function(level){originalUpdateStatus(level);};
document.getElementById("dismiss-intervention").addEventListener("click",async()=>{intervention.hidden=true;await fetch("/api/mudahale/ertele",{method:"POST"});});document.getElementById("balance-feed").addEventListener("click",async()=>{intervention.hidden=true;await firstLoad();});demoButton.addEventListener("click",async()=>{demoButton.disabled=true;demoButton.textContent="Hazırlanıyor…";try{const response=await fetch("/api/demo-senaryo",{method:"POST"});const data=await response.json();updateStatus(data.spiral_seviyesi);updateDuyguKatmani(data.duygu_katmani);document.getElementById("flow-current-mood").textContent="Olası anlık ritim: Yoğun · demo senaryosu";document.getElementById("desktop-current-mood").textContent="Olası anlık ritim: Yoğun · demo senaryosu";}finally{demoButton.disabled=false;demoButton.textContent="Demo akışını göster";}});
setupStories();
if(localAgent){document.getElementById("sifirla-buton").textContent="Yerel verileri sil";document.querySelector(".flow-eyebrow").textContent="DUYGU KATMANI · YEREL";localAgent.init().then(localAgent.summary).then(updateLocalAgent).catch(error=>console.warn("Local agent unavailable",error));}
firstLoad();
