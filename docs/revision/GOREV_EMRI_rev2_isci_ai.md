# GÖREV EMRİ — ICUS2026 Makale Revizyonu (rev2)

> **Rol dağılımı:** Bu dosya LİDER (beyin) ajan tarafından yazıldı. Sen İŞÇİ ajansın.
> Bu emirdeki görevleri uygula, sonunda **Bölüm 8'deki rapor kontratına birebir uyan**
> kapsamlı bir `.md` raporu yaz. Rapor lider tarafından denetlenecek; eksik veya
> doğrulanmamış iş reddedilir.

---

## 0. Ortam, kaynaklar ve temel kurallar

**Çalışma dizini (source of truth):**
`C:\Users\YE\PyCharmMiscProject\icus2026_planx_urban_resilience\paper\manuscript\src\`

| Ne | Yol |
|---|---|
| Ana belge | `src/main.tex` (bölümleri `src/sections/*.tex` içinden `\input` eder) |
| Başlık + özet | `src/sections/titleAbstract.tex` |
| Ayrı kapak sayfası | `src/title_page.tex` (ayrı derlenir) |
| Beyanlar (yazar katkısı) | `src/sections/declarations.tex` |
| Preamble | `src/mypreamble.sty` (`amsmath` **zaten yüklü**, denklem için ek paket gerekmez) |
| Kaynakça | `src/refs.bib` (apalike/natbib) |
| Şekil PNG'leri | `outputs/figures/` (graphicspath oradan okur) |
| Şekil verileri (geometrili) | `outputs/figure_gpkgs/figure_XX_*.gpkg` + `figure_gpkg_manifest.csv` |
| Şekil üretim betikleri | `scripts/make_*.py`, `scripts/generate_all_figures.py`, ortak stil: `scripts/_manuscript_style.py` |
| Analiz hattı (sayı üretir) | `scripts/pilot_01..14_*.py`, kanonik sayılar: `scripts/report_canonical_numbers.py` |
| Çıktı tabloları | `outputs/tables/*.csv` |

**Kurallar (ihlali = ret):**

1. **Analiz sayılarına dokunma.** Tablo 2 / Tablo 3 değerleri, R², ARI=0.38, Gini=0.26,
   Moran I değerleri, 223 hücrelik frontier, N=3.777 vb. tüm kanonik sayılar sabittir.
   Şekil yeniden üretirken bu sayıların değişmediğini doğrula
   (`scripts/report_canonical_numbers.py` ile karşılaştır).
2. **Referans uydurma yasak.** Yeni atıf eklenecekse DOI'si Crossref'ten
   (`https://api.crossref.org/works/<doi>`) doğrulanmadan `refs.bib`e giremez.
   Başlık/yazar/yıl/dergi birebir Crossref kaydıyla eşleşmeli. (Bu projenin yerleşik kuralıdır;
   `references/verification/` klasöründeki raporlara bak.)
3. **ORCID / akademik unvan uydurma yasak.** 3. yazar için bilinmeyen alanlara `TODO`
   işareti koy ve raporda "kullanıcıya sorulacaklar" altında listele.
4. **Yedek al:** düzenlemeye başlamadan önce
   `paper/manuscript/src` klasörünü `paper/manuscript/_backup_src_YYYYMMDD_HHMMSS.tar.gz`
   olarak arşivle (projede bu alışkanlık zaten var, örn. `outputs/_backup_figures_20260702_021838.tar.gz`).
5. Makale dili İngilizce; İngiliz/Amerikan yazım tutarlılığını bozma (metin "optimisation/optimise"
   ile "optimization/optimize"yi karışık kullanıyor — fırsat varken **tek forma sabitle**, önerim: "-ize" ailesi;
   yalnızca yazım düzeyinde, terminolojiye dokunmadan).
6. Her görevden sonra derle, log'da hata/undefined reference bırakma (Bölüm 7).

---

## Kritik ön tespitler (LİDER keşfinden — önce bunları içselleştir)

### A. PDF kaynaklardan ESKİ (bayat)
`src/main.pdf` 2026-07-01 01:02'de derlenmiş; `sections/*.tex` dosyaları ondan SONRA
(02.07'ye kadar) düzenlenmiş. Eski PDF'te bulunan `scale_stability` (eski Fig 7) ve
`spatial_inequality` (eski Fig 11) şekilleri kaynaklardan çıkarılıp panelleri
`cluster_synthesis` (Fig 6b,d) ve `geostats_map` (Fig 10c,d) içine taşınmış. Bu yüzden
kullanıcının PDF üzerinden verdiği şekil numaraları ile mevcut kaynak numaraları farklı.
**Şaşırmamak için eşleme tablosu (label esas alınır):**

| Label | Dosya | Eski PDF no (kullanıcının gördüğü) | Mevcut kaynakta yeniden derlenince |
|---|---|---|---|
| `fig:priority-synthesis` | `priority_synthesis.png` | **Figure 12** | Figure 10 |
| `fig:flow-sankey` | `flow_sankey.png` | **Figure 13** | Figure 11 |
| `fig:topsis-robustness` | `topsis_robustness.png` | **Figure 14** | Figure 12 |

Kullanıcının "Figure 12 / 13 / 14" talepleri bu üç label'a karşılık gelir. İlk iş:
temiz bir rebuild yapıp güncel numaralandırma tabanını kur.

### B. İç çelişki: beşinci eksen "pluvial" mi "cooling deficit" mi?
- `methodology.tex` §"optimize" (satır ~183): eksenleri **"heat, pluvial, coastal, access
  deficit, social vulnerability"** diye sayıyor.
- `results.tex` §res-priority, Fig 12 kapşonu ve `appendix.tex` `tab:params` ("Need axes"):
  **"heat, cooling deficit, access deficit, coastal exposure, social vulnerability"**.
- Giriş ve özet "üç tehlike: aşırı sıcak, ani (pluvial) taşkın, kıyı" iddiasında; ama
  optimizasyona pluvial ekseni HİÇ girmiyor.

Bu bir tutarlılık hatası ve "sığ metod çalışması" izleniminin somut kaynaklarından biri.
Görev 5.1'de çözümü tanımlı.

### C. Ek (supplementary) şekil numaralandırması bozuk
`appendix.tex` içinde kapşonlara elle "Supplementary Figure S5/S6/S7" yazılmış şekiller
(`supp_m1_heat_leverage`, `supp_vulnerability_robustness`, `supp_shap_stability`) belge
sırasında S1–S4'ten ÖNCE geliyor; ayrıca hepsi ana sayaçtan (Figure 15–18...) numara alıyor.
Görev 6.4'te düzeltilecek.

---

## GÖREV 1 — Denklemler (en yüksek öncelik)

Makalede şu an **tek bir numaralı denklem yok**; kullanıcı en önemli denklemlerin mutlaka
yer almasını istiyor. `amsmath` yüklü; `\begin{equation}...\end{equation}` + `\label{eq:...}`
kullan ve **her denklemi metin içinde en az bir kez `Equation~\eqref{...}` / `(Eq.~\ref{...})`
biçiminde referansla** (natbib + hyperref mevcut; `\eqref` için amsmath yeterli).

Aşağıdaki 8 denklem **zorunlu**, yerleştirme yerleri belirtildi. LaTeX blokları hazır;
notasyonu metinle uyumlu hale getirirken anlamı değiştirme. Denklemler `tab:params`daki
gerçek parametrelerle (18 bin, k=8 komşu, 2.000 Dirichlet çekimi, 6 blok CV...) tutarlı olmalı.

**Z1. Çapraz atama (cross-attribution) operatörü** — makalenin "metodolojik çekirdeği".
Yer: `methodology.tex` §\ref{sec:methods-xattr}, "Formally, the cross-attribution rule..."
cümlesinin yerine/yanına:

```latex
\begin{equation}\label{eq:xattr}
\bar{x}_{c}(g) \;=\; \frac{\sum_{t \in T(g)} a_{t \cap g}\, x_{c}(t)}
                        {\sum_{t \in T(g)} a_{t \cap g}},
\end{equation}
```
Burada $T(g)$ = $g$ hücresiyle kesişen tesselasyon hücreleri, $a_{t\cap g}$ = kesişim alanı,
$x_c(t)$ = $c$ karakterinin hücre değeri. Metinde alan-ağırlıklı medyan/IQR analoglarının da
aynı operatörle üretildiğini belirt.

**Z2. Ağ hizmet alanı (service area) tanımı.** Yer: aynı alt bölüm, 400/800 m tanımının yanına:

```latex
\begin{equation}\label{eq:servicearea}
S_{r}(g) \;=\; \{\, e \in E \;:\; d_{\mathrm{net}}(v_{g}, e) \le r \,\},
\qquad r \in \{400, 800\}\,\mathrm{m},
\end{equation}
```
$v_g$ = hücre merkezine en yakın düğüm, $d_{\mathrm{net}}$ = kenar-uzunluk ağırlıklı en kısa
yol (Dijkstra) mesafesi, $E$ = sokak segmentleri kümesi.

**Z3. SHAP (Shapley) atfı.** Yer: `methodology.tex` §\ref{sec:methods-explain}:

```latex
\begin{equation}\label{eq:shap}
\phi_{j} \;=\; \sum_{S \subseteq F \setminus \{j\}}
\frac{|S|!\,\bigl(|F|-|S|-1\bigr)!}{|F|!}\,
\Bigl[ f_{x}\bigl(S \cup \{j\}\bigr) - f_{x}(S) \Bigr],
\end{equation}
```
$F$ = öznitelik kümesi, $f_x(S)$ = koşullu beklenen model çıktısı. Atıf: TreeSHAP için
Lundberg vd. 2020, *Nature Machine Intelligence* (DOI `10.1038/s42256-019-0138-9`) —
**önce Crossref'ten doğrula**, `refs.bib`e ekle (bib'de şu an SHAP metodolojik atfı YOK; bu bir eksik).

**Z4. Pareto baskınlık (dominance) tanımı.** Yer: `methodology.tex` §\ref{sec:methods-optimize}:

```latex
\begin{equation}\label{eq:pareto}
i \succ j \;\iff\; n_{k}(i) \ge n_{k}(j)\;\; \forall k \in \{1,\dots,5\}
\;\;\wedge\;\; \exists\, k :\; n_{k}(i) > n_{k}(j),
\end{equation}
```
$n_k(\cdot)$ = büyük değerin daha yüksek ihtiyacı gösterdiği yönde kodlanmış ihtiyaç ekseni;
baskılanmayan (non-dominated) küme = öncelik cephesi (frontier).

**Z5. Entropi ağırlıkları.** Yer: aynı alt bölüm (TOPSIS'ten önce):

```latex
\begin{equation}\label{eq:entropy}
e_{k} \;=\; -\frac{1}{\ln m} \sum_{i=1}^{m} p_{ik} \ln p_{ik},
\qquad
w_{k} \;=\; \frac{1 - e_{k}}{\sum_{l} \bigl(1 - e_{l}\bigr)},
\qquad
p_{ik} \;=\; \frac{r_{ik}}{\sum_{i} r_{ik}},
\end{equation}
```

**Z6. TOPSIS yakınlık katsayısı.** Yer: hemen ardından:

```latex
\begin{equation}\label{eq:topsis}
C_{i} \;=\; \frac{D_{i}^{-}}{D_{i}^{+} + D_{i}^{-}},
\qquad
D_{i}^{\pm} \;=\; \Bigl( \sum_{k} \bigl( w_{k} r_{ik} - v_{k}^{\pm} \bigr)^{2} \Bigr)^{1/2},
\end{equation}
```
$v_k^{+}/v_k^{-}$ = ideal/anti-ideal noktalar; $r_{ik}$ = vektör-normalize karar matrisi.
(Hwang \& Yoon 1981 zaten bib'de: `hwang1981MultipleAttribute`.)

**Z7. Global Moran's I.** Yer: `methodology.tex` §\ref{sec:methods-spatial}:

```latex
\begin{equation}\label{eq:moran}
I \;=\; \frac{n}{\sum_{i}\sum_{j} w_{ij}}\;
\frac{\sum_{i}\sum_{j} w_{ij}\, z_{i} z_{j}}{\sum_{i} z_{i}^{2}},
\end{equation}
```
$w_{ij}$ = satır-standardize k-en yakın komşu ağırlıkları ($k=8$), $z_i$ = ortalamadan sapma.
İstersen local Moran $I_i$ ve Getis-Ord $G_i^{*}$'ı tek bir ek denklemde ver (isteğe bağlı O2).

**Z8. Gini katsayısı (eşitlik ekseni).** Yer: aynı alt bölüm:

```latex
\begin{equation}\label{eq:gini}
G \;=\; 1 - \sum_{k=1}^{n} \bigl( X_{k} - X_{k-1} \bigr)\bigl( Y_{k} + Y_{k-1} \bigr),
\end{equation}
```
$X_k$ = kümülatif hücre payı, $Y_k$ = kümülatif maruziyet$\times$kırılganlık yükü payı
(Lorenz eğrisi trapez yaklaşımı; Fig `fig:geomap`d ile uyumlu).

**İsteğe bağlı (yer varsa ekle, raporda ekleyip eklemediğini gerekçelendir):**
- O1: Yönelim entropisi $H_{o} = -\sum_{i=1}^{18} p_i \ln p_i / \ln 18$ (uzunluk-ağırlıklı,
  18 bin; Boeing 2019 *Applied Network Science*, DOI `10.1007/s41109-019-0189-1` — doğrulayıp ekle).
- O2: Getis-Ord $G_i^{*}$ standart formu.
- O3: Silhouette $s(i)=\frac{b(i)-a(i)}{\max\{a(i),b(i)\}}$ ve/veya ARI (küme seçimi + ölçek kararlılığı).
- O4: Yön-kodlu z-standardizasyon $z_{ij} = s_j (x_{ij}-\mu_j)/\sigma_j$ (winsorize [1,99] sonrası).

Denklem enflasyonu yapma: zorunlu 8 + en fazla 2–3 isteğe bağlı. XGBoost amaç fonksiyonunu
yazmana gerek yok (atıfla geçiliyor); SHAP denklemi mekanizma iddiasının bel kemiği olduğu için zorunlu.

---

## GÖREV 2 — Em-dash / en-dash ve yapay-zeka yazım izleri temizliği

Mevcut envanter (LİDER saydı): `---` (em-dash) **90 adet**, kelime--kelime en-dash **31 adet**.
Dağılım: results 22, discussion 15, background 12, study_area 10, appendix 8, conclusions 8,
methodology 7, introduction 4, titleAbstract 4.

**Kurallar:**
1. Düz metinde `---` (em-dash) **tamamen kalkacak**. Mekanik virgülleme YAPMA; her cümleyi
   doğal biçimde yeniden kur: iki nokta, parantez, ayrı cümle, "that is", "namely" vb.
   Anlam ve vurgu korunacak.
2. Kelime--kelime en-dash bileşikleri (`fabric--resilience`, `catchment--radius`,
   `exposure--vulnerability`, `morphology--temperature`, `explain $\rightarrow$ optimize` vb.):
   normal kısa çizgiye çevir (`fabric-resilience`) veya yeniden ifade et
   ("the exposure and vulnerability burden"). `$\rightarrow$` içeren "explain
   $\rightarrow$ optimize" kalıbını metin genelinde tek forma indir: önerim
   **"explain-then-optimize"** (zaten birkaç yerde bu form var).
3. Sayı aralıkları: düz metinde "2014--2024" → "2014 to 2024" / "between 2014 and 2024";
   "400/800\,m" formu kalabilir. **Tablo hücrelerinde ve refs.bib sayfa aralıklarında `--`
   kalabilir** (tipografik standart; kullanıcının hedefi düzyazıdaki yapay-zeka izleri).
4. Başlıkta da en-dash var (`Fabric--Resilience`) — Görev 4 ile birlikte çözülür.
5. Diğer yapay-zeka izlerini de tara ve azalt (raporda önce/sonra say):
   - Aşırı `\emph{}` vurgusu (metinde çok sık; en az yarıya indir, yalnızca gerçek terim
     tanımlarında bırak).
   - Tekrarlanan "honest/honestly/candid" ailesi (≥4 kez geçiyor) — bir kez kalsın, kalanını
     "conservative", "cautious", "we do not over-read" gibi çeşitlendir.
   - "notably", "crucially", "importantly" yığılmaları; üçlü paralel kurgu tekrarı.
6. Temizlik sonrası doğrulama (Bölüm 7'deki grep komutları) sıfır `---` göstermeli.

---

## GÖREV 3 — Üçüncü yazar: Hilmi Evren Erdin (3. sıra)

Üç dosyada güncelleme:

1. **`sections/titleAbstract.tex`** — `\author{}` bloğuna 3. sırada ekle:
   ```latex
   \and Hilmi Evren Erdin\thanks{%TODO-UNVAN%, Department of City and Regional
   Planning, Dokuz Eyl\"ul University, \.{I}zmir, T\"urkiye. ORCID %TODO-ORCID%.}
   ```
2. **`title_page.tex`** — `\textsuperscript{3}` satırı, affiliation bloğu, ORCID satırı ve
   **CRediT** bloğuna ekle. CRediT önerisi (kullanıcı onayına tabi, raporda işaretle):
   `Hilmi Evren Erdin: Supervision, Conceptualization, Writing - Review & Editing.`
3. **`sections/declarations.tex`** — "Author contributions" paragrafına aynı katkı setiyle ekle.

**Uydurma yasak:** ORCID ve akademik unvan (Doç. Dr. / Prof. Dr.) alanlarını `%TODO%`
bırak, raporun "Kullanıcıya sorulacaklar" bölümünde listele. Affiliation olarak DEÜ Şehir ve
Bölge Planlama makul varsayımdır ama bunu da onaya işaretle.

---

## GÖREV 4 — Başlık kısaltma

Mevcut başlık (2 satır, 18 kelime, üstelik en-dash içeriyor):
> *Grid-Based Urban Morphometrics for Climate Resilience: Explainable, Pareto-Aware
> Fabric--Resilience Priorities for the İzmir Functional Urban Region*

Kullanıcı isteği: kısa, göze hoş; "optimization" veya "Pareto" geçebilir. Kurallar:
≤ 12 kelime hedefle, iki nokta üst üste en fazla bir kez, hiçbir dash türü kullanma.

**Aday listesi (birini seç, seçimini raporda 2–3 cümleyle gerekçelendir):**
1. **Explain, then Optimize: Urban Fabric and Climate Adaptation Priorities in İzmir** *(LİDER önerisi — iki aşamalı yöntemi ve şehri tek nefeste veriyor)*
2. Explainable Morphometrics and Pareto Optimization for Climate Adaptation in İzmir
3. Pareto-Aware Climate Adaptation Priorities for Urban Fabric in İzmir
4. Urban Form, Heat and Equity: Multi-Objective Adaptation Priorities for İzmir
5. From Urban Fabric to Adaptation Priorities: An Explainable Multi-Objective Workflow

Güncellenecek yerler: `titleAbstract.tex` `\title{}`, `title_page.tex` başlık bloğu ve
(varsa) üst bilgi/PDF metadata. Anahtar kelimeler listesini yeni başlıkla çakışmayacak
şekilde gözden geçir (başlıkta geçen kelimeyi keyword'te tekrar etmemek iyi pratiktir).

---

## GÖREV 5 — Derinleştirme: "sığ metod çalışması" izlenimini kır

Somut, sınırlı-kapsamlı yükseltmeler (yeni analiz koşturmadan yapılabilenler öncelikli):

**5.1 (ZORUNLU) Eksen çelişkisini çöz.** Ön tespit B'deki tutarsızlık:
`methodology.tex`'teki "(heat, pluvial, coastal, access deficit, social vulnerability)"
listesini gerçek pipeline ile eşitle: **heat, cooling deficit, access deficit, coastal
exposure, social vulnerability** (bkz. `tab:params` "Need axes"). Ardından özet + giriş +
proxies alt bölümündeki "üç tehlike (heat, pluvial, coastal)" anlatısını dürüstçe hizala:
pluvial maruziyeti tarama katmanı olarak üretildiğini ama öncelik eksenine girmediğini,
hidrodinamik doğrulama ile birlikte gelecek çalışmaya bırakıldığını AÇIKÇA yaz (limitasyonlara
bir madde ekle). Önce `scripts/pilot_11_priority.py` içinde pluvial ekseni gerçekten var mı
kontrol et; varsa ve çıktısı `outputs/tables/adaptation_priority.csv`te duruyorsa alternatif
olarak ekseni metne geri kazandırmayı değerlendir — hangisini seçtiğini kanıtla raporla.

**5.2 (ZORUNLU) Araştırma sorusu → cevap eşlemesi.** Girişte 4 soru tanımlı ama
sonuçlarda/sonuç bölümünde tek tek cevaplanmıyor. `conclusions.tex`i (veya discussion'ın
başını) RQ1–RQ4'ü sırayla, birer cümlelik net cevapla kapatacak şekilde yeniden yapılandır
("RQ1: yes, the seven strata are sharply differentiated (Table 2)..." tarzı).

**5.3 (ZORUNLU) Politika çeviri tablosu.** Discussion §policy'ye küçük bir tablo ekle:
satırlar = 7 doku katmanı; sütunlar = baskın SHAP mekanizması (Şekil `fig:shap`b'den),
öncelik sırası (Tablo 3), önerilen müdahale paketi (roof/yard greening, albedo, gölgeleme,
tahliye erişimi...). Veriler `outputs/tables/shap_per_stratum_mechanism.csv` +
`adaptation_priority.csv`ten; yeni analiz yok, mevcut bulguların karar diline çevirisi.
Bu tablo "method paper" algısını "decision-support paper" algısına çevirir.

**5.4 (ZORUNLU) Nicel senaryo cümlesi.** SHAP bağımlılık grafiklerinden (Fig
`fig:explainable-heat-interactions`) türeyen en az bir sayısal karşı-olgusal ifade ekle;
örn. yeşil örtü payının SHAP etkisinin katmanlar arası aralığı zaten hesaplı
(peripheral'da $-0.81$°C, industrial'da $+0.40$°C footprint etkisi). Bunları
"attributable contrast" diliyle discussion'a taşı: "moving a coarse-grain cell's green-cover
fraction from its stratum median to the peripheral median is associated with..." gibi.
YENİ SAYI ÜRETME; yalnızca var olan SHAP çıktılar'ndan (`outputs/tables/shap_*.csv`) oku.

**5.5 (İsteğe bağlı, öner ama uygulamadan önce raporda maliyetini yaz):**
- Dışlama eşiği duyarlılığı (built fraction 0.10, slope %15) için tek paragraflık gerekçe
  veya mini duyarlılık notu.
- LCZ (Local Climate Zones) ile kavramsal kıyas paragrafı: bu iş neden LCZ değil,
  LCZ'ye ne ekliyor (intro'da ima var, discussion'da tek paragraf net kıyas iyi olur).
- Landsat 100 m LST ↔ 250 m hücre ölçek uyumu belirsizliğinin bir cümleyle nicelenmesi
  (S1 PSF paneline referansla).

---

## GÖREV 6 — Şekil cerrahisi

Ortak kurallar: yeni/revize şekiller `scripts/_manuscript_style.py` stilini ve
`raw_morphology_maps` kartografik dilini (ölçek çubuğu, kuzey oku, kıyı çizgisi, EPSG:32635)
kullanacak. Üretimi `scripts/` altına yeni/revize `make_*.py` olarak ekle ve
`generate_all_figures.py`e bağla. Şekil verisi hazır: `outputs/figure_gpkgs/`.

**6.1 Fig `fig:priority-synthesis` (kullanıcının Figure 12'si) — MEKANSALLAŞTIR.**
Mevcut: (a) doku-düzeyi scatter, (b) hücre-düzeyi Pareto scatter. Sorun: 223 frontier
hücresinin NEREDE olduğu görülmüyor; oysa metnin ana mesajı mekânsal hedefleme.
Yapılacak: paneli üçe çıkar veya (b)'yi değiştir:
- (a) doku-düzeyi scatter (kalsın, küçülebilir),
- (b) hücre-düzeyi Pareto scatter (kalsın),
- **(c) YENİ HARİTA:** 3.777 hücre; baskılanan hücreler açık gri, 223 frontier hücresi
  katman rengiyle dolu + koyu kontur; kıyı çizgisi; körfez çevresine inset zoom.
  Veri: `figure_12_priority_synthesis.gpkg` (geometri + dominance bayrağı; alan adlarını
  `figure_gpkg_manifest.csv`ten doğrula) veya `pilot_13_cell_pareto.py` çıktısı.
Kapşonu ve `results.tex` §res-priority metnini yeni panele göre güncelle ("frontier cells
concentrate along the bay-front..." gibi mekânsal bir okuma cümlesi ekle — sayıları gpkg'den doğrula).

**6.2 Fig `fig:flow-sankey` (kullanıcının Figure 13'ü) — KALDIR.**
- `results.tex`ten figure ortamını ve ona bağlanan cümleyi ("The transition flow from
  a-priori fabric strata ... Figure~\ref{fig:flow-sankey}, illustrating how...") sil;
  paragraf akışını pürüzsüz bırak.
- Başka `\ref{fig:flow-sankey}` kalmadığını grep'le doğrula.
- `generate_all_figures.py` ve `make_fig09_flow_sankey.py`i pipeline'dan çıkar (dosyayı
  silme, orchestrator'dan düş); `flow_sankey.png` diskte kalabilir.
- Strata↔cluster geçiş bilgisi zaten `tab:cluster-priority` + `cluster_vs_stratum.csv`te;
  bilgi kaybı yok — raporda bunu belirt.

**6.3 Fig `fig:topsis-robustness` (kullanıcının Figure 14'ü) — YARI MEKANSALLAŞTIR.**
Mevcut: (a) Monte-Carlo sıra boxplot'ları (değerli, KALSIN), (b) paralel koordinat grafiği
(soyut, zayıf). Yapılacak: (b)'yi şu haritayla değiştir:
- Hücre düzeyinde entropi-ağırlıklı TOPSIS yakınlık skoru $C_i$ haritası (sürekli renk
  rampası) + 223 frontier hücresi konturla bindirilmiş. Böylece Fig 12(c) ile görsel köprü
  kurulur. Veri: `figure_14_topsis_robustness.gpkg` (yoksa `pilot_11_priority.py` hücre
  skorlarını üretir; `cell_priority_top20.csv` çapraz kontrol için).
- Paralel koordinat panelindeki entropi ağırlık kutusu bilgisini kapşon metnine taşı
  (bilgi kaybolmasın). Alternatifi (parallel coords'u supplementary'ye taşımak) uygun görürsen
  raporda gerekçelendir.

**6.4 Ek şekil düzeni ve tekrar ayıklama.**
1. **Numaralandırmayı onar:** appendix şekilleri ana sayaçla "Figure 15–18" alıyor ama
   kapşonlarda elle "S1..S7" yazıyor ve belge sırası S5,S6,S7,S1,S2,S3,S4 şeklinde bozuk.
   Çözüm: appendix başına şu bloğu ekle ve TÜM kapşonlardaki elle yazılmış "Supplementary
   Figure S#:" öneklerini sil:
   ```latex
   \renewcommand{\thefigure}{S\arabic{figure}}
   \setcounter{figure}{0}
   \renewcommand{\thetable}{S\arabic{table}}
   \setcounter{table}{0}
   ```
   (Tabloları da S-serisine almak isteyip istemediğine ana metin çapraz referanslarını
   kontrol ederek karar ver; `tab:cluster-priority`, `tab:heat-leverage`, `tab:vuln-robust`,
   `tab:params` appendix'te.) Belge sırasına göre S-numaraları otomatik ve tutarlı olur.
2. **Tekrar ayıklama (en az şu ikisini uygula, farkındaysan fazlasını öner):**
   - `supp_topsis_sensitivity` (S4) panel (c) "strata $C_i$ dağılımları", ana Fig
     `fig:topsis-robustness`(a) sıra dağılımlarıyla büyük ölçüde aynı bilgiyi verir →
     paneli düşür veya kapşondan tek cümleyle S4'ü üç panele indir.
   - Ana Fig `fig:shap` içindeki CV performans inset'i, S3 (`supp_xgb_diagnostics`) ile
     birebir tekrar → inset'i sadeleştir (tek satır $R^2$) veya S3'e havale et.
   - `supp_data_quality` (S1) panel (d) demografik korelasyon, metinde tek cümleyle
     anlatılıyor; kalması savunulabilir — dokunmadan önce raporda görüş bildir.
3. Şekil değişikliklerinden sonra `export_figure_gpkgs.py` manifestini ve
   `figure_gpkg_export_report.md`yi güncelle (numara eşlemesi değişecek).

---

## GÖREV 7 — Doğrulama ve derleme

Her büyük görevden sonra ve en sonda:

```powershell
cd C:\Users\YE\PyCharmMiscProject\icus2026_planx_urban_resilience\paper\manuscript\src
latexmk -pdf -interaction=nonstopmode main.tex   # yoksa: pdflatex x2 + bibtex + pdflatex x2
latexmk -pdf -interaction=nonstopmode title_page.tex
```

Kontroller (raporda çıktılarıyla birlikte):
1. `main.log`: `Undefined references`, `Citation ... undefined`, `multiply defined` = SIFIR.
2. Em-dash denetimi: `grep -c -- '---' sections/*.tex` → tümü 0.
   En-dash denetimi: `grep -oE '[a-zA-Z]--[a-zA-Z]' sections/*.tex` → boş.
3. `grep -n 'flow-sankey' sections/*.tex main.tex` → boş.
4. `%TODO` işaretleri sadece Erdin ORCID/unvan alanlarında.
5. `scripts/check_citations.py` çalıştır → temiz.
6. Şekil yeniden üretildiyse `scripts/report_canonical_numbers.py` ile kanonik sayıların
   değişmediğini göster.
7. Yeni PDF'i sayfa sayfa görsel kontrol et: denklem taşmaları (overfull hbox), şekil
   yerleşimi, S-numaralandırma, başlık satır kırılımı.

---

## GÖREV 8 — Rapor kontratı (LİDER'e dönüş)

Raporu şuraya yaz: `docs/revision/ISCI_RAPORU_rev2.md`. Zorunlu bölümler:

```markdown
# İŞÇİ RAPORU — rev2
## 1. Yönetici özeti (≤10 satır: ne yapıldı, ne yapılmadı, neden)
## 2. Görev durum tablosu
   | Görev | Durum (TAMAM/KISMİ/YAPILMADI) | Kanıt (dosya:satır / grep çıktısı / sayfa no) |
## 3. Eklenen denklemler (numara, label, yerleştirildiği bölüm, metin içi referans cümlesi)
## 4. Em-dash/en-dash denetimi (önce/sonra grep sayıları, dosya bazında)
## 5. Seçilen başlık + gerekçe + güncellenen dosyalar
## 6. Yazar değişikliği (yapılan ekler + TODO alanları)
## 7. Şekil değişiklikleri (her şekil için: eski→yeni durum, üretim betiği, PNG yolu,
     kapşon metni; Fig12(c) ve Fig14(b) haritalarının küçük önizleme yolları)
## 8. Derinleştirme değişiklikleri (5.1–5.4 tek tek; eksen çelişkisi çözümünün kanıtı)
## 9. Tutarlılık taraması: senin bulduğun EK sorunlar (LİDER'in listesi dışında)
## 10. Build kanıtı (latexmk özeti, log uyarı sayısı, PDF sayfa sayısı, şekil sayısı)
## 11. Kullanıcıya sorulacaklar (Erdin ORCID/unvan/CRediT onayı, başlık onayı, vb.)
## 12. Değiştirilen dosyaların tam listesi + yedek arşivin yolu
```

**Öncelik sırası (zaman kısıtında bu sırayla):**
1. Yedek + rebuild taban çizgisi
2. GÖREV 1 (denklemler) ve 5.1 (eksen çelişkisi)
3. GÖREV 3 (yazar) + GÖREV 4 (başlık)
4. GÖREV 2 (dash temizliği)
5. GÖREV 6.2 (sankey sil) → 6.1 → 6.3 → 6.4
6. GÖREV 5.2–5.4
7. GÖREV 7 doğrulama + GÖREV 8 rapor

**Bitti tanımı (definition of done):** yukarıdaki 7 doğrulama maddesi kanıtlı, rapor
kontrata uygun, PDF temiz derleniyor, kanonik sayılar değişmemiş, TODO'lar yalnızca
kullanıcı onayı gerektiren alanlarda.
