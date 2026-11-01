"""Thin, rate-limited wrappers around the NCBI E-utilities used throughout the study.

All requests go to https://eutils.ncbi.nlm.nih.gov/entrez/eutils/ . NCBI allows
3 requests/s without an API key and 10/s with one; set NCBI_API_KEY in the
environment to use a key. Functions retry transient failures four times.
"""
import os, time, re
import xml.etree.ElementTree as ET
import requests

BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
API_KEY = os.environ.get("NCBI_API_KEY")
PAUSE = 0.11 if API_KEY else 0.35


def _params(**kw):
    if API_KEY:
        kw["api_key"] = API_KEY
    return kw


def count(term, year=None):
    """Number of PubMed records matching `term`, optionally restricted to a publication year ([dp])."""
    t = term + (f' AND ("{year}"[dp])' if year else "")
    for _ in range(4):
        try:
            r = requests.get(BASE + "esearch.fcgi", params=_params(db="pubmed", term=t, rettype="count", retmode="json"), timeout=60)
            time.sleep(PAUSE)
            return int(r.json()["esearchresult"]["count"])
        except Exception:
            time.sleep(1.5)
    return None


def search_ids(term, retmax=10000):
    """PMIDs matching `term` (first `retmax`, PubMed default sort)."""
    r = requests.get(BASE + "esearch.fcgi", params=_params(db="pubmed", term=term, retmax=retmax, retmode="json"), timeout=120).json()
    time.sleep(PAUSE)
    return [int(x) for x in r["esearchresult"]["idlist"]]


def fetch_abstracts(pmids, chunk=200):
    """Title, abstract and publication types for each PMID (efetch XML)."""
    out = {}
    for i in range(0, len(pmids), chunk):
        ch = pmids[i:i + chunk]
        root = None
        for _ in range(4):
            try:
                x = requests.post(BASE + "efetch.fcgi", data=_params(db="pubmed", id=",".join(map(str, ch)), retmode="xml"), timeout=120).text
                root = ET.fromstring(x)
                break
            except Exception:
                time.sleep(2)
        if root is None:
            continue
        for a in root.findall(".//PubmedArticle"):
            pm = int(a.findtext(".//PMID"))
            t = a.find(".//ArticleTitle")
            ti = "".join(t.itertext()) if t is not None else ""
            ab = " ".join("".join(e.itertext()) for e in a.findall(".//AbstractText"))
            pt = [e.text for e in a.findall(".//PublicationType")]
            out[pm] = dict(title=ti, abstract=ab, ptypes=";".join(pt))
        time.sleep(PAUSE)
    return out


def summaries(pmids, chunk=200):
    """esummary records keyed by PMID (used to verify existence, dates and journal of every reference)."""
    out = {}
    for i in range(0, len(pmids), chunk):
        ch = pmids[i:i + chunk]
        r = {}
        for _ in range(4):
            try:
                r = requests.post(BASE + "esummary.fcgi", data=_params(db="pubmed", id=",".join(map(str, ch)), retmode="json"), timeout=90).json()["result"]
                break
            except Exception:
                time.sleep(2)
        for u in r.get("uids", []):
            out[int(u)] = r[u]
        time.sleep(PAUSE)
    return out


def first_year(rec):
    """Earliest of print and electronic publication year in an esummary record."""
    ys = [int(m.group(1)) for s in (rec.get("pubdate"), rec.get("epubdate")) if s for m in [re.match(r"(\d{4})", s)] if m]
    return min(ys) if ys else None
