// İçgörü: all figures are calculated from this browser's local interaction log.
const reactionLabels={begendim:["👍","Beğendim"],umutlandim:["✨","Umutlandım"],dusundum:["🤔","Düşündüm"],kizdim:["😠","Kızdım"],gerildim:["😣","Gerildim"]};
const topicLabels={gundem:"Gündem",teknoloji:"Teknoloji",bilim:"Bilim",spor:"Spor",sanat:"Kültür",saglik:"Yaşam",ekonomi:"Ekonomi",egitim:"Eğitim",oyun:"Oyun",seyahat:"Keşif"};
let allEvents=[],activeRange="week",trace=null,etiketModeli=null,seyirTum=[];
const $=id=>document.getElementById(id);
function rangeStart(range){const now=Date.now();if(range==="today"){const d=new Date();d.setHours(0,0,0,0);return +d;}return now-(range==="month"?30:7)*86400000;}
function scopedEvents(){return allEvents.filter(event=>event.createdAt>=rangeStart(activeRange));}
function countBy(items,key){return items.reduce((result,item)=>{const value=key(item);if(value)result[value]=(result[value]||0)+1;return result;},{});}
// Bos durum: onceden yalnizca duz bir <p> idi ve 132px'lik bos gri kutunun
// ortasinda "veri yok" yazisi urunun bozuk oldugu izlenimi veriyordu.
// Artik ikon + aciklama + (gerektiginde) yonlendirici bir eylem gosteriyor.
function empty(target,message,ikon="icgoru",eylem){
  const eylemHtml = eylem
    ? `<a class="bos-durum-eylem" href="${eylem.href}">${eylem.metin} <svg class="ikon ikon-sm" aria-hidden="true"><use href="#i-ok-sag"/></svg></a>`
    : "";
  target.innerHTML=`<div class="bos-durum"><svg class="ikon" aria-hidden="true"><use href="#i-${ikon}"/></svg><p>${message}</p>${eylemHtml}</div>`;
}
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
// Grafik cizildiginde kutu role="img" tasir; bos durumda icine tiklanabilir
// bir baglanti konuldugu icin rol kaldirilir (resim rolu etkilesimli oge
// iceremez; axe: nested-interactive).
function renderLine(events){const target=$("rhythm-chart"),interactions=events.filter(event=>event.type==="interaction");target.removeAttribute("role");if(!interactions.length){empty(target,"Akışta biraz gezindiğinde, zaman içindeki etkileşim ritmin burada belirir.","icgoru",{href:"/index.html?demo=1",metin:"Örnek senaryoyu çalıştır"});$("rhythm-caption").textContent="Henüz veri yok";return;}
  const start=rangeStart(activeRange),end=Date.now(),buckets=Array.from({length:7},()=>0),span=Math.max(1,end-start);interactions.forEach(event=>buckets[Math.min(6,Math.floor((event.createdAt-start)/span*7))]++);
  // Tek bir zaman diliminde kumelenmis veri (orn. kisa bir demo oturumu),
  // 6 sifir + 1 ani sivri uctan olusan yanitici/cirkin bir grafik uretir --
  // veriyi uydurmak yerine, boyle durumlarda durustce "henuz yeterli zaman
  // yayilimi yok" mesaji gosteriyoruz (konu×kategori isi haritasinda da
  // aynen bu ilkeyi izledik).
  const nonEmptyBuckets=buckets.filter(count=>count>0).length;
  if(nonEmptyBuckets<=1){empty(target,"Etkileşimlerin tek bir zaman diliminde kümelendi. Zamana yayıldıkça burada bir ritim çizilir.","icgoru");$("rhythm-caption").textContent=`${interactions.length} etkileşim`;return;}
  const max=Math.max(1,...buckets),points=buckets.map((count,index)=>[8+index*46,104-(count/max)*76]);
  const linePath=smoothPath(points),areaPath=`${linePath} L284,104 L8,104 Z`;
  target.setAttribute("role","img");
  target.innerHTML=`<svg viewBox="0 0 292 112" preserveAspectRatio="none" aria-hidden="true"><path class="chart-grid" d="M8 104H284M8 66H284M8 28H284"/><path class="chart-area" d="${areaPath}"/><path class="chart-line" d="${linePath}"/>${points.map(([x,y])=>`<circle cx="${x}" cy="${y}" r="3"/>`).join("")}</svg>`;
  $("rhythm-caption").textContent=`${interactions.length} etkileşim`;
}
function renderTopics(events){const target=$("topic-chart"),values=countBy(events.filter(event=>event.type==="interaction"),event=>event.topic);const rows=Object.entries(values).sort((a,b)=>b[1]-a[1]).slice(0,4);if(!rows.length){empty(target,"Konu dağılımı henüz oluşmadı.");return;}const max=Math.max(...rows.map(([,count])=>count));target.innerHTML=rows.map(([topic,count])=>`<div class="topic-row"><span>${topicLabels[topic]||topic}</span><div><i style="width:${count/max*100}%"></i></div><b>${count}</b></div>`).join("");}
const KATEGORI_RENK={sakin:"#8fb3a8",mutluluk:"#adeb4b",umut:"#79c4e8",sinirli:"#f0bd76",anksiyete:"#f4868e"};
const KATEGORI_SIRA=["sakin","mutluluk","umut","sinirli","anksiyete"];
const TEPKI_YONU={begendim:"olumlu",umutlandim:"olumlu",dusundum:"notr",kizdim:"olumsuz",gerildim:"olumsuz"};
const CEVAP_ADI={sakin:"Sakin",mutluluk:"Mutluluk",umut:"Umut",sinirli:"Sinirli",anksiyete:"Yoğun"};
const OLUMSUZ_CEVAP=new Set(["sinirli","anksiyete"]);
const yz=x=>`%${Math.round(x*100)}`;
// Unutulmuş açık bir sekme toplamı domine etmesin diye süre 60 sn'de kesilir (günlük özetle aynı).
const sure=event=>Math.min(Math.max(Number(event.dwell)||0,0),60);
// Kullanım süresi ana sayfadaki "Kullanım" kartıyla aynı hesaptan gelir (LocalPersonalization.kullanimOzeti).
const sureMetni=saniye=>{const dk=Math.round(saniye/60);if(dk<1)return "1 dk'dan az";return dk<60?`${dk} dk`:`${Math.floor(dk/60)} sa${dk%60?` ${dk%60} dk`:""}`;};
// Olası ruh hali seyri: her etkileşim anında son 30 dakikanın birleşik tahmini
// (trained-models.js ruhHaliSeyri). Tek gönderi sayılmaz; raporlarda her an
// o sırada geçen süreyle ağırlıklandırılır: 2 sn göz atmak ile 1 dk okumak
// aynı ağırlıkta değildir.
function ruhHaliSeyriHesapla(interactions){
  if(typeof window.TrainedModels==="undefined"||!window.TrainedModels.ruhHaliSeyri)return [];
  const olaylar=interactions.map(event=>({zaman:event.createdAt/1000,event,ozellik:{duygu:event.tone,dwell_saniye:event.dwell,tiklama:event.click?1:0,roket:event.rocket?1:0,yorum:event.comment?1:0}}));
  return window.TrainedModels.ruhHaliSeyri(olaylar,etiketModeli).map(({olay,durum})=>({event:olay.event,durum}));
}
function scopedSeyir(){const bas=rangeStart(activeRange);return seyirTum.filter(adim=>adim.event.createdAt>=bas);}
// Süre ağırlıklı dağılım. belirsizPay: pencerede yeterli kanıt olmayan anların süre payı.
function ruhHaliDagilimi(seyir){
  const top=Object.fromEntries(KATEGORI_SIRA.map(k=>[k,0]));let kanitli=0,toplam=0;
  seyir.forEach(({event,durum})=>{const s=sure(event);toplam+=s;if(!durum)return;kanitli+=s;KATEGORI_SIRA.forEach(k=>{top[k]+=s*durum.olasiliklar[k];});});
  return {olasiliklar:Object.fromEntries(KATEGORI_SIRA.map(k=>[k,kanitli?top[k]/kanitli:0])),belirsizPay:toplam?1-kanitli/toplam:1,toplamSure:toplam,kanitliSure:kanitli};
}
function dagilimMetni(d){
  if(!d.kanitliSure)return "yeterli kanıt yok";
  return KATEGORI_SIRA.map(k=>`${CEVAP_ADI[k].toLocaleLowerCase("tr-TR")} ${yz(d.olasiliklar[k])}`).join(" · ")+(d.belirsizPay>=.005?` (yeterli kanıt olmayan süre: ${yz(d.belirsizPay)})`:"");
}
// Gönüllü tepkilerin yönü. Olumsuz tepkinin yoğun tonlu içeriğe mi (habere
// verilen beklenen tepki) yoksa olumlu/nötr içeriğe mi verildiği ayrıca sayılır.
function tepkiDengesi(reactions){
  const d={olumlu:0,notr:0,olumsuz:0,olumsuzYogunIcerik:0};
  reactions.forEach(event=>{const yon=TEPKI_YONU[event.reaction];if(!yon)return;d[yon]++;if(yon==="olumsuz"&&Number(event.tone)<-0.2)d.olumsuzYogunIcerik++;});
  return d;
}
function sayimMetni(sayim,adlar){const satirlar=Object.entries(sayim).sort((a,b)=>b[1]-a[1]);return satirlar.length?satirlar.map(([k,v])=>`${adlar[k]||k} ${v}`).join(" · "):"yok";}
function renderHeatmap(){
  const target=$("heatmap-chart");
  if(typeof window.TrainedModels==="undefined"){empty(target,"Model bu sayfada henüz yüklenmedi.");return;}
  const seyir=scopedSeyir().filter(adim=>adim.durum);
  if(seyir.length<5){empty(target,"Birkaç etkileşim daha sonra konu × olası ritim örüntün burada görünür.","veri");return;}
  // Her hücre: o konudaki gönderilerde geçen sürenin hangi olası ritimde geçtiği.
  const konuSure={},sayim={};
  seyir.forEach(({event,durum})=>{const s=sure(event);konuSure[event.topic]=(konuSure[event.topic]||0)+s;sayim[event.topic]=sayim[event.topic]||{};KATEGORI_SIRA.forEach(kat=>{sayim[event.topic][kat]=(sayim[event.topic][kat]||0)+s*durum.olasiliklar[kat];});});
  const konular=Object.entries(konuSure).sort((a,b)=>b[1]-a[1]).slice(0,6).map(([topic])=>topic);
  konular.forEach(topic=>KATEGORI_SIRA.forEach(kat=>{sayim[topic][kat]/=konuSure[topic]||1;}));
  const max=Math.max(.01,...konular.flatMap(topic=>KATEGORI_SIRA.map(kat=>sayim[topic][kat])));
  target.innerHTML=`<div class="heatmap-row"><b></b>${KATEGORI_SIRA.map(kat=>`<span style="background:none;font-size:8px;color:var(--muted)">${kat.slice(0,4)}</span>`).join("")}</div>`+
    konular.map(topic=>`<div class="heatmap-row"><b>${topicLabels[topic]||topic}</b>${KATEGORI_SIRA.map(kat=>{const pay=sayim[topic][kat]||0;return `<span style="--heat-color:${KATEGORI_RENK[kat]};--heat:${pay/max}" title="${kat}: ${yz(pay)}">${pay>=.05?Math.round(pay*100):""}</span>`;}).join("")}</div>`).join("")+
    `<p class="dogrulama-not">Sayılar, o konudaki gönderilerde geçen sürenin yüzde kaçının hangi olası ritimde geçtiğidir. Ritim tek gönderiden değil, son 30 dakikadaki etkileşimlerin birleşik tahmininden gelir.</p>`;
}
// Eslesme orani tek basina anlamsiz olabilir: iki taban cizgisiyle yan yana
// gosterilir. Model "hep en sik cevabi soyle" tahmininden iyi degilse bu
// acikca yazilir.
async function renderDogrulama(){
  const target=$("dogrulama-chart"),not=$("dogrulama-not"),agent=window.LocalPersonalization;
  not.textContent="";
  if(!agent){empty(target,"Yerel model bu sayfada yüklenmedi.");return;}
  const ozet=await agent.dogrulamaOzeti();
  if(!ozet.toplam){empty(target,"Ara sıra çıkan kısa onay sorusunu yanıtladıkça, tahminin gerçekle ne kadar örtüştüğü burada ölçülür.","tepki");return;}
  const y=oran=>`%${Math.round(oran*100)}`;
  target.innerHTML=`<div><b>${y(ozet.eslesmeOrani)}</b><span>tahmin eşleşti · ${ozet.toplam} cevap</span></div><div><b>${y(ozet.cogunlukOrani)}</b><span>"hep en sık cevap" tabanı</span></div><div><b>${y(ozet.rastgeleOrani)}</b><span>rastgele tahmin</span></div>`;
  const kiyas=ozet.toplam<5?`Henüz ${ozet.toplam} cevap var; karşılaştırma için en az 5 cevap gerekiyor.`:ozet.eslesmeOrani>ozet.cogunlukOrani?"Model şu an iki taban çizgisini de geçiyor.":"Model henüz \"hep en sık cevabı söyle\" tahmininden iyi değil; bu dürüstçe gösterilir.";
  const kisisel=ozet.kisiselOrani!==null&&ozet.kisiselOrani!==undefined?` Kişisel uyarlama: ${y(ozet.kisiselOrani)} (${ozet.kisiselSayisi} cevap; her cevap önce tahmin edildi, sonra öğrenildi). Varsayılan model: ${y(ozet.varsayilanOrani)}.`:"";
  not.textContent=kiyas+kisisel+await spiralDogrulamaMetni(agent,y);
}
// Spiral tahmini (sentetik veriyle eğitildi) ile öz-bildirimin uyumu ve
// kişisel kalibrasyonun akışa bağlanıp bağlanmadığı.
async function spiralDogrulamaMetni(agent,y){
  const s=await agent.spiralDogrulamaOzeti();
  if(!s.toplam)return "";
  let metin=` Spiral tahmini ile cevapların uyumu: ${y(s.varsayilanUyum)} (${s.toplam} cevap; "hep en sık cevap" tabanı ${y(s.cogunlukUyum)}).`;
  const b=x=>x.toFixed(2).replace(".",",");
  if(s.kisiselSayisi)metin+=s.etkin?` Kişisel kalibrasyon aynı cevaplarda daha az hata yaptığı için dengelemeye bağlandı (uyum ${y(s.kisiselUyum)}; Brier hatası ${b(s.kisiselBrier)}, varsayılan ${b(s.ayniVarsayilanBrier)}).`:` Kişisel kalibrasyon henüz dengelemeye bağlı değil: en az ${s.esik} cevapta varsayılandan daha az hata yapması gerekiyor (şu an ${s.kisiselSayisi} cevap).`;
  return metin;
}
function renderReactions(events){
  const target=$("reaction-chart"),tepkiler=events.filter(event=>event.type==="post_reaction"||event.type==="news_reaction"),values=countBy(tepkiler,event=>event.reaction);const rows=Object.entries(values);
  if(!rows.length){empty(target,"Bir gönderiye tepki verdiğinde seçimlerin burada toplanır.","tepki");return;}
  const d=tepkiDengesi(tepkiler),etkilesim=events.filter(event=>event.type==="interaction").length;
  target.innerHTML=rows.map(([reaction,count])=>`<div class="reaction-row"><span>${reactionLabels[reaction]?.[0]||"☺"}</span><b>${reactionLabels[reaction]?.[1]||reaction}</b><i>${count}</i></div>`).join("")+
    `<p class="dogrulama-not">${d.olumlu} olumlu · ${d.notr} düşündüm · ${d.olumsuz} olumsuz${etkilesim?` · 100 etkileşimde ${Math.round(tepkiler.length/etkilesim*100)} tepki`:""}${d.olumsuz?`. Yoğun tonlu içeriğe verilen olumsuz tepki: ${d.olumsuzYogunIcerik}/${d.olumsuz}.`:""}</p>`;
}
function renderSummary(events){const interactions=events.filter(event=>event.type==="interaction"),reactions=events.filter(event=>event.type==="post_reaction"||event.type==="news_reaction");$("kpi-interactions").textContent=interactions.length;$("kpi-reactions").textContent=reactions.length;const hareket=trace?.movedCount;$("kpi-moved").textContent=hareket??"—";const hareketAlt=document.querySelector("#kpi-moved + span");if(hareketAlt)hareketAlt.textContent=hareket==null?"demo çalışmadı":"son demo";
  const kullanim=window.LocalPersonalization?.kullanimOzeti?.(events);if(kullanim){$("kpi-sure").textContent=kullanim.toplam.oturum?sureMetni(kullanim.toplam.sureSn):"—";$("kpi-sure-alt").textContent=`${kullanim.toplam.gonderi} gönderi · ${kullanim.toplam.oturum} oturum`;}
  if(!interactions.length){$("insight-status-title").textContent="Veri bekleniyor";$("insight-status-text").textContent="Etkileşimlerin yalnızca bu cihazda özetlenir.";return;}
  const topics=Object.entries(countBy(interactions,event=>event.topic)).sort((a,b)=>b[1]-a[1]);const top=topicLabels[topics[0]?.[0]]||"çeşitli konular";$("insight-status-title").textContent="Akış ritmin oluşuyor";$("insight-status-text").textContent=`Bu ${activeRange==="today"?"gün":activeRange==="week"?"hafta":"ay"} en çok ${top} içeriğiyle etkileştin. ${reactions.length?"Gönüllü tepkilerin sıralamayı yerelde günceller.":"İstersen tepki vererek akışı daha açık biçimde şekillendirebilirsin."}`;
}
// Uzmana götürülebilir, yorumsuz veri özeti -- haftalik_rapor.py'nin
// LLM tabanlı terapist-raporu özelliğinin yerini alır (o, yeni cihaz-içi
// mimaride artik erişilemiyor). LLM cagrisi YOK, tamamen bu cihazdaki
// IndexedDB kaydından hesaplanan yapılandırılmış bir metin -- local-first
// ilkesini bozmaz. Uçuncu sahis/notr dil, tavsiye yok, zorunlu sinirlilik notu.
// Zaman boyutu: cihazdaki kayıt (en fazla 12 hafta) hafta hafta özetlenir.
// En güvenilir veri kişinin kendi bildirimleri olduğu için tarih ve saatiyle
// ayrı bir bölümde, model tahminlerinden önce verilir.
const GUN_ADI=["Paz","Pzt","Sal","Çar","Per","Cum","Cmt"];
const GUN_DILIMI=[["Gece (00–06)",0,6],["Sabah (06–12)",6,12],["Öğleden sonra (12–18)",12,18],["Akşam (18–24)",18,24]];
const kisaTarih=zaman=>{const d=new Date(zaman);return `${String(d.getDate()).padStart(2,"0")}.${String(d.getMonth()+1).padStart(2,"0")}`;};
async function terapistOzetiOlustur(){
  const interactions=allEvents.filter(event=>event.type==="interaction");
  if(!interactions.length) return "Henüz bu cihazda kaydedilmiş bir etkileşim yok. Özet, veri biriktikçe anlamlı olacaktır.";
  const reactions=allEvents.filter(event=>event.type==="post_reaction"||event.type==="news_reaction");
  const checkins=allEvents.filter(event=>event.type==="checkin"&&event.value);
  const ilkTarih=new Date(interactions[0].createdAt).toLocaleDateString("tr-TR"),sonTarih=new Date(interactions.at(-1).createdAt).toLocaleDateString("tr-TR");
  const toplamDk=Math.round(interactions.reduce((a,event)=>a+sure(event),0)/60);
  const enCokKonular=Object.entries(countBy(interactions,event=>event.topic)).sort((a,b)=>b[1]-a[1]).slice(0,3).map(([topic,count])=>`${topicLabels[topic]||topic} (${count})`).join(", ");

  const saat=zaman=>{const d=new Date(zaman);return `${String(d.getHours()).padStart(2,"0")}:${String(d.getMinutes()).padStart(2,"0")}`;};
  const bildirimSatirlari=checkins.slice(-30).map(event=>`    ${new Date(event.createdAt).toLocaleDateString("tr-TR")} ${GUN_ADI[new Date(event.createdAt).getDay()]} ${saat(event.createdAt)} — ${CEVAP_ADI[event.value]||event.value}`);
  const dilimSatiri=GUN_DILIMI.map(([ad,bas,son])=>{const icinde=checkins.filter(event=>{const s=new Date(event.createdAt).getHours();return s>=bas&&s<son;});return icinde.length?`${ad} ${icinde.length} (${icinde.filter(event=>OLUMSUZ_CEVAP.has(event.value)).length} sinirli/yoğun)`:null;}).filter(Boolean).join(" · ");

  const haftaSatirlari=[];
  for(let h=0;h<12;h++){
    const bitis=Date.now()-h*7*86400000,bas=bitis-7*86400000,icinde=event=>event.createdAt>=bas&&event.createdAt<bitis;
    const seyir=seyirTum.filter(adim=>icinde(adim.event)),haftaCevap=checkins.filter(icinde);
    if(!seyir.length&&!haftaCevap.length)continue;
    const d=ruhHaliDagilimi(seyir),t=tepkiDengesi(reactions.filter(icinde));
    haftaSatirlari.push(`  ${kisaTarih(bas)}–${kisaTarih(bitis-1)}: ${seyir.length} etkileşim, yaklaşık ${Math.round(d.toplamSure/60)} dk`,
      `    Kendi bildirimleri: ${sayimMetni(countBy(haftaCevap,event=>event.value),CEVAP_ADI)}`,
      `    Gönüllü tepkiler: ${t.olumlu} olumlu · ${t.notr} düşündüm · ${t.olumsuz} olumsuz`,
      `    Olası ritim (süreye göre): ${dagilimMetni(d)}`);
  }

  const t=tepkiDengesi(reactions);
  const tepkiSatirlari=reactions.length?[
    `  - ${t.olumlu} olumlu (beğendim, umutlandım) · ${t.notr} düşündüm · ${t.olumsuz} olumsuz (kızdım, gerildim)`,
    `  - 100 etkileşim başına ${Math.round(reactions.length/interactions.length*100)} tepki`,
    t.olumsuz?`  - Olumsuz tepkilerin ${t.olumsuzYogunIcerik}/${t.olumsuz} tanesi yoğun tonlu içeriğe, kalanı olumlu ya da nötr tonlu içeriğe verildi.`:null,
  ].filter(Boolean):["  - Gönüllü tepki verilmedi."];

  const genel=ruhHaliDagilimi(seyirTum),konuSure={},konuOlumsuz={};
  seyirTum.forEach(({event,durum})=>{if(!durum)return;const s=sure(event);konuSure[event.topic]=(konuSure[event.topic]||0)+s;konuOlumsuz[event.topic]=(konuOlumsuz[event.topic]||0)+s*(durum.olasiliklar.sinirli+durum.olasiliklar.anksiyete);});
  const negatifKonular=Object.keys(konuSure).filter(topic=>konuSure[topic]>=60).map(topic=>[topic,konuOlumsuz[topic]/konuSure[topic]]).sort((a,b)=>b[1]-a[1]).slice(0,3).map(([topic,pay])=>`${topicLabels[topic]||topic} ${yz(pay)}`).join(", ")||"karşılaştırma için yeterli süre yok";
  // Eşleşme, özetin kapsadığı cevaplardan hesaplanır (her cevapta modelin önceden kaydettiği tahmin).
  // Önceden cihazdaki toplam sayaç kullanılıyordu; jüri demosu olay kaydını sıfırladığı için
  // "0 cevap" ile "6 onay sorusu" aynı özette yan yana çıkabiliyordu.
  const olculen=checkins.filter(event=>typeof event.eslesme==="boolean");
  const dogrulamaSatiri=olculen.length?`  - Kendi bildirimleriyle modelin önceden kaydedilen tahmininin eşleşme oranı: %${Math.round(olculen.filter(event=>event.eslesme).length/olculen.length*100)} (${olculen.length} cevap; rastgele tahmin %20)`:"  - Model tahmini ile kendi bildirimler henüz karşılaştırılmadı.";
  return [
    "VERİ ÖZETİ",
    `  - Kayıt aralığı: ${ilkTarih} - ${sonTarih} (bu cihaz en fazla 12 hafta saklar)`,
    `  - Toplam etkileşim: ${interactions.length} · toplam gezinme süresi yaklaşık ${toplamDk} dk`,
    `  - Gönüllü tepki: ${reactions.length} · kontrol sorusu cevabı: ${checkins.length}`,
    "",
    "KİŞİNİN KENDİ BİLDİRİMLERİ (\"Şu an nasıl hissediyorsun?\" cevapları)",
    ...(checkins.length?[
      `  - Dağılım: ${sayimMetni(countBy(checkins,event=>event.value),CEVAP_ADI)}`,
      `  - Günün saatine göre: ${dilimSatiri}`,
      `  - Son ${bildirimSatirlari.length} bildirim:`,
      ...bildirimSatirlari,
    ]:["  - Henüz kontrol sorusu cevaplanmadı."]),
    "",
    "HAFTALIK SEYİR (en yeni hafta üstte)",
    ...(haftaSatirlari.length?haftaSatirlari:["  - Veri yok."]),
    "",
    "GÖNÜLLÜ TEPKİLER (tüm dönem)",
    ...tepkiSatirlari,
    "",
    "GÖZLEMLENEN DAVRANIŞSAL ÖRÜNTÜLER",
    `  - En sık etkileşilen konular: ${enCokKonular}`,
    `  - Olası ritim dağılımı (süreye göre, davranışsal sinyalden türetilmiştir): ${dagilimMetni(genel)}`,
    `  - Sürenin en büyük payı "sinirli"/"yoğun" olası ritimde geçen konular (en az 1 dk): ${negatifKonular}`,
    dogrulamaSatiri,
    "",
    "SINIRLILIKLAR",
    "  - Bu belge bir teşhis veya klinik değerlendirme değildir.",
    "  - Olası ritim tek bir gönderiden değil, son 30 dakikadaki etkileşimlerin birleşik tahmininden hesaplanır ve o sırada geçen süreyle ağırlıklandırılır. Yine de davranıştan türetilmiş bir tahmindir, doğrudan bir duygu ölçümü değildir.",
    "  - Alttaki model sentetik senaryo verisiyle eğitilmiştir; gerçek klinik doğrulaması yoktur. Kişinin kendi bildirimleri model tahminlerinden daha güvenilirdir.",
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
function render(){const events=scopedEvents();renderSummary(events);renderLine(events);renderTopics(events);renderReactions(events);renderHeatmap();renderDogrulama();}
async function init(){const agent=window.LocalPersonalization;if(!agent)return;await agent.init();[allEvents,trace,etiketModeli]=await Promise.all([agent.getLocalEvents(),agent.getDecisionTrace(),agent.etiketModeli()]);seyirTum=ruhHaliSeyriHesapla(allEvents.filter(event=>event.type==="interaction"));render();}
document.querySelectorAll(".range-switch button").forEach(button=>button.addEventListener("click",()=>{activeRange=button.dataset.range;document.querySelectorAll(".range-switch button").forEach(item=>item.classList.toggle("active",item===button));render();}));
$("insight-detail-button").addEventListener("click",()=>$("real-insights").scrollIntoView({behavior:"smooth",block:"start"}));
init().catch(error=>console.warn("Local insight data unavailable",error));
