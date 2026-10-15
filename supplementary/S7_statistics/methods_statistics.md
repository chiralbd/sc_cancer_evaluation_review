# Statistical methods: verification, intervals and coverage models

Inputs: archive `artifacts-sc.zip` (data pull 4 Oct 2026). All numbers below were computed by code from the archive CSVs; no new PubMed queries were made.

## 1. Re-derivation of quoted quantities (`verified_quantities.csv`)
Every numeric claim in `sc_cancer_genomics_gap_review.md` that can be derived from the archive was recomputed (120 rows: 101 match, 1 approximate, 6 mismatch, 12 not verifiable from the archive).
- Subfield volume: `pubmed_topic_volume_long.csv`, series `__SUBFIELD_TOTAL__`. 2026 projection = 2026 partial count (7,342 to 4 Oct, day 277) × 365/277 = 9674.
- Topic volume 2023–26 = sum of the 2023–2026 per-topic PubMed counts (2026 partial, not projected).
- Share change = (topic_2025/total_2025)/(topic_2021/total_2021), recomputed from counts.
- Verified benchmarks per topic = PMIDs with `is_benchmark==True` in `benchmark_classification.csv`, joined to topic tags in `sc_cancer_corpus.csv` (pipe-separated; tags overlap, so per-topic counts sum to 274 over 158 unique benchmarks).
- Methodological problems: rows of `limitations_extracted.csv` with `problem_type != 'none'` and `none != True` (n = 1,506). Per-topic shares use the row sums of `problem_type_by_topic.csv` (all extracted problems for the topic, including `other`) as denominator; that denominator reproduces the review's 2.1%, 2.6% and 13% figures.

## 2. Intervals (`ci_tables.csv`)
- Proportions: Wilson score 95% intervals (`statsmodels.stats.proportion.proportion_confint(method='wilson')`). Covered: 158/486 verified-benchmark share; benchmark-kind mix; all 17 problem types over 1,506; benchmarking-topic share of the 2025 subfield; per-topic shares of no_ground_truth, no_benchmark, metric_invalid, parameter_sensitivity, uncertainty and causality; per-topic verified/evaluation-titled fraction.
- Rates: exact (Garwood) Poisson 95% intervals for verified benchmarks per 1,000 topic papers 2023–26: lower = χ²(0.025; 2k)/2, upper = χ²(0.975; 2k+2)/2, divided by papers and scaled by 1,000. Papers-per-benchmark intervals are the reciprocals.

## 3. Topic-level coverage model (`coverage_model.csv`, `topic_class_mapping.csv`)
Unit: topic (n = 26). Outcome: verified benchmark count. Offset: log(topic PubMed papers 2023–26). Covariates: log(share change 2025 vs 2021); binary `method` = 1 for method/measurement topics.
**Indicator definition.** `method` = 1 if the topic's object is an analytic/computational task, an evaluation activity, or a measurement technology/assay (16 topics: cnv_scdna, clonal_phylogeny, malignant_calling, ith_quantification, deconvolution, lineage_barcoding, perturbseq, benchmarking, integration_batch, qc_artifacts, foundation_dl, cell_communication, spatial_tumor, epigenome_multiome, tcr_bcr_repertoire, ctc_liquid_biopsy); `method` = 0 if the object is a biological question or clinical/application endpoint (10 topics: tme_composition, tcell_exhaustion, resistance_persister, drug_response_pred, immunotherapy_resp, metastasis, pancancer_atlas, clinical_prognosis, plasticity_emt, longitudinal_therapy). Six ambiguous topics are flagged in the mapping; `method_alt` flips them (drug_response_pred → method; spatial_tumor, tcr_bcr_repertoire, ctc_liquid_biopsy, epigenome_multiome, cell_communication → biology).
**Models.** NB2 (`statsmodels.formula.api.negativebinomial`, ML estimation of α, BFGS then Newton), and Poisson GLM with the same formula and offset. Poisson vs NB compared by likelihood ratio on α with a boundary-corrected p (½·χ²₁), Pearson χ²/df for the Poisson fit, and AIC. Fits: primary; excluding the `benchmarking` topic; window-matched outcome (benchmarks published 2023–26 only, matching the offset window); alternative classification (each with and without `benchmarking`).

**Results (NB2 IRRs).**
- Primary: method 4.87 (95% CI 2.13–11.13; p=0.00017); log share change 0.56 (95% CI 0.24–1.29; p=0.171); α = 0.86. Poisson Pearson χ²/df = 29.2; LR test for α p < 0.001. The overdispersion is almost entirely the benchmarking topic (164 benchmarks per 1,000 papers).
- Excluding benchmarking: method 2.44 (95% CI 1.72–3.47; p=5.61e-07); log share change 0.64 (95% CI 0.48–0.86; p=0.00273) (IRR per doubling of share = 0.73); α = 0.061, LR p = 0.072; Poisson χ²/df = 1.86 — Poisson and NB give near-identical estimates.
- Window-matched, excl. benchmarking: method 2.81 (95% CI 1.87–4.22; p=6.6e-07); log share change 0.78 (95% CI 0.56–1.08; p=0.134).
- Alternative classification, excl. benchmarking: method 1.89 (95% CI 1.18–3.02; p=0.00812); log share change 0.63 (95% CI 0.43–0.91; p=0.0135).
Interpretation: method/measurement topics carry roughly 2–3× the benchmark rate of biology/application topics after adjusting for volume, robust to classification and window. A negative association with share growth (faster-growing topics less benchmarked per paper) is present when benchmarking is excluded with all-year counts, but it is not significant with the window-matched outcome (p = 0.13), so it should be reported as suggestive.

## 4. Temporal trend (`coverage_trend.csv`)
Per year 2015–2026: verified benchmarks (publication year from `sc_cancer_corpus.csv` `year`, all 486 PMIDs matched) against subfield PubMed volume. 2014 (2 evaluation-titled papers, 1 benchmark) is excluded because the volume series starts in 2015. 2026 is partial in both numerator and denominator (to 4 Oct), so its ratio is used unprojected.
Tests of year (centred at 2020): Poisson GLM with offset log(subfield papers); NB2 with the same offset; binomial GLM (benchmarks out of subfield papers); Poisson fit restricted to 2015–2025; binomial GLM of verified fraction among evaluation-titled papers; Poisson GLM of evaluation-titled papers; exact conditional comparison of pooled rates 2023–26 vs 2015–20.
Results: benchmarks per 1,000 papers fell by a rate ratio of 0.924 per year (95% CI 0.876–0.974; p = 0.0036); NB α ≈ 0.011 (no overdispersion); 2015–2025 only: 0.930 (0.874–0.989; p = 0.020). Pooled rate 6.77/1,000 in 2015–20 vs 3.92/1,000 in 2023–26 (ratio 0.58; exact conditional p = 0.0089). The verified fraction among evaluation-titled papers shows no trend (OR/year 0.976, p = 0.46), so the decline is in evaluation-titled output relative to volume, not in classification yield.

## 5. Caveats
- Topics overlap (median 3 tags per paper), so the 26 topic observations are not independent; model SEs are optimistic.
- Benchmark numerators come from an LLM-assisted classification of a title-keyword query (`benchmark|comparison|evaluation|assessment`); benchmarks without these title words are missed, uniformly across years only if title conventions are stable.
- Denominators are independent PubMed topic queries; numerators rest on keyword topic tagging of the corpus.
- The review's papers-per-benchmark table divides all-year (2014–2026) benchmark counts by 2023–26 papers; window-matched counts are given in the model input and reduce several topic counts (e.g. ctc_liquid_biopsy 8 → 3; clinical_prognosis 37 → 23).
