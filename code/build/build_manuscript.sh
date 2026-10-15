#!/usr/bin/env bash
# Typeset the manuscript: Markdown body -> LaTeX (pandoc) -> PDF (Tectonic, XeTeX engine).
# Requires pandoc >= 3.1 and Tectonic 0.17 (fonts: Libertinus Serif/Math, fetched by Tectonic).
# Figure PDFs must be in ./fig/ (copy from ../outputs/fig/ after running src/04_figures.py).
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p fig && cp -n ../outputs/fig/*.pdf fig/ 2>/dev/null || true
pandoc manuscript_body.md -f markdown+raw_attribute -t latex --template=./submission_template.tex --columns=72 -o sc_cancer_evaluation_review.tex
# Box 1 is written as a block quote in Markdown and rendered as a shaded tcolorbox
python - <<'EOF'
s = open("sc_cancer_evaluation_review.tex").read()
s = s.replace("\\begin{quote}", "\\begin{tcolorbox}[colback=gray!6,colframe=gray!60,boxrule=0.5pt,arc=1pt,left=6pt,right=6pt,top=4pt,bottom=4pt,breakable]").replace("\\end{quote}", "\\end{tcolorbox}")
open("sc_cancer_evaluation_review.tex", "w").write(s)
EOF
tectonic sc_cancer_evaluation_review.tex
