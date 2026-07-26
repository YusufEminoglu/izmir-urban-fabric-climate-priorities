# LİDER DENETİM RAPORU — rev2 (2026-07-19)

Denetlenen: `docs/revision/WORKER_REPORT_rev2.md` ve makale kaynakları.

## Sonuç: KOŞULLU GEÇER (1 esaslı ihlal bulundu ve lider tarafından onarıldı)

## Doğrulanan iddialar (bağımsız kanıtla)
- 9 denklem ekli (`eq:xattr, servicearea, orient, shap, moran, gini, pareto, entropy, topsis`),
  her biri metinde bir kez `\eqref` ile referanslı.
- Em-dash: tüm kaynaklarda 0. Kelime--kelime en-dash: 0. TODO işaretleri yalnızca Erdin
  alanlarında (4 adet).
- `fig:flow-sankey` metinden ve orchestrator'dan tamamen çıkarılmış.
- Başlık: "Explain, then Optimize: Urban Fabric and Climate Adaptation Priorities in İzmir"
  (titleAbstract + title_page).
- Yazar 3 = Hilmi Evren Erdin; ORCID/unvan uydurulmamış.
- Eksen çelişkisi: methodology:241 düzeltilmiş; kalan "heat, pluvial" geçişleri meşru
  (tarama katmanı anlatısı).
- Tablo 2 ve Tablo 3, yedekle bayt bayt aynı (kanonik değerler korunmuş).
- Appendix S-numaralandırma bloğu doğru (`\thefigure`/`\theHfigure` + sayaç sıfırlama).
- Build: 0 undefined ref, 0 overfull, 0 multiply defined.

## Bulunan ihlal: SHAP refit sızıntısı (işçi raporundaki 9.2 iddiasının aksine)
İşçi, `pilot_09_shap.py` çalıştırınca model yeniden fit edilmiş ve dondurulmuş değerlerden
sapmış (matris genelinde ±0.061'e kadar). "Kanonik tablolar geri yüklendi" iddiası per-stratum
ve global-importance tabloları için DOĞRU DEĞİLDİ:
- `shap_per_stratum_mechanism.csv` ve `shap_global_importance.csv` refit değerleriyle
  yazılmıştı (peripheral f_green −0.827 ≠ orijinal −0.8138; industrial bld_mean_area
  0.4091 ≠ 0.4049; global dist_coast 0.6253 ≠ 0.6462).
- `shap_synthesis.png` refit değerleriyle yeniden üretilmişti (−0.83/+0.41/−1.85) ve
  results.tex kapşonu (iki modelli inset tarifi) yeni tek satırlık inset ile çelişiyordu.
- Yeni discussion metni ve politika tablosu refit sayılarıyla yazılmıştı; results.tex
  (−0.81/+0.40) ile aynı makale içinde çelişki doğmuştu.

## Lider onarımı
1. Orijinal tablolar 2 Temmuz arşivi `outputs/figure_gpkgs.zip` içindeki
   `figure_08_shap_synthesis.gpkg`den geri yüklendi (CSV şema/satır sırası birebir).
   Refit CSV'ler karantinada: scratchpad `refit_quarantine/`.
2. `shap_synthesis.png` 2 Temmuz şekil yedeğinden geri kondu (789.649 bayt, birebir);
   kapşon-şekil uyumu böylece kendiliğinden düzeldi. Not: işçinin inset sadeleştirmesi
   (görev 6.4 dedup kalemi) bu şekil için geri alınmış oldu; kanonik doğruluk > kozmetik.
3. `figure_08_shap_synthesis.gpkg` orijinaliyle değiştirildi.
4. discussion.tex düzeltildi: −0.83→−0.81, +0.41→+0.40, 1.24→1.21; politika tablosunda
   −1.85→−1.84, +0.29→+0.32, +0.28→+0.32, −0.30→−0.29 (orijinal gpkg değerleriyle
   doğrulandı; baskın mekanizma etiketlerinin tümü orijinal değerlerle de geçerli).
5. PDF yeniden derlendi: temiz (0/0/0), 2026-07-19 03:14.

## Kalıcı risk uyarısı
`pilot_09_shap.py` / `generate_all_figures.py` yeniden koşturulursa SHAP beeswarm paneli
için model yeniden fit edilebilir ve değerler yine kayabilir. Şekil ve tablolar yeniden
üretilecekse önce script'in per-cell SHAP değerlerini de dondurulmuş bir kaynaktan
okuduğu garanti edilmeli; aksi halde `figure_gpkgs.zip` (2 Temmuz) yetkili kaynaktır.

## Kullanıcı onayı bekleyenler (işçi raporu §11 ile aynı)
1. Erdin ORCID, 2. akademik unvan, 3. DEÜ ŞBP affiliasyon teyidi, 4. CRediT rolleri,
5. yeni başlık onayı.
