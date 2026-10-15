# Submission package — The evaluation gap in single-cell cancer genomics

Quantitative review, benchmark catalogue and ground-truth resource.
Data: PubMed volume counts 2015 to 15 October 2026; stratified abstract sample 2015–2026 (150/year); benchmark catalogue, GEO ground-truth catalogue and reference verification 14–15 October 2026.

## Contents
- manuscript/sc_cancer_evaluation_review.pdf — typeset manuscript (title page, line numbers, 1.5 spacing; 121 references; abstract 301 words; main text 6,266 words; 6 figures, 6 tables, 1 box)
- manuscript/sc_cancer_evaluation_review.tex — LaTeX source (XeLaTeX/Tectonic; compiles in place with figure PDFs in manuscript/fig/)
- manuscript/sc_cancer_evaluation_review.md — Markdown version
- manuscript/references.bib — bibliography (every record resolved against PubMed, Crossref or arXiv)
- figures/Figure1–6.pdf (vector) and .png (300 dpi), numbered in order of first citation — no in-panel titles; legends are in the manuscript
- tables/Table1–6.csv — source data for Tables 1–6 (Table 2 uses the 2015–2026 window; Table 3 includes the 2015–2026 stated-problem coding)
- supplementary/S1–S8 — Supplementary Data as listed in the manuscript
- code/ — Supplementary Data S9: analysis code (standalone scripts that refit every model and re-render every figure, with a reproduction check of 85 printed values; PubMed queries and retrieval; verbatim coding instructions; full execution record). Start with code/README.md
  - S7_statistics/update_2026-10-15/ — 2026 update (queries, ratios, refitted models), full-window coverage models, topic-by-year panel models, single-cell-genomics sensitivity analyses, and the 2015–2026 stated-problem sample, coding and model-coder agreement. These supersede the files in original_2026-10-04/.

## Correction in this version
Preparing the code release showed that 29 papers had been drawn in two adjacent years of the stratified abstract sample and counted twice. Each is now counted once (1,771 unique abstracts, 989 using single-cell omics data). Estimates moved by at most a few tenths of a percentage point and no conclusion changed; details are in code/README.md.

## Items to complete before submission
1. Corresponding-author e-mail (placeholder on title page).
2. Authors' contributions statement (placeholder in Declarations).
3. Licence for the code (code/README.md) and, if deposited publicly, its repository DOI in the Code availability statement.
4. Target-journal formatting (reference style, word limits, figure file requirements).

## Known limitations (stated in the manuscript)
Abstract-level coding (assessment counts are lower bounds); model-based second coders, with low agreement for rare problem categories; the subfield query includes non-genomics single-cell work before 2020, and the subfield-wide decline is not significant when restricted to single-cell genomics; GEO-only, regex-based ground-truth catalogue with unmeasured recall; 2026 counts updated by query-ratio scaling.
