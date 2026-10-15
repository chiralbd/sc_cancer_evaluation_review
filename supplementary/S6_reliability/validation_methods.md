# Second-pass classification reliability: methods and results

Date run: 14 Oct 2026. The inputs are the 4 Oct 2026 data-pull files from the prior-analysis zip (`benchmark_classification.csv`, `limitations_extracted.csv`, `sc_cancer_corpus.csv`).

## Abstract source
All 486 benchmark PMIDs and all 200 subsample PMIDs already had a title and an abstract in `sc_cancer_corpus.csv` (100% coverage). That file holds PubMed-derived records, so no new efetch call was made.

## Part 1: benchmark re-classification (n = 486)
- **Definition given to the rater.** A benchmark is a study whose stated purpose includes a systematic, head-to-head comparison of at least 2 named computational tools, algorithms, pipelines or experimental platforms/protocols on a shared task (same data or same samples), assessed on common criteria. A new-method paper counts only if it reports a systematic comparison against at least 2 named existing tools on shared data. The following do not count: reviews; biological or clinical "evaluation" of a gene, drug, cell population, model system or cohort; validation of a single tool; comparisons of biological conditions, tissues or species.
- **Blinding.** The rater saw only the title and abstract. First-pass labels were never shown to it.
- **Rater A: 394 PMIDs.** These were rated by `host.llm` at the utility (Haiku-class) tier. The resolved model was claude-haiku-4-5-20251001, run with temperature 0 and a forced-tool structured output: is_benchmark, n_named_entities_compared, comparison_type and rationale. This tier differs from the platform's default reasoning (Sonnet-class) tier.
- **Rater B: 92 PMIDs** (positions 395–486 in file order). The host enforces a 2.0M-token ceiling per frame on `host.llm`, and the batch hit it after 394 requests. Each request cost about 5.1k input tokens because the host system prompt is large. The remaining 92 abstracts were therefore rated by hand by the session model, which is a different model again. The same written definition was applied, and first-pass labels were not viewed until rating was finished. The reading used condensed text: the title, the first 650 characters and the last 300 characters of each abstract.

## Part 2: problem-type re-extraction (200 PMIDs)
- **Sample.** 200 PMIDs were drawn with `numpy.random.default_rng(1).choice(unique ids, 200, replace=False)` from the 1,757 PMIDs in `limitations_extracted.csv`.
- **Unit of agreement.** The first pass assigned one primary problem type per paper (1,757 rows for 1,757 PMIDs). The second pass therefore also assigned one primary label per paper, from the same 18-value vocabulary: causality, clinical_translation, confounding, cost_scalability, data_access, generalization, interpretability, metric_invalid, no_benchmark, no_ground_truth, none, other, parameter_sensitivity, reproducibility, resolution_limit, sample_size, technical_artifact, uncertainty. Presence/absence per paper × category is the one-hot coding of these labels.
- **Rater.** The LLM ceiling was already exhausted, so all 200 abstracts were labelled by hand by the session model, blind to the first-pass label and statement. The reading used the title, the first 750 characters and the last 300 characters of each abstract.
- **Working definitions of the second pass.** The first-pass category definitions were not available, so these were written fresh:
  - no_ground_truth: absence of a validated reference standard, labels or gold standard against which a method or result could be checked.
  - causality: a mechanism, role or driver is unknown.
  - interpretability: composition, heterogeneity or landscape is poorly characterised.
  - metric_invalid: a performance metric does not measure what it claims to.
  - parameter_sensitivity: results depend on analysis choices.
  - uncertainty: lack of error or confidence quantification.

## Statistics
Cohen's kappa was computed directly as (po − pe)/(1 − pe), together with percent agreement and the 2×2 cells (both+, first-only, second-only, both−). 95% CIs come from a nonparametric bootstrap over papers (2,000 resamples, numpy seed 1, percentile method). Two overall problem-type measures are reported:
1. pooled paper × category presence/absence (200 × 18 cells);
2. multiclass kappa on the primary label.

A sensitivity analysis merges no_ground_truth, causality and interpretability into one "knowledge_gap" class.

## Results
### Benchmark (validation_agreement.csv)
| subset | n | first + | second + | both + | first only | second only | % agree | kappa [95% CI] |
|---|---|---|---|---|---|---|---|---|
| all 486 (mixed raters) | 486 | 158 | 166 | 134 | 24 | 32 | 88.5 | 0.741 [0.676, 0.798] |
| Haiku-4.5 subset | 394 | 139 | 159 | 127 | 12 | 32 | 88.8 | 0.763 [0.693, 0.829] |
| manual subset | 92 | 19 | 7 | 7 | 12 | 0 | 87.0 | 0.481 [0.229, 0.700] |

- **Counts.** The second pass found 166 benchmarks; the first pass found 158. The consensus count (both raters positive) is **134**.
- **Where the raters disagree.**
  - Of the 32 second-pass-only positives, 14 were first-pass new_method_with_baselines and 16 were biological_evaluation. The second rater counted new-method papers with ≥2 named baselines as benchmarks.
  - All 24 first-pass-only positives were first-pass method_comparison or platform_comparison. Many compare non-tools: CAR-T cell types, xenograft routes, SGLT2 inhibitors, radionuclides, organs.
- **Interpretation.** A defensible range for the benchmark count is **134–166**, with 158 inside it. Agreement is "substantial" on the Landis–Koch scale.

### Problem types (n = 200)
- **Overall agreement is low.** Pooled presence/absence: 91.9% agreement, kappa 0.227 [0.170, 0.287]. Multiclass primary label: 27.0% agreement, kappa 0.167 [0.110, 0.229]. After merging into knowledge_gap: multiclass kappa 0.302 [0.225, 0.380]; knowledge_gap itself 0.505 [0.378, 0.620].
- **no_ground_truth.** The first pass assigned it to 45/200 papers; the second pass to 1/200. None overlapped: kappa −0.010 [−0.029, 0.000]. Of the 45 first-pass no_ground_truth papers, the second pass coded 30 as causality and 9 as interpretability. Their first-pass statements are mostly "mechanism/landscape unknown" (e.g. "Mechanisms of circulating tumor cell immune evasion unknown"). These are not statements about a missing reference standard.
- **metric_invalid.** First pass 4/200, second pass 0/200: kappa 0.000.
- **parameter_sensitivity.** First pass 2/200, second pass 0/200: kappa 0.000.
- **uncertainty.** Neither pass assigned it in the subsample (0/0), so kappa is undefined.
- **Categories with moderate agreement.** reproducibility 0.798 and data_access 0.664 rest on 1–2 positives each and have wide CIs. technical_artifact is 0.446 and resolution_limit 0.304.

## Implications for the review's claims
1. The 158/486 benchmark count is reasonably reliable (kappa ≈ 0.74). Report it as 158 (second-pass 166; consensus 134).
2. The headline "no ground truth = 24.2% of methodological problems" does **not** replicate under a strict reading of "ground truth". The first-pass label mostly captured unknown biological mechanism or landscape. The claim should be reworded (e.g. "unresolved biology / absent reference knowledge") or the 1,757 statements should be re-coded with explicit definitions before it is used.
3. The rare categories (metric validity 1.1%, parameter sensitivity 2.3%, uncertainty 0.7%) stayed rare, or became rarer, in the second pass. The qualitative claim "rarely stated in abstracts" holds, but the per-category kappa cannot be estimated reliably at these prevalences.

## Limitations
- The second raters are mixed: Haiku-4.5 for 394 benchmark abstracts; the session model, reading by hand, for 92 benchmark and all 200 problem-type abstracts. The cause was the per-frame LLM token ceiling.
- The manual ratings used condensed abstracts (mid-abstract text truncated). This can miss baseline comparisons, e.g. for the TRACE, Hypatia and GATE papers, which the first pass called method comparisons.
- The first-pass category definitions were unavailable. Part of the problem-type disagreement is therefore a difference in definitions rather than random error, and that is itself a finding about construct validity.
- This is one second pass, not adjudicated by a human. Counts in this file are provisional.
