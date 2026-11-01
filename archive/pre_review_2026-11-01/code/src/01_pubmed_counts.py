"""Step 1 - PubMed publication volume for the subfield and 26 topics, 2015-2026.

Reproduces Methods 2.1 and 2.7:
  * yearly counts of the subfield query and of each topic query (AND subfield);
  * the 2026 update: for each query, ratio = count today / count with Entrez
    date <= 2026/10/04; the archived 2026 count is multiplied by that ratio.

Network: eutils.ncbi.nlm.nih.gov (about 380 requests, ~3 min without an API key).
Counts drift slightly as PubMed indexes records (e.g. 2015 subfield: 443 in the
archive, 442 on 15 Oct 2026), so a re-run reproduces the published values
approximately, not exactly. The values used in the paper are in
data/raw_inputs/pubmed_volume_long.csv.

Usage:  python 01_pubmed_counts.py [--years 2015 2026] [--out ../outputs/pubmed_volume_rerun.csv]
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))

import argparse, os
from concurrent.futures import ThreadPoolExecutor

import pandas as pd

import eutils
from queries import SUBFIELD, TOPICS, EDAT_SNAPSHOT_2026_10_04, topic_query

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--years", nargs=2, type=int, default=[2015, 2026])
    ap.add_argument("--out", default=os.path.join(HERE, "..", "outputs", "pubmed_volume_rerun.csv"))
    ap.add_argument("--workers", type=int, default=3)
    a = ap.parse_args()
    years = range(a.years[0], a.years[1] + 1)

    jobs = [("__SUBFIELD_TOTAL__", SUBFIELD, y) for y in years]
    jobs += [(t, topic_query(t), y) for t in TOPICS for y in years]

    def run(j):
        t, q, y = j
        return t, y, eutils.count(q, y)

    with ThreadPoolExecutor(a.workers) as ex:
        rows = [dict(topic=t, year=y, count=c) for t, y, c in ex.map(run, jobs)]
    df = pd.DataFrame(rows)

    # 2026 growth ratio relative to the archived 4 October 2026 snapshot (Methods 2.7)
    if 2026 in years:
        ratios = []
        for t, q in [("__SUBFIELD_TOTAL__", SUBFIELD)] + [(t, topic_query(t)) for t in TOPICS]:
            then = eutils.count(q + EDAT_SNAPSHOT_2026_10_04, 2026)
            now = eutils.count(q, 2026)
            ratios.append(dict(topic=t, count_edat_le_2026_10_04=then, count_today=now, ratio=now / then if then else 1.0))
        pd.DataFrame(ratios).to_csv(a.out.replace(".csv", "_2026_ratios.csv"), index=False)

    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    df.to_csv(a.out, index=False)
    print(df.pivot(index="topic", columns="year", values="count").head(5).to_string())
    print("wrote", a.out)


if __name__ == "__main__":
    main()
