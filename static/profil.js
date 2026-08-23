const profileRoot=document.getElementById("profile-content");
const escapeProfile=value=>{const node=document.createElement("div");node.textContent=value;return node.innerHTML;};
const requestedId=new URLSearchParams(location.search).get("u")||"emiryusuf";
const fallbackUser=DEMO_USERS[requestedId]||DEMO_USERS.emiryusuf;
let following=false;

function renderProfile(user,posts){
  const topics=(fallbackUser.topics||[]).map(topic=>`<span>${escapeProfile(topic)}</span>`).join("");
  const ownProfile=user.id==="emiryusuf";
  profileRoot.innerHTML=`<section class="profile-hero"><div class="profile-avatar" style="--profile-color:${user.color}">${escapeProfile(user.initials)}</div><div class="profile-name-row"><div><h1>${escapeProfile(user.name)}</h1><p>${escapeProfile(user.handle)}</p></div>${ownProfile?"":"<button id=\"follow-button\" class=\"follow-button "+(following?"following":"")+"\" type=\"button\">"+(following?"Takiptesin":"Takip et")+"</button>"}</div><p class="profile-bio">${escapeProfile(user.bio)}</p><div class="profile-stats"><span><b>${user.post_count}</b> gönderi</span><span><b>${user.followers}</b> takipçi</span><span><b>${user.following}</b> takip</span></div><div class="profile-topics">${topics||"<span>NSosyal üyesi</span>"}</div></section><section class="profile-post-section"><div class="profile-section-title"><h2>Gönderiler</h2><span>${posts.length} görünüm</span></div><div class="profile-grid">${posts.map(post=>`<article class="profile-post"><img src="${postImage(post)}" alt="${escapeProfile(post.konu)} için temsili görsel" loading="lazy"><div><span>${escapeProfile(post.konu)}</span><p>${escapeProfile(post.metin)}</p></div></article>`).join("")||"<p class='profile-empty'>Bu profilde henüz gönderi yok.</p>"}</div></section>`;
  const button=document.getElementById("follow-button");
  if(button)button.addEventListener("click",async event=>{event.currentTarget.disabled=true;try{const response=await fetch(`/api/kullanicilar/${encodeURIComponent(requestedId)}/takip`,{method:"POST"});const data=await response.json();following=data.takipte;renderProfile(data.kullanici,posts);}finally{event.currentTarget.disabled=false;}});
}
async function loadProfile(){
  try{const response=await fetch(`/api/kullanicilar/${encodeURIComponent(requestedId)}`);if(!response.ok)throw new Error("Profil bulunamadı");const data=await response.json();following=data.kullanici.following_by_viewer;renderProfile(data.kullanici,data.gonderiler||[]);}catch{profileRoot.innerHTML='<div class="profile-empty">Profil şu an yüklenemedi.</div>';}}
document.getElementById("profile-more").addEventListener("click",()=>alert("Profil bildirimleri demo modunda açık."));
loadProfile();
