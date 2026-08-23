$ErrorActionPreference = "Stop"

$projectRoot = if ($PSScriptRoot) { Split-Path -Parent $PSScriptRoot } else { (Get-Location).Path }
$sourcePath = Join-Path $projectRoot "NSosyal_Teknik_Rapor.docx"
$outputPath = Join-Path $projectRoot "NSosyal_Teknik_Rapor_Guncel.docx"
$assetRoot = Join-Path $projectRoot "docs\report-assets"

Copy-Item -LiteralPath $sourcePath -Destination $outputPath -Force

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0

function Find-Paragraph {
    param($Document, [string]$Prefix)
    foreach ($paragraph in $Document.Paragraphs) {
        $text = ($paragraph.Range.Text -replace "[\r\a]", "").Trim()
        if ($text.StartsWith($Prefix)) { return $paragraph }
    }
    throw "Paragraph not found: $Prefix"
}

function Set-ParagraphText {
    param($Document, [string]$Prefix, [string]$Text)
    $paragraph = Find-Paragraph $Document $Prefix
    $range = $paragraph.Range.Duplicate
    $range.End = $range.End - 1
    $range.Text = $Text
}

function Find-Heading {
    param($Document, [string]$Text)
    foreach ($paragraph in $Document.Paragraphs) {
        $paragraphText = ($paragraph.Range.Text -replace "[\r\a]", "").Trim()
        $styleName = [string]$paragraph.Range.Style.NameLocal
        if ($paragraphText -eq $Text -and $styleName -match "Başlık 1|Heading 1") { return $paragraph }
    }
    throw "Heading not found: $Text"
}

function Add-PictureToCell {
    param($Cell, [string]$Path, [string]$Caption, [double]$Width)
    $range = $Cell.Range.Duplicate
    $range.End = $range.End - 1
    $shape = $range.InlineShapes.AddPicture($Path, $false, $true, $range)
    $shape.LockAspectRatio = -1
    $shape.Width = $Width
    $cellRange = $Cell.Range
    $cellRange.ParagraphFormat.Alignment = 1
    $captionRange = $Cell.Range.Duplicate
    $captionRange.End = $captionRange.End - 1
    $captionRange.InsertAfter("`r$Caption")
    $Cell.Range.Font.Name = "Arial"
    $Cell.Range.Font.Size = 9
}

try {
    $document = $word.Documents.Open($outputPath)

    Set-ParagraphText $document "Projenin kapsamı," "Projenin kapsamı, sosyal ağ deneyimini koruyan ve yapay zekâyı sessiz bir kalite katmanı olarak kullanan uçtan uca bir prototiptir. FastAPI sunucu; herkese açık aday gönderileri, kullanıcı/profil verilerini, örnek haber havuzunu ve açıklama uç noktalarını sağlar. Tarayıcıdaki yerel ajan ise durma süresi, tıklama, yorum ve gönüllü tepki sinyallerini IndexedDB içinde tutar; konu ilgisini, içerik çeşitliliğini ve duygusal yoğunluk dengelemesini açıklanabilir bir skorla birleştirerek akışı cihaz üzerinde yeniden sıralar. İçerik kaldırılmaz; yalnızca sıralamadaki ağırlığı değişebilir. Çözüm; ana akış, hikâyeler, kullanıcı profilleri, Keşfet, Haberler, İçgörü ve ayrı Jüri/Teknik görünümünden oluşur. NSosyal veya T3 AI'a gerçek API erişimi yoktur; sistem bağımsız ve entegrasyona hazır bir kanıt-of-konsepttir. Davranışsal çıkarımlar teşhis olarak sunulmaz; kullanıcı tepkisi gönüllüdür ve tahminden daha güçlü bir sinyal olarak ele alınır."

    Set-ParagraphText $document "Backend Python/FastAPI" "Backend Python/FastAPI ile geliştirilmiştir. Sunucu; aday içerik, profil, haber, demo paketi ve teknik inceleme verilerini REST uç noktaları üzerinden sağlar. Duygu analizi için Türkçe BERT, davranışsal sınıflandırıcılar için scikit-learn bileşenleri korunmuştur. Güncel yarışma prototipinde kişiselleştirme katmanı ayrıca tarayıcıda çalışan, bağımlılıksız bir JavaScript ajanıyla uygulanmıştır: ham etkileşim geçmişi IndexedDB'de kalır; sunucuya yalnızca herkese açık aday içerik isteği gider. Frontend mobil-öncelikli HTML/CSS/JavaScript yapısındadır; dwell-time için Intersection Observer, çevrim içi sıralama ve karar izi için IndexedDB, yeniden sıralama nedenini görünür kılmak için Web Animations API kullanılır. Harici görsel API bağımlılığı demo anında kaldırılmış; Pexels kaynaklı, lisans/provenans bilgisi belgelenmiş küratörlü görseller yerel varlık olarak paketlenmiştir."

    Set-ParagraphText $document "Sistemin teknik altyapısı," "Sistemin güncel veri akışı iki sınırı açıkça ayırır. (1) Sunucu tarafı: GET /api/gonderiler ve GET /api/demo-paketi herkese açık adayları sağlar; profil, Keşfet ve Haberler sayfalarının içerik verisi FastAPI'den gelir. (2) Cihaz tarafı: görüntülenme/durma, tıklama, yorum ve gönüllü tepki olayları yerel ajan tarafından IndexedDB'ye yazılır. Ajan; ilgi ağırlığı, çeşitlilik katkısı, yoğunluk dengelemesi ve açık tepki etkisini birleştirerek local_skor üretir. Ana akış kartları aynı DOM düğümleri korunarak animasyonla yeniden sıralanır. Kullanıcı 'Neden bu?' panelinde ilgi, dengeleme, tepki etkisi ve son yerel skoru inceleyebilir; 'Yerel verileri sil' ile profili sıfırlayabilir. Haber akışında Kızdım/Gerildim tepkisi verilirse aynı olayı daha yapıcı çerçeveleyen alternatif kaynak önerisi sunulur. Bu mimari, sosyal özellikleri sunucuda tutarken hassas davranış örüntüsünü cihaz sınırında bırakır."

    Set-ParagraphText $document "Proje sürüm kontrolü altında" "Proje sürüm kontrolü altında, küçük ve anlamlı commit'lerle geliştirilmiştir. Güncel açık depo: https://github.com/emirzoz/nsosyal2. ui/mobile-redesign dalındaki commit geçmişi; mobil arayüz dönüşümü, yerel kişiselleştirme ajanı, haber tepkileri, dinamik sıralama animasyonu, jüri karar izi, gerçek İçgörü grafikleri ve mobil tepki düzeltmelerini ayrı değişiklikler halinde izlenebilir kılar. Raporla birlikte sunulan güncel prototip bu geçmişteki f10f050, 1f8ca98, bb823dd ve c8f8b97 gibi işlev odaklı commit'lerle doğrulanabilir."

    Set-ParagraphText $document "Kullanıcı akışı şu şekilde" "Güncel mobil kullanıcı akışı şu şekilde işler:"
    Set-ParagraphText $document "Kullanıcı ana akışa girer" "Kullanıcı ana akışa girer; sosyal gönderiler, gerçek görseller, yazar kimliği, hikâyeler ve mobil alt gezinme doğrudan görünür. Duygu katmanı akışı kaplayan bir panel değil, kompakt bir durum satırıdır."
    Set-ParagraphText $document "Bir gönderiyle etkileşime girer" "Kullanıcı gönderide durur, karta girer, yorum yapar veya Tepki tekerinden Beğendim, Umutlandım, Düşündüm, Kızdım ya da Gerildim seçeneklerinden birini gönüllü olarak seçer."
    Set-ParagraphText $document "Sistem bu etkileşimi anında işler" "Yerel ajan bu sinyali cihazda işler; yeterli örüntü oluştuğunda aynı aday havuzu içinde yoğun içeriklerin ağırlığını azaltır ve kartları 340 ms'lik neden-sonuç animasyonuyla yeniden sıralar."
    Set-ParagraphText $document '"Neden bunu görüyorsun?"' "Kullanıcı 'Neden bu?' düğmesiyle gönderinin ilgi eşleşmesini, akış ayarını ve yerel sonucunu insan-okunur biçimde görür; teknik ayrıntılar isteğe bağlı genişletilir."
    Set-ParagraphText $document "Yaklaşık her 8 etkileşimde" "Öz-bildirim sorusu sık ve kesintili biçimde gösterilmez; düşük sıklıkta, geçilebilir ve gönüllü bir kontrol olarak sunulur. Açık Tepki seçimi, kullanıcının kendi ifadesi olduğu için örtük tahminden daha güçlü kabul edilir."
    Set-ParagraphText $document 'İstediği an "Haftalık Rapor"' "Kullanıcı İçgörü sekmesinde bugün/hafta/ay aralığını seçebilir; gerçek yerel olay günlüğünden hesaplanan etkileşim ritmi çizgisi, konu dağılımı, gönüllü tepki dağılımı ve demo sıralama hareketini görür. Grafikler dekoratif sabit değerler değildir."
    Set-ParagraphText $document "Tasarım kararlarının gerekçesi" "Tasarım dili 'Calm Intelligence' olarak tanımlanmıştır: sosyal medya birincil, zekâ katmanı ikincildir. Mobil 390×844 ana hedef; 360×800, 393×852 ve 430×932 ek doğrulama boyutlarıdır. Ana akışta büyük analitik panel kullanılmaz; ✦ işareti açıklanabilir zekâ için tutarlı motif görevi görür. Tepki seçici, kartın overflow/animasyon bağlamında kırpılmaması için doğrudan document.body altında tek bir sayfa-seviyesi tepsi olarak çalışır. Alt gezinme 44 piksele yakın dokunma hedefleriyle sabitlenmiştir. Keşfet akışı rastgele sıralama yerine deterministik ilk 24 kartı kullanır; bu hem demo tekrarlanabilirliğini hem performansı artırır. İçgörü grafikleri renk dışında metin ve sayısal değer de taşır. Hareket azaltma tercihi CSS ile desteklenir. Kullanılabilirlik kontrolleri mobil ve masaüstünde Playwright ile yapılmış; tepki açma/seçme/kaydetme, yeniden sıralama, profil içeriği, besteci, haber alternatifi ve yatay taşma durumları doğrulanmıştır."

    Set-ParagraphText $document "Sistemin sıralama/tespit katmanı" "Sistemin sıralama/tespit katmanı iki yürütme düzeyine ayrılır. BERT ve açıklanabilir scikit-learn modelleri sunucu tarafında referans/entegrasyon mimarisini sürdürürken, canlı yarışma demosunun kişisel sıralaması tarayıcıda hafif aritmetik skorlarla çalışır. Yerel skor; temel ilgi skorunun %48'i, cihazdaki konu ağırlığının %34'ü, çeşitlilik katkısı, yoğunluk dengelemesi ve son gönüllü tepkinin konuya etkisini birleştirir. Her terim Jüri görünümünde ayrı ayrı gösterilebilir. Ham olayların 240 kayıtla sınırlandırılması depolama büyümesini kontrol eder; model çağrısı veya ağ bağlantısı olmadan sıralama yapılabildiği için demo gecikmesi ve bağlantı riski düşüktür."
    Set-ParagraphText $document "Etkinlik, uydurma olmayan" "Etkinlik, deterministik jüri senaryosuyla görünür ve tekrar üretilebilir biçimde kanıtlanır. Hazır paket 12 kurgusal aday gönderi ve açıkça 'örnek/demo' olarak etiketlenen 10 davranış sinyali içerir. Tarayıcı önce aynı adayların başlangıç sırasını hesaplar, sinyalleri gerçek recordInteraction/recordPostReaction fonksiyonlarından geçirir, sonra aynı rank fonksiyonunu yeniden çalıştırır. Güncel senaryoda 9 gönderinin konumu değişir; sonuç sabit bir ekran görüntüsü veya hard-code edilmiş son sıra değildir. Karar izi, başlangıç/son sıra, ilgi, dengeleme ve tepki etkisiyle birlikte IndexedDB'de saklanır ve Jüri ekranında gösterilir. İçerik silinmez; hareket yalnızca sıralama düzeyindedir."

    Set-ParagraphText $document "Ürün, fikir düzeyinde" "Ürün fikir düzeyinde kalmayıp çalışan, çok ekranlı ve demo-güvenli bir prototiple desteklenmiştir. Ana akışın yanı sıra gerçek kullanıcı profilleri ve hikâyeler; görsel Keşfet akışı; tepki sonrası alternatif çerçeve öneren Haberler; gerçek yerel olaylardan grafik üreten İçgörü; gönderi oluşturma ve bildirim panelleri; karar izini gösteren ayrı Jüri sayfası çalışır durumdadır. Güncel yenilik, yalnızca duygu sınıflandırması değil, gönüllü geri bildirim + yerel gizlilik + açıklanabilir çok-amaçlı sıralama üçlüsüdür."
    Set-ParagraphText $document "Prototip, bu vizyonun" "Prototip temel mekanizmayı ve jüriye gösterilebilir karar zincirini kanıtlar. Üretim sürümüne geçişte gerçek çok-kullanıcılı kimlik doğrulama, içerik moderasyonu, cihazlar arası isteğe bağlı profil taşıma, uzun dönem A/B testi, gerçek kullanıcı kalibrasyonu ve erişilebilirlik denetimi ayrı iş paketleri olarak ele alınmalıdır. Mevcut demo verisi kurgusaldır ve arayüzde örnek olarak belirtilir; Pexels görsellerinin kaynağı static/assets/explore/CREDITS.md dosyasında belgelenir."
    Set-ParagraphText $document "Gizlilik önceliğinin artırılması" "Gizlilik-öncelikli kişiselleştirme prototipte uygulanmıştır: ham durma süresi, tıklama ve tepki geçmişi IndexedDB'de cihazda tutulur; sunucu aday içerik sağlar. Gelecek aşama, kullanıcı isterse cihazlar arasında güvenli profil taşıma ve toplu model iyileştirmesi için diferansiyel gizlilik/federe öğrenme seçeneklerinin ayrı tehdit modeliyle değerlendirilmesidir."
    Set-ParagraphText $document "Dijital Refah Ağacı" "İçgörü ekranı artık sabit bir metafor yerine gerçek yerel veriden üretilen çizgi ve dağılım grafiklerini içerir: etkileşim ritmi, konu karışımı, gönüllü tepki sayıları ve son demo sıralama hareketi. Gelecekte uzun dönem karşılaştırma için haftalar arası değişim ve kullanıcı/model uyum güven aralığı eklenebilir; düşük örneklemde aşırı yorum yapılmaması temel kuraldır."

    Set-ParagraphText $document "Teknik sürdürülebilirlik iki ayrı" "Teknik sürdürülebilirlik bakım, demo güvenilirliği ve gizlilik sınırı üzerinden ele alınır. Sunucu modelleri periyodik veri-kayması testi gerektirir; yerel ajan ise sürümlü IndexedDB şeması, 240 olaylık üst sınır ve tek düğmeyle sıfırlama sağlar. Küratörlü görsellerin yerel paketlenmesi ve deterministik demo verisi, internet/API kotası kaynaklı yarışma riskini azaltır. FastAPI uç noktaları korunarak arayüz aşamalı geliştirilmiştir; büyük bir framework göçünün getireceği teslim riski bilinçli olarak alınmamıştır. Otomatik pytest kontrolleri backend/demo paketi davranışını, Playwright kontrolleri mobil akışları doğrular."
    Set-ParagraphText $document "Sosyal sürdürülebilirlik açısından" "Sosyal sürdürülebilirlikte kullanıcı kontrolü temel tasarım koşuludur. Sistem davranışı teşhis etmez; yalnızca olası etkileşim örüntüsü ve içerik yoğunluğu dili kullanır. Kullanıcı gönüllü tepkiyle sistemi düzeltebilir, müdahaleyi geçebilir, neden açıklamasını inceleyebilir ve yerel profili silebilir. Haberler akışında amaç kızgınlığı bastırmak değil, aynı gelişmenin daha yapıcı çerçevesini görünür kılarak perspektif çeşitliliği sunmaktır. Üretim öncesi gerçek kullanıcı çalışması, yanlış-pozitif müdahale oranı, müdahale kabul/ret oranı ve kullanıcı/model uyumu ölçülmeden ruh sağlığı faydası iddia edilmeyecektir."

    Set-ParagraphText $document "İP3: Backend/arayüz" "İP3: Mobil ürün, backend ve kullanılabilirlik"
    Set-ParagraphText $document "FastAPI backend, web arayüzü" "FastAPI backend; mobil-öncelikli sosyal akış; profil, hikâye, Keşfet, Haberler ve İçgörü; Playwright düzeltmeleri"
    Set-ParagraphText $document "İP4: Şeffaflık" "İP4: Yerel kişiselleştirme, şeffaflık ve jüri demosu"
    Set-ParagraphText $document "LLM destekli haftalık" "IndexedDB yerel ajanı, gönüllü tepki sistemi, açıklama paneli, karar izi ve deterministik demo paketi"

    $targetHeading = Find-Heading $document "UYGULANABİLİRLİK"
    $selection = $word.Selection
    $selection.SetRange($targetHeading.Range.Start, $targetHeading.Range.Start)
    $selection.Style = $document.Styles.Item("Normal")
    $selection.Font.Name = "Arial"
    $selection.Font.Size = 12
    $selection.Font.Bold = 1
    $selection.TypeText("Prototip Görselleri ve Çalışan Kanıt")
    $selection.TypeParagraph()
    $selection.Font.Bold = 0
    $selection.TypeText("Aşağıdaki ekranlar 23 Ağustos 2026 tarihinde çalışan yerel prototipten, aynı deterministik jüri senaryosu çalıştırılarak alınmıştır. Görseller maket değildir; gösterilen sayılar tarayıcıdaki gerçek demo olay günlüğü ve gerçek sıralama fonksiyonunun çıktısıdır.")
    $selection.TypeParagraph()

    $table1 = $document.Tables.Add($selection.Range, 1, 2)
    $table1.Borders.Enable = 0
    $table1.Rows.AllowBreakAcrossPages = 0
    Add-PictureToCell $table1.Cell(1,1) (Join-Path $assetRoot "01-mobile-feed-demo.png") "Şekil 1. Mobil ana akış ve yerel duygu katmanı." 190
    Add-PictureToCell $table1.Cell(1,2) (Join-Path $assetRoot "02-mobile-reaction-tray.png") "Şekil 2. Karttan bağımsız, dokunmatik Tepki tepsisi." 190
    $selection.SetRange($table1.Range.End, $table1.Range.End)
    $selection.TypeParagraph()

    $table2 = $document.Tables.Add($selection.Range, 1, 2)
    $table2.Borders.Enable = 0
    $table2.Rows.AllowBreakAcrossPages = 0
    Add-PictureToCell $table2.Cell(1,1) (Join-Path $assetRoot "03-explore-reactions.png") "Şekil 3. Keşfet gönderisinde Tepkiler seçimi." 190
    Add-PictureToCell $table2.Cell(1,2) (Join-Path $assetRoot "04-local-insights.png") "Şekil 4. Yerel olaylardan üretilen gerçek İçgörü grafikleri." 190
    $selection.SetRange($table2.Range.End, $table2.Range.End)
    $selection.TypeParagraph()

    $juryPath = Join-Path $assetRoot "05-jury-evidence.png"
    $juryShape = $selection.InlineShapes.AddPicture($juryPath, $false, $true, $selection.Range)
    $juryShape.LockAspectRatio = -1
    $juryShape.Width = 430
    $selection.MoveRight(1) | Out-Null
    $selection.TypeParagraph()
    $selection.Font.Name = "Arial"
    $selection.Font.Size = 9
    $selection.ParagraphFormat.Alignment = 1
    $selection.TypeText("Şekil 5. Jüri görünümü: yerel sinyaller, önce/sonra sıralama ve karar gerekçesi.")
    $selection.TypeParagraph()
    $selection.Font.Size = 12
    $selection.ParagraphFormat.Alignment = 0
    $selection.TypeText("Görsel kanıtın ölçülebilir karşılığı: demo paketinde 12 aday ve 10 hazırlanmış örnek sinyal bulunur; güncel tekrar üretilebilir çalışmada 9 kart yer değiştirmiştir. Tepki kaydı, İçgörü grafikleri ve Jüri karar izi aynı origin altındaki IndexedDB verisini kullanır.")
    $selection.TypeParagraph()

    if ($document.TablesOfContents.Count -gt 0) { $document.TablesOfContents.Item(1).Update() }
    $document.Repaginate()
    $document.Save()
    Write-Output "Updated report: $outputPath"
    Write-Output "Pages: $($document.ComputeStatistics(2))"
    Write-Output "Inline images: $($document.InlineShapes.Count)"
}
finally {
    if ($document) { $document.Close([ref]0) }
    $word.Quit()
}
