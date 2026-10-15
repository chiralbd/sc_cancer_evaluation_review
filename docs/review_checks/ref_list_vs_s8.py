# Matches each manuscript reference to its S8 row by PMID or DOI, then checks year and numbering.
import csv, re
s = open("manuscript/sc_cancer_evaluation_review.md", encoding="utf-8").read()
entries = dict(re.findall(r"^(\d+)\. (.+)$", s.split("## References", 1)[1], flags=re.M))
s8 = list(csv.DictReader(open("supplementary/S8_review_references.csv", encoding="utf-8")))
unmatched, renumbered, year_issues = [], [], []
for r in s8:
    key = r["pmid"] or r["doi"]
    hits = [n for n, e in entries.items() if key and key.lower() in e.lower()]
    if not hits:
        unmatched.append(r["n"]); continue
    n = hits[0]
    if n != r["n"]:
        renumbered.append((r["n"], n))
    if r["year"] not in entries[n]:
        year_issues.append(n)
matched = len(s8) - len(unmatched)
print(f"S8 rows: {len(s8)}; manuscript entries: {len(entries)}; matched by PMID/DOI: {matched}")
print("S8 rows not found in manuscript list:", unmatched or "none")
print("year not found in manuscript entry:", year_issues or "none")
print(f"S8 'n' differs from manuscript number for {len(renumbered)} rows; first few (S8 n -> manuscript n):", renumbered[:6])
