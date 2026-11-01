"""Revision 2026-11-01 - statistical refits answering review findings B-01, B-02, B-03,
B-06, B-09, D-04, D-07, D-08.

Runs offline from data/raw_inputs/, tables/ and supplementary/S7_statistics/update_2026-10-15/.
Writes supplementary/S7_statistics/revision_2026-11-01/*.csv (+ one figure). It does not
modify any existing file: 03_statistics.py remains the generator of the published numbers,
and this script only adds robust-SE, overlap, multiplicity and sensitivity output.

  B-02  robust_se_refits.csv            every panel / coverage / trend quantity under naive,
                                        topic-clustered, HC0 (and GEE / quasi-Poisson / NB2) SEs
  D-04  topic_overlap_factors.csv       overlap factors and the untagged-benchmark count
        topic_overlap_sensitivity.csv   single-primary-topic refits and a benchmark-PMID bootstrap
  B-03  multiplicity_bh.csv             Benjamini-Hochberg within three declared families
  B-01  denominator_correction.csv      158/486 vs 158/489 with Wilson intervals
  B-06  verified_fraction_bounds.csv    what the verified-fraction interval actually permits
  D-08  supporting_sensitivity.csv      title-query recall stability; non-sc-omics negative control
        title_query_recall_by_year.csv, negative_control_by_year.csv, supporting_sensitivity.png
  D-07  problem_period_counts.csv       absolute positives per period
        composition_shift_by_year.csv, composition_confound_tests.csv
  B-09  update_calibration_audit.csv    what the shipped files can and cannot verify
        per_topic_calibration_errors.csv

Usage:  python 03b_statistics_revision_2026-11-01.py
"""
import os
import re
import sys
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy.stats import binomtest
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.proportion import proportion_confint

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from coding_prompt import CATEGORIES, EVALUATION_CHECKS  # noqa: E402

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
IN = os.path.join(ROOT, "code", "data", "raw_inputs")
S7U = os.path.join(ROOT, "supplementary", "S7_statistics", "update_2026-10-15")
OUT = os.path.join(ROOT, "supplementary", "S7_statistics", "revision_2026-11-01")
os.makedirs(OUT, exist_ok=True)

rd = lambda n: pd.read_csv(os.path.join(IN, n))  # noqa: E731
SEED_ASSIGN, SEED_BOOT, N_ASSIGN, N_BOOT = 20261101, 42, 200, 1000


def ex(m, t):
    ci = np.exp(m.conf_int().loc[t])
    return float(np.exp(m.params[t])), float(ci.iloc[0]), float(ci.iloc[1]), float(m.pvalues[t])


def ratio(m):
    n = list(m.params.index)
    L = np.zeros(len(n))
    L[n.index("yc_m")] = 1
    L[n.index("yc_b")] = -1
    td = m.t_test(L)
    ci = td.conf_int()[0]
    return float(np.exp(td.effect[0])), float(np.exp(ci[0])), float(np.exp(ci[1])), float(td.pvalue)


# ------------------------------------------------------------------ inputs
ti = rd("topic_inputs.csv")
ti["logoff"] = np.log(ti.papers_23_26)
ti["logoff15"] = np.log(ti.papers_15_26)
vol = rd("pubmed_volume_long.csv")
volp = vol[vol.topic != "__SUBFIELD_TOTAL__"].pivot(index="topic", columns="year", values="count")
bdf = rd("benchmark_pmids_year_topics.csv")
bx = bdf.assign(topic=bdf.topics.str.split("|")).explode("topic")
bx = bx[bx.year.between(2015, 2026)]
by_ty = bx.groupby(["topic", "year"]).size()
P = pd.DataFrame([dict(topic=t, year=y, papers=int(volp.loc[t, y]), bench=int(by_ty.get((t, y), 0)))
                  for t in ti.topic for y in range(2015, 2027)])
P = P[P.papers > 0].merge(ti[["topic", "method"]], on="topic")
P["yc"] = P.year - 2020
P["lo"] = np.log(P.papers)
Pn = P[P.topic != "benchmarking"].copy()
Pn["yc_m"] = Pn.yc * Pn.method
Pn["yc_b"] = Pn.yc * (1 - Pn.method)

ty = rd("yearly_series.csv")
ty["yc"] = ty.year - 2020
ty["lo"] = np.log(ty.subfield_papers)

cod = rd("problem_coding_primary_raw.csv").fillna({"problems": ""})
sy = rd("problem_coding_primary.csv")[["pmid", "year"]].sort_values(["pmid", "year"]).drop_duplicates("pmid", keep="first")
cod = cod.merge(sy, on="pmid", validate="one_to_one")
shr = cod.groupby("year").sc_genomics.mean()
BB = rd("benchmark_sc_genomics_flags.csv")

# ------------------------------------------------------------------ B-02: robust SEs
rows = []


def add(model, quantity, est, lo, hi, p, setype, n, ncl=np.nan, note=""):
    rows.append(dict(model=model, quantity=quantity, estimate=est, lower95=lo, upper95=hi,
                     p=p, se_type=setype, n_obs=n, n_clusters=ncl, note=note))


FML = "bench ~ yc_m + yc_b + C(topic)"
PANEL = "topic-year panel, Poisson FE (excl. benchmarking)"
for setype, kw in [("naive model-based", {}),
                   ("cluster-robust (topic)", dict(cov_type="cluster", cov_kwds={"groups": Pn.topic})),
                   ("HC0 robust", dict(cov_type="HC0"))]:
    m = smf.glm(FML, Pn, offset=Pn.lo, family=sm.families.Poisson()).fit(**kw)
    ncl = Pn.topic.nunique() if "cluster" in setype else np.nan
    add(PANEL, "panel biology/application slope (RR/yr)", *ex(m, "yc_b"), setype, len(Pn), ncl)
    add(PANEL, "panel method slope (RR/yr)", *ex(m, "yc_m"), setype, len(Pn), ncl)
    add(PANEL, "panel slope ratio (method/biology)", *ratio(m), setype, len(Pn), ncl)
for setype, kw in [("naive model-based", {}),
                   ("cluster-robust (topic)", dict(cov_type="cluster", cov_kwds={"groups": Pn.topic})),
                   ("HC0 robust", dict(cov_type="HC0"))]:
    m = smf.glm("bench ~ yc + C(topic)", Pn, offset=Pn.lo, family=sm.families.Poisson()).fit(**kw)
    add("topic-year panel, common slope", "panel all-topic slope (RR/yr)", *ex(m, "yc"), setype,
        len(Pn), Pn.topic.nunique() if "cluster" in setype else np.nan)
gee = sm.GEE.from_formula(FML, groups="topic", data=Pn, offset=Pn.lo.values,
                          family=sm.families.Poisson(), cov_struct=sm.cov_struct.Exchangeable()).fit()
add("topic-year panel, GEE exchangeable", "GEE panel biology/application slope (RR/yr)", *ex(gee, "yc_b"), "GEE robust (topic)", len(Pn), Pn.topic.nunique())
add("topic-year panel, GEE exchangeable", "GEE panel method slope (RR/yr)", *ex(gee, "yc_m"), "GEE robust (topic)", len(Pn), Pn.topic.nunique())
add("topic-year panel, GEE exchangeable", "GEE panel slope ratio", *ratio(gee), "GEE robust (topic)", len(Pn), Pn.topic.nunique())

bxs = bdf.merge(BB[["pmid", "sc_genomics"]], on="pmid")
bxs = bxs[bxs.sc_genomics == True].assign(topic=lambda d: d.topics.str.split("|")).explode("topic")  # noqa: E712
by_s = bxs[bxs.year.between(2015, 2026)].groupby(["topic", "year"]).size()
Ps = Pn.copy()
Ps["bench_sc"] = [int(by_s.get((t, y), 0)) for t, y in zip(Ps.topic, Ps.year)]
Ps["lo_sc"] = np.log(Ps.papers * Ps.year.map(shr))
kt = Ps.groupby("topic").bench_sc.sum()
Ps = Ps[Ps.topic.isin(kt[kt > 0].index)]
SCP = "topic-year panel, sc-genomics benchmarks only"
for setype, kw in [("naive model-based", {}),
                   ("cluster-robust (topic)", dict(cov_type="cluster", cov_kwds={"groups": Ps.topic})),
                   ("HC0 robust", dict(cov_type="HC0"))]:
    m = smf.glm("bench_sc ~ yc_m + yc_b + C(topic)", Ps, offset=Ps.lo_sc, family=sm.families.Poisson()).fit(**kw)
    ncl = Ps.topic.nunique() if "cluster" in setype else np.nan
    add(SCP, "sc-restricted panel biology slope (RR/yr)", *ex(m, "yc_b"), setype, len(Ps), ncl)
    add(SCP, "sc-restricted panel method slope (RR/yr)", *ex(m, "yc_m"), setype, len(Ps), ncl)
    add(SCP, "sc-restricted panel slope ratio", *ratio(m), setype, len(Ps), ncl)


def nbfit(df, outcome, term, off, **kw):
    f = f"{outcome} ~ log_share_change + {term}"
    nb = smf.negativebinomial(f, df, offset=df[off]).fit(disp=0, method="bfgs", maxiter=3000)
    return smf.negativebinomial(f, df, offset=df[off]).fit(start_params=nb.params, disp=0,
                                                           method="newton", maxiter=200, **kw)


SPECS = [("full_window", "bench_15_26", "method", False, "logoff15", "NB2 coverage: full window 2015-26, all 26 topics"),
         ("full_window_excl_benchmarking", "bench_15_26", "method", True, "logoff15", "NB2 coverage: full window, excl. benchmarking (25 topics)"),
         ("full_window_alt_excl_benchmarking", "bench_15_26", "method_alt", True, "logoff15", "NB2 coverage: full window, alt classification, excl. benchmarking"),
         ("window_matched_excl_benchmarking", "bench_23_26", "method", True, "logoff", "NB2 coverage: window-matched 2023-26, excl. benchmarking")]
for fit, outc, term, excl, off, label in SPECS:
    df = ti[ti.topic != "benchmarking"] if excl else ti
    fits = [("naive model-based", nbfit(df, outc, term, off)),
            ("HC0 robust", nbfit(df, outc, term, off, cov_type="HC0")),
            ("cluster-robust (topic, singleton clusters)", nbfit(df, outc, term, off, cov_type="cluster", cov_kwds={"groups": df.topic.values}))]
    for tm in [term, "log_share_change"]:
        q = ("method indicator IRR" if tm != "log_share_change" else "log share-change IRR") + f" [{fit}]"
        for setype, m in fits:
            add(label, q, *ex(m, tm), setype, len(df), len(df) if "cluster" in setype else np.nan)

SUBF = "Poisson GLM: benchmarks/yr, offset log(subfield papers), 2015-2026"
for setype, kw in [("naive model-based", {}), ("HC0 robust", dict(cov_type="HC0"))]:
    add(SUBF, "subfield benchmark trend (RR/yr)",
        *ex(smf.glm("verified_benchmarks ~ yc", ty, offset=ty.lo, family=sm.families.Poisson()).fit(**kw), "yc"), setype, len(ty))
pois_base = smf.glm("verified_benchmarks ~ yc", ty, offset=ty.lo, family=sm.families.Poisson()).fit()
add("Poisson GLM: benchmarks/yr (quasi-Poisson, Pearson scale)", "subfield benchmark trend (RR/yr)",
    *ex(smf.glm("verified_benchmarks ~ yc", ty, offset=ty.lo, family=sm.families.Poisson()).fit(scale="X2"), "yc"),
    "quasi-Poisson scaled", len(ty), np.nan, f"Pearson chi2/df={pois_base.pearson_chi2 / pois_base.df_resid:.3f}")
nb = smf.negativebinomial("verified_benchmarks ~ yc", ty, offset=ty.lo).fit(disp=0, maxiter=500)
add("NB2: benchmarks/yr, offset log(subfield papers)", "subfield benchmark trend (RR/yr)", *ex(nb, "yc"),
    "NB2 model-based", len(ty), np.nan, f"alpha={float(nb.params['alpha']):.4f}")
t25 = ty[ty.year <= 2025]
for setype, kw in [("naive model-based", {}), ("HC0 robust", dict(cov_type="HC0"))]:
    add("Poisson GLM: benchmarks/yr, 2015-2025 only", "subfield benchmark trend 2015-2025 (RR/yr)",
        *ex(smf.glm("verified_benchmarks ~ yc", t25, offset=t25.lo, family=sm.families.Poisson()).fit(**kw), "yc"), setype, len(t25))
    add("Poisson GLM: evaluation-titled/yr, offset log(subfield papers)", "evaluation-titled trend (RR/yr)",
        *ex(smf.glm("eval_titled ~ yc", ty, offset=ty.lo, family=sm.families.Poisson()).fit(**kw), "yc"), setype, len(ty))
    add("Binomial GLM: verified fraction of evaluation-titled", "verified-fraction trend (OR/yr)",
        *ex(smf.glm("verified_benchmarks + I(eval_titled - verified_benchmarks) ~ yc", ty, family=sm.families.Binomial()).fit(**kw), "yc"), setype, len(ty))
REF = pd.DataFrame(rows)
REF.to_csv(os.path.join(OUT, "robust_se_refits.csv"), index=False)


def pick(d, quantity, se="naive model-based", col="p"):
    r = REF[(REF.quantity == quantity) & (REF.se_type == se) & (REF.model.str.contains(d, regex=False))]
    assert len(r) == 1, (d, quantity, len(r))
    return float(r[col].iloc[0])


# ------------------------------------------------------------------ D-04: overlap
T2 = pd.read_csv(os.path.join(ROOT, "tables", "Table2_coverage.csv"))
ntag = bdf.topics.fillna("").apply(lambda s: 0 if s == "" else len(s.split("|")))
ovl = [dict(statistic="sum of topic paper counts 2015-2026 (Table 2)", value=int(T2.papers_15_26.sum())),
       dict(statistic="subfield papers 2015-2026 (yearly_series.csv)", value=int(ty.subfield_papers.sum())),
       dict(statistic="paper overlap factor", value=round(T2.papers_15_26.sum() / ty.subfield_papers.sum(), 4)),
       dict(statistic="sum of topic benchmark counts 2015-2026 (Table 2)", value=int(T2.bench_15_26.sum())),
       dict(statistic="unique benchmarks 2015-2026", value=int(ty.verified_benchmarks.sum())),
       dict(statistic="benchmark overlap factor", value=round(T2.bench_15_26.sum() / ty.verified_benchmarks.sum(), 4)),
       dict(statistic="benchmarks in catalogue (all years)", value=len(bdf)),
       dict(statistic="benchmarks carrying no topic tag", value=int((ntag == 0).sum())),
       dict(statistic="mean topic tags per benchmark (all 158)", value=round(float(ntag.mean()), 4)),
       dict(statistic="mean topic tags per tagged benchmark (126)", value=round(float(ntag[ntag > 0].mean()), 4))]
ovl += [dict(statistic=f"benchmarks with exactly {k} topic tag(s)", value=int(v)) for k, v in ntag.value_counts().sort_index().items()]
pd.DataFrame(ovl).to_csv(os.path.join(OUT, "topic_overlap_factors.csv"), index=False)

tsize = ti.set_index("topic").papers_15_26.to_dict()
tagged = bdf[bdf.topics.notna() & (bdf.topics != "")].copy()
tagged["tags"] = tagged.topics.str.split("|")
rng = np.random.default_rng(SEED_ASSIGN)


def pick_topic(tags, rule):
    tags = [t for t in tags if t in tsize]
    if rule == "rarest":
        return min(tags, key=lambda t: tsize[t])
    if rule == "largest":
        return max(tags, key=lambda t: tsize[t])
    return rng.choice(tags)


def refit_primary(assign_map):
    a = pd.DataFrame({"pmid": list(assign_map), "topic": list(assign_map.values())}).merge(bdf[["pmid", "year"]], on="pmid")
    a = a[a.year.between(2015, 2026)]
    tt = ti.copy()
    tt["bench_p"] = tt.topic.map(a.groupby("topic").size()).fillna(0).astype(int)
    d = tt[tt.topic != "benchmarking"]
    nb_ = smf.negativebinomial("bench_p ~ log_share_change + method", d, offset=d.logoff15).fit(disp=0, method="bfgs", maxiter=3000)
    nb_ = smf.negativebinomial("bench_p ~ log_share_change + method", d, offset=d.logoff15).fit(start_params=nb_.params, disp=0, method="newton", maxiter=200)
    g = a.groupby(["topic", "year"]).size()
    Q = Pn.copy()
    Q["benchp"] = [int(g.get((t, y), 0)) for t, y in zip(Q.topic, Q.year)]
    m = smf.glm("benchp ~ yc_m + yc_b + C(topic)", Q, offset=Q.lo, family=sm.families.Poisson()).fit()
    return ex(nb_, "method"), ex(m, "yc_b"), ex(m, "yc_m"), ratio(m)


sens = []


def addsens(an, q, est, lo, hi, p, n=np.nan, note=""):
    sens.append(dict(analysis=an, quantity=q, estimate=est, lower95=lo, upper95=hi, p=p, n=n, note=note))


IRRQ = "NB2 method IRR, full window excl. benchmarking"
PUB = "published (overlapping topic tags)"
_pubnb = nbfit(ti[ti.topic != "benchmarking"], "bench_15_26", "method", "logoff15")
addsens(PUB, IRRQ, *ex(_pubnb, "method"), 25, "270 topic-benchmark rows over 157 unique benchmarks")
_pubg = smf.glm(FML, Pn, offset=Pn.lo, family=sm.families.Poisson()).fit()
addsens(PUB, "panel biology slope", *ex(_pubg, "yc_b"), len(Pn), "naive Poisson SEs")
addsens(PUB, "panel method slope", *ex(_pubg, "yc_m"), len(Pn), "")
addsens(PUB, "panel slope ratio", *ratio(_pubg), len(Pn), "")
LAB = {"rarest": "single primary topic = rarest tag (smallest 2015-26 topic volume)",
       "largest": "single primary topic = commonest tag (largest 2015-26 topic volume)"}
for rule in ["rarest", "largest"]:
    irr, bio, meth, rat = refit_primary({r.pmid: pick_topic(r.tags, rule) for r in tagged.itertuples()})
    addsens(LAB[rule], IRRQ, *irr, 25, "126 tagged benchmarks, one topic each")
    addsens(LAB[rule], "panel biology slope", *bio, len(Pn), "")
    addsens(LAB[rule], "panel method slope", *meth, len(Pn), "")
    addsens(LAB[rule], "panel slope ratio", *rat, len(Pn), "")
rand = []
for _ in range(N_ASSIGN):
    try:
        r4 = refit_primary({r.pmid: pick_topic(r.tags, "random") for r in tagged.itertuples()})
        rand.append([r4[k][j] for k in range(4) for j in (0, 3)])
    except Exception:
        pass
RA = pd.DataFrame(rand, columns=["IRR", "IRR_p", "bio", "bio_p", "meth", "meth_p", "ratio", "ratio_p"])
RLAB = f"single primary topic = uniform random draw ({N_ASSIGN} replicates)"
for q, vc, pc in [(IRRQ, "IRR", "IRR_p"), ("panel biology slope", "bio", "bio_p"),
                  ("panel method slope", "meth", "meth_p"), ("panel slope ratio", "ratio", "ratio_p")]:
    v = RA[vc].replace([np.inf, -np.inf], np.nan).dropna()
    addsens(RLAB, q, float(v.median()), float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5)), np.nan, len(v),
            f"interval is the 2.5-97.5 percentile across assignment draws, not a sampling CI; "
            f"{float((RA[pc] < 0.05).mean()):.3f} of draws gave p<0.05")

pm = bdf[bdf.year.between(2015, 2026)].reset_index(drop=True)
rng2 = np.random.default_rng(SEED_BOOT)
boot = []
for _ in range(N_BOOT):
    s = pm.iloc[rng2.integers(0, len(pm), len(pm))]
    sx = s.assign(topic=s.topics.fillna("").str.split("|")).explode("topic")
    sx = sx[sx.topic.isin(tsize)]
    tt = ti.copy()
    tt["bp"] = tt.topic.map(sx.groupby("topic").size()).fillna(0).astype(int)
    d = tt[tt.topic != "benchmarking"]
    try:
        nb_ = smf.negativebinomial("bp ~ log_share_change + method", d, offset=d.logoff15).fit(disp=0, method="bfgs", maxiter=3000)
        nb_ = smf.negativebinomial("bp ~ log_share_change + method", d, offset=d.logoff15).fit(start_params=nb_.params, disp=0, method="newton", maxiter=200)
        irr, shr_ = float(np.exp(nb_.params["method"])), float(np.exp(nb_.params["log_share_change"]))
    except Exception:
        irr = shr_ = np.nan
    g = sx.groupby(["topic", "year"]).size()
    Q = Pn.copy()
    Q["bp"] = [int(g.get((t, y), 0)) for t, y in zip(Q.topic, Q.year)]
    try:
        m = smf.glm("bp ~ yc_m + yc_b + C(topic)", Q, offset=Q.lo, family=sm.families.Poisson()).fit()
        bio, met = float(np.exp(m.params["yc_b"])), float(np.exp(m.params["yc_m"]))
        rat = met / bio
    except Exception:
        bio = met = rat = np.nan
    boot.append((irr, shr_, bio, met, rat))
BO = pd.DataFrame(boot, columns=["IRR", "share_IRR", "bio", "meth", "ratio"])
BLAB = f"nonparametric bootstrap over the 157 benchmark PMIDs ({N_BOOT:,} replicates)"
for q, c in [(IRRQ, "IRR"), ("NB2 log share-change IRR", "share_IRR"), ("panel biology slope", "bio"),
             ("panel method slope", "meth"), ("panel slope ratio", "ratio")]:
    v = BO[c].replace([np.inf, -np.inf], np.nan).dropna()
    addsens(BLAB, q, float(v.median()), float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5)),
            2 * min(float((v > 1).mean()), float((v < 1).mean())), len(v),
            "percentile CI; p is the two-sided bootstrap p against the null of 1")
pd.DataFrame(sens).to_csv(os.path.join(OUT, "topic_overlap_sensitivity.csv"), index=False)

# ------------------------------------------------------------------ B-03: multiplicity
early, late = ty[ty.year <= 2020], ty[ty.year >= 2023]
bt = binomtest(int(late.verified_benchmarks.sum()),
               int(late.verified_benchmarks.sum() + early.verified_benchmarks.sum()),
               late.subfield_papers.sum() / (late.subfield_papers.sum() + early.subfield_papers.sum()))
famA = [("NB2 coverage, window-matched 2023-26, excl. benchmarking: method IRR", pick("window-matched", "method indicator IRR [window_matched_excl_benchmarking]")),
        ("NB2 coverage, full window, excl. benchmarking: method IRR (2.35)", pick("full window, excl", "method indicator IRR [full_window_excl_benchmarking]")),
        ("Poisson: evaluation-titled per subfield paper, trend (RR 0.940)", pick("evaluation-titled/yr", "evaluation-titled trend (RR/yr)")),
        ("NB2 coverage, full window, all 26 topics: method IRR (4.84)", pick("full window 2015-26", "method indicator IRR [full_window]")),
        ("Poisson: benchmarks per 1,000 subfield papers, trend 2015-2026 (RR 0.922)", pick("2015-2026", "subfield benchmark trend (RR/yr)")),
        ("Panel: biology/application year slope (RR 0.901)", pick("Poisson FE", "panel biology/application slope (RR/yr)")),
        ("NB2 coverage, full window, alt classification, excl. benchmarking: method IRR (1.88)", pick("alt classification", "method indicator IRR [full_window_alt_excl_benchmarking]")),
        ("Exact conditional rate comparison 2023-26 vs 2015-20", float(bt.pvalue)),
        ("sc-restricted panel: biology year slope (RR 0.882)", pick("sc-genomics benchmarks only", "sc-restricted panel biology slope (RR/yr)")),
        ("Poisson: benchmark trend 2015-2025 only (RR 0.930)", pick("2015-2025 only", "subfield benchmark trend 2015-2025 (RR/yr)")),
        ("Panel: slope ratio method/biology (1.12)", pick("Poisson FE", "panel slope ratio (method/biology)")),
        ("sc-genomics sensitivity: benchmark trend 2015-2026 (RR 0.920)", float(pd.read_csv(os.path.join(ROOT, "code", "outputs", "sc_genomics_sensitivity.csv")).p.iloc[0])),
        ("sc-restricted panel: slope ratio", pick("sc-genomics benchmarks only", "sc-restricted panel slope ratio")),
        ("NB2 coverage, full window, excl. benchmarking: log share-change IRR (0.79)", pick("full window, excl", "log share-change IRR [full_window_excl_benchmarking]")),
        ("NB2 coverage, window-matched, excl. benchmarking: log share-change IRR (0.77)", pick("window-matched", "log share-change IRR [window_matched_excl_benchmarking]")),
        ("Binomial: verified fraction of evaluation-titled, trend (OR 0.973)", pick("verified fraction", "verified-fraction trend (OR/yr)")),
        ("Panel: method-topic year slope (RR 1.012)", pick("Poisson FE", "panel method slope (RR/yr)"))]
A = pd.DataFrame(famA, columns=["test", "p"]).sort_values("p").reset_index(drop=True)
T3 = pd.read_csv(os.path.join(ROOT, "tables", "Table3_problem_types.csv"))
B = T3[["problem_type", "OR_per_year", "OR_lo", "OR_hi", "p"]].sort_values("p").reset_index(drop=True)
B = B.rename(columns={"problem_type": "test"})
B["test"] = "Table 3 OR/yr: " + B["test"]
PP = pd.read_csv(os.path.join(ROOT, "code", "outputs", "problem_prevalence.csv")).set_index("problem_type")
C = pd.DataFrame([("any evaluation-check problem, OR/yr (0.808)", PP.loc["any_check"].p),
                  ("any methodological problem, OR/yr", PP.loc["any_problem"].p)],
                 columns=["test", "p"]).sort_values("p").reset_index(drop=True)
fams = []
for name, fr in [("A: primary model tests (17)", A), ("B: Table 3 per-year odds ratios (17)", B),
                 ("C: section 3.3 headline abstract-level trend models (2)", C)]:
    fr = fr.copy()
    fr.insert(0, "family", name)
    fr["rank"] = np.arange(1, len(fr) + 1)
    fr["q_BH"] = multipletests(fr.p, method="fdr_bh")[1]
    fr["p_bonferroni"] = np.minimum(fr.p * len(fr), 1)
    fams.append(fr)
MU = pd.concat(fams, ignore_index=True)
MU["significant_unadjusted_0.05"] = MU.p < 0.05
MU["significant_BH_0.05"] = MU.q_BH < 0.05
MU["significant_bonferroni_0.05"] = MU.p_bonferroni < 0.05
MU.to_csv(os.path.join(OUT, "multiplicity_bh.csv"), index=False)

# ------------------------------------------------------------------ B-01 / B-06
den = []
for lab, k, n in [("published: 158 of 486 (4 Oct 2026 snapshot)", 158, 486),
                  ("corrected: 158 of 489 (486 at 4 Oct + 3 indexed 5-15 Oct)", 158, 489),
                  ("2015-2026 series only: 158 of 487", 158, 487)]:
    lo, hi = proportion_confint(k, n, method="wilson")
    den.append(dict(label=lab, k=k, n=n, pct=k / n * 100, wilson_lo=lo * 100, wilson_hi=hi * 100))
pd.DataFrame(den).to_csv(os.path.join(OUT, "denominator_correction.csv"), index=False)
assert int(ty.eval_titled.sum()) == 487, "eval_titled 2015-2026 no longer sums to 487"

orv, lo_, hi_, p_ = ex(smf.glm("verified_benchmarks + I(eval_titled - verified_benchmarks) ~ yc", ty, family=sm.families.Binomial()).fit(), "yc")
f15 = ty.loc[ty.year == 2015, "verified_benchmarks"].iloc[0] / ty.loc[ty.year == 2015, "eval_titled"].iloc[0]
o15 = f15 / (1 - f15)
pd.DataFrame([dict(quantity="verified fraction of evaluation-titled papers, OR per year", estimate=orv, lower95=lo_, upper95=hi_, p=p_),
              dict(quantity="cumulative odds change 2015->2026 (11 year-steps)", estimate=orv ** 11, lower95=lo_ ** 11, upper95=hi_ ** 11, p=np.nan),
              dict(quantity="implied 2026 yield (%) anchored at the 2015 observed 4/12 = 33.3%",
                   estimate=100 * (o15 * orv ** 11) / (1 + o15 * orv ** 11),
                   lower95=100 * (o15 * lo_ ** 11) / (1 + o15 * lo_ ** 11),
                   upper95=100 * (o15 * hi_ ** 11) / (1 + o15 * hi_ ** 11), p=np.nan)]
             ).to_csv(os.path.join(OUT, "verified_fraction_bounds.csv"), index=False)

# ------------------------------------------------------------------ D-07 / D-08
S1 = pd.read_csv(os.path.join(ROOT, "supplementary", "S1_benchmark_catalogue.csv"))
pat = re.compile(r"benchmark|comparison|evaluation|assessment", re.I)
S1c = S1.assign(hit=S1.title.fillna("").apply(lambda s: int(bool(pat.search(s)))))
Sr = S1c[S1c.year.between(2015, 2026)].copy()
Sr["yc"] = Sr.year - 2020
mr = smf.glm("hit ~ yc", Sr, family=sm.families.Binomial()).fit()
byy = Sr.groupby("year").hit.agg(k="sum", n="count")
byy["recall"] = byy.k / byy.n
byy.to_csv(os.path.join(OUT, "title_query_recall_by_year.csv"))

PC = pd.read_csv(os.path.join(S7U, "problem_coding_2015_2026.csv"))
PC["any_check"] = (PC[EVALUATION_CHECKS].sum(axis=1) > 0).astype(int)
PC["yc"] = PC.year - 2020
PC["abslen"] = PC.abstract.fillna("").str.len()
PC["period"] = pd.cut(PC.year, [2014, 2018, 2021, 2023, 2026], labels=["2015-18", "2019-21", "2022-23", "2024-26"])
sup = [dict(analysis="Title-query recall among the benchmark catalogue", quantity="recall, all 269 catalogue records",
            k=int(S1c.hit.sum()), n=len(S1c), estimate=float(S1c.hit.mean()), lower95=np.nan, upper95=np.nan, p=np.nan,
            note="title contains benchmark|comparison|evaluation|assessment (case-insensitive)")]
lo, hi = proportion_confint(int(Sr.hit.sum()), len(Sr), method="wilson")
sup.append(dict(analysis="Title-query recall among the benchmark catalogue", quantity="recall, 2015-2026 records",
                k=int(Sr.hit.sum()), n=len(Sr), estimate=float(Sr.hit.mean()), lower95=lo, upper95=hi, p=np.nan, note="Wilson interval"))
e = ex(mr, "yc")
sup.append(dict(analysis="Title-query recall among the benchmark catalogue", quantity="logistic recall ~ year, OR per year",
                k=int(Sr.hit.sum()), n=len(Sr), estimate=e[0], lower95=e[1], upper95=e[2], p=e[3],
                note="no detectable time trend in recall; conditional on catalogue membership (see caveat)"))
for lab, mask in [("single-cell-omics abstracts", PC.sc_genomics == True),  # noqa: E712
                  ("non-single-cell-omics abstracts (negative control)", PC.sc_genomics != True)]:  # noqa: E712
    s = PC[mask]
    e = ex(smf.glm("any_check ~ yc", s, family=sm.families.Binomial()).fit(), "yc")
    sup.append(dict(analysis="Negative control: evaluation-check share by year", quantity=f"{lab}: OR per year",
                    k=int(s.any_check.sum()), n=len(s), estimate=e[0], lower95=e[1], upper95=e[2], p=e[3],
                    note="logistic GLM, any evaluation-check problem ~ year centred 2020"))
for per_, v in PC.groupby("period", observed=True).abslen.median().items():
    sup.append(dict(analysis="Abstract length over the window", quantity=f"median abstract length, {per_} (characters)",
                    k=np.nan, n=int((PC.period == per_).sum()), estimate=float(v), lower95=np.nan, upper95=np.nan,
                    p=np.nan, note="all 1,771 sampled abstracts"))
G = PC[PC.sc_genomics == True].copy()  # noqa: E712
G["is_review"] = G.ptypes.fillna("").str.contains("Review").astype(int)
G["is_rsnih"] = G.ptypes.fillna("").str.contains("Research Support").astype(int)
G["n_ptypes"] = G.ptypes.fillna("").apply(lambda s: len([x for x in s.split(";") if x]))
ea = ex(smf.glm("any_check ~ yc + abslen", G, family=sm.families.Binomial()).fit(), "yc")
sup.append(dict(analysis="Abstract length over the window", quantity="sc-omics evaluation-check OR per year, adjusted for abstract length",
                k=int(G.any_check.sum()), n=len(G), estimate=ea[0], lower95=ea[1], upper95=ea[2], p=ea[3],
                note="unadjusted OR 0.8077; adjustment does not attenuate"))
pd.DataFrame(sup).to_csv(os.path.join(OUT, "supporting_sensitivity.csv"), index=False)
nc_year = PC.groupby(["year", "sc_genomics"]).any_check.agg(k="sum", n="count").reset_index()
nc_year["pct"] = nc_year.k / nc_year.n * 100
nc_year.to_csv(os.path.join(OUT, "negative_control_by_year.csv"), index=False)

per = G.groupby("period", observed=True).agg(n=("any_check", "size"), k_check=("any_check", "sum"), k_prob=("any_problem", "sum"))
per["pct_check"] = per.k_check / per.n * 100
per["pct_prob"] = per.k_prob / per.n * 100
lo, hi = proportion_confint(per.k_check, per.n, method="wilson")
per["check_lo"], per["check_hi"] = lo * 100, hi * 100
shr_y = PC.groupby("year").sc_genomics.mean() * 100
p7 = per.reset_index().rename(columns={"n": "n_sc_omics_abstracts", "k_check": "positives_any_evaluation_check", "k_prob": "positives_any_problem"})
p7["sc_omics_share_pct_first_year"] = [shr_y.loc[y] for y in [2015, 2019, 2022, 2024]]
p7["sc_omics_share_pct_last_year"] = [shr_y.loc[y] for y in [2018, 2021, 2023, 2026]]
p7.to_csv(os.path.join(OUT, "problem_period_counts.csv"), index=False)
pd.DataFrame({"year": shr_y.index, "sc_omics_share_pct": shr_y.values,
              "n_drawn": PC.groupby("year").size().values}).to_csv(os.path.join(OUT, "composition_shift_by_year.csv"), index=False)
comp = []
for lab, f, s in [("unadjusted (published)", "any_check ~ yc", G),
                  ("adjusted for abstract length", "any_check ~ yc + abslen", G),
                  ("adjusted for publication-type covariates", "any_check ~ yc + is_review + is_rsnih + n_ptypes", G),
                  ("adjusted for length and publication type", "any_check ~ yc + abslen + is_review + is_rsnih + n_ptypes", G),
                  ("restricted to 2019-2026 (sc-omics share >=39%)", "any_check ~ yc", G[G.year >= 2019]),
                  ("restricted to 2021-2026 (sc-omics share >=69%)", "any_check ~ yc", G[G.year >= 2021])]:
    e = ex(smf.glm(f, s, family=sm.families.Binomial()).fit(), "yc")
    comp.append(dict(model=lab, formula=f, n=len(s), positives=int(s.any_check.sum()),
                     OR_per_year=e[0], lower95=e[1], upper95=e[2], p=e[3]))
pd.DataFrame(comp).to_csv(os.path.join(OUT, "composition_confound_tests.csv"), index=False)

# ------------------------------------------------------------------ B-09
UL = pd.read_csv(os.path.join(S7U, "update_log_2026-10-15.csv"))
UL["ratio_recomp"] = UL.count_2026_on_2026_10_15 / UL.count_2026_edat_to_2026_10_04
UL["updated_recomp"] = np.round(UL.archived_2026 * UL.growth_ratio)
srow = UL[UL.series == "__SUBFIELD_TOTAL__"].iloc[0]
cal = UL[UL.series != "__SUBFIELD_TOTAL__"][["series", "calibration_mean_abs_log_error_2017_2021_2025"]].sort_values(
    "calibration_mean_abs_log_error_2017_2021_2025", ascending=False)
cal = cal.rename(columns={"calibration_mean_abs_log_error_2017_2021_2025": "mean_abs_log_error_2017_2021_2025"})
cal["implied_factor"] = np.exp(cal.mean_abs_log_error_2017_2021_2025)
cal.to_csv(os.path.join(OUT, "per_topic_calibration_errors.csv"), index=False)
aud = [dict(claim="updated_2026 = round(archived_2026 x growth_ratio)", checkable="yes", result=f"{int((UL.updated_recomp == UL.updated_2026).sum())}/27 series exact"),
       dict(claim="growth_ratio = 15 Oct count / 4 Oct count", checkable="yes", result="reproduces for all 27 series" if np.allclose(UL.ratio_recomp, UL.growth_ratio) else "DOES NOT reproduce"),
       dict(claim="growth ratios ranged 1.014 to 1.064", checkable="yes", result=f"recomputed range {UL.growth_ratio.min():.4f}-{UL.growth_ratio.max():.4f}"),
       dict(claim="subfield ratio 1.031; 7,342 -> 7,571", checkable="yes", result=f"recomputed {srow.growth_ratio:.4f}; {int(srow.archived_2026)} -> {int(srow.updated_2026)}"),
       dict(claim="three evaluation-titled 2026 records indexed after 4 Oct, none a benchmark", checkable="yes", result="new_evaluation_titled_2026-10-05_to_15.csv lists 3 records, all is_benchmark=False"),
       dict(claim="reconstructed query reproduced every year 2015-2025 within +-0.7%", checkable="no", result="per-year reconstructed counts are not in the released package; cannot be checked"),
       dict(claim="example 442 versus 443 records in 2015", checkable="no", result="no file contains a reconstructed 2015 count; the only '442' in the package is an unrelated sample size"),
       dict(claim="example 7,528 versus 7,556 in 2025", checkable="no", result="the string 7528 / 7,528 does not occur anywhere in supplementary/ or code/"),
       dict(claim="per-topic clause selected as the best of two or three candidates on 2017/2021/2025", checkable="partly", result="only the resulting mean absolute log error is released, not the candidate clauses or their counts"),
       dict(claim="subfield calibration error", checkable="no", result="calibration_mean_abs_log_error_2017_2021_2025 is NaN for __SUBFIELD_TOTAL__ in the released log"),
       dict(claim="per-topic calibration quality", checkable="yes",
            result=f"released for all 26 topics; median {cal.mean_abs_log_error_2017_2021_2025.median():.3f}, "
                   f"worst {cal.mean_abs_log_error_2017_2021_2025.max():.3f} ({cal.series.iloc[0]}, factor {cal.implied_factor.iloc[0]:.2f}x); "
                   f"{int((cal.mean_abs_log_error_2017_2021_2025 > 0.2).sum())} of 26 topics exceed 0.2")]
pd.DataFrame(aud).to_csv(os.path.join(OUT, "update_calibration_audit.csv"), index=False)

# ------------------------------------------------------------------ figure (D-08)
import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

plt.rcParams.update({"font.size": 8, "axes.labelsize": 8, "xtick.labelsize": 6, "ytick.labelsize": 6,
                     "axes.spines.top": False, "axes.spines.right": False, "savefig.bbox": None})
fig, axs = plt.subplots(1, 2, figsize=(7.2, 3.0))
ax = axs[0]
lo_r, hi_r = proportion_confint(byy.k.values, byy.n.values, method="wilson")
ax.errorbar(byy.index.values, byy.recall.values * 100,
            yerr=[(byy.recall.values - lo_r) * 100, (hi_r - byy.recall.values) * 100],
            fmt="o", ms=4, lw=0.9, capsize=2, color="#1f4e79", zorder=3)
xs = np.linspace(2015, 2026, 100)
ax.plot(xs, mr.predict(pd.DataFrame({"yc": xs - 2020})) * 100, color="#c0504d", lw=1.4, zorder=2)
ax.axhline(float(Sr.hit.mean()) * 100, ls=":", lw=0.8, color="#8c8c8c", zorder=1)
ax.set_xlabel("Publication year")
ax.set_ylabel("Catalogue records whose title\nmatches the query (%)")
ax.set_xticks([2015, 2020, 2025])
ax.set_ylim(40, 112)
ax.set_xlim(2014.3, 2026.7)
ax.text(2015.0, 45, "OR 1.042 per year (0.929–1.170), p = 0.48", fontsize=6, color="#c0504d")
ax = axs[1]
for flag, col, lab in [(True, "#1f4e79", "single-cell omics"), (False, "#8c8c8c", "not single-cell omics")]:
    s = nc_year[nc_year.sc_genomics == flag].sort_values("year")
    ax.plot(s.year, s.pct, "o-", ms=3.5, lw=1.2, color=col, zorder=3 if flag else 2)
    ax.text(2026.3, float(s[s.year == 2026].pct.iloc[0]), lab, color=col, fontsize=6, va="center")
ax.set_xlabel("Publication year")
ax.set_ylabel("Abstracts stating an\nevaluation-check problem (%)")
ax.set_xticks([2015, 2020, 2025])
ax.set_xlim(2014.3, 2031.5)
ax.set_ylim(-1.5, 36)
ax.text(2014.8, 33.0, "OR 0.808 per year (0.74–0.88), p < 0.0001", fontsize=6, color="#1f4e79")
ax.text(2014.8, 30.0, "OR 1.066 per year (0.96–1.18), p = 0.23", fontsize=6, color="#8c8c8c")
for a, letter in zip(axs, "ab"):
    a.text(-0.20, 1.04, letter, transform=a.transAxes, fontsize=10, fontweight="bold", va="bottom", ha="left")
fig.subplots_adjust(left=0.115, right=0.985, bottom=0.17, top=0.93, wspace=0.42)
fig.savefig(os.path.join(OUT, "supporting_sensitivity.png"), dpi=300)
fig.savefig(os.path.join(OUT, "supporting_sensitivity.pdf"))
plt.close(fig)

print("revision outputs written to", OUT)
for k, v in [("panel biology clustered p", pick("Poisson FE", "panel biology/application slope (RR/yr)", "cluster-robust (topic)")),
             ("panel ratio clustered p", pick("Poisson FE", "panel slope ratio (method/biology)", "cluster-robust (topic)")),
             ("slope-ratio BH q", float(MU[MU.test.str.startswith("Panel: slope ratio")].q_BH.iloc[0])),
             ("clinical-translation BH q", float(MU[MU.test == "Table 3 OR/yr: clinical_translation"].q_BH.iloc[0]))]:
    print(f"  {k}: {v:.4f}")
