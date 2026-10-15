# Supplementary Data S9 — analysis code

Code for *The evaluation gap in single-cell cancer genomics: a quantitative review, benchmark catalogue and ground-truth resource* (data to 15 October 2026).

The folder has two parts:

1. `src/` — standalone, documented scripts. Run offline, they refit every model in the paper from the supplied inputs and check the results against the values printed in the manuscript. Online, they re-run the PubMed retrieval and the abstract coding.
2. `provenance/` — the verbatim record of every code cell executed during the study, in execution order: 332 cells from the main session and four parallel sub-analyses.

## Quick start (offline, about 10 s)

```bash
pip install -r requirements.txt
cd src
python 03_statistics.py   # all models -> ../outputs/*.csv and ../outputs/reproduction_check.csv
python 04_figures.py      # Figures 1-6 -> ../outputs/fig/
```

Expected output of `03_statistics.py`: `85/85 quantities reproduce the manuscript values at the printed precision`. `04_figures.py` produces PNGs that are pixel-identical to the published figures (checked on 15 October 2026).

## Layout

| Path | Content | Manuscript |
|---|---|---|
| `src/queries.py` | Subfield query, 26 topic queries (with calibration error against the archived counts), evaluation-title query, Entrez-date snapshot cap, research-article filter | §2.1, §2.7 |
| `src/eutils.py` | Rate-limited NCBI E-utilities wrappers (count, search, efetch abstracts, esummary, first publication year) | §2.1–2.9 |
| `src/01_pubmed_counts.py` | Yearly subfield and topic counts, 2015–2026; 2026 update ratios | §2.1, §2.7 |
| `src/02_sample_and_code_abstracts.py` | Stratified sample (150 per year) and stated-problem coding (primary and second model) | §2.4 |
| `src/coding_prompt.py` | Verbatim coding definitions, category list and tool schema | §2.4, Table 3 |
| `src/03_statistics.py` | Trend tests, NB2 topic-coverage models (2023–26 and 2015–26), topic-by-year panel, single-cell-genomics sensitivity, stated-problem prevalence and trends, coder agreement, topic rates, reproduction check | §2.8, §3.1–3.3, Tables 2–3 |
| `src/04_figures.py`, `figstyle.py`, `figure_inputs.py` | Figure code as used for the published figures, with a loader for the snapshotted figure inputs | Figs 1–6 |
| `data/raw_inputs/` | Analysis-ready inputs: PubMed volume (`pubmed_volume_long.csv`), topic table, yearly series, benchmark PMIDs with year and topic tags, sc-genomics flags, primary and second-model codes | — |
| `data/figure_inputs/` | Exact in-memory objects consumed by the figure code | Figs 1–6 |
| `data/expected_values.csv` | 85 values as printed in the manuscript (with the phrase that contains each), used by the reproduction check | — |
| `build/` | pandoc template, Markdown body and `build_manuscript.sh` (pandoc → LaTeX → Tectonic) | — |
| `provenance/*_session.md` / `.jsonl` | Executed code, in order, with tool, environment, description and status | all |

## What reproduces exactly and what approximately

- **Exactly (offline):** every statistical model, interval and test, given the supplied inputs. The same goes for every figure.
- **Approximately (online):**
  - PubMed counts drift as records are indexed or re-dated. For example, the 2015 subfield count was 443 in the archive and 442 on 15 October 2026.
  - The original 2015–2025 topic queries were not preserved. `queries.py` holds reconstructions calibrated to the archived counts, and the paper uses the archived counts for 2015–2025, applying the reconstructed queries only for the 2026 update ratios (§2.7). A re-run on 15 October 2026 matched the archived 2015 counts exactly for 13 of 26 topics (12 with non-zero counts; spatial transcriptomics had none in either). Summed over topics, it gave 428 papers against 418 archived (+2.4%), with the largest relative differences in topics with fewer than 20 papers that year, such as deconvolution (3 against 1) and T-cell exhaustion (1 against 5).
  - `esearch` ordering changes over time, so re-sampling draws different abstracts.
  - Language-model coding is not bit-reproducible across API versions.
  - The values used in the paper are therefore shipped as data: `supplementary/S7_statistics/update_2026-10-15/problem_sample_2015_2026.csv` and `data/raw_inputs/`.
- **Not re-runnable from `src/`:** the benchmark catalogue (search, screening and manual corrections), the GEO ground-truth catalogue, the first-pass validation and the reference verification. Their complete executed code is in `provenance/benchmarks_session.md`, `foundations_session.md`, `validation_session.md` and `statistics_session.md`. Their outputs are Supplementary Data S1–S8.

## Provenance record

| Session | Cells | Failed cells |
|---|---|---|
| `main_session` | 213 | 22 |
| `statistics_session` | 21 | 0 |
| `validation_session` | 26 | 2 |
| `benchmarks_session` | 36 | 2 |
| `foundations_session` | 36 | 3 |

Notes on reading the record:
- **Cell structure:** cells ran in a persistent interpreter, so later cells depend on variables defined earlier.
- **Failed cells:** kept unchanged and marked `FAILED`; the next cell normally contains the fix.
- **Platform calls:** cells of type `repl`, and calls to `host.*`, are services of the analysis platform. These include dispatching sub-analyses, saving files, and calling language models through `host.llm` (primary coder `claude-haiku-4-5-20251001`; second coder `claude-sonnet-5`). `src/02_sample_and_code_abstracts.py` issues the equivalent requests through the public Anthropic API.
- **Session-specific paths:** paths such as `{{artifact:...}}` and absolute paths are specific to that session.

## Correction made while preparing this release

Re-running the stated-problem analysis as a standalone script showed that 29 papers had been drawn in two adjacent years. PubMed's `[dp]` field matches both electronic and print publication years. The earlier analysis counted these 29 papers twice. Each is now counted once, in its earlier year.

This gives 1,771 unique abstracts, of which 989 use single-cell omics data (previously reported as 998). Several estimates changed at the first or third decimal: for example, the evaluation-check share in 2015–18 went from 13.8% to 14.0%, and the single-cell-genomics trend from 0.919 (p = 0.055) to 0.920 (p = 0.058). No conclusion changed. The manuscript, Table 3, Figure 4 and the supplementary files reflect the corrected values.

## Before public release

Add a licence of your choice (none is asserted here). If you deposit this folder in a public repository, cite its DOI in the Code availability statement.
