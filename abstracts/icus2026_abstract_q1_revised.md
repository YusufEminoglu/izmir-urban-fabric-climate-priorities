# ICUS 2026 Abstract — Q1-Calibre Revision (CMT-ready)

> Blind submission body: no author names, affiliations, references or figures inside the
> abstract text. Literature grounding for every claim is documented separately in
> `docs/submission/icus2026_literature_positioning_dossier.md`.
>
> Canonical source of this text: `scripts/build_icus2026_submission_ready_pdf.py` (this file is
> generated from it; keep this file in sync after editing the script). Word counts: Turkish 706,
> English 750 (both within the 500–750 rule). Full-census revision: 3,777 cells, four super-types, ARI 0.38.
>
> Status: draft for author verification. Per the congress AI-ethics rule, the author must read,
> verify and own the final prose before submitting to CMT.

---

## TURKISH TITLE

Kentsel Doku Morfometrisi ve İklim Dirençliliği: İzmir İşlevsel Kent Bölgesi İçin Açıklanabilir ve Pareto-Uyumlu Karar Destek Protokolü

## TURKISH ABSTRACT

Kentsel morfometri, yapılı formu ulusal ve küresel ölçeklerde sınıflandırabilen, yinelenebilir ve denetimsiz bir bilime olgunlaşmış; buna koşut olarak iklim-kent yazını kentsel formu yer yüzey sıcaklığının, ısı kırılganlığının ve plüvyal taşkın güzergâhlarının birincil belirleyicisi olarak ele almaya başlamıştır. Ancak bu iki yazın, uyumun bir metropol bölge ölçeğinde planlandığı düzeyde nadiren buluşur. İklim dirençliliği hâlâ idari birimler, kaba ızgaralar veya yerel iklim bölgeleri üzerinden değerlendirilmekte; böylece benzer yoğunluğa sahip iki alan aynı risk sınıfına atanırken belirgin biçimde farklı ısı, erişim ve kırılganlık sonuçları üretebilmektedir. Bu çalışma, İzmir işlevsel kent bölgesi için tüm kentsel hücreleri kapsayan (tam sayım) 250 metrelik bir analiz gridi üzerine kurulu; morfometriyi çoklu tehlike maruziyeti ve sosyal kırılganlıkla açık iki aşamalı bir mantıkla birleştiren; açık kaynaklı, denetlenebilir ve QGIS tabanlı bir tipomorfolojik iş akışı önerir: açıklanabilir makine öğrenmesi ölçülen bir ısı çıktısını morfolojik mekanizmalara bağlar, çok amaçlı (Pareto) optimizasyon ise bu mekanizmaları sağlam ve ödünleşim-farkında uyum önceliklerine dönüştürür. Katkı, tamamlanmış bir atlas değil, tek bir işlevsel kent bölgesinde tam-sayım ölçeğinde gösterilen aktarılabilir ve test edilebilir bir protokoldür; betimleyici yalnızca-form tipolojilerinden ve idari direncilik indekslerinden ayrışır.

Çerçevenin özü, kentsel dokunun üç boyutunu ayırır: tip olarak doku (betimleyici bir sınıf), ölçüm olarak doku (morfometrik gösterge vektörü) ve mekanizma olarak doku (formun iklim riskini düzenlediği güzergâh). Bu ayrım, eşit yoğunluktaki alanların neden farklı dirençlilik sonuçları ürettiği sezgisini sınanabilir bir önermeye dönüştürür.

Görgül tasarım, İzmir bölgesi üzerinde 250 metrelik bir analiz gridine dayanır. Kentsel olmayan (düşük yapılı alan oranlı), açık su ve dik eğimli alanlar dışlandıktan sonra kalan hücreler yedi önsel doku stratumuna (tarihsel merkez, ızgara konut, apartman bloğu, kıyı dönüşüm, yamaç/eğimli, sanayi-lojistik ve çeper genişleme) atanır; tüm kalan hücreler analize girer (tam sayım; örnekleme yok). Stratumlar, kümeleme öncesinde arazi kullanımı ve uzaktan algılama temelli kural-tabanlı (geçici) vekillerle tanımlanır; kümeleme bu sınıflamayı üretmek yerine sınar ve geliştirir, böylece örneklem-tipoloji döngüselliği önlenir.

Analiz birimi her 250 metrelik grid hücresidir. Yapı ayak izleri morfolojik tessellation hücrelerine, temizlenmiş yol merkez çizgileri segment grafına dönüştürülür; hücre ölçeğindeki morfometri ve ağ göstergeleri alan ağırlıklı ortanca, çeyrekler arası açıklık ve yoğunluk ölçüleriyle grid hücresine çapraz aktarılırken, her hücre çevresindeki 400 ve 800 metrelik ağ servis alanı menzilleri erişilebilirliği ve hareket potansiyelini taşır. Yöntemin özü tekil araçlar değil bu çapraz aktarım kuralıdır: yapılı form yoğunluğunu, hareket potansiyelini ve tehlike maruziyetini koşut katmanlar yerine tek bir hücrede karşılaştırılabilir kılar.

Zincir, PlanX Urban Resilience ve GeoStats Lab'i birleştiren bir QGIS projesinde çalışır. Girdiler açık veri ve belediye veri portallarıdır: yol ağı ve bina ayak izleri OpenStreetMap ile İzmir Büyükşehir Belediyesi (İBB) veri portalından; arazi örtüsü ve yer yüzey sıcaklığı Copernicus ve Landsat'tan; yeşil-mavi altyapı, toplanma alanları ve hizmetler belediye verilerinden; sosyal kırılganlık ise TÜİK ADNKS yaş ve bağımlılık verilerinden türetilir. Hedeflenen stresörler aşırı sıcak, plüvyal taşkın ve kıyı maruziyetidir. Geçirimsiz yüzey maruziyeti doğrudan arazi örtüsünden ölçülür.

Ağ metrikleri (OSMnx/NetworkX; angular integration ve choice) ve morfometrik karakterler (momepy/GeoPandas: taban alanı oranı, açıklık, kompaktlık, cephe sürekliliği, blok geçirgenliği, hücre heterojenliği) iklim-direncilik vekilleriyle tamamlanır: gölge ve güneşlenme potansiyeli, yeşil-mavi soğutma, toplanma alanı ve günlük hizmet erişimi ve geçirimsiz maruziyet ile sosyal kırılganlığın örtüşmesi. Mekânsal yapı, Moran's I, LISA, Getis-Ord sıcak noktalar ve maruziyet eşitsizliğinin Gini ölçüsüyle incelenir.

Sentez açıkça iki aşamalıdır. Önce, tüm kentsel hücreler boyunca havuzlanmış ince ölçekte açıklanabilir bir gradient-boosting modeli ölçülen yer yüzey sıcaklığını morfometrik ve konfigürasyonel sürücülerden tahmin eder; Shapley (SHAP) ataması her dokuda ısıyı hangi mekanizmanın sürüklediğini belirler. Ardından göstergeler yön kodlu ve z-standartlaştırılır, temel bileşen analizi eşdoğrusallığı azaltır ve Ward hiyerarşik kümeleme doku-direncilik profilleri üretir; küme sayısı silhouette skoruyla, çözünürlük kararlılığı ise 250'ye karşı 500 metre gridler arasında Düzeltilmiş Rand İndeksiyle sınanır. İkinci olarak uyum öncelikleri çok amaçlı bir problem olarak kurulur: Pareto-optimal cephe, baskın-altı hücreleri (açık müdahale adayları) ödünleşim hücrelerinden ayırır; TOPSIS bir sıralama verir, entropi ağırlığı ve Monte-Carlo pertürbasyonları sağlamlığı raporlar. İzmir işlevsel kent bölgesinin 3.777 kentsel hücresinin tamamı üzerinde (tam sayım) zincir uçtan uca yürütülmüştür. Yedi ön-tanımlı doku, TBA ve Ward kümelemeyle dört sağlam morfometrik üst-tipe yoğunlaşır; sınıflandırma 250'ye karşı 500 metre çözünürlükte geniş hatlarıyla kararlıdır (ARI=0,38). Açıklanabilir ısı modeli, metropolitan ölçekte kıyı gradyanının yaz yer yüzey sıcaklığını formdan daha güçlü kontrol ettiğini ortaya koyar; ancak morfolojik mekanizmalar ayırt edilebilirdir. En çarpıcı bulgu, ısı, erişim, kıyı maruziyeti ve sosyal kırılganlık birlikte değerlendirildiğinde, en serin doku olan kıyı dönüşümünün en yüksek uyum önceliği olarak sıralanmasıdır—yalnızca ısıya dayalı bir değerlendirmenin tam tersine. Tüm parametreler, katmanlar ve kodlar aktarılabilirlik için paylaşılır.

## TURKISH KEYWORDS

kentsel morfometri; yaya erişilebilirliği; sosyal kırılganlık; hiyerarşik kümeleme; çok ölçütlü karar analizi

---

## ENGLISH TITLE

Urban Fabric Morphometrics and Climate Resilience: An Explainable, Pareto-Aware Decision Support Protocol for the İzmir Functional Urban Region

## ENGLISH ABSTRACT

Urban morphometrics has matured into a reproducible, unsupervised science that classifies built form at national and global scales, while a parallel literature treats urban form as a first-order control on land-surface temperature, heat vulnerability and pluvial-flood pathways. These trajectories rarely meet at the metropolitan planning scale. Resilience is often assessed over coarse administrative or climate zones, assigning areas of similar density to the same risk class despite different thermal and accessibility outcomes. This study proposes an open-source, auditable, QGIS-based typomorphological workflow for the İzmir functional urban region, applied as a full census on a 250-metre grid, that couples morphometrics with multi-hazard exposure and social vulnerability through a two-stage logic: explainable machine learning attributes a measured thermal outcome to morphological mechanisms, and multi-objective (Pareto) optimisation turns those mechanisms into robust, trade-off-aware adaptation priorities. The contribution is a transferable, testable protocol demonstrated at full-census scale over one functional urban region, and is distinguished from both descriptive form-only typologies and administrative resilience indices.

The framework separates three senses of urban fabric: fabric-as-type (a descriptive taxon), fabric-as-measurement (a morphometric vector) and fabric-as-mechanism (the pathway through which form modulates risk). This distinction turns the intuition that equally dense areas differ in resilience outcomes into a testable proposition.

The design uses a 250-metre analysis grid over the İzmir functional urban region. After excluding non-urban (low built fraction), open water, and steep-slope cells, the remainder are assigned to seven a priori strata (historic core, grid residential, apartment-block, waterfront transformation, hillside/incremental, industrial-logistics, peripheral expansion). All retained cells are analysed: the study is a full census of the 3,777 urban cells, not a sample. Strata are defined a priori from land use and remote sensing as rule-based (provisional) proxies before clustering, which tests and refines this classification rather than generating it, avoiding circularity.

Each 250-metre grid cell is the analytical unit. Building footprints are converted into morphological tessellation cells and cleaned road-centre lines into a segment graph; cell-level morphometrics and network metrics are cross-attributed to the grid cell through area-weighted median, interquartile range and density measures, while 400- and 800-metre network service-area reaches carry accessibility and movement potential. The cross-attribution rule, not the tools, is the methodological core: it makes built-form intensity, movement potential and hazard exposure commensurable within one cell rather than as parallel layers.

The workflow runs in a QGIS project combining PlanX Urban Resilience and GeoStats Lab. All inputs are public open data: street networks and building footprints from OpenStreetMap and the İzmir Metropolitan Municipality (BBB); land cover and land-surface temperature from Copernicus and Landsat; green-blue infrastructure, coastline, assembly areas and services from municipal portals; and social vulnerability from Turkish Statistical Institute/ADNKS age and dependency ratios. Target stressors are extreme heat, pluvial flooding and coastal exposure. Impervious exposure is measured directly from satellite land cover, not inferred from building density.

Synthesis is explicitly two-stage. First, an explainable gradient-boosting model is trained at fine scale, pooled across all urban cells, to predict measured land-surface temperature from morphometric and configurational drivers; Shapley (SHAP) attribution identifies which mechanism dominates heat in each fabric. Indicators are then z-standardised, principal component analysis reduces collinearity, and Ward hierarchical clustering yields fabric-resilience profiles, with cluster number set by silhouette score and resolution stability tested between 250- and 500-metre grids via the Adjusted Rand Index. Second, adaptation priorities are framed as a multi-objective problem: a Pareto-optimal frontier separates dominated cells from trade-off cells, while TOPSIS provides a ranking and robustness is evaluated. Over a full census of all 3,777 urban cells of the İzmir region, the chain runs end to end. The seven a-priori strata consolidate into four robust morphometric super-types via PCA and Ward clustering, broadly stable across grid resolution (ARI = 0.38). The explainable heat model shows that, at metropolitan scale, the coastal gradient controls summer land-surface temperature more strongly than form, which is nonetheless a secondary but genuine control, with morphological mechanisms remaining identifiable. The sharpest finding is an equity inversion: when heat, access, coastal exposure and social vulnerability are assessed jointly, the coolest fabric—waterfront transformation—ranks as the highest adaptation priority, the opposite of a heat-only reading. All parameters, layers and code are released for transfer.

## ENGLISH KEYWORDS


## What changed and why it reads at Q1 level (v3 — grid-based functional-region design)

1. **Literature-grounded gap.** Opening states the live 2024–2026 tension: morphometrics is now
   scalable/unsupervised/reproducible (Fleischmann; Araldi & Fusco 2024; Debray et al. 2025), and
   climate-urban work shows form is a first-order control on heat/flood/vulnerability (Wang et al.
   2025; Turner et al. 2025; Iqbal et al. 2025) — yet the two rarely meet at the scale adaptation is
   planned across a metropolitan region.
2. **The "same density, different outcome" hook is motivated** (Iqbal et al. 2025; Wang, Zhou & Yu
   2025), and the three senses of *urban fabric* (taxon / measurement / mechanism) are disambiguated.
3. **Headline method unit — "explain → optimize".** Explainable gradient boosting + **SHAP** on a
   **measured** outcome (land-surface temperature) names each fabric's dominant heat mechanism;
   **multi-objective (Pareto)** optimisation + TOPSIS + entropy/Monte-Carlo robustness turns
   mechanisms into trade-off-aware priorities. Anchors: Wang/Liu/Li 2025-26 (SHAP-LST);
   Zhang 2024 & Zhu 2025 (Pareto).
4. **NEW spatial design (v3):**
   - **Unit:** a sampled **250 m analysis grid** (INSPIRE/GHSL-aligned) — deliberately a square grid,
     distinct from hex/node designs; 250 m matches Landsat LST resolution (robust heat signal) and is
     reproducible. Grid-resolution stability is tested 250 vs 500 m via the Adjusted Rand Index.
   - **Extent:** the **İzmir functional urban region** (metropolitan), stratified by seven a-priori
     fabric types and spatially balanced sampled.
   - **Integration:** the cross-attribution rule is retargeted to the grid (tessellation cells +
     network + hazard → grid cell); 400/800 m become per-cell accessibility *reaches*.
5. **Statistical dimension via GeoStats Lab:** Moran's I, LISA, Getis-Ord hot spots and a **Gini
   of the exposure–vulnerability burden** (an equity axis), plus Monte-Carlo sensitivity — an
   open, auditable, QGIS-native statistics layer alongside PlanX Urban Resilience. (MGWR is deferred
   to the full journal study; the journal version drops the earlier spatial-Gini decomposition as an artefact.)
6. **All inputs are public open data** (OpenStreetMap, Copernicus/ESA, Landsat LST, TÜİK).
   The blind body names no other project. Related-work / shared-open-data disclosure for the journal
   track is documented in the literature dossier (§6) — distinct unit, DV, method and question keep
   this a genuinely separate study.

Full claim-by-claim citation mapping and verified DOIs: `docs/submission/icus2026_literature_positioning_dossier.md`.
