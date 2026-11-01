"""Step 6 - PRISMA 2020-style two-arm flow diagram and the counts behind it.

Arm 1  evaluation-titled benchmark screen -> benchmark catalogue (S1, n = 269)
Arm 2  GEO ground-truth screen            -> ground-truth catalogue (S3, 923 series / 830 groups)

Counts are read from the corrected catalogues and from the archived first-pass screen, never typed:
  arm 1  supplementary/S6_reliability/benchmark_second_pass.csv  (486 records, first_pass_kind)
         supplementary/S7_statistics/update_2026-10-15/new_evaluation_titled_2026-10-05_to_15.csv (3 records)
         S1_benchmark_catalogue_corrected.csv                    (269 records)
  arm 2  S4_ground_truth_methods_corrected.md section 2a/2b      (funnel)
         S3_ground_truth_catalogue_corrected.csv                 (923 series)

Output: ../../figures/PRISMA_flow.{pdf,png} (300 dpi) and ../../tables/PRISMA_counts.csv
Usage:  python 06_prisma.py
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from figstyle import apply_style, METH, BIO, GREY

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
apply_style()

# ------------------------------------------------------------------ arm 1 counts
bs = pd.read_csv(os.path.join(ROOT, "supplementary", "S6_reliability", "benchmark_second_pass.csv"))
nt = pd.read_csv(os.path.join(ROOT, "supplementary", "S7_statistics", "update_2026-10-15",
                              "new_evaluation_titled_2026-10-05_to_15.csv"))
S1 = pd.read_csv(os.environ["S1_CSV"])

n_first_pull = len(bs)
n_late = len(nt)
n_identified = n_first_pull + n_late
kinds = bs.loc[~bs.first_pass_is_benchmark, "first_pass_kind"].value_counts()
assert (~nt.is_benchmark).all(), "late records assumed non-benchmark"
excl = {
    "Biological or clinical evaluation, not a method benchmark": int(kinds["biological_evaluation"]) + n_late,
    "Method paper with token baselines":                          int(kinds["new_method_with_baselines"]),
    "Review or narrative overview":                               int(kinds["review"]),
    "Other (not a genuine benchmark)":                            int(kinds["other"]),
}
n_excluded = sum(excl.values())
n_verified = int(bs.first_pass_is_benchmark.sum())
assert n_identified - n_excluded == n_verified
n_window = n_verified - 1                      # one 1958-2014 record outside 2015-2026
n_cat = len(S1)
n_carried = int(S1.in_prior_158.sum())
n_added = n_cat - n_carried
n_cat_window = int(S1.year.between(2015, 2026).sum())
assert int(S1.pubmed_verified.sum()) == n_cat

# ------------------------------------------------------------------ arm 2 counts (corrected S4 funnel)
S3 = pd.read_csv(os.environ["S3_CSV"], low_memory=False)
A2 = dict(base=6141, union=2715, union_raw=3473, outside_union=3426,
          filt14=2024, filt14_fail=691, filt5=1336, filt5_groups=1166, filt5_fail=688,
          final=len(S3), final_groups=int(S3.study_group.nunique()))
A2_excl = {"No single-cell evidence in the series or its own samples (E1)": 300,
           "No human single-cell sample (E2)": 1,
           "No cancer material profiled (E3a)": 60,
           "Cancer only as reagent or co-culture target (E3b)": 9,
           "Cancer patient, but profiled material explicitly non-tumour (E3c)": 43}
A2["removed"] = sum(A2_excl.values())
assert A2["filt5"] - A2["removed"] == A2["final"] == 923
assert A2["base"] - A2["outside_union"] == A2["union"]
assert A2["union"] - A2["filt14_fail"] == A2["filt14"]
assert A2["filt14"] - A2["filt5_fail"] == A2["filt5"]

# ------------------------------------------------------------------ counts table
rows = [
 ("1 benchmark screen","Identification","Evaluation-titled records identified in PubMed",n_identified,
  f"{n_first_pull} retrieved 4 Oct 2026; {n_late} further records indexed 5-15 Oct 2026"),
 ("1 benchmark screen","Screening","Records screened on title and abstract",n_identified,
  "two independent coding passes; inter-pass Cohen's kappa = 0.74 (0.68-0.80), 88.5% agreement"),
 ("1 benchmark screen","Screening","Records excluded",n_excluded,"; ".join(f"{k}: {v}" for k,v in excl.items())),
] + [("1 benchmark screen","Screening - exclusion reason",k,v,"") for k,v in excl.items()] + [
 ("1 benchmark screen","Included","Verified method benchmarks",n_verified,
  "32.3% of evaluation-titled records (Wilson 95% CI 28.3-36.6)"),
 ("1 benchmark screen","Included","Verified benchmarks in the 2015-2026 analysis window",n_window,
  "one verified benchmark published in 2014 falls outside the window"),
 ("1 catalogue assembly","Identification","Additional records sought by targeted searching",np.nan,
  "16 class-specific PubMed queries; about 90 targeted landmark searches; 14 supplementary queries"),
 ("1 catalogue assembly","Included","Benchmark catalogue (Supplementary Data S1)",n_cat,
  f"{n_carried} carried from the verified first-pass screen, {n_added} added by targeted searching; "
  f"all {n_cat} resolved through PubMed efetch and re-checked by esummary title match; "
  f"{n_cat_window} dated 2015-2026"),
 ("2 GEO screen","Identification","GEO DataSets base query (human tumour single-cell GSE)",A2["base"],
  "retrieved only; never classified, and not the denominator of any reported fraction"),
 ("2 GEO screen","Identification","Union of the nine modality queries",A2["union"],
  f"{A2['union_raw']} hits before de-duplication"),
 ("2 GEO screen","Identification","Base-set series outside the modality union",A2["outside_union"],
  "56% of the base set; cannot enter the catalogue, so the catalogue is a lower bound"),
 ("2 GEO screen","Screening","Passing eligibility filters 1-4",A2["filt14"],
  f"{A2['filt14_fail']} failed: gdstype not sequencing, non-human taxon, no single-cell regex, or no cancer regex"),
 ("2 GEO screen","Screening","At least one modality rule fires on series-level text",A2["filt5"],
  f"{A2['filt5_fail']} carried no modality call; {A2['filt5_groups']} study groups - this was the published catalogue"),
 ("2 GEO screen","Screening","Removed by the series-level eligibility re-screen",A2["removed"],
  "; ".join(f"{k}: {v}" for k,v in A2_excl.items())),
] + [("2 GEO screen","Screening - exclusion reason",k,v,"") for k,v in A2_excl.items()] + [
 ("2 GEO screen","Screening","Corrected CITE-seq rule applied",A2["final"],
  "modality-level only: 6 of 227 CITE-seq calls dropped as androgen-deprivation-therapy false positives"),
 ("2 GEO screen","Included","Ground-truth catalogue (Supplementary Data S3)",A2["final"],
  f"{A2['final_groups']} study groups; audited precision 130/140 = 92.9% (87.4-96.1)"),
]
cnt = pd.DataFrame(rows, columns=["arm","stage","box","n","detail"])
cnt.to_csv(os.path.join(ROOT, "tables", "PRISMA_counts.csv"), index=False)

# ------------------------------------------------------------------ diagram
import textwrap

FIGW, FIGH = 11.0, 9.4
FS_MAIN, FS_EXCL = 6.4, 5.9
MW, EW = 0.250, 0.185
LX, LEX = 0.335, 0.105
RX, REX = 0.715, 0.900
WRAP_MAIN, WRAP_EXCL = 44, 36
GAP, GAP_E = 0.026, 0.013

def _lines(text, width):
    out = []
    for ln in text.split("\n"):
        out.extend(textwrap.wrap(ln, width) or [""])
    return out
def _h(n, fs):
    return (n * fs * 1.42 / 72.0) / FIGH + 0.018

fig = plt.figure(figsize=(FIGW, FIGH))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")

def draw_box(x, y, lines, w, fs, fc, align):
    h = _h(len(lines), fs)
    ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.003,rounding_size=0.006",
                                linewidth=0.7, edgecolor="0.35", facecolor=fc, zorder=2))
    tx = x if align == "center" else x - w/2 + 0.009
    ax.text(tx, y, "\n".join(lines), ha=align, va="center", fontsize=fs, zorder=3, linespacing=1.42)
    return h
def arrow(p0, p1):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=7,
                                 linewidth=0.7, color="0.35", shrinkA=0, shrinkB=0, zorder=1))

def column(x, ex, items, top, side):
    """items: (kind, text). Returns (bottom_of_last_main, cursor)."""
    prep = [(k, _lines(t, WRAP_MAIN if k == "main" else WRAP_EXCL)) for k, t in items]
    prep = [(k, L, _h(len(L), FS_MAIN if k == "main" else FS_EXCL)) for k, L in prep]
    cursor = top; last_bottom = None
    for k, L, h in prep:
        yc = cursor - h/2
        if k == "main":
            draw_box(x, yc, L, MW, FS_MAIN, "white", "center")
            if last_bottom is not None:
                ax.plot([x, x], [last_bottom, yc + h/2 + 0.004], color="0.35", lw=0.7, zorder=1)
                arrow((x, yc + h/2 + 0.012), (x, yc + h/2))
            last_bottom = yc - h/2
            cursor = last_bottom - GAP
        else:
            draw_box(ex, yc, L, EW, FS_EXCL, "#f2f2f2", "left")
            x0 = x + MW/2 if side == "right" else x - MW/2
            x1 = ex - EW/2 if side == "right" else ex + EW/2
            ax.plot([x, x], [last_bottom, yc], color="0.35", lw=0.7, zorder=1)
            arrow((x0, yc), (x1, yc))
            cursor = yc - h/2 - GAP_E
    return last_bottom, cursor

TOP = 0.945
ax.text(LX, TOP + 0.030, "Arm 1 \u2014 evaluation-titled benchmark screen", ha="center", fontsize=7.6, fontweight="bold", color=METH)
ax.text(RX, TOP + 0.030, "Arm 2 \u2014 GEO ground-truth screen", ha="center", fontsize=7.6, fontweight="bold", color=BIO)

excl1 = f"Records excluded, n = {n_excluded}\n" + "\n".join(f"\u2022 {k}: {v}" for k, v in excl.items())
arm1 = [
 ("main", f"Evaluation-titled records identified in PubMed\nn = {n_identified} ({n_first_pull} at the 4 Oct 2026 pull; "
          f"{n_late} indexed 5\u201315 Oct 2026)"),
 ("main", f"Records screened on title and abstract\nn = {n_identified} (two coding passes; \u03ba = 0.74, 88.5% agreement)"),
 ("excl", excl1),
 ("main", f"Verified method benchmarks\nn = {n_verified} (32.3%; 95% CI 28.3\u201336.6)"),
 ("main", f"In the 2015\u20132026 analysis window\nn = {n_window} (one verified benchmark published 2014)"),
 ("main", "Additional records sought by targeted searching: 16 class-specific PubMed queries; "
          "\u224890 targeted landmark searches; 14 supplementary queries"),
 ("main", "Records assessed for inclusion in the catalogue: primary contribution is a comparative evaluation of "
          "\u22652 existing methods, or of platforms with computational read-outs; preprint and journal versions merged"),
]
arm2 = [
 ("main", f"GEO DataSets base query (human tumour single-cell GSE)\nn = {A2['base']:,} retrieved \u2014 never classified"),
 ("excl", f"Base-set series outside the modality union, n = {A2['outside_union']:,} (56%)\n"
          "These cannot enter the catalogue, so every count is a lower bound"),
 ("main", f"Union of the nine modality queries\nn = {A2['union']:,} ({A2['union_raw']:,} hits before de-duplication)"),
 ("excl", f"Failed eligibility filters 1\u20134, n = {A2['filt14_fail']}\n"
          "\u2022 gdstype not sequencing\n\u2022 non-human taxon\n\u2022 no single-cell regex match\n\u2022 no cancer regex match"),
 ("main", f"Passing eligibility filters 1\u20134\nn = {A2['filt14']:,}"),
 ("excl", f"No modality rule fired, n = {A2['filt5_fail']}"),
 ("main", f"\u22651 modality rule fires on series-level text\n"
          f"n = {A2['filt5']:,} series in {A2['filt5_groups']:,} study groups (the published catalogue)"),
 ("excl", f"Removed by the series-level eligibility re-screen, n = {A2['removed']}\n"
          + "\n".join(f"\u2022 {k}: {v}" for k, v in A2_excl.items())),
 ("main", f"Corrected CITE-seq rule applied\nn = {A2['final']} (modality-level only: 6 of 227 CITE-seq calls dropped)"),
]
b1, c1 = column(LX, LEX, arm1, TOP, "left")
b2, c2 = column(RX, REX, arm2, TOP, "right")

ybot_top = min(c1, c2) - 0.022
L_in = _lines(f"Benchmark catalogue (Supplementary Data S1)\nn = {n_cat} PubMed-verified benchmarks in 16 method "
              f"classes ({n_carried} carried from the first-pass screen, {n_added} added by targeted searching; "
              f"{n_cat_window} dated 2015\u20132026)", WRAP_MAIN)
R_in = _lines(f"Ground-truth catalogue (Supplementary Data S3)\nn = {A2['final']} series in {A2['final_groups']} study "
              f"groups (audited precision 130/140 = 92.9%, 87.4\u201396.1; recall not measured)", WRAP_MAIN)
hmax = max(_h(len(L_in), FS_MAIN), _h(len(R_in), FS_MAIN))
yc_in = ybot_top - hmax/2
for xx, LL, fc, bb in [(LX, L_in, "#e8f0f4", b1), (RX, R_in, "#f7efe3", b2)]:
    draw_box(xx, yc_in, LL, MW, FS_MAIN, fc, "center")
    ax.plot([xx, xx], [bb, yc_in + hmax/2 + 0.004], color="0.35", lw=0.7, zorder=1)
    arrow((xx, yc_in + hmax/2 + 0.012), (xx, yc_in + hmax/2))
ybottom = yc_in - hmax/2
ax.plot([0.525, 0.525], [ybottom - 0.01, TOP + 0.022], color="0.86", lw=0.6, zorder=0)
for lab, y0, y1 in [("Identification", TOP, TOP - 0.115),
                    ("Screening", TOP - 0.125, ybot_top),
                    ("Included", ybot_top - 0.004, ybottom)]:
    ax.text(0.0055, (y0 + y1) / 2, lab, rotation=90, ha="center", va="center", fontsize=6.6, color="0.4")


out_png = os.path.join(ROOT, "figures", "PRISMA_flow.png")
fig.savefig(out_png, bbox_inches="tight")
fig.savefig(out_png.replace(".png", ".pdf"), bbox_inches="tight")
print("PRISMA written; arm1 identified", n_identified, "excluded", n_excluded, "verified", n_verified,
      "catalogue", n_cat, "| arm2 final", A2["final"], A2["final_groups"], "| ybottom", round(ybottom,3))
