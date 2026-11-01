# Compares S8 reference metadata (title, year, DOI, retraction status) with live PubMed records.
# Needs internet. One batched NCBI E-utilities request; no API key required.
import csv, json, re, urllib.request

rows = list(csv.DictReader(open("supplementary/S8_review_references.csv", encoding="utf-8")))
pmids = [r["pmid"] for r in rows if r["pmid"].strip()]
url = ("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&retmode=json&id="
       + ",".join(pmids))
res = json.load(urllib.request.urlopen(url, timeout=60))["result"]

norm = lambda t: re.sub(r"[^a-z0-9]", "", t.lower())
problems = 0
for r in rows:
    p = r["pmid"].strip()
    if not p:
        print(f"[{r['n']}] no PMID (verified via {r['verified_via']}): check DOI {r['doi']} by hand")
        continue
    rec = res.get(p)
    if not rec or "error" in rec:
        print(f"[{r['n']}] PMID {p} not found"); problems += 1; continue
    doi = next((a["value"] for a in rec.get("articleids", []) if a["idtype"] == "doi"), "")
    issues = []
    if norm(rec["title"]) != norm(r["title"]):
        issues.append(f"title differs: PubMed '{rec['title'][:70]}'")
    if not rec.get("pubdate", "").startswith(r["year"]) and r["year"] not in rec.get("epubdate", ""):
        issues.append(f"year {r['year']} vs PubMed {rec.get('pubdate')}")
    if doi and r["doi"] and doi.lower() != r["doi"].lower():
        issues.append(f"DOI {r['doi']} vs PubMed {doi}")
    if any("Retract" in t for t in rec.get("pubtype", [])):
        issues.append("RETRACTION-RELATED PUBLICATION TYPE")
    if issues:
        problems += 1
        print(f"[{r['n']}] PMID {p}: " + "; ".join(issues))
print(f"\n{len(rows)} references, {len(pmids)} with PMID, {problems} flagged")
