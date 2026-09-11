# Erişilebilirlik Değerlendirmesi

Son güncelleme: 11.09.2026. Hedef: WCAG 2.1 AA.

## Yöntem

- **Otomatik denetim:** axe-core 4.9.1, `wcag2a`, `wcag2aa`, `wcag21aa`
  kural etiketleri; 7 sayfa (ana akış, Haberler, İçgörü, Ayarlar, Keşfet,
  Profil, Jüri). Denetim kalıcı bir tarayıcı testidir:
  `tests/e2e/test_erisilebilirlik.py` (her sayfa için ayrı test, taze tarayıcı
  bağlamında, yani boş yerel veriyle).
- **Etkileşim testleri (Playwright):** açık rıza kutusunda Tab odağının kutu
  içinde dönmesi, kapalı diyalogların odaklanamaz olması, açılınca
  kullanılabilir olması, 390 px genişlikte hiçbir sayfada yatay taşma olmaması.
- **Elle kontrol:** dokunma hedefleri, odak halkaları, hareket azaltma tercihi,
  mobil ve masaüstü görünüm.

## Bulgular ve düzeltmeler

İlk denetimde 4 kural türünde 62 ihlal (hepsi "serious") bulundu; hepsi
düzeltildi, güncel durum **0 ihlal**.

| Kural | Adet | Neden | Düzeltme |
|---|---|---|---|
| `link-name` | 24 (6 sayfa × 4) | Mobil alt menüde etiketler `display:none` ile gizlendiği için bağlantıların erişilebilir adı yoktu | Etiket görsel olarak gizli ama ekran okuyucuya açık (`tema.css`) |
| `color-contrast` | 32 | Eski paletten kalan soluk yeşil-gri 8–9 px etiketler (2,7–4,2:1) ve yeşil zemin üzerinde siyah metin (3,5:1) | Etiketler `--muted` (#5b6470, beyaz üzerinde 6,4:1) ve en az 11 px; yeşil zeminde beyaz metin (5,4:1) |
| `aria-hidden-focus` | 5 | Kapalı paneller `aria-hidden="true"` ama içindeki düğmelere Tab ile gidilebiliyordu | `static/erisim.js`: `aria-hidden` olan diyaloglar otomatik olarak `inert` |
| `nested-interactive` | 1 | İçgörü'deki ritim grafiği kutusu `role="img"` iken boş durumda içine bağlantı konuyordu | Rol yalnızca grafik çizildiğinde veriliyor |

## Diğer önlemler

- Dokunma hedefleri en az 44 px (Apple HIG), metin düğmelerinde görünmez
  dokunma payı.
- Görünür odak halkası tüm etkileşimli öğelerde.
- Ayarlar'daki anahtarlar `role="switch"` + `aria-checked`, açıklamaları
  `aria-describedby` ile bağlı.
- Açık rıza kutusu `role="dialog"` + `aria-modal`, iki seçenek eşit ağırlıkta.
- Durum değişiklikleri (akış güncellendi, ayar kaydedildi, dengeleme bildirimi)
  `aria-live` / `role="status"` ile duyurulur.
- Grafiklerde bilgi yalnızca renkle verilmez; sayı ve metin de vardır.
- `prefers-reduced-motion` desteklenir (iskelet animasyonu, geçişler).

## Sınırlılıklar

- Otomatik araçlar erişilebilirlik sorunlarının ancak bir kısmını yakalar;
  ekran okuyucu (NVDA, VoiceOver) ile gerçek kullanıcı testi yapılmadı.
- Karanlık mod yok.
- Duygu tepki tepsisinde renkli emojiler bilinçli olarak korundu (etiket metni
  de var).
