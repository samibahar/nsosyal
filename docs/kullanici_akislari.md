# Kullanıcı Akışları ve Veri Sınırı

## Mimari: neyin nerede işlendiği

```mermaid
flowchart LR
  subgraph Sunucu["Sunucu (FastAPI)"]
    B["Duygu modeli (BERT v3)<br/>gönderi başına bir kez"]
    A["Aday seçimi<br/>48 aday, her konudan en az 2"]
  end
  subgraph Cihaz["Kullanıcının cihazı (tarayıcı)"]
    I[("IndexedDB<br/>ham davranış, en fazla 240 olay<br/>günlük toplamlar, 12 hafta")]
    S["Spiral v2 + ruh hali modeli"]
    R["Sıralama: ilgi + çeşitlilik + doz"]
  end
  B --> A -->|herkese açık aday gönderiler| R
  I --> S --> R --> F["Akış: ilk 12 gönderi"]
  F -->|durma, tıklama, tepki| I
```

Sunucu davranış verisi kabul eden hiçbir uç nokta sunmaz; bu bir tarayıcı
testiyle ve `demo_kontrol.py` ile doğrulanır.

## 1. İlk açılış ve açık rıza

```mermaid
flowchart TD
  G[İlk açılış] --> K{"Bilgilendirme:<br/>ne tutulur, nerede, teşhis değildir"}
  K -->|Açık başlat| A[Duygu katmanı açık]
  K -->|Kapalı başlat| C["Dört anahtar kapalı<br/>akış yalnızca ilgiyle kişiselleşir"]
  A --> Y[Ayarlar'dan her an değiştirilebilir]
  C --> Y
```

Seçim ve tarihi yalnızca cihazda saklanır; Ayarlar → "Verilerin" bölümünde
görünür.

## 2. Akış, dengeleme ve açıklama

```mermaid
flowchart TD
  K[Kullanıcı akışta geziniyor] --> O["Olaylar cihaza yazılır<br/>(gönderi, süre, tıklama, tepki)"]
  O --> Y{"Son 30 dk'da yoğun tonlu içerikte<br/>kendi okuma hızına göre uzun ve pasif kalma?"}
  Y -->|hayır| N[Akış yalnızca ilgi ve çeşitlilikle]
  Y -->|evet| D["Doz: yoğun içerik payı<br/>taban × (1 − 0,6 × yoğunluk)<br/>yoğun gönderiler aralıklanır"]
  D --> B1["Bir kez bildirim:<br/>Tamam / Bu oturumda dengeleme yapma"]
  D --> E["Kartta 'dengelendi' etiketi"]
  E --> NB["Neden bu? → kaç sıra aşağı,<br/>payın hedefi (ör. %33 → %20)"]
  R["Resmi/acil bilgi hesapları"] -.->|muaf| D
```

## 3. Kontrol sorusu ve cihazda öğrenme

```mermaid
flowchart TD
  S["Ara sıra: Şu an nasıl hissediyorsun?<br/>(8 etkileşimde bir, en az 20 dk arayla)"] --> T["Önce tahmin: varsayılan ve kişisel model<br/>(cevap gelmeden, kullanıcıya gösterilmeden)"]
  T --> C[Kullanıcının cevabı]
  C --> K["Karşılaştırma sayaçları<br/>(model, 'hep en sık cevap', rastgele %20)"]
  C --> U["Kişisel modelde tek küçük adım<br/>(varsayılana doğru düzenlileştirilmiş)"]
  K --> I[İçgörü → Model doğrulama]
```

Kişisel model yalnızca tahmin etiketlerini etkiler; akışın sıralamasını
kullanıcı başına kaydırmaz.

## 4. Kontrol ve silme

- **Ayarlar:** duygu dengeleme, renkleri yumuşatma, kontrol soruları, kişisel
  uyarlama (her biri ayrı anahtar).
- **Tüm yerel verileri sil:** olaylar, profil, günlük özetler ve kişisel model
  silinir; ayar seçimleri korunur. İki adımlı onay.

## 5. Yedek yol: tarayıcı yerel depolamaya izin vermiyorsa

Akış açılır ama kişiselleştirilmez; durum kartı "Kişiselleştirme kapalı" der ve
hiçbir davranış verisi gönderilmez (tarayıcı testiyle doğrulanır).

## 6. Jüri demosu

Hazır 12 aday ve 10 örnek sinyal cihazda, gerçek sıralama fonksiyonlarıyla
işlenir; önce/sonra sıra ve gerekçe `/juri.html`'de saklanır. Dengeleme
Ayarlar'dan kapatılıp demo tekrar çalıştırılırsa yoğun gönderiler aşağı alınmaz.
