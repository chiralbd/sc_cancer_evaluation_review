"""Convert the reformatted manuscript .tex to a submission-style .docx."""
import re, subprocess, sys
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, Cm, RGBColor

tex, workdir, out, pandoc = sys.argv[1:5]
s = open(tex, encoding="utf-8").read()

# --- simplify LaTeX for pandoc's reader ---------------------------------
pre, body = s.split(r"\begin{document}", 1)
body = re.sub(r"\\begin\{titlepage\}.*?\\end\{titlepage\}", "", body, flags=re.S)
title = ("The evaluation gap in single-cell cancer genomics: a quantitative review, "
         "benchmark catalogue and ground-truth resource")
front = (
    r"\noindent Md. Jubayer Hossain\textsuperscript{1,2,*}" "\n\n"
    r"\noindent \textsuperscript{1}Center for Health Innovation, Research, Action, and Learning -- Bangladesh (CHIRAL Bangladesh), Dhaka, Bangladesh" "\n\n"
    r"\noindent \textsuperscript{2}DeepBio, Dhaka, Bangladesh" "\n\n"
    r"\noindent \textsuperscript{*}\textbf{Correspondence:} Md. Jubayer Hossain, E-mail: \href{mailto:contact.jubayerhossain@gmail.com}{contact.jubayerhossain@gmail.com}" "\n\n"
    r"\noindent \textbf{Running title:} The evaluation gap in single-cell cancer genomics" "\n\n"
    r"\noindent \textbf{Article type:} Review (quantitative review and resource)" "\n\n"
    r"\noindent \textbf{Word counts:} abstract 303 words; main text 6,280 words (Introduction to Conclusions, excluding tables, legends and references)" "\n\n"
    r"\noindent \textbf{Display items:} 6 figures, 6 tables, 1 box. \textbf{References:} 121. \textbf{Supplementary data:} S1--S9" "\n\n"
    "PAGEBREAKMARK\n\n"
)
body = front + body
for cmd in [r"\linenumbers", r"\nolinenumbers", r"\clearpage", r"\endgroup",
            r"\setlength{\tabcolsep}{2pt}"]:
    body = body.replace(cmd, "")
body = re.sub(r"\\begingroup\\small\\setstretch\{[0-9.]+\}", "", body)
body = body.replace(r"\begin{tablefont}", "").replace(r"\end{tablefont}", "")
body = body.replace(r"\thead{", r"\textbf{").replace(r"\pandocbounded{", "{")
body = re.sub(r"\\href\{([^{}]+)\}\{\\nolinkurl\{([^{}]+)\}\}", r"\\href{\1}{\2}", body)
body = re.sub(r"\\begin\{enumerate\}\[label=\{\[\\arabic\*\]\}[^\n]*\]", r"\\begin{enumerate}", body)
# Box 1 -> quote with bold title
body = re.sub(r"\\begin\{tcolorbox\}\[.*?title=\{(.*?)\}\]\\small",
              lambda m: "\\begin{quote}\n\\textbf{" + m.group(1) + "}\n", body, flags=re.S)
body = body.replace(r"\end{tcolorbox}", r"\end{quote}")
body = body.replace(".pdf}", ".png}").replace(r"\includegraphics[keepaspectratio,", r"\includegraphics[width=\linewidth,keepaspectratio,")
body = body.replace(r"\section{1. Introduction}", "PAGEBREAKMARK\n\n" + r"\section{1. Introduction}", 1)
body = body.replace(r"\section{References}", "PAGEBREAKMARK\n\n" + r"\section{References}", 1)

simple = ("\\documentclass{article}\n\\usepackage{graphicx,longtable,booktabs,hyperref}\n"
          "\\title{" + title + "}\n\\date{}\n\\begin{document}\n\\maketitle\n" + body)
open(f"{workdir}/for_docx.tex", "w", encoding="utf-8").write(simple)
subprocess.run([pandoc, "for_docx.tex", "-f", "latex", "-t", "docx", "-o", "raw.docx"],
               cwd=workdir, check=True)

# --- style the docx --------------------------------------------------------
d = Document(f"{workdir}/raw.docx")
FONT = "Times New Roman"
for st in d.styles:
    if st.type == 1:  # paragraph/character
        try:
            st.font.name = FONT
            st.font.color.rgb = RGBColor(0, 0, 0)
            rpr = st.element.get_or_add_rPr()
            rf = rpr.find(qn("w:rFonts"))
            if rf is None:
                rf = OxmlElement("w:rFonts"); rpr.append(rf)
            for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
                rf.set(qn(a), FONT)
            for a in ("w:asciiTheme", "w:hAnsiTheme", "w:cstheme", "w:eastAsiaTheme"):
                if rf.get(qn(a)) is not None:
                    del rf.attrib[qn(a)]
        except Exception:
            pass

def para_fmt(name, size, bold=None, italic=None, before=0, after=6, line=1.5, align=None):
    try:
        st = d.styles[name]
    except KeyError:
        return
    st.font.size = Pt(size)
    if bold is not None: st.font.bold = bold
    if italic is not None: st.font.italic = italic
    pf = st.paragraph_format
    pf.space_before, pf.space_after, pf.line_spacing = Pt(before), Pt(after), line
    if align is not None: pf.alignment = align

para_fmt("Normal", 12)
for n in ("Body Text", "First Paragraph", "Compact"):
    para_fmt(n, 12, after=6, line=2.0 if n != "Compact" else 1.5)
para_fmt("Title", 16, bold=True, after=12, line=1.15, align=WD_ALIGN_PARAGRAPH.LEFT)
para_fmt("Heading 1", 14, bold=True, before=18, after=6, line=1.15)
para_fmt("Heading 2", 12, bold=True, italic=False, before=12, after=4, line=1.15)
para_fmt("Heading 3", 12, bold=False, italic=True, before=10, after=4, line=1.15)
para_fmt("Image Caption", 10, italic=False, before=4, after=12, line=1.15)
para_fmt("Table Caption", 10, italic=False, before=12, after=4, line=1.15)
para_fmt("Block Text", 11, before=6, after=6, line=1.15)
for n in ("Title", "Heading 1", "Heading 2", "Heading 3"):
    try: d.styles[n].font.color.rgb = RGBColor(0, 0, 0)
    except KeyError: pass

# page breaks, references in smaller type
in_refs = False
for p in d.paragraphs:
    if p.text.strip() == "PAGEBREAKMARK":
        # drop the marker; next paragraph starts a new page (no break glyph in viewers)
        nxt = p._p.getnext()
        while nxt is not None and nxt.tag != qn("w:p"):
            nxt = nxt.getnext()
        p._p.getparent().remove(p._p)
        if nxt is not None:
            nxt.get_or_add_pPr().append(OxmlElement("w:pageBreakBefore"))
        continue
    if p.style.name.startswith("Heading") and p.text.strip() == "References":
        in_refs = True
        continue
    if in_refs:
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(3)
        for r in p.runs: r.font.size = Pt(10)
# Box 1: shade quote paragraphs
for p in d.paragraphs:
    if p.style.name == "Block Text":
        ppr = p._p.get_or_add_pPr()
        shd = OxmlElement("w:shd"); shd.set(qn("w:val"), "clear"); shd.set(qn("w:fill"), "F2F2F2")
        ppr.append(shd)

# tables: booktabs-like borders, 9 pt text, bold header row, autofit width
data_tables = [t for t in d.tables if len(t.rows) > 1]  # 1x1 tables are pandoc figure holders
for t in data_tables:
    tblPr = t._tbl.tblPr
    for old in tblPr.findall(qn("w:tblBorders")): tblPr.remove(old)
    b = OxmlElement("w:tblBorders")
    for edge, val in (("top", "single"), ("bottom", "single"), ("left", "nil"),
                      ("right", "nil"), ("insideH", "nil"), ("insideV", "nil")):
        e = OxmlElement(f"w:{edge}"); e.set(qn("w:val"), val)
        if val == "single": e.set(qn("w:sz"), "8"); e.set(qn("w:color"), "000000")
        b.append(e)
    tblPr.append(b)
    w = tblPr.find(qn("w:tblW"))
    if w is None: w = OxmlElement("w:tblW"); tblPr.append(w)
    w.set(qn("w:type"), "pct"); w.set(qn("w:w"), "5000")
    for i, row in enumerate(t.rows):
        for c in row.cells:
            if i == 0:
                tcPr = c._tc.get_or_add_tcPr()
                tb = OxmlElement("w:tcBorders"); bt = OxmlElement("w:bottom")
                bt.set(qn("w:val"), "single"); bt.set(qn("w:sz"), "6"); bt.set(qn("w:color"), "000000")
                tb.append(bt); tcPr.append(tb)
            for p in c.paragraphs:
                p.paragraph_format.line_spacing = 1.0
                p.paragraph_format.space_after = Pt(1)
                p.paragraph_format.space_before = Pt(1)
                for r in p.runs:
                    r.font.size = Pt(9)
                    if i == 0: r.font.bold = True

# page setup, line numbers, page numbers
for sec in d.sections:
    sec.page_height, sec.page_width = Cm(29.7), Cm(21.0)
    sec.left_margin = sec.right_margin = sec.top_margin = sec.bottom_margin = Cm(2.5)
    sp = sec._sectPr
    ln = OxmlElement("w:lnNumType")
    ln.set(qn("w:countBy"), "1"); ln.set(qn("w:restart"), "continuous"); ln.set(qn("w:distance"), "283")
    sp.append(ln)
    fp = sec.footer.paragraphs[0]; fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = fp.add_run()
    for kind, txt in (("begin", None), (None, "PAGE"), ("end", None)):
        if kind:
            fc = OxmlElement("w:fldChar"); fc.set(qn("w:fldCharType"), kind); run._r.append(fc)
        else:
            it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = txt; run._r.append(it)
    hp = sec.header.paragraphs[0]; hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hr = hp.add_run("The evaluation gap in single-cell cancer genomics"); hr.italic = True; hr.font.size = Pt(9)

# no line numbers inside tables / references (suppressLineNumbers)
def suppress(p):
    ppr = p._p.get_or_add_pPr(); e = OxmlElement("w:suppressLineNumbers"); ppr.append(e)
for t in data_tables:
    for row in t.rows:
        for c in row.cells:
            for p in c.paragraphs: suppress(p)

d.core_properties.title = title
d.core_properties.author = "Md. Jubayer Hossain"
d.save(out)
print("saved", out)
