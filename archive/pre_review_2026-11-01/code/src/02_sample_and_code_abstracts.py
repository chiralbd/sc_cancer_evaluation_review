"""Step 2 - stratified abstract sample (150 per year, 2015-2026) and stated-problem coding.

Reproduces Methods 2.4.

Sampling. For each publication year, all research records matching the subfield
query (reviews, editorials, comments and errata excluded) are retrieved, shuffled
with numpy default_rng(2026), and the first 150 with an abstract of >= 400
characters that are not typed 'Review' are kept (260 candidates fetched per year).
PubMed's esearch ordering and index change over time, so a re-run draws a
different sample; the sample analysed in the paper is shipped as
supplementary/S7_statistics/update_2026-10-15/problem_sample_2015_2026.csv and
the codes as data/raw_inputs/problem_coding_primary_raw.csv.

Coding. Abstracts are coded with forced tool use under the definitions in
coding_prompt.py. In the study, the primary coder was claude-haiku-4-5-20251001
(temperature 0, batches of 15; missing items re-requested in batches of 10) and a
random 150-abstract reliability subsample (random_state=7) was re-coded by a
second, larger model (claude-sonnet-5, default temperature, no extended thinking).
The session called these models through the analysis platform's internal LLM
interface; this script issues the equivalent requests through the public
Anthropic Messages API (pip install anthropic; set ANTHROPIC_API_KEY). Model
outputs are not deterministic across API versions, so re-coding reproduces the
published prevalences approximately.

Usage:
  python 02_sample_and_code_abstracts.py sample  --out ../outputs/sample_rerun.csv
  python 02_sample_and_code_abstracts.py code    --sample <csv> --model claude-haiku-4-5-20251001 --out ../outputs/codes_rerun.csv
  python 02_sample_and_code_abstracts.py code    --sample <csv> --model claude-sonnet-5 --subsample 150 --seed 7 --no-temperature --out ../outputs/codes_second.csv
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))

import argparse, json, os, sys
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pandas as pd

import eutils
from queries import SUBFIELD, NOT_REVIEW
from coding_prompt import TOOL, build_prompt


def sample(out, per_year=150, n_candidates=260, seed=2026):
    rng = np.random.default_rng(seed)
    rows = []
    for y in range(2015, 2027):
        ids = eutils.search_ids(f'{SUBFIELD} AND ("{y}"[dp]){NOT_REVIEW}')
        cand = [int(c) for c in rng.permutation(ids)[:n_candidates]]
        ab = eutils.fetch_abstracts(cand)
        keep = [p for p in cand if p in ab and len(ab[p]["abstract"]) >= 400 and "Review" not in ab[p]["ptypes"]][:per_year]
        rows += [dict(pmid=p, year=y, **ab[p]) for p in keep]
        print(y, len(ids), "eligible ->", len(keep), file=sys.stderr)
    pd.DataFrame(rows).to_csv(out, index=False)


def code(sample_csv, model, out, batch=15, subsample=None, seed=7, temperature=True, workers=8):
    import anthropic  # public SDK
    client = anthropic.Anthropic()
    s = pd.read_csv(sample_csv).fillna("")
    if subsample:
        s = s.sample(subsample, random_state=seed)

    def call(b):
        kw = dict(model=model, max_tokens=3000, tools=[TOOL], tool_choice={"type": "tool", "name": TOOL["name"]},
                  messages=[{"role": "user", "content": build_prompt(b.itertuples())}])
        if temperature:
            kw["temperature"] = 0
        try:
            r = client.messages.create(**kw)
            return [blk.input for blk in r.content if blk.type == "tool_use"]
        except Exception as e:  # keep going; missing items are retried below
            print("error:", str(e)[:200], file=sys.stderr)
            return []

    def run(frame, size):
        batches = [frame.iloc[i:i + size] for i in range(0, len(frame), size)]
        with ThreadPoolExecutor(workers) as ex:
            res = list(ex.map(call, batches))
        got = {}
        for r in res:
            for inp in r:
                for it in inp.get("items", []):
                    got.setdefault(int(it["id"]), it)
        return got

    codes = run(s, batch)
    miss = s[~s.pmid.isin(codes)]
    if len(miss):
        for k, v in run(miss, 10).items():
            codes.setdefault(k, v)
    pd.DataFrame([dict(pmid=k, sc_genomics=bool(v["sc_genomics"]), problems="|".join(v["problems"])) for k, v in codes.items()]).to_csv(out, index=False)
    print("coded", len(codes), "of", len(s), file=sys.stderr)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["sample", "code"])
    ap.add_argument("--sample")
    ap.add_argument("--model", default="claude-haiku-4-5-20251001")
    ap.add_argument("--subsample", type=int)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--no-temperature", action="store_true")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    if a.step == "sample":
        sample(a.out)
    else:
        code(a.sample, a.model, a.out, subsample=a.subsample, seed=a.seed, temperature=not a.no_temperature)
