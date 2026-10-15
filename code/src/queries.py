"""PubMed query definitions used in the study.

SUBFIELD reproduces the archived subfield totals for 2015-2025 within +/-0.7%
(Methods 2.7). TOPICS holds, for each of the 26 topics, the candidate query whose
counts best matched the archived topic counts (lowest mean |log ratio| over
2017, 2021 and 2025); calibration errors are in TOPIC_CALIBRATION. Every topic
query is combined with SUBFIELD by AND.
"""

SUBFIELD = '("single-cell"[tiab] OR "single cell"[tiab] OR scRNA-seq[tiab] OR snRNA-seq[tiab]) AND (cancer[tiab] OR tumor[tiab] OR tumour[tiab] OR carcinoma[tiab] OR leukemia[tiab] OR lymphoma[tiab] OR melanoma[tiab] OR glioma[tiab])'

# Evaluation-titled papers (candidate benchmarks)
EVAL_TITLED = SUBFIELD + ' AND (benchmark*[ti] OR comparison[ti] OR evaluation[ti] OR assessment[ti])'

# Entrez-date cap reproducing the archived 4 October 2026 snapshot
EDAT_SNAPSHOT_2026_10_04 = ' AND ("1900/01/01"[edat] : "2026/10/04"[edat])'

# Research-article filter used for the stratified abstract sample (Methods 2.4)
NOT_REVIEW = ' NOT (review[pt] OR "systematic review"[pt] OR editorial[pt] OR comment[pt] OR erratum[pt])'

TOPICS = {
    'clinical_prognosis': '(prognos*[tiab] OR biomarker*[tiab] OR survival[tiab])',
    'tme_composition': '("microenvironment"[tiab])',
    'immunotherapy_resp': '(immunotherapy[tiab] OR "immune checkpoint"[tiab] OR "PD-1"[tiab] OR "PD-L1"[tiab] OR ICB[tiab] OR CAR-T[tiab])',
    'metastasis': '(metasta*[tiab] OR dissemination[tiab] OR invasion[tiab])',
    'tcell_exhaustion': '("T cell"[tiab] OR "T-cell"[tiab]) AND (exhaust*[tiab] OR dysfunct*[tiab] OR state*[tiab])',
    'drug_response_pred': '("drug response"[tiab] OR "drug sensitivity"[tiab] OR "drug resistance"[tiab] OR "drug prediction"[tiab])',
    'spatial_tumor': '("spatial transcriptom*"[tiab] OR "spatial omics"[tiab] OR Visium[tiab] OR "spatially resolved"[tiab])',
    'foundation_dl': '("deep learning"[tiab] OR "foundation model*"[tiab] OR "neural network*"[tiab] OR transformer[tiab] OR "machine learning"[tiab])',
    'plasticity_emt': '(plasticity[tiab] OR EMT[tiab] OR "epithelial-mesenchymal"[tiab] OR stemness[tiab] OR "cancer stem"[tiab])',
    'cell_communication': '("cell-cell communication"[tiab] OR "ligand-receptor"[tiab] OR CellChat[tiab] OR CellPhoneDB[tiab] OR "intercellular communication"[tiab])',
    'resistance_persister': '("drug resistance"[tiab] OR "therapy resistance"[tiab] OR "treatment resistance"[tiab] OR chemoresistan*[tiab] OR persister*[tiab] OR "acquired resistance"[tiab])',
    'ith_quantification': '("intratumor heterogeneity"[tiab] OR "intratumoral heterogeneity"[tiab] OR "intra-tumor heterogeneity"[tiab] OR "intratumour heterogeneity"[tiab] OR "tumor heterogeneity"[tiab] OR "tumour heterogeneity"[tiab])',
    'pancancer_atlas': '(pan-cancer[tiab] OR pancancer[tiab] OR "across cancer types"[tiab] OR "multiple cancer types"[tiab])',
    'malignant_calling': '("malignant cell*"[tiab] OR "tumor cell identification"[tiab] OR inferCNV[tiab] OR copyKAT[tiab] OR SCEVAN[tiab])',
    'cnv_scdna': '("copy number variation*"[tiab] OR "copy number alteration*"[tiab] OR "copy-number"[tiab] OR inferCNV[tiab] OR scDNA*[tiab] OR "single-cell DNA"[tiab])',
    'tcr_bcr_repertoire': '(TCR[tiab] OR BCR[tiab] OR "T cell receptor"[tiab] OR "B cell receptor"[tiab] OR clonotyp*[tiab] OR repertoire[tiab])',
    'deconvolution': '(deconvolut*[tiab] OR CIBERSORT*[tiab] OR BayesPrism[tiab] OR MuSiC[tiab])',
    'longitudinal_therapy': '(longitudinal[tiab] OR "on-treatment"[tiab] OR "serial"[tiab] OR "post-treatment"[tiab])',
    'epigenome_multiome': '(scATAC*[tiab] OR "chromatin accessibility"[tiab] OR multiome[tiab] OR "single-cell multi-omic*"[tiab] OR "single-cell multiomic*"[tiab])',
    'clonal_phylogeny': '("clonal evolution"[tiab] OR phylogen*[tiab] OR "clonal architecture"[tiab] OR "clonal dynamics"[tiab] OR "subclonal"[tiab])',
    'ctc_liquid_biopsy': '("circulating tumor cell*"[tiab] OR "circulating tumour cell*"[tiab] OR CTC*[tiab] OR "liquid biopsy"[tiab] OR "minimal residual disease"[tiab] OR MRD[tiab])',
    'perturbseq': '(Perturb-seq[tiab] OR CROP-seq[tiab] OR "single-cell CRISPR"[tiab] OR "CRISPR screen*"[tiab] OR ECCITE-seq[tiab])',
    'integration_batch': '("batch effect*"[tiab] OR "batch correction"[tiab] OR "data integration"[tiab] OR "integration method*"[tiab])',
    'benchmarking': '(benchmark*[tiab])',
    'qc_artifacts': '(doublet*[tiab] OR "ambient RNA"[tiab] OR "ambient"[tiab] OR "quality control"[tiab])',
    'lineage_barcoding': '("lineage tracing"[tiab] OR "lineage barcod*"[tiab] OR "cellular barcod*"[tiab] OR "mitochondrial DNA mutation*"[tiab] OR "mtDNA mutation*"[tiab] OR "lineage recording"[tiab])',
}

TOPIC_CALIBRATION = {
    'clinical_prognosis': {'candidate_index': 0, 'mean_abs_log_error': 0.0075},
    'tme_composition': {'candidate_index': 1, 'mean_abs_log_error': 0.1396},
    'immunotherapy_resp': {'candidate_index': 2, 'mean_abs_log_error': 0.0221},
    'metastasis': {'candidate_index': 0, 'mean_abs_log_error': 0.007},
    'tcell_exhaustion': {'candidate_index': 0, 'mean_abs_log_error': 0.8593},
    'drug_response_pred': {'candidate_index': 1, 'mean_abs_log_error': 0.245},
    'spatial_tumor': {'candidate_index': 2, 'mean_abs_log_error': 0.0921},
    'foundation_dl': {'candidate_index': 1, 'mean_abs_log_error': 0.0065},
    'plasticity_emt': {'candidate_index': 0, 'mean_abs_log_error': 0.1156},
    'cell_communication': {'candidate_index': 1, 'mean_abs_log_error': 0.2171},
    'resistance_persister': {'candidate_index': 1, 'mean_abs_log_error': 0.1209},
    'ith_quantification': {'candidate_index': 0, 'mean_abs_log_error': 0.049},
    'pancancer_atlas': {'candidate_index': 1, 'mean_abs_log_error': 0.269},
    'malignant_calling': {'candidate_index': 1, 'mean_abs_log_error': 0.0028},
    'cnv_scdna': {'candidate_index': 2, 'mean_abs_log_error': 0.0839},
    'tcr_bcr_repertoire': {'candidate_index': 0, 'mean_abs_log_error': 0.0217},
    'deconvolution': {'candidate_index': 2, 'mean_abs_log_error': 0.2215},
    'longitudinal_therapy': {'candidate_index': 1, 'mean_abs_log_error': 0.1142},
    'epigenome_multiome': {'candidate_index': 1, 'mean_abs_log_error': 0.274},
    'clonal_phylogeny': {'candidate_index': 1, 'mean_abs_log_error': 0.0137},
    'ctc_liquid_biopsy': {'candidate_index': 0, 'mean_abs_log_error': 0.0893},
    'perturbseq': {'candidate_index': 1, 'mean_abs_log_error': 0.4013},
    'integration_batch': {'candidate_index': 1, 'mean_abs_log_error': 0.0101},
    'benchmarking': {'candidate_index': 1, 'mean_abs_log_error': 0.1707},
    'qc_artifacts': {'candidate_index': 1, 'mean_abs_log_error': 0.0184},
    'lineage_barcoding': {'candidate_index': 1, 'mean_abs_log_error': 0.0523},
}


def topic_query(topic):
    return f"{SUBFIELD} AND ({TOPICS[topic]})"
