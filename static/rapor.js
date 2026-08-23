// İçgörü page: friendly summary first, inspectable live data second.
const COLORS={sakin:"#74cdb9",mutluluk:"#b493f3",umut:"#f5bd64",sinirli:"#f4868e",anksiyete:"#80aee9"};
function setSummary(total, distribution){
  const title=document.getElementById("insight-status-title"),text=document.getElementById("insight-status-text");
  const rhythm=document.getElementById("insight-rhythm-value"), rhythmNote=document.getElementById("insight-rhythm-note");
  const balance=document.getElementById("insight-balance-value"), balanceNote=document.getElementById("insight-balance-note");
  if(!total){title.textContent="Akış ritmi sakin";text.textContent="Bugün kendine ait bir ritim oluşuyor.";rhythm.textContent="Kendi hızında";rhythmNote.textContent="Henüz gözlem birikiyor";balance.textContent="Başlangıçta";balanceNote.textContent="Veri geldikçe netleşir";return;}
  const dominant=Object.entries(distribution).sort((a,b)=>b[1]-a[1])[0];
  title.textContent="Akışın takipte";text.textContent=`Bu oturumda ${total} etkileşimden nazik bir özet oluşturduk.`;
  rhythm.textContent=`${total} etkileşim`;rhythmNote.textContent="Bu oturumdan gözlemlendi";
  balance.textContent=dominant&&dominant[1]?"Ritim oluşuyor":"Dengeli";balanceNote.textContent="Kesin bir değerlendirme değildir";
}
function renderDistribution(data){
  const section=document.getElementById("canli-bolum");if(!data.toplam_etkilesim){section.style.display="none";setSummary(0,{});return;}
  section.style.display="block";document.getElementById("canli-toplam").textContent=data.toplam_etkilesim;setSummary(data.toplam_etkilesim,data.kategori_dagilimi);
  const target=document.getElementById("canli-dagilim");target.innerHTML=data.kategoriler.map(category=>{const count=data.kategori_dagilimi[category]||0;const pct=Math.round(count/data.toplam_etkilesim*100);return `<div class="distribution-row"><span>${category}</span><div><i style="width:${pct}%;background:${COLORS[category]||COLORS.sakin}"></i></div><b>%${pct}</b></div>`;}).join("");
  renderHeatmap(data);
}
function renderHeatmap(data){
  const holder=document.getElementById("isi-haritasi-kapsayici"),target=document.getElementById("isi-haritasi");if(!data.konular?.length){holder.style.display="none";return;}holder.style.display="block";
  const max=Math.max(1,...data.konular.flatMap(topic=>data.kategoriler.map(category=>data.konu_kategori_izgara[topic][category]||0)));
  target.innerHTML=`<div class="heatmap">${data.konular.map(topic=>`<div class="heatmap-row"><b>${topic}</b>${data.kategoriler.map(category=>{const value=data.konu_kategori_izgara[topic][category]||0;return `<span title="${category}: ${value}" style="--heat:${value/max};--heat-color:${COLORS[category]||COLORS.sakin}">${value||"·"}</span>`;}).join("")}</div>`).join("")}</div>`;
}
async function loadSession(){try{const response=await fetch("/api/psikolojik-ozet");renderDistribution(await response.json());}catch(error){console.warn("Insight session summary unavailable",error);}}
async function loadValidation(){try{const data=await (await fetch("/api/dogrulama-ozet")).json();const section=document.getElementById("dogrulama-ozet-bolum");if(!data.toplam_onay){section.style.display="none";return;}section.style.display="block";const rate=data.eslesme_orani===null?"—":`%${Math.round(data.eslesme_orani*100)}`;document.getElementById("dogrulama-ozet-icerik").innerHTML=`<div class="validation-grid"><div><b>${data.toplam_onay}</b><span>gönüllü yanıt</span></div><div><b>${data.eslesen}</b><span>uyumlu tahmin</span></div><div><b>${rate}</b><span>eşleşme</span></div></div>${data.toplam_onay<5?'<p class="data-note">Az sayıdaki yanıt, güvenilir bir oran anlamına gelmez.</p>':''}`;}catch(error){console.warn("Validation summary unavailable",error);}}
async function loadNote(){const section=document.getElementById("llm-rapor-bolum"),therapist=document.getElementById("terapist-rapor-bolum");try{const data=await (await fetch("/api/haftalik-rapor")).json();if(!data.mevcut){section.style.display="none";therapist.style.display="none";return;}section.style.display="block";therapist.style.display="block";document.getElementById("llm-rapor-icerik").textContent=data.metin;}catch{section.style.display="none";therapist.style.display="none";}}
async function generateDataSummary(){const button=document.getElementById("terapist-rapor-buton"),target=document.getElementById("terapist-rapor-icerik");button.disabled=true;target.textContent="Hazırlanıyor…";try{const data=await (await fetch("/api/terapist-raporu")).json();target.textContent=data.mevcut?data.metin:"Şu an hazırlanamıyor.";}catch{target.textContent="Şu an hazırlanamıyor.";}finally{button.disabled=false;}}
document.getElementById("terapist-rapor-buton").addEventListener("click",generateDataSummary);
document.querySelectorAll(".range-switch button").forEach(button=>button.addEventListener("click",()=>{document.querySelectorAll(".range-switch button").forEach(item=>item.classList.toggle("active",item===button));}));
function openLive(){document.getElementById("real-insights").scrollIntoView({behavior:"smooth",block:"start"});}
document.getElementById("insight-detail-button").addEventListener("click",openLive);document.getElementById("gentle-detail-button").addEventListener("click",openLive);
async function loadLocalDemo(){
  const agent=window.LocalPersonalization;if(!agent)return false;
  try{await agent.init();const trace=await agent.getDecisionTrace();if(!trace?.demo)return false;const summary=trace.summary||{};
    document.getElementById("insight-status-title").textContent="Jüri senaryosu tamamlandı";
    document.getElementById("insight-status-text").textContent="Hazır örnek sinyaller bu cihazda işlendi; akışın hareketini inceleyebilirsin.";
    document.getElementById("insight-rhythm-value").textContent=`${trace.movedCount} gönderi değişti`;
    document.getElementById("insight-rhythm-note").textContent="Aynı adaylar, yeni sıralama";
    document.getElementById("insight-balance-value").textContent=`%${Math.round((summary.intensity||0)*100)} yoğunluk`;
    document.getElementById("insight-balance-note").textContent="Örnek senaryo · teşhis değildir";
    return true;
  }catch{return false;}
}
(async()=>{if(await loadLocalDemo())return;loadSession();loadValidation();loadNote();})();
