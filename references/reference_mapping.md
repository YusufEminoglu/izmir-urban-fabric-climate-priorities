# ICUS 2026 PlanX Urban Resilience — Reference Mapping Guide

Bu doküman, `paper/manuscript/src/refs.bib` içindeki **DOI-doğrulanmış** literatürün makalenin
hangi bölümlerinde (alt-bölümler) kullanılacağını gösteren stratejik haritadır. Tam tablo
(her kaynağın yıl/dergi/DOI/başlık dökümü) için bkz. `references/reference_index.md`;
doğrulama kanıtları için bkz. `references/verification/`.

**Doğrulama kuralı:** Her `@article` kaydı DOI'si üzerinden Crossref'ten çekildi; DOI==DOI, dergi
tipi (`journal-article`) ve Q1-aday dergi kontrolü zorunlu tutuldu. Ardından kayıtlar `.bib`'ten
yeniden ayrıştırılıp Crossref (kontrol 2) ve OpenAlex'e (kontrol 3) karşı bağımsız olarak yeniden
sorgulandı; başlık/yıl/dergi her iki serviste de eşleşmeyen tek bir kayıt kalmadı
(`independent_verification_report.md`: **68/68 PASS, 0 FAIL**).

**Dergi-düzeyi notu:** Kaynaklar Q1-*aday* dergi olarak işaretlendi; nihai WOS/JCR çeyreklik
doğrulaması gönderim öncesi kurumsal erişimle yapılmalıdır.

**Sayım:** 68 doğrulanmış dergi referansı + 2 yazar-yazılım atfı
(`eminoglu2026planxresilience`, `eminoglu2026planxgeostats`).

---

## 1. Giriş (Introduction)

**Alt-bölüm 1.1 — İklim dirençliliği ve kentsel form sorunsalı**
- **Referanslar:** `hamin2009UrbanForm`, `reckien2018CitiesPlanning`, `chu2025EvaluatiCities`, `o2026CitiesNeed`
- **Bağlam:** Kentsel formun iklim uyumu ile azaltımı arasındaki dengeyi (Hamin & Gurran), 885 AB
  kentinin plan değerlendirmesini (Reckien) ve uyum planlamasında dağıtımsal adalet/bütünleşik
  sağlık yaklaşımını (Chu; O'Donnell) çerçevelemek için. Açık-kaynak, tekrarlanabilir bir tarama
  iş akışının neden gerekli olduğunu gerekçelendirir.

**Alt-bölüm 1.2 — Araştırma boşluğu ve katkı**
- **Referanslar:** `fleischmann2022EvolutioUrban`, `boeing2022StreetNetwork`, `rupp2026WhereHeat`
- **Bağlam:** Kentsel morfolojinin "açık, tekrarlanabilir veri bilimi"ne dönüşümü ve açık-kaynak
  ısı-riski endeksleri; PlanX iş akışının bu açık-bilim damarına nasıl oturduğunu konumlandırır.

## 2. Literatür (Literature Review)

**Alt-bölüm 2.1 — Kentsel morfometri ve niceliksel kentsel form**
- **Referanslar:** `dibble2019OriginSpaces`, `fleischmann2021MeasurinUrban`, `fleischmann2022MethodolFoundati`, `fleischmann2022EvolutioUrban`, `wu2022CultivatHistoric`
- **Bağlam:** Niteliksel tipo-morfolojiden sayısal taksonomiye geçiş; morfometrik karakterlerin
  (kompaktlık, kapsama, çevre/alan) standartlaştırılması. Çalışmadaki örüntü-örneklemesinin
  metodolojik temeli.

**Alt-bölüm 2.2 — Sokak-ağı konfigürasyonu ve space syntax**
- **Referanslar:** `porta2012StreetCentrali`, `araldi2019FromStreet`, `boeing2020MultiScale`, `boeing2020PlanaritStreet`, `pafka2020LimitsSpace`, `araldi2025MultiLevel`
- **Bağlam:** Merkeziyet/bütünleşme ölçütleri, sokak-temelli (street-based) çoklu ölçek analizi ve
  space syntax'in tasarım sınırları (Pafka). PlanX ana modüllerindeki ağ-merkeziyet ve segment
  analizi seçimlerini gerekçelendirir.

**Alt-bölüm 2.3 — Yapılı-form yoğunluğu (Spacematrix mantığı)**
- **Referanslar:** `li2020InfluencDensity`, `lu2019ExplorinAssociat`, `bobkova2021TowardsAnalytic`
- **Bağlam:** Yoğunluk (FSI/GSI/kapsama) ile mikroklima/maruziyet arasındaki ilişki; parsel
  sistemlerinin niceliksel profili. Spacematrix-türü yoğunluk betimleyicilerinin dirençlilikle bağı.

**Alt-bölüm 2.4 — Kentsel doku tipolojisi ve sınıflandırma**
- **Referanslar:** `bobkova2021TowardsAnalytic`, `yu2023UrbanNeighbou`, `venerandi2024UrbanForm`, `govind2024DelineatNeighbor`, `araldi2025MultiLevel`
- **Bağlam:** Çok-ölçekli mahalle sınıflandırması ve morfometrik kümeleme. İzmir Körfezi
  transektindeki doku arketiplerinin (tarihi çekirdek, ızgara, apartman dokusu, yamaç, vb.)
  kümeleme tasarımının dayanağı.

**Alt-bölüm 2.5 — Kentsel dirençlilik ve çoklu-afet çerçevesi**
- **Referanslar:** `balica2012FloodVulnerab`, `chan2018TowardsResilien`, `bush2019BuildingUrban`, `wang2019LocalFloods`, `liu2025HomogeneHeteroge`
- **Bağlam:** Kıyı kentlerinde sel-kırılganlık endeksi, dirençli sel yönetimi, doğa-temelli
  çözümlerle dirençlilik ve yol-ağlarının afet-kaynaklı çöküşü. Çoklu-afet sentez modülünün
  kavramsal çerçevesi.

## 3. Çalışma Alanı ve Veri (Study Area & Data)

**Alt-bölüm 3.x — İzmir / Akdeniz / kıyı bağlamı + açık veri**
- **Referanslar:** `bhuyan2023MappingCharacte`, `venter2020HyperlocMapping`, `boeing2022StreetNetwork`
- **Bağlam:** Açık-kaynak veri + yapay zekâ ile bina/sel maruziyeti envanteri, açık sokak-ağı
  modelleri ve kalabalık-kaynaklı sıcaklık verisi. İzmir veri envanterinin (OSM, DEM, nüfus)
  açık-veri gerekçesi.

## 4. Yöntem (Methodology) — Açık-kaynak QGIS iş akışı

**Alt-bölüm 4.1 — Açık-kaynak / tekrarlanabilir morfometri ekosistemi**
- **Referanslar:** `fleischmann2019MomepyUrban`, `fleischmann2022EvolutioUrban`, `boeing2022StreetNetwork`
- **Yazılım atıfları:** `eminoglu2026planxresilience`, `eminoglu2026planxgeostats`
- **Bağlam:** PlanX'i QGIS morfometri ekosistemi içinde (momepy, OSMnx hattıyla yan yana)
  konumlandırır. **Bu çalışmanın özgün araç katkısı burada ilk kez atıf alır** (aşağıdaki
  "Yazılım Atıfları" bölümüne bakınız).

**Alt-bölüm 4.2 — Isı maruziyeti, SVF ve termal mekanizmalar**
- **Referanslar:** `guo2016CharacteImpact`, `middel2018ViewFactor`, `huang2019InvestigEffects`, `guo2020ImpactUrban`, `li2020InfluencDensity`, `jeon2023ImpactsUrban`
- **Bağlam:** 2D/3D morfoloji–LST ilişkisi, SVF ayak izi ve ızgara vs. blok-temelli LST
  karşılaştırması. PlanX ısı-konfor modülünün ve morfolojik sürücülerin gerekçesi.

**Alt-bölüm 4.3 — Sosyal kırılganlık ve eşitlik**
- **Referanslar:** `aroca2017ConstrucIntegrat`, `sabrin2020DevelopiVulnerab`, `venerandi2024UrbanForm`
- **Bağlam:** Bütünleşik sosyal kırılganlık endeksi ve eşitlik-düzeltmeli uyum önceliği. PlanX
  Social Vulnerability Index + Equity-Adjusted Adaptation Priority modüllerinin temeli.

**Alt-bölüm 4.4 — Erişilebilirlik, yürünebilirlik ve acil erişim**
- **Referanslar:** `tannous2021AccessibGreen`, `de2023UnderstaPredicti`, `govind2024DelineatNeighbor`
- **Bağlam:** Ağ-temelli erişilebilirlik, yeşil-alan erişimi (space syntax ile) ve sokak-arayüzü
  analizi. PlanX Network/Emergency Accessibility modüllerinin dayanağı.

**Alt-bölüm 4.5 — Mekânsal istatistik (Gi*, LISA, GWR)**
- **Referanslar:** `sanchez2019SpotAnalysis`, `purwanto2021SpatioteAnalysis`, `zhao2018GeographWeighted`
- **Yazılım atfı:** `eminoglu2026planxgeostats`
- **Bağlam:** Hot-spot (Getis-Ord Gi*), küme/aykırı (LISA) ve coğrafi-ağırlıklı regresyon (GWR).
  **PlanX GeoStats Lab'in** açığa çıkardığı yöntemlerin literatür temeli; burada GeoStats eklentisi
  atıf alır.

## 5. Bulgular (Results)

- **Referanslar:** `guo2020ImpactUrban`, `marando2022UrbanHeat`, `massaro2023SpatiallOptimize`, `jeon2023ImpactsUrban`
- **Bağlam:** Doku-tipi başına LST/maruziyet farklılaşması ve yeşil-altyapı azaltım etkisi
  bulgularını dış vaka çalışmalarıyla kıyaslamak için.

## 6. Tartışma ve Sonuç (Discussion & Conclusions)

**Alt-bölüm 6.1 — Yeşil altyapı ve doğa-temelli serinletme**
- **Referanslar:** `yu2020CriticalReview`, `schwaab2021RoleUrban`, `marando2022UrbanHeat`, `massaro2023SpatiallOptimize`
- **Bağlam:** Mavi-yeşil alanların serinletme eşiği, kentsel ağaçların LST düşürücü rolü ve
  nüfus-maruziyetini azaltan mekânsal-optimal yeşillendirme. ECO-senaryo önerilerinin dayanağı.

**Alt-bölüm 6.2 — Uyum planlaması ve politika çevirisi**
- **Referanslar:** `geneletti2016EcosysteBased`, `wamsler2020EnvironmClimate`, `babi2021NexusBetween`, `chu2025EvaluatiCities`, `o2026CitiesNeed`, `rupp2026WhereHeat`
- **Bağlam:** Ekosistem-temelli uyum, politika bütünleştirme, NbS-ekosistem hizmetleri bağı ve
  açık-kaynak ısı-riski endekslerinin transfer edilebilirliği. Öncelik sınıflarının planlama
  diline çevrilmesi.

---

## Yazılım Atıfları (Author Software) — eklentilere ilk atıf nasıl yapılır?

İlk kez kendi QGIS eklentilerine atıf yapıyorsun. Eklentiler **hakemli makale değil, yazılımdır**;
bu yüzden DOI-doğrulamalı dergi listesinden ayrı tutuldu ve `refs.bib` sonunda `@software` tipiyle,
**GitHub deposu + sürüm + erişim tarihi** ile verildi. Metadata her eklentinin `metadata.txt`
dosyasından harfi harfine alındı.

> **Önemli:** En kalıcı/atıf-dostu yol bir **DOI** almaktır. GitHub deposunu
> [Zenodo](https://zenodo.org) ile bağlayıp bir *release* yayınlarsan Zenodo sürüm-spesifik bir DOI
> üretir; sonra `@software` kaydına `doi = {...}` ekleyip bu kaynağı da DOI-doğrulama hattından
> geçirebilirsin. Resmî QGIS Plugin Hub sayfaları da (`plugins.qgis.org/plugins/<ad>/`) `url`
> olarak eklenebilir. Şimdilik GitHub deposu birincil kaynak.

**1) PlanX: Urban Resilience** — bu çalışmanın ana dirençlilik tarama paketi.
```bibtex
@software{eminoglu2026planxresilience,
  author       = {Eminoglu, Yusuf},
  title        = {{PlanX: Urban Resilience -- a QGIS Processing suite for city-scale multi-hazard resilience screening}},
  year         = {2026},
  version      = {1.25.0},
  publisher    = {QGIS Python Plugins Repository},
  howpublished = {QGIS plugin},
  url          = {https://github.com/YusufEminoglu/planx_urban_resilience},
  note         = {Version 1.25.0. Accessed 14 June 2026}
}
```
- **Metinde ilk atıf:** Yöntem 4.1'de iş akışı tanıtılırken: "…dirençlilik göstergeleri açık-kaynak
  PlanX: Urban Resilience QGIS eklentisiyle (sürüm 1.25.0; \citep{eminoglu2026planxresilience})
  üretildi."

**2) PlanX GeoStats Lab** ("gestats") — mekânsal istatistik (Gi*, LISA, GWR/MGWR) modülleri.
```bibtex
@software{eminoglu2026planxgeostats,
  author       = {Eminoglu, Yusuf},
  title        = {{PlanX GeoStats Lab -- spatial statistics tools for QGIS planning workflows}},
  year         = {2026},
  version      = {0.9.17},
  publisher    = {QGIS Python Plugins Repository},
  howpublished = {QGIS plugin},
  url          = {https://github.com/YusufEminoglu/planx_geostats},
  note         = {Version 0.9.17. Accessed 14 June 2026}
}
```
- **Metinde ilk atıf:** Yöntem 4.5'te: "…hot-spot (Gi*), LISA ve GWR analizleri PlanX GeoStats Lab
  eklentisiyle (sürüm 0.9.17; \citep{eminoglu2026planxgeostats}) yürütüldü."

**Etik notu (project_guide §7):** Kongre sayfası katı yapay-zekâ/intihal uyarısı içeriyor. Bu harita
ve .bib bir *destek* aracıdır; nihai metin yazar tarafından yeniden yazılmalı, atıflar PDF'ten
teyit edilmeli ve sahiplenilmelidir.
