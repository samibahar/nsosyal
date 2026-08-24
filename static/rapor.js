// İçgörü: all figures are calculated from this browser's local interaction log.
const reactionLabels={begendim:["👍","Beğendim"],umutlandim:["✨","Umutlandım"],dusundum:["🤔","Düşündüm"],kizdim:["😠","Kızdım"],gerildim:["😣","Gerildim"]};
const topicLabels={gundem:"Gündem",teknoloji:"Teknoloji",bilim:"Bilim",spor:"Spor",sanat:"Kültür",saglik:"Yaşam",ekonomi:"Ekonomi",egitim:"Eğitim",oyun:"Oyun",seyahat:"Keşif"};
let allEvents=[],activeRange="week",trace=null;
const $=id=>document.getElementById(id);
function rangeStart(range){const now=Date.now();if(range==="today"){const d=new Date();d.setHours(0,0,0,0);return +d;}return now-(range==="month"?30:7)*86400000;}
function scopedEvents(){return allEvents.filter(event=>event.createdAt>=rangeStart(activeRange));}
function countBy(items,key){return items.reduce((result,item)=>{const value=key(item);if(value)result[value]=(result[value]||0)+1;return result;},{});}
function empty(target,message){target.innerHTML=`<p class="chart-empty">${message}</p>`;}
// Catmull-Rom -> kubik Bezier: noktalar arasinda yumusak bir egri ciker
// (duz polyline'in keskin/cirkin durmasi yerine).
function smoothPath(points){
  if(points.length<2)return `M${points[0][0]},${points[0][1]}`;
  let d=`M${points[0][0]},${points[0][1]}`;
  for(let i=0;i<points.length-1;i++){
    const p0=points[i===0?0:i-1],p1=points[i],p2=points[i+1],p3=points[i+2<points.length?i+2:i+1];
    const c1x=p1[0]+(p2[0]-p0[0])/6,c1y=p1[1]+(p2[1]-p0[1])/6;
    const c2x=p2[0]-(p3[0]-p1[0])/6,c2y=p2[1]-(p3[1]-p1[1])/6;
    d+=` C${c1x},${c1y} ${c2x},${c2y} ${p2[0]},${p2[1]}`;
  }
  return d;
}
function renderLine(events){const target=$("rhythm-chart"),interactions=events.filter(event=>event.type==="interaction");if(!interactions.length){empty(target,"Akışta biraz gezindiğinde, burada zaman içindeki etkileşim ritmin görünür.");$("rhythm-caption").textContent="Henüz veri yok";return;}
  const start=rangeStart(activeRange),end=Date.now(),buckets=Array.from({length:7},()=>0),span=Math.max(1,end-start);interactions.forEach(event=>buckets[Math.min(6,Math.floor((event.createdAt-start)/span*7))]++);
  // Tek bir zaman diliminde kumelenmis veri (orn. kisa bir demo oturumu),
  // 6 sifir + 1 ani sivri uctan olusan yanitici/cirkin bir grafik uretir --
  // veriyi uydurmak yerine, boyle durumlarda durustce "henuz yeterli zaman
  // yayilimi yok" mesaji gosteriyoruz (konu×kategori isi haritasinda da
  // aynen bu ilkeyi izledik).
  const nonEmptyBuckets=buckets.filter(count=>count>0).length;
  if(nonEmptyBuckets<=1){empty(target,"Etkileşimlerin şu ana kadar tek bir zaman diliminde kümelendi. Zamana yayıldıkça burada bir ritim görünecek.");$("rhythm-caption").textContent=`${interactions.length} etkileşim`;return;}
  const max=Math.max(1,...buckets),points=buckets.map((count,index)=>[8+index*46,104-(count/max)*76]);
  const linePath=smoothPath(points),areaPath=`${linePath} L284,104 L8,104 Z`;
  target.innerHTML=`<svg viewBox="0 0 292 112" preserveAspectRatio="none" aria-hidden="true"><path class="chart-grid" d="M8 104H284M8 66H284M8 28H284"/><path class="chart-area" d="${areaPath}"/><path class="chart-line" d="${linePath}"/>${points.map(([x,y])=>`<circle cx="${x}" cy="${y}" r="3"/>`).join("")}</svg>`;
  $("rhythm-caption").textContent=`${interactions.length} etkileşim`;
}
function renderTopics(events){const target=$("topic-chart"),values=countBy(events.filter(event=>event.type==="interaction"),event=>event.topic);const rows=Object.entries(values).sort((a,b)=>b[1]-a[1]).slice(0,4);if(!rows.length){empty(target,"Konu dağılımı henüz oluşmadı.");return;}const max=Math.max(...rows.map(([,count])=>count));target.innerHTML=rows.map(([topic,count])=>`<div class="topic-row"><span>${topicLabels[topic]||topic}</span><div><i style="width:${count/max*100}%"></i></div><b>${count}</b></div>`).join("");}
const KATEGORI_RENK={sakin:"#8fb3a8",mutluluk:"#adeb4b",umut:"#79c4e8",sinirli:"#f0bd76",anksiyete:"#f4868e"};
const KATEGORI_SIRA=["sakin","mutluluk","umut","sinirli","anksiyete"];
function renderHeatmap(events){
  const target=$("heatmap-chart");
  if(typeof window.TrainedModels==="undefined"){empty(target,"Model bu sayfada henüz yüklenmedi.");return;}
  const interactions=events.filter(event=>event.type==="interaction");
  if(interactions.length<5){empty(target,"Birkaç etkileşimden sonra burada konu × olası ritim örüntün görünecek.");return;}
  const sayim={};
  interactions.forEach(event=>{
    const tahmin=window.TrainedModels.psikolojikTahmin({duygu:event.tone,dwell_saniye:event.dwell,tiklama:event.click?1:0,roket:event.rocket?1:0,yorum:event.comment?1:0});
    sayim[event.topic]=sayim[event.topic]||{};
    sayim[event.topic][tahmin.kategori]=(sayim[event.topic][tahmin.kategori]||0)+1;
  });
  const konular=Object.entries(sayim).map(([topic,kats])=>[topic,Object.values(kats).reduce((a,b)=>a+b,0)]).sort((a,b)=>b[1]-a[1]).slice(0,6).map(([topic])=>topic);
  const max=Math.max(1,...konular.flatMap(topic=>KATEGORI_SIRA.map(kat=>sayim[topic][kat]||0)));
  target.innerHTML=`<div class="heatmap-row"><b></b>${KATEGORI_SIRA.map(kat=>`<span style="background:none;font-size:8px;color:var(--muted)">${kat.slice(0,4)}</span>`).join("")}</div>`+
    konular.map(topic=>`<div class="heatmap-row"><b>${topicLabels[topic]||topic}</b>${KATEGORI_SIRA.map(kat=>{const deger=sayim[topic][kat]||0;return `<span style="--heat-color:${KATEGORI_RENK[kat]};--heat:${deger/max}" title="${kat}: ${deger}">${deger||""}</span>`;}).join("")}</div>`).join("");
}
async function renderDogrulama(){
  const target=$("dogrulama-chart"),agent=window.LocalPersonalization;
  if(!agent){empty(target,"Yerel model bu sayfada yüklenmedi.");return;}
  const ozet=await agent.dogrulamaOzeti();
  if(!ozet.toplam){empty(target,"Ara sıra çıkan kısa onay sorusuna cevap verdikçe, tahminin gerçekle ne kadar örtüştüğü burada görünür.");return;}
  const yuzde=Math.round(ozet.eslesmeOrani*100);
  target.innerHTML=`<div><b>${ozet.toplam}</b><span>onay sorusu</span></div><div><b>%${yuzde}</b><span>tahmin eşleşti</span></div><div><b>${KATEGORI_SIRA.length}</b><span>olası kategori</span></div>`;
}
function renderReactions(events){const target=$("reaction-chart"),values=countBy(events.filter(event=>event.type==="post_reaction"||event.type==="news_reaction"),event=>event.reaction);const rows=Object.entries(values);if(!rows.length){empty(target,"Bir tepkini seçtiğinde burada görünür.");return;}target.innerHTML=rows.map(([reaction,count])=>`<div class="reaction-row"><span>${reactionLabels[reaction]?.[0]||"☺"}</span><b>${reactionLabels[reaction]?.[1]||reaction}</b><i>${count}</i></div>`).join("");}
function renderSummary(events){const interactions=events.filter(event=>event.type==="interaction"),reactions=events.filter(event=>event.type==="post_reaction"||event.type==="news_reaction");$("kpi-interactions").textContent=interactions.length;$("kpi-reactions").textContent=reactions.length;$("kpi-moved").textContent=trace?.movedCount??"—";
  if(!interactions.length){$("insight-status-title").textContent="Veri bekleniyor";$("insight-status-text").textContent="Etkileşimlerin yalnızca bu cihazda özetlenir.";return;}
  const topics=Object.entries(countBy(interactions,event=>event.topic)).sort((a,b)=>b[1]-a[1]);const top=topicLabels[topics[0]?.[0]]||"çeşitli konular";$("insight-status-title").textContent="Akış ritmin oluşuyor";$("insight-status-text").textContent=`Bu ${activeRange==="today"?"gün":activeRange==="week"?"hafta":"ay"} en çok ${top} içeriğiyle etkileştin. ${reactions.length?"Gönüllü tepkilerin sıralamayı yerelde günceller.":"İstersen tepki vererek akışı daha açık biçimde şekillendirebilirsin."}`;
}
// Uzmana götürülebilir, yorumsuz veri özeti -- haftalik_rapor.py'nin
// LLM tabanlı terapist-raporu özelliğinin yerini alır (o, yeni cihaz-içi
// mimaride artik erişilemiyor). LLM cagrisi YOK, tamamen bu cihazdaki
// IndexedDB kaydından hesaplanan yapılandırılmış bir metin -- local-first
// ilkesini bozmaz. Uçuncu sahis/notr dil, tavsiye yok, zorunlu sinirlilik notu.
async function terapistOzetiOlustur(){
  const interactions=allEvents.filter(event=>event.type==="interaction");
  if(!interactions.length) return "Henüz bu cihazda kaydedilmiş bir etkileşim yok. Özet, veri biriktikçe anlamlı olacaktır.";
  const tarihler=interactions.map(event=>event.createdAt).sort((a,b)=>a-b);
  const ilkTarih=new Date(tarihler[0]).toLocaleDateString("tr-TR"),sonTarih=new Date(tarihler.at(-1)).toLocaleDateString("tr-TR");
  const reactions=allEvents.filter(event=>event.type==="post_reaction"||event.type==="news_reaction");
  const konuSayim=countBy(interactions,event=>event.topic);
  const enCokKonular=Object.entries(konuSayim).sort((a,b)=>b[1]-a[1]).slice(0,3).map(([topic,count])=>`${topicLabels[topic]||topic} (${count})`).join(", ");
  let kategoriSayim={},konuKategoriSayim={};
  if(typeof window.TrainedModels!=="undefined"){
    interactions.forEach(event=>{
      const tahmin=window.TrainedModels.psikolojikTahmin({duygu:event.tone,dwell_saniye:event.dwell,tiklama:event.click?1:0,roket:event.rocket?1:0,yorum:event.comment?1:0});
      kategoriSayim[tahmin.kategori]=(kategoriSayim[tahmin.kategori]||0)+1;
      konuKategoriSayim[event.topic]=konuKategoriSayim[event.topic]||{};
      konuKategoriSayim[event.topic][tahmin.kategori]=(konuKategoriSayim[event.topic][tahmin.kategori]||0)+1;
    });
  }
  const kategoriSatirlari=KATEGORI_SIRA.map(kat=>`  - ${kat}: %${Math.round((kategoriSayim[kat]||0)/interactions.length*100)}`).join("\n");
  const negatifKonular=Object.entries(konuKategoriSayim)
    .map(([topic,kats])=>[topic,(kats.sinirli||0)+(kats.anksiyete||0)])
    .filter(([,toplam])=>toplam>0).sort((a,b)=>b[1]-a[1]).slice(0,3)
    .map(([topic])=>topicLabels[topic]||topic).join(", ")||"belirgin bir örüntü gözlenmedi";
  const dogrulama=window.LocalPersonalization?await window.LocalPersonalization.dogrulamaOzeti():{toplam:0};
  const dogrulamaSatiri=dogrulama.toplam?`  - Kullanıcı öz-bildirimiyle model tahmininin eşleşme oranı: %${Math.round(dogrulama.eslesmeOrani*100)} (${dogrulama.toplam} onay sorusu)`:"  - Henüz onay sorusu cevaplanmadı.";
  return [
    "VERİ ÖZETİ",
    `  - Kayıt aralığı: ${ilkTarih} - ${sonTarih}`,
    `  - Toplam etkileşim: ${interactions.length}`,
    `  - Gönüllü tepki sayısı: ${reactions.length}`,
    "",
    "GÖZLEMLENEN DAVRANIŞSAL ÖRÜNTÜLER",
    `  - En sık etkileşilen konular: ${enCokKonular}`,
    "  - Olası kategori dağılımı (davranışsal sinyalden türetilmiştir):",
    kategoriSatirlari,
    `  - "Sinirli"/"anksiyete" örüntüsüyle en çok ilişkilendirilen konular: ${negatifKonular}`,
    dogrulamaSatiri,
    "",
    "SINIRLILIKLAR",
    "  - Bu belge bir teşhis veya klinik değerlendirme değildir.",
    "  - Kategoriler; bakma süresi, tıklama ve tepki gibi davranışsal sinyallerden türetilmiş olası örüntülerdir, doğrudan bir duygu ölçümü değildir.",
    "  - Alttaki model sentetik senaryo verisiyle eğitilmiştir; gerçek klinik doğrulaması yoktur.",
    "  - Bu özet tek başına bir değerlendirme için yeterli değildir; nihai yorum uzmana aittir.",
  ].join("\n");
}
document.getElementById("terapist-ozet-buton")?.addEventListener("click",async event=>{
  const buton=event.currentTarget,alan=$("terapist-ozet-metin"),kopyala=$("terapist-ozet-kopyala");
  buton.disabled=true;buton.textContent="Oluşturuluyor…";
  alan.textContent=await terapistOzetiOlustur();
  alan.style.display="block";kopyala.style.display="inline-flex";
  buton.disabled=false;buton.textContent="Özeti yeniden oluştur";
});
document.getElementById("terapist-ozet-kopyala")?.addEventListener("click",async event=>{
  const buton=event.currentTarget;
  try{await navigator.clipboard.writeText($("terapist-ozet-metin").textContent);const eski=buton.textContent;buton.textContent="Kopyalandı ✓";setTimeout(()=>buton.textContent=eski,1500);}catch{}
});
function render(){const events=scopedEvents();renderSummary(events);renderLine(events);renderTopics(events);renderReactions(events);renderHeatmap(events);renderDogrulama();}
async function init(){const agent=window.LocalPersonalization;if(!agent)return;await agent.init();[allEvents,trace]=await Promise.all([agent.getLocalEvents(),agent.getDecisionTrace()]);render();}
document.querySelectorAll(".range-switch button").forEach(button=>button.addEventListener("click",()=>{activeRange=button.dataset.range;document.querySelectorAll(".range-switch button").forEach(item=>item.classList.toggle("active",item===button));render();}));
$("insight-detail-button").addEventListener("click",()=>$("real-insights").scrollIntoView({behavior:"smooth",block:"start"}));
init().catch(error=>console.warn("Local insight data unavailable",error));
