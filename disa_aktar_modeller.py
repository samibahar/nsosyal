# -*- coding: utf-8 -*-
"""
Eğitilmiş spiral (lojistik regresyon) ve psikolojik durum (SGDClassifier)
modellerinin katsayılarını static/trained-weights.js'e dışa aktarır.

NEDEN: local-agent.js ham davranış verisini (hangi gönderiye ne kadar
bakıldığı) cihazdan hiç çıkarmıyor. Sunucuya veri göndermek yerine modelin
kendisi (birkaç düzine sayı: ağırlıklar, kesişim, ölçekleyici ortalama/ölçek)
istemciye taşınıyor; çıkarım JS'te aynı matematikle yapılıyor.

Spiral modelinin özellik sabitleri (pencere, yarı ömür, okuma hızı...) de
buradan yazılır; tarayıcı bunları spiral_ozellik.py'den kopyalamaz, tek kaynak
Python tarafıdır.
"""
import json

import spiral_ozellik
from spiral_model import egitilmis
from psikolojik_durum import _VARSAYILAN_MODEL, _OLCEKLEYICI

spiral = egitilmis()

veri = {
    "spiral": {
        "surum": 2,
        "ozellik_sirasi": spiral_ozellik.OZELLIK_ADLARI,
        "coef": spiral["model"].coef_[0].tolist(),
        "intercept": float(spiral["model"].intercept_[0]),
        "olcekleyici_ortalama": spiral["olcekleyici"].mean_.tolist(),
        "olcekleyici_olcek": spiral["olcekleyici"].scale_.tolist(),
        "parametreler": spiral_ozellik.PARAMETRELER,
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
