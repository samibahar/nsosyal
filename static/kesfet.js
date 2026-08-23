const topicStyles={spor:["⚽","linear-gradient(145deg,#9dce68,#356b49)","#315f42"],gundem:["◎","linear-gradient(145deg,#f3b66e,#a96f40)","#79513d"],teknoloji:["⌁","linear-gradient(145deg,#7fc8ec,#416ba2)","#335b8b"],bilim:["✺","linear-gradient(145deg,#c0a9ed,#625996)","#514882"],saglik:["◌","linear-gradient(145deg,#a7dcc8,#528d7e)","#397566"],ekonomi:["↗","linear-gradient(145deg,#f1cf7d,#a68036)","#826436"],sanat:["♫","linear-gradient(145deg,#ecad9f,#ae6075)","#8e455d"],egitim:["⌂","linear-gradient(145deg,#bddd99,#5d8850)","#4e7440"],oyun:["◈","linear-gradient(145deg,#cb9eef,#7654a0)","#593b86"],seyahat:["⌁","linear-gradient(145deg,#7ecbc7,#367d82)","#2e6873"]};
let posts=[];let activeTopic="all";let query="";
const grid=document.getElementById("explore-grid");
const safe=value=>{const node=document.createElement("div");node.textContent=value;return node.innerHTML;};
function styleFor(topic){return topicStyles[topic]||["✦","linear-gradient(145deg,#b7d9a9,#66885d)","#52734e"]}
function visiblePosts(){return posts.filter(post=>(activeTopic==="all"||post.konu===activeTopic)&&post.metin.toLocaleLowerCase("tr").includes(query.toLocaleLowerCase("tr")));}
function card(post,index){const [glyph,background,shape]=styleFor(post.konu);const variant=index%7===0?" feature":index%5===0?" tall":"";return `<button class="explore-card${variant}" data-id="${post.id}" style="--explore-bg:${background};--explore-shape:${shape}"><span class="explore-glyph">${glyph}</span><span class="explore-topic">${safe(post.konu)}</span><span class="explore-card-text">${safe(post.metin)}</span><span class="explore-card-meta">${index%3===0?"▶  Keşfet":"✦  Senin için"}</span></button>`;}
function render(){const items=visiblePosts();grid.innerHTML=items.length?items.map(card).join(""):'<div class="explore-empty"><span>⌕</span><b>Burada henüz bir şey yok</b><p>Başka bir konu ya da arama deneyebilirsin.</p></div>';grid.querySelectorAll(".explore-card").forEach(button=>button.addEventListener("click",()=>openPost(posts.find(post=>post.id===Number(button.dataset.id)))));}
function openPost(post){if(!post)return;const [glyph,background]=styleFor(post.konu);document.getElementById("explore-modal-content").innerHTML=`<div class="modal-visual" style="background:${background}"><span>${glyph}</span></div><span class="eyebrow">${safe(post.konu)} · KEŞFET</span><h2>${safe(post.metin)}</h2><p>Bu içerik ilgi alanların ve akışındaki çeşitlilik için seçildi.</p><div class="modal-actions"><button type="button">♡ Beğen</button><button type="button">↗ Paylaş</button><a href="/index.html">Akışa dön →</a></div>`;const modal=document.getElementById("explore-modal");modal.classList.add("open");modal.setAttribute("aria-hidden","false");}
function closeModal(){const modal=document.getElementById("explore-modal");modal.classList.remove("open");modal.setAttribute("aria-hidden","true");}
async function load(){grid.innerHTML='<div class="loading-state">Keşif hazırlanıyor…</div>';try{const response=await fetch("/api/kesfet");posts=(await response.json()).gonderiler;posts.sort(()=>Math.random()-.5);render();}catch{grid.innerHTML='<div class="explore-empty"><b>Keşif şu an yüklenemedi.</b><p>Bağlantıyı kontrol edip tekrar dene.</p></div>';}}
document.getElementById("explore-chips").addEventListener("click",event=>{const button=event.target.closest("button[data-topic]");if(!button)return;activeTopic=button.dataset.topic;document.querySelectorAll("#explore-chips button").forEach(item=>item.classList.toggle("active",item===button));render();});
document.getElementById("explore-search").addEventListener("input",event=>{query=event.target.value;render();});
document.getElementById("explore-search-clear").addEventListener("click",()=>{const input=document.getElementById("explore-search");input.value="";query="";input.focus();render();});
document.getElementById("explore-search-button").addEventListener("click",()=>document.getElementById("explore-search").focus());document.getElementById("explore-refresh").addEventListener("click",load);document.getElementById("explore-modal-close").addEventListener("click",closeModal);document.getElementById("explore-modal").addEventListener("click",event=>{if(event.target.id==="explore-modal")closeModal();});
load();

// Keep the Explore layout image-led while the captions remain the only text
// evaluated by the sentiment and feed-ranking layers.
const baseExploreRender=render;
render=function(){
  baseExploreRender();
  grid.querySelectorAll(".explore-card").forEach(button=>{
    const post=posts.find(item=>item.id===Number(button.dataset.id));
    if(post)button.insertAdjacentHTML("afterbegin",`<img class="explore-photo" src="${postImage(post)}" alt="${safe(post.konu)} iÃ§eriÄŸi iÃ§in temsili gÃ¶rsel" loading="lazy">`);
  });
};
const baseOpenExplorePost=openPost;
openPost=function(post){
  baseOpenExplorePost(post);
  const visual=document.querySelector("#explore-modal-content .modal-visual");
  if(visual)visual.innerHTML=`<img src="${postImage(post)}" alt="${safe(post.konu)} iÃ§eriÄŸi iÃ§in temsili gÃ¶rsel">`;
};
