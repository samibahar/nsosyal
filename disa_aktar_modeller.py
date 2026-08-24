# -*- coding: utf-8 -*-
"""
Eğitilmiş spiral (lojistik regresyon) ve psikolojik durum (SGDClassifier)
modellerinin katsayılarını static/trained-weights.js'e dışa aktarır.

NEDEN: Arkadaşımızın eklediği local-agent.js, ham davranış verisini (hangi
gönderiye ne kadar bakıldığı) cihazdan hiç çıkarmayan, gerçek bir gizlilik
iyileştirmesi. Ama bunu yaparken sunucudaki EĞİTİLMİŞ modelleri (spiral_model.py,
psikolojik_durum.py) besleyen /api/etkilesim çağrısını da atladığı için, bu
modeller artık boş/donmuş bir günlük üzerinde çalışıyor -- fiilen devre dışı.

ÇÖZÜM: Sunucuya veri göndermek yerine, modelin kendisini (sadece birkaç
düzine sayıdan ibaret: ağırlıklar + kesişim + ölçekleyici ortalama/ölçek)
istemciye taşımak. Lojistik regresyon/SGD çıkarımı (dot product + sigmoid/
softmax) JS'te birkaç satırla yeniden üretilebilir -- bu bir yaklaşıklama
DEĞİL, aynı eğitilmiş modelin birebir aynı matematiği, sadece Python yerine
JS'te çalıştırılıyor. Hiçbir ham etkileşim verisi cihazdan çıkmıyor.
"""
import json

from spiral_model import egit_ve_degerlendir as spiral_egit
from psikolojik_durum import _VARSAYILAN_MODEL, _OLCEKLEYICI, KATEGORILER

spiral_sonuc, _ = spiral_egit()
spiral_model = spiral_sonuc["Lojistik Regresyon"]["model"]

veri = {
    "spiral": {
        "ozellik_sirasi": [
            "negatif_dwell_toplam", "negatif_dwell_orani", "negatif_tekrar_sayisi",
            "ortalama_duygu", "tiklama_orani", "kaydirma_hizi",
        ],
        "coef": spiral_model.coef_[0].tolist(),
        "intercept": float(spiral_model.intercept_[0]),
    },
    "psikolojik": {
        "ozellik_sirasi": ["duygu", "dwell_saniye", "tiklama", "roket", "yorum"],
        "kategoriler": _VARSAYILAN_MODEL.classes_.tolist(),
        "coef": _VARSAYILAN_MODEL.coef_.tolist(),
        "intercept": _VARSAYILAN_MODEL.intercept_.tolist(),
        "olcekleyici_ortalama": _OLCEKLEYICI.mean_.tolist(),
        "olcekleyici_olcek": _OLCEKLEYICI.scale_.tolist(),
    },
}

js_icerik = (
    "// OTOMATIK URETILDI -- disa_aktar_modeller.py ile spiral_model.py ve\n"
    "// psikolojik_durum.py'deki EGITILMIS modellerden dışa aktarıldı. Elle\n"
    "// düzenleme yerine kaynak modeli değiştirip scripti yeniden çalıştırın.\n"
    "window.TrainedModelWeights = " + json.dumps(veri, ensure_ascii=False, indent=2) + ";\n"
)

with open("static/trained-weights.js", "w", encoding="utf-8") as f:
    f.write(js_icerik)

print("static/trained-weights.js yazildi.")
print("spiral dogruluk:", round(spiral_sonuc["Lojistik Regresyon"]["dogruluk"], 3))
