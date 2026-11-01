# Track note — GEO ground-truth catalogue (S3/S4/Table 5) repair

Findings addressed: **C-09, C-20, C-21, C-22, D-09, D-10**.
Inputs re-retrieved from GEO on 1 November 2026 (1,336 series SOFT records, 780 sample-level SOFT records,
esummary for all 1,336), <=3 requests/s, cached. Nothing in the original data files was overwritten.

## 1. The decision rules applied (quotable in Methods)

> **Series-level eligibility.** A GEO series was retained only if (i) a single-cell assay cue appears in the
> series title, in a sample title, in a supplementary-file name, or in the record of at least one human
> sample — the series summary and overall-design fields are not admissible, because GEO copies study-level
> text into every SubSeries, and the phrase 'single-cell suspension' is not a cue; (ii) where the sample set
> includes a non-human organism, at least one sample is both human and single-cell; and (iii) at least one
> profiled human sample is cancer-derived material — tumour tissue or tumour-derived cells, a cancer cell
> line, organoid or PDX, or cells of a haematological malignancy from an affected patient — rather than
> non-tumour material from a cancer patient, a non-cancer disease or healthy donor, or a cancer cell line
> used only as an unsequenced co-culture target.

> **CITE-seq protein modality.** The abbreviation ADT is accepted as evidence of antibody-derived-tag
> measurement only when it co-occurs, within 100 characters, with an antibody, feature-barcode or library
> context and does not co-occur with an androgen-deprivation context (androgen, deprivation therapy,
> castration, enzalutamide, abiraterone, degarelix, leuprolide, goserelin, bicalutamide, hormone therapy,
> SBRT, prostatectomy, CRPC, NEPC), or when it appears as a library-type label in the sample-title list
> beside mRNA/GEX/HTO/TCR/BCR/VDJ labels. An unambiguous cue (CITE-seq, TotalSeq, antibody-derived tag,
> REAP-seq, ECCITE, AbSeq, DOGMA-seq, ASAP-seq, TEA-seq, feature barcoding, antibody capture,
> oligo-conjugated or barcoded antibody, surface protein, proteogenomic) is accepted on its own.

> **Modality precision.** Each modality count is reported with the numerator and denominator of a seeded
> audit of the shipping rule and a Wilson 95% interval, and a precision-adjusted range obtained by applying
> those bounds to the count. A call is confirmed when the GEO record states that the study generated that
> data type, whether or not the data are deposited under the same accession.

## 2. What changed

**Eligibility (C-21).** 413 of 1,336 rows (30.9%) fail the screen: 300 E1 no single-cell evidence,
1 E2 no human single-cell sample, 60 E3a no cancer material, 9 E3b cancer only as reagent/target,
43 E3c cancer-patient non-tumour sample. All five series the review named as failures are removed
(GSE249056, GSE273417, GSE289427 — bulk-only SubSeries; GSE267071 — mouse-dominated bulk cell-line series;
GSE309239 — colorectal-cancer patients sampled away from the tumour as IBD-study controls).
Sensitivity: retaining class E3c instead of removing it gives 966 series.

**CITE-seq (C-22).** 227 → 221 on the published row set; 6 removed, every one an androgen-deprivation
false positive: GSE249886, GSE249887, GSE249888, GSE250189, GSE277590 (the five the review named) and
GSE213663. After the eligibility screen the modality stands at 181 series.

**Table 5 (C-09).** Re-deriving `benchmark_tasks` for all 1,336 published rows from the S4 map reproduces the
stored column with 0 disagreements — S3 was right and Table 5 was wrong. The two wrong cells are corrected:
genotype/hashtag multiplex → annotation_calibration, pipeline_robustness; mtDNA lineage → clone_calling.
All other Table 5 cells (series, study groups, median samples, top cancer types) are recomputed on the
corrected catalogue, and three new columns carry the audit numerator/denominator, the Wilson interval and
the precision-adjusted range.

**Precision (C-20 / D-09).** 140 modality calls over 137 series (20 longitudinal/on-treatment, 15 of each
other modality) against 8–10 per modality before. Overall 130/140 = 92.9% (Wilson 87.4–96.1%). The
longitudinal/on-treatment rule, never audited in its shipping form, scores 16/20 (58–92%).

**Funnel (D-10).** Written out as a seven-step table in the corrected S4 methods file, with the explicit
statement that 3,426 of the 6,141 base-set series (56%) were never classified, that recall is bounded by the
nine modality queries, and that 923 is a lower bound on what GEO holds.

## 3. Manuscript-visible numbers, old → new

| Claim | Published | Corrected |
|---|---|---|
| Validation-bearing series | 1,336 | **923** |
| Study groups | 1,166 | **830** |
| Paired bulk RNA | 459 | **233** (precision-adjusted 163–231) |
| Longitudinal / on-treatment | 297 | **229** (133–211) |
| Paired spatial | 250 | **186** (130–184) |
| CITE-seq protein | 227 | **181** (112–175) |
| Genotype / hashtag multiplex | 166 | **134** (106–134) |
| Matched WES/WGS | 138 | **106** (74–105) |
| Perturb-seq | 89 | **57** (40–57) |
| Cell-line mixture | 25 | **24** (19–24) |
| mtDNA lineage | 18 | **15** (11–15) |
| Deposited 2023–26 | 75.7% (1,011/1,336) | **72.2% (666/923)** |
| Malignant-calling series (§6.2) | 162 | **129** |
| Clone-calling series (§6.2) | 153 | **118** |
| Annotation-calibration series (§6.2) | 356 | **288** |
| Spatial-referee series (§6.2) | 250 | **186** |
| Deconvolution series | 698 | **423** |
| Pipeline-robustness series | 918 | **600** |
| Perturbation-response series | 381 | **282** |
| Lung cancer across the six most frequent modalities (§6.2) | 19–50 | **13–23** |
| Breast cancer / glioma across the same six (§6.2) | 8–47 | **4–30** (breast 4–20, glioma 8–30) |
| Paired bulk series quoted in §4.2 | 459 | **233** |
| Median samples per series | 14 | **14 (unchanged)** |
| Table 5 median samples (bulk/long/spatial/CITE/geno/WES/perturb/mix/mtDNA) | 18, 18, 12, 16, 8, 18, 14, 6, 25 | **20, 16, 12, 16, 8, 18, 13, 6, 29** |
| Table 5 'Benchmark tasks enabled', genotype row | malignant_calling, clone_calling, annotation_calibration, pipeline_robustness | **annotation_calibration, pipeline_robustness** |
| Table 5 'Benchmark tasks enabled', mtDNA row | malignant_calling, clone_calling | **clone_calling** |

Table 5's top cancer types change for every modality; see `tables/Table5_ground_truth_corrected.csv`.

## 4. Checks that passed (with denominators)

- `benchmark_tasks` re-derived from the S4 map reproduces the stored S3 column for **1,336 of 1,336** rows
  (0 disagreements). The catalogue follows its own documentation; Table 5 did not.
- Series, study-group and median-sample columns of the published Table 5 reproduce from the published S3 for
  **9 of 9** modalities (the author's `table5.py` check is sound as far as it goes); only the
  'Benchmark tasks enabled' column, which that script never reads, is wrong.
- **221 of 227** CITE-seq calls survive the corrected rule; the modality is not systematically unsound.
- **1 of 1,336** series fails the non-human screen — mouse contamination is rare, not systemic.
- Hand-check of the single-cell screen: **26 of 26** randomly drawn exclusions were correct.
- Precision audit: **130 of 140** calls confirmed; **3 of 9** modalities score 15/15 in their own stratum
  (genotype multiplex, cell-line mixture, mtDNA lineage) and **4 of 9** score 14/15 (paired bulk, spatial,
  WES/WGS, Perturb-seq).
- GEO retrieval: **1,336 of 1,336** series records and **780 of 780** requested sample-level records fetched
  with no failures.

## 5. Not established / not checked

- **Recall.** Not measured, before or now. 3,426 of the 6,141 base-set series were never classified, so 923
  is a lower bound and no coverage fraction can be computed from 1,336/2,024 or 923/2,024.
- **Deposition.** Whether a called modality is downloadable under the same accession: 94 of 140 audited calls
  (67.1%), from the structured pass only, **not** human-reviewed — provisional, and not used to filter.
- **E3c sensitivity.** The cancer-patient-non-tumour screen fires only where the record carries explicit
  control or non-tumour language; 43 removals is a lower bound on that failure mode.
- **Spatial-only series.** Spatial platform names count as single-cell cues (as in the published filter-3
  regex, which matches `10x`), so spatial-only series survive screen E1; GSE228056 and GSE195661 are two
  that remain.
- **Base-set discrepancy.** S4 section 1 records 6,142 hits for the base query, the manuscript prints 6,141;
  not reconciled. Immaterial — the base set feeds no downstream step.
- **Query counts not re-run.** Steps 1–4 of the funnel use the counts recorded in S4 at the 15 October 2026
  retrieval; the GEO queries were not re-executed, so those four counts are not independently verified here.
- **Other catalogues.** ArrayExpress/BioStudies, CELLxGENE and HTAN were not searched, before or now.
- **Figure 6 and the manuscript text** were not edited — other tracks own them.

## 6. Files written (none overwritten)

| File | Contents |
|---|---|
| `supplementary/S3_ground_truth_catalogue_corrected.csv` | 923 eligible series; `validation_modalities`, `n_modalities`, `benchmark_tasks` corrected; new `eligibility_status`, `eligibility_evidence`, `cite_rule_outcome`, `cite_rule_evidence` |
| `supplementary/S3_eligibility_screen_all_rows_corrected.csv` | all 1,336 published rows with the screen verdict and evidence span, including the 413 excluded |
| `supplementary/S3_corrections_diff.csv` | every changed cell: record id, field, old value, new value, reason, evidence span (431 rows) |
| `supplementary/S3_precision_audit_corrected.csv` | 140 audited modality calls with both criteria, human verdict and evidence quote |
| `supplementary/S3_modality_precision_corrected.csv` | per-modality precision, Wilson bounds, precision-adjusted count range |
| `supplementary/S4_ground_truth_methods_corrected.md` | corrected methods: funnel, eligibility screen, CITE rule, precision audit, corrected counts, limitations |
| `tables/Table5_ground_truth_corrected.csv` | Table 5 recomputed, task-mapping cells corrected, three precision columns added |
