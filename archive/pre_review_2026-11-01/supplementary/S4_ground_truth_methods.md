# Ground-truth dataset catalogue: methods

Data pull: GEO via NCBI E-utilities (db=gds, entry type GSE) and GEO series SOFT text (acc.cgi, targ=self, view=brief), retrieved 15 October 2026. Output: the ground-truth catalogue CSV (ground_truth_catalogue.csv).

## 1. Retrieval queries

A base query defined human tumour single-cell series. Each validation modality then added one clause. For cell-line mixtures and Perturb-seq, the cancer clause was widened with `K562 OR "cancer cell line(s)" OR "cell lines"`. All terms were `[All Fields]`, which in GEO also covers sample-level characteristics and protocols.

| Query | GEO hits |
|---|---|
| BASE (all human tumour single-cell GSE) | 6142 |
| matched_WES_WGS | 198 |
| CITE_seq_ADT | 308 |
| genotype_multiplexed | 538 |
| paired_bulk_RNA | 511 |
| paired_spatial | 486 |
| mtDNA_lineage | 48 |
| longitudinal_treatment | 1172 |
| cell_line_mixture | 51 |
| perturb_seq | 161 |

Union of the modality queries: 2715 unique records. All were retrieved in full; none was capped (the largest set was 1,172 against retmax=5000).

<details><summary>Exact query strings</summary>

**BASE (all human tumour single-cell GSE)**
```
("single cell"[All Fields] OR "single-cell"[All Fields] OR scRNA-seq[All Fields] OR snRNA-seq[All Fields] OR "single nucleus"[All Fields] OR scATAC-seq[All Fields] OR "10x Genomics"[All Fields]) AND (cancer[All Fields] OR tumor[All Fields] OR tumour[All Fields] OR carcinoma[All Fields] OR leukemia[All Fields] OR leukaemia[All Fields] OR lymphoma[All Fields] OR myeloma[All Fields] OR melanoma[All Fields] OR glioma[All Fields] OR glioblastoma[All Fields] OR sarcoma[All Fields] OR neuroblastoma[All Fields] OR malignant[All Fields] OR neoplasm[All Fields] OR adenocarcinoma[All Fields] OR metastasis[All Fields] OR metastatic[All Fields]) AND "Homo sapiens"[Organism] AND gse[Entry Type]
```
**matched_WES_WGS**
```
("single cell"[All Fields] OR "single-cell"[All Fields] OR scRNA-seq[All Fields] OR snRNA-seq[All Fields] OR "single nucleus"[All Fields] OR scATAC-seq[All Fields] OR "10x Genomics"[All Fields]) AND (cancer[All Fields] OR tumor[All Fields] OR tumour[All Fields] OR carcinoma[All Fields] OR leukemia[All Fields] OR leukaemia[All Fields] OR lymphoma[All Fields] OR myeloma[All Fields] OR melanoma[All Fields] OR glioma[All Fields] OR glioblastoma[All Fields] OR sarcoma[All Fields] OR neuroblastoma[All Fields] OR malignant[All Fields] OR neoplasm[All Fields] OR adenocarcinoma[All Fields] OR metastasis[All Fields] OR metastatic[All Fields]) AND "Homo sapiens"[Organism] AND gse[Entry Type] AND (exome[All Fields] OR "whole genome sequencing"[All Fields] OR "whole-genome sequencing"[All Fields] OR WES[All Fields] OR WGS[All Fields] OR "targeted DNA sequencing"[All Fields])
```
**CITE_seq_ADT**
```
("single cell"[All Fields] OR "single-cell"[All Fields] OR scRNA-seq[All Fields] OR snRNA-seq[All Fields] OR "single nucleus"[All Fields] OR scATAC-seq[All Fields] OR "10x Genomics"[All Fields]) AND (cancer[All Fields] OR tumor[All Fields] OR tumour[All Fields] OR carcinoma[All Fields] OR leukemia[All Fields] OR leukaemia[All Fields] OR lymphoma[All Fields] OR myeloma[All Fields] OR melanoma[All Fields] OR glioma[All Fields] OR glioblastoma[All Fields] OR sarcoma[All Fields] OR neuroblastoma[All Fields] OR malignant[All Fields] OR neoplasm[All Fields] OR adenocarcinoma[All Fields] OR metastasis[All Fields] OR metastatic[All Fields]) AND "Homo sapiens"[Organism] AND gse[Entry Type] AND (CITE-seq[All Fields] OR "antibody-derived tag"[All Fields] OR ADT[All Fields] OR TotalSeq[All Fields] OR "surface protein"[All Fields] OR REAP-seq[All Fields] OR "feature barcoding"[All Fields])
```
**genotype_multiplexed**
```
("single cell"[All Fields] OR "single-cell"[All Fields] OR scRNA-seq[All Fields] OR snRNA-seq[All Fields] OR "single nucleus"[All Fields] OR scATAC-seq[All Fields] OR "10x Genomics"[All Fields]) AND (cancer[All Fields] OR tumor[All Fields] OR tumour[All Fields] OR carcinoma[All Fields] OR leukemia[All Fields] OR leukaemia[All Fields] OR lymphoma[All Fields] OR myeloma[All Fields] OR melanoma[All Fields] OR glioma[All Fields] OR glioblastoma[All Fields] OR sarcoma[All Fields] OR neuroblastoma[All Fields] OR malignant[All Fields] OR neoplasm[All Fields] OR adenocarcinoma[All Fields] OR metastasis[All Fields] OR metastatic[All Fields]) AND "Homo sapiens"[Organism] AND gse[Entry Type] AND (demuxlet[All Fields] OR souporcell[All Fields] OR vireo[All Fields] OR "genetic demultiplexing"[All Fields] OR demultiplexed[All Fields] OR "natural genetic variation"[All Fields] OR "cell hashing"[All Fields] OR hashtag[All Fields] OR MULTI-seq[All Fields] OR pooled[All Fields])
```
**paired_bulk_RNA**
```
("single cell"[All Fields] OR "single-cell"[All Fields] OR scRNA-seq[All Fields] OR snRNA-seq[All Fields] OR "single nucleus"[All Fields] OR scATAC-seq[All Fields] OR "10x Genomics"[All Fields]) AND (cancer[All Fields] OR tumor[All Fields] OR tumour[All Fields] OR carcinoma[All Fields] OR leukemia[All Fields] OR leukaemia[All Fields] OR lymphoma[All Fields] OR myeloma[All Fields] OR melanoma[All Fields] OR glioma[All Fields] OR glioblastoma[All Fields] OR sarcoma[All Fields] OR neuroblastoma[All Fields] OR malignant[All Fields] OR neoplasm[All Fields] OR adenocarcinoma[All Fields] OR metastasis[All Fields] OR metastatic[All Fields]) AND "Homo sapiens"[Organism] AND gse[Entry Type] AND ("bulk RNA-seq"[All Fields] OR "bulk RNA sequencing"[All Fields] OR "bulk RNA"[All Fields] OR "bulk transcriptom*"[All Fields] OR "bulk sequencing"[All Fields])
```
**paired_spatial**
```
("single cell"[All Fields] OR "single-cell"[All Fields] OR scRNA-seq[All Fields] OR snRNA-seq[All Fields] OR "single nucleus"[All Fields] OR scATAC-seq[All Fields] OR "10x Genomics"[All Fields]) AND (cancer[All Fields] OR tumor[All Fields] OR tumour[All Fields] OR carcinoma[All Fields] OR leukemia[All Fields] OR leukaemia[All Fields] OR lymphoma[All Fields] OR myeloma[All Fields] OR melanoma[All Fields] OR glioma[All Fields] OR glioblastoma[All Fields] OR sarcoma[All Fields] OR neuroblastoma[All Fields] OR malignant[All Fields] OR neoplasm[All Fields] OR adenocarcinoma[All Fields] OR metastasis[All Fields] OR metastatic[All Fields]) AND "Homo sapiens"[Organism] AND gse[Entry Type] AND (Visium[All Fields] OR "spatial transcriptomics"[All Fields] OR "spatial transcriptome"[All Fields] OR Xenium[All Fields] OR CosMx[All Fields] OR MERFISH[All Fields] OR Slide-seq[All Fields] OR "Stereo-seq"[All Fields] OR "spatial RNA"[All Fields] OR GeoMx[All Fields])
```
**mtDNA_lineage**
```
("single cell"[All Fields] OR "single-cell"[All Fields] OR scRNA-seq[All Fields] OR snRNA-seq[All Fields] OR "single nucleus"[All Fields] OR scATAC-seq[All Fields] OR "10x Genomics"[All Fields]) AND (cancer[All Fields] OR tumor[All Fields] OR tumour[All Fields] OR carcinoma[All Fields] OR leukemia[All Fields] OR leukaemia[All Fields] OR lymphoma[All Fields] OR myeloma[All Fields] OR melanoma[All Fields] OR glioma[All Fields] OR glioblastoma[All Fields] OR sarcoma[All Fields] OR neuroblastoma[All Fields] OR malignant[All Fields] OR neoplasm[All Fields] OR adenocarcinoma[All Fields] OR metastasis[All Fields] OR metastatic[All Fields]) AND "Homo sapiens"[Organism] AND gse[Entry Type] AND (mtscATAC-seq[All Fields] OR MAESTER[All Fields] OR mtDNA[All Fields] OR "mitochondrial DNA"[All Fields] OR "mitochondrial mutations"[All Fields] OR "mitochondrial variants"[All Fields] OR ASAP-seq[All Fields] OR DOGMA-seq[All Fields])
```
**longitudinal_treatment**
```
("single cell"[All Fields] OR "single-cell"[All Fields] OR scRNA-seq[All Fields] OR snRNA-seq[All Fields] OR "single nucleus"[All Fields] OR scATAC-seq[All Fields] OR "10x Genomics"[All Fields]) AND (cancer[All Fields] OR tumor[All Fields] OR tumour[All Fields] OR carcinoma[All Fields] OR leukemia[All Fields] OR leukaemia[All Fields] OR lymphoma[All Fields] OR myeloma[All Fields] OR melanoma[All Fields] OR glioma[All Fields] OR glioblastoma[All Fields] OR sarcoma[All Fields] OR neuroblastoma[All Fields] OR malignant[All Fields] OR neoplasm[All Fields] OR adenocarcinoma[All Fields] OR metastasis[All Fields] OR metastatic[All Fields]) AND "Homo sapiens"[Organism] AND gse[Entry Type] AND (longitudinal[All Fields] OR on-treatment[All Fields] OR "on treatment"[All Fields] OR pre-treatment[All Fields] OR post-treatment[All Fields] OR "before and after"[All Fields] OR "serial biopsies"[All Fields] OR relapse[All Fields] OR "treatment-naive"[All Fields] OR neoadjuvant[All Fields])
```
**cell_line_mixture**
```
("single cell"[All Fields] OR "single-cell"[All Fields] OR scRNA-seq[All Fields] OR snRNA-seq[All Fields] OR "single nucleus"[All Fields] OR scATAC-seq[All Fields] OR "10x Genomics"[All Fields]) AND ((cancer[All Fields] OR tumor[All Fields] OR tumour[All Fields] OR carcinoma[All Fields] OR leukemia[All Fields] OR leukaemia[All Fields] OR lymphoma[All Fields] OR myeloma[All Fields] OR melanoma[All Fields] OR glioma[All Fields] OR glioblastoma[All Fields] OR sarcoma[All Fields] OR neuroblastoma[All Fields] OR malignant[All Fields] OR neoplasm[All Fields] OR adenocarcinoma[All Fields] OR metastasis[All Fields] OR metastatic[All Fields]) OR (K562[All Fields] OR "cancer cell line"[All Fields] OR "cancer cell lines"[All Fields] OR "cell lines"[All Fields])) AND "Homo sapiens"[Organism] AND gse[Entry Type] AND ("cell line mixture"[All Fields] OR "mixture of cell lines"[All Fields] OR "mixed cell lines"[All Fields] OR "cell lines were mixed"[All Fields] OR "pooled cell lines"[All Fields] OR MIX-seq[All Fields] OR "species-mixing"[All Fields] OR "species mixing"[All Fields] OR "mixture experiment"[All Fields] OR CellBench[All Fields])
```
**perturb_seq**
```
("single cell"[All Fields] OR "single-cell"[All Fields] OR scRNA-seq[All Fields] OR snRNA-seq[All Fields] OR "single nucleus"[All Fields] OR scATAC-seq[All Fields] OR "10x Genomics"[All Fields]) AND ((cancer[All Fields] OR tumor[All Fields] OR tumour[All Fields] OR carcinoma[All Fields] OR leukemia[All Fields] OR leukaemia[All Fields] OR lymphoma[All Fields] OR myeloma[All Fields] OR melanoma[All Fields] OR glioma[All Fields] OR glioblastoma[All Fields] OR sarcoma[All Fields] OR neuroblastoma[All Fields] OR malignant[All Fields] OR neoplasm[All Fields] OR adenocarcinoma[All Fields] OR metastasis[All Fields] OR metastatic[All Fields]) OR (K562[All Fields] OR "cancer cell line"[All Fields] OR "cancer cell lines"[All Fields] OR "cell lines"[All Fields])) AND "Homo sapiens"[Organism] AND gse[Entry Type] AND (Perturb-seq[All Fields] OR CROP-seq[All Fields] OR ECCITE-seq[All Fields] OR "CRISPR screen"[All Fields] OR "CRISPR screens"[All Fields] OR "pooled CRISPR"[All Fields] OR "single-cell CRISPR"[All Fields] OR Perturb-CITE-seq[All Fields])
```
</details>

## 2. Eligibility filters (applied to esummary plus SOFT text)

1. `gdstype` contains 'sequencing'. This drops microarray-only series.
2. Taxon includes *Homo sapiens*.
3. Single-cell regex matched in title, summary, overall design or sample titles.
4. Cancer regex matched (cancer terms, haematological malignancy acronyms, K562/HeLa).
5. At least one modality rule fired (Section 3).

Single-cell regex: `single[- ]?cell|single[- ]nucle|scRNA|snRNA|scATAC|snATAC|10x|chromium|drop-?seq|smart-?seq|CITE-seq|scDNA|Perturb-seq|CROP-seq|MAESTER|mtscATAC|ASAP-seq|DOGMA|multiome|BD Rhapsody|seq-?well|sci-RNA`

Cancer regex: `cancer|tumou?r|carcinoma|leuka?emi|lymphoma|myeloma|melanoma|gliom|glioblastoma|sarcoma|blastoma|malignan|neoplas|metasta|adenocarcinoma|myelodysplas|\bMDS\b|myeloproliferative|K562|HeLa|mesothelioma|seminoma|\bCLL\b|\bAML\b|\bB-ALL\b|\bT-ALL\b|\bHCC\b|\bNSCLC\b|\bccRCC\b|\bPDAC\b`

Eligible after filters 1-4: 2024. In the catalogue (filter 5 also satisfied): 1336 series in 1166 study groups. A study group is a SuperSeries together with its SubSeries.

## 3. Modality rules (regex over title + summary + overall_design + sample titles)

A modality call means the record states that the study generated that data type. It does **not** prove that the data are deposited in GEO: WES/WGS is often held in dbGaP/EGA under controlled access, and companion data often sit in a sibling SubSeries. Every call stores the matched text window in the `evidence` column so it can be audited.

| Modality | Regex (case-insensitive) | Exclusions |
|---|---|---|
| matched_WES_WGS | `whole[- ]exome \| \bexomes?\b \| \bWES\b \| whole[- ]genome (sequencing \| seq) \| \bWGS\b \| targeted (DNA  \| panel )?sequencing \| scDNA-seq \| single[- ]cell DNA \| DNA-seq \| copy[- ]number (profiling \| sequencing) of (bulk \| DNA) \| shallow WGS \| low[- ]pass WGS` | single match in a 'TCGA/public/previously published' context |
| CITE_seq_ADT | `CITE-?seq \| antibody[- ]derived tags? \| \bADTs?\b \| TotalSeq \| REAP-seq \| ECCITE \| surface protein \| oligo(nucleotide)?[- ]conjugated antibod \| barcoded antibod \| DOGMA-seq \| ASAP-seq \| TEA-seq \| AbSeq \| feature barcod` | TotalSeq/hashtag antibodies used only for hashing (counted as genotype_multiplexed instead) |
| genotype_multiplexed | `demuxlet \| freemuxlet \| souporcell \| vireo \| scSplit \| genetic(ally)? demultiplex \| genotype[- ](based )?demultiplex \| demultiplex\w* (by \| using \| based on \| with) (genotype \| SNP \| single nucleotide \| natural genetic \| germline) \| natural genetic variation \| cell hashing \| hashtag \| \bHTOs?\b \| MULTI-seq \| lipid[- ]tag \| CellPlex \| \bCMOs?\b \| cell multiplexing oligo \| sample multiplex \| multiplexed (samples \| donors \| patients \| cell lines) \| (samples \| donors \| patients \| cell lines) were (multiplexed \| pooled) \| pooled (samples \| donors \| patients \| cell lines)` |  |
| paired_bulk_RNA | `bulk RNA \| bulk transcriptom \| bulk[- ]seq \| bulk sequencing \| bulk tumou?r (RNA \| expression \| transcript) \| matched bulk \| bulk (and \| vs\.? \| versus) single[- ]cell \| bulk profil` | single match co-occurring with TCGA/TARGET/GTEx/ICGC/CPTAC/'public' bulk |
| paired_spatial | `Visium \| spatial(ly resolved)? transcriptom \| Xenium \| CosMx \| MERFISH \| Slide-?seq \| Stereo-?seq \| GeoMx \| spatial RNA \| spatial gene expression \| seqFISH \| spatial (multi-?)?omic \| spatial profil \| DBiT \| STARmap \| HDST \| spatial transcript` |  |
| mtDNA_lineage | `mtscATAC \| MAESTER \| ReDeeM \| mito(chondrial)?[- ]?(DNA )?(somatic )?(mutation \| variant)s? .{0,60}(lineage \| clon \| tracing \| tree) \| (lineage \| clon\w*) .{0,60}mito(chondrial)? ?(DNA )?(mutation \| variant) \| mtDNA (mutation \| variant)s? .{0,60}(lineage \| clon \| tracing) \| (lineage \| clon\w*) .{0,60}mtDNA (mutation \| variant) \| heteroplasm.{0,60}(lineage \| clon) \| mitochondrial (DNA )?genotyp` |  |
| longitudinal_treatment | `longitudinal \| on[- ]treatment \| pre-? ?(and \| / \| vs\.? \| versus) ?post-?[- ]?(treatment \| therapy) \| post-?treatment (samples \| biops \| tumou?rs?) \| (paired \| matched) pre- \| pre- and post \| pre- and on \| pre-? and on-?treatment \| before and after (treatment \| therapy \| \w+ (treatment \| therapy)) \| serial(ly)? (biops \| samples \| sampl \| collected) \| baseline and (on \| post) \| at diagnosis and (at )?relapse \| diagnosis (and \| to) relapse \| paired (primary and )?relapse \| matched relapse \| (multiple \| several \| \d+) time ?points \| across .{0,30}timepoints \| treatment timepoints \| (during \| after) (treatment \| therapy) with` |  |
| cell_line_mixture | `cell[- ]line mixture \| mixture of (\w+ )?(cancer )?cell lines \| mixed (cancer )?cell lines \| cell lines were (mixed \| pooled) \| pool(ed \| ing)? (of )?(\d+  \| several  \| multiple  \| many  \| \w+ )?(cancer )?cell lines \| MIX-seq \| species[- ]mix \| CellBench \| mixture (control )?experiment \| barnyard \| known (proportion \| mixture)` |  |
| perturb_seq | `Perturb-?seq \| CROP-?seq \| ECCITE-?seq \| Perturb-CITE \| Perturb-ATAC \| Spear-ATAC \| single[- ]cell CRISPR \| CRISPR[^.]{0,80}(single[- ]cell \| scRNA \| 10x) \| (single[- ]cell \| scRNA)[^.]{0,80}CRISPR (screen \| perturbation) \| Mosaic-seq \| TAP-seq \| CRISPR droplet sequencing \| sgRNA[^.]{0,40}(capture \| single[- ]cell)` |  |

`genotype_multiplexed` covers both genotype-based demultiplexing (demuxlet, souporcell, vireo, freemuxlet) and hashtag/lipid/CMO sample multiplexing. Both give a cell-to-sample label that is independent of the transcriptome.

## 4. Derived fields

- **cancer_type**: an ordered dictionary of 37 cancer-type regexes, keeping at most 3 labels. 'pan-cancer/multiple' is assigned when the text says pan-cancer or multiple tumour types; 'unspecified' when nothing matched.
- **sample_source**: patient tumour vs cancer cell line/model (cell line, organoid, PDX, xenograft), from keyword rules.
- **benchmark_tasks** (mapping from modality to task):
  - `malignant_calling` ← matched_WES_WGS, cell_line_mixture
  - `clone_calling` ← matched_WES_WGS, mtDNA_lineage
  - `deconvolution` ← paired_bulk_RNA, paired_spatial, cell_line_mixture
  - `annotation_calibration` ← CITE_seq_ADT, genotype_multiplexed, cell_line_mixture
  - `CCC_spatial_referee` ← paired_spatial
  - `pipeline_robustness` ← genotype_multiplexed, cell_line_mixture, longitudinal_treatment, perturb_seq, paired_bulk_RNA
  - `perturbation_response` ← perturb_seq, longitudinal_treatment
- **study_group**: the parent SuperSeries accession (from `!Series_relation = SubSeries of:`), otherwise the series' own accession. Use it to deduplicate at study level.

## 5. Precision audit

We hand-checked seeded random samples (8 per modality in round 1; 10 for the four revised modalities in round 2), asking whether the record states that the modality was generated in the study. Rules were tightened after each round.

| Modality | Audit result |
|---|---|
| matched_WES_WGS | 8/8 |
| CITE_seq_ADT | 7/8 (the one miss was TotalSeq hashtags; rule then tightened to exclude hashtag-only TotalSeq) |
| genotype_multiplexed | 8/8 |
| paired_bulk_RNA | 6/8 in round 1 (public TARGET/TCGA bulk); 9/10 after excluding public-bulk mentions |
| paired_spatial | 8/8 |
| mtDNA_lineage | 4/8 in round 1; 10/10 after requiring mtDNA variant + lineage/clone context or a named assay |
| longitudinal_treatment | 6/8 in round 1; 7/10 in round 2; then tightened once more (bare 'pre-treatment' and 'acquired resistance' dropped), and that final rule was not re-audited |
| cell_line_mixture | 7/8 (PDX human-mouse filtering miss; that pattern removed) |
| perturb_seq | 4/8 in round 1 (non-single-cell CRISPR screens); 10/10 after requiring a single-cell readout |

These are small-sample spot checks, so the precision figures are **provisional**. Recall was not measured. Because the rules read only series-level text (sample characteristics were not parsed), recall is lower than the GEO index counts in Section 1.

## 6. Counts

| Modality | Series | Study groups |
|---|---|---|
| matched_WES_WGS | 138 | 117 |
| CITE_seq_ADT | 227 | 216 |
| genotype_multiplexed | 166 | 152 |
| paired_bulk_RNA | 459 | 402 |
| paired_spatial | 250 | 218 |
| mtDNA_lineage | 18 | 9 |
| longitudinal_treatment | 297 | 266 |
| cell_line_mixture | 25 | 20 |
| perturb_seq | 89 | 77 |

| Benchmark task | Series |
|---|---|
| malignant_calling | 162 |
| clone_calling | 153 |
| deconvolution | 698 |
| annotation_calibration | 356 |
| CCC_spatial_referee | 250 |
| pipeline_robustness | 918 |
| perturbation_response | 381 |

Modalities per series: 1: 1049, 2: 245, 3: 38, 4: 4.

Sample source: patient tumour: 630, unspecified: 259, patient tumour + model: 245, cancer cell line/model: 202.

| Cancer type (multi-label) | Series |
|---|---|
| unspecified | 166 |
| lung cancer | 140 |
| breast cancer | 119 |
| glioma/glioblastoma | 113 |
| colorectal cancer | 94 |
| acute myeloid leukaemia | 88 |
| myelodysplastic/myeloproliferative | 79 |
| melanoma | 74 |
| renal cell carcinoma | 60 |
| lymphoma | 60 |
| hepatocellular/liver cancer | 51 |
| pancreatic cancer | 51 |
| acute lymphoblastic leukaemia | 47 |
| chronic myeloid leukaemia | 46 |
| multiple myeloma | 45 |
| sarcoma | 39 |
| leukaemia (other/unspecified) | 36 |
| prostate cancer | 35 |
| head and neck cancer | 34 |
| ovarian cancer | 33 |
| neuroblastoma | 27 |
| chronic lymphocytic leukaemia | 23 |
| pan-cancer/multiple | 20 |
| bladder/urothelial cancer | 18 |
| brain metastasis | 16 |
| skin (non-melanoma) | 15 |
| cervical cancer | 14 |
| adrenal/neuroendocrine | 13 |
| gastric cancer | 13 |
| oesophageal cancer | 12 |
| endometrial/uterine cancer | 9 |
| thyroid cancer | 8 |
| uveal melanoma | 8 |
| medulloblastoma | 7 |
| nasopharyngeal | 6 |
| germ cell tumour | 5 |
| retinoblastoma | 4 |
| mesothelioma | 4 |

Year range: 2015-2026. Median samples per series: 14.

## 7. Deviations and limitations

- An LLM adjudication pass over series summaries was planned but not run: the per-session LLM token ceiling was reached. Classification is regex-only and audited by hand (Section 5).
- Sample-level metadata (characteristics, library strategy) was not parsed, only series-level text plus sample titles.
- Only GEO was searched. ArrayExpress/BioStudies, CELLxGENE and HTAN were not.
- The mtDNA count (18 series) is much lower than the earlier audit's 79 GEO query hits. That earlier figure counted any mention of mtDNA or mitochondrial DNA; this catalogue requires lineage or clonal context.
- The counts differ from the gap review's 4 October GEO probes (e.g. WES 158 vs 138 here) because the queries and filters differ.
