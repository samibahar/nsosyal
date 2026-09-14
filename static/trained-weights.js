// OTOMATIK URETILDI -- disa_aktar_modeller.py ile spiral_model.py ve
// psikolojik_durum.py'deki EGITILMIS modellerden dışa aktarıldı. Elle
// düzenleme yerine kaynak modeli değiştirip scripti yeniden çalıştırın.
window.TrainedModelWeights = {
  "spiral": {
    "surum": 2,
    "ozellik_sirasi": [
      "yogun_pay",
      "goreli_oyalanma",
      "yogun_fazla_kalma",
      "aktif_oran"
    ],
    "coef": [
      0.0,
      1.5613791629624274,
      0.0,
      -0.8511704323524601
    ],
    "intercept": -0.847848322040859,
    "olcekleyici_ortalama": [
      0.38310258943355613,
      0.3700859742695236,
      0.5870955900367274,
      0.11098042253720718
    ],
    "olcekleyici_olcek": [
      0.2786068659701715,
      0.5615202627157339,
      0.637781790466962,
      0.11064383354402015
    ],
    "parametreler": {
      "pencere_saniye": 1800,
      "yari_omur_saniye": 600,
      "maks_gonderi": 20,
      "min_gonderi": 3,
      "yogun_ton": -0.2,
      "okuma_taban": 1.5,
      "kelime_hizi": 3.5,
      "varsayilan_kelime": 12,
      "oran_ust": 4.0,
      "fazla_ust": 3.0,
      "goreli_pay": 0.1,
      "goreli_ust": 2.0
    }
  },
  "psikolojik": {
    "ozellik_sirasi": [
      "duygu",
      "dwell_saniye",
      "tiklama",
      "roket",
      "yorum"
    ],
    "kategoriler": [
      "anksiyete",
      "mutluluk",
      "sakin",
      "sinirli",
      "umut"
    ],
    "coef": [
      [
        -2.3956028845645947,
        -0.25662330890618107,
        -0.5177216456292133,
        -1.1401099585352872,
        -0.3783086987893429
      ],
      [
        2.7057422080496267,
        -1.1236590293137654,
        0.31005288571210926,
        0.6486469935637205,
        0.722994550594779
      ],
      [
        0.9315558699898073,
        -1.9914835280204457,
        -1.1897892305429338,
        -1.407169944150278,
        -0.417631389809781
      ],
      [
        -2.114418692882867,
        0.44491035143271335,
        0.5335072895211018,
        0.765423213464837,
        0.32355025766048107
      ],
      [
        1.009248028000805,
        1.4347813516411514,
        0.2675578602825997,
        -0.9504085504822556,
        -0.9117356675963806
      ]
    ],
    "intercept": [
      -2.4772421235689728,
      -3.0240956201345766,
      -2.666774659443303,
      -2.751285434878612,
      -2.7660064477894064
    ],
    "olcekleyici_ortalama": [
      -0.004171603951541071,
      4.132334757488416,
      0.2592,
      0.2634666666666667,
      0.18986666666666666
    ],
    "olcekleyici_olcek": [
      0.5995983782229258,
      4.202925154140149,
      0.43819557277544124,
      0.44051331673653255,
      0.39219550680184206
    ],
    "dwell_ust": 15.0
  }
};
