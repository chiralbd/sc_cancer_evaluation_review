# Internal critical review guide

**Manuscript:** *The evaluation gap in single-cell cancer genomics: a quantitative review, benchmark catalogue and ground-truth resource* (Md. Jubayer Hossain)
**Version under review:** `manuscript/sc_cancer_evaluation_review.pdf` (also `.docx`), data to 15 October 2026
**Purpose:** a critical human check before journal submission.

---

## 1. Scope

Focus your evaluation on three tasks:

1. **References.** Cross-check references for accuracy and completeness.
2. **Numbers and claims.** Evaluate the numbers and claims in the text against the data.
3. **Tables and figures.** Cross-check tables and figures against the underlying datasets and the claims made about them.

Out of scope for this round: the choice of topic, writing style, journal fit and the wider scientific framing. Note anything serious you see there, but do not spend time on it.

**Why this matters.** Language models helped with the literature retrieval, abstract coding, second coding pass and drafting (see the AI-use statement in Declarations). No human has checked the references, numbers or tables line by line. Assume any sentence, number or citation could be wrong until you have checked it against a source.

---

## 2. Where things are

| What | Path |
|---|---|
| Manuscript (PDF / Word / LaTeX / Markdown) | `manuscript/sc_cancer_evaluation_review.{pdf,docx,tex,md}` |
| Figures | `figures/Figure1–6.{pdf,png}` |
| Tables as CSV | `tables/Table1–6_*.csv` |
| S1 Benchmark catalogue (269 studies) | `supplementary/S1_benchmark_catalogue.csv` |
| S3 Ground-truth catalogue (1,336 GEO series) | `supplementary/S3_ground_truth_catalogue.csv` |
| S4 GEO queries and classification rules | `supplementary/S4_ground_truth_methods.md` |
| S5 Foundational references with claim checks (106) | `supplementary/S5_foundations_refs.csv` |
| S6 Coding reliability | `supplementary/S6_reliability/` |
| S7 Statistics, model inputs and outputs, 2026 update | `supplementary/S7_statistics/` |
| S8 Reference table and BibTeX | `supplementary/S8_review_references.csv`, `S8_references.bib` |
| Analysis code and inputs | `code/` (start with `code/README.md`) |
| Check scripts for this review | `docs/review_checks/` |

**Running the check scripts.** Run every script from the project root (`sc_cancer_evaluation_review/`):

```bash
cd code && python3.11 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt && cd ..
python docs/review_checks/cite_order.py
```

The scripts only read files and print results. `ref_metadata.py` needs internet access (one request to PubMed).

---

## 3. Team and process

| Workstream | People | Main output |
|---|---|---|
| A. References | 2 | reference audit sheet |
| B. Numbers and claims | 2 | numbers audit sheet |
| C. Tables and figures | 2 | table/figure audit sheet |

1. Everyone reads the full PDF once.
2. Each pair works through its checklist below. Within a pair, split the work, then each person re-checks a sample of the other's items.
3. Log every finding in the shared findings log (Section 8).
4. Consolidation meeting: go through critical and major findings and agree what must be fixed before submission.
5. The author responds to every finding in the log: fixed, rebutted (with reason) or deferred (with reason).

**Rules:**
- Check against the **source** (PubMed, the paper itself, the data file), never against another part of the manuscript alone.
- Every finding needs a location: section, PDF line number, table/figure, or file and row.
- Do not use language-model tools to do the checking. The point of this round is a human check.

---

## 4. Pre-check results (already run, 15 October 2026)

These scripted checks were run while preparing this guide. Repeat them, then do the manual checks they cannot do.

| Check | Script | Result |
|---|---|---|
| Every reference cited; numbered in order of first citation | `cite_order.py` | **Pass.** 121 references, all cited, numbering in order of first appearance |
| Reference metadata against live PubMed (title, year, DOI, retraction flags) | `ref_metadata.py` | **Pass for 114 with PMID**, 0 flagged. 7 without PMID (refs to conference papers, books, statistics journals) need hand checks |
| Typeset reference list against S8 | `ref_list_vs_s8.py` | **Finding.** Same 121 works, years agree, but S8's `n` column uses an old order: 99 rows have the wrong number (e.g. S8 row 20 is reference [26]). S8 must be renumbered before release |
| Table 4 against S1 | `table4.py` | **Pass.** Every cell matches |
| Table 5 against S3 | `table5.py` | **Pass**, except trivial rounding: mtDNA lineage median samples is 25.5 in S3 and 25 in Table 5 |
| Earlier consistency issues | — | **Fixed before review:** 157 vs 158 benchmarks (one is from 2014; Fig. 1b caption corrected) and 1,800 vs 1,771 abstracts (abstract corrected) |

---

## 5. Workstream A — References

### A1. Existence and metadata (all 121)

- Run `ref_metadata.py`. For each flagged item, open the PubMed record and confirm.
- Hand-check the 7 references without a PMID, references [70], [72], [78], [88], [89], [90] and [91] in the manuscript (the script lists them by their S8 rows 68, 70, 76, 86–89), via their DOI at `https://doi.org/<doi>`. Check authors, title, year, venue, volume and pages.
- For every reference, check the **author list** in the typeset entry against PubMed. The script does not check authors.
- Check that preprints are not cited where a published version exists. Search the title on PubMed for any bioRxiv or arXiv reference.

### A2. Does the reference support the sentence? (claim check)

This is the most important manual check. The common model errors are: the right paper cited for the wrong claim; a claim stated more strongly than the source; or a number in the text that is not in the cited paper.

- **Sample:** all references cited for a specific number or result (for example "41 recurrent meta-programmes identified across 1,163 tumour samples [20–22]"), plus a random 30 of the rest. Use a random number generator on 1–121 and record the seed.
- For each, read at least the abstract, and the full text where the claim is specific. Record: *supported / partly supported / not supported / cannot tell*, with the passage that supports it.
- S5 already records, for 106 foundational references, the claim attributed to each and whether it was checked against the abstract (`claim`, `claim_check` columns). Re-check a random 20 of them independently. Do not read S5's verdict until you have made your own.

### A3. Completeness

- For each method class in §4, are the obvious landmark benchmarks and method papers cited? List anything important that is missing, with PMID or DOI.
- Are statements of fact without any citation present? Mark sentences in §1, §4, §5 and §6 that need a citation.
- Every database, resource or tool mentioned (GEO, PubMed, CELLxGENE, HTAN, TISCH, software versions) should have a citation or URL.

### A4. Consistency across files

- `manuscript/references.bib`, `supplementary/S8_references.bib`, `S8_review_references.csv` and the typeset list must agree. `ref_list_vs_s8.py` covers S8 against the typeset list; spot-check the `.bib` files.
- Confirm the S8 numbering problem (Section 4) and record it as a finding for the author.

---

## 6. Workstream B — Numbers and claims

### B1. Automated reproduction of the statistics

```bash
cd code/src
python 03_statistics.py   # expect: "85/85 quantities reproduce the manuscript values at the printed precision"
```

This refits every model from the supplied inputs and compares 85 quantities with the values printed in the manuscript (`code/data/expected_values.csv`). Record the exact output. Any mismatch is a **major** finding. It writes results to `code/outputs/`.

What this does **not** cover: numbers outside those 85, numbers that come straight from the catalogues (S1, S3), and whether the text describes the numbers correctly. B2–B4 cover those.

### B2. Trace every number in the abstract and the headline results

For each number below, find it in the source file, recompute it if you can, and check that the text in the abstract, the main text, the figure caption and the table all agree.

| Claim | Where in paper | Source to check |
|---|---|---|
| 443 records in 2015, 7,556 in 2025, 7,571 to 15 Oct 2026 | Abstract, §3.1 | `S7_statistics/update_2026-10-15/pubmed_topic_volume_long_2026-10-15.csv`, `update_log_2026-10-15.csv` |
| 486 evaluation-titled papers, 158 benchmarks (32.5%, 28.5–36.8) | Abstract, §3.2 | `S6_reliability/benchmark_second_pass.csv`; recompute the Wilson interval |
| κ = 0.74 (0.68–0.80); 0.76 on 394; 0.48 on 92 | Abstract, §3.3, §9 | `S6_reliability/validation_agreement.csv` |
| Rate ratio 0.922 (0.875–0.972), p = 0.0027 | Abstract, §3.2, Fig. 1b | `update_2026-10-15/coverage_trend_tests_2026-10-15.csv` |
| Biology topics 0.90 (0.84–0.97); method topics flat | Abstract, §3.2 | `update_2026-10-15/topic_year_panel_models.csv` |
| IRR 2.35 (1.66–3.31) | Abstract, §3.2 | `update_2026-10-15/coverage_model_full_window_2015_2026.csv` |
| Single-cell-genomics trend 0.920 (0.844–1.003), p = 0.058 | §3.2, §9 | `update_2026-10-15/trend_sc_genomics_sensitivity.csv` |
| "No ground truth" 24.2% (364/1,506); κ = −0.01; 45 vs 1 | Abstract, §3.3 | `S6_reliability/problem_types_second_pass.csv` |
| 1,771 unique abstracts, 989 single-cell omics; 1.1% "no ground truth" | Abstract, §3.3 | `update_2026-10-15/problem_coding_2015_2026.csv` |
| 14.0% (2015–18) → 3.6% (2024–26); OR 0.81 | Abstract, §3.3, Fig. 4c | `update_2026-10-15/problem_prevalence_trends_2015_2026.csv` |
| 269 benchmarks; 48 cancer-specific; 15 / 9 / 8 (5.6%, 3.3%, 3.0%); 4, 2, 0 in cancer | Abstract, §3.4 | `S1_benchmark_catalogue.csv` |
| 91 simulation; 44 orthogonal; 107 not stated | §3.4, Fig. 5a | `S1_benchmark_catalogue.csv` (`table4.py` prints the totals) |
| 1,336 series; 1,166 groups; 138 WES/WGS, 227 CITE-seq, 250 spatial | Abstract, §2.6, §6.2 | `S3_ground_truth_catalogue.csv` (`table5.py` prints them) |

Then do the same for a further **random 30 numbers** anywhere in §3–§6, picked by PDF line number.

### B3. Arithmetic and internal consistency

- Percentages: recompute numerator / denominator for every percentage you check.
- Intervals: proportions should have Wilson 95% intervals and rates exact Poisson intervals (§2.8). Recompute a sample (for example with `statsmodels.stats.proportion.proportion_confint(k, n, method="wilson")`).
- Totals: sums in tables should equal the totals in the text.
- The same quantity must have the same value everywhere (abstract, text, caption, table, supplement). Watch especially for values that changed after the 15 October update or the duplicate-abstract correction described in `code/README.md`.
- Time windows: check that each number states its window (2015–2026, 2023–26, 2015–2025) and that numerator and denominator cover the same window. 2026 is a partial year (to 15 October).

### B4. Do the claims follow from the numbers?

For every claim in the abstract and in the first and last paragraph of each Results subsection, ask whether the wording matches the strength of the evidence. Points to look at in particular:

- "Benchmarks per 1,000 papers declined by 7.8% per year." The decline is robust subfield-wide but not significant when restricted to single-cell genomics (p = 0.058). Is this caveat visible enough where the claim is made?
- "The decline was concentrated in biology and application topics." Check the slope-difference test (p = 0.042) and how many tests were run.
- §3.4 calls the convergence of two sources "the central empirical result". Both sources are abstract-level and the benchmark checks are lower bounds. Is the word "central" justified?
- "Public validation data are more widely available than used." The comparison is GEO series that *state* a modality against benchmarks that *state* a ground truth in the abstract. Is this a fair comparison?
- Any causal wording ("because", "led to", "drives") resting on descriptive or correlational data.

Record each as *supported / overstated / unsupported*, with a suggested rewording.

---

## 7. Workstream C — Tables and figures

### C1. Tables

For each table, compare the typeset table in the PDF with its CSV in `tables/`, then the CSV with the underlying data.

| Table | CSV | Underlying data | How to check |
|---|---|---|---|
| 1 Topic taxonomy and growth | `Table1_taxonomy.csv` | `pubmed_topic_volume_long_2026-10-15.csv` | Recompute 2021, 2025, 2023–26 totals, CAGR 2021–25 and share change for at least 8 topics |
| 2 Benchmark coverage by topic | `Table2_coverage.csv` | `coverage_model_input_2026-10-15.csv`, `benchmark_pmids_year_topics.csv` in `code/data/raw_inputs/` | Recompute benchmarks per 1,000 and the exact Poisson interval for at least 8 topics |
| 3 Stated problem types | `Table3_problem_types.csv` | `problem_types_second_pass.csv`, `problem_coding_2015_2026.csv`, `problem_coding_model_agreement.csv` | Recompute percentages, κ and odds ratios for at least 5 rows |
| 4 Benchmark catalogue by class | `Table4_benchmark_classes.csv` | S1 | `table4.py` (passes); also check the `year_range`, `n_2024_26` and `median_n_tools` columns by hand for 4 classes |
| 5 Public validation data | `Table5_ground_truth.csv` | S3 | `table5.py` (passes); also check `top_cancer_types` and `benchmark_tasks_enabled` for 3 rows, and open 10 GEO series to confirm the modality really exists |
| 6 Research agenda | `Table6_agenda.csv` | the text and cited references | Check every anchor reference is the right paper and every "gap evidence" entry matches a number in §3 |

For every table also check: column headings and units; the caption explains every abbreviation; footnotes; row order as stated; and that the PDF table matches the CSV exactly (no dropped rows).

### C2. Figures

1. Regenerate the figures and compare them with the published ones:
   ```bash
   cd code/src && python 04_figures.py   # writes ../outputs/fig/
   ```
   `code/README.md` says they should be pixel-identical to `figures/`. Compare visually or with an image-diff tool.
2. For each figure, check every number in the **caption** against the data and the text (for example, Fig. 1 caption: 443, 7,556, 7,571, n = 12 years, 157 benchmarks, 0.922, 6.2×, 0.44×).
3. Check each panel against the text that cites it: the bar, point or line the text describes should show what the text says.
4. Check axes: labels, units, log scales marked, axis ranges that do not exaggerate, and intervals shown where the caption says they are.
5. Check colours and legends are explained and that the figure is readable in greyscale.
6. Check that each figure is cited in the text, in order, and that panel letters in the text match the figure.

### C3. Catalogue spot-checks (data behind Tables 4–5 and Fig. 5–6)

The scripts confirm that the tables match S1 and S3. They cannot confirm that S1 and S3 are themselves right.

- **S1:** draw 20 random rows. For each, open the PubMed record and check that it meets the inclusion rule (§2.5: a comparative evaluation of at least two existing methods), and that `method_class`, `cancer_specific`, `ground_truth_strategy` and the three `assessed_*` flags are correct from the abstract.
- **S3:** draw 20 random rows. Open each `geo_url` and confirm the listed `validation_modalities` are actually in that series.
- Report the error rate for each field, with the row IDs.

---

## 8. Findings log

Use one shared spreadsheet with these columns:

| ID | Reviewer | Workstream (A/B/C) | Location (section / PDF line / table / figure / file:row) | Finding | Evidence (source, link, recomputed value) | Severity | Suggested fix | Author response | Status |
|---|---|---|---|---|---|---|---|---|---|

**Severity scale:**

| Level | Meaning | Examples |
|---|---|---|
| **Critical** | A headline number or claim is wrong, or a citation is fabricated | Reproduction check fails; a cited paper does not exist; an abstract number is wrong |
| **Major** | A number, table cell or citation is wrong, or a claim overstates the evidence | Table value does not match data; citation does not support the sentence; S8 numbering wrong |
| **Minor** | Small inaccuracy, missing detail, conclusions unaffected | Rounding differences; caption missing an abbreviation; author list typo |
| **Trivial** | Typos, formatting | Inconsistent dashes, spacing |

Status values: `open`, `fixed`, `rebutted` (with reason), `deferred` (with reason).

---

## 9. Consolidation meeting agenda

1. Pre-check results and reproduction output, 5 min
2. Workstream A: references, 15 min
3. Workstream B: numbers and claims, 20 min
4. Workstream C: tables and figures, 15 min
5. Agree the must-fix list before submission and who writes the consolidated report, 5 min

---

## 10. Confidentiality

This manuscript is unpublished. Do not share the files outside the team, do not upload them to public services, and do not paste text into public language-model tools.
