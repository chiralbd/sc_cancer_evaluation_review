"""Reformat pandoc-generated manuscript .tex into a clean submission layout."""
import re, sys

src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()

# ---- split preamble / title block / body -------------------------------
body = s[s.index(r"\end{titlepage}") + len(r"\end{titlepage}"):s.index(r"\end{document}")]

PREAMBLE = r"""\documentclass[11pt]{article}

%% ---------------------------------------------------------------
%% Page layout and fonts
%% ---------------------------------------------------------------
\usepackage[a4paper,top=2.5cm,bottom=2.5cm,left=2.5cm,right=2.5cm,headheight=14pt]{geometry}
\usepackage{fontspec}
\setmainfont{LibertinusSerif}[Extension=.otf,UprightFont=*-Regular,BoldFont=*-Bold,ItalicFont=*-Italic,BoldItalicFont=*-BoldItalic]
\usepackage{unicode-math}
\setmathfont{LibertinusMath-Regular.otf}
\usepackage{microtype}
\usepackage{setspace}
\onehalfspacing
\setlength{\parindent}{1.5em}
\setlength{\parskip}{0pt}
\emergencystretch=3em
\clubpenalty=10000
\widowpenalty=10000

%% ---------------------------------------------------------------
%% Packages
%% ---------------------------------------------------------------
\usepackage{amsmath}
\usepackage{graphicx}
\usepackage{booktabs,longtable,array,calc}
\usepackage[table]{xcolor}
\usepackage[most]{tcolorbox}
\usepackage{enumitem}
\usepackage{float}
\usepackage[mathlines]{lineno}
\usepackage{fancyhdr}
\usepackage{titlesec}
\usepackage{caption}
\usepackage{xurl}
\usepackage[hidelinks]{hyperref}
\urlstyle{same}
\hypersetup{
  pdftitle={The evaluation gap in single-cell cancer genomics: a quantitative review, benchmark catalogue and ground-truth resource},
  pdfauthor={Md. Jubayer Hossain},
  pdfkeywords={single-cell RNA sequencing; cancer genomics; benchmarking; meta-research; ground truth; calibration; multiverse analysis}
}

%% ---------------------------------------------------------------
%% Headings (sections are numbered manually in the text)
%% ---------------------------------------------------------------
\setcounter{secnumdepth}{0}
\titleformat{\section}{\normalfont\large\bfseries}{}{0pt}{}
\titleformat{\subsection}{\normalfont\normalsize\bfseries}{}{0pt}{}
\titleformat{\subsubsection}{\normalfont\normalsize\itshape}{}{0pt}{}
\titlespacing*{\section}{0pt}{1.6ex plus .4ex minus .2ex}{0.8ex plus .2ex}
\titlespacing*{\subsection}{0pt}{1.2ex plus .3ex minus .2ex}{0.5ex plus .1ex}
\titlespacing*{\subsubsection}{0pt}{1.0ex plus .3ex minus .2ex}{0.3ex plus .1ex}

%% ---------------------------------------------------------------
%% Header / footer
%% ---------------------------------------------------------------
\pagestyle{fancy}
\fancyhf{}
\fancyhead[R]{\small\itshape The evaluation gap in single-cell cancer genomics}
\fancyfoot[C]{\small\thepage}
\renewcommand{\headrulewidth}{0pt}
\fancypagestyle{plain}{\fancyhf{}\fancyfoot[C]{\small\thepage}\renewcommand{\headrulewidth}{0pt}}

%% ---------------------------------------------------------------
%% Floats, captions and tables
%% ---------------------------------------------------------------
\captionsetup{font={small,stretch=1.1},labelformat=empty,justification=justified,singlelinecheck=false,skip=6pt}
\captionsetup[longtable]{font={small,stretch=1.1},labelformat=empty,justification=justified,singlelinecheck=false,skip=4pt}
\floatplacement{figure}{!htbp}
\makeatletter\def\fps@figure{!htbp}\makeatother
\renewcommand{\topfraction}{0.9}
\renewcommand{\bottomfraction}{0.8}
\renewcommand{\textfraction}{0.07}
\renewcommand{\floatpagefraction}{0.75}
\setkeys{Gin}{width=\linewidth,height=0.62\textheight,keepaspectratio}
\setlength{\LTcapwidth}{\textwidth}
\setlength{\LTpre}{6pt}
\setlength{\LTpost}{6pt}
\renewcommand{\arraystretch}{1.2}
\newenvironment{tablefont}{\par\scriptsize\setlength{\tabcolsep}{3.5pt}\nolinenumbers}{\par\linenumbers}
\newcommand{\thead}[1]{\textbf{#1}}

%% ---------------------------------------------------------------
%% Lists and pandoc compatibility
%% ---------------------------------------------------------------
\setlist{noitemsep,topsep=3pt,leftmargin=*}
\providecommand{\tightlist}{\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}
\providecommand{\pandocbounded}[1]{#1}

\begin{document}

%% ===============================================================
%% Title page
%% ===============================================================
\begin{titlepage}
\thispagestyle{empty}
\begin{flushleft}
\setstretch{1.15}
{\Large\bfseries\hyphenpenalty=10000
The evaluation gap in single-cell cancer genomics: a quantitative review, benchmark catalogue and ground-truth resource\par}
\vspace{2em}
{\large Md.\ Jubayer Hossain\textsuperscript{1,2,*}\par}
\vspace{1.2em}
{\small
\textsuperscript{1}Center for Health Innovation, Research, Action, and Learning -- Bangladesh (CHIRAL Bangladesh), Dhaka, Bangladesh\par
\textsuperscript{2}DeepBio, Dhaka, Bangladesh\par}
\vspace{1.5em}
{\small
\textsuperscript{*}\textbf{Correspondence:} Md.\ Jubayer Hossain\\
E-mail: \href{mailto:contact.jubayerhossain@gmail.com}{contact.jubayerhossain@gmail.com}\par}
\vspace{2.5em}
\renewcommand{\arraystretch}{1.3}
{\small
\begin{tabular}{@{}p{0.27\textwidth}p{0.69\textwidth}@{}}
\textbf{Running title} & The evaluation gap in single-cell cancer genomics\\
\textbf{Article type} & Review (quantitative review and resource)\\
\textbf{Abstract} & 303 words\\
\textbf{Main text} & 6,280 words (Introduction to Conclusions, excluding tables, legends and references)\\
\textbf{Display items} & 6 figures, 6 tables, 1 box\\
\textbf{References} & 121\\
\textbf{Supplementary data} & S1--S9\\
\end{tabular}}
\end{flushleft}
\end{titlepage}

\linenumbers
"""

# ---- body clean-up ------------------------------------------------------
# Re-join headings that pandoc wrapped across lines, then promote one level.
def join_heading(m):
    return m.group(1) + "{" + " ".join(m.group(2).split()) + "}"
body = re.sub(r"(\\(?:sub)*section)\{([^{}]*?)\}", join_heading, body, flags=re.S)
body = body.replace(r"\subsection{", r"\section{").replace(r"\subsubsection{", r"\subsection{")

# Abstract on its own page, with keywords; main text starts on a new page.
# Abstract: flush-left paragraphs so the Background/Methods/Results/Conclusions labels align.
body = body.replace(r"\section{Abstract}\label{abstract}",
                    "\\section{Abstract}\\label{abstract}\n\\begingroup\\setlength{\\parindent}{0pt}\\setlength{\\parskip}{0.6ex}", 1)
body = body.replace(r"\section{1. Introduction}", "\\endgroup\n\\clearpage\n\\section{1. Introduction}", 1)
body = body.replace(r"\section{References}", "\\clearpage\n\\section{References}", 1)

# Grammar fix in abstract (double 'and' in list).
body = body.replace(
    "and a\ncatalogue of 1,336 GEO", "a\ncatalogue of 1,336 GEO")

# Tables: scriptsize wrapper -> tablefont; bold header cells; bold "Table N." label.
body = body.replace(r"\begin{scriptsize}", r"\begin{tablefont}").replace(r"\end{scriptsize}", r"\end{tablefont}")
body = re.sub(r"\\begin\{minipage\}\[b\]\{\\linewidth\}\\raggedright\n(.*?)\n\\end\{minipage\}",
              lambda m: "\\begin{minipage}[b]{\\linewidth}\\raggedright\n\\thead{" + m.group(1) + "}\n\\end{minipage}",
              body, flags=re.S)
body = re.sub(r"\\caption\{(Table \d+\.)", r"\\caption{\\textbf{\1}", body)
body = body.replace(r"\begin{longtable}[]", r"\begin{longtable}[l]")
body = body.replace(r"\toprule\noalign{}", r"\toprule").replace(r"\midrule\noalign{}", r"\midrule").replace(r"\bottomrule\noalign{}", r"\bottomrule")

# Table 4 (14 columns): rebalance widths so short headers fit.
j = body.index(r"\caption{\textbf{Table 4.}")
k = body.rindex(r"\begin{longtable}", 0, j)
spec = body[k:j]
widths = ["0.1350", "0.0300", "0.0650", "0.1000"] + ["0.0660"] * 10
vals = re.findall(r"\\real\{([0-9.]+)\}", spec)
assert len(vals) == 14, vals
it = iter(widths)
spec = re.sub(r"(\\real\{)[0-9.]+(\})", lambda m: m.group(1) + next(it) + m.group(2), spec)
body = body[:k] + "\\setlength{\\tabcolsep}{2pt}\n" + spec + body[j:]

# DOIs in references: allow line breaks inside long DOI strings.
body = re.sub(r"doi:\\href\{([^{}]+)\}\{([^{}]+)\}", r"doi:\\href{\1}{\\nolinkurl{\2}}", body)

# Figures: keep figures from floating ahead of their first mention in a section.
body = body.replace("\\begin{figure}\n", "\\begin{figure}[!htbp]\n")

# Box 1: title bar style.
body = body.replace(
    r"\begin{tcolorbox}[colback=gray!6,colframe=gray!60,boxrule=0.5pt,arc=1pt,left=6pt,right=6pt,top=4pt,bottom=4pt,breakable]"
    + "\n" + r"\textbf{Box 1. Minimum evaluation standard for single-cell cancer" + "\nmethods}",
    r"\begin{tcolorbox}[enhanced,breakable,colback=gray!5,colframe=gray!55,boxrule=0.6pt,arc=2pt,left=8pt,right=8pt,top=6pt,bottom=6pt,"
    r"fonttitle=\bfseries,coltitle=black,colbacktitle=gray!18,title={Box 1. Minimum evaluation standard for single-cell cancer methods}]\small")

# Declarations: author contribution placeholder (sole author).
body = body.replace(
    "\\textbf{Authors' contributions.} {[}To be confirmed by the author before\nsubmission.{]}",
    "\\textbf{Authors' contributions.} M.J.H. conceived and designed the study,\n"
    "curated the data, performed the analyses, prepared the figures and\n"
    "wrote and revised the manuscript.")

# References: numbered [n] list in small type, single-spaced, no line numbers.
i = body.index(r"\section{References}")
head, refs = body[:i], body[i:]
refs = refs.replace("\\begin{enumerate}\n\\def\\labelenumi{\\arabic{enumi}.}\n\\tightlist",
                    "\\begingroup\\small\\setstretch{1.05}\\nolinenumbers\n"
                    "\\begin{enumerate}[label={[\\arabic*]},leftmargin=2.6em,labelsep=0.5em,itemsep=1.5pt]", 1)
refs = refs.rstrip()
assert refs.endswith(r"\end{enumerate}")
refs += "\n\\endgroup\n"
body = head + refs

for needle in ["contact.jubayerhossain", "fonttitle=", "M.J.H. conceived", "a\ncatalogue of 1,336 GEO", "\\clearpage\n\\section{1. Introduction}"]:
    assert needle in PREAMBLE + body, needle
assert "and a\ncatalogue of 1,336 GEO" not in body
open(dst, "w", encoding="utf-8").write(PREAMBLE + body + "\n\\end{document}\n")
print("written", dst)
