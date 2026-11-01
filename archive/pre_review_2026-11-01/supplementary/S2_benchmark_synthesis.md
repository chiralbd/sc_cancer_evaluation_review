# Benchmark catalogue for single-cell cancer genomics — per-class synthesis

Companion to `benchmark_catalogue.csv` (269 records) and `benchmark_catalogue_class_summary.csv`. Every PMID cited below is a row of the catalogue. All bibliographic fields were taken from PubMed efetch, and every record was re-checked by esummary title match (269/269 matched). Data pull: 14–15 Oct 2026.

## How the catalogue was built

- **Sources.** (a) The 158 `is_benchmark=True` PMIDs from the prior `benchmark_classification.csv`. Of these, 54 are included directly and 4 more appear only as alternative (preprint/duplicate) versions of included papers. The remaining 100 were excluded as out of scope: clinical/assay comparisons, dosimetry, cell-culture models and similar (54+4+100=158). (b) 16 class-specific PubMed benchmark queries (top 80 by relevance each). (c) About 90 targeted landmark/title queries, e.g. Luecken 2022, Saelens 2019, Abdelaal 2019, Squair 2021, Xi & Li 2021, Dimitrov 2022, Li B 2022, Li H 2023, Pratapa 2020, Ahlmann-Eltze 2025, Kedzierska 2025, Csendes 2025, Kernfeld 2025. (d) 14 supplementary title-level queries for the thinner classes. The pool held about 1,750 candidates. Inclusion was decided by manual title screening, aided by an LLM pre-screen of the first 500 candidates.
- **Inclusion rule.** The paper's primary contribution must be a comparative evaluation of at least 2 existing computational methods, or of platforms/protocols with computational read-outs. New-method papers and pure reviews were excluded. Preprint and journal versions were merged (`other_version_pmids`), keeping the journal record.
- **Evaluation fields.** These were extracted from abstracts by transparent keyword rules. 40 records, including all landmarks and all CNV, lineage, perturbation and drug-response records, were checked and corrected by hand against the abstract (`extraction` column). The boolean fields take the value `True` or `unclear`. `unclear` means the abstract does not say; it does **not** mean "not assessed". **All assessment counts are therefore lower bounds from abstracts and are provisional** until full texts are read.

## Cross-class headline numbers (abstract-level, provisional)

| Quantity | n / 269 |
|---|---|
| Cancer-specific benchmarks | 48 (17.8%) |
| Published 2024–2026 | 151 (56.1%) |
| Ground truth mentions simulation | 91 (33.8%) |
| Orthogonal assay (WES/WGS/scDNA, CITE-seq, FISH/imaging, protein) | 44 (16.4%) |
| Expert/published annotation | 24 (8.9%) |
| Held-out experimental measurements (perturbation/drug) | 12 (4.5%) |
| Genotype multiplexing / barcoded singlets | 11 (4.1%) |
| Curated reference (literature/ChIP/database) | 9 (3.3%) |
| Cell-line mixture / controlled reference sample | 8 (3.0%) |
| Consensus-only | 3 (1.1%) |
| Ground truth not stated in abstract | 107 (39.8%) |
| Robustness to parameters/pipeline choices stated | 15 (5.6%) |
| Calibration / uncertainty / error-rate control stated | 9 (3.3%) |
| Validity of the evaluation metric itself examined | 8 (3.0%) |
| Code/data availability stated in abstract | 52 (19.3%) |

Within the 48 cancer-specific benchmarks, 14 mention an orthogonal assay and 11 simulation. Parameter robustness is stated in 4, calibration in 2 (40051984, 42070330), and metric validity in **0**.

These proportions match the corpus-level gap review. Parameter sensitivity was 2.3%, uncertainty 0.7% and metric validity 1.1% of methodological limitation statements. Among dedicated benchmarks, these three properties are also the least-assessed dimensions.

---

## 1. CNV inference & malignant-cell calling (n = 7, all cancer-specific, all 2024–2026)

- **What is benchmarked.** scRNA-seq CNV callers: inferCNV, CopyKAT, CaSpER, HoneyBADGER, sciCNV, SCEVAN, Numbat and others. Tasks are malignant-vs-normal classification, CNV-profile accuracy and subclone recovery (42039587, 41038850, 40584741, 40037644, 39200223, 41160707). Spatial CNA inference (9 methods, 69 sections) is covered by 42838986.
- **Ground truth.** A mixture of orthogonal DNA-level truth (matched multi-omics/WGS: 40037644, 41038850), cell-line mixtures (40584741), simulation (42039587) and marker-based expert labels (39200223, 41160707). No benchmark uses one shared, matched scDNA+scRNA truth set across all tools.
- **Consensus.** Allele-aware methods (Numbat) lead when allelic information is available. Expression-only tools (CopyKAT, SCEVAN) are the practical default otherwise (40037644, 42039587, 41038850). Two disease-specific comparisons report <30% overlap between callers and many false positives (39200223, 41160707).
- **Sensitivity.** Reference choice, sequencing depth and tumour purity strongly change results (40584741, 40037644, 41038850). This is the only class where parameter/reference sensitivity is routinely reported (3/7).
- **Never assessed (abstract level).** Calibration of per-cell malignancy probabilities, metric validity, and performance in low-aneuploidy tumours or across tumour-type strata with an independent DNA truth.

## 2. Bulk deconvolution (n = 29, 10 cancer-specific)

- **What.** Reference-based and reference-free deconvolution of bulk RNA-seq, methylation and cfDNA/EV data.
- **Ground truth.** Mostly pseudo-bulk simulation from scRNA-seq (16/29; e.g. 33159064, 38956606, 41582216, 33845875). Orthogonal truth (flow cytometry, IHC, multi-assay snRNA/RNAscope) appears in 8 (31878981, 40197307, 41408313, 38412834, 38755121). Controlled mixtures appear in 2 (31510660, 34346485).
- **Consensus.** Accuracy collapses when a cell type is missing from the reference (33159064). Realistic heterogeneous pseudo-bulk changes the rankings; BayesPrism and a MuSiC/CIBERSORTx hybrid perform best there (38956606). Bisque/hspe win on multi-assay brain truth (40197307). Results in tumours depend on experimental factors (37864274).
- **Never assessed.** Uncertainty or confidence intervals on estimated proportions (0/29) and metric validity (0/29). Malignant-cell-state deconvolution with a DNA-level truth is also missing.

## 3. Data integration / batch correction (n = 25, 1 cancer-specific)

- **What.** scRNA-seq batch correction (31948481, 34949812, 33524142), multimodal/mosaic integration (39322753, 38493343, 37875977, 41083898, 41214134), cross-species integration (37838716, 39778870) and semi-supervised integration (41838767).
- **Ground truth.** Published annotations combined with batch labels. Real batches are labelled "expert annotation" or unclear; simulation appears in 5. Paired multi-omics serves as orthogonal truth in 6.
- **Consensus.** scANVI, Scanorama, scVI and scGen lead on complex atlas tasks (34949812). Harmony, LIGER and Seurat 3 lead in the earlier benchmark (31948481). Rankings depend on HVG selection and scaling (34949812).
- **Metric validity.** The only class with a dedicated metric critique: silhouette-based scores mislead (40739072). The kBET test metric is 30573817, and overcorrection-aware evaluation is 40158033. Only one integration benchmark is cancer-specific (33402734, bulk multi-omics). **Tumour-specific integration, where malignant cells are patient-specific and batch and biology are confounded, has no dedicated benchmark in the catalogue.**

## 4. Cell-type annotation & label transfer (n = 17, 3 cancer-specific)

- **What.** Supervised classifiers and reference mapping (31500660, 31675098, 33359678, 39120646), scATAC annotation (36131234, 36583014), spatial annotation (39833693, 42395478, 42694281), LLM-based annotation (38528186, 41396814), out-of-distribution detection (40439669) and cancer datasets (36585784, 41913233).
- **Ground truth.** Almost exclusively author or expert labels (9/17). One benchmark uses experimentally (FACS-) labelled immune subtypes (39120646).
- **Consensus.** General-purpose SVM is a robust baseline (31500660, 36585784, 36131234). SingleR performs best on Xenium (39833693). Cancer-cell labels are the least reliable class.
- **Never assessed.** Calibration of label confidence and "unknown" rejection is assessed only in 40439669 (OOD detection, non-cancer). Circularity, where labels derive from the same markers used by the tools, is not examined in any of the 17 abstracts.

## 5. Cell–cell communication (n = 6, 0 cancer-specific)

- **What.** Ligand–receptor inference methods and resources (35680885, 35822343, 37169965, 37827697), spatial validation (36253792) and spatial crosstalk tools (41952215).
- **Ground truth.** No direct truth exists. Proxies are spatial co-localisation, cytokine activity and receptor protein (35680885), spatial distance (36253792), and simulation (41952215). Agreement between methods serves as a consensus proxy.
- **Consensus.** Resource choice changes predictions as much as method choice (35680885). Using ≥2 methods is recommended (36253792).
- **Never assessed.** Any perturbation-validated truth, calibration of interaction scores, or tumour-microenvironment-specific evaluation. Zero cancer-specific benchmarks exist in this class.

## 6. Spatial transcriptomics — deconvolution, domains, SVG, alignment, platforms (n = 36, 6 cancer-specific)

- **What.** Spot deconvolution (35577954, 36941264, 38787371, 36515467, 35753702, 41648323), domain/clustering (36410733, 38491270, 41472857, 40240000, 39123269, 40966657, 42421749), SVG detection (37723583, 38076922, 38225676, 40968359, 40139667, 42041225), alignment/multi-slice (41933187, 41024097) and platform comparisons in tumours (41006245, 41107232, 40542418, 41795633, 41266321).
- **Ground truth.** Mainly simulation (19/36). Orthogonal assays appear in 8, e.g. matched imaging platforms and smFISH (35577954, 41107232, 41006245).
- **Consensus.** For deconvolution, cell2location and RCTD are repeatedly top (35577954, 38787371), with CARD and Tangram also strong (36941264). A simple regression baseline beats almost half of the dedicated methods (38787371). For SVG detection, SPARK-X performs well and Moran's I is a strong baseline (40968359, 38076922). No domain-detection method wins across platforms (40240000, 41472857).
- **Metric validity.** Spatial ARI (41001748) and benchmark pitfalls in clustering (42637979) are now being questioned. p-value calibration is assessed for SVG (40968359) and type-I error for co-localisation (40051984, cancer).
- **Never assessed.** Tumour-specific deconvolution with malignant-state references (only 41648323 is cancer-specific). Uncertainty of spot proportions is also absent.

## 7. GRN / regulon inference (n = 13, 0 cancer-specific)

- **What.** BEELINE-type algorithm benchmarks (31907445, 36626328, 37215029, 29914350, 33828580, 38627250), perturbation-based network inference (40069299), TF-activity inference (42752548) and association measures (30962620).
- **Ground truth.** Simulation (8/13), curated networks and ChIP (4) and Perturb-seq (40069299, 42752548).
- **Consensus.** Performance is modest overall. Methods often fail to beat random guessing on experimental data (37215029, 29914350). Prior-knowledge methods (Inferelator, MERLIN) win when priors are available (36626328). Interventional methods do not beat observational ones on real data (40069299).
- **Metric validity.** Partial-label metric ceilings (42379339) are the only metric-validity work in the class.
- **Never assessed.** Cancer GRNs and the reproducibility of regulons across patients.

## 8. Lineage tracing / mtDNA / somatic-variant clone calling (n = 3) — the thinnest class

- **What.** CRISPR lineage reconstruction in a DREAM challenge (34146472), recorder comparison by simulation (42215861) and variant calling on 10x libraries against matched WGS (39147582, cancer).
- **Gap.** **No benchmark of mtDNA variant-based clone callers (e.g. MQuad, mgatk-based pipelines, MAESTER workflows) was found in PubMed.** Lineage-tree reconstruction tools are compared only inside method papers (excluded). This is a strong candidate for a resource contribution.

## 9. Clonal phylogeny / scDNA (n = 17, 7 cancer-specific)

- **What.** Mostly experimental single-cell WGA kit and protocol comparisons from 2006–2021 (25136831, 26091148, 26251698, 28207771, 34433869). Computational benchmarks cover scDNA CNA detection (32658894), ploidy estimation (40916931), subclonal deconvolution of bulk tumours (34737285), purity/clonality estimation (24562872) and simulators for subclonal reconstruction (38410652).
- **Ground truth.** Orthogonal bulk WGS or known cell lines in 8. Simulation appears in 5.
- **Never assessed.** **No benchmark of single-cell phylogeny inference tools (SCITE, SiFit, SPhyR, etc.) on a shared truth was found.** Uncertainty of inferred trees and robustness to doublets/ADO are not benchmarked independently.

## 10. Differential expression & differential abundance (n = 12, 0 cancer-specific)

- **What.** scRNA-seq DE methods (29481549, 28588607, 27373736, 36993457, 35743881), pseudoreplication and multi-subject designs (34584091, 33531494, 35880426), batch handling in DE (32322368, 36944632), marker selection (38409056) and DA methods (38172966).
- **Ground truth.** Simulation (6), and matched bulk of purified populations (34584091).
- **Consensus.** This is the most consistent recommendation in the catalogue. Pseudobulk or mixed models that account for biological replicates control false discoveries, while cell-level tests inflate them (34584091, 33531494, 35880426). Known batch should be modelled as a covariate, not pre-corrected (32322368).
- **Calibration.** DE is the class where calibration/FDR control is most often assessed (4/12).
- **Never assessed.** Cancer-specific DE/DA, where patient-specific malignant states break the "shared cell type across conditions" assumption.

## 11. Doublets, demultiplexing & ambient RNA (n = 13, 0 cancer-specific)

- **What.** Doublet detection (33338399, 34382023, 41675246, 38925122), genetic and hashtag demultiplexing (37197983, 37829177, 39387404, 40702707, 39975005) and ambient-RNA removal (37337297, 42688285, 42844284).
- **Ground truth.** This is the best-grounded class: genotype multiplexing, cross-species pooling or synthetic barcodes in 10/13.
- **Consensus.** DoubletFinder gives the best accuracy and cxds the best speed (33338399). CellBender estimates background best (37337297); CellBender, DecontX and SoupX are generally good (42688285). Hyperparameter tuning matters (41675246).
- **Never assessed.** Tumour samples, which carry high ambient load from necrotic tissue and aneuploid doublets that confound CNV calling.

## 12. Trajectory inference & RNA velocity (n = 8, 0 cancer-specific)

- **What.** TI methods (30936559: 45 methods, 110 real + 229 synthetic datasets), potency measures (30289442) and RNA velocity (41509202, 41916302, 42509564, 42224352, 42126634).
- **Consensus.** TI method choice depends on topology (30936559). No velocity method is uniformly best, and rankings vary by metric (41509202, 41916302).
- **Never assessed.** Calibration of pseudotime/velocity uncertainty, and any cancer evolution or plasticity truth (e.g. lineage-barcoded tumours).

## 13. Perturbation-response prediction (n = 11, all 2025–2026)

- **What.** Deep-learning and foundation-model predictors versus simple baselines (40759747, 40269681, 40407144, 41250104, 41381899, 42715312, 42121287, 42860076).
- **Ground truth.** Held-out Perturb-seq or drug-screen measurements (10/11).
- **Consensus.** This is the strongest consensus in the catalogue. Simple linear or mean baselines match or beat deep models and foundation models (40759747, 40269681, 40407144, 41250104).
- **Metric validity.** Most active here (4/11). R² hides DE failures (40161693). Control-reuse inflates correlation metrics (42182243). Scores can diverge from biological signatures (42121287), and rankings depend on the evaluation perspective (42715312).
- **Never assessed.** Cancer-cell-line or patient-derived perturbation contexts as a distinct stratum. Calibrated predictive uncertainty is also missing.

## 14. Single-cell foundation models (n = 14, 2 cancer-specific)

- **What.** Zero-shot and fine-tuned evaluation of scGPT, Geneformer, scFoundation, UCE and others (40251685, 41869863, 41044630, 40843339, 41542465, 41727141), pretraining scale (42265208, 42531328), interpretability (42482180) and cancer outcomes (41279698).
- **Ground truth.** Expert labels or none stated (11/14 unclear).
- **Consensus.** FMs do not consistently beat task-specific or parameter-free baselines (40251685, 41869863, 41727141, 41044630). They show limited advantage for predicting cancer patient outcomes (41279698).
- **Never assessed.** Calibration, data leakage between pretraining corpora and test sets (not stated in any abstract), and tumour-specific tasks beyond annotation.

## 15. Drug-response prediction (n = 3, 2 cancer-specific)

- **What.** FM-based single-cell drug-response benchmarks (41381537: 8 FMs + 2 LLMs, 60 datasets), FM embeddings for drug response (42322669) and transfer learning from cell lines to single cells (41359728).
- **Gap.** **Only 3 benchmarks exist.** There is no shared single-cell drug-response truth set with measured per-cell or per-clone response.

## 16. Other preprocessing / platform benchmarks (n = 55)

- **What.** Normalization, imputation, clustering, HVG/feature selection, alignment, pipelines (pipeComp 32873325; mixture-control pipelines 31133762; 31604912), simulation fidelity (36991470), protocols/platforms (32518403, 32341560, 33349700, 38689972) and cancer state discovery (41231245, CanSig).
- **Notes.** Cancer-relevant items include normalization in cancer studies (42070330: 465 pipelines), FFPE vs fresh vs frozen ccRCC (41394662), controlled-heterogeneity cancer benchmark data (38307867) and clustering on tumours (36420149). Simulation fidelity is a cross-cutting threat: simulators inflate integration performance and destabilize clustering rankings (36991470).

---

## What has never (or almost never) been assessed — cross-class summary

1. **Calibration of uncertainty** outside DE and SVG p-values. This includes per-cell malignancy probabilities, deconvolution proportions, annotation confidence, perturbation predictions and phylogenies.
2. **Metric validity in cancer settings.** 0 of 48 cancer-specific benchmarks examine it. Metric critiques exist only for integration (40739072), spatial clustering (41001748, 42637979), GRN (42379339) and perturbation (40161693, 42182243).
3. **Tumour-specific benchmarks for integration, CCC, GRN, DE/DA, trajectory and doublets/ambient RNA.** There are 0–1 cancer-specific records in each of these classes.
4. **mtDNA clone calling and single-cell phylogeny inference.** No dedicated computational benchmark was found in PubMed.
5. **Shared, matched multi-modal ground truth.** Matched scDNA + scRNA + spatial data from the same tumour, usable across CNV, clone, deconvolution and spatial classes, does not exist. Each benchmark builds its own truth, and 39.8% of abstracts do not state the ground truth at all.

## Caveats

- Evaluation fields come from abstracts with keyword rules plus manual checks of 40 records. Full texts were not read, so all assessment counts are lower bounds and provisional.
- Searches were relevance-ranked and capped per query, so the catalogue is broad but not exhaustive. Preprint-only benchmarks absent from PubMed (some foundation-model and perturbation benchmarks on bioRxiv/arXiv) are missing unless PubMed indexes them.
- The `n_tools_compared` field holds the number stated in the abstract (rule-extracted; 'unclear' when none is stated). `tools` lists only names recognised from a dictionary of ~300 tools and is incomplete.
