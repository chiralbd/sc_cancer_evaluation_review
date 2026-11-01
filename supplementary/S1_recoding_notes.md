# S1 benchmark-catalogue re-coding: rule, procedure and corrected numbers

Prepared 2026-11-01 for the revision of *The evaluation gap in single-cell cancer genomics*.
Addresses review findings **C-17 (critical)**, **C-18**, **A-04 / B-13**, **A-05** and **D-01**.
No original file was modified; every output carries a `_corrected` or new-file name.

## 1. Source of the coded text

All 269 PMIDs in `supplementary/S1_benchmark_catalogue.csv` were re-fetched from PubMed
(`efetch`, 2026-11-01). **269/269 resolved.** Three records returned a PubMed entry with a title but
**no abstract text**: PMID 41214134, 42637979, 38977827. Those three were **not re-coded**; their
original values are carried through unchanged and flagged `abstract_available = False`. Every other
record was coded from the retrieved title + abstract only. The retrieved text is stored verbatim in
`supplementary/S1_benchmark_abstracts_2026-11-01.csv` so the coding is auditable.

## 2. Decision rule (quotable in Methods)

> Evaluation fields were re-coded from the PubMed title and abstract alone. **Robustness to analytical
> choices** was marked assessed when the abstract states that the study (a) varied a secondary analytical
> choice - an analysis choice other than the identity of the methods under comparison (parameters,
> hyperparameters, thresholds, preprocessing, normalisation, imputation, filtering, feature selection,
> clustering resolution, reference panel or annotation choice, pipeline composition, software
> implementation, random seed) - and reported a result about its effect; (b) named robustness, stability,
> resilience or reproducibility as one of the dimensions on which the methods were evaluated, compared or
> ranked; (c) stress-tested the methods on deliberately degraded, perturbed or restricted input
> (downsampling, reduced depth or cell number, added noise, label corruption, imbalance perturbation,
> missing or mismatched reference, low-quality or fixed material); or (d) reported an explicit conclusion
> that performance, rankings or biological conclusions depend on, or are unaffected by, such a factor.
> The field was left unassessed when the only robustness language was 'robust' or 'stable' as a bare
> quality adjective, part of a tool name, reproducibility of the authors' own code or workflow, a gap or
> future-work statement, background motivation for a newly proposed method, or the plain fact of comparing
> the methods under test across several datasets or simulation scenarios. Comparison of experimental
> platforms or kits is the subject of a platform benchmark, not a robustness assessment, unless (b) or (d)
> also applies.
>
> **Calibration or uncertainty** was marked assessed when the abstract states that the study examined the
> reliability of reported probabilities, confidences or error rates: calibration or miscalibration of
> scores, false-discovery-rate or type-I-error control, inflated or conservative p-values, false positives
> on null data, uncertainty quantification, interval coverage, or rejection of unknown / out-of-distribution
> classes judged by the reliability of the prediction. Instrument calibration, parameter tuning, and
> sensitivity or FDR reported only as an accuracy metric at a fixed threshold do not qualify.
>
> **Metric validity** was marked assessed when the abstract states that the study interrogated the scoring
> function itself: whether a metric measures what it claims, disagreement between metrics or rank changes
> with the metric, a metric shown to be misleading, biased or inflated, comparison or critique of evaluation
> metrics as an object of study, behaviour against null, random, trivial or deliberately simple baselines,
> or a new metric proposed together with a stated deficiency of existing ones. Merely using several metrics
> does not qualify.
>
> **Ground-truth strategy** was coded multi-label from a fixed vocabulary (simulation; orthogonal assay;
> expert annotation; held-out experimental measurements; genotype multiplexing; cell-line mixture or
> controlled design; curated reference; consensus-only; not stated), using only strategies the abstract
> states were used for evaluation. For prediction-task benchmarks (perturbation response, drug response,
> protein abundance) the measured outcome that predictions are scored against is coded as held-out
> experimental measurements. 'Not stated' is used when and only when none of the others is stated.
>
> All counts remain lower bounds: a study that performed a check but did not mention it in its abstract is
> coded as not assessed.

## 3. Procedure and reliability

1. A transparent keyword/regex rule implementing clauses (a)-(d) was run over all 269 abstracts, producing
   candidate flags and matched spans.
2. An independent full-census pass applied the rule above to each of the 269 abstracts under forced
   structured output, returning a decision, the clause satisfied, and a verbatim evidence span per field.
3. The author hand-read and adjudicated **132 of 269 records (49%)** for robustness - every record the
   regex rule flagged as changed (102) plus a seeded random sample of 30 unflagged records
   (`numpy.default_rng(20261101)`); **all 12 census-positive and all 3 keyword-screened negative records**
   for calibration; **all 36 census-positive and all 38 keyword-screened negative records** for metric
   validity; and **82 records** for ground truth (all 33 that moved out of 'not stated', all 29 that moved
   into it, and a seeded random 20 of the 50 remaining label changes).
4. Where the author's reading and the census pass disagreed, the author's reading is the value in the
   corrected catalogue (`recoding_source = hand-adjudicated`); otherwise the census value stands
   (`rule+assisted-census`).

Agreement on the 132 hand-read robustness records: census pass vs hand reading **kappa 0.76, agreement
90.2%** (precision 0.93, recall 0.94); the regex rule alone vs hand reading **kappa 0.55, agreement 81.8%**
(precision 0.87, recall 0.88). The regex rule alone is therefore not sufficient and is reported only as the
screening layer. On the hardest ground-truth stratum (label changes not involving 'not stated') the census
pass matched the author's reading exactly in **14 of 20** audited records; the 6 disagreements were corrected
by hand. Records outside the audited strata carry the census label.

Clause distribution of the 141 robustness positives: (a) secondary analytical choice 55,
(b) robustness named as an evaluated dimension 42, (c) stress test 16,
(d) explicit dependence conclusion 28.

## 4. Manuscript-visible numbers: old -> new

### 4.1 The three checks (denominator 269)

| Check | Old | New | Wilson 95% CI (new) |
|---|---|---|---|
| Robustness to analytical choices | 15 (5.6%) | **141 (52.4%)** | 46.5-58.3% |
| Calibration / uncertainty | 9 (3.3%) | **10 (3.7%)** | 2.0-6.7% |
| Metric validity | 8 (3.0%) | **36 (13.4%)** | 9.8-18.0% |

Old Wilson intervals for reference: robustness 3.4-9.0%, calibration 1.8-6.2%, metric validity 1.5-5.8%.

**The robustness correction is nine-fold, not two-fold.** The review's census (C-17) estimated 34-36/269
(12.6-13.4%) using a narrow pattern that required the *word* robustness to appear as an assessed dimension.
That narrow construct corresponds to clause (b) alone, which here gives **42/269 = 15.6% (11.8-20.4%)** -
consistent with, and slightly above, the review's estimate. The 52.4% figure additionally counts the
sensitivity analyses, stress tests and dependence conclusions that the field name
`assessed_robustness_to_parameters` is supposed to capture but that never use the word 'robustness'.
A third, intermediate variant - positives whose abstract contains any robustness-family word - is
**67/269 = 24.9% (20.1-30.4%)**. The manuscript should quote 52.4% as the headline with 15.6% named
explicitly as the narrow 'states the word' variant; whichever is chosen, 5.6% cannot stand.

### 4.2 Cancer-specific subgroup (48 vs 221) - finding D-01

| Check | Cancer old | Cancer new (Wilson) | Non-cancer old | Non-cancer new (Wilson) | Fisher p old -> new |
|---|---|---|---|---|---|
| Robustness | 4/48 (8.3%) | **19/48 = 39.6% (27.0-53.7%)** | 11/221 (5.0%) | **122/221 = 55.2% (48.6-61.6%)** | 0.317 -> **0.056** |
| Calibration | 2/48 (4.2%) | **1/48 = 2.1% (0.4-10.9%)** | 7/221 (3.2%) | **9/221 = 4.1% (2.2-7.6%)** | 0.664 -> **1.000** |
| Metric validity | 0/48 (0.0%) | **4/48 = 8.3% (3.3-19.6%)** | 8/221 (3.6%) | **32/221 = 14.5% (10.4-19.7%)** | 0.358 -> **0.351** |

The '0 of 48 cancer-specific benchmarks assess metric validity' claim is **false under the corrected
coding**: four do - PMIDs 37172634 (Nava, 2023, bulk deconvolution), 42070330 (Saxena, 2026, preprocessing),
32266244 (Chakraborty, 2020, preprocessing) and 41044630 (Wu, 2025, foundation models). The direction of the robustness difference
also reverses - cancer-specific benchmarks are now numerically *less* likely to assess robustness, at
p = 0.056, which is not significant at 0.05 and rests on a subgroup of 48. The defensible statement remains
the one D-01 recommends: the 48-benchmark cancer subset is too small to resolve a difference from the
whole-catalogue base rate, and no cancer-specific deficit is established for any of the three checks.

### 4.3 Ground-truth strategy (finding C-18)

| Strategy | Old | New |
|---|---|---|
| simulation | 91 (33.8%) | **97 (36.1%)** |
| orthogonal assay | 44 (16.4%) | **35 (13.0%)** |
| expert annotation | 24 (8.9%) | **25 (9.3%)** |
| held-out experimental measurements | 12 | **13** |
| genotype multiplexing | 11 | **9** |
| cell-line mixture / controlled design | 8 | **16** |
| curated reference | 9 | **9** |
| consensus-only | 3 | **2** |
| not stated | 107 (39.8%) | **99 (36.8%)** |

Wilson 95% CIs for the three figures the manuscript prints: simulation 97/269 = 36.1% (Wilson 95% CI 30.6-42.0%); orthogonal assay
35/269 = 13.0% (Wilson 95% CI 9.5-17.6%); not stated 99/269 = 36.8% (Wilson 95% CI 31.3-42.7%). 183 of 269 records (68%) are unchanged. All five records the review
named are resolved in the direction it predicted: 38755121 and 34600479 lose their unsupported
'orthogonal assay'; 39702273 and 38172966 gain 'simulation'; 35172874 gains 'genotype multiplexing'.
The largest systematic shift is the drop in 'orthogonal assay' (44 -> 35): nine of those flags rested on an
assay the abstract never names, including one whose own S1 annotation read 'source not specified in abstract'.

### 4.4 Table 4 and Figure 5

`tables/Table4_benchmark_classes_corrected.csv` replaces every ground-truth and check column; `n`,
`cancer_specific`, `year_range`, `n_2024_26` and `median_n_tools` are unchanged. Two columns present in the
Figure 5a input but absent from the printed Table 4 (`gt_curated`, `gt_consensus`) are included so that the
table and the figure share one source. **55 of the 144 cells of the Figure 5a class x ground-truth matrix
change** (`code/data/figure_inputs/fig5a_matrix_corrected.csv`). Figure 5b benchmark values move from
15/9/8 of 269 to **141/10/36 of 269** (`code/data/figure_inputs/fig5b_benchmark_checks_corrected.csv`); the
stated-problem side of panel b (n = 1,506) is not in this track's scope and is unchanged here.

## 5. Checks that passed (reported with denominators)

- **15 of 15** records originally flagged `assessed_robustness_to_parameters = True` are confirmed by the
  abstract under the new rule. No original robustness flag was withdrawn; the entire C-17 error is omission.
- **8 of 8** records originally flagged `assessed_metric_validity = True` are confirmed (one, PMID 42637979,
  on its title alone because PubMed holds no abstract for it).
- **7 of 9** records originally flagged `assessed_calibration_or_uncertainty = True` are confirmed;
  2 are withdrawn (below).
- **183 of 269** ground-truth strategy strings are unchanged.
- **269 of 269** PMIDs resolve in PubMed and every title matches the S1 title field.
- PMID 42838986 (finding A-05) is present in S1, is one of the 7 records of class
  'CNV inference & malignant-cell calling', and its catalogued fields are confirmed.

## 6. Individual findings

**A-04 / B-13 (annotation calibration).** PMID 40439669 (Theunissen et al., *Brief Bioinform* 2025) evaluates
six out-of-distribution detection methods for automatic cell-type annotation, stating that data shifts and
unseen labels "significantly affect the reliability of cell type predictions" and evaluating the methods on
their ability to identify novel cell types. Under clause 2 of the calibration rule (rejection of unknown
classes judged by the reliability of the prediction) this **is** a calibration assessment, and the record is
re-coded `assessed_calibration_or_uncertainty = True`. This is a judgement call at the boundary of the rule
and is flagged as such. Consequently the annotation class now shows **1** calibration assessment, not 0, and
section 4.4's sentence ("assessed in only one record, and it is not cancer-specific [35]") is **supported** by
the corrected catalogue - PMID 40439669 is the only one of the 17 annotation records and is not
cancer-specific. Table 4's annotation Calib. cell changes 0 -> 1, and the headline calibration figure moves
9/269 = 3.3% -> 10/269 = 3.7%.

**A-05 (uncited seventh CNV benchmark).** Confirmed in S1 and verified against PubMed esummary. Metadata for
the references track: **Han S, Xiong Z, Zhou Y, Yang C. Benchmarking copy number alteration inference methods
for spatial transcriptomics. Nat Commun. 2026 Sep 5;17(1). doi:10.1038/s41467-026-77500-5. PMID 42838986.**
Catalogue fields verified: class 'CNV inference & malignant-cell calling', cancer_specific True, 9 tools
compared, 2026, `pubmed_verified` True. Its abstract states no ground-truth strategy and none of the three
checks, so it is coded 'not stated' / unassessed on all four re-coded fields - unchanged from the original.

**C-18 (ground-truth errors in both directions).** Addressed in section 4.3.

**D-01 (cancer-specific deficit).** Addressed in section 4.2.

## 7. Not established / not checked

- **Not established:** the three fields for PMIDs 41214134, 42637979 and 38977827. PubMed returns no abstract
  text for these records, so they cannot be coded under an abstract-level protocol. Their original values are
  carried through unchanged and must not be presented as verified.
- **Not checked:** 137 of 269 records were not hand-read for robustness, and 187 were not hand-read for ground
  truth; those values come from the census pass whose measured agreement with hand reading is kappa 0.76
  (robustness) and 14/20 exact (hardest ground-truth stratum). The remaining disagreement rate implies an
  uncertainty of roughly +/-5 records on the robustness count that is **not** reflected in the Wilson intervals,
  which capture sampling error only.
- **Not checked:** full texts. Every count here remains an abstract-level lower bound, exactly as section 2.5
  declares.
- **Not checked:** no independent human second coder. The agreement statistics above are model-vs-author, not
  human-vs-human, and do not discharge the requirement in `docs/internal_review_guide.md` for a human round.
- **Not re-derived:** `n_tools_compared`, `metrics`, `datasets_public`, `cancer_specific`, `method_class`,
  `year` and all other S1 columns. Only the four fields named in this track were re-coded.
- **Not in scope:** the stated-problem side of Figure 5b (n = 1,506), Table 3, Table 6 and all manuscript text.

## 8. Files written

| File | Content |
|---|---|
| `supplementary/S1_benchmark_catalogue_corrected.csv` | 269 rows, original 22 columns plus `*_recoded` and `*_evidence` for the four fields, `robustness_clause`, `recoding_source`, `abstract_available` |
| `supplementary/S1_recoding_diff.csv` | 245 changed cells: pmid, field, old value, new value, reason, evidence span, coding source |
| `supplementary/S1_benchmark_abstracts_2026-11-01.csv` | the 269 fetched titles and abstracts the coding is based on |
| `tables/Table4_benchmark_classes_corrected.csv` | 16 classes x corrected ground-truth and check columns |
| `code/data/figure_inputs/fig5a_matrix_corrected.csv` | corrected 16 x 9 class-by-ground-truth matrix |
| `code/data/figure_inputs/fig5b_benchmark_checks_corrected.csv` | corrected Figure 5b benchmark points with Wilson intervals |
