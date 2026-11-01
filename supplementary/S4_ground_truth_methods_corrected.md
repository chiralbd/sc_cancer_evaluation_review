# Ground-truth dataset catalogue: methods (corrected)

This file supersedes `S4_ground_truth_methods.md` for sections 2, 5, 6 and 7. Sections 1, 3 and 4 of the
original file (retrieval queries, modality regexes, derived-field definitions) are unchanged except where
stated. Corrections were made in response to review findings C-09, C-20, C-21, C-22, D-09 and D-10.
GEO records were re-retrieved on 1 November 2026 (series SOFT, `acc.cgi targ=self form=text view=brief`;
sample SOFT, `targ=gsm view=brief`; `esummary db=gds` for sample titles and taxon), at <=3 requests/s.

## 2a. Screening funnel (explicit; PRISMA-style)

| Step | Set | n | Reason for loss at this step |
|---|---|---|---|
| 1 | GEO DataSets base query (human tumour single-cell GSE), retrieved | 6,141 | retrieved only; **never classified** — plays no part in steps 2–7 |
| 2 | Union of the nine modality queries (3,473 hits before de-duplication) | 2,715 | 3,426 base-set series (56%) are outside the union and cannot enter the catalogue |
| 3 | Eligibility filters 1–4 (gdstype contains 'sequencing'; human taxon; single-cell regex; cancer regex) | 2,024 | 691 failed one of filters 1–4 |
| 4 | Filter 5: at least one modality rule fires on series-level text | 1,336 (1,166 study groups) | 688 carried no modality call — **this was the published catalogue** |
| 5 | Series-level eligibility re-screen (new; see 2b) | 923 (830 study groups) | 413 removed: 300 no single-cell evidence; 1 no human single-cell sample; 60 no cancer material; 9 cancer only as reagent/target; 43 cancer-patient non-tumour sample |
| 6 | Corrected CITE-seq rule (new; see 3a) | 923 | modality-level only: 6 of 227 CITE-seq calls dropped |
| 7 | **Final corrected catalogue** | **923 series in 830 study groups** | |

Recall is bounded by the nine modality queries, not by the base set. **1,336 was, and 923 is, a lower bound
on what GEO holds**: a validation-bearing series that none of the nine queries retrieves cannot enter the
catalogue, and no recall estimate was made. The base-set figure of 6,141 frames the search space only; it is
not the denominator of any fraction reported in the paper. (Section 1 of the original S4 records 6,142 hits
for the same base query; the one-record difference is unreconciled and immaterial, since the base set is
never used downstream.)

## 2b. Series-level eligibility screen (new)

Section 2.6 states the catalogue is filtered to 'sequencing-based, human, single-cell, cancer series'. The
published filters tested that at the level of the *study text*, which for a SubSeries is frequently the text
of its parent SuperSeries. The following tests are applied to the *series* and to its own samples.

**E1 — single-cell evidence.** A series is retained only if a single-cell assay cue appears in (i) the series
title, (ii) a sample title, (iii) a supplementary-file name, or (iv) the record of at least one human sample
(`!Sample_title`, `!Sample_source_name_ch1`, `!Sample_characteristics_ch1`, `!Sample_extract_protocol_ch1`,
`!Sample_data_processing`, `!Sample_library_strategy`). The series summary and overall-design fields are
**not** admissible evidence, because GEO copies study-level text into every SubSeries. The phrase
'single-cell suspension' is excluded from the cue list (it describes dissociation, not an assay).
*300 of 1,336 series fail (22.5%).* Twenty-six randomly drawn exclusions were hand-checked against the GEO
record; 26/26 were correct (bulk RNA-seq, bulk ATAC-seq, ChIP-seq, CUT&RUN, MeDIP-seq, miRNA-seq, gDNA).

**E2 — human single-cell sample.** A series whose sample set includes a non-human organism is retained only
if at least one sample is both human and single-cell. *1 of 1,336 fails.*

**E3 — cancer material.** A series is retained only if at least one profiled human sample is cancer-derived:
tumour tissue or tumour-derived cells, a cancer cell line/organoid/PDX, or cells of a haematological
malignancy from an affected patient. Candidates for failure were identified mechanically — (a) no cancer term
(the section 2 cancer regex) in the title, in any sample title or in any sample record, or (b) explicit
control/non-tumour sampling language anywhere in the record — and each candidate (n = 222) was then
adjudicated against its GEO record with a stored verbatim evidence span. Three failure classes:
E3a no cancer material at all (60 series: COVID-19, IBD, keloid, Sjögren's, healthy atlases, CAR-T
manufacturing from healthy donors); E3b cancer present only as a reagent or co-culture target that is not
itself sequenced (9); E3c the donor has cancer but the profiled material is explicitly non-tumour, e.g.
resection material taken away from the cancer site, or post-transplant immune reconstitution (43).
*112 of 1,336 fail.*

Screen sensitivity is not uniform: E3c can only be detected where the record carries explicit control or
non-tumour language, so the 43 removals are a lower bound on that failure mode.

## 3a. Corrected CITE_seq_ADT rule (replaces the CITE_seq_ADT row of section 3)

The published rule accepted the bare token `ADT`, which in prostate and prostate-adjacent studies denotes
**androgen deprivation therapy**. The corrected rule is:

1. Accept if an unambiguous cue is present: `CITE-seq`, `antibody-derived tag`, `TotalSeq`, `REAP-seq`,
   `ECCITE`, `AbSeq`, `DOGMA-seq`, `ASAP-seq`, `TEA-seq`, `feature barcoding`, `antibody capture`,
   `oligo(nucleotide)-conjugated antibody`, `barcoded antibody`, `(cell) surface protein`, `protein panel`,
   `InTraSeq`, `SIGNAL-seq`, `proteogenomic`.
2. Otherwise, for each occurrence of `\bADTs?\b`, read a ±100-character window. **Reject** the occurrence if
   the window matches an androgen-deprivation sense (`androgen`, `deprivation therapy`, `castrat`,
   `enzalutamide`, `abiraterone`, `degarelix`, `leuprolide`, `goserelin`, `bicalutamide`, `hormone
   therapy/deprivation/sensitive`, `SBRT`, `prostatectom`, `CRPC`, `NEPC`, `anti-androgen`, or
   `continued/received/underwent/after/before/during/on ADT`). Otherwise **accept** it if the window carries
   an antibody/feature-barcode context (`librar`, `derived cDNA`, `antibod`, `capture`, `GEX`, `HTO`, `TCR`,
   `BCR`, `VDJ`, `feature`, `tag`, `protein`, `panel`, `oligo`, `CITE`, `multiom`, `hashtag`, `count`,
   `matrix`, `assay`, `surface`, `epitope`).
3. Otherwise accept if `ADT` appears as a library-type label in the sample-title list (alongside `mRNA`,
   `GEX`, `HTO`, `TCR`, `BCR`, `VDJ`, `RNA`, `protein`, or where the summary mentions protein measurement)
   and no androgen-deprivation term is present in that list.

Re-screening all 227 published CITE-seq calls: **221 retained, 6 removed** — GSE249886, GSE249887, GSE249888,
GSE250189, GSE277590 (all quote 'androgen deprivation therapy (ADT)' or 'continued ADT and SBRT') and
GSE213663 ('control or ADT condition', prostate cancer-associated fibroblasts). Acceptance route for the 221
retained: 196 unambiguous cue, 22 ADT in an antibody context, 3 ADT as a sample-title library label.

## 4a. Benchmark-task mapping (unchanged; verification)

Re-deriving `benchmark_tasks` for all 1,336 published rows from the section 4 map reproduces the stored
column with **0 disagreements**. The published S3 column is correct; Table 5's 'Benchmark tasks enabled'
column was not, and has been corrected in `tables/Table5_ground_truth_corrected.csv`
(genotype/hashtag multiplex: annotation_calibration, pipeline_robustness; mtDNA lineage: clone_calling).

## 5a. Precision audit (replaces section 5)

Seeded sample (`numpy.random.default_rng(20261106)`) drawn from the **corrected** catalogue: 20
longitudinal/on-treatment calls and 15 of every other modality, 140 modality calls over 137 series — against
8–10 per modality in the published audit. Each call was judged against the re-retrieved GEO record on the
criterion S4 itself states: *does the record say that this study generated that data type* (counting data
held in a sibling SubSeries or an external repository). Every verdict carries a verbatim evidence span and is
released in `supplementary/S3_precision_audit_corrected.csv`.

Procedure: a first structured pass over every call, then human review of all 17 non-confirmed verdicts and of
12 randomly drawn confirmed verdicts. Human review agreed with 12/12 confirmed calls and with 10/17
non-confirmed calls; the 7 disagreements were all over-strict rejections (single-cell DNA counted as matched
DNA sequencing; hashtag and CROP-seq evidence carried only in sample titles) and were overridden to
confirmed. The figures below are the human-adjudicated ones.

| Modality | Published count | Corrected count | Audit | Precision (Wilson 95%) | Precision-adjusted count |
|---|---|---|---|---|---|
| Paired bulk RNA | 459 | 233 | 14/15 | 70–99% | 163–231 |
| Longitudinal / on-treatment | 297 | 229 | 16/20 | 58–92% | 133–211 |
| Paired spatial | 250 | 186 | 14/15 | 70–99% | 130–184 |
| CITE-seq protein | 227 | 181 | 13/15 | 62–96% | 112–175 |
| Genotype / hashtag multiplex | 166 | 134 | 15/15 | 80–100% | 106–134 |
| Matched WES/WGS | 138 | 106 | 14/15 | 70–99% | 74–105 |
| Perturb-seq | 89 | 57 | 14/15 | 70–99% | 40–57 |
| Cell-line mixture | 25 | 24 | 15/15 | 80–100% | 19–24 |
| mtDNA lineage | 18 | 15 | 15/15 | 80–100% | 11–15 |

Overall precision 130/140 = **92.9%** (Wilson 95% 87.4–96.1%). The longitudinal/on-treatment rule — unaudited
in the published S4, which recorded only that it had been 'tightened once more' after scoring 7/10 — now
scores 16/20 (58–92%); the four failures are single-timepoint treated-versus-control comparisons.

A second, stricter question was recorded for each call: are samples of that data type part of *this* GEO
series? 94 of 140 (67.1%) — this figure is from the structured pass only and was not human-reviewed, so it is
**provisional**. It quantifies the warning already in section 3: a modality call says the study generated the
data, not that the data are downloadable from this accession.

## 6a. Corrected counts

Total: **923 series in 830 study groups** (published: 1,336 in 1,166).

| Modality | Series (published → corrected) | Study groups (published → corrected) |
|---|---|---|
| Paired bulk RNA | 459 → 233 | 402 → 206 |
| Longitudinal / on-treatment | 297 → 229 | 266 → 209 |
| Paired spatial | 250 → 186 | 218 → 167 |
| CITE-seq protein | 227 → 181 | 216 → 175 |
| Genotype / hashtag multiplex | 166 → 134 | 152 → 123 |
| Matched WES/WGS | 138 → 106 | 117 → 91 |
| Perturb-seq | 89 → 57 | 77 → 54 |
| Cell-line mixture | 25 → 24 | 20 → 19 |
| mtDNA lineage | 18 → 15 | 9 → 9 |

| Benchmark task | Series (published → corrected) |
|---|---|
| malignant_calling | 162 → 129 |
| clone_calling | 153 → 118 |
| deconvolution | 698 → 423 |
| annotation_calibration | 356 → 288 |
| CCC_spatial_referee | 250 → 186 |
| pipeline_robustness | 918 → 600 |
| perturbation_response | 381 → 282 |

Deposited 2023–26: 666 of 923 = **72.2%** (published: 1,011 of 1,336 = 75.7%). Year range 2015–2026.
Median samples per series: 14, unchanged from the published catalogue.

## 7a. Deviations and limitations (replaces section 7)

- Classification remains **regex-only**. The LLM adjudication pass described as planned but not run in the
  published section 7 was still not run over the whole catalogue; a structured adjudication pass was used
  only for the eligibility candidates (222 series) and the precision audit (140 calls), in both cases with
  human review and stored evidence spans.
- Recall was not measured, and the catalogue is bounded by the nine modality queries (funnel step 2).
- Only GEO was searched. ArrayExpress/BioStudies, CELLxGENE and HTAN were not.
- The single-cell cue list counts spatial platform names (Visium, Xenium, CosMx, GeoMx, Slide-seq,
  Stereo-seq, MERFISH) as single-cell evidence, following the published filter-3 regex, which matches `10x`.
  Spatial-only series with no dissociated single-cell data therefore survive screen E1; at least two such
  series remain in the corrected catalogue (GSE228056, GSE195661).
- Whether a called modality is actually deposited in the same accession is quantified only provisionally
  (67.1%, section 5a) and was not used to filter the catalogue.
