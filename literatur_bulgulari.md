# Literatür Taraması — Rapor İçin Uygulanabilir Bulgular

19.08.2026 gecesi, kullanıcı isteğiyle yapıldı. Tüm kaynaklar gerçek, WebSearch
ile doğrulandı — hiçbir atıf uydurulmadı. Amaç: raporun teknik/bilimsel
dayanağını güçlendirmek ve tasarım kararlarımızı (doğrulama, olmasa da
sınırlılıkları) literatürle test etmek.

## 1. Ecological Momentary Assessment (EMA) — en doğrudan ilgili bulgu

Az önce kodladığımız "aktif öğrenme / kendi kendini doğrulama döngüsü"
(kullanıcıya ara sıra "şu an gerçekte nasıl hissediyorsun?" sorusu), aslında
psikolojide **EMA (Ecological Momentary Assessment)** / **ESM (Experience
Sampling Method)** olarak bilinen, iyi kurulmuş bir araştırma yönteminin
bağımsız bir yeniden keşfi.

- **"Investigating Best Practices for Ecological Momentary Assessment"**,
  *JMIR* 2024;26:e50275 — https://www.jmir.org/2024/1/e50275
  Bulgu: soru SAYISININ artması uyumu (compliance) düşürüyor, ama örnekleme
  SIKLIĞI tek başına uyumla ilişkili değil → "az soru, sık sorma" doğru
  prensip. Bizim "her ~8 etkileşimde tek soru" tasarımımızla birebir uyumlu.
- **"Measuring Criterion Validity of Microinteraction EMA (Micro-EMA)"**,
  PMC7991987 — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7991987/
  Tek-soruluk mikro-EMA'nın, araştırma sınıfı sürekli sensörle tutarlı
  kriter geçerliliği taşıdığını gösteriyor.
- **"Modeling Behaviour to Predict User State: Self-Reports as Ground
  Truth"**, arXiv:2007.14461 — https://arxiv.org/pdf/2007.14461
  ESM öz-bildirimlerinin ML modelleri için ground-truth olarak kullanıldığını
  belgeliyor, AMA tekrarlı sorgunun kullanıcı yorgunluğuna (fatigue) ve
  rastgele/anlamsız yanıtlara yol açabileceği riskini de not ediyor.

**Raporda kullan:** "Bu mekanizma tesadüfen değil, psikolojide yerleşik bir
yöntemin (EMA/micro-EMA) hafif bir uygulaması" de. Ama kullanıcı yorgunluğu
riskini de dürüstçe bir sınırlılık olarak yaz.

## 2. Pasif kullanım / dwell-time / doomscrolling — kanıt orta güçte, abartma

- **Meta-analiz (141 çalışma):** "Are active and passive social media use
  related to mental health, wellbeing, and social support outcomes?",
  *JCMC* 29(1), 2024 — https://academic.oup.com/jcmc/article/29/1/zmad055/7595758
  Pasif kullanımın olumsuz sonuçlarla ilişkisi genelde KÜÇÜK/DEĞİŞKEN;
  sosyal kaygı ile ilişki sadece 3 çalışmaya dayanıyor (zayıf kanıt).
- **Doomscrolling:** ScienceDirect 2024, "Beyond the Scroll: Intolerance of
  Uncertainty... Doomscrolling" — https://www.sciencedirect.com/science/article/abs/pii/S0191886924003799
  Doomscrolling kaygı/stres/kontrol kaybıyla ilişkili (destekleyici) ama
  çoğu çalışma kesitsel — nedensellik kanıtlanmamış.

**Raporda kullan:** "Uzun pasif dwell-time = olumsuz spiral" varsayımımızı
KESİN değil "olası örüntü" diliyle sun (zaten disiplin kuralımız buydu, artık
literatür desteği de var). Abartılı nedensellik iddiası kurma.

## 3. Pasif sinyallerden duygu-durumu çıkarımı (digital phenotyping)

- **"Passive Sensing for Mental Health Monitoring Using ML with Wearables
  and Smartphones: Scoping Review"**, *JMIR* 2025 —
  https://www.jmir.org/2025/1/e77066
  GPS + telefon kullanımıyla depresyon şiddeti sınıflandırmasında %86.5
  doğruluk, PHQ-9 ile r=-0.63 bildirilmiş. AMA: eksik veri ve sınırlı dış
  geçerlilik önemli önyargı kaynağı; kişiselleştirilmiş modellerde tahmin
  gücünün büyük kısmının "kişi kimliği" değişkeninden geldiği (yani modelin
  zamanla değişimden çok kararlı bireysel farkları yakaladığı) bulunmuş.

**Raporda kullan:** Bu alan meşru bir araştırma alanı (yaklaşımımızı
destekler) AMA kişiye-özgü kalibrasyon olmadan güvenilirlik sınırlı —
`psikolojik_durum.py`'nin şu an sentetik/genellenmiş (kişiye özelleşmemiş)
olduğunu bilinen bir sınırlılık olarak açıkça yaz. Gelecek iş önerisi:
kullanıcı bazlı kalibrasyon (doğrulama döngüsünün topladığı veriyle).

## 4. Refah-farkında (wellbeing-aware) sıralama algoritmaları

- **"Challenging Social Media Threats using Collective Well-being Aware
  Recommendation Algorithms..."**, arXiv:2102.04211 —
  https://arxiv.org/pdf/2102.04211
  "Collective Well-Being aware Recommender Systems (CWB-RS)" kavramı —
  etkileşim optimizasyonu yerine uzun-vadeli kümülatif refahı maksimize
  etmeyi öneriyor. Bizim iki-katmanlı (ilgi+refah) motorumuzla kavramsal
  paralel.
- **"Better Feeds: Algorithms That Put People First"**, Georgetown KGI,
  Mart 2025 — https://kgi.georgetown.edu/wp-content/uploads/2025/02/Better-Feeds_-Algorithms-That-Put-People-First.pdf
  Endüstri/politika düzeyinde "insan-öncelikli" sıralama ilkeleri.

**Raporda kullan:** "Yenilikçilik ve Özgünlük" / "Problemi Çözme Başarısı"
kriterlerinde akademik emsal olarak referans ver — fikrimiz havada değil.

## 5. Algoritmik şeffaflık / "neden bunu görüyorsun"

- **"Explainable recommendation: when design meets trust calibration"**,
  *World Wide Web* journal (Springer) —
  https://link.springer.com/article/10.1007/s11280-021-00916-0
  Açıklamalar genelde güveni/memnuniyeti artırır, AMA nüans: çok detaylı
  açıklama "algorithmic aversion"a (kullanıcı nasıl çalıştığını öğrenince
  güvenmemeye başlaması) yol açabilir.

**Raporda/tasarımda kullan:** Şeffaflık panelini "az ama net" tut (zaten
mevcut tasarım kısa açıklama cümlesi + birkaç çubuk şeklinde — bu doğru
yönde, aşırı teknik detaya kaymaktan kaçın).

---

## En Uygulanabilir 5 Bulgu (özet)

1. Doğrulama döngümüz EMA/micro-EMA'nın meşru bir uygulaması — literatürle
   isimlendirilip güçlendirilebilir, ama kullanıcı yorgunluğu riski dürüstçe
   yazılmalı.
2. Pasif dwell-time'ın olumsuz duyguyla ilişkisi literatürde ORTA güçte —
   "olası örüntü" dilini koru, kesinlik iddia etme.
3. Davranıştan duygu-durumu çıkarımı meşru ama kişiye-özgü kalibrasyon
   olmadan sınırlı — bu, mevcut sınırlılığımızı ve gelecek iş önerisini
   (kişiselleştirme) netleştiriyor.
4. İki-katmanlı refah-farkında sıralama konseptinin akademik emsali var
   (CWB-RS) — yenilikçilik bölümünde referans ver.
5. Şeffaflık panelinde "az ama net" ilkesi kritik — mevcut kısa tasarımı
   koru, aşırı detaya kaçma.
