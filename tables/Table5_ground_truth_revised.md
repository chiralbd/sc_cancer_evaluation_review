**Table 5. Public validation-bearing tumour single-cell series in GEO, by modality.** Corrected catalogue of 1 November 2026: 923 series in 830 study groups, after a series-level eligibility re-screen and a corrected CITE-seq rule. Study groups collapse SuperSeries and their SubSeries. Tasks are those the modality can supply truth for. Audit gives the hand-adjudicated confirmed/sampled modality calls with the Wilson 95% interval on precision; the precision-adjusted series range applies that interval to the modality count.

| Modality | Series | Study groups | Median samples | Most frequent cancer types (series) | Benchmark tasks enabled | Audit (confirmed/n; precision 95% CI) | Precision-adjusted series |
|--------------------|--------|--------|--------|------------------------------------|--------------------------------|------------------------|------------------------|
| Paired bulk RNA | 233 | 206 | 20 | glioma/glioblastoma (25); acute myeloid leukaemia (25); lung cancer (23) | deconvolution, pipeline robustness | 14/15 (70–99%) | 163–231 |
| Longitudinal / on-treatment | 229 | 209 | 16 | acute myeloid leukaemia (32); glioma/glioblastoma (30); breast cancer (17) | pipeline robustness, perturbation response | 16/20 (58–92%) | 133–211 |
| Paired spatial | 186 | 167 | 12 | glioma/glioblastoma (22); breast cancer (20); pancreatic cancer (20) | deconvolution, CCC spatial referee | 14/15 (70–99%) | 130–184 |
| CITE-seq protein | 181 | 175 | 16 | acute myeloid leukaemia (23); myelodysplastic/myeloproliferative (19); lung cancer (19) | annotation calibration | 13/15 (62–96%) | 112–175 |
| Genotype / hashtag multiplex | 134 | 123 | 8 | acute myeloid leukaemia (19); lung cancer (17); renal cell carcinoma (13) | annotation calibration, pipeline robustness | 15/15 (80–100%) | 106–134 |
| Matched WES/WGS | 106 | 91 | 18 | lung cancer (13); colorectal cancer (12); lymphoma (10) | malignant calling, clone calling | 14/15 (70–99%) | 74–105 |
| Perturb-seq | 57 | 54 | 13 | chronic myeloid leukaemia (21); breast cancer (6); acute myeloid leukaemia (6) | pipeline robustness, perturbation response | 14/15 (70–99%) | 40–57 |
| Cell-line mixture | 24 | 19 | 6 | lung cancer (11); chronic myeloid leukaemia (6); sarcoma (3) | malignant calling, deconvolution, annotation calibration, pipeline robustness | 15/15 (80–100%) | 19–24 |
| mtDNA lineage | 15 | 9 | 29 | chronic lymphocytic leukaemia (5); colorectal cancer (4); acute myeloid leukaemia (3) | clone calling | 15/15 (80–100%) | 11–15 |
