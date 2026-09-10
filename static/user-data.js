// Fictional, deterministic demo accounts. No real-person identities are used.
const DEMO_USERS={
  denizcetin:{name:"Deniz Çetin",handle:"@denizcetin",initials:"DÇ",bio:"Teknoloji, bilim ve açık kaynak notları.",color:"#5079a2",topics:["teknoloji","bilim"]},
  eceyilmaz:{name:"Ece Yılmaz",handle:"@eceyilmaz",initials:"EY",bio:"Kültür rotaları, sergiler ve küçük keşifler.",color:"#a66175",topics:["sanat","seyahat"]},
  ardaatlas:{name:"Arda Atlas",handle:"@ardaatlas",initials:"AA",bio:"Spor, oyun ve her gün biraz hareket.",color:"#4a8155",topics:["spor","oyun"]},
  selinkaya:{name:"Selin Kaya",handle:"@selinkaya",initials:"SK",bio:"Kampüs hayatı ve iyi yaşam üzerine.",color:"#527e6f",topics:["saglik","egitim"]},
  mertdemir:{name:"Mert Demir",handle:"@mertdemir",initials:"MD",bio:"Şehir, ekonomi ve gündelik notlar.",color:"#966d47",topics:["gundem","ekonomi"]},
  emiryusuf:{name:"Emir Yusuf",handle:"@emiryusuf",initials:"EU",bio:"NSosyal'de yeni fikirleri takip ediyor.",color:"#1f2720",topics:[]}
};
const TOPIC_AUTHORS={
  teknoloji:["denizcetin"],bilim:["denizcetin"],sanat:["eceyilmaz"],seyahat:["eceyilmaz"],
  spor:["ardaatlas"],oyun:["ardaatlas"],saglik:["selinkaya"],egitim:["selinkaya"],
  gundem:["mertdemir"],ekonomi:["mertdemir"]
};
function authorForPost(post){
  if(post&&post.yazar&&DEMO_USERS[post.yazar])return {id:post.yazar,...DEMO_USERS[post.yazar]};
  const options=TOPIC_AUTHORS[(post&&post.konu)||""]||["emiryusuf"];
  const id=options[(Math.abs(Number(post&&post.id)||1)-1)%options.length];
  return {id,...DEMO_USERS[id]};
}
