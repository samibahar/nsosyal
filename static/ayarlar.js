// Ayarlar: tüm seçimler ve özetler bu tarayıcının IndexedDB alanından okunur,
// hiçbiri sunucuya gönderilmez.
const ajan=window.LocalPersonalization;
const $=id=>document.getElementById(id);
const GUN_MS=86400000;
const KONU_ADLARI={gundem:"Gündem",teknoloji:"Teknoloji",bilim:"Bilim",spor:"Spor",sanat:"Kültür",saglik:"Yaşam",yasam:"Yaşam",ekonomi:"Ekonomi",egitim:"Eğitim",oyun:"Oyun",seyahat:"Keşif"};
const KONTROL_ADLARI={sakin:"Sakin",mutluluk:"Mutluluk",umut:"Umut",sinirli:"Sinirli",anksiyete:"Yoğun"};
const HAFTA_ADI=["Bu hafta","Geçen hafta","2 hafta önce","3 hafta önce"];
const TEPKI_YONU={begendim:1,umutlandim:1,kizdim:-1,gerildim:-1};
const AYAR_MESAJ={
  dengeleme:["Duygu dengeleme açıldı.","Duygu dengeleme kapatıldı. Akış artık yalnızca ilgi alanlarına göre sıralanıyor."],
  doygunluk:["Renk yumuşatma açıldı.","Renk yumuşatma kapatıldı."],
  kontrolSorulari:["Kontrol soruları açıldı.","Kontrol soruları kapatıldı."],
  kisiselUyarlama:["Kişisel uyarlama açıldı.","Kişisel uyarlama kapatıldı. Kişisel model silinmedi; yeniden açınca kaldığı yerden devam eder."],
};
const yuzde=x=>`%${Math.round(x*100)}`;
const topla=(hedef,kaynak={})=>Object.entries(kaynak).forEach(([k,v])=>{hedef[k]=(hedef[k]||0)+v;});
function gunAnahtari(zaman){const d=new Date(zaman);return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,"0")}-${String(d.getDate()).padStart(2,"0")}`;}

function anahtarlariGoster(ayarlar){document.querySelectorAll("[data-ayar]").forEach(buton=>buton.setAttribute("aria-checked",String(!!ayarlar[buton.dataset.ayar])));}
async function kisiselDurumGoster(){
  const durum=await ajan.kisiselModelDurumu();
  const spiral=durum.spiralEtkin?"Dengeleme için kişisel uyarlama etkin.":"Akış için varsayılan tahmin kullanılıyor.";
  $("kisisel-durum").textContent=durum.guncelleme?`${durum.guncelleme} yanıtla güncellendi. ${spiral}`:"Henüz kontrol sorusu yanıtlanmadı.";
}
// Pilot dosyası: indirmeden önce içeriği sayfada gösterilir.
async function pilotGoster(){
  const dosya=await ajan.pilotDosyasi(),adet=dosya.kayitlar.length;
  $("pilot-indir").textContent=`Pilot dosyasını indir (${adet} cevap)`;$("pilot-indir").disabled=!adet;
  $("pilot-icerik").textContent=JSON.stringify(dosya,null,1);
  return dosya;
}
$("pilot-indir").addEventListener("click",async()=>{
  const dosya=await pilotGoster(),bag=document.createElement("a");
  bag.href=URL.createObjectURL(new Blob([JSON.stringify(dosya)],{type:"application/json"}));
  bag.download=`nsosyal-pilot-${dosya.katilimci}.json`;document.body.append(bag);bag.click();bag.remove();
  setTimeout(()=>URL.revokeObjectURL(bag.href),1000);
});

// Son 4 hafta, bugünden geriye 7'şer günlük pencereler.
function haftalar(gunler,adet=4){
  const harita=new Map(gunler.map(gun=>[gun.tarih,gun]));
  return Array.from({length:adet},(_,h)=>{
    const t={etkilesim:0,dwell:0,yogunDwell:0,konular:{},kontroller:{},tepkiler:{},gunSayisi:0,ornek:false};
    for(let i=0;i<7;i++){
      const gun=harita.get(gunAnahtari(Date.now()-(h*7+i)*GUN_MS));if(!gun)continue;
      t.gunSayisi++;t.ornek=t.ornek||!!gun.ornek;t.etkilesim+=gun.etkilesim||0;t.dwell+=gun.dwell||0;t.yogunDwell+=gun.yogunDwell||0;
      topla(t.konular,gun.konular);topla(t.kontroller,gun.kontroller);topla(t.tepkiler,gun.tepkiler);
    }
    t.pay=t.dwell?t.yogunDwell/t.dwell:null;
    t.enKonu=Object.entries(t.konular).sort((a,b)=>b[1]-a[1])[0]?.[0]||null;
    return t;
  });
}
function uzunDonemGoster(ozet){
  const h=haftalar(ozet.gunler),[bu,gecen]=h;
  $("ornek-rozet").hidden=!ozet.ornekVar;$("ornek-yukle").hidden=ozet.ornekVar;$("ornek-kaldir").hidden=!ozet.ornekVar;
  let cumle;
  if(bu.pay!==null&&gecen.pay!==null){const fark=Math.round((bu.pay-gecen.pay)*100);cumle=`Bu hafta yoğun tonlu içerikte geçen sürenin payı ${yuzde(bu.pay)}; geçen hafta ${yuzde(gecen.pay)} idi${fark===0?" (değişmedi)":` (${Math.abs(fark)} puan ${fark<0?"azaldı":"arttı"})`}.`;}
  else if(bu.pay!==null)cumle=`Bu hafta yoğun tonlu içerikte geçen sürenin payı ${yuzde(bu.pay)}. Karşılaştırma için geçen haftadan da veri gerekiyor.`;
  else if(gecen.pay!==null)cumle=`Bu hafta henüz etkileşim yok. Geçen hafta yoğun tonlu içerikte geçen sürenin payı ${yuzde(gecen.pay)} idi.`;
  else cumle="Henüz günlük özet yok. Akışta gezindikçe her gün için yalnızca toplam sayılar tutulur; hangi gönderiye baktığın tutulmaz.";
  $("uzun-karsilastirma").textContent=cumle;
  const enCok=Math.max(1,...h.map(t=>t.etkilesim));
  $("hafta-grafik").innerHTML=h.map((t,i)=>{
    const etiket=`${HAFTA_ADI[i]}: ${t.etkilesim} etkileşim${t.pay!==null?`, yoğun tonlu içerik payı ${yuzde(t.pay)}`:""}`;
    const olumlu=Object.entries(t.tepkiler).filter(([k])=>TEPKI_YONU[k]>0).reduce((a,[,v])=>a+v,0),olumsuz=Object.entries(t.tepkiler).filter(([k])=>TEPKI_YONU[k]<0).reduce((a,[,v])=>a+v,0);
    const tepki=olumlu||olumsuz?` · tepki ${olumlu} olumlu / ${olumsuz} olumsuz`:"";
    const alt=t.pay!==null?`yoğun ${yuzde(t.pay)}${t.enKonu?` · en çok ${KONU_ADLARI[t.enKonu]||t.enKonu}`:""}${tepki}`:"veri yok";
    return `<div class="hafta-satir"><span class="hafta-ad">${HAFTA_ADI[i]}${t.ornek?' <i class="ornek-isaret">örnek</i>':""}</span><div class="hafta-cubuk" role="img" aria-label="${etiket}"><i style="width:${t.etkilesim/enCok*100}%"><em style="width:${(t.pay||0)*100}%"></em></i></div><b>${t.etkilesim}</b><small>${alt}</small></div>`;
  }).join("");
  const kontroller={};h.forEach(t=>topla(kontroller,t.kontroller));
  const satirlar=Object.entries(kontroller).sort((a,b)=>b[1]-a[1]);
  $("kontrol-dagilimi").innerHTML=satirlar.length?`<b>Son 4 haftada kontrol sorularına cevapların</b><div>${satirlar.map(([k,v])=>`<span>${KONTROL_ADLARI[k]||k} <i>${v}</i></span>`).join("")}</div>`:"";
}
async function veriGoster(ozet){
  const [durum,onay]=await Promise.all([ajan.kisiselModelDurumu(),ajan.getOnay()]),gercekGun=ozet.gunler.filter(gun=>!gun.ornek).length;
  $("veri-listesi").innerHTML=[
    `<li><b>${onay?(onay.secim==="acik"?"Açık":"Kapalı"):"—"}</b> ilk açılış tercihin<small>${onay?`${new Date(onay.tarih).toLocaleDateString("tr-TR")} tarihinde seçildi; yukarıdaki anahtarlarla istediğin an değiştirebilirsin.`:"Henüz seçim yapılmadı."}</small></li>`,
    `<li><b>${ozet.olaySayisi}</b> ham etkileşim kaydı<small>${Math.round(ozet.saklamaGun/7)} hafta saklanır; daha eskisi kendiliğinden silinir.</small></li>`,
    `<li><b>${gercekGun}</b> günlük özet<small>Yalnızca gün başına toplam sayılar, ${Math.round(ozet.saklamaGun/7)} hafta saklanır.</small></li>`,
    `<li><b>${durum.guncelleme}</b> kişisel model güncellemesi<small>Kontrol sorusu cevaplarından, yalnızca bu cihazda.</small></li>`,
    `<li><b>${durum.pilotKayit}</b> pilot kaydı<small>Her kontrol sorusu anı için cevap ve özet sayılar. Yalnızca sen indirip gönderirsen cihazdan çıkar.</small></li>`,
    `<li><b>Yok</b> sunucuya giden davranış kaydı<small>Sunucu yalnızca herkese açık aday gönderileri sağlar.</small></li>`,
  ].join("");
}
async function yenile(){
  const [ayarlar,ozet]=await Promise.all([ajan.getAyarlar(),ajan.uzunDonemOzeti()]);
  anahtarlariGoster(ayarlar);uzunDonemGoster(ozet);await Promise.all([kisiselDurumGoster(),veriGoster(ozet),pilotGoster()]);
}

document.querySelectorAll("[data-ayar]").forEach(buton=>buton.addEventListener("click",async()=>{
  const anahtar=buton.dataset.ayar,yeni=buton.getAttribute("aria-checked")!=="true";
  buton.setAttribute("aria-checked",String(yeni));
  try{anahtarlariGoster(await ajan.setAyar(anahtar,yeni));$("ayar-bildirim").textContent=AYAR_MESAJ[anahtar][yeni?0:1];}
  catch{buton.setAttribute("aria-checked",String(!yeni));$("ayar-bildirim").textContent="Ayar kaydedilemedi, lütfen tekrar dene.";}
}));
$("ornek-yukle").addEventListener("click",async()=>{const ozet=await ajan.ornekGecmisYukle();uzunDonemGoster(ozet);veriGoster(ozet);});
$("ornek-kaldir").addEventListener("click",async()=>{const ozet=await ajan.ornekGecmisiKaldir();uzunDonemGoster(ozet);veriGoster(ozet);});
$("kisisel-sifirla").addEventListener("click",async()=>{await ajan.kisiselModeliSifirla();await yenile();$("veri-bildirim").textContent="Kişisel model sıfırlandı; tahminler varsayılan modelle yapılacak.";});
// Silme geri alınamaz: ilk dokunuş yalnızca onay ister, 4 saniye içinde
// ikinci dokunuş siler.
let silmeOnayi=null;
$("tumunu-sil").addEventListener("click",async event=>{
  const buton=event.currentTarget,metin=buton.lastChild;
  if(!silmeOnayi){buton.classList.add("onay");metin.textContent=" Emin misin? Silmek için tekrar dokun";silmeOnayi=setTimeout(()=>{silmeOnayi=null;buton.classList.remove("onay");metin.textContent=" Tüm yerel verileri sil";},4000);return;}
  clearTimeout(silmeOnayi);silmeOnayi=null;buton.classList.remove("onay");metin.textContent=" Tüm yerel verileri sil";
  await ajan.erase();await yenile();$("veri-bildirim").textContent="Yerel veriler silindi. Ayar seçimlerin korundu.";
});
// Sunum öncesi sıfırlama (bilgisayarda ana sayfanın sol menüsünde de var).
$("oturum-sifirla").addEventListener("click",async()=>{await ajan.oturumuSifirla();await yenile();$("sifirla-bildirim").textContent="Oturum sıfırlandı. İlgi alanların, kişisel modelin ve geçmişin korundu.";});
let tamSifirlamaOnayi=null;
$("tamamen-sifirla").addEventListener("click",async event=>{
  const buton=event.currentTarget,metin=buton.lastChild;
  if(!tamSifirlamaOnayi){buton.classList.add("onay");metin.textContent=" Emin misin? Silmek için tekrar dokun";tamSifirlamaOnayi=setTimeout(()=>{tamSifirlamaOnayi=null;buton.classList.remove("onay");metin.textContent=" Tamamen sıfırla";},4000);return;}
  clearTimeout(tamSifirlamaOnayi);tamSifirlamaOnayi=null;buton.classList.remove("onay");metin.textContent=" Tamamen sıfırla";
  await ajan.tamamenSifirla();await yenile();$("sifirla-bildirim").textContent="Her şey sıfırlandı. Ana sayfa ilk kez açılmış gibi açılacak.";
});

if(ajan){ajan.init().then(yenile).catch(error=>{console.warn("Ayarlar yüklenemedi",error);$("ayar-bildirim").textContent="Yerel depolama bu tarayıcıda kullanılamıyor.";});}
