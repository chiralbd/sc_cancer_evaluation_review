# Checks that citations are numbered in order of first appearance and that every reference is cited.
import re
s = open("manuscript/sc_cancer_evaluation_review.md", encoding="utf-8").read()
body, refs = s.split("## References", 1)
n_refs = len(re.findall(r"^\d+\. ", refs, flags=re.M))
seen = []
for group in re.findall(r"\[(\d[\d,–\- ]*)\]", body):
    for part in group.replace(" ", "").split(","):
        a, _, b = part.replace("–", "-").partition("-")
        for n in range(int(a), int(b or a) + 1):
            if n not in seen:
                seen.append(n)
print("references in list:", n_refs)
print("distinct references cited:", len(seen))
print("never cited:", sorted(set(range(1, n_refs + 1)) - set(seen)))
print("cited but not in list:", sorted(set(seen) - set(range(1, n_refs + 1))))
print("out of order (first appearance):", [n for i, n in enumerate(seen) if n != i + 1][:20])
