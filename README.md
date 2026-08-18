# NSosyal İnovasyon Yarışması — Proje Klasörü

Bu klasör, TEKNOFEST NSosyal İnovasyon Yarışması 2026 projemizin kod tarafını
**Claude Code** ile (yerel bilgisayarınızda, gerçek internet erişimiyle) devam
ettirebilmeniz için hazırlandı. Cowork'te (bulut ortamı) HuggingFace'e ağ erişimi
kısıtlı olduğu için gerçek BERT modelini indiremedik — bu yüzden mimariyi önce
sözlük-tabanlı basit bir stand-in ile kanıtladık (`spike_poc.py`, çalıştı ve
doğru sonuç verdi). Şimdi buradan devam edip gerçek modeli bağlayabilirsiniz.

Fikir/plan/araştırma tarafı (rapor metni, PDF'ler, çalışma planı) Cowork'te
kalmaya devam edecek — orada zaten iyi çalışıyor. Bu klasör sadece **kod**
kısmı için.

## Bu klasörde ne var?

- `CLAUDE.md` — Projenin TAM bağlamı: ürün konsepti, alınan kararlar, reddedilen
  yaklaşımlar (tekrar önerilmemesi için), doğrulanmış NSosyal bulguları,
  kullanılacak araçlar, iş modeli fikirleri. Claude Code bu dosyayı otomatik
  okuyacak, siz hiçbir şeyi baştan anlatmak zorunda kalmayacaksınız.
- `spike_poc.py` — Çalışan, kanıtlanmış bir kanıt-of-konsept. İki katmanlı
  skor motoru + refah katmanı + spiral tespiti + açıklanabilirlik mantığının
  hepsini uçtan uca gösteriyor (henüz gerçek BERT modeli değil, basit bir
  sözlük kullanıyor). Çalıştırmak için: `python3 spike_poc.py`
- `requirements.txt` — Sıradaki adımlar için gereken Python paketleri.

## Claude Code'u kurma (yerel bilgisayarınızda)

Claude Code, terminalden çalışan bir araç. Kurulum için **Pro, Max, Team,
Enterprise ya da Console hesabı gerekiyor** (ücretsiz hesapla çalışmıyor).

**macOS / Linux / WSL:**
```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Windows (PowerShell):**
```powershell
irm https://claude.ai/install.ps1 | iex
```

Node.js kurulu olması gerekmiyor (standart kurulum için). Terminal kullanmak
istemiyorsanız, Claude'un terminal gerektirmeyen bir masaüstü uygulaması
alternatifi de var.

## Bu projeyi başlatma

1. Bu klasörü (`nsosyal-projesi/`) bilgisayarınıza indirin/açın.
2. Terminalde bu klasöre girin:
   ```bash
   cd nsosyal-projesi
   ```
3. Claude Code'u başlatın:
   ```bash
   claude
   ```
4. Claude Code açıldığında `CLAUDE.md` dosyasını otomatik okuyacak ve projenin
   tüm bağlamına sahip olacak. Doğrudan şöyle bir şeyle başlayabilirsiniz:
   > "CLAUDE.md'yi oku, spike_poc.py'yi incele, sonra duygu_skoru() fonksiyonunu
   > gerçek savasy/bert-base-turkish-sentiment-cased modeliyle değiştirelim."
5. Bağımlılıkları kurmak isterseniz (Claude Code sizin için de yapabilir):
   ```bash
   pip install -r requirements.txt
   ```

## Git / GitHub

Rapor kontrol listesi düzenli commit geçmişi istiyor. Bu klasörü bir git
reposu olarak başlatıp GitHub'a bağlamanızı öneririz:
```bash
git init
git add .
git commit -m "İlk commit: proje bağlamı + kanıt-of-konsept spike"
```
Sonra GitHub'da boş bir repo oluşturup `git remote add origin <repo-url>` ile
bağlayabilirsiniz. Claude Code bu adımlarda da yardımcı olabilir.

## Cowork ile iş bölümü (önerilen kullanım şekli)

- **Cowork (burada):** Rapor metni, PDF üretimi, araştırma, plan güncellemeleri,
  görsel/döküman işleri.
- **Claude Code (yerelde):** Gerçek model entegrasyonu, backend/API kodu, spiral
  sınıflandırıcı eğitimi, web arayüzü, git/GitHub yönetimi.

İki taraf da aynı `CLAUDE.md` mantığından besleniyor, yani hangi ortamda
çalışırsanız çalışın kararlar tutarlı kalacak.
