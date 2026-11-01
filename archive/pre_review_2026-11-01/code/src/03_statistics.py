"""Step 3 - all statistical models reported in the manuscript, from the shipped inputs.

Runs offline from data/raw_inputs/ and writes outputs/*.csv. Reproduces Methods 2.8:

  A. Yearly benchmark coverage trend (Poisson / NB2 / binomial GLMs; exact
     conditional comparison 2023-26 vs 2015-20).                     -> trend_tests.csv
  B. Topic-level coverage models, NB2 with log(topic papers) offset, for the
     2023-2026 window and the full 2015-2026 window.               -> topic_coverage_models.csv
  C. Topic-year panel: Poisson GLM with topic fixed effects and separate year
     slopes for method and biology/application topics.            -> topic_year_panel.csv
  D. Single-cell-genomics sensitivity analyses (denominator scaled by the
     sampled single-cell-omics share; benchmarks restricted to sc genomics).
                                                                 -> sc_genomics_sensitivity.csv
  E. Stated-problem prevalence (Wilson CIs) and per-year logistic trends among
     abstracts that use single-cell omics data; period summaries.   -> problem_prevalence.csv, problem_periods.csv
  F. Agreement between the primary and second model coders (Cohen's kappa).
                                                                 -> coder_agreement.csv
  G. Per-topic benchmark rates per 1,000 papers with exact Poisson CIs.
                                                                 -> topic_rates.csv
Finally compares the recomputed values with the values printed in the
manuscript (data/expected_values.csv)                           -> reproduction_check.csv

Usage:  python 03_statistics.py
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))

import os

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy.stats import binomtest, chi2
from statsmodels.stats.proportion import proportion_confint

from coding_prompt import CATEGORIES, EVALUATION_CHECKS

HERE = os.path.dirname(os.path.abspath(__file__))
IN = os.path.join(HERE, "..", "data", "raw_inputs")
OUT = os.path.join(HERE, "..", "outputs")
os.makedirs(OUT, exist_ok=True)


def rd(name):
    return pd.read_csv(os.path.join(IN, name))


def ex(m, term):
    """exp(coef), exp(CI), p for one term of a fitted statsmodels model."""
    ci = np.exp(m.conf_int().loc[term])
    return float(np.exp(m.params[term])), float(ci.iloc[0]), float(ci.iloc[1]), float(m.pvalues[term])


def pois_ci_per1000(k, n):
    lo = 0 if k == 0 else chi2.ppf(0.025, 2 * k) / 2
    hi = chi2.ppf(0.975, 2 * k + 2) / 2
    return lo / n * 1000, hi / n * 1000


R = []  # (key, value) pairs for the reproduction check


def rec(key, v):
    R.append((key, float(v)))


# ---------------------------------------------------------------- A. yearly trend
ty = rd("yearly_series.csv")
ty["yc"] = ty.year - 2020
ty["lo"] = np.log(ty.subfield_papers)


def pois(df, y):
    return smf.glm(f"{y} ~ yc", df, offset=df.lo, family=sm.families.Poisson()).fit()


rows = []
m = pois(ty, "verified_benchmarks"); e = ex(m, "yc")
rows.append(("Poisson GLM: benchmarks ~ year, offset log(subfield papers)", "rate ratio per year", *e[:3], e[3], m.pearson_chi2 / m.df_resid))
rec("trend_poisson_RR", e[0]); rec("trend_poisson_lo", e[1]); rec("trend_poisson_hi", e[2]); rec("trend_poisson_p", e[3])
nbm = smf.negativebinomial("verified_benchmarks ~ yc", ty, offset=ty.lo).fit(disp=0, maxiter=500); e = ex(nbm, "yc")
rows.append(("NB2: benchmarks ~ year, offset log(subfield papers)", "rate ratio per year", *e[:3], e[3], float(nbm.params["alpha"])))
bm = smf.glm("verified_benchmarks + I(subfield_papers - verified_benchmarks) ~ yc", ty, family=sm.families.Binomial()).fit(); e = ex(bm, "yc")
rows.append(("Binomial GLM: benchmarks of subfield papers ~ year", "odds ratio per year", *e[:3], e[3], np.nan))
vf = smf.glm("verified_benchmarks + I(eval_titled - verified_benchmarks) ~ yc", ty, family=sm.families.Binomial()).fit(); e = ex(vf, "yc")
rows.append(("Binomial GLM: verified fraction of evaluation-titled ~ year", "odds ratio per year", *e[:3], e[3], np.nan))
rec("verified_fraction_OR", e[0]); rec("verified_fraction_p", e[3])
ev = pois(ty, "eval_titled"); e = ex(ev, "yc")
rows.append(("Poisson GLM: evaluation-titled ~ year, offset log(subfield papers)", "rate ratio per year", *e[:3], e[3], np.nan))
rec("eval_titled_RR", e[0])
t25 = ty[ty.year <= 2025]; m25 = pois(t25, "verified_benchmarks"); e = ex(m25, "yc")
rows.append(("Poisson GLM 2015-2025 only (exclude partial 2026)", "rate ratio per year", *e[:3], e[3], np.nan))
rec("trend_2015_25_RR", e[0]); rec("trend_2015_25_p", e[3])
early, late = ty[ty.year <= 2020], ty[ty.year >= 2023]
ke, ne, kl, nl = early.verified_benchmarks.sum(), early.subfield_papers.sum(), late.verified_benchmarks.sum(), late.subfield_papers.sum()
bt = binomtest(int(kl), int(kl + ke), nl / (nl + ne))
rows.append(("Exact conditional rate comparison: 2023-26 vs 2015-20", "rate ratio late/early", (kl / nl) / (ke / ne), np.nan, np.nan, bt.pvalue, np.nan))
rec("early_rate_per1000", ke / ne * 1000); rec("late_rate_per1000", kl / nl * 1000); rec("late_early_p", bt.pvalue)
pd.DataFrame(rows, columns=["model", "effect", "estimate", "lower95", "upper95", "p", "dispersion_or_alpha"]).to_csv(os.path.join(OUT, "trend_tests.csv"), index=False)
rec("subfield_papers_2015_2026", ty.subfield_papers.sum()); rec("benchmarks_2015_2026", ty.verified_benchmarks.sum())

# ---------------------------------------------------------------- B. topic coverage models
ti = rd("topic_inputs.csv")
ti["logoff"] = np.log(ti.papers_23_26)
ti["logoff15"] = np.log(ti.papers_15_26)


def nbfit(df, outcome, term, off):
    f = f"{outcome} ~ log_share_change + {term}"
    nb = smf.negativebinomial(f, df, offset=df[off]).fit(disp=0, method="bfgs", maxiter=2000)
    nb = smf.negativebinomial(f, df, offset=df[off]).fit(start_params=nb.params, disp=0, method="newton", maxiter=200)
    po = smf.glm(f, df, offset=df[off], family=sm.families.Poisson()).fit()
    return nb, po


specs = [  # (fit name, outcome, classification term, exclude benchmarking topic, offset)
    ("primary", "true_benchmarks", "method", False, "logoff"),
    ("excl_benchmarking", "true_benchmarks", "method", True, "logoff"),
    ("window_matched_23_26", "bench_23_26", "method", False, "logoff"),
    ("window_matched_excl_benchmarking", "bench_23_26", "method", True, "logoff"),
    ("alt_classification", "true_benchmarks", "method_alt", False, "logoff"),
    ("alt_classification_excl_benchmarking", "true_benchmarks", "method_alt", True, "logoff"),
    ("full_window", "bench_15_26", "method", False, "logoff15"),
    ("full_window_excl_benchmarking", "bench_15_26", "method", True, "logoff15"),
    ("full_window_alt_excl_benchmarking", "bench_15_26", "method_alt", True, "logoff15"),
]
rows = []
for fit, outc, term, excl, off in specs:
    df = ti[ti.topic != "benchmarking"] if excl else ti
    nb, po = nbfit(df, outc, term, off)
    for tm in ["log_share_change", term]:
        e = ex(nb, tm); ep = ex(po, tm)
        rows.append(dict(fit=fit, model="NB2", term=tm, n_topics=len(df), IRR=e[0], IRR_lower95=e[1], IRR_upper95=e[2], p=e[3], alpha=float(nb.params["alpha"])))
        rows.append(dict(fit=fit, model="Poisson", term=tm, n_topics=len(df), IRR=ep[0], IRR_lower95=ep[1], IRR_upper95=ep[2], p=ep[3], alpha=np.nan,
                         pearson_chi2_df=po.pearson_chi2 / po.df_resid))
CMo = pd.DataFrame(rows)
CMo.to_csv(os.path.join(OUT, "topic_coverage_models.csv"), index=False)
for fit, term in [("full_window", "method"), ("full_window_excl_benchmarking", "method"), ("full_window_excl_benchmarking", "log_share_change"),
                  ("full_window_alt_excl_benchmarking", "method_alt"), ("window_matched_excl_benchmarking", "method"),
                  ("window_matched_excl_benchmarking", "log_share_change")]:
    r = CMo[(CMo.fit == fit) & (CMo.model == "NB2") & (CMo.term == term)].iloc[0]
    rec(f"nb2_{fit}_{term}_IRR", r.IRR); rec(f"nb2_{fit}_{term}_lo", r.IRR_lower95); rec(f"nb2_{fit}_{term}_hi", r.IRR_upper95)

# ---------------------------------------------------------------- C. topic-year panel
vol = rd("pubmed_volume_long.csv")
vol = vol[vol.topic != "__SUBFIELD_TOTAL__"].pivot(index="topic", columns="year", values="count")
bdf = rd("benchmark_pmids_year_topics.csv")
bx = bdf.assign(topic=bdf.topics.str.split("|")).explode("topic")
bx = bx[bx.year.between(2015, 2026)]
by_ty = bx.groupby(["topic", "year"]).size()
P = pd.DataFrame([dict(topic=t, year=y, papers=int(vol.loc[t, y]), bench=int(by_ty.get((t, y), 0)))
                  for t in ti.topic for y in range(2015, 2027)])
P = P[P.papers > 0].merge(ti[["topic", "method"]], on="topic")
P["yc"] = P.year - 2020
P["lo"] = np.log(P.papers)
Pn = P[P.topic != "benchmarking"].copy()
Pn["yc_m"] = Pn.yc * Pn.method
Pn["yc_b"] = Pn.yc * (1 - Pn.method)
g1 = smf.glm("bench ~ yc + C(topic)", Pn, offset=Pn.lo, family=sm.families.Poisson()).fit()
g3 = smf.glm("bench ~ yc_m + yc_b + C(topic)", Pn, offset=Pn.lo, family=sm.families.Poisson()).fit()
names = list(g3.params.index)
Lc = np.zeros(len(names)); Lc[names.index("yc_m")] = 1; Lc[names.index("yc_b")] = -1
td = g3.t_test(Lc)
rows = []
for nm, lab in [("yc_m", "method topics"), ("yc_b", "biology/application topics")]:
    e = ex(g3, nm); rows.append(dict(effect=f"year rate ratio, {lab}", estimate=e[0], lower95=e[1], upper95=e[2], p=e[3]))
rows.append(dict(effect="ratio of year effects (method / biology)", estimate=float(np.exp(td.effect[0])),
                 lower95=float(np.exp(td.conf_int()[0][0])), upper95=float(np.exp(td.conf_int()[0][1])), p=float(td.pvalue)))
e = ex(g1, "yc"); rows.append(dict(effect="year rate ratio, all topics (common slope)", estimate=e[0], lower95=e[1], upper95=e[2], p=e[3]))
PANo = pd.DataFrame(rows).assign(n_topic_years=len(Pn), n_benchmarks=int(Pn.bench.sum()), pearson_dispersion=g3.pearson_chi2 / g3.df_resid)
PANo.to_csv(os.path.join(OUT, "topic_year_panel.csv"), index=False)
rec("panel_biology_RR", PANo.estimate[1]); rec("panel_biology_lo", PANo.lower95[1]); rec("panel_biology_hi", PANo.upper95[1]); rec("panel_biology_p", PANo.p[1])
rec("panel_method_RR", PANo.estimate[0]); rec("panel_ratio", PANo.estimate[2]); rec("panel_ratio_p", PANo.p[2]); rec("panel_topic_years", len(Pn))

# ---------------------------------------------------------------- E (part). coded abstracts
cod = rd("problem_coding_primary_raw.csv").fillna({"problems": ""})
# The yearly draws overlap for 29 papers whose electronic and print publication years
# differ (PubMed [dp] matches both). Each PMID is counted once, in its earliest year.
samp_years = rd("problem_coding_primary.csv")[["pmid", "year"]]
samp_years = samp_years.sort_values(["pmid", "year"]).drop_duplicates("pmid", keep="first")
cod = cod.merge(samp_years, on="pmid", validate="one_to_one")
for c in CATEGORIES:
    cod[c] = cod.problems.apply(lambda s: int(c in s.split("|")))
cod["any_problem"] = (cod[CATEGORIES].sum(axis=1) > 0).astype(int)
cod["any_check"] = (cod[EVALUATION_CHECKS].sum(axis=1) > 0).astype(int)
shr = cod.groupby("year").sc_genomics.mean()
rec("n_coded", len(cod)); rec("n_sc_omics", int(cod.sc_genomics.sum()))
rec("sc_share_2015_pct", shr[2015] * 100); rec("sc_share_2026_pct", shr[2026] * 100)

# ---------------------------------------------------------------- D. single-cell-genomics sensitivity
BB = rd("benchmark_sc_genomics_flags.csv")
tyg = ty[["year", "subfield_papers", "verified_benchmarks", "yc"]].copy()
tyg["sc_share"] = tyg.year.map(shr)
tyg["sc_papers"] = tyg.subfield_papers * tyg.sc_share
tyg["sc_bench"] = tyg.year.map(BB[BB.year.between(2015, 2026)].groupby("year").sc_genomics.sum()).fillna(0).astype(int)
tyg["lo_sc"] = np.log(tyg.sc_papers)
rows = []
for nm, df in [("sc-genomics benchmarks / sc-genomics papers, 2015-2026", tyg), ("same, 2015-2025", tyg[tyg.year <= 2025]),
               ("same, 2019-2026", tyg[tyg.year >= 2019])]:
    mm = smf.glm("sc_bench ~ yc", df, offset=df.lo_sc, family=sm.families.Poisson()).fit(); e = ex(mm, "yc")
    rows.append(dict(analysis=nm, estimate=e[0], lower95=e[1], upper95=e[2], p=e[3], dispersion=mm.pearson_chi2 / mm.df_resid))
mA = smf.glm("verified_benchmarks ~ yc", tyg, offset=tyg.lo_sc, family=sm.families.Poisson()).fit(); e = ex(mA, "yc")
rows.append(dict(analysis="all benchmarks / sc-genomics papers, 2015-2026", estimate=e[0], lower95=e[1], upper95=e[2], p=e[3], dispersion=mA.pearson_chi2 / mA.df_resid))
# panel restricted to sc-genomics benchmarks
bxs = bdf.merge(BB[["pmid", "sc_genomics"]], on="pmid")
bxs = bxs[bxs.sc_genomics == True].assign(topic=lambda d: d.topics.str.split("|")).explode("topic")
by_s = bxs[bxs.year.between(2015, 2026)].groupby(["topic", "year"]).size()
Ps = Pn.copy()
Ps["bench_sc"] = [int(by_s.get((t, y), 0)) for t, y in zip(Ps.topic, Ps.year)]
Ps["lo_sc"] = np.log(Ps.papers * Ps.year.map(shr))
kt = Ps.groupby("topic").bench_sc.sum(); Ps = Ps[Ps.topic.isin(kt[kt > 0].index)]
g4 = smf.glm("bench_sc ~ yc_m + yc_b + C(topic)", Ps, offset=Ps.lo_sc, family=sm.families.Poisson()).fit()
n4 = list(g4.params.index); L4 = np.zeros(len(n4)); L4[n4.index("yc_m")] = 1; L4[n4.index("yc_b")] = -1; td4 = g4.t_test(L4)
for nm, lab in [("yc_m", "panel, method topics (sc genomics only)"), ("yc_b", "panel, biology/application topics (sc genomics only)")]:
    e = ex(g4, nm); rows.append(dict(analysis=lab, estimate=e[0], lower95=e[1], upper95=e[2], p=e[3], dispersion=g4.pearson_chi2 / g4.df_resid))
rows.append(dict(analysis="panel, ratio method/biology (sc genomics only)", estimate=float(np.exp(td4.effect[0])),
                 lower95=float(np.exp(td4.conf_int()[0][0])), upper95=float(np.exp(td4.conf_int()[0][1])), p=float(td4.pvalue), dispersion=np.nan))
SCo = pd.DataFrame(rows); SCo.to_csv(os.path.join(OUT, "sc_genomics_sensitivity.csv"), index=False)
rec("sc_trend_RR", SCo.estimate[0]); rec("sc_trend_lo", SCo.lower95[0]); rec("sc_trend_hi", SCo.upper95[0]); rec("sc_trend_p", SCo.p[0])
rec("sc_trend_2015_25_RR", SCo.estimate[1]); rec("sc_trend_2015_25_lo", SCo.lower95[1]); rec("sc_trend_2015_25_hi", SCo.upper95[1]); rec("sc_trend_2015_25_p", SCo.p[1])
rec("sc_panel_biology_RR", SCo.estimate[5]); rec("sc_panel_biology_lo", SCo.lower95[5]); rec("sc_panel_biology_hi", SCo.upper95[5]); rec("sc_panel_biology_p", SCo.p[5]); rec("sc_panel_ratio_p", SCo.p[6])
rec("sc_benchmarks", int(BB.sc_genomics.sum()))

# ---------------------------------------------------------------- E. stated-problem prevalence
G = cod[cod.sc_genomics].copy(); G["yc"] = G.year - 2020
rows = []
for c in CATEGORIES + ["any_problem", "any_check"]:
    k = int(G[c].sum()); lo, hi = proportion_confint(k, len(G), method="wilson")
    try:
        mm = smf.glm(f"{c} ~ yc", G, family=sm.families.Binomial()).fit(); e = ex(mm, "yc")
    except Exception:
        e = (np.nan,) * 4
    rows.append(dict(problem_type=c, n_abstracts=len(G), k=k, pct=k / len(G) * 100, lower95=lo * 100, upper95=hi * 100,
                     pct_2015_20=G[G.year <= 2020][c].mean() * 100, pct_2023_26=G[G.year >= 2023][c].mean() * 100,
                     OR_per_year=e[0], OR_lo=e[1], OR_hi=e[2], p=e[3]))
TP = pd.DataFrame(rows).sort_values("k", ascending=False); TP.to_csv(os.path.join(OUT, "problem_prevalence.csv"), index=False)
tpi = TP.set_index("problem_type")
for c in ["any_problem", "sample_size", "generalization", "clinical_translation", "no_ground_truth", "parameter_sensitivity",
          "no_benchmark", "uncertainty", "metric_invalid"]:
    rec(f"prev_{c}_pct", tpi.loc[c].pct)
rec("clinical_translation_OR", tpi.loc["clinical_translation"].OR_per_year)
rec("any_check_OR", tpi.loc["any_check"].OR_per_year); rec("any_check_OR_lo", tpi.loc["any_check"].OR_lo); rec("any_check_OR_hi", tpi.loc["any_check"].OR_hi)
G["period"] = pd.cut(G.year, [2014, 2018, 2021, 2023, 2026], labels=["2015-18", "2019-21", "2022-23", "2024-26"])
PERo = G.groupby("period", observed=True)[["any_problem", "any_check"]].agg(["sum", "count"])
PERo.columns = ["_".join(c) for c in PERo.columns]
for c in ["any_problem", "any_check"]:
    PERo[f"{c}_pct"] = PERo[f"{c}_sum"] / PERo[f"{c}_count"] * 100
PERo.to_csv(os.path.join(OUT, "problem_periods.csv"))
rec("any_check_2015_18_pct", PERo.any_check_pct.iloc[0]); rec("any_check_2024_26_pct", PERo.any_check_pct.iloc[3])
rec("any_problem_2015_18_pct", PERo.any_problem_pct.iloc[0]); rec("any_problem_2024_26_pct", PERo.any_problem_pct.iloc[3])

# ---------------------------------------------------------------- F. coder agreement
c2 = rd("problem_coding_second_model.csv").fillna({"problems": ""}).set_index("pmid")
c1 = cod.set_index("pmid")
ids = [p for p in c2.index if p in c1.index]


def kappa(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    po = (a == b).mean(); pe = a.mean() * b.mean() + (1 - a.mean()) * (1 - b.mean())
    return (po - pe) / (1 - pe) if pe < 1 else np.nan


rows = [("sc_genomics", kappa(c1.loc[ids, "sc_genomics"], c2.loc[ids, "sc_genomics"]), int(c1.loc[ids, "sc_genomics"].sum()), int(c2.loc[ids, "sc_genomics"].sum()))]
for c in CATEGORIES + ["any_problem"]:
    f2 = c2.loc[ids, "problems"].apply(lambda s: (len(s) > 0) if c == "any_problem" else (c in s.split("|"))).astype(int)
    f1 = c1.loc[ids, c]
    rows.append((c, kappa(f1, f2), int(f1.sum()), int(f2.sum())))
KA = pd.DataFrame(rows, columns=["category", "kappa", "positives_primary", "positives_second"])
KA.to_csv(os.path.join(OUT, "coder_agreement.csv"), index=False)
ka = KA.set_index("category").kappa
for c in ["sc_genomics", "technical_artifact", "parameter_sensitivity", "sample_size", "any_problem"]:
    rec(f"kappa_{c}", ka[c])

# ---------------------------------------------------------------- G. topic rates
rows = []
for r in ti.itertuples():
    lo, hi = pois_ci_per1000(r.bench_15_26, r.papers_15_26)
    lo2, hi2 = pois_ci_per1000(r.bench_23_26, r.papers_23_26)
    rows.append(dict(topic=r.topic, label=r.label, method=r.method, papers_15_26=r.papers_15_26, bench_15_26=r.bench_15_26,
                     rate_15_26=r.bench_15_26 / r.papers_15_26 * 1000, lower95=lo, upper95=hi,
                     papers_23_26=r.papers_23_26, bench_23_26=r.bench_23_26, rate_23_26=r.bench_23_26 / r.papers_23_26 * 1000, lower95_23_26=lo2, upper95_23_26=hi2))
TR = pd.DataFrame(rows).sort_values("rate_15_26", ascending=False); TR.to_csv(os.path.join(OUT, "topic_rates.csv"), index=False)
tr = TR.set_index("topic")
for t in ["deconvolution", "cnv_scdna", "clonal_phylogeny", "clinical_prognosis", "benchmarking"]:
    rec(f"rate15_{t}", tr.loc[t].rate_15_26)
rec("papers15_clinical_prognosis", tr.loc["clinical_prognosis"].papers_15_26); rec("papers15_lineage_barcoding", tr.loc["lineage_barcoding"].papers_15_26)

# ---------------------------------------------------------------- reproduction check
got = pd.DataFrame(R, columns=["quantity", "recomputed"])
exp_path = os.path.join(HERE, "..", "data", "expected_values.csv")
if os.path.exists(exp_path):
    expv = pd.read_csv(exp_path)
    chk = expv.merge(got, on="quantity", how="left")  # values printed in the manuscript
    got.to_csv(os.path.join(OUT, "recomputed_values.csv"), index=False)  # all recomputed values
    chk["abs_diff"] = (chk.recomputed - chk.published).abs()
    tol = 0.5 * 10.0 ** (-chk.decimals_in_manuscript)
    chk["matches_manuscript_rounding"] = chk.abs_diff <= tol + 1e-9
    chk.to_csv(os.path.join(OUT, "reproduction_check.csv"), index=False)
    print(f"{int(chk.matches_manuscript_rounding.sum())}/{len(chk)} quantities reproduce the manuscript values at the printed precision")
    bad = chk[~chk.matches_manuscript_rounding]
    if len(bad):
        print(bad.to_string())
else:
    got.to_csv(os.path.join(OUT, "recomputed_values.csv"), index=False)
print("outputs written to", os.path.abspath(OUT))
