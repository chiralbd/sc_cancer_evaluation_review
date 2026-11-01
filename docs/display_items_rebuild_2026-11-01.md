# Display-item rebuild from the corrected data — 1 November 2026

Rebuild of Tables 1–6, Figures 1–6 and a new two-arm PRISMA 2020 flow diagram against the corrected
catalogues produced by the four data-repair tracks. No original file was overwritten: every table and
figure is written with a `_revised` suffix, and the PRISMA items are new files.

Corrected inputs used
- `S1_benchmark_catalogue_corrected.csv` (269 records, re-coded evaluation fields)
- `fig5a_matrix_corrected.csv` (16 classes × 9 ground-truth categories)
- `S3_ground_truth_catalogue_corrected.csv` (923 series, 830 study groups)
- `Table5_ground_truth_corrected.csv`, `S3_modality_precision_corrected.csv`
- `S4_ground_truth_methods_corrected.md` (GEO screening funnel)
- `supplementary/S7_statistics/revision_2026-11-01/multiplicity_bh.csv`

Robustness is reported throughout under the **narrow** construct: `robustness_clause == 'b'` **and**
`assessed_robustness_to_parameters_recoded` true, giving 42/269 = 15.6% (Wilson 11.8–20.4). The broad
reading (141/269) appears nowhere in the rebuilt display items. The supplied
`Table4_benchmark_classes_corrected.csv` carries the broad column; the revised Table 4 does not.

---

## 1. Tables

### Table 1 — topic taxonomy: UNCHANGED, verified
Regenerated from the archived PubMed volume panel (`S7_statistics/update_2026-10-15/pubmed_topic_volume_long_2026-10-15.csv`).
All 26 rows × 6 derived values (2021, 2025, 2026-partial, 2023–26, CAGR, share change) reproduce the
published table exactly — **156/156 values, 0 mismatches**. The emitted Markdown block is byte-identical
to the manuscript's Table 1 block (28 lines).

### Table 2 — coverage by topic: UNCHANGED, verified
Papers 2015–26 recomputed from the same volume panel; rates, exact Poisson 95% intervals and
papers-per-benchmark recomputed from the counts; the 2023–26 columns checked against
`coverage_model_input_2026-10-15.csv`. **208/208 values reconcile, 0 mismatches.** The emitted Markdown
block is byte-identical to the manuscript's Table 2 block (28 lines). The statistics refit altered
variance estimators and multiplicity adjustments, not per-topic point estimates.

### Table 3 — stated problems: one column ADDED
A `BH q` column was added between `OR per year (95% CI)` and `κ model pair`, taken from family B of
`multiplicity_bh.csv` (the 17-test family of per-year odds ratios). **16 of 17 rows receive a q-value**;
`other` is inestimable (OR 7.1 × 10⁸, CI 0–∞) and is printed as —. Each q was matched to its row by
problem type and the 16 OR point estimates in the table agree with those in the multiplicity file to
1 × 10⁻⁶. Two q-values change an interpretation and should be picked up by the text track:
`clinical_translation` nominal p = 0.0031, q = 0.0125 (survives); `no_benchmark` nominal p = 0.0221,
q = 0.0537 (**no longer significant after adjustment**). All other displayed cells are byte-identical to
the manuscript's Table 3 block.

### Table 4 — benchmark classes: REBUILT
Rebuilt directly from the corrected S1, not copied from the supplied corrected table. Two ground-truth
columns are new (`Curated`, `Consensus`): the re-coding introduced them as distinct categories, they
carry 9 and 2 records, and they appear in Figure 5a, so dropping them would make the strategy columns
irreconcilable with the figure.

- **272/272 cells derive from the corrected S1** (16 rows × 17 fields).
- Column totals against the corrected S1 directly: n = 269, cancer-specific = 48, simulation 97,
  orthogonal 35, genotype 9, mixture 16, held-out 13, expert 25, curated 9, consensus 2, not stated 99,
  robustness 42, calibration 10, metric validity 36, records dated ≥ 2024 = 151.
- Against the supplied `Table4_benchmark_classes_corrected.csv`: **257/272 cells identical**; the 15
  differences are exactly the `robust_params` column (supplied total 141 broad, rebuilt total 42 narrow).

### Table 5 — ground truth: REBUILT, two columns ADDED
Series, study groups and median samples recomputed from the corrected S3: **27/27 values, 0 mismatches**.
All **27 (cancer type, count) pairs** in the "most frequent cancer types" column verified against the
corrected S3, and each verified to be in the modality's top three by count. Where counts tie, the ordering
of the supplied corrected table was kept (five ties: longitudinal 17, CITE-seq 19, genotype 13,
WES/WGS 10, Perturb-seq 6).

The `Benchmark tasks enabled` column was confirmed against the data rather than the prose: for each of the
nine modalities, every series carrying that modality **alone** has exactly the task set the table claims —
**9/9 mappings confirmed**. Task totals over the corrected S3 reproduce Supplementary S4 §6a exactly
(malignant_calling 129, clone_calling 118, deconvolution 423, annotation_calibration 288,
CCC_spatial_referee 186, pipeline_robustness 600, perturbation_response 282).

Two columns added: `Audit (confirmed/n; precision 95% CI)` and `Precision-adjusted series`. All
**36/36 precision values** (audit numerator/denominator, Wilson interval, adjusted range, corrected count)
match `S3_modality_precision_corrected.csv` for all nine modalities.

### Table 6 — research agenda: gap evidence and public-data counts REWRITTEN
Every number in the two rewritten columns was recomputed from the corrected catalogues:

| Row | Published gap evidence | Revised |
|---|---|---|
| A1 | Metric validity stated in **0/48** cancer-specific benchmarks | **4/48 (8.3%)** and 36/269 (13.4%), Fisher p = 0.351 — the "0/48" claim is false under the corrected coding |
| A2 | Robustness stated in 5.6% of benchmarks (4/48 cancer) | **15.6% (42/269)**, 7/48 cancer (14.6%), Fisher p = 1.000 |
| A3 | Calibration stated in 3.3% of benchmarks (2/48 cancer) | **3.7% (10/269)**, 1/48 cancer (2.1%), Fisher p = 1.000 |
| A4–A8 | gap evidence unchanged | verified: 266 lineage papers 2023–26 with 0 benchmarks; 7 CNV/malignant-calling benchmarks; 6 CCC benchmarks, 0 cancer-specific, topic share 2.32×; 13,532 prognosis papers and 23 benchmarks 2023–26; 1/25 integration benchmarks cancer-specific |

Public-data series counts change in every row that cites one: cell-line mixture 25 → 24, genotype
multiplex 166 → 134, longitudinal 297 → 229, paired bulk 459 → 233, CITE-seq 227 → 181, matched WES/WGS
138 → 106, paired spatial 250 → 186, mtDNA lineage 18 → 15 (9 study groups, unchanged).

Anchor-reference numbers were left as published. Reference renumbering belongs to the reference track
(`S8_reference_renumbering_cascade.csv`) and depends on which additions are adopted.

---

## 2. Figures

Figures were regenerated with `code/src/05_figures_revised.py`, which reproduces `04_figures.py` verbatim
for Figures 1–4 and rebuilds Figures 5 and 6 from the corrected inputs. Page geometry matches the
originals exactly (same `figsize`, same `bbox_inches='tight'`, 300 dpi). No titles inside panels.

### Verified identical (pixel-diff against the published PNG, RGBA, per-pixel)
| Figure | Differing pixels | Total pixels |
|---|---|---|
| Figure 1 | **0** | 2,729,760 |
| Figure 2 | **0** | 3,677,500 |
| Figure 3 | **0** | 2,033,262 |
| Figure 4 | **0** | 2,036,556 |

Figure 3 was checked as instructed and is unchanged in data as well as in pixels. The published
`04_figures.py` also reproduces Figures 5 and 6 pixel-identically from the *old* snapshot (0 differing
pixels each), which establishes that the renderer is deterministic and that the Figure 5/6 differences
below come from the corrected data alone.

### Rebuilt
**Figure 5** — panel a from `fig5a_matrix_corrected.csv`; the matrix is identical in all **144/144 cells**
to an independent rebuild from the corrected S1, so the published matrix and the corrected S1 agree.
Panel b now carries 42 / 10 / 36 of 269 against the unchanged first-pass comparison circles
(34 / 10 / 16 of 1,506). The x-limit was extended from 0–10% to 0–24% because the robustness interval now
reaches 20.4%; the legend text was moved with it. Everything else in the panel is the published code.

**Figure 6** — all three panels rebuilt from the corrected S3. Panel b now starts at 2015 rather than
2016, because the corrected catalogue contains two 2015 series; 2017 remains empty. Panel c's column
order changed with the corrected cancer-type frequencies (breast cancer moves from rank 2 to rank 4;
head and neck cancer enters the top 14, replacing pancreatic cancer's former position in the ordering).

### Caption numbers to verify (one list per figure)

**Figure 1**
- (a) subfield papers per year 2015–2026; 2026 = 7,571 records, partial to 15 Oct (hatched); 2015 = 443; total 2015–26 = 34,595
- (b) verified benchmarks per 1,000 subfield papers, 12 yearly points with exact Poisson 95% CI; Poisson fit rate ratio 0.922 (0.875–0.972), p = 0.0027
- (c) 26 topics; share of subfield 2025 vs 2021, range 0.44× to 6.23×; 16 method/measurement and 10 biology/application topics

**Figure 2**
- (a) 25 topics excluding benchmarking; verified benchmarks per 1,000 papers 2015–26, 0.00 to 11.54; 2 topics with zero benchmarks in 2023–26 (open circles)
- (b) same 25 topics, share change vs rate, marker area ∝ √(papers 2023–26)
- (c) incidence-rate ratios from NB2 coverage models: method-topic IRR 4.84 (2.09–11.18) all 26 topics, 2.35 (1.66–3.31) excluding benchmarking over the full window; log share-change IRR 0.79 (0.60–1.06)

**Figure 3**
- (a) first- vs second-pass classification of the 489 evaluation-titled records; confusion counts [[134.0, 32.0], [24.0, 296.0]]; κ = 0.74 (0.68–0.80), 88.5% agreement
- (b) per-category Cohen's κ on 200 re-coded abstracts, 9 of 17 categories plotted; 'no ground truth' 45 → 1 positives, κ = -0.01; merged knowledge-gap category κ = 0.51 (0.38–0.62), 105 → 120 positives

**Figure 4**
- (a) single-cell-omics share of the stratified sample, 17% in 2015 to 89% in 2026; n = 1,771 abstracts over 12 years
- (b) 16 problem types, percentage of 989 single-cell-omics abstracts stating each, Wilson 95% CI
- (c) any stated problem and any evaluation check by period; evaluation-check positives 18/129 (2015–18), 15/240 (2019–21), 7/229 (2022–23), 14/391 (2024–26) = 14.0 / 6.2 / 3.1 / 3.6%

**Figure 5**
- (a) 16 method classes × 9 ground-truth categories, 269 benchmarks; cell colour is the fraction of the class; 305 class-by-strategy assignments in total (categories are not mutually exclusive); 99 benchmarks state no strategy
- (b) robustness 42/269 = 15.6% (Wilson 11.8–20.4) vs 34/1,506 = 2.3% (1.6–3.1) of stated problems
- (b) calibration/uncertainty 10/269 = 3.7% (2.0–6.7) vs 10/1,506 = 0.7% (0.4–1.2)
- (b) metric validity 36/269 = 13.4% (9.8–18.0) vs 16/1,506 = 1.1% (0.7–1.7); the abstract-verifiable pair is 35/269 = 13.0% (9.5–17.6), because PMID 42637979 has no PubMed abstract and is flagged from its title

**Figure 6**
- (a) 923 series in 830 study groups; paired bulk RNA 233, longitudinal/on-treatment 229, paired spatial 186, CITE-seq protein 181, genotype/hashtag multiplex 134, matched WES/WGS 106, Perturb-seq 57, cell-line mixture 24, mtDNA lineage 15
- (b) series by deposition year 2015–2026: 2, 4, 0, 11, 25, 43, 57, 115, 134, 171, 179, 182; 666 of 923 = 72.2% deposited 2023–26; 2026 bar is partial (hatched)
- (c) 9 modalities × the 14 most frequent cancer types; largest cell 32 (longitudinal × acute myeloid leukaemia); dots mark zero; median samples per series 14

> **Flag for the text track.** The Figure 3 panel-a confusion matrix sums to **486**, not 489: it was
> built on the 4 October 2026 pull. The three records indexed 5–15 October were classified non-benchmark
> in a single pass and never entered the two-pass agreement analysis. The published caption says "the 489
> evaluation-titled papers". The figure is unchanged (and correct for what it shows); the caption needs
> the 486 denominator, or an explicit note. This is pre-existing, not introduced by this rebuild.

---

## 3. PRISMA

`code/src/06_prisma.py` writes `figures/PRISMA_flow.{pdf,png}` (300 dpi, 11.0 × 9.4 in) and
`tables/PRISMA_counts.csv`. Every count in the diagram is read from a file, not typed, and four
arithmetic identities are asserted at render time (identified − excluded = verified; base − outside-union
= union; union − filter-1–4 failures = 2,024; 1,336 − 413 = 923).

- Arm 1: 489 identified (486 + 3), 489 screened, 331 excluded (167 biological/clinical evaluation; 116 method paper with token baselines; 41 review; 7 other), 158 verified (32.3%, 28.3–36.6), 157 in the 2015–2026 window, 269 in the assembled catalogue (54 carried, 215 added, 267 dated 2015–2026)
- Arm 2: 6,141 base set (never classified), 2,715 modality-query union (3,473 raw hits; 3,426 base-set series outside the union), 2,024 after filters 1–4 (691 failed), 1,336 series / 1,166 groups after the modality rule (688 no call), 413 removed at the eligibility re-screen (300 / 1 / 60 / 9 / 43), 923 series in 830 study groups final

Arm 1 exclusion reasons were recovered from the archived first-pass screen
(`S6_reliability/benchmark_second_pass.csv`, `first_pass_kind` over the 328 non-benchmarks of the 486-record
pull) plus the three later records (`new_evaluation_titled_2026-10-05_to_15.csv`, all non-benchmark).
Arm 2 is the funnel of the corrected S4 §2a/§2b.

**Not established.** The 269-record catalogue cannot be partitioned by search stream from the released
`sources` field: the field carries 136 distinct overlapping values mixing stream tags (`SEED`,
`SUPPLEMENTARY_SEARCH:*`, `search:*`) with method-class names, so a record often matches more than one
stream and some labels are ambiguous. The diagram therefore reports the one split that is unambiguous —
54 records flagged `in_prior_158` (carried from the verified first-pass screen) and 215 added by targeted
searching — and names the four streams without claiming a per-stream count.

`supplementary/S10_PRISMA_checklist.md` records all 27 PRISMA 2020 items. Six are marked **not done**
(items 11/18 risk of bias in included studies; 14/21 reporting-bias assessment; 15/22 certainty of
evidence; 24a registration and protocol — the review was not registered and no protocol was written) and
three **partial** (6 single database per arm; 8 the second screening pass is a model rater, not a second
independent human reviewer; 9 extraction not independently duplicated).

---

## 4. Files written

Tables (`tables/`): `Table1_taxonomy_revised.{csv,md}`, `Table2_coverage_revised.{csv,md}`,
`Table3_problem_types_revised.{csv,md}`, `Table4_benchmark_classes_revised.{csv,md}`,
`Table5_ground_truth_revised.{csv,md}`, `Table6_agenda_revised.{csv,md}`, `PRISMA_counts.csv`.

Figures (`figures/`): `Figure1_revised.{png,pdf}` … `Figure6_revised.{png,pdf}`,
`PRISMA_flow.{png,pdf}`.

Supplementary: `S10_PRISMA_checklist.md`.

Code: `code/src/05_figures_revised.py`, `code/src/06_prisma.py`,
`code/outputs/figure_revision_report.json` (overlap check and machine-readable caption numbers).

---

## 5. Provenance of the coding behind Tables 4–6 and Figure 5

Every evaluation-check count in Table 4, Table 6 and Figure 5b is inherited from the re-coding track, not
re-derived here, and it is not a uniform hand read. `recoding_source` in the corrected S1 records
**174 of 269 records as hand-adjudicated and 95 as rule plus assisted census**. The re-coding track
reported its own reliability limits (partial hand coverage for robustness, a keyword screen for
calibration and metric validity, with model-assisted adjudication elsewhere); those limits propagate
unchanged into every display item rebuilt here. The counts are reproducible lower bounds on what the
abstracts state under the stated rules, not independently verified assessments of what the benchmarks did,
and the share resting on assisted rather than hand coding should be stated wherever 15.6 / 3.7 / 13.4% is
reported. Three of the 269 records have no PubMed abstract (`abstract_available` false), which is why the
metric-validity figure is reported as 36/269 = 13.4% with the abstract-verifiable pair 35/269 = 13.0%
alongside.

Likewise, the Table 5 modality counts and the Figure 6 panels inherit the GEO track's limits: per-modality
precision rests on a 140-call audit (15–20 calls per modality) rather than a census, the eligibility
adjudication covered 222 candidate series rather than all survivors, recall was never measured, and
whether a called modality is actually deposited in the same accession is only provisionally quantified
(67.1%, not human-reviewed). Table 5's precision-adjusted range column exists to keep those intervals in
view next to the raw counts; the raw counts on their own should not be read as settled.
