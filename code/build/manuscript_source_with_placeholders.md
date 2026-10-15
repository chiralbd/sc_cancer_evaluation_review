---
title: "The evaluation gap in single-cell cancer genomics: a quantitative review, benchmark catalogue and ground-truth resource"
---

## Abstract

**Background.** Single-cell cancer genomics grew from 443 PubMed records in 2015 to 7,556 in 2025. Whether evaluation of its computational methods has kept pace has not been quantified.

**Methods.** We combined a 26-topic PubMed volume series (2015 to 15 October 2026); verification of all 486 evaluation-titled papers with an independent second coding pass; a catalogue of 269 PubMed-verified benchmarks in 16 method classes, coded for ground-truth strategy and for assessment of robustness, calibration and metric validity; and a catalogue of 1,336 GEO tumour single-cell series carrying orthogonal validation data; and explicit-definition coding of a stratified sample of 1,800 abstracts (150 per year, 2015–2026). Rates were modelled by negative-binomial and Poisson regression.

**Results.** Of 486 evaluation-titled papers, 158 (32.5%; 95% CI 28.5–36.8) were genuine benchmarks (inter-pass κ = 0.74). Benchmarks per 1,000 papers declined by 7.8% per year (rate ratio 0.922, 0.875–0.972); the decline was concentrated in biology and application topics (0.90 per year, 0.84–0.97), whereas method topics were flat. Over 2015–2026, method topics received more benchmarks per paper (IRR 2.35, 1.66–3.31). "No ground truth", the most frequently coded limitation (24.2%), did not replicate on re-coding (κ ≈ 0) and was stated in 1.1% of abstracts under an explicit definition. Abstracts stating any evaluation-check problem fell from 14.0% (2015–18) to 3.6% (2024–26). Robustness to analytical choices was reported in 5.6% of benchmarks, calibration in 3.3% and metric validity in 3.0%; metric validity was reported in none of the 48 cancer-specific benchmarks. Public validation data are more widely available than used: 138 series carry matched exomes, 227 CITE-seq protein and 250 paired spatial data, whereas 44 benchmarks state an orthogonal-assay ground truth.

**Conclusions.** Evaluation in this field is limited less by absent ground truth than by rarely performed checks and under-used public validation data. We release both catalogues, a ten-item evaluation standard and an eight-study research agenda.

**Keywords:** single-cell RNA sequencing; cancer genomics; benchmarking; meta-research; ground truth; calibration; multiverse analysis

## 1. Introduction

Biological conclusions drawn from tumour single-cell data depend on a sequence of computational decisions. The identification of malignant cells, the integration of patients, the reference used to label the immune compartment and the inference of cell-type proportions or interactions are each delegated to software. That software typically returns point estimates; in the benchmark literature catalogued here, calibration or uncertainty is assessed in 3.3% of studies (§3.4). Principles for evaluating such software are nevertheless established. Neutral comparison studies [@boulesteix2013] should be designed to avoid the self-assessment trap, in which developers rank their own method best [@norel2011; @buchka2021]. They should follow explicit design guidelines [@weber2019; @mangul2019] and be extensible as methods change [@sonrel2023; @luecken2025op]. Landmark neutral benchmarks exist for many single-cell tasks, including clustering [@duo2018], differential expression [@soneson2018; @squair2021], trajectory inference [@saelens2019], annotation [@abdelaal2019], batch correction [@tran2020; @luecken2022], doublet detection [@xi2021], cell–cell communication [@dimitrov2022], spatial integration [@li2022spatial], deconvolution [@avilacobos2020] and perturbation prediction [@ahlmann2025].

Two questions remain open. The first is whether this evaluation effort has reached cancer-specific applications; tumour microenvironment composition alone accounted for 9,383 papers in 2023–26 (Table 1). The second is whether it addresses the failure modes specific to tumour data. Malignant cells show extensive inter- and intratumoural transcriptional heterogeneity, with 41 recurrent meta-programmes identified across 1,163 tumour samples [@patel2014; @tirosh2016; @gavish2023]. Copy-number alterations, which are absent from normal tissue, are themselves inferred from expression [@patel2014; @gao2021; @gao2023]. Reference atlases used for annotation are built predominantly from non-malignant tissue [@regev2017]. None of these properties is represented in benchmarks that use only non-malignant data. Yet only 48 of the 269 benchmarks catalogued here (17.8%) are cancer-specific (§3.4).

This review quantifies the evaluation gap. We quantify how benchmark coverage has scaled with publication volume across 26 subtopics and test whether coverage is shrinking. We then ask what the literature says is wrong, and check whether those statements survive independent coding. Next we catalogue what existing benchmarks actually check, and locate where ground truth already exists in public repositories. Section 4 synthesises the state of evaluation for each major method class. Section 5 develops the three checks that the evidence identifies as most neglected: metric validity, robustness to analytical choices, and calibration. Section 6 maps the public ground-truth resource. Sections 7 and 8 propose a minimum evaluation standard and a research agenda. The benchmark catalogue, ground-truth catalogue and all derived tables are released with the paper.

## 2. Methods

### 2.1 Taxonomy, volume series and corpus

We defined 26 subtopics of single-cell cancer genomics spanning methods and measurement (for example CNV inference and scDNA-seq, integration, lineage tracing, spatial transcriptomics) and biology and application (for example immunotherapy response, tumour microenvironment composition, metastasis). For each topic and for the subfield as a whole, we retrieved annual PubMed record counts for 2015–2026 through NCBI E-utilities, giving 324 topic-year counts. Counts for 2026 run to 15 October 2026 (§2.7). We summarise growth as the ratio of a topic's 2025 share of the subfield to its 2021 share. Abstracts for 2023–2026 (n = 3,627) were harvested with topic tags; topics overlap and are not a partition. A bioRxiv screen (15,682 preprints, 18 months) yielded 372 single-cell cancer preprints. Because the bioRxiv API exposes only a short abstract preview, preprint ratios are not used inferentially here.

### 2.2 Benchmark verification and problem extraction

All 486 papers whose titles contained "benchmark", "comparison", "evaluation" or "assessment" were classified from their abstracts as genuine methods benchmarks or not. A genuine benchmark is a systematic comparison of two or more named tools or platforms on a shared task. Separately, each abstract in the corpus was coded for its stated limitations and open problems into a 17-category controlled vocabulary, giving 1,757 extraction rows. Of these, 1,506 were methodological problems.

### 2.3 Reliability of the coding

Both coding tasks were repeated blind to the first-pass labels, using a reworded prompt and a different model tier. A smaller model (Haiku-tier) rated 394 of the 486 benchmark abstracts. After that model's token budget was exhausted, the remaining 92 benchmark abstracts and the entire random subsample of 200 problem-coded abstracts (seed 1) were rated from condensed abstracts (title, opening and closing sentences) by the coordinating language-model agent that ran the analysis. That agent did not see the first-pass labels, but it is not an independent human coder, and no human adjudication was performed. We report Cohen's κ with bootstrap 95% intervals separately by rater subset. Second-pass counts are from one non-adjudicated pass and are treated as provisional.

### 2.4 Stated problems, 2015–2026

The archived abstract corpus covers 2023–2026 and is weighted towards recent records (2,073 of its 3,627 abstracts were first published in 2026, as confirmed by re-dating every record against PubMed). To examine change over time, we drew a stratified random sample of 150 research abstracts per publication year from 2015 to 2026 (seed 2026) from the subfield query, excluding reviews, editorials, comments and errata and requiring an abstract of at least 400 characters. Each abstract was coded by a model coder (Haiku-class, temperature 0, structured output, 15 abstracts per request) with written definitions for 17 problem types (Table 3); a problem type was coded only when the abstract explicitly stated it, and multiple types per abstract were allowed. The coder also flagged whether the study generated or analysed single-cell omics data, as distinct from flow cytometry, imaging or other non-sequencing single-cell assays. Because PubMed's publication-date field matches both electronic and print years, 29 papers were drawn in two adjacent years; each was counted once, in its earlier year, leaving 1,771 unique abstracts. Analyses were restricted to abstracts flagged as single-cell omics. A random 150 of the coded abstracts were re-coded independently by a stronger model (Sonnet-class) with the same definitions to estimate agreement. The 158 verified benchmarks were flagged for single-cell omics in the same way.

### 2.5 Benchmark catalogue

We assembled a catalogue of benchmark studies relevant to single-cell cancer genomics. Sources were the verified first-pass benchmarks within scope, 16 class-specific PubMed queries, about 90 targeted searches for landmark benchmarks, and 14 supplementary queries. Inclusion required that the primary contribution be a comparative evaluation of at least two existing methods, or of platforms with computational read-outs; preprint and journal versions were merged. All 269 records were resolved through PubMed efetch and re-checked by esummary title match. Evaluation fields were coded from abstracts by keyword rules, with manual correction of 40 records including all landmark records. The fields are the ground-truth strategy, the number of tools, and whether robustness to parameters, calibration or uncertainty, and the validity of the metric itself were assessed. A field is marked as assessed only when the abstract says so. All assessment counts are therefore lower bounds.

### 2.6 Ground-truth catalogue

We queried GEO DataSets for human tumour single-cell series. The base set held 6,141 series, and the union of nine modality queries gave 2,715 records. After filtering to sequencing-based, human, single-cell, cancer series, 2,024 were eligible. From series-level text we classified nine validation modalities: matched WES/WGS, CITE-seq protein, genotype or hashtag multiplexing, paired bulk RNA, paired spatial, mtDNA lineage, longitudinal or on-treatment sampling, cell-line mixtures and Perturb-seq. Classification used documented, spot-audited regular-expression rules. The result is 1,336 validation-bearing series in 1,166 SuperSeries-collapsed study groups. Each series was mapped to the benchmark tasks it can support. A modality call means the submitters state that the data were generated. Controlled-access deposition (dbGaP/EGA) was not checked, recall was not measured, and ArrayExpress, HTAN and CELLxGENE were not searched.

### 2.7 Update of 2026 counts to 15 October 2026

The volume series was first retrieved on 4 October 2026. To extend 2026 to 15 October 2026 without altering the 2015–2025 series, we reconstructed the subfield query and calibrated it against the archived counts: it reproduced every year from 2015 to 2025 within ±0.7% (for example, 442 versus 443 records in 2015 and 7,528 versus 7,556 in 2025). For each topic we selected, from two or three candidate clauses, the one that best reproduced the archived 2017, 2021 and 2025 counts. For every series we then counted 2026 records with an Entrez date up to 4 October and all 2026 records on 15 October using the same reconstructed query, and multiplied the archived 2026 count by this growth ratio, so that differences between the reconstructed and original queries cancel. Growth ratios ranged from 1.014 to 1.064 across topics and were 1.031 for the subfield, which rose from 7,342 to 7,571 records. The same title query identified three evaluation-titled 2026 records indexed after 4 October; none was a methods benchmark, so the verified 2026 benchmark count remains 25. All models in §2.8 were refitted on the updated denominators. Queries, counts and ratios are released in Supplementary Data S7.

### 2.8 Statistical analysis

Proportions carry Wilson score 95% intervals; benchmark rates per 1,000 papers carry exact Poisson intervals. Per-topic benchmark counts were modelled with NB2 negative-binomial regression, with an offset of log topic volume (2015–26 in the primary specification) and two covariates. One is log share change (2025 vs 2021). The other is an indicator for method and measurement topics, whose mapping and rationale are released with the paper. Sensitivity fits excluded the benchmarking topic itself, restricted numerator and offset to 2023–26, and used an alternative topic coding. Poisson fits are reported where the LR test for overdispersion was not significant. The temporal trend was modelled as a Poisson GLM of verified benchmarks per year with an offset of log subfield volume (2015–2026), with binomial and NB2 sensitivity fits and a 2015–2025 fit that excludes the partial year. Topic-level coverage was analysed over the full window (benchmarks and papers 2015 to 15 October 2026) as the primary specification, with the 2023–26 window as a sensitivity analysis. To locate the temporal decline, we fitted a Poisson model to topic-by-year benchmark counts with topic fixed effects, an offset of log topic-year volume and separate year slopes for method and biology topics, excluding the benchmarking topic. As sensitivity analyses for the subfield trend and the panel, numerators were restricted to single-cell-genomics benchmarks and denominators were multiplied by the yearly single-cell-omics share estimated from the stratified sample (§2.4). Prevalence trends in stated problems were tested by logistic regression on publication year. Before writing, 120 quantities quoted in our earlier gap analysis were recomputed from the archived data. 101 matched exactly and one matched approximately. Six did not match: preprint-ratio denominators, one rounded range, and a numerator-window inconsistency discussed in §3.2. Twelve could not be checked from archived data, and none of those twelve is used here.

### 2.9 Reference verification

Every work cited was resolved to its PubMed or Crossref record (one machine-learning conference paper via arXiv). For foundational references, the claim attributed to each work was checked against its abstract and rewritten where it was not supported as first stated. Records that could not be resolved were dropped rather than cited from memory.

## 3. Results

### 3.1 A fast-growing field whose growth is in applications

The subfield grew 17-fold between 2015 and 2025 (Fig. 1a; Table 1) and had already reached 7,571 records by 15 October 2026, a full-year pace of about 9,600. All 26 topics grew in absolute terms, but share moved sharply. Spatial transcriptomics in tumours gained share 6.2-fold between 2021 and 2025. Drug-response prediction gained 3.2-fold, deep learning and foundation models 3.1-fold, and cell–cell communication 2.3-fold. The topics losing share were mature method areas: clonal evolution and phylogeny (0.44×), CTC and liquid biopsy (0.46×), intratumour-heterogeneity metrics (0.67×) and lineage tracing (0.68×) (Fig. 1c). Benchmarking and evaluation as a topic accounted for 87 papers in 2025.

{{FIG1}}

{{TABLE1}}

### 3.2 Benchmark coverage is thin, uneven and declining

Of the 486 evaluation-titled papers, 158 (32.5%; 95% CI 28.5–36.8) were genuine method benchmarks; the remainder used "evaluation" for clinical or biological assessments, or were reviews or method papers with token baselines. Across 2015–2026, verified benchmarks per 1,000 subfield papers fell from 6.77 in 2015–2020 to 3.88 in 2023–2026 (rate ratio 0.57; exact conditional p = 0.0085). The yearly trend was a 7.8% annual decline (Poisson rate ratio 0.922, 95% CI 0.875–0.972, p = 0.0027; Fig. 1b). The decline held when the partial year 2026 was excluded (0.930, p = 0.020) and under NB2 and binomial specifications. The share of evaluation-titled papers that were genuine benchmarks showed no trend (odds ratio 0.973 per year, p = 0.40). Coverage therefore fell because evaluation-titled work of every kind failed to keep pace with the field (rate ratio 0.940 per year, 0.911–0.969), not because evaluation work became less rigorous.

The subfield query does not capture single-cell genomics alone. In the stratified sample (§2.4), the share of abstracts that used single-cell omics data rose from 17% in 2015 to 89% in 2026 (§3.3), and 100 of the 158 verified benchmarks were single-cell-genomics benchmarks. When both the numerator and the denominator were restricted to single-cell genomics, the point estimate was similar but no longer significant (rate ratio 0.920 per year, 0.844–1.003, p = 0.058; 2015–2025 only, 0.95, 0.86–1.06). The subfield-wide decline is therefore robust, whereas the decline within single-cell genomics alone is consistent in direction but not established.

Across the full 2015–2026 window, coverage differs by more than an order of magnitude across topics (Fig. 2a; Table 2). The subfield produced 34,595 papers and 157 verified benchmarks in this window. Lineage tracing (397 papers) and perturbation screens (136 papers) had no verified benchmark. Bulk deconvolution, CNV inference and clonal phylogeny had 8.2–11.5 benchmarks per 1,000 papers, whereas the four largest biology topics (clinical prognosis, tumour microenvironment composition, immunotherapy response and metastasis) each had between 1.4 and 2.2. Clinical prognosis and biomarkers produced 16,859 papers and 37 benchmarks in 2015–26.

The negative-binomial model separates topic size from topic type (Fig. 2c). Across all 26 topics, method and measurement topics received more benchmarks per paper (IRR 4.84, 2.09–11.18). This estimate is inflated by the benchmarking topic itself, which is by construction dense in benchmarks. Excluding it reduced overdispersion to near zero (α = 0.05) and gave IRR 2.35 (1.66–3.31). The method-topic effect was robust to an alternative topic coding (IRR 1.88, 1.19–2.98) and to a 2023–26 window (2.81, 1.87–4.22). Share growth was associated with fewer benchmarks per paper in every specification, but the association was not significant over the full window (IRR 0.79 per e-fold, 0.60–1.06, p = 0.11) or in the 2023–26 window (0.77, 0.55–1.08), and it should be read as suggestive.

A topic-by-year panel locates the decline (§2.8). With topic fixed effects and an offset of log topic-year volume (294 topic-years, 25 topics), benchmark coverage in biology and application topics fell by 9.9% per year (rate ratio 0.901, 0.840–0.966, p = 0.0035), whereas coverage in method and measurement topics did not change (rate ratio 1.012, 0.927–1.103). The two slopes differed (ratio 1.12, 1.00–1.26, p = 0.042). Restricting the panel to single-cell-genomics benchmarks and genomics-adjusted denominators preserved the decline in biology and application topics (rate ratio 0.882, 0.795–0.979, p = 0.018), although the difference between slopes was no longer significant (p = 0.086). The evaluation deficit is thus growing specifically in the application topics that account for most of the literature.

The numerator window also qualifies a claim in our earlier gap analysis. Counting benchmarks from all years against 2023–26 papers makes CTC and liquid-biopsy work appear well benchmarked, at 71 papers per benchmark. Counting only 2023–26 benchmarks gives about 189 papers per benchmark. Mature topics are well covered partly by older work that may predate current methods.

{{FIG2}}

{{TABLE2}}

### 3.3 What the literature says is wrong, and what survives re-coding

Under first-pass coding, the most common methodological problem was "no ground truth" (364/1,506; 24.2%, 22.1–26.4). It was the top-ranked problem in 21 of 26 topics. It was followed by causality (19.9%) and interpretability (12.5%) (Table 3). Three categories describe checks that need no gold standard, and all three were rare: parameter sensitivity (2.3%, 1.6–3.1), metric invalidity (1.1%, 0.7–1.7) and uncertainty (0.7%, 0.4–1.2).

Independent re-coding changes the interpretation of the most common category (Fig. 3). Benchmark classification showed substantial agreement: 88.5% and κ = 0.74 (0.68–0.80), or κ = 0.76 on the 394 abstracts rated by the model. The second pass found 166 benchmarks against 158, and the two passes agreed on 134. Problem-type coding replicated poorly overall (pooled κ = 0.23, 0.17–0.29). "No ground truth" did not replicate at all: 45 of 200 subsample abstracts under the first pass, 1 under the second (κ = −0.01). The second coder assigned 30 of the 45 to causality and 9 to interpretability. On inspection, these statements describe unknown mechanisms or an uncharacterised landscape rather than the absence of a reference standard. Merging the three knowledge-gap categories raised agreement to κ = 0.51 (0.38–0.62). The 24.2% figure therefore measures the field's statements of unknown biology, not a stated shortage of evaluation truth, and we do not use it as evidence of an evaluation deficit.

The three neglected checks behave differently. They are rare under both codings: in the 200-abstract subsample, metric invalidity was 4 versus 0, parameter sensitivity 2 versus 0, and uncertainty 0 versus 0. Their κ values are undefined or zero because almost nothing is coded in either pass. Rarity is the replicated finding; the per-category agreement statistic is uninformative at this prevalence. We therefore test the same three checks directly in the benchmark literature (§3.4), where the question is whether the evaluation was done, not whether authors complained about its absence.

To test whether these patterns hold across the history of the field, we coded a stratified sample of abstracts from 2015 to 2026 under explicit definitions (§2.4; Fig. 4). The 1,800 draws contained 1,771 unique abstracts, of which 989 used single-cell omics data. Under the explicit definition, "no ground truth" was stated in 1.1% (0.6–2.0) of these abstracts, confirming that the first-pass figure of 24.2% reflected a loose category rather than a frequent complaint. The most frequently stated problems were sample size (15.3% (13.2–17.6)), generalisability (14.5% (12.4–16.8)) and clinical translation (8.5% (6.9–10.4)); the last increased over time (OR 1.14 per year (1.05–1.24)). The five problem types that correspond to evaluation checks were each stated in less than 2% of abstracts: parameter sensitivity 1.8% (1.2–2.9), absence of benchmarks 1.4% (0.8–2.4), uncertainty 1.3% (0.8–2.2), absence of ground truth 1.1% (0.6–2.0) and metric validity 0.4% (0.2–1.0). Taken together, the share of abstracts stating any of the five fell from 14.0% in 2015–18 to 3.6% in 2024–26 (OR 0.81 per year, 0.74–0.88; Fig. 4c), a steeper decline than for any stated problem (55.0% to 41.2%; OR 0.94 per year (0.90–0.98)). Agreement between two model coders on 150 abstracts was high for the single-cell-omics flag (κ = 0.88) and for technical artefacts (κ = 0.85), moderate for sample size (κ = 0.63), and low for the presence of any stated problem (κ = 0.35) and for most rare categories, which had five or fewer positives under either coder. Because a single coder and prompt were applied to every year, systematic coder bias is constant across years, but the absolute prevalences should be interpreted as approximate.

{{FIG4}}

{{FIG6}}

{{TABLE3}}

### 3.4 What benchmarks check

The 269 catalogued benchmarks span 16 method classes (Table 4). 151 (56.1%) were published in 2024–2026 and 48 (17.8%) are cancer-specific. Simulation was the most commonly stated source of ground truth (91; 33.8%). Orthogonal assays were stated in 44 (16.4%) and expert or published labels in 24 (8.9%). Held-out experimental measurements appeared in 12, genotype multiplexing in 11 and cell-line mixtures in 8. 107 abstracts (39.8%) did not state their ground truth at all (Fig. 5a).

Physical ground truth is concentrated in a few classes. Doublet and ambient-RNA benchmarks use genotype or synthetic-barcode truth in 10 of 13. Perturbation-prediction benchmarks score held-out measurements in 10 of 11. Annotation benchmarks rely on expert labels in 9 of 17, and foundation-model evaluations do not state truth in 11 of 14.

Robustness to parameters or pipeline choices was stated in 15 benchmarks (5.6%), calibration or uncertainty in 9 (3.3%) and metric validity in 8 (3.0%) (Fig. 5b). Among the 48 cancer-specific benchmarks the counts were 4, 2 and 0. Abstract-level coding undercounts these checks. Even so, the same three dimensions are the least represented both in what the literature states as problems and in what the benchmarks report doing. This convergence, from two independent sources, is the central empirical result of this review.

{{FIG3}}

{{TABLE4}}


## 4. State of evaluation by method class

This section summarises, for each method class, the findings that are consistent across benchmarks, those that conflict, and the questions that no benchmark has addressed. Counts refer to the 269-record catalogue (Supplementary Data S1); claims are limited to what the cited abstracts report.

### 4.1 CNV inference and malignant-cell calling

All seven benchmarks in this class are cancer-specific and published in 2024–2026 [@chen2025cnv; @song2025cnv; @oketch2024; @dugo2025; @p42039587; @p41038850; @p40584741]. A consensus is emerging but conditional. Haplotype-aware inference with Numbat [@gao2023] leads when allelic information is available. Expression-only callers such as copyKAT [@gao2021] and SCEVAN [@defalco2023] are the practical default otherwise, though inferCNV-style smoothing [@patel2014; @tirosh2016] remains the most used. Two disease-specific comparisons found less than 30% overlap between callers and many false positives [@oketch2024; @dugo2025]. Reference choice, depth and purity change results [@p40584741; @song2025cnv]. This is the only class in which sensitivity to the reference is routinely reported. No benchmark scores the binary malignant call against a shared, matched DNA-level truth across tumour types, or stratifies by aneuploidy burden. Near-diploid tumours, in which expression-based CNV inference has little copy-number signal to exploit, are not analysed as a separate stratum in any of the seven benchmarks.

### 4.2 Bulk deconvolution

Deconvolution is among the most benchmarked classes, with 29 records, 10 of them cancer-specific. Its ground truth is mostly pseudo-bulk simulation (16 of 29). Results are sensitive to normalisation and reference construction [@avilacobos2020] and degrade sharply when a cell type is missing from the reference [@p33159064]. More realistic heterogeneous pseudo-bulk reorders the methods [@p38956606]. None of the 29 abstracts reports uncertainty on estimated proportions, and none examines metric validity. For tumours, deconvolution of malignant states against DNA-level truth is missing. The ground-truth catalogue lists 459 series with paired bulk and single-cell data from the same tumours that could anchor such a test.

### 4.3 Integration and batch correction

Atlas-level integration has a mature benchmark [@luecken2022], earlier comparisons [@tran2020] and the only dedicated metric critique in the catalogue. That critique shows that silhouette-based scores cannot reliably assess batch removal or conservation of biological signal [@rautenstrauch2025]. Only 1 of 25 integration benchmarks is cancer-specific. Integration benchmarks score the removal of batch effects jointly with the conservation of biological variation [@luecken2022]. In tumours, patient-specific malignant programmes [@tirosh2016; @gavish2023] are confounded with patient as a batch variable. No integration benchmark in the catalogue quantifies how much of that patient-specific malignant signal is removed.

### 4.4 Annotation and label transfer

General-purpose classifiers are a strong baseline for automatic annotation [@abdelaal2019]. Annotation benchmarks rely mostly on author-supplied labels (9 of 17), which raises a circularity problem: the labels were usually derived from the same marker genes that the evaluated tools use. Calibration of label confidence and rejection of unknown cell types are assessed in only one record, and it is not cancer-specific [@p40439669]. Conformal prediction sets for annotation with guaranteed coverage have been proposed [@lopezdecastro2025], but have not been evaluated on tumour data. Whether confidence scores remain calibrated when the malignant compartment is absent from the reference, the default situation in tumour data, has not been tested.

### 4.5 Cell–cell communication

Communication inference is shaped as much by the choice of ligand–receptor resource as by the choice of method [@dimitrov2022]. Only 6 benchmarks exist and none is cancer-specific, although communication is among the fastest-growing topics (2.3-fold share gain). Spatial co-localisation is used as a proxy truth [@dimitrov2022; @p36253792]. No benchmark uses matched spatial data from the same tumour as an external referee, though the ground-truth catalogue lists 250 series with paired spatial data.

### 4.6 Spatial transcriptomics

Spatial methods have 36 benchmarks. For spot deconvolution, cell2location and RCTD are repeatedly among the best [@li2022spatial; @p38787371], but a simple regression baseline outperforms nearly half of the dedicated methods [@p38787371]. No domain-detection method wins across platforms [@p40240000]. Metric validity is beginning to be examined in this class, with critiques of spatial ARI [@p41001748] and of clustering-benchmark pitfalls [@p42637979]. A type-I-error assessment of co-localisation statistics in cancer [@p40051984] is one of only two calibration analyses among cancer-specific benchmarks.

### 4.7 Gene-regulatory-network inference

GRN benchmarks report modest performance overall. On experimental data, methods often do not beat random predictors [@p37215029; @p29914350], and interventional methods do not beat observational ones [@p40069299]. None of the 13 GRN benchmarks is cancer-specific. The aneuploid tumour genome, where expression changes track copy number, breaks assumptions that GRN inference makes in normal tissue, and this has not been benchmarked.

### 4.8 Lineage tracing and clonal phylogeny

Lineage tracing is the thinnest class: 3 records, none of which benchmarks mitochondrial-variant clone callers. Natural mtDNA mutations are now an established lineage marker in human cells [@ludwig2019; @lareau2021; @miller2022; @weng2024], and dedicated variant-selection tools exist [@kwok2022]. Yet 266 lineage-tracing papers in 2023–26 rely on these callers without a neutral comparison. Clonal-phylogeny benchmarks are mostly older comparisons of whole-genome amplification protocols. No neutral benchmark of single-cell phylogeny-inference tools on shared truth was found.

### 4.9 Differential expression and abundance

DE has the most consistent methodological consensus in the catalogue. Tests that treat cells as independent replicates inflate false discoveries, while pseudobulk and mixed models control them [@squair2021; @zimmerman2021; @crowell2020]. This is the single-cell form of a classical pseudoreplication error [@lazic2010]. DE is also the class in which calibration (FDR control) is most often assessed (4 of 12). No DE or DA benchmark is cancer-specific. In tumours, patient-specific malignant states violate the assumption that cell types are shared across conditions.

### 4.10 Doublets, demultiplexing and ambient RNA

This is the best-grounded class. Genotype multiplexing [@kang2018; @heaton2020; @huang2019] and antibody or lipid hashing [@stoeckius2018; @mcginnis2019multi; @howitt2023] supply truth in 10 of 13 benchmarks [@xi2021; @p42688285]. None of the 13 is cancer-specific. Because doublet and ambient-RNA correction precede malignant-cell calling (§4.1), errors at this step propagate to it, but that propagation has not been measured in tumour data. Genetic demultiplexing has been shown to work in pooled tumour samples [@weber2021gs], so the experimental design for a tumour-specific benchmark exists.

### 4.11 Perturbation prediction and foundation models

Perturbation prediction has the strongest consensus in the catalogue. Simple linear or mean baselines match or beat deep-learning and foundation-model predictors [@ahlmann2025; @p40759747; @p41250104]. It is also the class where metric validity is most actively studied (4 of 11 records). Correlation-based scores can be inflated by reusing control cells [@p42182243], and R² can hide failures on differentially expressed genes [@p40161693]. Foundation models do not consistently beat simpler baselines in zero-shot evaluation [@kedzierska2025; @p40251685], and show limited advantage for cancer patient outcomes [@p41279698]. None of these abstracts states a check for leakage between pretraining corpora and test sets.

### 4.12 Drug-response prediction

Drug-response prediction gained share 3.2-fold since 2021 but has 3 benchmarks in the catalogue [@p41381537]. No shared single-cell truth set with measured per-cell or per-clone response exists. Pooled cell-line designs with SNP demultiplexing [@mcfarland2020] and patient-model Perturb-CITE-seq [@frangieh2021] show how one could be built.

## 5. Three neglected checks

The analyses in §3 identify three checks that are rare both as stated problems and as reported analyses. None of them requires a new gold standard.

### 5.1 Is the metric measuring what it claims?

A benchmark is only as informative as its scoring function. Chance-corrected partition agreement [@hubert1985] has known dependence on cluster number and balance [@steinley2004]. Silhouette widths [@rousseeuw1987] can reward over-correction in integration [@rautenstrauch2025]. Two-dimensional embeddings distort high-dimensional structure in ways that make them poor evaluation targets [@chari2023]. In perturbation prediction, the choice of metric and control can change the ranking of methods [@p42182243; @p40161693]. Metric validity can be checked without ground truth. A valid metric must respond monotonically to controlled degradation (adding noise, merging clusters, permuting labels). It must not be maximised by trivial baselines, and it must rank methods consistently with an orthogonal criterion where one exists. Not one of the 48 cancer-specific benchmarks in the catalogue reports such a check in its abstract.

### 5.2 Is the conclusion robust to defensible analytical choices?

Outside genomics, analytical flexibility is a documented source of false or fragile findings [@ioannidis2005; @simmons2011]. Two remedies exist. Multiverse analysis [@steegen2016] and specification-curve analysis [@simonsohn2020] report a result across all defensible pipelines. Many-analyst studies show directly that teams given the same data reach different conclusions [@silberzahn2018; @botvinik2020]. A standard single-cell workflow involves a sequence of defensible but consequential analytical choices. Transformation choice [@ahlmann2023], preprocessing pipeline [@vieth2019; @shainer2021; @germain2020] and preprocessing for RNA velocity [@soneson2021] each change downstream results. A recent study of cancer scRNA-seq reports that normalisation choice alone drives biological interpretation [@saxena2026]. Yet robustness was stated in 5.6% of benchmarks and in 4 of 48 cancer-specific ones. The parallel question for biological claims has not been asked systematically: how often does the headline result of a tumour scRNA-seq paper survive the defensible alternatives? Community best-practice guides [@luecken2019; @heumos2023] narrow the range of choices but do not quantify the sensitivity of conclusions to the choices that remain.

### 5.3 Is the stated confidence honest?

Modern predictive models are often overconfident [@guo2017]. Conformal prediction provides distribution-free coverage guarantees for any model [@lei2018; @vovk2022; @angelopoulos2023]. Single-cell applications are only beginning to appear, for cell-type annotation [@lopezdecastro2025] and in the recognition that reference-based annotation needs explicit uncertainty [@natgen2024brief]. Calibration was stated in 3.3% of benchmarks. Per-cell malignancy probabilities, deconvolution proportions, annotation scores, inferred interactions and perturbation predictions are almost never reported with calibrated uncertainty. The relevant test is simple: a reliability diagram and an expected calibration error against an independent label. Its most informative stress case is the tumour-specific one, cells from populations absent from the reference.

### 5.4 Null models

A fourth, related check is comparison against an appropriate null. Most random gene-expression signatures are significantly associated with breast-cancer outcome [@venet2011]. Meta-analysis of published ovarian-cancer signatures found modest, overlapping performance across validation cohorts [@waldron2014]. Clinical prognosis is the largest topic in this subfield (13,532 papers in 2023–26) and produced 23 benchmarks in that window. Single-cell-derived prognostic signatures have not been systematically tested against size- and proliferation-matched random sets.

## 6. Ground truth already exists

### 6.1 Designs that supply truth

Several experimental designs provide truth independent of the transcriptome being analysed (Table 5). Cell-line mixtures with known composition [@tian2019; @zheng2017; @mereu2020; @ding2020] supply known identity and proportions. Genotype multiplexing with demuxlet, souporcell and vireo [@kang2018; @heaton2020; @huang2019] and antibody or lipid hashing [@stoeckius2018; @mcginnis2019multi] supply known sample of origin and doublet status. Genotype demultiplexing works in pooled tumour samples [@weber2021gs]. CITE-seq and related assays [@stoeckius2017; @peterson2017; @mimitou2019; @hao2021] give a protein readout that is measured independently of the RNA used for annotation. Spike-ins [@jiang2011; @svensson2017; @ziegenhain2022] supply known molecule counts. Somatic mtDNA variants supply lineage relationships [@ludwig2019; @lareau2021; @miller2022]. Pooled CRISPR screens with single-cell readout [@dixit2016; @adamson2016; @replogle2022; @frangieh2021] supply known interventions. Matched exome or genome sequencing supplies DNA-level truth for malignancy and clone structure.

Simulation remains the most common stated ground truth (33.8% of benchmarks), but its fidelity is limited. Most scRNA-seq simulators fail to reproduce multi-group and batch structure [@crowell2023; @cao2021]. Newer simulators improve fidelity [@zappia2017; @sun2021sd2; @song2024], but a ranking obtained on simulated data needs confirmation on physical truth.

### 6.2 Where it is, publicly

The ground-truth catalogue locates 1,336 GEO series (1,166 study groups) of human tumour single-cell data with at least one orthogonal validation modality (Fig. 6; Table 5). The modalities are paired bulk RNA in 459 series, longitudinal or on-treatment sampling in 297, paired spatial data in 250, CITE-seq protein in 227, genotype or hashtag multiplexing in 166, matched WES/WGS in 138, Perturb-seq in 89, cell-line mixtures in 25 and mtDNA lineage in 18. Three quarters of these series (75.7%) were deposited in 2023–26, so the resource is newer than most of the benchmarks that could use it. Coverage is uneven. Lung cancer is represented by 19–50 series in each of the six most frequent modalities, and breast cancer and glioma by 8–47. Cell-line mixtures and mtDNA lineage data are rare everywhere: 25 and 18 series, with mtDNA lineage concentrated in chronic lymphocytic leukaemia and colorectal cancer. Mapping modalities to tasks gives 162 series usable for malignant-calling truth, 153 for clone calling, 356 for annotation calibration and 250 for a spatial referee of communication inference. These complement curated atlases and portals [@sun2021tisch; @han2023tisch2; @yuan2019; @gavish2023; @rozenblatt2020; @cellxgene2025; @regev2017; @kinker2020; @zheng2021; @cheng2021], which index expression data but not the validation modalities that make data usable for evaluation.

{{FIG5}}

{{TABLE5}}

## 7. A minimum evaluation standard

On the basis of the gaps quantified in §3, we propose a ten-item standard that method papers and benchmarks in this field could meet with existing data (Box 1). It extends general benchmarking guidelines [@weber2019; @boulesteix2013] with the four checks found to be least often reported: metric validity, analytical robustness, calibration and null-model comparison.

> **Box 1. Minimum evaluation standard for single-cell cancer methods**
>
> 1. **Declare the design.** State whether the study is neutral or developer-led; developer-led comparisons should report the self-assessment risk [@norel2011; @buchka2021].
> 2. **Name the ground truth and its independence.** State what the truth is, how it was obtained, and whether it shares information (markers, genes, cells) with the method being scored.
> 3. **Prefer physical truth.** Where the ground-truth catalogue lists a matching modality (Table 5), use it; treat simulation as a complement, and report a realism check [@crowell2023].
> 4. **Validate the metric.** Show that the metric responds to controlled degradation and is not maximised by a trivial baseline.
> 5. **Report a multiverse.** Re-run the headline comparison across the defensible preprocessing choices (normalisation, feature selection, integration, resolution, reference) and report the spread [@steegen2016; @simonsohn2020].
> 6. **Report calibration.** For any probability or confidence score, report a reliability diagram and expected calibration error; include cells from populations absent from the reference.
> 7. **Use the replicate as the unit.** Infer at the level of patients or samples, not cells [@squair2021; @zimmerman2021].
> 8. **Include simple baselines and nulls.** Linear or mean predictors, random gene sets of matched size, and permuted labels [@ahlmann2025; @venet2011].
> 9. **Stratify by tumour properties.** Report performance by aneuploidy burden, purity and cancer type where the data allow.
> 10. **Release for extension.** Release code, inputs and per-method outputs in a form that lets the benchmark be extended [@sonrel2023; @luecken2025op].

## 8. Research agenda

Table 6 lists eight concrete studies, ordered by the strength of the gap evidence and the readiness of public data. Each can be conducted with series already listed in the ground-truth catalogue, without new data generation. For each, both a positive and a negative outcome would be informative, because neither outcome has been established empirically.

{{TABLE6}}

## 9. Limitations

Several limitations qualify these findings.

First, all problem coding and benchmark-attribute coding used abstracts rather than full texts. A robustness or calibration analysis reported only in a supplement is not captured, so the 5.6%, 3.3% and 3.0% figures are lower bounds. The direction of this bias is known but its magnitude is not; a full-text audit of the 48 cancer-specific benchmarks would bound it.

Second, coding was model-assisted, and the second coding pass was not performed by an independent human. Benchmark classification replicated well (κ = 0.74), whereas problem-type coding did not (pooled κ = 0.23), and its most frequent category did not replicate at all. For this reason the problem-type distribution is not used as primary evidence of the evaluation gap. The second raters differed by subset: a smaller model for 394 benchmark abstracts (κ = 0.76), and the coordinating language-model agent, reading condensed abstracts, for the remaining 92 (κ = 0.48) and for all 200 problem-type abstracts. The problem-type reliability estimates therefore rest entirely on a model second rater. No pass was adjudicated, and a human-coded reliability sample is the most important next step for this evidence layer.

Third, coverage of both catalogues is incomplete. PubMed searches were relevance-ranked and capped, so benchmarks available only as preprints are missing. The ground-truth catalogue was built with regular-expression rules on series-level text; precision was spot-audited, recall was not measured, and only GEO was searched.

Fourth, topics are keyword-defined and overlapping, and the method/biology indicator is an author classification. An alternative coding was fitted as a sensitivity analysis and preserved the direction of every effect.

Fifth, influence is proxied by publication volume rather than citations; citation-weighted analysis could change which gaps are judged most consequential.

Sixth, the subfield query captures single-cell work beyond genomics, especially before 2020: only 17% of sampled 2015 abstracts used single-cell omics data, against 89% in 2026. The subfield-wide decline in benchmark coverage is robust, but restricted to single-cell genomics it is consistent in direction and not significant (rate ratio 0.92, 0.84–1.00); the decline in biology and application topics persists under the same restriction.

Seventh, the 2015–2026 problem coding is model-based, and agreement between two model coders was low for the presence of any stated problem (κ = 0.35) and for most rare categories. Prevalence trends are interpretable because one coder and one prompt were applied to all years, but absolute prevalences are approximate.

## 10. Conclusions

Publication volume in single-cell cancer genomics has grown faster than the evaluation of the methods on which that literature depends. Benchmark coverage per paper is falling (rate ratio 0.922 per year), and the fall is concentrated in biology and application topics (0.90 per year). Over the same period, the share of abstracts that state any evaluation-check problem fell from 14.0% to 3.6%. The most frequently coded limitation, an absence of ground truth, did not replicate under independent coding (κ = −0.01). Public ground truth is available: matched exomes, surface-protein measurements, genotype pools and spatial data exist for 1,336 tumour series. The checks that are missing, namely metric validity, robustness to analytical choices and calibrated uncertainty, require no new ground truth. These checks are rare both among the problems the literature states and among the analyses its benchmarks report. The catalogues released with this review are intended to lower the cost of performing them.

## Supplementary information

The following files accompany this review:

{{RESOURCES}}

Literature and repository data were retrieved from PubMed (NCBI E-utilities), Crossref, bioRxiv and NCBI GEO between 4 and 15 October 2026; PubMed volume counts were updated to 15 October 2026.

## Declarations

**Ethics approval and consent to participate.** Not applicable; this study analysed published literature and public repository metadata only.

**Consent for publication.** Not applicable.

**Availability of data and materials.** All derived data are provided as Supplementary Data S1–S8 (listed above) and in the accompanying archive. Source records are publicly available from PubMed, Crossref, bioRxiv and NCBI GEO.

**Code availability.** Model inputs (coverage_model_input.csv) and full model specifications (methods_statistics.md) are provided in Supplementary Data S7, from which every reported model can be refitted. Figure source data are provided as Tables 1–6 and Supplementary Data S1–S7. All code used for data retrieval, abstract coding, statistical analysis, figure generation and typesetting is provided as Supplementary Data S9. It comprises standalone Python scripts that refit every reported model from the supplied inputs and check the results against the values printed in this article, the PubMed query definitions and E-utilities retrieval scripts, the verbatim coding instructions, and the complete record of executed analysis code. Analyses used Python 3.11.16 with NumPy 2.4.6, pandas 2.3.3, SciPy 1.17.1, statsmodels 0.15.0 and Matplotlib 3.11.1; the manuscript was typeset with pandoc 3.12.1 and Tectonic 0.17.0.

**Competing interests.** The author declares no competing interests.

**Funding.** This work received no specific funding.

**Authors' contributions.** [To be confirmed by the author before submission.]

**Acknowledgements.** None.

**Use of artificial-intelligence tools.** Literature retrieval, abstract coding, the second coding pass and drafting were performed with the assistance of large language models under the protocol described in §2. All bibliographic records were resolved against PubMed, Crossref or arXiv, and coding reliability is reported in §3.3. The author takes responsibility for the content.

## References

{{REFERENCES}}
