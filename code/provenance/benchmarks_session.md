# Sub-agent: Benchmark literature (PubMed searches, screening, 269-record catalogue, field extraction)
Verbatim record of every code cell executed in this session, in execution order. Cells are notebook-style: they share one persistent interpreter, so later cells use variables created by earlier ones. Failed cells are kept and marked; the cell that follows usually corrects them.
Tool legend: `python` = persistent Python kernel; `bash` = fresh shell; `repl` = orchestration kernel of the analysis platform (sub-agent dispatch, artifact and memory calls; not needed to reproduce results). Calls to `host.*` (e.g. `host.llm`, `host.artifact_path`) are platform services; `src/` provides public equivalents.
Cells: 36; failed: 2.

## Cell 1 · bash (python) · ok

Unzipping prior analysis artifact

```bash
mkdir -p prior && cd prior && unzip -o -q "/Users/jubayer/.claude-science/orgs/89d7686f-eb25-4116-8f44-856d205cc44b/artifacts/proj_e32ccc743087/c1980142-77dc-48d1-aeeb-c35fa1fd69f3/vbd928677_artifacts-sc.zip" && find . -type f | head -30 && python -c "
import pandas as pd,glob
f=glob.glob('**/benchmark_classification.csv',recursive=True)[0]
d=pd.read_csv(f);print(f,d.shape);print(d.columns.tolist());print(d.is_benchmark.value_counts());print(d.head(3).to_string())"
```

## Cell 2 · python (python) · ok

Inspecting host.llm API

```python
help(host.llm)
```

## Cell 3 · python (python) · FAILED

Running per-class PubMed benchmark searches

```python

import requests, time, json, pandas as pd, re
E="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
def es(q,n=60):
    for _ in range(3):
        try:
            r=requests.get(E+"esearch.fcgi",params=dict(db="pubmed",term=q,retmax=n,retmode="json",sort="relevance"),timeout=30)
            time.sleep(0.4); return r.json()["esearchresult"]["idlist"]
        except Exception as e: time.sleep(2)
    return []
B='(benchmark*[tiab] OR "systematic comparison"[tiab] OR "systematic evaluation"[tiab] OR "comprehensive evaluation"[tiab] OR "comparative analysis"[tiab] OR "performance evaluation"[tiab] OR "comparison of"[ti] OR evaluation[ti] OR benchmarking[ti] OR assessment[ti])'
SC='(single-cell[tiab] OR "single cell"[tiab] OR scRNA-seq[tiab] OR spatial transcriptomic*[tiab])'
Q={
"CNV inference & malignant-cell calling":[f'(copy number[tiab] OR CNV[tiab] OR aneuploid*[tiab] OR malignant cell*[tiab] OR inferCNV[tiab] OR copyKAT[tiab]) AND {SC} AND {B}'],
"bulk deconvolution":[f'(deconvolution[tiab] OR "cell type proportion*"[tiab] OR "cellular composition"[tiab]) AND (bulk[tiab] OR tumor[tiab]) AND {B} AND (single-cell[tiab] OR reference[tiab] OR transcriptom*[tiab])'],
"data integration/batch correction":[f'("batch correction"[tiab] OR "batch effect*"[tiab] OR "data integration"[tiab] OR integration[ti]) AND {SC} AND {B}'],
"cell-type annotation & label transfer":[f'("cell type annotation"[tiab] OR "cell-type annotation"[tiab] OR "cell type identification"[tiab] OR "label transfer"[tiab] OR "cell type classification"[tiab] OR classifier*[ti]) AND {SC} AND {B}'],
"cell-cell communication":[f'("cell-cell communication"[tiab] OR "cell-cell interaction*"[tiab] OR "ligand-receptor"[tiab] OR "intercellular communication"[tiab]) AND {B}'],
"spatial (deconvolution, domains, SVG)":[f'(spatial transcriptomic*[tiab] OR spatially resolved[tiab] OR Visium[tiab]) AND (deconvolution[tiab] OR "spatial domain*"[tiab] OR clustering[tiab] OR "spatially variable"[tiab] OR "cell segmentation"[tiab] OR imputation[tiab] OR alignment[tiab] OR mapping[tiab]) AND {B}'],
"GRN/regulon inference":[f'("gene regulatory network*"[tiab] OR GRN[tiab] OR regulon*[tiab] OR "network inference"[tiab]) AND {SC} AND {B}'],
"lineage tracing/mtDNA clone calling":[f'("lineage tracing"[tiab] OR mitochondrial[tiab] OR mtDNA[tiab] OR "clone calling"[tiab] OR "clonal"[tiab] OR "somatic mutation*"[tiab] OR "variant calling"[tiab] OR SNV[tiab]) AND {SC} AND {B}'],
"clonal phylogeny/scDNA":[f'("single-cell DNA"[tiab] OR scDNA-seq[tiab] OR "tumor phylogen*"[tiab] OR "phylogeny inference"[tiab] OR "intratumor heterogeneity"[tiab] OR "single-cell whole genome"[tiab] OR "whole genome amplification"[tiab]) AND {B}'],
"differential abundance & differential expression":[f'("differential expression"[tiab] OR "differential abundance"[tiab] OR "differentially expressed"[tiab] OR pseudobulk[tiab] OR pseudoreplication[tiab] OR "compositional"[tiab]) AND {SC} AND {B}'],
"doublet detection & ambient RNA":[f'(doublet*[tiab] OR multiplet*[tiab] OR "ambient RNA"[tiab] OR demultiplex*[tiab] OR "empty droplet*"[tiab] OR "quality control"[ti]) AND {SC} AND {B}'],
"trajectory inference":[f'(trajectory[tiab] OR pseudotime[tiab] OR "RNA velocity"[tiab] OR "lineage inference"[tiab]) AND {SC} AND {B}'],
"perturbation-response prediction":[f'(perturbation*[tiab] OR Perturb-seq[tiab] OR "CRISPR screen*"[tiab]) AND (prediction[tiab] OR predict*[tiab] OR model*[tiab]) AND {SC} AND {B}'],
"single-cell foundation models":[f'("foundation model*"[tiab] OR scGPT[tiab] OR Geneformer[tiab] OR "large language model*"[tiab] OR "pretrained"[tiab] OR "zero-shot"[tiab] OR scFoundation[tiab]) AND {SC} AND (evaluat*[tiab] OR {B})'],
"drug-response prediction":[f'("drug response"[tiab] OR "drug sensitivity"[tiab] OR "drug resistance prediction"[tiab] OR "drug response prediction"[tiab]) AND {SC} AND (predict*[tiab]) AND {B}'],
"other preprocessing (clustering, normalization, imputation, dimensionality reduction)":[f'(clustering[tiab] OR normalization[tiab] OR imputation[tiab] OR "dimensionality reduction"[tiab] OR "feature selection"[tiab] OR "library preparation"[tiab] OR "protocol*"[ti] OR alignment[tiab]) AND {SC} AND {B}'],
}
cand={}
for c,qs in Q.items():
    for q in qs:
        ids=es(q,80 if 'other' not in c else 50)
        for i in ids: cand.setdefault(i,set()).add(c)
        print(c,len(ids))
# landmark targeted searches
L={
"Luecken benchmarking atlas-level data integration":"Luecken[au] AND atlas-level integration[ti]",
"Saelens trajectory":"Saelens W[au] AND trajectory inference[ti]",
"Abdelaal annotation":"Abdelaal T[au] AND comparison automatic cell identification[tiab]",
"Squair DE":"Squair JW[au] AND differential expression[ti]",
"Xi Li doublet":"Xi NM[au] AND doublet[ti]",
"Dimitrov CCC":"Dimitrov D[au] AND cell-cell communication[ti]",
"Li spatial deconv 2022":"Li B[au] AND benchmark spatial deconvolution[tiab] AND Nat Methods[ta]",
"Li 2023 spatial":"Li H[au] AND benchmarking spatial deconvolution[tiab]",
"Pratapa GRN":"Pratapa A[au] AND gene regulatory[ti]",
"Ahlmann-Eltze perturbation":"Ahlmann-Eltze C[au] AND perturbation[ti]",
"Kedzierska":"Kedzierska KZ[au]",
"Tran batch":"Tran HTN[au] AND batch-effect correction[ti]",
"Avila Cobos deconv":"Avila Cobos F[au] AND deconvolution[ti]",
"Sturm deconv":"Sturm G[au] AND deconvolution[ti]",
"Soneson DE":"Soneson C[au] AND bias robustness scalability differential expression[ti]",
"Crowell muscat":"Crowell HL[au] AND multi-sample multi-condition[ti]",
"Huang Zhang ambient/ Janssen":"Janssen P[au] AND ambient RNA[ti]",
"Kim CNV benchmark":"benchmarking single-cell copy number[tiab]",
"Gao CNV benchmark":"single-cell CNV callers[tiab] AND benchmark*[tiab]",
"Liu Yu ccc":"Liu Z[au] AND evaluation cell-cell communication[tiab]",
"Hu spatial domain benchmark":"benchmarking clustering spatial transcriptomics[tiab]",
"SVG benchmark":"spatially variable genes[tiab] AND benchmark*[tiab]",
"Pasquini SVG":"spatially variable gene detection methods[tiab]",
"McCarthy BEELINE?":"BEELINE[tiab]",
"Kernfeld perturbation":"Kernfeld E[au] AND perturbation[tiab]",
"Csendes perturbation":"Csendes G[au]",
"Wenteler perteval":"PertEval-scFM[tiab]",
"Boiarsky":"Boiarsky R[au]",
"scEval foundation":"foundation models single-cell evaluation[tiab] AND zero-shot[tiab]",
"Zhao doublet/ambient":"ambient RNA removal methods comparison[tiab]",
"Weber tracing":"lineage tracing benchmark*[tiab]",
"Cassiopeia":"Jones MG[au] AND Cassiopeia[tiab]",
"mito clone benchmark":"mitochondrial variant clone benchmark*[tiab]",
"Sun deconv bulk":"Jin H[au] AND benchmark deconvolution[tiab]",
"Mereu protocols":"Mereu E[au] AND benchmarking single-cell RNA-sequencing protocols[ti]",
"Ding protocols":"Ding J[au] AND systematic comparison single-cell[ti]",
"Duo clustering":"Duò A[au]",
"Hou imputation":"Hou W[au] AND imputation[ti]",
"Zappia":"Zappia L[au] AND benchmark*[tiab]",
"DA benchmark":"differential abundance single-cell benchmark*[tiab]",
"Milo":"Dann E[au] AND differential abundance[ti]",
"velocity bench":"RNA velocity benchmark*[tiab]",
"drug response sc benchmark":"single-cell drug response prediction benchmark*[tiab]",
"CellMixS/kBET":"Büttner M[au] AND batch[ti]",
"Chazarra-Gil":"Chazarra-Gil R[au]",
"Huang annotation":"Huang Q[au] AND evaluation cell type annotation[ti]",
"tumour cell identification benchmark":"tumor cell identification[tiab] AND single-cell[tiab] AND benchmark*[tiab]",
"spatial Yan":"spatial transcriptomics benchmark*[ti]",
"cell typists Pasquini annotation spatial":"cell type annotation spatial transcriptomics benchmark*[tiab]",
"Chen GRN":"Chen S[au] AND Mar JC[au] AND gene regulatory network[tiab]",
"McCalla GRN":"McCalla SG[au]",
"Kang regulon":"single-cell gene regulatory network inference benchmark*[tiab]",
"scDNA cnv benchmark":"single-cell DNA copy number benchmark*[tiab]",
"phylogeny benchmark":"tumor phylogeny inference single-cell benchmark*[tiab]",
"perturbation benchmark":"genetic perturbation prediction benchmark*[tiab]",
"Wu perturbation":"PerturBench[tiab]",
"scPerturBench":"single-cell perturbation prediction methods benchmark*[tiab]",
"Liu Hecht foundation":"single-cell foundation model benchmark*[tiab]",
}
for k,q in L.items():
    ids=es(q,15)
    for i in ids: cand.setdefault(i,set()).add("LANDMARK:"+k)
    print(k,len(ids))
bc=pd.read_csv("prior/benchmark_classification.csv")
seed=bc[bc.is_benchmark==True].id.astype(str).tolist()
for i in seed: cand.setdefault(i,set()).add("SEED")
print(len(cand))
```

## Cell 4 · python (python) · ok

Running per-class PubMed benchmark searches

```python

import requests, time, json, pandas as pd, re
E="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
def es(q,n=60):
    for _ in range(3):
        try:
            r=requests.get(E+"esearch.fcgi",params=dict(db="pubmed",term=q,retmax=n,retmode="json",sort="relevance"),timeout=30)
            time.sleep(0.4); return r.json()["esearchresult"]["idlist"]
        except Exception as e: time.sleep(2)
    return []
B='(benchmark*[tiab] OR "systematic comparison"[tiab] OR "systematic evaluation"[tiab] OR "comprehensive evaluation"[tiab] OR "comparative analysis"[tiab] OR "performance evaluation"[tiab] OR "comparison of"[ti] OR evaluation[ti] OR benchmarking[ti] OR assessment[ti])'
SC='(single-cell[tiab] OR "single cell"[tiab] OR scRNA-seq[tiab] OR spatial transcriptomic*[tiab])'
Q={
"CNV inference & malignant-cell calling":f'(copy number[tiab] OR CNV[tiab] OR aneuploid*[tiab] OR malignant cell*[tiab] OR inferCNV[tiab] OR copyKAT[tiab]) AND {SC} AND {B}',
"bulk deconvolution":f'(deconvolution[tiab] OR "cell type proportion*"[tiab] OR "cellular composition"[tiab]) AND (bulk[tiab] OR tumor[tiab]) AND {B} AND (single-cell[tiab] OR reference[tiab] OR transcriptom*[tiab])',
"data integration/batch correction":f'("batch correction"[tiab] OR "batch effect*"[tiab] OR "data integration"[tiab] OR integration[ti]) AND {SC} AND {B}',
"cell-type annotation & label transfer":f'("cell type annotation"[tiab] OR "cell-type annotation"[tiab] OR "cell type identification"[tiab] OR "label transfer"[tiab] OR "cell type classification"[tiab] OR classifier*[ti]) AND {SC} AND {B}',
"cell-cell communication":f'("cell-cell communication"[tiab] OR "cell-cell interaction*"[tiab] OR "ligand-receptor"[tiab] OR "intercellular communication"[tiab]) AND {B}',
"spatial (deconvolution, domains, SVG)":f'(spatial transcriptomic*[tiab] OR spatially resolved[tiab] OR Visium[tiab]) AND (deconvolution[tiab] OR "spatial domain*"[tiab] OR clustering[tiab] OR "spatially variable"[tiab] OR "cell segmentation"[tiab] OR imputation[tiab] OR alignment[tiab] OR mapping[tiab]) AND {B}',
"GRN/regulon inference":f'("gene regulatory network*"[tiab] OR GRN[tiab] OR regulon*[tiab] OR "network inference"[tiab]) AND {SC} AND {B}',
"lineage tracing/mtDNA clone calling":f'("lineage tracing"[tiab] OR mitochondrial[tiab] OR mtDNA[tiab] OR "clone calling"[tiab] OR "clonal"[tiab] OR "somatic mutation*"[tiab] OR "variant calling"[tiab] OR SNV[tiab]) AND {SC} AND {B}',
"clonal phylogeny/scDNA":f'("single-cell DNA"[tiab] OR scDNA-seq[tiab] OR "tumor phylogen*"[tiab] OR "phylogeny inference"[tiab] OR "intratumor heterogeneity"[tiab] OR "single-cell whole genome"[tiab] OR "whole genome amplification"[tiab]) AND {B}',
"differential abundance & differential expression":f'("differential expression"[tiab] OR "differential abundance"[tiab] OR "differentially expressed"[tiab] OR pseudobulk[tiab] OR pseudoreplication[tiab] OR "compositional"[tiab]) AND {SC} AND {B}',
"doublet detection & ambient RNA":f'(doublet*[tiab] OR multiplet*[tiab] OR "ambient RNA"[tiab] OR demultiplex*[tiab] OR "empty droplet*"[tiab] OR "quality control"[ti]) AND {SC} AND {B}',
"trajectory inference":f'(trajectory[tiab] OR pseudotime[tiab] OR "RNA velocity"[tiab] OR "lineage inference"[tiab]) AND {SC} AND {B}',
"perturbation-response prediction":f'(perturbation*[tiab] OR Perturb-seq[tiab] OR "CRISPR screen*"[tiab]) AND (prediction[tiab] OR predict*[tiab] OR model*[tiab]) AND {SC} AND {B}',
"single-cell foundation models":f'("foundation model*"[tiab] OR scGPT[tiab] OR Geneformer[tiab] OR "large language model*"[tiab] OR "pretrained"[tiab] OR "zero-shot"[tiab] OR scFoundation[tiab]) AND {SC} AND (evaluat*[tiab] OR {B})',
"drug-response prediction":f'("drug response"[tiab] OR "drug sensitivity"[tiab] OR "drug resistance prediction"[tiab] OR "drug response prediction"[tiab]) AND {SC} AND (predict*[tiab]) AND {B}',
"other":f'(clustering[tiab] OR normalization[tiab] OR imputation[tiab] OR "dimensionality reduction"[tiab] OR "feature selection"[tiab] OR "library preparation"[tiab] OR protocol*[ti]) AND {SC} AND {B}',
}
cand={}
for c,q in Q.items():
    ids=es(q,80 if c!='other' else 50)
    for i in ids: cand.setdefault(i,set()).add(c)
    print(c,len(ids))
L={
"Luecken integration":"Luecken[au] AND atlas-level integration[ti]",
"Saelens trajectory":"Saelens W[au] AND trajectory inference[ti]",
"Abdelaal annotation":"Abdelaal T[au] AND automatic cell identification[tiab]",
"Squair DE":"Squair JW[au] AND differential expression[ti]",
"Xi Li doublet":"Xi NM[au] AND doublet[ti]",
"Dimitrov CCC":"Dimitrov D[au] AND cell-cell communication[ti]",
"Li spatial deconv":"Li B[au] AND benchmark spatial deconvolution[tiab]",
"Li H spatial":"Li H[au] AND benchmarking spatial[tiab] AND deconvolution[tiab]",
"Pratapa GRN":"Pratapa A[au] AND gene regulatory[ti]",
"Ahlmann-Eltze perturbation":"Ahlmann-Eltze C[au] AND perturbation[tiab]",
"Kedzierska":"Kedzierska KZ[au]",
"Tran batch":"Tran HTN[au] AND batch-effect correction[ti]",
"Avila Cobos deconv":"Avila Cobos F[au] AND deconvolution[ti]",
"Sturm deconv":"Sturm G[au] AND deconvolution[ti]",
"Soneson DE":"Soneson C[au] AND differential expression analysis[ti]",
"Crowell muscat":"Crowell HL[au] AND multi-sample multi-condition[ti]",
"Janssen ambient":"Janssen P[au] AND ambient RNA[ti]",
"CNV bench1":"benchmarking single-cell copy number[tiab]",
"CNV bench2":"copy number variation inference scRNA-seq benchmark*[tiab]",
"CCC eval":"evaluation cell-cell communication inference methods[tiab]",
"domain bench":"benchmarking spatial clustering methods[tiab]",
"SVG bench":"spatially variable genes[tiab] AND benchmark*[tiab]",
"Kernfeld":"Kernfeld E[au] AND perturbation[tiab]",
"Csendes":"Csendes G[au] AND perturbation[tiab]",
"Boiarsky":"Boiarsky R[au]",
"FM zero-shot":"foundation models single-cell zero-shot[tiab]",
"ambient comparison":"ambient RNA[tiab] AND comparison[tiab] AND single-cell[tiab] AND methods[tiab]",
"lineage tracing bench":"lineage tracing[tiab] AND benchmark*[tiab] AND reconstruction[tiab]",
"mito clone":"mitochondrial variants[tiab] AND clone*[tiab] AND benchmark*[tiab]",
"Jin deconv":"Jin H[au] AND Liu Z[au] AND deconvolution[tiab]",
"Mereu protocols":"Mereu E[au] AND benchmarking single-cell RNA-sequencing protocols[ti]",
"Ding protocols":"Ding J[au] AND systematic comparison single-cell[ti]",
"Duo clustering":"Duò A[au] AND clustering[tiab]",
"Hou imputation":"Hou W[au] AND imputation[ti]",
"DA bench":"differential abundance[tiab] AND single-cell[tiab] AND benchmark*[tiab]",
"velocity bench":"RNA velocity[tiab] AND benchmark*[tiab]",
"drug sc bench":"single-cell[tiab] AND drug response prediction[tiab] AND benchmark*[tiab]",
"Buttner":"Büttner M[au] AND batch[ti]",
"Chazarra-Gil":"Chazarra-Gil R[au]",
"tumor cell id":"malignant cells[tiab] AND single-cell[tiab] AND benchmark*[tiab]",
"spatial bench ti":"spatial transcriptomics[ti] AND benchmark*[ti]",
"spatial annot":"cell type annotation spatial transcriptomics benchmark*[tiab]",
"McCalla GRN":"McCalla SG[au]",
"GRN bench":"gene regulatory network inference[tiab] AND single-cell[tiab] AND benchmark*[tiab]",
"scDNA cnv":"single-cell DNA[tiab] AND copy number[tiab] AND benchmark*[tiab]",
"phylogeny bench":"phylogeny[tiab] AND single-cell[tiab] AND tumor[tiab] AND benchmark*[tiab]",
"perturb bench":"perturbation prediction[tiab] AND benchmark*[tiab] AND single-cell[tiab]",
"FM bench":"foundation model*[tiab] AND single-cell[tiab] AND benchmark*[ti]",
"Huang ambient/doublet":"doublet detection[tiab] AND benchmark*[tiab]",
"Tian mixology":"Tian L[au] AND mixture control experiments[tiab]",
"Hao cancer annotation":"cell type annotation[tiab] AND tumor[tiab] AND benchmark*[tiab]",
"cnv scDNA vs WGS":"single-cell copy number[tiab] AND whole genome[tiab] AND comparison[tiab] AND methods[tiab]",
}
for k,q in L.items():
    ids=es(q,15)
    for i in ids: cand.setdefault(i,set()).add("LANDMARK:"+k)
    print(k,len(ids),end='; ')
bc=pd.read_csv("prior/benchmark_classification.csv")
seed=bc[bc.is_benchmark==True].id.astype(str).tolist()
for i in seed: cand.setdefault(i,set()).add("SEED")
print("\nTOTAL",len(cand))
```

## Cell 5 · python (python) · ok

Adding missing landmark searches and fetching records

```python

extra={
"Li B 2022 spatial integration":'"Benchmarking spatial and single-cell transcriptomics integration methods"[ti]',
"Janssen background noise":'background noise[ti] AND single-cell expression data[ti]',
"Nguyen DE integration":'benchmarking integration of single-cell differential expression[ti]',
"Avila Cobos 2020":'"Benchmarking of cell type deconvolution pipelines"[ti]',
"mito clone2":'mitochondrial[tiab] AND single-cell[tiab] AND lineage[tiab] AND benchmark*[tiab]',
"cnv3":'(inferCNV[tiab] OR CopyKAT[tiab] OR Numbat[tiab] OR CaSpER[tiab]) AND comparison[tiab]',
"Liu CCC 2022":'Liu Z[au] AND cell-cell communication[ti] AND evaluation[ti]',
"Wang spatial domain":'spatial domain[tiab] AND benchmark*[ti]',
"Yuan spatial clustering bench":'benchmarking spatial clustering[ti]',
"Zhang perturb":'"Benchmarking" [ti] AND perturbation[ti]',
"Kedzierska zero":'zero-shot[ti] AND single-cell foundation models[ti]',
"Liu scEval":'evaluating[ti] AND single-cell foundation models[ti]',
"Weber DS bench":'differential state[tiab] AND benchmark*[tiab] AND single-cell[tiab]',
"Zimmerman pseudoreplication":'Zimmerman KD[au] AND pseudoreplication[ti]',
"Hao CNV benchmark 2025?":'copy number[ti] AND single-cell[ti] AND benchmark*[ti]',
}
for k,q in extra.items():
    ids=es(q,10)
    for i in ids: cand.setdefault(i,set()).add("LANDMARK:"+k)
    print(k,len(ids),end='; ')
import xml.etree.ElementTree as ET
ids=list(cand)
recs={}
for s in range(0,len(ids),200):
    chunk=ids[s:s+200]
    for _ in range(3):
        try:
            r=requests.post(E+"efetch.fcgi",data=dict(db="pubmed",id=",".join(chunk),retmode="xml"),timeout=120); break
        except Exception: time.sleep(3)
    root=ET.fromstring(r.content)
    for a in root.findall(".//PubmedArticle"):
        pm=a.findtext(".//MedlineCitation/PMID")
        art=a.find(".//Article")
        title="".join(art.find("ArticleTitle").itertext()) if art.find("ArticleTitle") is not None else ""
        ab=" ".join("".join(x.itertext()) for x in art.findall(".//Abstract/AbstractText"))
        jr=a.findtext(".//Journal/ISOAbbreviation") or a.findtext(".//Journal/Title")
        yr=a.findtext(".//JournalIssue/PubDate/Year") or (a.findtext(".//JournalIssue/PubDate/MedlineDate") or "")[:4] or a.findtext(".//ArticleDate/Year")
        au=a.find(".//AuthorList/Author")
        fa=""
        if au is not None:
            fa=(au.findtext("LastName") or au.findtext("CollectiveName") or "")+(" "+au.findtext("Initials") if au.findtext("Initials") else "")
        doi=""
        for x in a.findall(".//PubmedData/ArticleIdList/ArticleId"):
            if x.get("IdType")=="doi": doi=x.text
        pts=[p.text for p in a.findall(".//PublicationType")]
        recs[pm]=dict(pmid=pm,doi=doi,first_author=fa,year=yr,journal=jr,title=title,abstract=ab,pubtypes=";".join(pts),sources=";".join(sorted(cand.get(pm,[]))))
    time.sleep(0.5)
R=pd.DataFrame(recs.values());print("\n",len(ids),len(R),(R.abstract.str.len()<50).sum())
R.to_pickle("cand.pkl")
```

## Cell 6 · python (python) · ok

Heuristic prefilter of candidate records

```python

R["txt"]=(R.title+" "+R.abstract)
kw=R.txt.str.contains(r"benchmark|systematic(ally)? (compar|evaluat|assess)|comprehensive(ly)? (compar|evaluat|assess)|we (compared|evaluated|assessed)|comparison of|comparative (analysis|evaluation|study)|evaluation of|performance of (\w+ ){0,3}(methods|tools|algorithms)|head-to-head",case=False,regex=True)
dom=R.txt.str.contains(r"single.cell|scRNA|snRNA|spatial|deconvol|scDNA|cell type|single.nucle",case=False,regex=True)
seedm=R.sources.str.contains("SEED"); lm=R.sources.str.contains("LANDMARK")
keep=(kw&dom)|seedm|lm
print(keep.sum(), seedm.sum(), lm.sum())
R2=R[keep].copy(); print((R2.abstract.str.len()).mean())
```

## Cell 7 · python (python) · FAILED

LLM screening of candidates (stage 1)

```python

scr_tool={"name":"screen","description":"screen record","input_schema":{"type":"object","properties":{
 "is_benchmark":{"type":"boolean","description":"True if the paper's PRIMARY contribution is a comparative evaluation/benchmark of >=2 existing computational methods (or of experimental protocols/platforms with computational readouts) — NOT a new method paper that merely compares against baselines, NOT a review without new comparisons, NOT a biological study."},
 "method_class":{"type":"string","enum":["CNV inference & malignant-cell calling","bulk deconvolution","data integration/batch correction","cell-type annotation & label transfer","cell-cell communication","spatial (deconvolution, domains, SVG)","GRN/regulon inference","lineage tracing/mtDNA clone calling","clonal phylogeny/scDNA","differential abundance & differential expression","doublet detection & ambient RNA","trajectory inference","perturbation-response prediction","single-cell foundation models","drug-response prediction","other single-cell preprocessing/analysis","not single-cell relevant"]}},
 "required":["is_benchmark","method_class"]}}
reqs=[{"prompt":f"Title: {t}\nAbstract (truncated): {a[:700]}","tools":[scr_tool],"tool_choice":{"type":"tool","name":"screen"},"max_tokens":120} for t,a in zip(R2.title,R2.abstract)]
out=[]
for s in range(0,len(reqs),500):
    out+=host.llm(reqs[s:s+500],max_concurrency=24)
R2["s_bench"]=[o.get("tool_use",{}).get("input",{}).get("is_benchmark") if "error" not in o else None for o in out]
R2["s_class"]=[o.get("tool_use",{}).get("input",{}).get("method_class") if "error" not in o else None for o in out]
print(R2.s_bench.value_counts(dropna=False)); print(R2[R2.s_bench==True].s_class.value_counts())
print(pd.crosstab(R2.sources.str.contains("SEED"),R2.s_bench))
R2.to_pickle("R2.pkl")
```

## Cell 8 · python (python) · ok

Testing whether host.llm still available

```python

try: print(host.llm("Say ok",max_tokens=5)["text"])
except Exception as e: print(e)
print(len(out))
```

## Cell 9 · python (python) · ok

Checking stage-1 screening results obtained

```python

err=sum("error" in o for o in out);print(err)
sub=R2.iloc[:500].copy()
sub["s_bench"]=[o.get("tool_use",{}).get("input",{}).get("is_benchmark") if "error" not in o and o.get("tool_use") else None for o in out]
sub["s_class"]=[o.get("tool_use",{}).get("input",{}).get("method_class") if "error" not in o and o.get("tool_use") else None for o in out]
print(sub.s_bench.value_counts(dropna=False))
print(sub[sub.s_bench==True].s_class.value_counts())
print(pd.crosstab(sub.sources.str.contains("SEED"),sub.s_bench.astype(str)))
```

## Cell 10 · python (python) · ok

Rule-based benchmark scoring of candidates

```python

R2=R2.copy()
R2["llm_bench"]=None; R2["llm_class"]=None
R2.loc[sub.index,"llm_bench"]=sub.s_bench; R2.loc[sub.index,"llm_class"]=sub.s_class
t=R2.title.str.lower(); a=R2.abstract.str.lower()
tb=t.str.contains(r"benchmark|comparison|comparative|compar(e|ing)|evaluat|assess|systematic|how (well|good|reliable)|performance of|revisit|pitfall|guideline|best practice|critical|limitations|fail|robustness of|reproducib|versus| vs\.? |head-to-head|survey of methods|which (method|tool)|are .* (better|ready)|do .* (outperform|capture)",regex=True)
ab=a.str.contains(r"we (benchmark|systematically|comprehensively|compared|evaluated|assessed|performed a (systematic|comprehensive|benchmark))|benchmark(ed|ing)? (of )?(\w+ ){0,2}(\d+|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|eighteen|twenty)\b|(\d+|six|seven|eight|nine|ten|eleven|twelve|fourteen|sixteen) (state-of-the-art |popular |widely used |existing |computational |published )*(methods|tools|algorithms|approaches|pipelines|packages|models|software)",regex=True)
neg=t.str.contains(r"^(a |an )?(novel|new)\b|: a (novel|new|tool|method|framework|deep|robust|scalable|fast|unified|computational|bayesian|statistical|python|r package)|enables|reveals|atlas of|landscape of|identif(y|ies)|we present",regex=True)
R2["rule"]=(tb.astype(int)*2+ab.astype(int)-neg.astype(int)*2)
R2["seed"]=R2.sources.str.contains("SEED")
print(pd.crosstab(R2.rule,R2.llm_bench.astype(str)))
```

## Cell 11 · python (python) · ok

Building manual review pool and writing titles

```python

lm=R2.sources.str.contains("LANDMARK")
pool=R2[(R2.llm_bench==True)|R2.seed|lm|((R2.llm_bench.isna())&(R2.rule>=0))|((R2.llm_bench==False)&(R2.rule>=2))].copy()
pool=pool.sort_values("pmid").reset_index(drop=True)
print(len(pool))
with open("pool_titles.txt","w") as f:
    for i,r in pool.iterrows():
        tag=("S" if r.seed else "")+("L" if "LANDMARK" in r.sources else "")+({True:"+",False:"-"}.get(r.llm_bench,"?"))
        f.write(f"{i}|{tag}|{r.year}|{r.title[:150]}\n")
pool.to_pickle("pool.pkl")
```

## Cell 12 · python (python) · ok

Extra targeted searches for missing landmarks

```python

more={
"Liu CCC spatial":'Evaluation of cell-cell interaction methods by integrating single-cell RNA sequencing data with spatial information[ti]',
"Sun dimred":'accuracy, robustness and scalability of dimensionality reduction methods for single-cell RNA-seq analysis[ti]',
"Boiarsky FM":'deep dive into single-cell RNA sequencing foundation models[ti]',
"Csendes":'Csendes G[au] AND perturbation[tiab]',
"Wenteler":'Wenteler A[au]',
"Bendidi":'transcriptomics foundation models perturbation[tiab] AND benchmark*[tiab]',
"Kuipers phylo":'single-cell[tiab] AND phylogen*[tiab] AND mutation*[tiab] AND benchmark*[ti]',
"mtDNA variant callers":'mitochondrial[ti] AND variant[ti] AND single-cell[ti] AND (benchmark*[ti] OR comparison[ti] OR evaluation[ti])',
"Huang ccc bench":'cell-cell communication[ti] AND benchmark*[ti]',
"annotation bench cancer":'cell type annotation[ti] AND (benchmark*[ti] OR evaluation[ti] OR comparison[ti])',
"integration bench":'integration[ti] AND single-cell[ti] AND benchmark*[ti]',
"DE bench":'differential expression[ti] AND single-cell[ti] AND (benchmark*[ti] OR comparison[ti] OR evaluation[ti])',
"trajectory bench":'trajectory[ti] AND (benchmark*[ti] OR comparison[ti] OR evaluation[ti])',
"GRN bench ti":'gene regulatory network*[ti] AND single-cell[tiab] AND (benchmark*[ti] OR evaluation[ti])',
"drug bench":'drug response[ti] AND single-cell[ti] AND (benchmark*[ti] OR evaluation[ti] OR comparison[ti])',
"malignant id":'(malignant[ti] OR tumor cells[ti] OR tumour cells[ti] OR cancer cells[ti]) AND single-cell[ti] AND (benchmark*[ti] OR comparison[ti] OR evaluation[ti])',
"lineage tree bench":'lineage[ti] AND tree*[ti] AND (benchmark*[tiab]) AND CRISPR[tiab]',
"FM eval":'foundation model*[ti] AND single-cell[ti] AND (evaluat*[ti] OR benchmark*[ti] OR assess*[ti])',
"spatial deconv bench":'spatial[ti] AND deconvolution[ti] AND benchmark*[ti]',
"doublet ambient bench":'(doublet[ti] OR ambient[ti] OR demultiplexing[ti]) AND benchmark*[ti]',
"cnv scdna bench":'(copy number[ti] OR CNV[ti]) AND single-cell[ti] AND (benchmark*[ti] OR comparison[ti] OR evaluation[ti] OR assessment[ti])',
}
newids={}
for k,q in more.items():
    for i in es(q,25):
        if i not in recs: newids.setdefault(i,set()).add("LANDMARK:"+k)
        else: cand.setdefault(i,set()).add("LANDMARK:"+k)
print(len(newids))
ids=list(newids)
r=requests.post(E+"efetch.fcgi",data=dict(db="pubmed",id=",".join(ids),retmode="xml"),timeout=120)
root=ET.fromstring(r.content)
new=[]
for a in root.findall(".//PubmedArticle"):
    pm=a.findtext(".//MedlineCitation/PMID"); art=a.find(".//Article")
    title="".join(art.find("ArticleTitle").itertext())
    ab=" ".join("".join(x.itertext()) for x in art.findall(".//Abstract/AbstractText"))
    jr=a.findtext(".//Journal/ISOAbbreviation") or a.findtext(".//Journal/Title")
    yr=a.findtext(".//JournalIssue/PubDate/Year") or (a.findtext(".//JournalIssue/PubDate/MedlineDate") or "")[:4] or a.findtext(".//ArticleDate/Year")
    au=a.find(".//AuthorList/Author"); fa=""
    if au is not None: fa=(au.findtext("LastName") or au.findtext("CollectiveName") or "")+(" "+au.findtext("Initials") if au.findtext("Initials") else "")
    doi=next((x.text for x in a.findall(".//PubmedData/ArticleIdList/ArticleId") if x.get("IdType")=="doi"),"")
    new.append(dict(pmid=pm,doi=doi,first_author=fa,year=yr,journal=jr,title=title,abstract=ab,sources=";".join(newids[pm])))
N=pd.DataFrame(new).sort_values("pmid").reset_index(drop=True)
for i,r_ in N.iterrows(): print(i,r_.year,r_.title[:120])
N.to_pickle("new.pkl")
```

## Cell 13 · python (python) · ok

Assembling selected records with class labels

```python

P="""1 SCDNA,9 SCDNA,12 SCDNA,20 SCDNA,24 SCDNA,34 SCDNA,40 SCDNA,50 DADE,51 OTHER,52 SCDNA,58 OTHER,60 SCDNA,61 OTHER,63 TRAJ,69 INT,77 TRAJ,78 OTHER,84 OTHER,90 ANN,91 DECONV,93 ANN,95 DECONV,97 GRN,99 INT,106 OTHER,112 OTHER,118 OTHER,119 OTHER,124 SCDNA,130 OTHER,132 OTHER,134 DECONV,136 DECONV,139 DBL,140 OTHER,141 ANN,144 INT,147 INT,148 OTHER,149 DADE,153 GRN,155 DECONV,161 SCDNA,166 LIN,170 OTHER,173 DECONV,175 DBL,177 SCDNA,182 DADE,188 OTHER,190 INT,193 OTHER,195 OTHER,198 DBL,212 SPA,213 SPA,216 CCC,221 DECONV,225 CCC,226 OTHER,243 OTHER,245 ANN,249 DECONV,255 SPA,256 OTHER,261 SPA,266 ANN,267 ANN,269 OTHER,271 GRN,278 GRN,282 OTHER,286 GRN,287 DADE,290 SPA,291 DADE,293 OTHER,296 SCDNA,308 CCC,309 DBL,310 GRN,315 DBL,328 PERT,333 SPA,340 CCC,341 DBL,342 INT,344 DECONV,353 OTHER,358 INT,364 SPA,366 SPA,370 OTHER,373 DADE,379 SPA,384 OTHER,387 OTHER,395 DECONV,396 SCDNA,398 INT,401 FM,403 SPA,404 INT,405 OTHER,412 OTHER,413 OTHER,414 DECONV,423 OTHER,427 DECONV,429 FM,432 SPA,439 DBL,443 DECONV,445 SPA,463 ANN,464 SPA,467 LIN,471 CNV,479 OTHER,483 INT,484 PERT,490 DBL,523 OTHER,528 INT,529 SPA,533 ANN,535 SPA,540 DECONV,543 DECONV,544 DBL,548 DBL,553 CNV,554 SPA,558 SPA,563 SPA,564 SPA,565 PERT,571 OTHER,575 SPA,579 FM,580 DECONV,581 PERT,587 DRUG,596 DECONV,599 SPA,602 CNV,615 DBL,620 PERT,626 FM,630 SPA,632 SPA,633 SCDNA,637 SPA,643 SPA,644 SPA,646 SPA,649 CNV,651 FM,655 INT,657 SPA,663 CNV,672 OTHER,673 PERT,676 SPA,680 FM,681 OTHER,693 DRUG,695 DRUG,696 PERT,697 OTHER,700 OTHER,702 ANN,703 DECONV,713 PERT,715 SPA,719 ANN,721 TRAJ,725 FM,731 DECONV,734 SPA,738 DBL,745 FM,751 FM,749 OTHER,754 SPA,765 ANN,766 TRAJ,767 SPA,769 SPA,777 CNV,779 SPA,782 INT,783 OTHER,792 PERT,795 TRAJ,799 PERT,803 LIN,804 OTHER,805 TRAJ,817 FM,833 GRN,834 ANN,840 OTHER,846 FM,861 SPA,866 DBL,868 ANN,869 PERT,878 DECONV,889 CNV,890 DBL,893 PERT"""
NP="12 OTHER,14 DADE,21 CCC,24 INT,29 INT,34 GRN,39 INT,43 PERT,46 INT,49 INT,50 INT,51 FM,54 FM,55 INT,56 PERT,59 ANN"
CL={"CNV":"CNV inference & malignant-cell calling","DECONV":"bulk deconvolution","INT":"data integration/batch correction","ANN":"cell-type annotation & label transfer","CCC":"cell-cell communication","SPA":"spatial (deconvolution, domains, SVG, platforms)","GRN":"GRN/regulon inference","LIN":"lineage tracing/mtDNA clone calling","SCDNA":"clonal phylogeny/scDNA","DADE":"differential abundance & differential expression","DBL":"doublet detection, demultiplexing & ambient RNA","TRAJ":"trajectory inference & RNA velocity","PERT":"perturbation-response prediction","FM":"single-cell foundation models","DRUG":"drug-response prediction","OTHER":"other preprocessing/platform benchmarks"}
rows=[]
for tok in P.split(","):
    i,c=tok.split(); r_=pool.loc[int(i)].to_dict(); r_["method_class"]=CL[c]; rows.append(r_)
for tok in NP.split(","):
    i,c=tok.split(); r_=N.loc[int(i)].to_dict(); r_["method_class"]=CL[c]; rows.append(r_)
C=pd.DataFrame(rows)
C["nt"]=C.title.str.lower().str.replace(r"[^a-z0-9]","",regex=True)
dup=C.groupby("nt").pmid.apply(list)
print(len(C), C.nt.nunique())
print([v for v in dup if len(v)>1])
```

## Cell 14 · python (python) · ok

Inspecting duplicate records' journals

```python

for v in [v for v in dup if len(v)>1]:
    print(C[C.pmid.isin(v)][["pmid","year","journal","title"]].to_string(header=False,index=False,max_colwidth=60))
print(C[C.title.str.contains("Benchmarking spatial and single-cell")][["pmid","year","journal","doi"]])
print(C.journal.value_counts().head(25))
```

## Cell 15 · python (python) · ok

Deduplicating preprint/journal versions

```python

pre=C.journal.isin(["bioRxiv","ArXiv","Res Sq","medRxiv"])
C["is_preprint"]=pre
C["nt2"]=C.nt.str[:45]
C=C.sort_values(["is_preprint","year"],ascending=[True,False])
grp=C.groupby("nt2")
keep=[];alt={}
for k,g in grp:
    keep.append(g.index[0]); alt[g.index[0]]=";".join(g.pmid.iloc[1:])
D=C.loc[keep].copy(); D["other_version_pmids"]=[alt[i] for i in D.index]
print(len(D)); print(D[D.other_version_pmids!=""][["pmid","journal","other_version_pmids","title"]].to_string(max_colwidth=50))
print(D[D.title.str.contains("orecasting|differential abundance methods|35577955")][["pmid","journal","title"]])
pt=R.set_index("pmid").pubtypes
print(pt.get("35577955"), pt.get("35577954"))
```

## Cell 16 · python (python) · ok

Rule-based field extraction from abstracts

```python

D.loc[D.pmid=="41250104","other_version_pmids"]="37577640"; D=D[D.pmid!="37577640"].copy()
TOOLS="""inferCNV infercnv CopyKAT copyKAT Numbat CaSpER HoneyBADGER SCEVAN sciCNV CONICSmat XClone SCICoNE Ginkgo HMMcopy SCOPE AneuFinder CHISEL Alleloscope epiAneufinder SCYN SeCNV scAbsolute
CIBERSORT CIBERSORTx MuSiC BisqueRNA Bisque EPIC quanTIseq xCell MCP-counter TIMER DWLS SCDC BayesPrism AutoGeneS NNLS FARDEEP dtangle DeconRNASeq BayICE CPM Scaden TAPE ABIS ESTIMATE PUREE DeMixT ABSOLUTE MethylCIBERSORT EpiDISH MeDeCom InstaPrism
Harmony Seurat scVI scANVI Scanorama BBKNN fastMNN mnnCorrect MNN LIGER rliger ComBat Combat limma scGen trVAE SAUCIE Conos DESC scMerge BBKNN SCALEX scPoli totalVI MultiVI GLUE Symphony
SingleR scmap CHETAH scPred Garnett CellAssign SCINA CellTypist scArches Azimuth scDeepSort scBERT ACTINN SingleCellNet scClassify scSorter CellMarker scCATCH sc-type ScType clustifyr SVM ItClust
CellPhoneDB CellChat NATMI iTALK Connectome NicheNet LIANA SingleCellSignalR CytoTalk scTensor CellCall ICELLNET Domino COMMOT
cell2location RCTD SPOTlight stereoscope Tangram SpatialDWLS DestVI CARD STdeconvolve Seurat novoSpaRc SpaOTsc gimVI SpaGE BayesSpace SpaGCN STAGATE GraphST BASS DR.SC SEDR CCST stLearn SpatialDE SPARK SPARK-X nnSVG Moran SOMDE scGCO trendsceek MERINGUE Giotto Hotspot PASTE STalign
GENIE3 GRNBoost2 SCENIC PIDC SCODE SINCERITIES LEAP PPCOR SCRIBE GRISLI SCNS CellOracle Pando SCENIC+ FigR Dictys
Cassiopeia LinTIMaT startle mgatk MQuad Vireo cellsnp-lite souporcell demuxlet freemuxlet scSplit MAESTER
SCITE SiFit SPhyR OncoNEM BnpC SCIPhI Monovar SCcaller ROBUST PhylEx MEDALT
DESeq2 edgeR MAST limma-voom Wilcoxon muscat Milo miloR DA-seq Cydar scCODA propeller MELD Cacoa CNA NEBULA
Scrublet DoubletFinder scDblFinder cxds bcds hybrid DoubletDetection solo Solo scds DoubletDecon SoupX DecontX CellBender scAR FastCAR EmptyDrops HTODemux MULTIseqDemux GMM-Demux demuxEM hashedDrops
Monocle Monocle2 Monocle3 Slingshot PAGA TSCAN DPT Palantir scVelo velocyto CellRank SCORPIUS
GEARS CPA scGPT Geneformer scFoundation UCE scBERT CellFM GenePT linear PRnet chemCPA biolord
scDEAL SCAD scDrug DrugFormer Beyondcell""".split()
TOOLS=sorted(set(TOOLS),key=len,reverse=True)
num_words={"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,"eight":8,"nine":9,"ten":10,"eleven":11,"twelve":12,"thirteen":13,"fourteen":14,"fifteen":15,"sixteen":16,"seventeen":17,"eighteen":18,"nineteen":19,"twenty":20,"thirty":30,"forty":40,"fifty":50}
pat_n=re.compile(r"\b(\d{1,3}|"+"|".join(num_words)+r")\s+(?:(?:[\w\-]+)\s+){0,4}?(methods|tools|algorithms|approaches|pipelines|packages|models|software|callers|classifiers|programs|frameworks|strategies|platforms|technologies|protocols|kits|workflows|combinations)\b",re.I)
def ntools(t):
    vals=[]
    for m in pat_n.finditer(t):
        w=m.group(1).lower(); v=int(w) if w.isdigit() else num_words[w]
        ctx=t[max(0,m.start()-80):m.start()].lower()
        if 2<=v<=500: vals.append(v)
    return max(vals) if vals else "unclear"
def tools(t):
    found=[]
    for x in TOOLS:
        if re.search(r"(?<![\w\-])"+re.escape(x)+r"(?![\w\-])",t) and x.lower() not in [f.lower() for f in found]:
            if x in ("linear","CNA","hybrid","SVM","Moran","ROBUST","ESTIMATE","TIMER","EPIC","CPM","MNN","limma","Combat","CPA","Seurat","Solo","solo") and not re.search(r"(?<![\w\-])"+re.escape(x)+r"(?![\w\-])",t.replace(". ","|")): continue
            found.append(x)
    bad={"linear","hybrid","ROBUST","ESTIMATE","CNA"}
    found=[f for f in found if f not in bad or f.isupper() and f in ("ESTIMATE",)]
    return "; ".join(found)
GT=[("simulation",r"simulat|synthetic (data|dataset|benchmark)|in silico (mixture|data)|pseudo-?bulk mixture|artificial (mixture|bulk)|splatter|\bdyngen\b|SERGIO|BoolODE"),
    ("cell-line mixture/controlled design",r"cell[- ]line mix|mixture (control|experiment|of cell lines)|mixtures? of (\w+ ){0,3}cell lines|spike-in|ERCC|known (cell[- ]type )?proportions|reference samples|controlled (heterogeneity|mixture)"),
    ("genotype multiplexing",r"genetic(ally)? demultiplex|genotype[- ]based|SNP[- ]based|demuxlet|souporcell|multiplexed donors|natural genetic variation|freemuxlet|cell hashing|hashtag|species[- ]mixing|barnyard|synthetic (DNA )?barcodes"),
    ("orthogonal assay",r"whole[- ]exome|\bWES\b|whole[- ]genome sequencing|\bWGS\b|scDNA|single-cell DNA|CITE-seq|smFISH|\bFISH\b|MERFISH|seqFISH|flow cytometry|\bFACS\b|immunohistochem|\bIHC\b|ChIP-seq|\bChIP\b|Perturb-seq|CRISPR|lineage barcod|matched (bulk|DNA|genomic)|orthogonal|histolog|pathologist|karyotyp|SNP array|multi-omic(s)? (data|dataset)|paired (DNA|ATAC|protein)|protein (expression|measurement)|imaging[- ]based"),
    ("expert annotation",r"manual(ly)? annotat|expert|author[- ]provided|curated (labels|annotation)|published (labels|annotations)|original annotation|gold[- ]standard (labels|annotation)|annotated (by|labels)"),
    ("consensus-only",r"consensus (among|of|between) (methods|tools)|agreement (among|between) (methods|tools)|concordance (among|between) (methods|tools)|absence of (a )?ground truth|without (a )?ground truth|lack of ground truth"),
]
MET={"ARI":r"\bARI\b|adjusted rand","NMI":r"\bNMI\b|normalized mutual","AUROC":r"AUROC|AUC\b|area under the (receiver|ROC|curve)|ROC","AUPRC":r"AUPRC|AUPR|precision-recall|AUC-PR","F1":r"\bF1|F-score|F-measure","accuracy":r"accuracy","precision/recall":r"precision|recall|sensitivity|specificity","RMSE/MSE":r"RMSE|\bMSE\b|mean squared error|root mean","correlation":r"correlation|Pearson|Spearman|\bPCC\b","JSD":r"JSD|Jensen-Shannon","kBET/LISI/ASW":r"kBET|LISI|iLISI|cLISI|silhouette|\bASW\b","FDR/type I error":r"false discovery|\bFDR\b|type I error|false positive rate|\bFPR\b","runtime/scalability":r"runtime|running time|computational (cost|time|efficiency)|scalab|memory","stability/reproducibility":r"stabilit|reproducib","usability":r"usability|user-friendl|documentation","Moran's I/spatial coherence":r"Moran|spatial (coherence|continuity|autocorrelation)","downstream analysis impact":r"downstream"}
def gt(t):
    g=[n for n,p in GT if re.search(p,t,re.I)]
    return "; ".join(g) if g else "unclear"
def mets(t):
    m=[n for n,p in MET.items() if re.search(p,t,re.I)]
    return "; ".join(m) if m else "unclear"
def flag(p,t): return True if re.search(p,t,re.I) else "unclear"
P_PAR=r"(hyper)?parameter (setting|choice|selection|tuning|sensitivity|optimi)|sensitiv\w* to (\w+ ){0,3}(parameter|setting|hyperparameter)|default (parameter|setting)|hyperparameter|parameter[- ]tuning|choice of parameters|robust\w* to (\w+ ){0,3}parameter"
P_CAL=r"calibrat|uncertaint|confidence (interval|score|estimat)|false discovery|\bFDR\b|type I error|p-value (distribution|calibration|inflation)|false positive rate|credible interval|posterior"
P_MV=r"metric\w* (choice|selection|validity|bias|disagree|inconsisten|reliab|shortcoming|pitfall|ceiling|inflat|mislead)|choice of (evaluation )?metric|(evaluation|benchmark\w*) metrics? (are|were|is|can be) (biased|misleading|insufficient|inadequate|unreliable)|shortcomings of|spurious correlation|inflate[sd]? performance|AUC-PR is a more|metric ceiling|evaluation pitfall|benchmark pitfall|silhouette"
P_PUB=r"github|zenodo|figshare|publicly available|freely available|available (at|from|on|online|via)|https?://|open[- ]source|Bioconductor|CRAN|PyPI|code (is|and data are) available"
CANC=r"cancer|tumou?r|malignan|carcinoma|leuk(a)?emia|lymphoma|melanoma|glioma|glioblastoma|myeloma|sarcoma|neoplas|oncolog|metasta|adenocarcinoma|immuno-oncology"
out=[]
for _,r_ in D.iterrows():
    t=(r_.title+". "+(r_.abstract or ""))
    nc=len(re.findall(CANC,t,re.I))
    out.append(dict(cancer_specific=bool(re.search(CANC,r_.title,re.I)) or nc>=3, n_cancer_mentions=nc,
        n_tools_compared=ntools(t), tools=tools(t) or "unclear", ground_truth_strategy=gt(t), metrics=mets(t),
        assessed_robustness_to_parameters=flag(P_PAR,t), assessed_calibration_or_uncertainty=flag(P_CAL,t),
        assessed_metric_validity=flag(P_MV,t), datasets_public=flag(P_PUB,t)))
X=pd.concat([D.reset_index(drop=True),pd.DataFrame(out)],axis=1)
print(X.ground_truth_strategy.str.split("; ").explode().value_counts())
print(X.cancer_specific.sum(), (X.n_tools_compared=="unclear").sum())
for c in ["assessed_robustness_to_parameters","assessed_calibration_or_uncertainty","assessed_metric_validity","datasets_public"]: print(c,(X[c]==True).sum())
print((X.doi=="").sum(), (X.abstract.str.len()<50).sum())
```

## Cell 17 · python (python) · ok

Writing landmark abstracts for manual check

```python

lmk=["Luecken","Saelens","Abdelaal","Squair","Xi ","Dimitrov","Pratapa","Ahlmann","Kedzierska","Tran H","Li B","Li H","Sturm","Avila","Soneson","Tian L","Mereu","Crowell","Janssen","Zimmerman"]
sel=X[X.first_author.str.contains("|".join(lmk))]
with open("lmk.txt","w") as f:
    for _,r_ in sel.iterrows():
        f.write(f"## {r_.pmid} | {r_.first_author} {r_.year} {r_.journal} | {r_.method_class}\nT: {r_.title}\nA: {r_.abstract[:1800]}\nRULE: n={r_.n_tools_compared} | tools={r_.tools} | GT={r_.ground_truth_strategy} | M={r_.metrics} | par={r_.assessed_robustness_to_parameters} cal={r_.assessed_calibration_or_uncertainty} mv={r_.assessed_metric_validity} pub={r_.datasets_public} canc={r_.cancer_specific}\n\n")
print(len(sel)); print(sel[["pmid","first_author","year","title"]].to_string(max_colwidth=60))
```

## Cell 18 · python (python) · ok

Refining extraction rules and manual overrides

```python

GT=[("simulation",r"simulat|synthetic (data|dataset|benchmark|mixture|network)|in silico (mixture|data)|pseudo-?bulk (mixture|sample)|artificial (mixture|bulk)|splatter|\bdyngen\b|SERGIO|BoolODE"),
    ("cell-line mixture/controlled design",r"cell[- ]line mix|mixture (control|experiment|of cell lines)|mixtures? of (\w+ ){0,3}cell lines|spike-in|ERCC|known (cell[- ]type )?proportions|reference (samples?|materials?)|controlled (heterogeneity|mixture)|admixtures of cells"),
    ("genotype multiplexing",r"genetic(ally)? demultiplex|genotype[- ]based|SNP[- ]based|demuxlet|souporcell|multiplexed donors|natural genetic variation|freemuxlet|cell hashing|hashtag|species[- ]mixing|barnyard|synthetic (DNA )?barcodes|cross-genotype|two mouse subspecies|experimentally annotated doublets"),
    ("orthogonal assay",r"whole[- ]exome|\bWES\b|whole[- ]genome sequencing|\bWGS\b|scDNA|single-cell DNA|CITE-seq|smFISH|\bFISH\b|MERFISH|seqFISH|flow cytometry|\bFACS\b|immunohistochem|\bIHC\b|ChIP-seq|karyotyp|SNP array|matched (bulk|DNA|genomic|WGS)|orthogonal|pathologist|histolog|spatial colocali[sz]ation|protein abundance|cytokine activit|paired (DNA|ATAC|protein|datasets)|multi-?omics? (datasets?|data)|gold-standard estimates|lineage barcod|imaging-based (ground|reference)"),
    ("held-out experimental measurements",r"held-out|unseen (perturbation|cell|drug|gene)|observed (perturbation|response|expression)|post-perturbation|Perturb-seq|CRISPR screen|measured (drug )?response|drug sensitivity data|IC50"),
    ("curated reference (literature/ChIP/database)",r"literature-curated|curated (network|database|interaction|ground truth)|ChIP|known (regulatory|interactions|targets)|STRING|gold standard network"),
    ("expert annotation",r"manual(ly)? annotat|expert|author[- ]provided|curated (labels|annotation)|published (labels|annotations)|original annotation|gold[- ]standard (labels|annotation)|annotated (by|labels)|experimentally labeled|cell type labels"),
    ("consensus-only",r"consensus (among|of|between) (the )?(methods|tools)|agreement (among|between) (methods|tools)|concordance (among|between) (methods|tools)|absence of (a )?ground truth|without (a )?ground truth|lack of (a )?ground truth"),
]
MET={"ARI":(r"\bARI\b",0),"ARI_":(r"adjusted rand",re.I),"NMI":(r"\bNMI\b",0),"NMI_":(r"normali[sz]ed mutual",re.I),"AUROC":(r"AUROC|\bROC\b|\bAUC\b(?!-PR)",0),"AUROC_":(r"area under the (receiver|ROC)",re.I),
 "AUPRC":(r"AUPRC|AUPR\b|AUC-PR",0),"AUPRC_":(r"precision-recall|early precision",re.I),"F1":(r"\bF1\b|F-score|F-measure",0),"accuracy":(r"\baccuracy\b",re.I),
 "precision/recall":(r"\bprecision\b|\brecall\b",re.I),"sensitivity/specificity":(r"\bspecificity\b|\bsensitivity and specificity|true positive rate",re.I),
 "RMSE/MSE":(r"RMSE|\bMSE\b",0),"RMSE/MSE_":(r"mean squared error|root mean squared",re.I),"correlation":(r"\bcorrelation|Pearson|Spearman|\bPCC\b",re.I),
 "JSD":(r"\bJSD\b",0),"JSD_":(r"Jensen-Shannon",re.I),"kBET/LISI/ASW":(r"kBET|LISI|\bASW\b",0),"kBET/LISI/ASW_":(r"silhouette",re.I),
 "FDR/type I error":(r"\bFDR\b|\bFPR\b",0),"FDR/type I error_":(r"false discover|type (I|1) error|false positive rate|false positives",re.I),
 "runtime/scalability":(r"runtime|running time|computational (cost|time|efficiency|resources?)|scalab|memory (usage|consumption|requirement)",re.I),
 "stability/reproducibility":(r"stabilit|reproducib",re.I),"usability":(r"usability|user-friendl",re.I),"spatial coherence":(r"Moran|spatial (coherence|continuity|autocorrelation)|spatially aware",re.I),
 "downstream analysis impact":(r"downstream",re.I)}
def mets(t):
    m=[]
    for n,(p,fl) in MET.items():
        n=n.rstrip("_")
        if n not in m and re.search(p,t,fl): m.append(n)
    return "; ".join(m) if m else "unclear"
def gt(t):
    g=[n for n,p in GT if re.search(p,t,re.I)]
    return "; ".join(g) if g else "unclear"
VERB=r"(benchmark|compar|evaluat|assess|test|examin|systematically|investigat|review|consider|includ)"
def ntools(t):
    best=None; alls=[]
    for m in pat_n.finditer(t):
        w=m.group(1).lower(); v=int(w) if w.isdigit() else num_words[w]
        if not (2<=v<=500): continue
        pre=t[max(0,m.start()-60):m.start()].lower()
        if re.search(r"(more than|over|>|hundreds|developed|exist|available)\s*$",pre) : continue
        alls.append(v)
        if re.search(VERB,pre) and best is None: best=v
    return best if best else (max(alls) if alls else "unclear")
P_PAR=r"(hyper)?parameter[s]? (setting|choice|selection|tuning|sensitivity|optimi|configuration)|sensitiv\w* to (\w+ ){0,3}(parameter|setting|hyperparameter)|default (hyper)?parameter|hyperparameter|parameter[- ]tuning|choice of (parameters|normali[sz]ation|preprocessing)|robust\w* to (\w+ ){0,3}parameter|preprocessing (choices|steps|combinations)|impact of (data )?(transformation|normali[sz]ation|pre-?processing|prefiltering)"
P_CAL=r"calibrat|uncertaint|confidence (interval|score|estimat)|false discover|\bFDR\b|type (I|1) error|p-value (distribution|calibration|inflation)|false positive rate|credible interval"
for col,fn in [("n_tools_compared",ntools),("ground_truth_strategy",gt),("metrics",mets)]:
    X[col]=[fn(a+". "+(b or "")) for a,b in zip(X.title,X.abstract)]
X["assessed_robustness_to_parameters"]=[flag(P_PAR,a+". "+(b or "")) for a,b in zip(X.title,X.abstract)]
X["assessed_calibration_or_uncertainty"]=[flag(P_CAL,a+". "+(b or "")) for a,b in zip(X.title,X.abstract)]
X["assessed_metric_validity"]=[flag(P_MV,a+". "+(b or "")) for a,b in zip(X.title,X.abstract)]
X["extraction"]="rule-based (abstract keywords)"
OV={ # manual checks against abstracts read
"30936559":dict(n_tools_compared=45,ground_truth_strategy="simulation; expert annotation",tools="45 TI methods (dynverse; e.g. Slingshot, PAGA, Monocle)"),
"34949812":dict(n_tools_compared=68,ground_truth_strategy="simulation; expert annotation",metrics="14 metrics: batch removal (kBET/LISI/ASW etc.) + bio-conservation; runtime/scalability; usability",assessed_robustness_to_parameters=True,tools="scANVI; Scanorama; scVI; scGen; Harmony; Seurat; LIGER; fastMNN; BBKNN; ComBat (and others)"),
"31907445":dict(ground_truth_strategy="simulation; curated reference (literature/ChIP/database)",metrics="AUPRC; early precision",tools="12 algorithms (BEELINE; e.g. GENIE3, GRNBoost2, PIDC, SCODE, SINCERITIES, PPCOR, LEAP, SCRIBE)"),
"33159064":dict(ground_truth_strategy="simulation (pseudo-bulk)",metrics="error vs known proportions (RMSE/correlation)",assessed_robustness_to_parameters=True),
"35680885":dict(n_tools_compared="7 methods x 16 resources",ground_truth_strategy="orthogonal assay (spatial colocalisation, cytokine activity, receptor protein); consensus-only",metrics="overlap/agreement; coherence with orthogonal modalities"),
"34584091":dict(assessed_calibration_or_uncertainty=True,ground_truth_strategy="orthogonal assay (matched bulk of purified populations; not stated in abstract)",metrics="FDR/type I error; false discoveries"),
"33531494":dict(assessed_calibration_or_uncertainty=True,metrics="type I error; power"),
"29481549":dict(assessed_robustness_to_parameters=True,metrics="FDR/type I error; power; concordance; runtime/scalability",ground_truth_strategy="simulation; consensus-only"),
"40759747":dict(n_tools_compared=7,ground_truth_strategy="held-out experimental measurements",tools="5 foundation models (e.g. scGPT, scFoundation, GEARS-type DL) vs linear baselines",metrics="prediction error vs observed transcriptome change"),
"40251685":dict(n_tools_compared=2,ground_truth_strategy="expert annotation",metrics="cell-type clustering (e.g. AvgBIO/ASW), batch integration"),
"36991470":dict(assessed_metric_validity=True),
"31948481":dict(tools="Harmony; LIGER; Seurat 3; (14 methods incl. fastMNN, Scanorama, BBKNN, ComBat, limma, scGen, scVI)"),
"31500660":dict(tools="22 classifiers incl. SVM, SingleR, scmap, CHETAH, scPred, Garnett, ACTINN, SingleCellNet"),
"31133762":dict(n_tools_compared=3913,ground_truth_strategy="cell-line mixture/controlled design",metrics="task-specific (clustering ARI, imputation correlation, trajectory correlation, integration)"),
"32518403":dict(n_tools_compared=13,ground_truth_strategy="cell-line mixture/controlled design (reference sample)"),
"37337297":dict(ground_truth_strategy="genotype multiplexing (cross-subspecies pooling)"),
"41675246":dict(n_tools_compared=1,assessed_robustness_to_parameters=True),
"34382023":dict(ground_truth_strategy="genotype multiplexing; simulation (per Xi & Li 2021)"),
"33338399":dict(ground_truth_strategy="genotype multiplexing/experimentally annotated doublets; simulation"),
}
X=X.set_index("pmid")
for k,v in OV.items():
    for c,val in v.items(): X.loc[k,c]=val
    X.loc[k,"extraction"]="rule-based + manual check of abstract"
X=X.reset_index()
print(X.ground_truth_strategy.str.split("; ").explode().str.split(" \(").str[0].value_counts())
for c in ["assessed_robustness_to_parameters","assessed_calibration_or_uncertainty","assessed_metric_validity","datasets_public"]: print(c,(X[c]==True).sum())
print((X.n_tools_compared=="unclear").sum())
```

## Cell 19 · python (python) · ok

Writing CNV/lineage/perturbation abstracts for check

```python

sel=X[X.method_class.isin([CL["CNV"],CL["LIN"],CL["PERT"],CL["DRUG"]])]
with open("chk.txt","w") as f:
    for _,r_ in sel.iterrows():
        f.write(f"## {r_.pmid} | {r_.first_author} {r_.year} | {r_.method_class[:12]}\nT: {r_.title}\nA: {r_.abstract[:1300]}\nRULE: n={r_.n_tools_compared} | tools={r_.tools} | GT={r_.ground_truth_strategy} | M={r_.metrics} | par={r_.assessed_robustness_to_parameters} cal={r_.assessed_calibration_or_uncertainty} mv={r_.assessed_metric_validity} canc={r_.cancer_specific}\n\n")
print(len(sel))
```

## Cell 20 · python (python) · ok

Applying second round of manual corrections

```python

def tools(t):
    found=[]
    for x in TOOLS:
        fl=re.I if len(x)>=6 else 0
        if x in ("linear","hybrid","ROBUST","CNA","ESTIMATE","TIMER","EPIC","CPM","MNN","Combat","Moran","SVM","Solo","solo","Seurat","limma","Wilcoxon"): fl=0
        if re.search(r"(?<![\w\-])"+re.escape(x)+r"(?![\w\-])",t,fl) and x.lower() not in [f.lower() for f in found]:
            found.append(x)
    found=[f for f in found if f not in {"linear","hybrid","ROBUST","CNA","Moran"}]
    return "; ".join(found) if found else "unclear"
manual_tools={k for k,v in OV.items() if "tools" in v}
X["tools"]=[X.tools[i] if X.pmid[i] in manual_tools else tools(X.title[i]+". "+(X.abstract[i] or "")) for i in X.index]
X=X[~X.pmid.isin(["39333790","41465115","41385391"])].copy()
OV2={
"40584741":dict(ground_truth_strategy="cell-line mixture/controlled design; expert annotation (clinical sample)",assessed_robustness_to_parameters=True),
"39200223":dict(n_tools_compared=4,ground_truth_strategy="expert annotation (marker-based)"),
"40037644":dict(ground_truth_strategy="orthogonal assay (matched single-cell multi-omics / DNA)",assessed_robustness_to_parameters=True),
"41038850":dict(ground_truth_strategy="orthogonal assay (ground-truth CNVs; source not specified in abstract)",assessed_robustness_to_parameters=True),
"41160707":dict(ground_truth_strategy="expert annotation (marker-based)"),
"41250104":dict(assessed_robustness_to_parameters=True,ground_truth_strategy="held-out experimental measurements",metrics="accuracy vs simple baselines"),
"42715312":dict(ground_truth_strategy="held-out experimental measurements",metrics="24 metrics: expression accuracy, delta, DE recovery, distributional similarity",assessed_metric_validity=True),
"42185477":dict(ground_truth_strategy="orthogonal assay (clonal expansion of T/B cells)"),
"42860076":dict(assessed_calibration_or_uncertainty=True),
"42121287":dict(ground_truth_strategy="held-out experimental measurements",assessed_metric_validity=True),
"34146472":dict(ground_truth_strategy="simulation; orthogonal assay (intMEMOIR imaging-recorded lineages)"),
"41381537":dict(ground_truth_strategy="held-out experimental measurements (drug-response labels)"),
"40161693":dict(ground_truth_strategy="held-out experimental measurements"),
"42182243":dict(ground_truth_strategy="held-out experimental measurements"),
}
X=X.set_index("pmid")
for k,v in OV2.items():
    for c,val in v.items(): X.loc[k,c]=val
    X.loc[k,"extraction"]="rule-based + manual check of abstract"
X=X.reset_index()
X.loc[X.method_class==CL["CNV"],"cancer_specific"]=True
X.loc[X.pmid=="39147582","cancer_specific"]=True
print(len(X), X.cancer_specific.sum())
print(X.method_class.value_counts())
```

## Cell 21 · python (python) · ok

Supplementary searches for thin method classes

```python

TT='(benchmark*[ti] OR comparison[ti] OR comparative[ti] OR evaluation[ti] OR evaluating[ti] OR assessment[ti] OR assessing[ti] OR systematic[ti] OR comprehensive[ti])'
sup={
"CCC":f'("cell-cell communication"[tiab] OR "cell-cell interaction"[tiab] OR "ligand-receptor"[tiab] OR intercellular[tiab]) AND {TT} AND (single-cell[tiab] OR scRNA-seq[tiab])',
"DADE":f'("differential expression"[tiab] OR "differential abundance"[tiab] OR "differential state"[tiab] OR pseudobulk[tiab] OR "marker gene"[tiab] OR "gene set"[tiab]) AND {TT} AND (single-cell[ti] OR scRNA-seq[ti] OR single cell[ti])',
"TRAJ":f'(trajectory[tiab] OR pseudotime[tiab] OR "RNA velocity"[tiab] OR "cell fate"[tiab]) AND {TT} AND (single-cell[tiab] OR scRNA-seq[tiab]) AND (methods[tiab] OR tools[tiab] OR algorithms[tiab])',
"GRN":f'("gene regulatory network"[tiab] OR "transcription factor activity"[tiab] OR regulon[tiab] OR "network inference"[tiab]) AND {TT} AND (single-cell[tiab] OR scRNA-seq[tiab]) AND (methods[tiab] OR algorithms[tiab])',
"ANN":f'("cell type annotation"[tiab] OR "cell-type annotation"[tiab] OR "cell identification"[tiab] OR "label transfer"[tiab] OR "reference mapping"[tiab] OR "cell type classification"[tiab] OR "large language model"[tiab]) AND {TT} AND (single-cell[tiab] OR scRNA-seq[tiab])',
"LIN":f'("lineage tracing"[tiab] OR "lineage reconstruction"[tiab] OR mitochondrial mutation*[tiab] OR "mtDNA"[tiab] OR "somatic variant*"[tiab] OR "clonal"[tiab] OR "variant calling"[tiab] OR "clone"[tiab]) AND {TT} AND (single-cell[tiab] OR scRNA-seq[tiab]) AND (methods[tiab] OR tools[tiab] OR callers[tiab])',
"SCDNA":f'("tumor phylogeny"[tiab] OR "tumour phylogeny"[tiab] OR "phylogenetic"[tiab] OR "subclonal reconstruction"[tiab] OR "clonal reconstruction"[tiab] OR "copy number"[tiab]) AND {TT} AND ("single-cell DNA"[tiab] OR "single-cell sequencing"[tiab] OR scDNA-seq[tiab] OR "single-cell whole-genome"[tiab]) AND (methods[tiab] OR tools[tiab] OR algorithms[tiab])',
"DRUG":f'("drug response"[tiab] OR "drug sensitivity"[tiab] OR "drug resistance"[tiab] OR "drug perturbation"[tiab]) AND {TT} AND (single-cell[tiab] OR scRNA-seq[tiab]) AND (methods[tiab] OR models[tiab])',
"CNV":f'("copy number"[tiab] OR CNV[tiab] OR "malignant cell"[tiab] OR "tumor cell identification"[tiab] OR aneuploidy[tiab]) AND {TT} AND (scRNA-seq[tiab] OR "single-cell RNA"[tiab] OR "spatial transcriptomics"[tiab]) AND (methods[tiab] OR tools[tiab])',
"FM":f'("foundation model"[tiab] OR "foundation models"[tiab] OR scGPT[tiab] OR Geneformer[tiab] OR "large language models"[tiab]) AND {TT} AND (single-cell[tiab] OR scRNA-seq[tiab])',
"INT":f'("batch correction"[tiab] OR "batch effect"[tiab] OR integration[ti] OR "multi-omics integration"[tiab]) AND {TT} AND (single-cell[ti] OR scRNA-seq[ti])',
"DECONV":f'(deconvolution[ti] OR "cell type proportions"[tiab] OR "immune infiltration"[ti]) AND {TT} AND (methods[tiab] OR tools[tiab] OR algorithms[tiab])',
"DBL":f'(doublet*[tiab] OR "ambient RNA"[tiab] OR demultiplex*[tiab] OR "cell hashing"[tiab] OR "empty droplets"[tiab] OR "quality control"[ti]) AND {TT} AND (single-cell[tiab] OR scRNA-seq[tiab] OR single-nucleus[tiab])',
"SPA":f'("spatial transcriptomics"[tiab] OR "spatially resolved"[tiab]) AND {TT} AND (deconvolution[tiab] OR domain*[tiab] OR "spatially variable"[tiab] OR segmentation[tiab] OR alignment[tiab] OR imputation[tiab] OR "cell type annotation"[tiab] OR "cell-cell"[tiab]) AND (methods[tiab] OR tools[tiab] OR algorithms[tiab])',
}
have=set(X.pmid)|set(R.pmid)
S2={}
for k,q in sup.items():
    ids=es(q,60); S2[k]=[i for i in ids if i not in set(X.pmid)]
    print(k,len(ids),len(S2[k]))
allnew=sorted({i for v in S2.values() for i in v})
def efetch(ids):
    out=[]
    for s in range(0,len(ids),200):
        r=requests.post(E+"efetch.fcgi",data=dict(db="pubmed",id=",".join(ids[s:s+200]),retmode="xml"),timeout=120)
        for a in ET.fromstring(r.content).findall(".//PubmedArticle"):
            pm=a.findtext(".//MedlineCitation/PMID"); art=a.find(".//Article")
            title="".join(art.find("ArticleTitle").itertext())
            ab=" ".join("".join(x.itertext()) for x in art.findall(".//Abstract/AbstractText"))
            jr=a.findtext(".//Journal/ISOAbbreviation") or a.findtext(".//Journal/Title")
            yr=a.findtext(".//JournalIssue/PubDate/Year") or (a.findtext(".//JournalIssue/PubDate/MedlineDate") or "")[:4] or a.findtext(".//ArticleDate/Year")
            au=a.find(".//AuthorList/Author"); fa=""
            if au is not None: fa=(au.findtext("LastName") or au.findtext("CollectiveName") or "")+(" "+au.findtext("Initials") if au.findtext("Initials") else "")
            doi=next((x.text for x in a.findall(".//PubmedData/ArticleIdList/ArticleId") if x.get("IdType")=="doi"),"")
            pts=";".join(p.text for p in a.findall(".//PublicationType"))
            out.append(dict(pmid=pm,doi=doi,first_author=fa,year=yr,journal=jr,title=title,abstract=ab,pubtypes=pts))
        time.sleep(0.4)
    return pd.DataFrame(out)
M=efetch(allnew)
M["sup_class"]=[",".join(k for k,v in S2.items() if p in v) for p in M.pmid]
M=M.sort_values(["sup_class","pmid"]).reset_index(drop=True)
with open("sup_titles.txt","w") as f:
    for i,r_ in M.iterrows(): f.write(f"{i}|{r_.sup_class}|{r_.year}|{r_.journal[:18]}|{r_.title[:140]}\n")
print(len(M)); M.to_pickle("M.pkl")
```

## Cell 22 · python (python) · ok

Adding supplementary picks and re-extracting

```python

MP="7 OTHER,9 ANN,14 ANN,15 ANN,34 INT,39 GRN,114 DADE,115 DADE,119 OTHER,125 DADE,131 DADE,132 OTHER,135 DADE,138 OTHER,140 OTHER,147 OTHER,149 ANN,150 ANN,151 OTHER,161 OTHER,162 DADE,184 DECONV,185 SCDNA,187 DECONV,194 DECONV,203 DECONV,207 DECONV,209 DECONV,210 DECONV,211 DECONV,216 DECONV,218 DECONV,222 SPA,279 FM,285 FM,286 DRUG,288 FM,289 FM,291 GRN,294 GRN,296 GRN,302 GRN,307 INT,308 INT,311 OTHER,318 INT,319 INT,321 INT,328 INT,327 INT,352 OTHER,361 OTHER,383 SPA,396 SPA,401 CCC,405 SPA,411 OTHER,442 TRAJ,448 TRAJ"
rows=[]
for tok in MP.split(","):
    i,c=tok.split(); r_=M.loc[int(i)].to_dict(); r_["method_class"]=CL[c]; r_["sources"]="SUPPLEMENTARY_SEARCH:"+r_["sup_class"]; rows.append(r_)
A=pd.DataFrame(rows)
A["is_preprint"]=A.journal.isin(["bioRxiv","ArXiv","Res Sq","medRxiv"])
def extract(df):
    out=[]
    for _,r_ in df.iterrows():
        t=r_.title+". "+(r_.abstract or "")
        nc=len(re.findall(CANC,t,re.I))
        out.append(dict(cancer_specific=bool(re.search(CANC,r_.title,re.I)) or nc>=3,n_cancer_mentions=nc,n_tools_compared=ntools(t),tools=tools(t),
          ground_truth_strategy=gt(t),metrics=mets(t),assessed_robustness_to_parameters=flag(P_PAR,t),assessed_calibration_or_uncertainty=flag(P_CAL,t),
          assessed_metric_validity=flag(P_MV,t),datasets_public=flag(P_PUB,t),extraction="rule-based (abstract keywords)"))
    return pd.concat([df.reset_index(drop=True),pd.DataFrame(out)],axis=1)
A=extract(A)
cols=["pmid","doi","first_author","year","journal","title","abstract","method_class","sources","is_preprint","other_version_pmids","cancer_specific","n_cancer_mentions","n_tools_compared","tools","ground_truth_strategy","metrics","assessed_robustness_to_parameters","assessed_calibration_or_uncertainty","assessed_metric_validity","datasets_public","extraction"]
A["other_version_pmids"]=""
Y=pd.concat([X[cols],A[cols]],ignore_index=True)
Y["nt2"]=Y.title.str.lower().str.replace(r"[^a-z0-9]","",regex=True).str[:45]
Y=Y.sort_values(["is_preprint","year"],ascending=[True,False])
keep=[];alt={}
for k,g in Y.groupby("nt2",sort=False):
    keep.append(g.index[0]); alt[g.index[0]]=";".join([x for x in [g.other_version_pmids.iloc[0]]+list(g.pmid.iloc[1:]) if x])
Y=Y.loc[keep].copy(); Y["other_version_pmids"]=[alt[i] for i in Y.index]
Y=Y.drop(columns="nt2")
print(len(Y)); print(Y.method_class.value_counts())
print(Y[Y.title.str.contains("multi-assay|ancestry|semi-supervised",case=False)][["pmid","journal","other_version_pmids","title"]].to_string(max_colwidth=60))
```

## Cell 23 · python (python) · ok

Verifying PMIDs via esummary and extracting winner sentences

```python

ids=list(Y.pmid); summ={}
for s in range(0,len(ids),200):
    r=requests.post(E+"esummary.fcgi",data=dict(db="pubmed",id=",".join(ids[s:s+200]),retmode="json"),timeout=60).json()["result"]
    for k in r.get("uids",[]): summ[k]=r[k]
    time.sleep(0.4)
def norm(s): return re.sub(r"[^a-z0-9]","",s.lower())
Y["pubmed_verified"]=[p in summ and norm(summ[p]["title"])[:40]==norm(t)[:40] for p,t in zip(Y.pmid,Y.title)]
print(Y.pubmed_verified.value_counts())
bad=Y[~Y.pubmed_verified]; print(bad[["pmid","title"]].head(), [summ.get(p,{}).get("title") for p in bad.pmid[:5]])
# fill missing doi from esummary articleids
for i in Y.index[Y.doi==""]:
    a=summ.get(Y.pmid[i],{}).get("articleids",[])
    d=[x["value"] for x in a if x["idtype"]=="doi"]
    if d: Y.loc[i,"doi"]=d[0]
print("missing doi",(Y.doi=="").sum())
win=re.compile(r"[^.]*\b(outperform\w*|best[- ]perform\w*|top[- ]perform\w*|performed best|best overall|recommend\w*|superior|excel\w*|most accurate|highest accuracy|no single method|none of|did not outperform|not outperform|simple baselines?|linear baselines?)\b[^.]*\.",re.I)
with open("winners.txt","w") as f:
    for c,g in Y.groupby("method_class"):
        f.write(f"### {c}\n")
        for _,r_ in g.iterrows():
            m=[x.group(0).strip() for x in win.finditer(r_.abstract or "")]
            if m: f.write(f"{r_.pmid} {r_.first_author} {r_.year}: {' | '.join(s[:220] for s in m[:2])}\n")
```

## Cell 24 · python (python) · ok

Computing per-class statistics and cancer flags

```python

Y.loc[Y.pmid=="30963075","assessed_robustness_to_parameters"]=True
Y.loc[Y.pmid=="42070330","assessed_calibration_or_uncertainty"]=True  # bootstrap CIs stated
Y["gt_main"]=Y.ground_truth_strategy.str.replace(r"\s*\([^)]*\)","",regex=True)
cs=Y[Y.cancer_specific==True]
print(len(cs)); print("\n".join(f"{r.pmid} {r.method_class[:10]} {r.title[:90]}" for r in cs.itertuples()))
```

## Cell 25 · python (python) · ok

Saving catalogue CSV and per-class stats

```python

Y["year"]=pd.to_numeric(Y.year,errors="coerce").astype("Int64")
out_cols=["pmid","doi","first_author","year","journal","title","method_class","cancer_specific","n_tools_compared","tools","ground_truth_strategy","metrics","assessed_robustness_to_parameters","assessed_calibration_or_uncertainty","assessed_metric_validity","datasets_public","is_preprint","other_version_pmids","sources","in_prior_158","pubmed_verified","extraction"]
seedset=set(seed)
Y["in_prior_158"]=Y.pmid.isin(seedset)|Y.other_version_pmids.apply(lambda s: any(p in seedset for p in s.split(";") if p))
Y["sources"]=Y.sources.fillna("").str.replace("LANDMARK:","search:",regex=False)
Y=Y.sort_values(["method_class","year","first_author"],ascending=[True,False,True])
Y[out_cols].to_csv("benchmark_catalogue.csv",index=False)
def tcount(s): return (s==True).sum()
rows=[]
for c,g in Y.groupby("method_class"):
    gtc=g.gt_main.str.split("; ").explode().value_counts()
    rows.append(dict(method_class=c,n=len(g),cancer_specific=int(tcount(g.cancer_specific)),year_range=f"{g.year.min()}-{g.year.max()}",
        n_2024_26=int((g.year>=2024).sum()),gt_simulation=int(gtc.get("simulation",0)),gt_orthogonal=int(gtc.get("orthogonal assay",0)),
        gt_expert=int(gtc.get("expert annotation",0)),gt_genotype=int(gtc.get("genotype multiplexing",0)+gtc.get("genotype multiplexing/experimentally annotated doublets",0)),
        gt_mixture=int(gtc.get("cell-line mixture/controlled design",0)),gt_heldout=int(gtc.get("held-out experimental measurements",0)),gt_curated=int(gtc.get("curated reference",0)),
        gt_consensus=int(gtc.get("consensus-only",0)),gt_unclear=int(gtc.get("unclear",0)),
        robust_params=int(tcount(g.assessed_robustness_to_parameters)),calibration=int(tcount(g.assessed_calibration_or_uncertainty)),metric_validity=int(tcount(g.assessed_metric_validity)),public=int(tcount(g.datasets_public)),
        median_n_tools=pd.to_numeric(g.n_tools_compared,errors="coerce").median()))
ST=pd.DataFrame(rows).sort_values("n",ascending=False)
ST.to_csv("benchmark_catalogue_class_summary.csv",index=False)
print(ST.to_string(index=False))
tot=dict(n=len(Y),cancer=int(tcount(Y.cancer_specific)),par=int(tcount(Y.assessed_robustness_to_parameters)),cal=int(tcount(Y.assessed_calibration_or_uncertainty)),mv=int(tcount(Y.assessed_metric_validity)),pub=int(tcount(Y.datasets_public)),gt_unclear=int((Y.gt_main=="unclear").sum()),sim_only=int((Y.gt_main=="simulation").sum()),prior=int(Y.in_prior_158.sum()),pre=int(Y.is_preprint.sum()),manual=int(Y.extraction.str.contains("manual").sum()))
print(tot)
```

## Cell 26 · python (python) · ok

Listing excluded prior-benchmark seeds

```python

inc=set(Y.pmid)|{p for s in Y.other_version_pmids for p in s.split(";") if p}
ex=R[R.pmid.isin(seedset-inc)]
print(len(seedset), len(seedset&inc), len(ex))
for r_ in ex.itertuples(): print(r_.pmid, r_.title[:85])
```

## Cell 27 · python (python) · ok

Adding three omitted seed records and saving

```python

add={"30669152":CL["SCDNA"],"32266244":CL["OTHER"],"36111491":CL["OTHER"]}
B_=R[R.pmid.isin(add)].copy(); B_["method_class"]=B_.pmid.map(add); B_["is_preprint"]=False; B_["other_version_pmids"]=""
B_=extract(B_.reset_index(drop=True)); B_["pubmed_verified"]=True; B_["in_prior_158"]=True
B_["gt_main"]=B_.ground_truth_strategy
Y=pd.concat([Y,B_[[c for c in Y.columns if c in B_.columns]]],ignore_index=True)
i=Y.index[Y.pmid=="40909701"][0]; Y.loc[i,"other_version_pmids"]=";".join([x for x in [Y.other_version_pmids[i],"42109248"] if x])
Y["in_prior_158"]=Y.pmid.isin(seedset)|Y.other_version_pmids.fillna("").apply(lambda s: any(p in seedset for p in s.split(";") if p))
Y["sources"]=Y.sources.fillna("").str.replace("LANDMARK:","search:",regex=False)
Y["year"]=pd.to_numeric(Y.year,errors="coerce").astype("Int64")
Y=Y.sort_values(["method_class","year","first_author"],ascending=[True,False,True]).reset_index(drop=True)
Y[out_cols].to_csv("benchmark_catalogue.csv",index=False)
rows=[]
for c,g in Y.groupby("method_class"):
    gtc=g.gt_main.str.split("; ").explode().value_counts()
    rows.append(dict(method_class=c,n=len(g),cancer_specific=int(tcount(g.cancer_specific)),year_range=f"{g.year.min()}-{g.year.max()}",n_2024_26=int((g.year>=2024).sum()),
        gt_simulation=int(gtc.get("simulation",0)),gt_orthogonal=int(gtc.get("orthogonal assay",0)),gt_expert=int(gtc.get("expert annotation",0)),
        gt_genotype=int(sum(v for k,v in gtc.items() if k.startswith("genotype"))),gt_mixture=int(gtc.get("cell-line mixture/controlled design",0)),
        gt_heldout=int(gtc.get("held-out experimental measurements",0)),gt_curated=int(gtc.get("curated reference",0)),gt_consensus=int(gtc.get("consensus-only",0)),gt_unclear=int(gtc.get("unclear",0)),
        robust_params=int(tcount(g.assessed_robustness_to_parameters)),calibration=int(tcount(g.assessed_calibration_or_uncertainty)),metric_validity=int(tcount(g.assessed_metric_validity)),public=int(tcount(g.datasets_public)),
        median_n_tools=pd.to_numeric(g.n_tools_compared,errors="coerce").median()))
ST=pd.DataFrame(rows).sort_values("n",ascending=False); ST.to_csv("benchmark_catalogue_class_summary.csv",index=False)
tot=dict(n=len(Y),cancer=int(tcount(Y.cancer_specific)),par=int(tcount(Y.assessed_robustness_to_parameters)),cal=int(tcount(Y.assessed_calibration_or_uncertainty)),mv=int(tcount(Y.assessed_metric_validity)),pub=int(tcount(Y.datasets_public)),gt_unclear=int((Y.gt_main=="unclear").sum()),sim_only=int((Y.gt_main=="simulation").sum()),prior=int(Y.in_prior_158.sum()),pre=int(Y.is_preprint.sum()),manual=int(Y.extraction.str.contains("manual").sum()),verified=int(Y.pubmed_verified.sum()))
print(tot); print(ST[["method_class","n","cancer_specific"]].to_string(index=False))
# GT any-mention totals
gall=Y.gt_main.str.split("; ").explode().value_counts(); print(gall)
# which class-level pmids have mv/cal/par True
for c in ["assessed_robustness_to_parameters","assessed_calibration_or_uncertainty","assessed_metric_validity"]:
    print(c, Y[Y[c]==True][["pmid","first_author","year","method_class"]].apply(lambda r:f"{r.pmid}:{r.first_author}:{r.year}:{r.method_class[:8]}",axis=1).tolist())
```

## Cell 28 · python (python) · ok

Checking matched spans for flagged evaluation fields

```python

for c,p in [("assessed_calibration_or_uncertainty",P_CAL),("assessed_metric_validity",P_MV),("assessed_robustness_to_parameters",P_PAR)]:
    for r_ in Y[Y[c]==True].itertuples():
        if r_.extraction.startswith("rule-based +"): continue
        t=r_.title+". "+(r_.abstract or ""); m=re.search(p,t,re.I)
        if m: print(c[:12],r_.pmid, "..."+t[max(0,m.start()-90):m.end()+60].replace("\n"," ")+"...")
print(Y[Y.pmid=="42637979"][["first_author","title","journal"]].values)
```

## Cell 29 · python (python) · ok

Correcting false-positive flags and saving final CSV

```python

fix={("37025654","assessed_calibration_or_uncertainty"),("41266321","assessed_calibration_or_uncertainty"),("42482180","assessed_calibration_or_uncertainty"),("36747724","assessed_calibration_or_uncertainty"),
     ("36562244","assessed_metric_validity"),("42069651","assessed_robustness_to_parameters"),("33073843","assessed_robustness_to_parameters")}
for p,c in fix:
    Y.loc[Y.pmid==p,c]="unclear"; Y.loc[Y.pmid==p,"extraction"]="rule-based + manual check of abstract"
for i in Y.index[Y.first_author==""]:
    au=summ.get(Y.pmid[i],{}).get("authors",[]); Y.loc[i,"first_author"]=au[0]["name"] if au else "(no author listed)"
print(Y[Y.pmid=="42637979"].first_author.values)
Y[out_cols].to_csv("benchmark_catalogue.csv",index=False)
rows=[]
for c,g in Y.groupby("method_class"):
    gtc=g.gt_main.str.split("; ").explode().value_counts()
    rows.append(dict(method_class=c,n=len(g),cancer_specific=int(tcount(g.cancer_specific)),year_range=f"{g.year.min()}-{g.year.max()}",n_2024_26=int((g.year>=2024).sum()),
        gt_simulation=int(gtc.get("simulation",0)),gt_orthogonal=int(gtc.get("orthogonal assay",0)),gt_expert=int(gtc.get("expert annotation",0)),
        gt_genotype=int(sum(v for k,v in gtc.items() if k.startswith("genotype"))),gt_mixture=int(gtc.get("cell-line mixture/controlled design",0)),
        gt_heldout=int(gtc.get("held-out experimental measurements",0)),gt_curated=int(gtc.get("curated reference",0)),gt_consensus=int(gtc.get("consensus-only",0)),gt_unclear=int(gtc.get("unclear",0)),
        robust_params=int(tcount(g.assessed_robustness_to_parameters)),calibration=int(tcount(g.assessed_calibration_or_uncertainty)),metric_validity=int(tcount(g.assessed_metric_validity)),public=int(tcount(g.datasets_public)),
        median_n_tools=pd.to_numeric(g.n_tools_compared,errors="coerce").median()))
ST=pd.DataFrame(rows).sort_values("n",ascending=False); ST.to_csv("benchmark_catalogue_class_summary.csv",index=False)
tot=dict(n=len(Y),cancer=int(tcount(Y.cancer_specific)),par=int(tcount(Y.assessed_robustness_to_parameters)),cal=int(tcount(Y.assessed_calibration_or_uncertainty)),mv=int(tcount(Y.assessed_metric_validity)),pub=int(tcount(Y.datasets_public)),gt_unclear=int((Y.gt_main=="unclear").sum()),sim_only=int((Y.gt_main=="simulation").sum()),any_sim=int(Y.gt_main.str.contains("simulation").sum()),prior=int(Y.in_prior_158.sum()),pre=int(Y.is_preprint.sum()),manual=int(Y.extraction.str.contains("manual").sum()))
print(tot)
print(ST.to_string(index=False))
Y.to_pickle("Y_final.pkl")
```

## Cell 30 · python (python) · ok

Listing catalogue records for synthesis citations

```python

with open("cat_list.txt","w") as f:
    for c,g in Y.groupby("method_class"):
        f.write(f"### {c}\n")
        for r_ in g.itertuples(): f.write(f"{r_.pmid}|{r_.first_author}|{r_.year}|{'C' if r_.cancer_specific==True else ''}|{r_.gt_main[:40]}|{r_.title[:80]}\n")
```

## Cell 31 · bash (python) · ok

Locating catalogue list file

```bash
pwd; ls -la cat_list.txt benchmark_catalogue.csv 2>&1 | head; wc -l cat_list.txt
```

## Cell 32 · python (python) · ok

Computing headline percentages for synthesis

```python

n=len(Y)
g=Y.gt_main.str.split("; ").explode()
g=g.replace({"genotype multiplexing/experimentally annotated doublets":"genotype multiplexing"})
gc=g.groupby(level=0).apply(lambda s: set(s)).explode().value_counts()
pct=lambda k:f"{k} ({100*k/n:.1f}%)"
print({k:pct(v) for k,v in gc.items()})
for c in ["assessed_robustness_to_parameters","assessed_calibration_or_uncertainty","assessed_metric_validity","datasets_public","cancer_specific"]:
    print(c,pct(int((Y[c]==True).sum())))
print("2024-26", pct(int((Y.year>=2024).sum())), "preprint",int(Y.is_preprint.sum()))
cs=Y[Y.cancer_specific==True]; print("cancer GT", cs.gt_main.str.split("; ").explode().value_counts().to_dict())
print("cancer cal/par/mv",[(cs[c]==True).sum() for c in ["assessed_robustness_to_parameters","assessed_calibration_or_uncertainty","assessed_metric_validity"]])
```

## Cell 33 · python (python) · ok

Validating cited PMIDs against catalogue

```python

md=open("benchmark_synthesis.md").read()
cited=set(re.findall(r"\b(\d{8})\b",md))
print(len(cited), sorted(cited-set(Y.pmid)))
```

## Cell 34 · repl · ok

Submitting structured catalogue output

```python

output={
"summary":"Built a PubMed-verified catalogue of 269 benchmark/evaluation studies relevant to single-cell cancer genomics across 16 method classes (15 requested + 'other preprocessing/platform'). Sources: 54 in-scope PMIDs of the prior 158 is_benchmark=True set (104 excluded as out-of-scope clinical/assay comparisons), 16 class-level PubMed benchmark queries, ~90 targeted landmark queries (Luecken 2022, Saelens 2019, Abdelaal 2019, Squair 2021, Xi & Li 2021, Dimitrov 2022, Li B 2022, Li H 2023, Pratapa 2020, Ahlmann-Eltze 2025, Kedzierska 2025, etc. all found and verified) and 14 supplementary queries; ~1,750 candidates title-screened. All 269 bibliographic records come from efetch and match esummary titles. Preprint and journal versions were merged. Evaluation fields (n_tools, tools, ground truth, metrics, robustness, calibration, metric validity, data availability) were extracted from abstracts by keyword rules, with manual correction of 40 records; booleans are True/'unclear'. benchmark_synthesis.md gives the per-class synthesis (what is benchmarked, ground-truth strategy, consensus winners, never-assessed dimensions), citing 173 PMIDs, all present in the catalogue.",
"n_records":269,
"per_class_counts":"other preprocessing/platform 55; spatial (deconv/domains/SVG/platforms) 36; bulk deconvolution 29; integration/batch correction 25; annotation/label transfer 17; clonal phylogeny/scDNA 17; foundation models 14; GRN 13; doublets/demultiplexing/ambient 13; DE/DA 12; perturbation prediction 11; trajectory/RNA velocity 8; CNV & malignant calling 7; cell-cell communication 6; drug response 3; lineage tracing/mtDNA 3. Cancer-specific: 48 total (CNV 7/7, deconvolution 10, scDNA 7, spatial 6; 0 in CCC, GRN, DE/DA, doublets, trajectory, perturbation).",
"headline_patterns":"(Provisional, abstract-level lower bounds.) Ground truth: simulation is mentioned in 91/269 (33.8%), orthogonal assay in 44 (16.4%), expert labels in 24 (8.9%), held-out experimental measurements in 12, genotype multiplexing in 11, curated references in 9, cell-line mixtures in 8, consensus-only in 3; 107 (39.8%) abstracts do not state ground truth. Robustness to parameters is stated in 15 (5.6%), calibration/uncertainty in 9 (3.3%) and metric validity in 8 (3.0%); among the 48 cancer-specific benchmarks metric validity is stated in 0. The best-grounded classes are doublets/ambient RNA (genotype truth 10/13) and perturbation (held-out data 10/11). Perturbation also shows the strongest consensus: simple/linear baselines match or beat deep and foundation models. The other robust consensus is DE: pseudobulk or mixed models beat cell-level tests on FDR. Foundation models do not consistently beat baselines. CNV: Numbat leads when allelic data exist, CopyKAT/SCEVAN otherwise, with reference choice a major sensitivity. Spatial deconvolution: cell2location/RCTD are top, and a simple regression beats about half of methods. Gaps: no PubMed-indexed benchmark of mtDNA clone callers or single-cell phylogeny tools; no tumour-specific benchmark for integration, CCC, GRN, DE/DA, trajectory or ambient/doublets; no shared matched multi-modal tumour truth set. 56% of benchmarks are from 2024-2026.",
"artifacts":["benchmark_catalogue.csv (a4f8a518-3483-417a-8bce-cf455dd3c030)","benchmark_catalogue_class_summary.csv (f8790ac7-2ae2-4159-9e94-21156dea10e5)","benchmark_synthesis.md (0a88aa31-a0c2-4d03-94b1-02e487d2ac5a)"]
}
r=host.submit_output(output,
 completion_bullets=["Catalogued 269 PubMed-verified benchmark studies across 16 method classes","Extracted ground truth, metrics and robustness/calibration/metric-validity flags from abstracts","Wrote per-class synthesis citing 173 catalogue PMIDs"],
 deviations=["host.llm extraction was not possible: the per-frame 2M-token ceiling was reached after 500 screening requests (of ~1,094 planned), and no extraction calls ran. Evaluation fields were filled instead by abstract keyword rules plus manual checking/correction of 40 records (all landmarks, CNV, lineage, perturbation, drug classes). The other 229 records rely on rule-based extraction only, so all counts for robustness, calibration, metric validity, datasets_public, ground truth and n_tools are provisional lower bounds.",
 "Evaluation fields come from abstracts only; no full texts were read. 'unclear' means not stated in the abstract, not 'not assessed'.",
 "Only 54 of the 158 prior is_benchmark=True PMIDs were included (plus 3 as alternative versions). 104 were excluded as outside the method classes (clinical/assay/dosimetry/cell-model comparisons).",
 "PubMed searches were relevance-ranked and capped (80 per class query, 10-25 per landmark query, 60 per supplementary query), so coverage is broad but not exhaustive. Preprint-only benchmarks not indexed in PubMed are missing.",
 "Added a 16th class, 'other preprocessing/platform benchmarks' (55 records: normalization, imputation, clustering, protocols), beyond the requested 15. 'datasets_public' reflects availability statements in abstracts only (52/269).",
 "Crossref was not used; DOIs come from PubMed records (2 records lack a DOI)."])
print(r)
```

## Cell 35 · python (python) · ok

Recomputing seed accounting from saved catalogue

```python

cat=pd.read_csv("benchmark_catalogue.csv",dtype=str).fillna("")
d=set(cat.pmid)&seedset
alt={p for s in cat.other_version_pmids for p in s.split(";") if p}
a=(alt&seedset)-d
print(len(d),len(a),sorted(a),len(seedset)-len(d)-len(a))
md=open("benchmark_synthesis.md").read()
old="Of these, 54 fall within a method class and are included (3 more appear as alternative versions of included papers). The other 104 were excluded as out of scope: clinical/assay comparisons, dosimetry, cell-culture models and similar."
assert old in md
new=f"Of these, {len(d)} are included directly and {len(a)} more appear only as alternative (preprint/duplicate) versions of included papers. The remaining {len(seedset)-len(d)-len(a)} were excluded as out of scope: clinical/assay comparisons, dosimetry, cell-culture models and similar ({len(d)}+{len(a)}+{len(seedset)-len(d)-len(a)}=158)."
open("benchmark_synthesis.md","w").write(md.replace(old,new)); print(new)
```

## Cell 36 · repl · ok

Resubmitting corrected structured output

```python

output["summary"]=output["summary"].replace("54 in-scope PMIDs of the prior 158 is_benchmark=True set (104 excluded as out-of-scope clinical/assay comparisons)","54 PMIDs of the prior 158 is_benchmark=True set included directly, 4 more only as alternative versions of included papers, 100 excluded as out-of-scope clinical/assay comparisons (54+4+100=158)")
assert "54+4+100" in output["summary"]
output["artifacts"]=[a.replace("0a88aa31-a0c2-4d03-94b1-02e487d2ac5a","254deeda-996d-43d7-b91e-47d486afde0d") for a in output["artifacts"]]
devs=["host.llm extraction was not possible: the per-frame 2M-token ceiling was reached after 500 screening requests (of ~1,094 planned), and no extraction calls ran. Evaluation fields were filled instead by abstract keyword rules plus manual checking/correction of 40 records (all landmarks, CNV, lineage, perturbation, drug classes). The other 229 records rely on rule-based extraction only, so all counts for robustness, calibration, metric validity, datasets_public, ground truth and n_tools are provisional lower bounds.",
 "Evaluation fields come from abstracts only; no full texts were read. 'unclear' means not stated in the abstract, not 'not assessed'.",
 "Of the 158 prior is_benchmark=True PMIDs: 54 were included directly, 4 only as alternative versions of included papers (39763763, 39877088, 40386575, 42109248), and 100 were excluded as outside the method classes (clinical/assay/dosimetry/cell-model comparisons).",
 "PubMed searches were relevance-ranked and capped (80 per class query, 10-25 per landmark query, 60 per supplementary query), so coverage is broad but not exhaustive. Preprint-only benchmarks not indexed in PubMed are missing.",
 "Added a 16th class, 'other preprocessing/platform benchmarks' (55 records: normalization, imputation, clustering, protocols), beyond the requested 15. 'datasets_public' reflects availability statements in abstracts only (52/269).",
 "Crossref was not used; DOIs come from PubMed records (2 records lack a DOI)."]
r=host.submit_output(output,completion_bullets=["Catalogued 269 PubMed-verified benchmark studies across 16 method classes","Extracted ground truth, metrics and robustness/calibration/metric-validity flags from abstracts","Wrote per-class synthesis citing 173 catalogue PMIDs; corrected seed accounting (54+4+100)"],deviations=devs)
print(r["status"])
```
