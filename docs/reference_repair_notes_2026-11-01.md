# Reference and bibliography repair — Track A notes

Date: 2026-11-01. Scope: findings A-01 to A-26 of the consolidated review log.
No manuscript text, .tex, .bib original, figure or table was modified. Every output carries a `_corrected`
or clearly new filename; the originals are untouched.

## 1. Decision rule (quotable in the manuscript Methods)

> Each of the 121 reference entries was matched to its typeset manuscript reference number **by normalised
> title** (case, punctuation and whitespace removed), independently of the key number in either BibTeX file
> and of the `n` column of S8_review_references.csv. The title map was required to be one-to-one — 121
> entries, 121 distinct manuscript numbers, no collisions and no orphans — and was then cross-checked
> against the PMID and DOI recorded in each entry, which agreed in 121 of 121 cases. BibTeX keys were
> rewritten as `refNNN` where `NNN` is the manuscript reference number, so that a BibTeX-driven rebuild
> reproduces the printed numbering. Bibliographic metadata was taken from the registered record and from no
> other source: PubMed `efetch` for the 114 entries with a PMID, the Crossref works API for the five
> registered non-PMID entries, and the arXiv API for the one machine-learning conference paper. A field was
> corrected only when the registered record disagreed with the stored value; where the registered record was
> silent, the stored value was left unchanged and the entry is listed as not established.

Reference-support claims were assessed under the manuscript's own abstract-level protocol (§2.5): a claim is
treated as supported only when the source abstract says so. No full texts were consulted.

## 2. What changed

### 2.1 A-01 / A-02 — numbering (major; fixed)

Reproduced before fixing. The two .bib files were byte-identical (42,768 bytes, SHA-256
`d4457eb4…b156`). The key number equalled the manuscript reference number for **22 of 121** entries and
equalled the S8 `n` column for **121 of 121**, confirming that both files follow S8's superseded ordering
(example: `ref068` = Hubert & Arabie, *Comparing partitions* = manuscript [70]).

After correction, verified independently for both corrected files:

```
manuscript/references_corrected.bib:        entries=121 unique_keys=121 title->manuscript resolved=121
                                            key==manuscript_n=121/121 collisions=[] orphans=[]
supplementary/S8_references_corrected.bib:  entries=121 unique_keys=121 title->manuscript resolved=121
                                            key==manuscript_n=121/121 collisions=[] orphans=[]
```

The two corrected .bib files are again byte-identical by design (they are the same bibliography shipped in
two places); the defect was the ordering, not the duplication.

Repo check scripts, run from the project root:

```
$ python docs/review_checks/cite_order.py
references in list: 121
distinct references cited: 121
never cited: []
cited but not in list: []
out of order (first appearance): []

$ python docs/review_checks/ref_list_vs_s8.py            # ORIGINAL S8
S8 rows: 121; manuscript entries: 121; matched by PMID/DOI: 121
S8 rows not found in manuscript list: none
year not found in manuscript entry: none
S8 'n' differs from manuscript number for 99 rows; first few (S8 n -> manuscript n): [('20','26'),('21','27'),('22','28'),('23','29'),('24','30'),('25','31')]

$ python ref_list_vs_s8.py (same script, path swapped to the corrected CSV)
S8 rows: 121; manuscript entries: 121; matched by PMID/DOI: 121
S8 rows not found in manuscript list: none
year not found in manuscript entry: none
S8 'n' differs from manuscript number for 0 rows; first few (S8 n -> manuscript n): []
```

**Is the renumbering load-bearing for the build?** No, not for the current build. `sc_cancer_evaluation_review.tex`
contains **zero** `\cite` commands, no `\bibliography`/`\bibliographystyle`, no `thebibliography` environment and
zero `\bibitem`s: the reference list is a pandoc-generated `enumerate` of `\item`s with the numbers fixed by
list position. The .bib files are therefore a supplementary artefact today. They become load-bearing the moment
anyone rebuilds through BibTeX/biblatex, which is exactly the silent-renumbering risk A-01 describes.

### 2.2 Metadata corrections

| Finding | Entries | What changed |
|---|---|---|
| A-11 | [41], [92] | Empty author field, which typeset as a leading bare full stop, replaced by `{[No authors listed]}` in the .bib and `[No authors listed]` in S8. PubMed returns an empty AuthorList for both (PMIDs 42637979, 39592883), so the absence of a byline is factually correct. |
| A-12 | [7], [25], [87], [117], [118] | Collective (consortium) author restored in the S8 `authors` field at its PubMed position; for [118] the collective is the **first** author, so it is also prepended in the .bib byline. |
| A-12 (extension, found here) | 41 entries | The .bib author lists are truncated at 10 names with no BibTeX `and others`, so a rebuild would print an incomplete byline with no "et al.". `and others` appended wherever PubMed lists more authors than the .bib. |
| A-13 | [70], [72], [78], [89], [91] | Volume and pages filled from Crossref. |
| A-15 | [72], [78], [89], [91] | Author initials corrected: Rousseeuw P→PJ, Uhlmann E→EL, Martin D→DP, Tibshirani R→RJ, Angelopoulos A→AN. |
| A-25 | [88] | `@article` with journal "Proceedings of ICML 2017 (PMLR 70); arXiv:1706.04599" → `@inproceedings`, booktitle *Proceedings of the 34th International Conference on Machine Learning*, series PMLR, volume 70, pages 1321-1330; the arXiv DOI moved to a note. |
| A-25 | [90] | `@article` with journal "Springer (book)" → `@book`, publisher Springer International Publishing, ISBN 978-3-031-06648-1. |
| A-22 | S5, 106 rows | `claim_check` split into `claim_verdict` (supported 63; supported after revision 33; not established at abstract level 10) and `claim_check_provenance`; a `cited_in_manuscript` flag marks the 4 background PMIDs (29898899, 31900397, 32033589, 37197983) held in S5 but not among the 121 references. |

### 2.3 Partial rebuttal of A-13

A-13 states that the seven non-PMID .bib entries "carry no DOI field at all". That half does **not**
reproduce: all seven (`ref068`, `ref070`, `ref076`, `ref086`, `ref087`, `ref088`, `ref089`) already carry a
`doi` field. The volume/pages half does reproduce and is fixed for the five journal articles; [88] is a
conference paper and [90] a book, where volume/pages do not apply in the same way.

## 3. Citation-support repairs (text handed to the text track, not applied)

All old → new sentence pairs are in `supplementary/S8_text_track_handoff_sentences.csv` (30 rows, each with
the verbatim old text, the proposed new text, the reason and the evidence span).

**A-03 (§4.7).** Reproduced. PMID 37215029 reports accuracy "better than random chance but still far from
perfect"; the "fail to outperform random guessing" wording in that abstract describes prior literature.
PMID 29914350 reports that most assessed methods cannot predict network structure accurately and makes no
random-predictor comparison. A targeted PubMed sweep (3 queries, 200 distinct candidate records, abstracts
screened for sentences containing "random"/"chance" together with a negative-comparison verb) found **no**
abstract in the single-cell GRN benchmarking literature reporting that methods fail to beat a random
predictor. The claim is therefore **not established at abstract level** and the sentence must be reworded,
not re-cited. The replacement adds McCalla et al. 2023 (PMID 36626328), whose abstract supports the weaker,
correct statement ("most methods have a modest recovery of experimentally derived interactions based on
global metrics such as Area Under the Precision Recall curve").

**A-04 (§4.4), citation half.** Reproduced: S1 codes all 17 annotation records `unclear` for
`assessed_calibration_or_uncertainty`, including PMID 40439669 = reference [35], and 9 of 269 records
overall are coded `True`. The *citation* is correct — [35] is an evaluation of out-of-distribution detection
methods and its abstract states that the authors "evaluate six OOD detection methods … for their annotation
and OOD detection performance" and that those methods "can accurately identify novel cell types", which is
exactly the construct the field names. The *catalogue code* is what disagrees. Preferred resolution is the
S1 recode (owned by the catalogue track); a fallback sentence that needs no recode is supplied.

**A-05 (§4.1).** Reproduced: the class holds 7 records, `cancer_specific` True for 7/7, years 2024–2026;
refs [26–31] cover six. The seventh, Han S, Xiong Z, Zhou Y, Yang C. *Benchmarking copy number alteration
inference methods for spatial transcriptomics*. Nat Commun. 2026;17:10565, PMID 42838986,
doi 10.1038/s41467-026-77500-5, is verified by PubMed efetch and is uncited anywhere in the manuscript.
It must be inserted at the **end** of the existing `[26–31]` range in §4.1 sentence 1.

## 4. Renumbering cascade

Full table: `supplementary/S8_reference_renumbering_cascade.csv` (143 rows). The manuscript numbering is in
strict first-appearance order (`cite_order.py`: `out of order (first appearance): []`), so insertion position
determines the cascade exactly.

- **A-05 alone** (Han at the end of the §4.1 range): Han becomes **[32]**; existing [32]–[121] become
  [33]–[122]; **90 of 121** existing numbers change; the list grows 121 → 122.
- **All 22 proposed additions adopted**: the list grows 121 → **143**; **96 of 121** existing numbers change.
  Han becomes [41]; [117] (HTAN) → [32] and [118] (CELLxGENE) → [33], because A-18 requires citing them at
  their first mention in §2.6 rather than at their current first citation much later.

## 5. Proposed additions (22)

`supplementary/S8_references_additions_proposed.bib` and `supplementary/S8_reference_additions_proposed.csv`
hold a typeset entry in the manuscript's exact style and a BibTeX entry for each. Keys are author-year, not
`refNNN`, because the final numbers depend on which additions are adopted. Every record was verified against
PubMed efetch (16) or the Crossref works API (5); one (Python) is a book with a canonical URL and no DOI.

Completeness pass across the 12 §4 method classes
(`supplementary/S8_landmark_coverage_check.csv`): for each class the neutral benchmark a referee would name
was checked by PMID against the 121-entry list. **8 of 16 checked works were already cited** — Avila Cobos
2020 (§4.2), Luecken 2022 and Tran 2020 (§4.3), Abdelaal 2019 (§4.4), Dimitrov 2022 (§4.5, = reference [16]),
Soneson 2018 (§4.9), Xi & Li 2021 (§4.10) and Ahlmann-Eltze 2025 (§4.11). §4.8 claims no landmark and the
text explains why. The gaps are exactly those the review named (BEELINE, Sturm, Demuxafy) plus the two tool
method papers (§4.6) and the two uncited drug-response records (§4.12). **No further missing landmark work
was identified**; this pass was deliberately conservative and did not treat "catalogued in S1 but uncited"
as a gap, since 230 of the 269 S1 records are uncited by design.

## 6. A-18 — resources without a citation or URL

Reproduced: a regex scan of the manuscript body (everything before `## References`) returns **zero** http(s)
URLs. Named resources and the recommended treatment:

| Resource | Named | First body mention | Recommended treatment |
|---|---|---|---|
| PubMed / Entrez E-utilities | 19 / 3 | §2.1 | Numbered reference — Sayers EW et al. Nucleic Acids Res 2025;53:D20-D29 (PMID 39526373) |
| NCBI GEO | 11 | §2.6 | Numbered reference — Barrett T et al. Nucleic Acids Res 2013;41:D991-5 (PMID 23193258) |
| bioRxiv (server and API) | 4 | §2.1 | Numbered reference — Sever R et al. bioRxiv 2019, doi 10.1101/833400, **plus** inline URL `<https://api.biorxiv.org>` for the API |
| Crossref | 4 | §2.9 | Numbered reference — Hendricks G et al. Quant Sci Stud 2020;1:414-427 |
| dbGaP | 1 | §2.6 | Numbered reference — Mailman MD et al. Nat Genet 2007;39:1181-6 (PMID 17898773) |
| EGA | 1 | §2.6 | Numbered reference — Freeberg MA et al. Nucleic Acids Res 2022;50:D980-D987 (PMID 34791407) |
| ArrayExpress / BioStudies | 1 | §2.6 | Numbered reference — Sarkans U et al. Nucleic Acids Res 2021;49:D1502-D1506 (PMID 33211879) |
| HTAN | 1 | §2.6 | Already reference [117]; move the first citation to §2.6 |
| CELLxGENE | 1 | §2.6 | Already reference [118]; move the first citation to §2.6 |
| TISCH / TISCH2 | 0 in body | — | Already references [114], [115]; no change |
| Python | 2 | Declarations | Numbered reference — Van Rossum G, Drake FL. Python 3 Reference Manual. CreateSpace; 2009; inline `<https://www.python.org>` |
| NumPy | 1 | Declarations | Numbered reference — Harris CR et al. Nature 2020;585:357-362 (PMID 32939066) |
| pandas | 1 | Declarations | Numbered reference — McKinney W. Proc 9th Python in Science Conf 2010:56-61 |
| SciPy | 1 | Declarations | Numbered reference — Virtanen P et al. Nat Methods 2020;17:261-272 (PMID 32015543) |
| statsmodels | 1 | Declarations | Numbered reference — Seabold S, Perktold J. Proc 9th Python in Science Conf 2010:92-96 |
| Matplotlib | 1 | Declarations | Numbered reference — Hunter JD. Comput Sci Eng 2007;9:90-95 |
| pandoc | 1 | Declarations | **Inline URL** `<https://pandoc.org>` — no citable publication |
| Tectonic | 1 | Declarations | **Inline URL** `<https://tectonic-typesetting.github.io>` — no citable publication |
| arXiv | §2.9 | §2.9 | **Inline URL** `<https://arxiv.org>` |

Note: PubMed and GEO are first named in the Abstract (offsets 209 and 699). Citations are placed at the first
mention in the body proper, not in the Abstract, since most journals disallow citations there.

## 7. Manuscript-visible numbers

**Changed by this track: none.** No statistic, count or percentage printed in the manuscript is altered by
the bibliography repair. The numbers below are what this track checked and found unchanged, or changes that
are conditional on another track's decision.

Unchanged (checked, with denominators):

- Reference-list size: 121 entries, 121 cited, none never-cited, none cited-but-absent, none out of
  first-appearance order — unchanged.
- §4.1 "All seven benchmarks in this class are cancer-specific": 7/7 `cancer_specific = True`, years
  2024–2026 — confirmed, unchanged. Only the citation range changes.
- §4.10 "truth in 10 of 13 benchmarks": 10 of 13 records list genotype multiplexing — confirmed, unchanged.
  Only the attribution changes (0 of 13 list hashing).
- §4.12 "3 benchmarks in the catalogue": 3 records — confirmed, unchanged. Only the citations change.
- §5.3 / §3.4 robustness 5.6% (15/269) and metric validity 3.0% (8/269) — not touched by this track.
- S8 ↔ manuscript matching: 121/121 by PMID or DOI, 0 rows unmatched, 0 year mismatches — unchanged.
- Full PubMed re-verification of the 114 entries with a PMID: **0** title mismatches, **0** year mismatches,
  **0** DOI mismatches, **0** retraction-related publication types.

Conditional (owned by another track; stated here so the cascade is visible):

- §5.3 calibration **9/269 = 3.3% → 10/269 = 3.7%**, if and only if the catalogue track recodes PMID 40439669
  to `assessed_calibration_or_uncertainty = True` per A-04. The cancer-specific calibration count stays
  **2/48**, because that record is `cancer_specific = False`.
- Reference-list size **121 → 122** if only A-05 is adopted, or **121 → 143** if all 22 additions are adopted.

## 8. Not established / not checked

1. **"Methods often do not beat random predictors" has no abstract-level source.** Searched PubMed with 3
   queries (200 distinct candidate records) and screened every abstract; no single-cell GRN benchmark states
   that methods fail to beat a random predictor as its own finding. The claim must be reworded, not re-cited.
2. **PMLR page range for [88] (1321-1330) is carried from the review's finding A-25 and was not
   independently re-verified.** PMLR deposits no Crossref DOI for ICML 2017 and proceedings.mlr.press is not
   reachable from this sandbox; the arXiv API confirms authors, title and the "ICML 2017" venue but no pages.
3. **[90] edition number not established.** Crossref returns no `edition-number` for
   10.1007/978-3-031-06649-8; the entry records publisher, year and ISBN only.
4. **A-21 (four uncited mechanistic assertions) — no citation found.** No abstract-level source was located
   for any of the four; each is handed back to be marked as the author's reasoning.
5. **A-24 — not checkable at abstract level.** The specific dependence of the adjusted Rand index on cluster
   number and balance is not stated in the PMID 15355155 abstract; full text not consulted, per protocol.
6. **S5's 10 "not checked" rows remain not established.** They have no PubMed abstract; they are now labelled
   `not established at abstract level` rather than carrying a history string. They were not re-checked
   against full texts.
7. **Demuxafy's absence from S1 is not explained.** PMID 38622708 is in neither the 121-entry list nor the
   269-record catalogue. Whether this is a screening-rule exclusion or an omission is for the catalogue track.
8. **No full texts were read** anywhere in this track, in line with the manuscript's abstract-level protocol.

## 9. Files written

All are new files; no original was modified.

| File | Contents |
|---|---|
| `manuscript/references_corrected.bib` | 121 entries, keys = manuscript numbers, metadata corrected |
| `supplementary/S8_references_corrected.bib` | identical copy for the supplement |
| `supplementary/S8_review_references_corrected.csv` | `n` renumbered; author, volume, page and venue fixes |
| `supplementary/S5_foundations_refs_corrected.csv` | `claim_check` split; `cited_in_manuscript` flag added |
| `supplementary/S8_reference_mapping.csv` | manuscript_number, old/new bib key, old/corrected S8 n, title, pmid, doi, metadata-changed flag |
| `supplementary/S8_reference_repair_diff.csv` | every changed cell with reason and evidence span |
| `supplementary/S8_references_additions_proposed.bib` | BibTeX for the 22 proposed additions |
| `supplementary/S8_reference_additions_proposed.csv` | typeset entries, sections, findings, verification route |
| `supplementary/S8_reference_renumbering_cascade.csv` | number now / if A-05 only / if all adopted, 143 rows |
| `supplementary/S8_text_track_handoff_sentences.csv` | 30 old → new sentence pairs with evidence |
| `supplementary/S8_landmark_coverage_check.csv` | per-class landmark benchmark citation status |
| `docs/reference_repair_notes_2026-11-01.md` | this note |

Diff summary: 395 changed cells across 214 records — 106 × `S5.claim_check -> claim_verdict + claim_check_provenance`, 99 × `bibtex_key`, 99 × `S8.n`, 48 × `bib.author`, 11 × `S8.authors`, 6 × `S8.pages`, 5 × `bib.volume`, 5 × `bib.pages`, 5 × `S8.volume`, 4 × `S5.cited_in_manuscript`, 2 × `bibtex_type`, 2 × `S8.journal`, 1 × `bib.journal->booktitle`, 1 × `bib.doi`, 1 × `bib.journal->publisher`.
