# Sub-agent: Foundations (reference verification, GEO ground-truth catalogue)
Verbatim record of every code cell executed in this session, in execution order. Cells are notebook-style: they share one persistent interpreter, so later cells use variables created by earlier ones. Failed cells are kept and marked; the cell that follows usually corrects them.
Tool legend: `python` = persistent Python kernel; `bash` = fresh shell; `repl` = orchestration kernel of the analysis platform (sub-agent dispatch, artifact and memory calls; not needed to reproduce results). Calls to `host.*` (e.g. `host.llm`, `host.artifact_path`) are platform services; `src/` provides public equivalents.
Cells: 36; failed: 3.

## Cell 1 · bash (python) · ok

Unzipping prior analysis artifact

```bash
mkdir -p prior && cd prior && unzip -o -q "/Users/jubayer/.claude-science/orgs/89d7686f-eb25-4116-8f44-856d205cc44b/artifacts/proj_e32ccc743087/c1980142-77dc-48d1-aeeb-c35fa1fd69f3/vbd928677_artifacts-sc.zip" && find . -type f | head -30 && wc -l $(find . -name "*.md")
```

## Cell 2 · bash (python) · ok

Skimming gap review headings

```bash
cd prior && grep -n "^#" sc_cancer_genomics_gap_review.md | head -40; grep -n -i "GEO\|ground truth" sc_cancer_genomics_gap_review.md | head -20
```

## Cell 3 · python (python) · FAILED

Querying PubMed for candidate foundation refs

```python

import requests, time, json, pandas as pd, re
E="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
def esearch(term, db="pubmed", retmax=3):
    for i in range(4):
        try:
            r=requests.get(E+"esearch.fcgi",params=dict(db=db,term=term,retmax=retmax,retmode="json"),timeout=30)
            return r.json()["esearchresult"]["idlist"]
        except Exception as e: time.sleep(1.5)
    return []
def esummary(ids, db="pubmed"):
    out={}
    for i in range(0,len(ids),150):
        chunk=ids[i:i+150]
        for t in range(4):
            try:
                r=requests.post(E+"esummary.fcgi",data=dict(db=db,id=",".join(chunk),retmode="json"),timeout=60)
                j=r.json()["result"]; break
            except Exception: time.sleep(2)
        for u in j.get("uids",[]): out[u]=j[u]
        time.sleep(0.35)
    return out
Q = {
"weber2019":"essential guidelines computational method benchmarking[ti] AND Weber[au]",
"mangul2019":"systematic benchmarking omics computational tools[ti] AND Mangul[au]",
"boulesteix2013":"plea for neutral comparison studies[ti]",
"norel2011":"self-assessment trap[ti] AND Norel[au]",
"buchka2021":"optimistic performance evaluation newly introduced bioinformatic methods[ti]",
"sonrel2023":"Sonrel[au] AND benchmarks[ti]",
"steegen2016":"multiverse analysis[ti] AND Steegen[au]",
"simonsohn2020":"specification curve analysis[ti] AND Simonsohn[au]",
"silberzahn2018":"many analysts one data set[ti]",
"botvinik2020":"variability in the analysis of a single neuroimaging dataset by many teams[ti]",
"simmons2011":"false-positive psychology[ti]",
"ioannidis2005":"why most published research findings are false[ti] AND Ioannidis[au]",
"venet2011":"most random gene expression signatures are significantly associated with breast cancer outcome[ti]",
"squair2021":"confronting false discoveries in single-cell differential expression[ti]",
"zimmerman2021":"practical solution to pseudoreplication bias in single-cell studies[ti]",
"crowell2020":"subpopulation-specific state transitions multi-sample multi-condition[ti]",
"lazic2010":"problem of pseudoreplication in neuroscientific studies[ti]",
"luecken2022":"benchmarking atlas-level data integration in single-cell genomics[ti]",
"rautenstrauch2025":"silhouette[ti] AND single-cell[ti] AND integration[ti] AND Rautenstrauch[au]",
"ahlmann2023":"comparison of transformations for single-cell RNA-seq data[ti]",
"heumos2023":"best practices for single-cell analysis across modalities[ti]",
"luecken2019":"current best practices in single-cell RNA-seq analysis tutorial[ti]",
"germain2020":"pipeComp[ti]",
"vieth2019":"systematic evaluation of single cell RNA-seq analysis pipelines[ti]",
"tian2019":"benchmarking single cell RNA-sequencing analysis pipelines using mixture control experiments[ti]",
"duo2018":"systematic performance evaluation of clustering methods for single-cell RNA-seq data[ti]",
"soneson2018":"bias robustness and scalability in single-cell differential expression analysis[ti]",
"saelens2019":"comparison of single-cell trajectory inference methods[ti]",
"abdelaal2019":"comparison of automatic cell identification methods for single-cell RNA sequencing data[ti]",
"dimitrov2022":"comparison of methods and resources for cell-cell communication inference[ti]",
"tran2020":"benchmark of batch-effect correction methods for single-cell RNA sequencing data[ti]",
"ahlmann2025":"perturbation effect prediction does not yet outperform simple linear baselines[ti]",
"kedzierska2025":"zero-shot evaluation reveals limitations of single-cell foundation models[ti]",
"chari2023":"specious art of single-cell genomics[ti]",
"lahnemann2020":"eleven grand challenges in single-cell data science[ti]",
"zappia2017":"splatter simulation of single-cell RNA sequencing data[ti]",
"crowell2023":"shaky foundations of simulating single-cell RNA sequencing data[ti]",
"cao2021":"benchmark study of simulation methods for single-cell RNA sequencing data[ti]",
"song2024":"scDesign3[ti]",
"sun2021sd2":"scDesign2[ti]",
"kang2018":"multiplexed droplet single-cell RNA-sequencing using natural genetic variation[ti]",
"heaton2020":"souporcell[ti]",
"huang2019":"vireo[ti] AND Huang[au]",
"mcginnis2019multi":"MULTI-seq[ti]",
"stoeckius2018":"cell hashing with barcoded antibodies[ti]",
"stoeckius2017":"simultaneous epitope and transcriptome measurement in single cells[ti]",
"peterson2017":"multiplexed quantification of proteins and transcripts in single cells[ti]",
"mimitou2019":"multiplexed detection of proteins transcriptomes clonotypes and CRISPR perturbations in single cells[ti]",
"zheng2017":"massively parallel digital transcriptional profiling of single cells[ti]",
"svensson2017":"power analysis of single-cell RNA-sequencing experiments[ti]",
"jiang2011":"synthetic spike-in standards for RNA-seq experiments[ti]",
"mereu2020":"benchmarking single-cell RNA-sequencing protocols for cell atlas projects[ti]",
"ding2020":"systematic comparison of single-cell and single-nucleus RNA-sequencing methods[ti]",
"xi2021":"benchmarking computational doublet-detection methods for single-cell RNA sequencing data[ti]",
"ludwig2019":"lineage tracing in humans enabled by mitochondrial mutations and single-cell genomics[ti]",
"lareau2021":"massively parallel single-cell mitochondrial DNA genotyping and chromatin profiling[ti]",
"miller2022":"mitochondrial variant enrichment from high-throughput single-cell RNA sequencing resolves clonal populations[ti]",
"kwok2022":"MQuad[ti]",
"tirosh2016":"dissecting the multicellular ecosystem of metastatic melanoma by single-cell RNA-seq[ti]",
"patel2014":"single-cell RNA-seq highlights intratumoral heterogeneity in primary glioblastoma[ti]",
"gao2021":"delineating copy number and clonal substructure in human tumors from single-cell transcriptomes[ti]",
"defalco2023":"SCEVAN[ti] OR (De Falco[au] AND copy number[ti] AND single-cell[ti] AND 2023[dp])",
"gao2023":"haplotype-aware analysis of somatic copy number variations from single-cell transcriptomes[ti]",
"fan2018":"linking transcriptional and genetic tumor heterogeneity through allele analysis of single-cell RNA-seq data[ti]",
"muller2018":"CONICS[ti]",
"serin2020":"CaSpER[ti]",
"sun2021tisch":"TISCH[ti] AND tumor immune single-cell hub[ti]",
"han2023tisch2":"TISCH2[ti]",
"yuan2019":"CancerSEA[ti]",
"gavish2023":"hallmarks of transcriptional intratumour heterogeneity across a thousand tumours[ti]",
"rozenblatt2020":"Human Tumor Atlas Network[ti] AND 2020[dp]",
"cellxgene2025":"CZ CELLxGENE Discover[ti]",
"regev2017":"the human cell atlas[ti] AND Regev[au] AND 2017[dp]",
"kinker2020":"pan-cancer single-cell RNA-seq identifies recurring programs of cellular heterogeneity[ti]",
"zheng2021":"pan-cancer single-cell landscape of tumor-infiltrating T cells[ti]",
"cheng2021":"pan-cancer single-cell transcriptional atlas of tumor infiltrating myeloid cells[ti]",
"dixit2016":"Perturb-Seq dissecting molecular circuits with scalable single-cell RNA profiling of pooled genetic screens[ti]",
"adamson2016":"multiplexed single-cell CRISPR screening platform enables systematic dissection of the unfolded protein response[ti]",
"replogle2022":"mapping information-rich genotype-phenotype landscapes with genome-scale Perturb-seq[ti]",
"mcfarland2020":"multiplexed single-cell transcriptional response profiling to define cancer vulnerabilities and therapeutic mechanism of action[ti]",
"frangieh2021":"multimodal pooled Perturb-CITE-seq screens in patient models define mechanisms of cancer immune evasion[ti]",
"li2022spatial":"benchmarking spatial and single-cell transcriptomics integration methods[ti]",
"avila2020":"benchmarking of cell type deconvolution pipelines for transcriptomics data[ti]",
"cnvbench":"benchmark*[ti] AND copy number[ti] AND single-cell[ti] AND (RNA[ti] OR transcriptom*[ti])",
"conformal_sc":"conformal[ti] AND (single-cell[ti] OR single cell[ti])",
"calib_sc":"(calibrat*[ti] OR uncertainty[ti]) AND cell type[ti] AND (annotation[ti] OR classification[ti]) AND single-cell[tiab]",
"multiverse_sc":"(multiverse[tiab] OR analytical flexibility[tiab] OR researcher degrees of freedom[tiab]) AND (single-cell[tiab] OR scRNA-seq[tiab])",
"mtartifact":"mitochondrial[ti] AND single-cell[ti] AND (artifact*[ti] OR benchmark*[ti]) AND (lineage[tiab] OR clonal[tiab])",
"hie_no":"Kim[au] AND demultiplex*[ti] AND benchmark*[ti]",
}
hits={}
for k,q in Q.items():
    rmax = 8 if k in ("cnvbench","conformal_sc","calib_sc","multiverse_sc","mtartifact","hie_no") else 3
    hits[k]=esearch(q,retmax=rmax); time.sleep(0.35)
allids=sorted({i for v in hits.values() for i in v})
S=esummary(allids)
lines=[]
for k,v in hits.items():
    for i in v:
        s=S.get(i,{})
        lines.append(f"{k}\t{i}\t{s.get('pubdate','')[:4]}\t{s.get('source','')}\t{(s.get('authors') or [{'name':''}])[0]['name']}\t{s.get('title','')[:110]}")
    if not v: lines.append(f"{k}\tNONE")
open("pm_hits.tsv","w").write("\n".join(lines))
print(len(lines), sum(1 for k,v in hits.items() if not v), [k for k,v in hits.items() if not v])
```

## Cell 4 · python (python) · ok

Checking requests import

```python
import sys; print(sys.executable)
try:
    import requests; print(requests.__version__)
except Exception as e: print(e)
```

## Cell 5 · python (python) · ok

Querying PubMed for candidate foundation refs

```python

import requests, time, json, pandas as pd, re
E="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
def esearch(term, db="pubmed", retmax=3, **kw):
    for i in range(4):
        try:
            r=requests.get(E+"esearch.fcgi",params=dict(db=db,term=term,retmax=retmax,retmode="json",**kw),timeout=30)
            return r.json()["esearchresult"]
        except Exception as e: time.sleep(1.5)
    return {"idlist":[],"count":"0"}
def esummary(ids, db="pubmed"):
    out={}
    for i in range(0,len(ids),150):
        chunk=ids[i:i+150]; j={}
        for t in range(4):
            try:
                r=requests.post(E+"esummary.fcgi",data=dict(db=db,id=",".join(chunk),retmode="json"),timeout=60)
                j=r.json()["result"]; break
            except Exception: time.sleep(2)
        for u in j.get("uids",[]): out[u]=j[u]
        time.sleep(0.35)
    return out
Q = {
"weber2019":"essential guidelines computational method benchmarking[ti] AND Weber[au]",
"mangul2019":"systematic benchmarking omics computational tools[ti] AND Mangul[au]",
"boulesteix2013":"plea for neutral comparison studies[ti]",
"norel2011":"self-assessment trap[ti] AND Norel[au]",
"buchka2021":"optimistic performance evaluation newly introduced bioinformatic methods[ti]",
"sonrel2023":"Sonrel[au] AND benchmarks[ti]",
"steegen2016":"multiverse analysis[ti] AND Steegen[au]",
"simonsohn2020":"specification curve analysis[ti] AND Simonsohn[au]",
"silberzahn2018":"many analysts one data set[ti]",
"botvinik2020":"variability in the analysis of a single neuroimaging dataset by many teams[ti]",
"simmons2011":"false-positive psychology[ti]",
"ioannidis2005":"why most published research findings are false[ti] AND Ioannidis[au]",
"venet2011":"most random gene expression signatures are significantly associated with breast cancer outcome[ti]",
"squair2021":"confronting false discoveries in single-cell differential expression[ti]",
"zimmerman2021":"practical solution to pseudoreplication bias in single-cell studies[ti]",
"crowell2020":"subpopulation-specific state transitions multi-sample multi-condition[ti]",
"lazic2010":"problem of pseudoreplication in neuroscientific studies[ti]",
"luecken2022":"benchmarking atlas-level data integration in single-cell genomics[ti]",
"rautenstrauch2025":"silhouette[ti] AND Rautenstrauch[au]",
"ahlmann2023":"comparison of transformations for single-cell RNA-seq data[ti]",
"heumos2023":"best practices for single-cell analysis across modalities[ti]",
"luecken2019":"current best practices in single-cell RNA-seq analysis tutorial[ti]",
"germain2020":"pipeComp[ti]",
"vieth2019":"systematic evaluation of single cell RNA-seq analysis pipelines[ti]",
"tian2019":"benchmarking single cell RNA-sequencing analysis pipelines using mixture control experiments[ti]",
"duo2018":"systematic performance evaluation of clustering methods for single-cell RNA-seq data[ti]",
"soneson2018":"bias robustness and scalability in single-cell differential expression analysis[ti]",
"saelens2019":"comparison of single-cell trajectory inference methods[ti]",
"abdelaal2019":"comparison of automatic cell identification methods for single-cell RNA sequencing data[ti]",
"dimitrov2022":"comparison of methods and resources for cell-cell communication inference[ti]",
"tran2020":"benchmark of batch-effect correction methods for single-cell RNA sequencing data[ti]",
"ahlmann2025":"perturbation effect prediction does not yet outperform simple linear baselines[ti]",
"kedzierska2025":"zero-shot evaluation reveals limitations of single-cell foundation models[ti]",
"chari2023":"specious art of single-cell genomics[ti]",
"lahnemann2020":"eleven grand challenges in single-cell data science[ti]",
"zappia2017":"splatter simulation of single-cell RNA sequencing data[ti]",
"crowell2023":"shaky foundations of simulating single-cell RNA sequencing data[ti]",
"cao2021":"benchmark study of simulation methods for single-cell RNA sequencing data[ti]",
"song2024":"scDesign3[ti]",
"sun2021sd2":"scDesign2[ti]",
"kang2018":"multiplexed droplet single-cell RNA-sequencing using natural genetic variation[ti]",
"heaton2020":"souporcell[ti]",
"huang2019":"vireo[ti] AND Huang[au]",
"mcginnis2019multi":"MULTI-seq[ti]",
"stoeckius2018":"cell hashing with barcoded antibodies[ti]",
"stoeckius2017":"simultaneous epitope and transcriptome measurement in single cells[ti]",
"peterson2017":"multiplexed quantification of proteins and transcripts in single cells[ti]",
"mimitou2019":"multiplexed detection of proteins transcriptomes clonotypes and CRISPR perturbations in single cells[ti]",
"zheng2017":"massively parallel digital transcriptional profiling of single cells[ti]",
"svensson2017":"power analysis of single-cell RNA-sequencing experiments[ti]",
"jiang2011":"synthetic spike-in standards for RNA-seq experiments[ti]",
"mereu2020":"benchmarking single-cell RNA-sequencing protocols for cell atlas projects[ti]",
"ding2020":"systematic comparison of single-cell and single-nucleus RNA-sequencing methods[ti]",
"xi2021":"benchmarking computational doublet-detection methods for single-cell RNA sequencing data[ti]",
"ludwig2019":"lineage tracing in humans enabled by mitochondrial mutations and single-cell genomics[ti]",
"lareau2021":"massively parallel single-cell mitochondrial DNA genotyping and chromatin profiling[ti]",
"miller2022":"mitochondrial variant enrichment from high-throughput single-cell RNA sequencing resolves clonal populations[ti]",
"kwok2022":"MQuad[ti]",
"tirosh2016":"dissecting the multicellular ecosystem of metastatic melanoma by single-cell RNA-seq[ti]",
"patel2014":"single-cell RNA-seq highlights intratumoral heterogeneity in primary glioblastoma[ti]",
"gao2021":"delineating copy number and clonal substructure in human tumors from single-cell transcriptomes[ti]",
"defalco2023":"De Falco[au] AND copy number[ti] AND 2023[dp]",
"gao2023":"haplotype-aware analysis of somatic copy number variations from single-cell transcriptomes[ti]",
"fan2018":"linking transcriptional and genetic tumor heterogeneity through allele analysis of single-cell RNA-seq data[ti]",
"muller2018":"CONICS[ti]",
"serin2020":"CaSpER[ti]",
"sun2021tisch":"TISCH[ti] AND tumor immune single-cell hub[ti]",
"han2023tisch2":"TISCH2[ti]",
"yuan2019":"CancerSEA[ti]",
"gavish2023":"hallmarks of transcriptional intratumour heterogeneity across a thousand tumours[ti]",
"rozenblatt2020":"Human Tumor Atlas Network[ti] AND 2020[dp]",
"cellxgene2025":"CZ CELLxGENE Discover[ti]",
"regev2017":"the human cell atlas[ti] AND Regev[au] AND 2017[dp]",
"kinker2020":"pan-cancer single-cell RNA-seq identifies recurring programs of cellular heterogeneity[ti]",
"zheng2021":"pan-cancer single-cell landscape of tumor-infiltrating T cells[ti]",
"cheng2021":"pan-cancer single-cell transcriptional atlas of tumor infiltrating myeloid cells[ti]",
"dixit2016":"Perturb-Seq dissecting molecular circuits with scalable single-cell RNA profiling of pooled genetic screens[ti]",
"adamson2016":"multiplexed single-cell CRISPR screening platform enables systematic dissection of the unfolded protein response[ti]",
"replogle2022":"mapping information-rich genotype-phenotype landscapes with genome-scale Perturb-seq[ti]",
"mcfarland2020":"multiplexed single-cell transcriptional response profiling to define cancer vulnerabilities[ti]",
"frangieh2021":"multimodal pooled Perturb-CITE-seq screens in patient models define mechanisms of cancer immune evasion[ti]",
"li2022spatial":"benchmarking spatial and single-cell transcriptomics integration methods[ti]",
"avila2020":"benchmarking of cell type deconvolution pipelines for transcriptomics data[ti]",
"cnvbench":"benchmark*[ti] AND copy number[ti] AND single-cell[ti] AND (RNA[ti] OR transcriptom*[ti])",
"conformal_sc":"conformal[ti] AND (single-cell[ti] OR single cell[ti])",
"calib_sc":"(calibrat*[ti] OR uncertainty[ti]) AND cell type[ti] AND (annotation[ti] OR classification[ti] OR identification[ti])",
"multiverse_sc":"(multiverse[tiab] OR analytical flexibility[tiab] OR researcher degrees of freedom[tiab]) AND (single-cell[tiab] OR scRNA-seq[tiab])",
"mtartifact":"mitochondrial[ti] AND single-cell[ti] AND (artifact*[ti] OR benchmark*[ti] OR misinform*[ti])",
"demuxbench":"demultiplex*[ti] AND (benchmark*[ti] OR comparison[ti] OR evaluat*[ti]) AND single-cell[tiab]",
"cnvbench2":"(benchmark*[ti] OR comparison[ti] OR evaluation[ti]) AND (CNV[ti] OR copy number[ti]) AND single-cell[ti]",
"maligncall":"(malignant[ti] OR tumor cells[ti] OR tumour cells[ti]) AND (benchmark*[ti] OR comparison[ti]) AND single-cell[ti]",
}
SEARCHES={"cnvbench","conformal_sc","calib_sc","multiverse_sc","mtartifact","demuxbench","cnvbench2","maligncall"}
hits={}
for k,q in Q.items():
    hits[k]=esearch(q,retmax=10 if k in SEARCHES else 3)["idlist"]; time.sleep(0.35)
allids=sorted({i for v in hits.values() for i in v})
S=esummary(allids)
lines=[]
for k,v in hits.items():
    for i in v:
        s=S.get(i,{})
        lines.append(f"{k}\t{i}\t{s.get('pubdate','')[:4]}\t{s.get('source','')}\t{(s.get('authors') or [{'name':''}])[0]['name']}\t{s.get('title','')[:120]}")
    if not v: lines.append(f"{k}\tNONE")
open("pm_hits.tsv","w").write("\n".join(lines))
print(len(lines), [k for k,v in hits.items() if not v])
```

## Cell 6 · python (python) · ok

Second PubMed round for missing refs

```python

Q2={
"heumos2023":"Heumos L[au] AND best practices[ti]",
"luecken2019":"Luecken MD[au] AND best practices[ti] AND 2019[dp]",
"gao2021":"Gao R[au] AND copy number[ti] AND single-cell transcriptomes[ti]",
"sun2021tisch":"Sun D[au] AND TISCH[ti]",
"silberzahn2018":"Silberzahn R[au] AND many analysts[ti]",
"simmons2011":"Simmons JP[au] AND false-positive psychology[ti]",
"ioannidis2005":"Ioannidis JP[au] AND why most published research findings are false[ti] AND 2005[dp]",
"duo2018":"Duò A[au] AND clustering[ti]",
"cao2021":"Cao Y[au] AND simulation methods[ti] AND single-cell[ti]",
"ahlmann2025":"Ahlmann-Eltze C[au] AND perturbation[ti]",
"stoeckius2017":"Stoeckius M[au] AND epitope[ti]",
"svensson2017":"Svensson V[au] AND power analysis[ti]",
"muller2018":"Müller S[au] AND copy number[ti] AND single-cell[ti] AND 2018[dp]",
"serin2020":"Serin Harmanci A[au] AND CaSpER[ti]",
"sun2021sd2":"Sun T[au] AND scDesign2[ti] AND transparent simulator[ti]",
"calib_sc2":"Estimating uncertainty in reference-based cell type annotation[ti]",
"mtartifact":"Lareau CA[au] AND mitochondrial[ti] AND (artifact*[ti] OR phylogenetic[ti])",
"weng2024":"Weng C[au] AND mitochondrial[tiab] AND haematopoiesis[ti]",
"hao2021":"integrated analysis of multimodal single-cell data[ti]",
"flex_sc":"(choice*[ti] OR decision*[ti] OR robustness[ti]) AND (preprocessing[ti] OR pipeline*[ti] OR workflow*[ti]) AND (single-cell[ti] OR scRNA-seq[ti])",
"reprod_sc":"(reproducibility[ti] OR replicability[ti]) AND (single-cell[ti] OR scRNA-seq[ti]) AND (analysis[ti] OR clustering[ti])",
"signature_null":"random gene signatures[tiab] AND (prognostic[tiab] OR survival[tiab]) AND null[tiab]",
"cottrell":"Cottrell[au]? ",
"spikein_sc":"spike-in[ti] AND single-cell[ti] AND (benchmark*[ti] OR evaluat*[ti] OR control*[ti])",
"ground_truth_sc":"ground truth[ti] AND (single-cell[ti] OR scRNA-seq[ti])",
"hippen":"Hippen AA[au] AND deconvolution[ti]",
"sc_ccc_spatial":"cell-cell communication[ti] AND (benchmark*[ti] OR evaluation[ti]) AND spatial[tiab]",
"hubert_ari_sc":"adjusted rand index[ti]",
"openproblems":"Open Problems[ti] AND single-cell[ti]",
"mixtures_cline":"cell line mixture*[tiab] AND single-cell RNA[tiab] AND benchmark*[tiab]",
}
Q2.pop("cottrell")
SE2={"flex_sc","reprod_sc","signature_null","spikein_sc","ground_truth_sc","hippen","sc_ccc_spatial","hubert_ari_sc","openproblems","mixtures_cline"}
hits2={}
for k,q in Q2.items():
    hits2[k]=esearch(q,retmax=8 if k in SE2 else 3)["idlist"]; time.sleep(0.35)
S.update(esummary(sorted({i for v in hits2.values() for i in v}-set(S))))
lines=[]
for k,v in hits2.items():
    for i in v:
        s=S.get(i,{})
        lines.append(f"{k}\t{i}\t{s.get('pubdate','')[:4]}\t{s.get('source','')}\t{(s.get('authors') or [{'name':''}])[0]['name']}\t{s.get('title','')[:120]}")
    if not v: lines.append(f"{k}\tNONE")
open("pm_hits2.tsv","w").write("\n".join(lines)); print(len(lines))
```

## Cell 7 · python (python) · ok

Third PubMed round and Crossref DOI checks

```python

Q3={"hao2021":"Hao Y[au] AND integrated analysis of multimodal single-cell data[ti]",
"muller2018":"COpy-Number analysis[ti]",
"calib_sc3":"uncertainty[ti] AND cell type annotation[ti] AND Nat Genet[ta]",
"ziegenhain2022":"molecular spikes[ti]",
"hippen":"Hippen[au] AND (deconvolution[ti] OR single-cell[ti])",
"lareau_art":"Lareau CA[au] AND mitochondrial[tiab] AND 2023:2026[dp]",
"silberzahn_pm":"Silberzahn R[au]"}
for k,q in Q3.items():
    ids=esearch(q,retmax=6)["idlist"]; time.sleep(0.35)
    sm=esummary(ids) if ids else {}; S.update(sm)
    for i in ids: s=sm[i]; print(k,i,s['pubdate'][:4],s['source'],(s.get('authors') or [{'name':''}])[0]['name'],s['title'][:100])
    if not ids: print(k,"NONE")
def crossref(doi):
    r=requests.get("https://api.crossref.org/works/"+doi,timeout=30)
    if r.status_code!=200: return None
    m=r.json()["message"]
    return dict(doi=m["DOI"],title=(m.get("title") or [""])[0],journal=(m.get("container-title") or [""])[0],
                year=(m.get("issued",{}).get("date-parts") or [[None]])[0][0],
                authors="; ".join(f"{a.get('family','')} {a.get('given','')[:1]}".strip() for a in m.get("author",[])[:6]) + ("; et al." if len(m.get("author",[]))>6 else ""))
CR={"silberzahn2018":"10.1177/2515245917747646","angelopoulos2023":"10.1561/2200000101","hubert1985":"10.1007/BF01908075",
    "rousseeuw1987":"10.1016/0377-0427(87)90125-7","lei2018":"10.1080/01621459.2017.1307116","hurlbert1984":"10.2307/1942661",
    "vovk_book":"10.1007/978-3-031-06649-8"}
crres={}
for k,d in CR.items():
    crres[k]=crossref(d); print(k,crres[k]); time.sleep(0.3)
for aid in ["1706.04599","2107.07511"]:
    r=requests.get("http://export.arxiv.org/api/query",params={"id_list":aid},timeout=30)
    t=re.findall(r"<title>(.*?)</title>",r.text,re.S); au=re.findall(r"<name>(.*?)</name>",r.text); pub=re.findall(r"<published>(.*?)</published>",r.text)
    print(aid,t[-1:] ,au,pub)
```

## Cell 8 · python (python) · ok

Building verified foundations reference table

```python

ids=esearch("uncertainty[tiab] AND reference-based[tiab] AND annotation[tiab] AND Nat Genet[ta] AND 2024[dp]",retmax=5)["idlist"]
sm=esummary(ids); 
for i in ids: print(i, sm[i]['title'][:100], [a['name'] for a in sm[i]['authors'][:2]])
```

## Cell 9 · python (python) · ok

Assembling foundations_refs.csv from verified records

```python

A=[ # key, pmid, category, claim
("weber2019","31221194","benchmarking guidelines","Neutral benchmarks need defined purpose, representative datasets incl. ground truth, multiple metrics and reproducible code."),
("mangul2019","30918265","benchmarking guidelines","Systematic omics tool benchmarking requires gold-standard data, and most published tool comparisons lack it."),
("boulesteix2013","23637855","benchmarking guidelines","Neutral comparison studies, by authors not developing the compared methods, are needed to avoid biased method rankings."),
("sonrel2023","37198712","benchmarking guidelines","Single-cell benchmarks are rarely extensible or interoperable; a meta-analysis of benchmarks calls for continuous, open benchmarking."),
("luecken2025op","40595413","benchmarking guidelines","Open Problems formalises community-maintained, living benchmarks with task definitions and metrics for single-cell analysis."),
("norel2011","21988833","self-assessment trap","Method developers evaluating their own methods almost always rank them best (the self-assessment trap)."),
("buchka2021","33975646","self-assessment trap","Performance of newly introduced bioinformatic methods is over-optimistic relative to later neutral evaluation."),
("ioannidis2005","16060722","research reliability","Flexibility in designs, definitions and analysis inflates the false-positive rate of published findings."),
("simmons2011","22006061","analytical flexibility","Undisclosed flexibility in data collection and analysis allows presenting almost any result as significant."),
("steegen2016","27694465","multiverse analysis","Multiverse analysis reports results across all reasonable data-processing choices to expose fragility."),
("simonsohn2020","32719546","multiverse analysis","Specification-curve analysis estimates and tests the joint distribution of results across all defensible specifications."),
("silberzahn2018","","many-analyst studies","29 teams analysing one data set reached different effect estimates, showing analytical choices drive results."),
("botvinik2020","32483374","many-analyst studies","70 teams analysing one fMRI dataset reached substantially different hypothesis-test conclusions."),
("venet2011","22028643","random-signature null","Most random gene-expression signatures are significantly associated with breast cancer outcome, so signature prognostic value needs a random-set null."),
("waldron2014","24700801","random-signature null","Meta-analysis of published ovarian-cancer prognostic signatures shows modest, overlapping performance across validation cohorts."),
("guo2017","","calibration","Modern deep neural networks are poorly calibrated; temperature scaling is a simple fix."),
("angelopoulos2023","","conformal prediction","Conformal prediction gives distribution-free, finite-sample coverage guarantees for any predictive model."),
("lei2018","","conformal prediction","Split conformal inference yields valid distribution-free prediction intervals for regression."),
("vovk2022","","conformal prediction","Foundational monograph on conformal prediction and validity guarantees under exchangeability."),
("lopezdecastro2025","40973204","single-cell conformal/calibration","Conformal inference provides prediction sets with coverage guarantees for scRNA-seq cell-type annotation."),
("natgen2024brief","39592883","single-cell conformal/calibration","Reference-based single-cell cell-type annotation requires explicit uncertainty estimates (Nature Genetics research briefing)."),
("squair2021","34584091","pseudoreplication","Single-cell DE methods treating cells as replicates produce false discoveries; pseudobulk methods perform best against matched bulk ground truth."),
("zimmerman2021","33531494","pseudoreplication","Ignoring within-individual correlation of cells inflates type-I error; mixed models correct pseudoreplication bias."),
("crowell2020","33257685","pseudoreplication","Multi-sample multi-condition scRNA-seq DS analysis benefits from sample-level (pseudobulk) aggregation (muscat)."),
("lazic2010","20074371","pseudoreplication","Pseudoreplication is common in neuroscience and inflates false positives when non-independent units are treated as replicates."),
("hubert1985","","metric validity","Defines the adjusted Rand index, correcting partition agreement for chance."),
("rousseeuw1987","","metric validity","Defines the silhouette width for cluster validation."),
("steinley2004","15355155","metric validity","Properties and interpretation thresholds of the Hubert-Arabie ARI are characterised."),
("rautenstrauch2025","40739072","metric validity","Silhouette-based scores are unreliable for evaluating single-cell integration and can reward poor integration."),
("luecken2022","34949812","metric validity","Atlas-level integration benchmark (scIB) combines batch-removal and bio-conservation metrics; rankings depend on metric choice."),
("chari2023","37590228","metric validity","2D embeddings (t-SNE/UMAP) distort local and global structure and should not be used for quantitative inference."),
("ahlmann2023","37037999","analytical flexibility (single-cell)","Choice of count transformation affects downstream results; simple shifted-log performs as well as complex alternatives."),
("germain2020","32873325","analytical flexibility (single-cell)","pipeComp shows preprocessing choices (filtering, normalisation, dimensionality) alter clustering accuracy."),
("vieth2019","31604912","analytical flexibility (single-cell)","Choices of mapping, normalisation and library prep combine to drive scRNA-seq DE performance."),
("shainer2021","34521337","analytical flexibility (single-cell)","Choice of preprocessing pipeline changes clustering quality of scRNA-seq datasets."),
("soneson2021","33428615","analytical flexibility (single-cell)","Preprocessing choices alter RNA velocity estimates from droplet scRNA-seq."),
("saxena2026","42070330","analytical flexibility (single-cell)","Normalisation choice drives biological interpretation in scRNA-seq cancer studies."),
("heumos2023","37002403","best practice","Community best-practice recommendations for single-cell analysis across modalities."),
("luecken2019","31217225","best practice","Tutorial of current best practices for scRNA-seq analysis steps."),
("lahnemann2020","32033589","best practice","Eleven grand challenges in single-cell data science include benchmarking and ground truth."),
("duo2018","30271584","neutral benchmarks (single-cell)","Clustering method performance on scRNA-seq varies strongly by dataset and method."),
("soneson2018","29481549","neutral benchmarks (single-cell)","Single-cell DE methods show bias, varying robustness and scalability; many bulk methods do comparably."),
("saelens2019","30936559","neutral benchmarks (single-cell)","Trajectory inference performance depends on topology; benchmark of 45 methods."),
("abdelaal2019","31500660","neutral benchmarks (single-cell)","Automatic cell identification methods compared; general-purpose classifiers such as SVM perform well."),
("dimitrov2022","35680885","neutral benchmarks (single-cell)","Cell-cell communication predictions depend strongly on the chosen method and resource, with limited agreement."),
("tran2020","31948481","neutral benchmarks (single-cell)","Batch-correction methods benchmarked; Harmony, LIGER and Seurat 3 recommended."),
("xi2021","33338399","neutral benchmarks (single-cell)","Doublet-detection methods benchmarked on datasets with experimentally annotated doublets."),
("ahlmann2025","40759747","neutral benchmarks (single-cell)","Deep-learning perturbation-effect predictors do not outperform simple linear baselines."),
("kedzierska2025","40251685","neutral benchmarks (single-cell)","Zero-shot evaluation shows single-cell foundation models often underperform simpler baselines."),
("li2022spatial","35577954","neutral benchmarks (single-cell)","Spatial-scRNA integration methods for transcript prediction and cell-type deconvolution benchmarked."),
("avilacobos2020","33159064","neutral benchmarks (single-cell)","Deconvolution performance depends on data transformation, normalisation and reference choice."),
("zappia2017","28899397","simulation realism","Splatter provides a framework for simulating scRNA-seq count data and comparing simulators."),
("crowell2023","36991470","simulation realism","Most scRNA-seq simulators fail to reproduce complex structure (multi-group, batch), so simulation-based benchmarks can mislead."),
("cao2021","34824223","simulation realism","Benchmark of scRNA-seq simulation methods shows varying data-property fidelity."),
("sun2021sd2","34034771","simulation realism","scDesign2 simulates high-fidelity counts preserving gene correlations."),
("song2024","37169966","simulation realism","scDesign3 generates realistic multimodal and spatial single-cell data from a unified model."),
("tian2019","31133762","ground-truth design: cell-line mixtures","CellBench uses designed mixtures of cancer cell lines and RNA as ground truth for pipeline benchmarking."),
("zheng2017","28091601","ground-truth design: cell-line mixtures","Droplet scRNA-seq validated with species-mixing experiments and SNV-based genotype demultiplexing."),
("mcfarland2020","32855387","ground-truth design: cell-line mixtures","MIX-seq pools many cancer cell lines and demultiplexes by SNPs to profile drug responses."),
("mereu2020","32518403","ground-truth design: cell-line mixtures","Reference sample with known composition used to benchmark 13 scRNA-seq protocols."),
("ding2020","32341560","ground-truth design: cell-line mixtures","Systematic protocol comparison using mixtures of cell lines and tissue samples."),
("kang2018","29227470","ground-truth design: genotype multiplexing","demuxlet uses natural genetic variation to assign pooled cells to individuals and detect doublets."),
("heaton2020","32366989","ground-truth design: genotype multiplexing","souporcell clusters cells by genotype without reference genotypes."),
("huang2019","31836005","ground-truth design: genotype multiplexing","Vireo performs Bayesian genotype demultiplexing without reference genotypes."),
("weber2021gs","34553212","ground-truth design: genotype multiplexing","Genetic demultiplexing of pooled tumour scRNA-seq samples is effective in cancer, enabling multiplexed experimental design."),
("cardiello2023","37197983","ground-truth design: genotype multiplexing","Genetic demultiplexing tools evaluated on model-species data."),
("stoeckius2018","30567574","ground-truth design: sample hashing","Cell Hashing with barcoded antibodies enables multiplexing and doublet detection."),
("mcginnis2019multi","31209384","ground-truth design: sample hashing","MULTI-seq lipid-tagged indices for sample multiplexing."),
("howitt2023","37829177","ground-truth design: sample hashing","Benchmark of hashtag-oligo demultiplexing methods."),
("stoeckius2017","28759029","ground-truth design: CITE-seq","CITE-seq simultaneously measures surface epitopes and transcriptome in single cells."),
("peterson2017","28854175","ground-truth design: CITE-seq","REAP-seq quantifies proteins and transcripts in single cells."),
("mimitou2019","31011186","ground-truth design: CITE-seq","ECCITE-seq jointly detects proteins, transcriptomes, clonotypes and CRISPR perturbations."),
("hao2021","34062119","ground-truth design: CITE-seq","Weighted-nearest-neighbour integration of CITE-seq produces a multimodal PBMC reference."),
("svensson2017","28263961","ground-truth design: spike-ins","ERCC spike-ins quantify sensitivity and accuracy of scRNA-seq protocols."),
("jiang2011","21816910","ground-truth design: spike-ins","ERCC synthetic spike-in standards for RNA-seq."),
("ziegenhain2022","35468967","ground-truth design: spike-ins","Molecular spikes provide ground-truth RNA counting for single-cell protocols."),
("ludwig2019","30827679","ground-truth design: mtDNA lineage","Somatic mitochondrial mutations serve as natural lineage barcodes in human cells."),
("lareau2021","32788668","ground-truth design: mtDNA lineage","mtscATAC-seq with mgatk genotypes mtDNA at scale jointly with chromatin."),
("miller2022","35210612","ground-truth design: mtDNA lineage","MAESTER enriches mtDNA variants from 3' scRNA-seq to resolve clones."),
("kwok2022","35260582","ground-truth design: mtDNA lineage","MQuad selects informative mitochondrial variants for clonal substructure."),
("weng2024","38253266","ground-truth design: mtDNA lineage","ReDeeM high-depth mtDNA lineage tracing reconstructs human haematopoietic genealogies."),
("patel2014","24925914","cancer CNV inference","Early inference of large-scale CNVs from scRNA-seq to separate malignant cells in glioblastoma."),
("tirosh2016","27124452","cancer CNV inference","Expression-inferred CNV (inferCNV approach) distinguishes malignant from non-malignant cells in melanoma."),
("fan2018","29898899","cancer CNV inference","HoneyBADGER combines allele and expression signals to infer CNVs/LOH in scRNA-seq."),
("serin2020","31900397","cancer CNV inference","CaSpER integrates allelic shift and expression to identify CNV events."),
("gao2021","33462507","cancer CNV inference","copyKAT infers aneuploidy and clonal substructure to classify tumour vs normal cells."),
("defalco2023","36841879","cancer CNV inference","SCEVAN variational algorithm detects clonal CNV substructure and malignant cells."),
("gao2023","36163550","cancer CNV inference","Numbat uses haplotype-aware allele and expression signals for CNV and clone inference."),
("oketch2024","39200223","cancer CNV inference benchmark","CNV-based tumour-cell identification tools disagree in pancreatic cancer scRNA-seq."),
("chen2025cnv","40584741","cancer CNV inference benchmark","Benchmark of scRNA-seq CNV inference methods shows performance depends on data and reference."),
("song2025cnv","40037644","cancer CNV inference benchmark","CNA inference tools benchmarked using single-cell multi-omic ground truth."),
("dugo2025","41160707","cancer CNV inference benchmark","Tool comparison for tumour-cell detection via CNV in endometrial cancer."),
("sun2021tisch","33179754","cancer atlas/resource","TISCH: curated resource of tumour microenvironment scRNA-seq datasets."),
("han2023tisch2","36321662","cancer atlas/resource","TISCH2 expands curated tumour scRNA-seq datasets and tools."),
("yuan2019","30329142","cancer atlas/resource","CancerSEA maps functional states of cancer cells at single-cell resolution."),
("gavish2023","37258682","cancer atlas/resource","3CA: meta-programs of intratumour heterogeneity across >1000 tumours from curated scRNA-seq."),
("rozenblatt2020","32302568","cancer atlas/resource","HTAN charts tumour transitions across space and time at single-cell resolution."),
("cellxgene2025","39607691","cancer atlas/resource","CZ CELLxGENE Discover aggregates standardised single-cell data."),
("regev2017","29206104","cancer atlas/resource","The Human Cell Atlas vision for reference maps of all human cells."),
("kinker2020","33128048","cancer atlas/resource","Pan-cancer cell-line scRNA-seq identifies recurrent heterogeneity programs."),
("zheng2021","34914499","cancer atlas/resource","Pan-cancer atlas of tumour-infiltrating T cells."),
("cheng2021","33545035","cancer atlas/resource","Pan-cancer atlas of tumour-infiltrating myeloid cells."),
("dixit2016","27984732","ground-truth design: Perturb-seq","Perturb-seq couples pooled CRISPR screens with scRNA-seq readout."),
("adamson2016","27984733","ground-truth design: Perturb-seq","Multiplexed single-cell CRISPR screening dissects the unfolded protein response."),
("replogle2022","35688146","ground-truth design: Perturb-seq","Genome-scale Perturb-seq in K562 and RPE1 maps genotype-phenotype landscapes."),
("frangieh2021","33649592","ground-truth design: Perturb-seq","Perturb-CITE-seq in patient-derived melanoma models defines immune-evasion mechanisms."),
]
pm=[a[1] for a in A if a[1]]
miss=[p for p in pm if p not in S]; S.update(esummary(miss))
rows=[]
crmap={"silberzahn2018":crres["silberzahn2018"],"angelopoulos2023":crres["angelopoulos2023"],"lei2018":crres["lei2018"],
       "vovk2022":crres["vovk_book"],"hubert1985":crres["hubert1985"],"rousseeuw1987":crres["rousseeuw1987"]}
for key,p,cat,claim in A:
    if p:
        s=S[p]; doi=next((x['value'] for x in s['articleids'] if x['idtype']=='doi'),"")
        au=[a['name'] for a in s['authors']]
        rows.append(dict(key=key,pmid=p,doi=doi,authors="; ".join(au[:6])+("; et al." if len(au)>6 else "") or "[no authors listed]",
            year=int(s['pubdate'][:4]),journal=s['source'],title=s['title'].rstrip('.'),category=cat,claim=claim,verified_via="PubMed esummary"))
    elif key=="guo2017":
        rows.append(dict(key=key,pmid="",doi="10.48550/arXiv.1706.04599",authors="Guo C; Pleiss G; Sun Y; Weinberger KQ",year=2017,
            journal="Proceedings of ICML 2017 (PMLR 70); arXiv:1706.04599",title="On Calibration of Modern Neural Networks",category=cat,claim=claim,verified_via="arXiv API (not in PubMed/Crossref)"))
    else:
        c=crmap[key]
        rows.append(dict(key=key,pmid="",doi=c['doi'],authors=c['authors'],year=c['year'],journal=c['journal'] or "Springer (book)",title=c['title'],category=cat,claim=claim,verified_via="Crossref"))
F=pd.DataFrame(rows)
F.loc[F.authors=="","authors"]="[no authors listed]"
print(len(F), F.doi.eq("").sum(), F.duplicated('pmid').sum()-F.pmid.eq("").sum()+1 if F.pmid.eq("").any() else 0)
print(F[F.doi==""][['key','pmid']]); print(F.category.value_counts().to_string())
F.to_csv("foundations_refs.csv",index=False)
```

## Cell 10 · python (python) · ok

Fetching abstracts and inspecting host.llm

```python

import xml.etree.ElementTree as ET
def efetch_abs(pmids):
    out={}
    for i in range(0,len(pmids),100):
        r=requests.post(E+"efetch.fcgi",data=dict(db="pubmed",id=",".join(pmids[i:i+100]),retmode="xml"),timeout=90)
        root=ET.fromstring(r.content)
        for art in root.findall(".//PubmedArticle"):
            p=art.find(".//PMID").text
            out[p]=" ".join("".join(a.itertext()) for a in art.findall(".//AbstractText"))
        time.sleep(0.4)
    return out
ABS=efetch_abs([p for p in F.pmid if p])
print(len(ABS), sum(1 for v in ABS.values() if not v.strip()))
help(host.llm)
```

## Cell 11 · python (python) · ok

Checking claims against abstracts with LLM

```python

tool={"name":"judge","input_schema":{"type":"object","properties":{
  "verdict":{"type":"string","enum":["supported","partially","unsupported"]},
  "revised_claim":{"type":"string","description":"One sentence claim strictly supported by the abstract (keep any numbers only if in abstract)."}},
  "required":["verdict","revised_claim"]}}
idx=[i for i,r in F.iterrows() if r.pmid and ABS.get(r.pmid,"").strip()]
reqs=[{"prompt":f"Title: {F.at[i,'title']}\nAbstract: {ABS[F.at[i,'pmid']]}\n\nClaim: {F.at[i,'claim']}\n\nIs the claim supported by this abstract? Numbers in the claim must appear in the abstract. Give a revised one-sentence claim that the abstract supports, staying close to the original intent.",
       "tools":[tool],"tool_choice":{"type":"tool","name":"judge"},"max_tokens":400,"model":host.reasoning_model()} for i in idx]
res=host.llm(reqs,max_concurrency=16)
F["claim_check"]="not checked (no abstract)"
for i,r in zip(idx,res):
    if "error" in r: continue
    v=r["tool_use"]["input"]; F.at[i,"claim_check"]=v["verdict"]
    if v["verdict"]!="supported": F.at[i,"claim"]=v["revised_claim"]; F.at[i,"claim_check"]=v["verdict"]+" -> revised to abstract"
print(F.claim_check.value_counts().to_string())
print(F[F.claim_check.str.contains("revised")][['key','claim']].to_string()[:3000])
print(F[F.claim_check.str.startswith("not")][['key','pmid']].to_string())
```

## Cell 12 · python (python) · ok

Fixing empty claims and finalising refs CSV

```python

print(F[F.claim.str.strip()==""][['key','claim_check']])
print(F.loc[F.key.isin(['botvinik2020','saelens2019','mereu2020','rautenstrauch2025','steinley2004']),['key','claim','claim_check']].to_string())
```

## Cell 13 · python (python) · ok

Saving foundations_refs.csv

```python

F.loc[F.key=="silberzahn2018","claim"]="Many independent analysis teams given the same data set and question reached varied effect estimates, showing analytic choices drive results."
F.loc[F.claim_check.str.startswith("not"),"claim_check"]="not checked against abstract (no PubMed abstract; claim restricted to title/known scope)"
F=F[["key","pmid","doi","authors","year","journal","title","category","claim","claim_check","verified_via"]]
F.to_csv("foundations_refs.csv",index=False); print(len(F))
```

## Cell 14 · python (python) · ok

Querying GEO for validation-bearing tumour series

```python

SC='("single cell"[All Fields] OR "single-cell"[All Fields] OR scRNA-seq[All Fields] OR snRNA-seq[All Fields] OR "single nucleus"[All Fields] OR scATAC-seq[All Fields] OR "10x Genomics"[All Fields])'
CA='(cancer[All Fields] OR tumor[All Fields] OR tumour[All Fields] OR carcinoma[All Fields] OR leukemia[All Fields] OR leukaemia[All Fields] OR lymphoma[All Fields] OR myeloma[All Fields] OR melanoma[All Fields] OR glioma[All Fields] OR glioblastoma[All Fields] OR sarcoma[All Fields] OR neuroblastoma[All Fields] OR malignant[All Fields] OR neoplasm[All Fields] OR adenocarcinoma[All Fields] OR metastasis[All Fields] OR metastatic[All Fields])'
BASE=f'{SC} AND {CA} AND "Homo sapiens"[Organism] AND gse[Entry Type]'
MOD={
"matched_WES_WGS":'(exome[All Fields] OR "whole genome sequencing"[All Fields] OR "whole-genome sequencing"[All Fields] OR WES[All Fields] OR WGS[All Fields] OR "targeted DNA sequencing"[All Fields])',
"CITE_seq_ADT":'(CITE-seq[All Fields] OR "antibody-derived tag"[All Fields] OR ADT[All Fields] OR TotalSeq[All Fields] OR "surface protein"[All Fields] OR REAP-seq[All Fields] OR "feature barcoding"[All Fields])',
"genotype_multiplexed":'(demuxlet[All Fields] OR souporcell[All Fields] OR vireo[All Fields] OR "genetic demultiplexing"[All Fields] OR demultiplexed[All Fields] OR "natural genetic variation"[All Fields] OR "cell hashing"[All Fields] OR hashtag[All Fields] OR MULTI-seq[All Fields] OR pooled[All Fields])',
"paired_bulk_RNA":'("bulk RNA-seq"[All Fields] OR "bulk RNA sequencing"[All Fields] OR "bulk RNA"[All Fields] OR "bulk transcriptom*"[All Fields] OR "bulk sequencing"[All Fields])',
"paired_spatial":'(Visium[All Fields] OR "spatial transcriptomics"[All Fields] OR "spatial transcriptome"[All Fields] OR Xenium[All Fields] OR CosMx[All Fields] OR MERFISH[All Fields] OR Slide-seq[All Fields] OR "Stereo-seq"[All Fields] OR "spatial RNA"[All Fields] OR GeoMx[All Fields])',
"mtDNA_lineage":'(mtscATAC-seq[All Fields] OR MAESTER[All Fields] OR mtDNA[All Fields] OR "mitochondrial DNA"[All Fields] OR "mitochondrial mutations"[All Fields] OR "mitochondrial variants"[All Fields] OR ASAP-seq[All Fields] OR DOGMA-seq[All Fields])',
"longitudinal_treatment":'(longitudinal[All Fields] OR on-treatment[All Fields] OR "on treatment"[All Fields] OR pre-treatment[All Fields] OR post-treatment[All Fields] OR "before and after"[All Fields] OR "serial biopsies"[All Fields] OR relapse[All Fields] OR "treatment-naive"[All Fields] OR neoadjuvant[All Fields])',
"cell_line_mixture":'("cell line mixture"[All Fields] OR "mixture of cell lines"[All Fields] OR "mixed cell lines"[All Fields] OR "cell lines were mixed"[All Fields] OR "pooled cell lines"[All Fields] OR MIX-seq[All Fields] OR "species-mixing"[All Fields] OR "species mixing"[All Fields] OR "mixture experiment"[All Fields] OR CellBench[All Fields])',
"perturb_seq":'(Perturb-seq[All Fields] OR CROP-seq[All Fields] OR ECCITE-seq[All Fields] OR "CRISPR screen"[All Fields] OR "CRISPR screens"[All Fields] OR "pooled CRISPR"[All Fields] OR "single-cell CRISPR"[All Fields] OR Perturb-CITE-seq[All Fields])',
}
CL_EXTRA='(K562[All Fields] OR "cancer cell line"[All Fields] OR "cancer cell lines"[All Fields] OR "cell lines"[All Fields])'
qlog=[]; ids_by_mod={}
base_res=esearch(BASE,db="gds",retmax=0); qlog.append(("BASE",BASE,int(base_res["count"])))
print("base count",base_res["count"])
for m,clause in MOD.items():
    if m in ("cell_line_mixture","perturb_seq"):
        q=f'{SC} AND ({CA} OR {CL_EXTRA}) AND "Homo sapiens"[Organism] AND gse[Entry Type] AND {clause}'
    else: q=f'{BASE} AND {clause}'
    r=esearch(q,db="gds",retmax=5000); ids_by_mod[m]=r["idlist"]; qlog.append((m,q,int(r["count"])))
    print(m,r["count"],len(r["idlist"])); time.sleep(0.4)
```

## Cell 15 · python (python) · ok

Fetching GEO esummary metadata for union

```python

union=sorted({i for v in ids_by_mod.values() for i in v})
print(len(union))
G=esummary(union,db="gds")
print(len(G)); k=next(iter(G)); print({a:(str(b)[:80]) for a,b in G[k].items()})
```

## Cell 16 · python (python) · ok

Building GEO table and regex modality rules

```python

import ast
recs=[]
for u,s in G.items():
    samp=s.get('samples') or []
    stitles=" | ".join(x.get('title','') for x in samp[:60]) if isinstance(samp,list) else ""
    recs.append(dict(uid=u,gse="GSE"+s['gse'] if s.get('gse') else s['accession'],accession=s['accession'],title=s['title'],summary=s['summary'],
        gdstype=s['gdstype'],gpl=s['gpl'],taxon=s['taxon'],n_samples=int(s['n_samples'] or 0),year=int(s['pdat'][:4]),
        pubmed_ids=";".join(map(str,s.get('pubmedids') or [])),sample_titles=stitles,suppfile=s.get('suppfile',''),bioproject=s.get('bioproject','')))
D=pd.DataFrame(recs)
D["query_hits"]=D.uid.map(lambda u:";".join(m for m,v in ids_by_mod.items() if u in v))
D["txt"]=(D.title+" . "+D.summary).str.replace(r"\s+"," ",regex=True)
D["txt_all"]=D.txt+" . "+D.sample_titles
def rx(p): return re.compile(p,re.I)
SCRX=rx(r"single[- ]?cell|single[- ]nucle|scRNA|snRNA|scATAC|snATAC|10x|chromium|drop-?seq|smart-?seq|CITE-seq|scDNA|per[- ]cell|Perturb-seq|CROP-seq|MAESTER|mtscATAC|ASAP-seq|DOGMA|multiome")
CARX=rx(r"cancer|tumou?r|carcinoma|leuka?emia|lymphoma|myeloma|melanoma|gliom|glioblastoma|sarcoma|blastoma|malignan|neoplas|metasta|adenocarcinoma|myelodysplas|MDS\b|myeloproliferative|K562|HeLa|cancer cell line|mesothelioma|seminoma|CLL\b|AML\b|ALL\b")
RULES={
"matched_WES_WGS":r"whole[- ]exome|\bexome|\bWES\b|whole[- ]genome sequencing|\bWGS\b|targeted (DNA )?sequencing|DNA sequencing of (the )?(matched|tumou?r)|scDNA-seq|genomic DNA",
"CITE_seq_ADT":r"CITE-?seq|antibody[- ]derived tag|\bADTs?\b|TotalSeq|REAP-seq|ECCITE|surface protein|surface[- ]marker (expression|protein)s?.{0,40}(seq|antibod)|oligo[- ]conjugated antibod|DOGMA|ASAP-seq|TEA-seq|feature barcod",
"genotype_multiplexed":r"demuxlet|souporcell|vireo|freemuxlet|scSplit|genetic(ally)? demultiplex|demultiplex\w* (by|using|based on) (genotype|SNP|natural genetic)|natural genetic variation|genotype[- ]based demultiplex|cell hashing|hashtag|\bHTOs?\b|MULTI-seq|lipid[- ]tag|sample multiplex|multiplexed (samples|donors|patients)|pooled (samples|donors|patients|cell lines)|cells? from \w+ (patients|donors) (were )?pooled|CellPlex|CMO",
"paired_bulk_RNA":r"bulk RNA|bulk transcriptom|bulk sequencing|bulk RNA-?seq|bulk tumou?r (RNA|expression|transcript)|matched bulk|bulk-?seq",
"paired_spatial":r"Visium|spatial(ly resolved)? transcriptom|Xenium|CosMx|MERFISH|Slide-?seq|Stereo-?seq|GeoMx|spatial RNA|spatial gene expression|seqFISH|spatial omics|spatial multi-?omic|spatial profil|DBiT|STARmap|HDST",
"mtDNA_lineage":r"mtscATAC|MAESTER|\bmtDNA\b|mitochondrial DNA (mutation|variant|heteroplasm|lineage|genotyp)|mitochondrial (mutation|variant)s?|ASAP-seq|DOGMA-seq|ReDeeM|heteroplasm",
"longitudinal_treatment":r"longitudinal|on[- ]treatment|pre-? ?(and|/|vs\.?|versus) ?post-?[- ]?treatment|pre-?treatment|post-?treatment|before and after (treatment|therapy)|serial (biops|samples|sampling)|baseline and (on|post)|time ?points?|follow-up samples|at diagnosis and (at )?relapse|diagnosis.{0,20}relapse|paired (primary and )?relapse|neoadjuvant|resistance (emerg|acquir)|acquired resistance",
"cell_line_mixture":r"cell[- ]line mixture|mixture of (\w+ )?(cancer )?cell lines|mixed (cancer )?cell lines|cell lines were (mixed|pooled)|pool(ed|ing)? (of )?(\d+ |several |multiple |many )?(cancer )?cell lines|MIX-seq|species[- ]mix|human[- ]mouse mix|CellBench|in silico mixture|mixture (control )?experiment|barnyard",
"perturb_seq":r"Perturb-?seq|CROP-?seq|ECCITE-?seq|Perturb-CITE|CRISPR (screen|perturbation)s?|pooled CRISPR|single[- ]cell CRISPR|sgRNA library|guide RNA library|CRISPRi screen|CRISPRa screen|perturbation screen|Mosaic-seq|TAP-seq",
}
RR={m:rx(p) for m,p in RULES.items()}
for m,r in RR.items(): D["rx_"+m]=D.txt_all.str.contains(r)
D["rx_sc"]=D.txt_all.str.contains(SCRX); D["rx_ca"]=D.txt_all.str.contains(CARX)
D["is_seq"]=D.gdstype.str.contains("sequencing",case=False)
print(D[["rx_sc","rx_ca","is_seq"]].sum().to_dict())
keep=D.rx_sc & D.is_seq
print("kept sc+seq",keep.sum())
print(D.loc[keep,[c for c in D if c.startswith("rx_") and c not in("rx_sc","rx_ca")]].sum().to_string())
```

## Cell 17 · python (python) · ok

Testing GEO SOFT text endpoint reachability

```python

try:
    r=requests.get("https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi",params=dict(acc="GSE132465",targ="self",form="text",view="brief"),timeout=30)
    print(r.status_code, r.text[:1500])
except Exception as e: print("ERR",e)
```

## Cell 18 · python (python) · ok

Fetching GEO series SOFT text for all candidates

```python

from concurrent.futures import ThreadPoolExecutor
import os, pickle
SOFT={}
def get_soft(acc, targ="self"):
    for t in range(4):
        try:
            r=requests.get("https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi",params=dict(acc=acc,targ=targ,form="text",view="brief"),timeout=60)
            if r.status_code==200 and r.text.startswith("^"): return r.text
            time.sleep(2+t*2)
        except Exception: time.sleep(2+t*2)
    return None
def worker(acc):
    time.sleep(0.9); return acc,get_soft(acc)
with ThreadPoolExecutor(3) as ex:
    for acc,txt in ex.map(worker,D.accession.tolist()):
        SOFT[acc]=txt
pickle.dump(SOFT,open("geo_soft_self.pkl","wb"))
print(len(SOFT), sum(v is None for v in SOFT.values()))
```

## Cell 19 · bash (python) · ok

Checking surviving workspace files

```bash
ls -la *.csv *.tsv *.pkl 2>/dev/null; wc -l foundations_refs.csv
```

## Cell 20 · bash (python) · ok

Writing resumable GEO fetch script

```bash
mkdir -p geo && cat > geo/geo_fetch.py <<'EOF'
import requests, time, json, os, sys, pandas as pd
from concurrent.futures import ThreadPoolExecutor
E="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
def esearch(term, db="gds", retmax=5000):
    for i in range(5):
        try: return requests.get(E+"esearch.fcgi",params=dict(db=db,term=term,retmax=retmax,retmode="json"),timeout=60).json()["esearchresult"]
        except Exception: time.sleep(2)
def esummary(ids, db="gds"):
    out={}
    for i in range(0,len(ids),200):
        for t in range(5):
            try: j=requests.post(E+"esummary.fcgi",data=dict(db=db,id=",".join(ids[i:i+200]),retmode="json"),timeout=90).json()["result"]; break
            except Exception: time.sleep(3)
        for u in j.get("uids",[]): out[u]=j[u]
        time.sleep(0.4)
    return out
SC='("single cell"[All Fields] OR "single-cell"[All Fields] OR scRNA-seq[All Fields] OR snRNA-seq[All Fields] OR "single nucleus"[All Fields] OR scATAC-seq[All Fields] OR "10x Genomics"[All Fields])'
CA='(cancer[All Fields] OR tumor[All Fields] OR tumour[All Fields] OR carcinoma[All Fields] OR leukemia[All Fields] OR leukaemia[All Fields] OR lymphoma[All Fields] OR myeloma[All Fields] OR melanoma[All Fields] OR glioma[All Fields] OR glioblastoma[All Fields] OR sarcoma[All Fields] OR neuroblastoma[All Fields] OR malignant[All Fields] OR neoplasm[All Fields] OR adenocarcinoma[All Fields] OR metastasis[All Fields] OR metastatic[All Fields])'
BASE=f'{SC} AND {CA} AND "Homo sapiens"[Organism] AND gse[Entry Type]'
CL_EXTRA='(K562[All Fields] OR "cancer cell line"[All Fields] OR "cancer cell lines"[All Fields] OR "cell lines"[All Fields])'
MOD={
"matched_WES_WGS":'(exome[All Fields] OR "whole genome sequencing"[All Fields] OR "whole-genome sequencing"[All Fields] OR WES[All Fields] OR WGS[All Fields] OR "targeted DNA sequencing"[All Fields])',
"CITE_seq_ADT":'(CITE-seq[All Fields] OR "antibody-derived tag"[All Fields] OR ADT[All Fields] OR TotalSeq[All Fields] OR "surface protein"[All Fields] OR REAP-seq[All Fields] OR "feature barcoding"[All Fields])',
"genotype_multiplexed":'(demuxlet[All Fields] OR souporcell[All Fields] OR vireo[All Fields] OR "genetic demultiplexing"[All Fields] OR demultiplexed[All Fields] OR "natural genetic variation"[All Fields] OR "cell hashing"[All Fields] OR hashtag[All Fields] OR MULTI-seq[All Fields] OR pooled[All Fields])',
"paired_bulk_RNA":'("bulk RNA-seq"[All Fields] OR "bulk RNA sequencing"[All Fields] OR "bulk RNA"[All Fields] OR "bulk transcriptom*"[All Fields] OR "bulk sequencing"[All Fields])',
"paired_spatial":'(Visium[All Fields] OR "spatial transcriptomics"[All Fields] OR "spatial transcriptome"[All Fields] OR Xenium[All Fields] OR CosMx[All Fields] OR MERFISH[All Fields] OR Slide-seq[All Fields] OR "Stereo-seq"[All Fields] OR "spatial RNA"[All Fields] OR GeoMx[All Fields])',
"mtDNA_lineage":'(mtscATAC-seq[All Fields] OR MAESTER[All Fields] OR mtDNA[All Fields] OR "mitochondrial DNA"[All Fields] OR "mitochondrial mutations"[All Fields] OR "mitochondrial variants"[All Fields] OR ASAP-seq[All Fields] OR DOGMA-seq[All Fields])',
"longitudinal_treatment":'(longitudinal[All Fields] OR on-treatment[All Fields] OR "on treatment"[All Fields] OR pre-treatment[All Fields] OR post-treatment[All Fields] OR "before and after"[All Fields] OR "serial biopsies"[All Fields] OR relapse[All Fields] OR "treatment-naive"[All Fields] OR neoadjuvant[All Fields])',
"cell_line_mixture":'("cell line mixture"[All Fields] OR "mixture of cell lines"[All Fields] OR "mixed cell lines"[All Fields] OR "cell lines were mixed"[All Fields] OR "pooled cell lines"[All Fields] OR MIX-seq[All Fields] OR "species-mixing"[All Fields] OR "species mixing"[All Fields] OR "mixture experiment"[All Fields] OR CellBench[All Fields])',
"perturb_seq":'(Perturb-seq[All Fields] OR CROP-seq[All Fields] OR ECCITE-seq[All Fields] OR "CRISPR screen"[All Fields] OR "CRISPR screens"[All Fields] OR "pooled CRISPR"[All Fields] OR "single-cell CRISPR"[All Fields] OR Perturb-CITE-seq[All Fields])',
}
step=sys.argv[1]
if step=="search":
    qlog=[]; ids={}
    b=esearch(BASE,retmax=0); qlog.append(dict(modality="BASE (all human tumour single-cell GSE)",query=BASE,count=int(b["count"])))
    for m,c in MOD.items():
        q=(f'{SC} AND ({CA} OR {CL_EXTRA}) AND "Homo sapiens"[Organism] AND gse[Entry Type] AND {c}' if m in("cell_line_mixture","perturb_seq") else f'{BASE} AND {c}')
        r=esearch(q); ids[m]=r["idlist"]; qlog.append(dict(modality=m,query=q,count=int(r["count"]))); time.sleep(0.4)
    json.dump(dict(qlog=qlog,ids=ids),open("geo/queries.json","w"))
    union=sorted({i for v in ids.values() for i in v})
    G=esummary(union); json.dump(G,open("geo/esummary.json","w"))
    print(len(union),len(G))
elif step=="soft":
    G=json.load(open("geo/esummary.json"))
    accs=[g["accession"] for g in G.values()]
    done=set()
    if os.path.exists("geo/soft.jsonl"):
        for l in open("geo/soft.jsonl"): done.add(json.loads(l)["acc"])
    todo=[a for a in accs if a not in done]; print("todo",len(todo),flush=True)
    def get(acc):
        time.sleep(0.8)
        for t in range(4):
            try:
                r=requests.get("https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi",params=dict(acc=acc,targ="self",form="text",view="brief"),timeout=60)
                if r.status_code==200 and r.text.startswith("^"): return acc,r.text
            except Exception: pass
            time.sleep(2+2*t)
        return acc,None
    with open("geo/soft.jsonl","a") as fh, ThreadPoolExecutor(3) as ex:
        for n,(acc,txt) in enumerate(ex.map(get,todo)):
            fh.write(json.dumps(dict(acc=acc,txt=txt))+"\n"); fh.flush()
            if n%200==0: print(n,flush=True)
    print("done")
EOF
cd . && python geo/geo_fetch.py search
```

## Cell 21 · bash (python) · ok

Fetching GEO SOFT text resumably

```bash
python geo/geo_fetch.py soft 2>&1 | tail -3
```

## Cell 22 · python (python) · ok

Resolving GPL platform titles

```python

import json, requests, time, re, pandas as pd
E="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
G=json.load(open("geo/esummary.json"))
gpls=sorted({g for s in G.values() for g in (s.get('gpl') or '').split(';') if g})
print(len(gpls))
GPL={}
uids=[str(100000000+int(g)) for g in gpls]
for i in range(0,len(uids),200):
    j=requests.post(E+"esummary.fcgi",data=dict(db="gds",id=",".join(uids[i:i+200]),retmode="json"),timeout=90).json()["result"]
    for u in j.get("uids",[]): GPL[j[u]['accession']]=j[u]['title']
    time.sleep(0.4)
json.dump(GPL,open("geo/gpl_titles.json","w")); print(len(GPL), list(GPL.items())[:3])
```

## Cell 23 · repl · ok

Peeking at SOFT fetch progress

```python
print(host.exec_peek("5231f19b-e273-410a-8c2f-22ce06c12786"))
import os; print(sum(1 for _ in open("geo/soft.jsonl")) if os.path.exists("geo/soft.jsonl") else 0)
```

## Cell 24 · python (python) · ok

Defining modality, cancer-type and task rules

```python

def rx(p): return re.compile(p,re.I)
SCRX=rx(r"single[- ]?cell|single[- ]nucle|scRNA|snRNA|scATAC|snATAC|10x|chromium|drop-?seq|smart-?seq|CITE-seq|scDNA|Perturb-seq|CROP-seq|MAESTER|mtscATAC|ASAP-seq|DOGMA|multiome|BD Rhapsody|seq-?well|sci-RNA")
CARX=rx(r"cancer|tumou?r|carcinoma|leuka?emi|lymphoma|myeloma|melanoma|gliom|glioblastoma|sarcoma|blastoma|malignan|neoplas|metasta|adenocarcinoma|myelodysplas|\bMDS\b|myeloproliferative|K562|HeLa|mesothelioma|seminoma|\bCLL\b|\bAML\b|\bB-ALL\b|\bT-ALL\b|\bHCC\b|\bNSCLC\b|\bccRCC\b|\bPDAC\b")
RULES={
"matched_WES_WGS":r"whole[- ]exome|\bexomes?\b|\bWES\b|whole[- ]genome (sequencing|seq)|\bWGS\b|targeted (DNA |panel )?sequencing|scDNA-seq|single[- ]cell DNA|DNA-seq|copy[- ]number (profiling|sequencing) of (bulk|DNA)|shallow WGS|low[- ]pass WGS",
"CITE_seq_ADT":r"CITE-?seq|antibody[- ]derived tags?|\bADTs?\b|TotalSeq|REAP-seq|ECCITE|surface protein|oligo(nucleotide)?[- ]conjugated antibod|barcoded antibod|DOGMA-seq|ASAP-seq|TEA-seq|AbSeq|feature barcod",
"genotype_multiplexed":r"demuxlet|freemuxlet|souporcell|vireo|scSplit|genetic(ally)? demultiplex|genotype[- ](based )?demultiplex|demultiplex\w* (by|using|based on|with) (genotype|SNP|single nucleotide|natural genetic|germline)|natural genetic variation|cell hashing|hashtag|\bHTOs?\b|MULTI-seq|lipid[- ]tag|CellPlex|\bCMOs?\b|cell multiplexing oligo|sample multiplex|multiplexed (samples|donors|patients|cell lines)|(samples|donors|patients|cell lines) were (multiplexed|pooled)|pooled (samples|donors|patients|cell lines)",
"paired_bulk_RNA":r"bulk RNA|bulk transcriptom|bulk[- ]seq|bulk sequencing|bulk tumou?r (RNA|expression|transcript)|matched bulk|bulk (and|vs\.?|versus) single[- ]cell|bulk profil",
"paired_spatial":r"Visium|spatial(ly resolved)? transcriptom|Xenium|CosMx|MERFISH|Slide-?seq|Stereo-?seq|GeoMx|spatial RNA|spatial gene expression|seqFISH|spatial (multi-?)?omic|spatial profil|DBiT|STARmap|HDST|spatial transcript",
"mtDNA_lineage":r"mtscATAC|MAESTER|\bmtDNA\b|mitochondrial DNA (mutation|variant|heteroplasm|lineage|genotyp)|mitochondrial (somatic )?(mutation|variant)s?|ASAP-seq|DOGMA-seq|ReDeeM|heteroplasm",
"longitudinal_treatment":r"longitudinal|on[- ]treatment|pre-? ?(and|/|vs\.?|versus) ?post-?[- ]?(treatment|therapy)|pre-?treatment|post-?treatment|before and after (treatment|therapy|\w+ (treatment|therapy))|serial(ly)? (biops|samples|sampl|collected)|baseline and (on|post)|at diagnosis and (at )?relapse|diagnosis (and|to) relapse|paired (primary and )?relapse|matched relapse|neoadjuvant|acquired resistance|(during|after) (treatment|therapy) with|time ?course of (treatment|therapy)",
"cell_line_mixture":r"cell[- ]line mixture|mixture of (\w+ )?(cancer )?cell lines|mixed (cancer )?cell lines|cell lines were (mixed|pooled)|pool(ed|ing)? (of )?(\d+ |several |multiple |many |\w+ )?(cancer )?cell lines|MIX-seq|species[- ]mix|human[- ]mouse mix|CellBench|mixture (control )?experiment|barnyard|known (proportion|mixture)",
"perturb_seq":r"Perturb-?seq|CROP-?seq|ECCITE-?seq|Perturb-CITE|CRISPR(i|a|-KO)? (screen|perturbation)s?|pooled CRISPR|single[- ]cell CRISPR|sgRNA library|guide RNA library|perturbation screen|Mosaic-seq|TAP-seq|CRISPR-?(based )?(knockout|interference|activation) screen",
}
RR={m:rx(p) for m,p in RULES.items()}
CANCER=[ # (label, regex) ordered: specific first
("acute myeloid leukaemia",r"acute myeloid|\bAML\b"),("acute lymphoblastic leukaemia",r"acute lymphoblastic|\bB-ALL\b|\bT-ALL\b|\bALL\b patients"),
("chronic lymphocytic leukaemia",r"chronic lymphocytic|\bCLL\b"),("chronic myeloid leukaemia",r"chronic myeloid|\bCML\b|K562"),
("myelodysplastic/myeloproliferative",r"myelodysplas|\bMDS\b|myeloproliferative|\bMPN\b|myelofibrosis|clonal haematopoiesis|clonal hematopoiesis|\bCHIP\b"),
("multiple myeloma",r"myeloma|plasma cell neoplas"),("lymphoma",r"lymphoma|\bDLBCL\b|Hodgkin|mycosis fungoides|S[ée]zary|\bCTCL\b"),
("leukaemia (other/unspecified)",r"leuka?emi"),
("glioma/glioblastoma",r"gliom|glioblastoma|\bGBM\b|astrocytom|oligodendrogliom|\bDIPG\b|ependymom"),("medulloblastoma",r"medulloblastom"),
("neuroblastoma",r"neuroblastom"),("brain metastasis",r"brain metasta"),
("melanoma",r"melanoma"),("uveal melanoma",r"uveal melanoma"),
("breast cancer",r"breast|mammary|\bTNBC\b"),("lung cancer",r"lung|\bNSCLC\b|\bSCLC\b|\bLUAD\b|\bLUSC\b"),
("colorectal cancer",r"colorectal|colon|rectal|\bCRC\b"),("hepatocellular/liver cancer",r"hepatocellular|\bHCC\b|liver cancer|hepatoblastom|cholangiocarcinom|biliary"),
("pancreatic cancer",r"pancrea|\bPDAC\b"),("gastric cancer",r"gastric|stomach"),("oesophageal cancer",r"oesophag|esophag|\bESCC\b"),
("head and neck cancer",r"head and neck|\bHNSCC\b|oral (squamous|cancer)|nasopharyn|laryn|oropharyn|tongue"),
("prostate cancer",r"prostat"),("bladder/urothelial cancer",r"bladder|urothelial"),("renal cell carcinoma",r"renal|kidney|\bccRCC\b|\bRCC\b|Wilms"),
("ovarian cancer",r"ovar|\bHGSOC\b"),("endometrial/uterine cancer",r"endometri|uterine"),("cervical cancer",r"cervical|cervix"),
("thyroid cancer",r"thyroid"),("sarcoma",r"sarcoma|Ewing|\bGIST\b"),("skin (non-melanoma)",r"basal cell carcinoma|cutaneous squamous|\bcSCC\b|Merkel"),
("mesothelioma",r"mesothelioma"),("nasopharyngeal",r"nasopharyn"),("retinoblastoma",r"retinoblastom"),("germ cell tumour",r"germ cell tumou?r|seminoma|teratom"),
("adrenal/neuroendocrine",r"neuroendocrine|pheochromocytom|paragangliom|adrenocortical"),
]
CRX=[(l,rx(p)) for l,p in CANCER]
PANRX=rx(r"pan-?cancer|multiple (cancer|tumou?r) types|across (\d+|several|multiple) (cancer|tumou?r) types")
def cancer_types(t):
    if PANRX.search(t): return "pan-cancer/multiple"
    labs=[l for l,r in CRX if r.search(t)]
    if "uveal melanoma" in labs: labs=[l for l in labs if l!="melanoma"]
    if any(l.startswith(("acute","chronic")) for l in labs): labs=[l for l in labs if l!="leukaemia (other/unspecified)"]
    return "; ".join(labs[:3])+(" (+)" if len(labs)>3 else "") if labs else "unspecified"
TASKS={ # benchmark task -> modalities enabling it
"malignant_calling":["matched_WES_WGS","genotype_multiplexed","cell_line_mixture","mtDNA_lineage"],
"clone_calling":["matched_WES_WGS","mtDNA_lineage","genotype_multiplexed"],
"deconvolution":["paired_bulk_RNA","paired_spatial","cell_line_mixture"],
"annotation_calibration":["CITE_seq_ADT","genotype_multiplexed","cell_line_mixture"],
"CCC_spatial_referee":["paired_spatial"],
"pipeline_robustness":["genotype_multiplexed","cell_line_mixture","longitudinal_treatment","perturb_seq","paired_bulk_RNA"],
"perturbation_response":["perturb_seq","longitudinal_treatment"],
}
print("ok")
```

## Cell 25 · python (python) · ok

Parsing SOFT text and applying regex rules

```python

SOFT={}
for l in open("geo/soft.jsonl"):
    d=json.loads(l); SOFT[d["acc"]]=d["txt"]
print(len(SOFT), sum(v is None for v in SOFT.values()))
def soft_fields(t):
    f={}
    for line in (t or "").splitlines():
        if line.startswith("!Series_"):
            k,_,v=line[8:].partition(" = "); f.setdefault(k,[]).append(v)
    return f
Q=json.load(open("geo/queries.json")); ids_by_mod=Q["ids"]
recs=[]
for u,s in G.items():
    f=soft_fields(SOFT.get(s['accession']))
    samp=s.get('samples') or []
    recs.append(dict(uid=u,gse=s['accession'],title=s['title'],summary=s['summary'],overall_design=" ".join(f.get("overall_design",[])),
        relations="; ".join(f.get("relation",[])),gdstype=s['gdstype'],gpl=s['gpl'],taxon=s['taxon'],n_samples=int(s['n_samples'] or 0),
        year=int(s['pdat'][:4]),pubmed_ids=";".join(map(str,s.get('pubmedids') or [])),
        sample_titles=" | ".join(x.get('title','') for x in samp[:80]),suppfile=s.get('suppfile','')))
D=pd.DataFrame(recs)
D["query_hits"]=D.uid.map(lambda u:";".join(m for m,v in ids_by_mod.items() if u in v))
D["txt"]=(D.title+" . "+D.summary+" . "+D.overall_design).str.replace(r"\s+"," ",regex=True)
D["txt_all"]=D.txt+" . "+D.sample_titles
D["is_seq"]=D.gdstype.str.contains("sequencing",case=False)
D["rx_sc"]=D.txt_all.str.contains(SCRX); D["rx_ca"]=D.txt_all.str.contains(CARX)
D["human"]=D.taxon.str.contains("Homo sapiens")
import warnings; warnings.filterwarnings("ignore")
for m,r in RR.items(): D["rx_"+m]=D.txt_all.str.contains(r)
modcols=["rx_"+m for m in RULES]
D["n_rx"]=D[modcols].sum(1)
elig=D.is_seq & D.rx_sc & D.rx_ca & D.human
print("eligible",elig.sum(),"with>=1 modality",(elig&(D.n_rx>0)).sum())
print(D.loc[elig,modcols].sum().to_string())
D.to_pickle("geo/D_regex.pkl")
```

## Cell 26 · python (python) · FAILED

LLM adjudication of modalities on 1460 series

```python

MODS=list(RULES)
tool={"name":"classify","input_schema":{"type":"object","properties":{
 "human_cancer_single_cell":{"type":"boolean","description":"Series contains single-cell/single-nucleus data from human tumour/cancer patient samples or human cancer cell lines"},
 "sample_source":{"type":"string","enum":["patient tumour","cancer cell line","PDX/organoid","mixed","non-cancer"]},
 "cancer_type":{"type":"string","description":"short canonical cancer type(s), e.g. 'lung adenocarcinoma'; 'pan-cancer' if many"},
 "modalities":{"type":"array","items":{"type":"string","enum":MODS},
   "description":"Only modalities that this study actually generated or paired for the same patients/samples (including companion SubSeries/controlled-access), not ones merely cited or from unrelated public data"}},
 "required":["human_cancer_single_cell","sample_source","cancer_type","modalities"]}}
DEF=("Modality definitions: matched_WES_WGS = exome/genome/targeted DNA or scDNA sequencing of the same tumours/patients; "
"CITE_seq_ADT = antibody-oligo surface protein measured in the same cells (CITE-seq, TotalSeq, AbSeq, ASAP/DOGMA/TEA-seq); "
"genotype_multiplexed = several donors/samples/cell lines pooled in one lane and demultiplexed by genotype or hashtags/CMOs; "
"paired_bulk_RNA = bulk RNA-seq of the same tumours/samples; paired_spatial = spatial transcriptomics/proteomics of the same tumours; "
"mtDNA_lineage = mitochondrial DNA variants used for clonal/lineage tracing; longitudinal_treatment = same patients/models sampled at >=2 time points or pre/on/post treatment; "
"cell_line_mixture = designed mixture of distinct cell lines or species with known identity; perturb_seq = pooled CRISPR perturbations with single-cell readout.")
sub=D[elig&(D.n_rx>0)].copy()
def mk(r):
    t=f"GEO {r.gse} | {r.title}\nSUMMARY: {r.summary[:1100]}\nDESIGN: {r.overall_design[:700]}\nSAMPLES: {r.sample_titles[:300]}\nRegex flagged: {', '.join(m for m in MODS if r['rx_'+m])}"
    return {"prompt":DEF+"\n\n"+t+"\n\nClassify this GEO series.","tools":[tool],"tool_choice":{"type":"tool","name":"classify"},"max_tokens":300}
reqs=[mk(r) for _,r in sub.iterrows()]
out=[]
for i in range(0,len(reqs),500):
    out+=host.llm(reqs[i:i+500],max_concurrency=24)
json.dump([o.get("tool_use",{}).get("input") if "error" not in o else {"error":o["error"]} for o in out],open("geo/llm_out.json","w"))
print(len(out), sum("error" in o for o in out))
```

## Cell 27 · python (python) · ok

Regex-only classification with evidence snippets

```python

# Negative/precision filters
NEG={
"matched_WES_WGS":rx(r"(TCGA|public|previously published|published)\W{0,3}.{0,40}(exome|WES|WGS)"),
"paired_bulk_RNA":rx(r"(TCGA|GTEx|ICGC|CPTAC|public(ly available)?) .{0,40}bulk|bulk .{0,40}(TCGA|GTEx|ICGC)"),
}
CELLLINE=rx(r"cell lines?\b|K562|HeLa|MCF-?7|A549|HCT-?116|Jurkat|THP-1|HEK293|organoid|PDX|xenograft")
PATIENT=rx(r"patients?|biops|resect|surgical|primary tumou?r|specimen")
def snippet(r,t):
    m=r.search(t); 
    return "" if not m else t[max(0,m.start()-60):m.end()+60].replace("\n"," ")
def classify(row):
    t=row.txt_all; mods=[]; ev={}
    for m,r in RR.items():
        if r.search(t):
            if m in NEG and NEG[m].search(t) and len(r.findall(t))<=1: continue
            mods.append(m); ev[m]=snippet(r,t)
    return mods,ev
C=D[elig].copy()
res=C.apply(classify,axis=1)
C["validation_modalities"]=[";".join(x[0]) for x in res]
C["evidence"]=[" || ".join(f"{k}: …{v}…" for k,v in x[1].items()) for x in res]
C=C[C.validation_modalities!=""]
C["cancer_type"]=C.txt_all.map(cancer_types)
C["sample_source"]=C.txt.map(lambda t:"patient tumour + model" if (PATIENT.search(t) and CELLLINE.search(t)) else "cancer cell line/model" if CELLLINE.search(t) else "patient tumour" if PATIENT.search(t) else "unspecified")
C["platform"]=C.gpl.map(lambda g:"; ".join(f"GPL{x}: {GPL.get('GPL'+x,'')}" for x in g.split(";") if x))
C["is_superseries"]=C.summary.str.contains("SuperSeries",case=False)|C.relations.str.contains("SubSeries")
def tasks(ms):
    s=set(ms.split(";")); return ";".join(k for k,v in TASKS.items() if s & set(v))
TASKS["malignant_calling"]=["matched_WES_WGS","cell_line_mixture"]
TASKS["clone_calling"]=["matched_WES_WGS","mtDNA_lineage"]
C["benchmark_tasks"]=C.validation_modalities.map(tasks)
print(len(C)); 
for m in MODS: print(m, C.validation_modalities.str.contains(m).sum())
```

## Cell 28 · python (python) · ok

Sampling hits per modality for manual audit

```python

lines=[]; AUD=[]
for m in MODS:
    s=C[C.validation_modalities.str.contains(m)].sample(min(8,C.validation_modalities.str.contains(m).sum()),random_state=1)
    for _,r in s.iterrows():
        ev=[e for e in r.evidence.split(" || ") if e.startswith(m)][0]
        lines.append(f"[{m}] {r.gse} | {r.title[:90]} || {ev[len(m)+2:][:230]}"); AUD.append((m,r.gse))
open("geo/audit.txt","w").write("\n".join(lines)); print(len(lines))
```

## Cell 29 · python (python) · ok

Tightening rules and re-auditing weak modalities

```python

RULES["mtDNA_lineage"]=r"mtscATAC|MAESTER|ReDeeM|mito(chondrial)?[- ]?(DNA )?(somatic )?(mutation|variant)s? .{0,60}(lineage|clon|tracing|tree)|(lineage|clon\w*) .{0,60}mito(chondrial)? ?(DNA )?(mutation|variant)|mtDNA (mutation|variant)s? .{0,60}(lineage|clon|tracing)|(lineage|clon\w*) .{0,60}mtDNA (mutation|variant)|heteroplasm.{0,60}(lineage|clon)|mitochondrial (DNA )?genotyp"
RULES["perturb_seq"]=r"Perturb-?seq|CROP-?seq|ECCITE-?seq|Perturb-CITE|Perturb-ATAC|Spear-ATAC|single[- ]cell CRISPR|CRISPR[^.]{0,80}(single[- ]cell|scRNA|10x)|(single[- ]cell|scRNA)[^.]{0,80}CRISPR (screen|perturbation)|Mosaic-seq|TAP-seq|CRISPR droplet sequencing|sgRNA[^.]{0,40}(capture|single[- ]cell)"
RULES["longitudinal_treatment"]=r"longitudinal|on[- ]treatment|pre-? ?(and|/|vs\.?|versus) ?post-?[- ]?(treatment|therapy)|pre-?treatment|post-?treatment|before and after (treatment|therapy|\w+ (treatment|therapy))|serial(ly)? (biops|samples|sampl|collected)|baseline and (on|post)|at diagnosis and (at )?relapse|diagnosis (and|to) relapse|paired (primary and )?relapse|matched relapse|acquired resistance|(multiple|several|\d+) time ?points|across .{0,30}timepoints|treatment timepoints|(during|after) (treatment|therapy) with"
RULES["cell_line_mixture"]=RULES["cell_line_mixture"].replace("|human[- ]mouse mix","")
CITE_ONLY_HASH=rx(r"TotalSeq[^.]{0,30}(hashtag|HTO)|hashtag antibod")
CITE_STRONG=rx(r"CITE-?seq|antibody[- ]derived tags?|\bADTs?\b|REAP-seq|ECCITE|surface protein|AbSeq|DOGMA-seq|ASAP-seq|TEA-seq|feature barcod|TotalSeq-?[ABC]? (antibod|panel)")
NEG["paired_bulk_RNA"]=rx(r"bulk[^.]{0,40}(TCGA|TARGET|GTEx|ICGC|CPTAC|public)|(TCGA|TARGET|GTEx|ICGC|CPTAC|public(ly available)?)[^.]{0,60}bulk")
RR={m:rx(p) for m,p in RULES.items()}
def classify(row):
    t=row.txt_all; mods=[]; ev={}
    for m,r in RR.items():
        if r.search(t):
            if m in NEG and NEG[m].search(t) and len(r.findall(t))<=1: continue
            if m=="CITE_seq_ADT" and CITE_ONLY_HASH.search(t) and not CITE_STRONG.search(t): continue
            mods.append(m); ev[m]=snippet(r,t)
    return mods,ev
C=D[elig].copy(); res=C.apply(classify,axis=1)
C["validation_modalities"]=[";".join(x[0]) for x in res]
C["evidence"]=[" || ".join(f"{k}: …{v}…" for k,v in x[1].items()) for x in res]
C=C[C.validation_modalities!=""].copy()
for m in MODS: print(m, C.validation_modalities.str.contains(m).sum())
lines=[]
for m in ["mtDNA_lineage","perturb_seq","longitudinal_treatment","paired_bulk_RNA"]:
    s=C[C.validation_modalities.str.contains(m)].sample(10,random_state=7)
    for _,r in s.iterrows():
        ev=[e for e in r.evidence.split(" || ") if e.startswith(m)][0]
        lines.append(f"[{m}] {r.gse} | {r.title[:80]} || {ev[len(m)+2:][:200]}")
open("geo/audit2.txt","w").write("\n".join(lines))
```

## Cell 30 · python (python) · ok

Finalising catalogue with grouping and tasks

```python

RULES["longitudinal_treatment"]=RULES["longitudinal_treatment"].replace("|pre-?treatment|post-?treatment","|post-?treatment (samples|biops|tumou?rs?)|(paired|matched) pre-|pre- and post|pre- and on|pre-? and on-?treatment").replace("|acquired resistance","")
RR={m:rx(p) for m,p in RULES.items()}
C=D[elig].copy(); res=C.apply(classify,axis=1)
C["validation_modalities"]=[";".join(x[0]) for x in res]
C["evidence"]=[" || ".join(f"{k}: …{v}…" for k,v in x[1].items()) for x in res]
C=C[C.validation_modalities!=""].copy()
C["cancer_type"]=C.txt_all.map(cancer_types)
C["sample_source"]=C.txt.map(lambda t:"patient tumour + model" if (PATIENT.search(t) and CELLLINE.search(t)) else "cancer cell line/model" if CELLLINE.search(t) else "patient tumour" if PATIENT.search(t) else "unspecified")
C["platform"]=C.gpl.map(lambda g:"; ".join(f"GPL{x}: {GPL.get('GPL'+x,'')}" for x in g.split(";") if x))
C["superseries_of"]=C.relations.str.findall(r"SubSeries of: (GSE\d+)").map(lambda x:";".join(x))
C["n_subseries"]=C.relations.str.count(r"SuperSeries of: GSE")
C["is_superseries"]=C.n_subseries>0
C["study_group"]=C.apply(lambda r:r.superseries_of.split(";")[0] if r.superseries_of else r.gse,axis=1)
C["benchmark_tasks"]=C.validation_modalities.map(tasks)
C["organism"]=C.taxon
C["processed_files"]=C.suppfile
C["geo_url"]="https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc="+C.gse
C["matched_by_geo_query"]=C.query_hits
C["n_modalities"]=C.validation_modalities.str.count(";")+1
cols=["gse","title","year","n_samples","organism","cancer_type","sample_source","platform","validation_modalities","n_modalities","benchmark_tasks",
      "evidence","matched_by_geo_query","is_superseries","n_subseries","superseries_of","study_group","pubmed_ids","processed_files","geo_url"]
OUT=C[cols].sort_values(["n_modalities","year"],ascending=[False,False]).drop_duplicates("gse")
OUT.to_csv("ground_truth_catalogue.csv",index=False)
print(len(OUT), OUT.study_group.nunique())
mc={m:int(OUT.validation_modalities.str.contains(m).sum()) for m in MODS}; print(mc)
mg={m:int(OUT[OUT.validation_modalities.str.contains(m)].study_group.nunique()) for m in MODS}; print(mg)
tc={t:int(OUT.benchmark_tasks.str.contains(t).sum()) for t in TASKS}; print(tc)
ct=OUT.cancer_type.str.split("; ").explode().str.replace(r" \(\+\)","",regex=True).value_counts(); print(ct.head(40).to_string())
print(OUT.n_modalities.value_counts().sort_index().to_dict(), OUT.sample_source.value_counts().to_dict())
```

## Cell 31 · python (python) · FAILED

Writing ground_truth_methods.md

```python

ql=Q["qlog"]
AUDIT={"matched_WES_WGS":"8/8","CITE_seq_ADT":"7/8 (the one miss was TotalSeq hashtags; rule then tightened to exclude hashtag-only TotalSeq)","genotype_multiplexed":"8/8",
"paired_bulk_RNA":"6/8 in round 1 (public TARGET/TCGA bulk); 9/10 after excluding public-bulk mentions",
"paired_spatial":"8/8","mtDNA_lineage":"4/8 in round 1; 10/10 after requiring mtDNA variant + lineage/clone context or a named assay",
"longitudinal_treatment":"6/8 in round 1; 7/10 in round 2; then tightened once more (bare 'pre-treatment' and 'acquired resistance' dropped), and that final rule was not re-audited",
"cell_line_mixture":"7/8 (PDX human-mouse filtering miss; that pattern removed)","perturb_seq":"4/8 in round 1 (non-single-cell CRISPR screens); 10/10 after requiring a single-cell readout"}
md=[]
md.append("# Ground-truth dataset catalogue: methods\n")
md.append(f"Data pull: GEO via NCBI E-utilities (db=gds, entry type GSE) and GEO series SOFT text (acc.cgi, targ=self, view=brief), retrieved 15 October 2026. Output: {host.artifact_marker('PLACEHOLDER') if False else 'ground_truth_catalogue.csv'}.\n")
md.append("## 1. Retrieval queries\n")
md.append("A base query defined human tumour single-cell series. Each validation modality then added one clause. For cell-line mixtures and Perturb-seq, the cancer clause was widened with `K562 OR \"cancer cell line(s)\" OR \"cell lines\"`. All terms were `[All Fields]`, which in GEO also covers sample-level characteristics and protocols.\n")
md.append("| Query | GEO hits |\n|---|---|")
for q in ql: md.append(f"| {q['modality']} | {q['count']} |")
md.append(f"\nUnion of the modality queries: {len(G)} unique records. All were retrieved in full; none was capped (the largest set was 1,172 against retmax=5000).\n")
md.append("<details><summary>Exact query strings</summary>\n")
for q in ql: md.append(f"**{q['modality']}**\n```\n{q['query']}\n```")
md.append("</details>\n")
md.append("## 2. Eligibility filters (applied to esummary plus SOFT text)\n")
md.append("1. `gdstype` contains 'sequencing'. This drops microarray-only series.\n2. Taxon includes *Homo sapiens*.\n3. Single-cell regex matched in title, summary, overall design or sample titles.\n4. Cancer regex matched (cancer terms, haematological malignancy acronyms, K562/HeLa).\n5. At least one modality rule fired (Section 3).\n")
md.append(f"Eligible after filters 1-4: {int(elig.sum())}. In the catalogue (filter 5 also satisfied): {len(OUT)} series in {OUT.study_group.nunique()} study groups. A study group is a SuperSeries together with its SubSeries.\n")
md.append("## 3. Modality rules (regex over title + summary + overall_design + sample titles)\n")
md.append("A modality call means the record states that the study generated that data type. It does **not** prove that the data are deposited in GEO: WES/WGS is often held in dbGaP/EGA under controlled access, and companion data often sit in a sibling SubSeries. Every call stores the matched text window in the `evidence` column so it can be audited.\n")
md.append("| Modality | Regex (case-insensitive) | Exclusions |\n|---|---|---|")
EXC={"paired_bulk_RNA":"single match co-occurring with TCGA/TARGET/GTEx/ICGC/CPTAC/'public' bulk","matched_WES_WGS":"single match in a 'TCGA/public/previously published' context",
     "CITE_seq_ADT":"TotalSeq/hashtag antibodies used only for hashing (counted as genotype_multiplexed instead)"}
for m in MODS: md.append(f"| {m} | `{RULES[m].replace('|',' \\| ')}` | {EXC.get(m,'')} |")
md.append("\n`genotype_multiplexed` covers both genotype-based demultiplexing (demuxlet, souporcell, vireo, freemuxlet) and hashtag/lipid/CMO sample multiplexing. Both give a cell-to-sample label that is independent of the transcriptome.\n")
md.append("## 4. Derived fields\n")
md.append("- **cancer_type**: an ordered dictionary of 37 cancer-type regexes, keeping at most 3 labels. 'pan-cancer/multiple' is assigned when the text says pan-cancer or multiple tumour types; 'unspecified' when nothing matched.")
md.append("- **sample_source**: patient tumour vs cancer cell line/model (cell line, organoid, PDX, xenograft), from keyword rules.")
md.append("- **benchmark_tasks** (mapping from modality to task):")
for t,v in TASKS.items(): md.append(f"  - `{t}` ← {', '.join(v)}")
md.append("- **study_group**: the parent SuperSeries accession (from `!Series_relation = SubSeries of:`), otherwise the series' own accession. Use it to deduplicate at study level.\n")
md.append("## 5. Precision audit\n")
md.append("We hand-checked seeded random samples (8 per modality in round 1; 10 for the four revised modalities in round 2), asking whether the record states that the modality was generated in the study. Rules were tightened after each round.\n")
md.append("| Modality | Audit result |\n|---|---|")
for m in MODS: md.append(f"| {m} | {AUDIT[m]} |")
md.append("\nThese are small-sample spot checks, so the precision figures are **provisional**. Recall was not measured. Because the rules read only series-level text (sample characteristics were not parsed), recall is lower than the GEO index counts in Section 1.\n")
md.append("## 6. Counts\n")
md.append("| Modality | Series | Study groups |\n|---|---|---|")
for m in MODS: md.append(f"| {m} | {mc[m]} | {mg[m]} |")
md.append("\n| Benchmark task | Series |\n|---|---|")
for t in TASKS: md.append(f"| {t} | {tc[t]} |")
md.append("\nModalities per series: "+", ".join(f"{k}: {v}" for k,v in OUT.n_modalities.value_counts().sort_index().items())+".\n")
md.append("Sample source: "+", ".join(f"{k}: {v}" for k,v in OUT.sample_source.value_counts().items())+".\n")
md.append("| Cancer type (multi-label) | Series |\n|---|---|")
for k,v in ct.items(): md.append(f"| {k} | {v} |")
md.append("\nYear range: %d-%d. Median samples per series: %d.\n"%(OUT.year.min(),OUT.year.max(),OUT.n_samples.median()))
md.append("## 7. Deviations and limitations\n")
md.append("- An LLM adjudication pass over series summaries was planned but not run: the per-session LLM token ceiling was reached. Classification is regex-only and audited by hand (Section 5).\n- Sample-level metadata (characteristics, library strategy) was not parsed, only series-level text plus sample titles.\n- Only GEO was searched. ArrayExpress/BioStudies, CELLxGENE and HTAN were not.\n- The mtDNA count (18 series) is much lower than the earlier audit's 79 GEO query hits. That earlier figure counted any mention of mtDNA or mitochondrial DNA; this catalogue requires lineage or clonal context.\n- The counts differ from the gap review's 4 October GEO probes (e.g. WES 158 vs 138 here) because the queries and filters differ.\n")
open("ground_truth_methods.md","w").write("\n".join(md)); print(len(md))
```

## Cell 32 · bash (python) · ok

Checking python version

```bash
echo ok
```

## Cell 33 · python (python) · ok

Writing ground_truth_methods.md (fixed)

```python

ql=Q["qlog"]
AUDIT={"matched_WES_WGS":"8/8","CITE_seq_ADT":"7/8 (the one miss was TotalSeq hashtags; rule then tightened to exclude hashtag-only TotalSeq)","genotype_multiplexed":"8/8",
"paired_bulk_RNA":"6/8 in round 1 (public TARGET/TCGA bulk); 9/10 after excluding public-bulk mentions",
"paired_spatial":"8/8","mtDNA_lineage":"4/8 in round 1; 10/10 after requiring mtDNA variant + lineage/clone context or a named assay",
"longitudinal_treatment":"6/8 in round 1; 7/10 in round 2; then tightened once more (bare 'pre-treatment' and 'acquired resistance' dropped), and that final rule was not re-audited",
"cell_line_mixture":"7/8 (PDX human-mouse filtering miss; that pattern removed)","perturb_seq":"4/8 in round 1 (non-single-cell CRISPR screens); 10/10 after requiring a single-cell readout"}
EXC={"paired_bulk_RNA":"single match co-occurring with TCGA/TARGET/GTEx/ICGC/CPTAC/'public' bulk","matched_WES_WGS":"single match in a 'TCGA/public/previously published' context",
     "CITE_seq_ADT":"TotalSeq/hashtag antibodies used only for hashing (counted as genotype_multiplexed instead)"}
md=["# Ground-truth dataset catalogue: methods\n",
"Data pull: GEO via NCBI E-utilities (db=gds, entry type GSE) and GEO series SOFT text (acc.cgi, targ=self, view=brief), retrieved 15 October 2026. Output: the ground-truth catalogue CSV (ground_truth_catalogue.csv).\n",
"## 1. Retrieval queries\n",
"A base query defined human tumour single-cell series. Each validation modality then added one clause. For cell-line mixtures and Perturb-seq, the cancer clause was widened with `K562 OR \"cancer cell line(s)\" OR \"cell lines\"`. All terms were `[All Fields]`, which in GEO also covers sample-level characteristics and protocols.\n",
"| Query | GEO hits |","|---|---|"]
md+= [f"| {q['modality']} | {q['count']} |" for q in ql]
md.append(f"\nUnion of the modality queries: {len(G)} unique records. All were retrieved in full; none was capped (the largest set was 1,172 against retmax=5000).\n")
md.append("<details><summary>Exact query strings</summary>\n")
for q in ql: md.append(f"**{q['modality']}**\n```\n{q['query']}\n```")
md.append("</details>\n")
md.append("## 2. Eligibility filters (applied to esummary plus SOFT text)\n")
md.append("1. `gdstype` contains 'sequencing'. This drops microarray-only series.\n2. Taxon includes *Homo sapiens*.\n3. Single-cell regex matched in title, summary, overall design or sample titles.\n4. Cancer regex matched (cancer terms, haematological malignancy acronyms, K562/HeLa).\n5. At least one modality rule fired (Section 3).\n")
md.append(f"Single-cell regex: `{SCRX.pattern}`\n\nCancer regex: `{CARX.pattern}`\n")
md.append(f"Eligible after filters 1-4: {int(elig.sum())}. In the catalogue (filter 5 also satisfied): {len(OUT)} series in {OUT.study_group.nunique()} study groups. A study group is a SuperSeries together with its SubSeries.\n")
md.append("## 3. Modality rules (regex over title + summary + overall_design + sample titles)\n")
md.append("A modality call means the record states that the study generated that data type. It does **not** prove that the data are deposited in GEO: WES/WGS is often held in dbGaP/EGA under controlled access, and companion data often sit in a sibling SubSeries. Every call stores the matched text window in the `evidence` column so it can be audited.\n")
md.append("| Modality | Regex (case-insensitive) | Exclusions |"); md.append("|---|---|---|")
for m in MODS:
    pat=RULES[m].replace("|"," \\| ")
    md.append(f"| {m} | `{pat}` | {EXC.get(m,'')} |")
md.append("\n`genotype_multiplexed` covers both genotype-based demultiplexing (demuxlet, souporcell, vireo, freemuxlet) and hashtag/lipid/CMO sample multiplexing. Both give a cell-to-sample label that is independent of the transcriptome.\n")
md.append("## 4. Derived fields\n")
md.append("- **cancer_type**: an ordered dictionary of 37 cancer-type regexes, keeping at most 3 labels. 'pan-cancer/multiple' is assigned when the text says pan-cancer or multiple tumour types; 'unspecified' when nothing matched.")
md.append("- **sample_source**: patient tumour vs cancer cell line/model (cell line, organoid, PDX, xenograft), from keyword rules.")
md.append("- **benchmark_tasks** (mapping from modality to task):")
for t,v in TASKS.items(): md.append(f"  - `{t}` ← {', '.join(v)}")
md.append("- **study_group**: the parent SuperSeries accession (from `!Series_relation = SubSeries of:`), otherwise the series' own accession. Use it to deduplicate at study level.\n")
md.append("## 5. Precision audit\n")
md.append("We hand-checked seeded random samples (8 per modality in round 1; 10 for the four revised modalities in round 2), asking whether the record states that the modality was generated in the study. Rules were tightened after each round.\n")
md.append("| Modality | Audit result |"); md.append("|---|---|")
for m in MODS: md.append(f"| {m} | {AUDIT[m]} |")
md.append("\nThese are small-sample spot checks, so the precision figures are **provisional**. Recall was not measured. Because the rules read only series-level text (sample characteristics were not parsed), recall is lower than the GEO index counts in Section 1.\n")
md.append("## 6. Counts\n"); md.append("| Modality | Series | Study groups |"); md.append("|---|---|---|")
for m in MODS: md.append(f"| {m} | {mc[m]} | {mg[m]} |")
md.append("\n| Benchmark task | Series |"); md.append("|---|---|")
for t in TASKS: md.append(f"| {t} | {tc[t]} |")
md.append("\nModalities per series: "+", ".join(f"{k}: {v}" for k,v in OUT.n_modalities.value_counts().sort_index().items())+".\n")
md.append("Sample source: "+", ".join(f"{k}: {v}" for k,v in OUT.sample_source.value_counts().items())+".\n")
md.append("| Cancer type (multi-label) | Series |"); md.append("|---|---|")
for k,v in ct.items(): md.append(f"| {k} | {v} |")
md.append("\nYear range: %d-%d. Median samples per series: %d.\n"%(OUT.year.min(),OUT.year.max(),OUT.n_samples.median()))
md.append("## 7. Deviations and limitations\n")
md.append("- An LLM adjudication pass over series summaries was planned but not run: the per-session LLM token ceiling was reached. Classification is regex-only and audited by hand (Section 5).\n- Sample-level metadata (characteristics, library strategy) was not parsed, only series-level text plus sample titles.\n- Only GEO was searched. ArrayExpress/BioStudies, CELLxGENE and HTAN were not.\n- The mtDNA count (18 series) is much lower than the earlier audit's 79 GEO query hits. That earlier figure counted any mention of mtDNA or mitochondrial DNA; this catalogue requires lineage or clonal context.\n- The counts differ from the gap review's 4 October GEO probes (e.g. WES 158 vs 138 here) because the queries and filters differ.\n")
open("ground_truth_methods.md","w").write("\n".join(md)); print(len(md), OUT.year.min(), OUT.year.max())
```

## Cell 34 · repl · ok

Submitting structured output

```python
out={
"summary":"Part A: 106 foundational references verified (99 via PubMed esummary, 6 via Crossref, 1 via arXiv), each with a one-sentence claim checked against its PubMed abstract where one exists (63 supported as written, 33 rewritten to match the abstract, 10 without an abstract). They cover benchmarking guidelines, the self-assessment trap, multiverse/specification-curve and many-analyst studies, random-signature nulls, calibration/conformal prediction (incl. 2 single-cell papers), pseudoreplication, metric validity (ARI, silhouette, scIB), simulation realism, ground-truth designs (cell-line mixtures, genotype/hashtag multiplexing, CITE-seq, spike-ins, mtDNA lineage, Perturb-seq), cancer CNV callers and 4 CNV benchmarks, and 10 atlases/resources. Part B: GEO DataSets queries (base human-tumour single-cell GSE = 6,141; union of 9 modality queries = 2,715 records, all retrieved) were filtered to sequencing + human + single-cell + cancer (2,024 eligible). Hand-audited regex rules applied to series SOFT text gave 1,336 validation-bearing series in 1,166 SuperSeries study groups, each with cancer type, platform, modalities, evidence snippet and benchmark tasks. Precision figures from the spot audit are provisional.",
"n_foundation_refs":106,
"n_gt_series":1336,
"gt_counts_by_modality":"series (study groups): paired_bulk_RNA 459 (402); longitudinal_treatment 297 (266); paired_spatial 250 (218); CITE_seq_ADT 227 (216); genotype_multiplexed 166 (152; includes hashtag/CMO multiplexing); matched_WES_WGS 138 (117); perturb_seq 89 (77); cell_line_mixture 25 (20); mtDNA_lineage 18 (9). Tasks: pipeline_robustness 918, deconvolution 698, perturbation_response 381, annotation_calibration 356, CCC_spatial_referee 250, malignant_calling 162, clone_calling 153.",
"artifacts":["2ebbc522-4ea2-4e32-b5ca-8dbb99903467 foundations_refs.csv","fdc5bfe0-163d-4a37-b9bd-fa79b4c5f606 ground_truth_catalogue.csv","a31907fb-bcbf-48bc-9d7f-64e82d368414 ground_truth_methods.md"]}
host.submit_output(out,completion_bullets=["Verified 106 foundational references via PubMed/Crossref/arXiv","Built a 1,336-series GEO ground-truth catalogue with modality evidence","Documented queries, regex rules, audit and counts in methods file"],
 deviations=["LLM adjudication of GEO summaries was not run (the per-frame host.llm 2M-token ceiling was reached). Modality and cancer-type calls are regex-only, spot-audited on 8-10 records per modality; precision figures are provisional and recall was not measured.",
 "GEO sample-level metadata (characteristics, library strategy) was not parsed: only series title, summary, overall design and the first 80 sample titles were used, so counts are lower than raw GEO index hits.",
 "A modality call means the study states it generated the data; actual deposition (e.g. WES in dbGaP/EGA, or companion SubSeries) was not checked. genotype_multiplexed also includes hashtag/CMO multiplexing.",
 "Dropped as unresolvable: CONICS (Müller 2018), Hurlbert 1984, a Lareau mtDNA-artifact paper. Guo 2017 verified via arXiv only (not in PubMed/Crossref). The Nature Genetics 2024 annotation-uncertainty record is an author-less research briefing; the underlying research article was not found.",
 "Only GEO was searched (no ArrayExpress/HTAN/CELLxGENE)."])
```

## Cell 35 · bash (python) · ok

Re-verifying PMID 40595413 via esummary

```bash
grep 40595413 pm_hits2.tsv; curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=40595413&retmode=json" | python -c "import json,sys;r=json.load(sys.stdin)['result']['40595413'];print(r['title'],r['source'],r['pubdate'],r['authors'][0]['name'],[a['value'] for a in r['articleids'] if a['idtype']=='doi'])"; grep luecken2025op foundations_refs.csv | cut -c1-200
```

## Cell 36 · repl · ok

Resubmitting structured output

```python
host.submit_output(out,completion_bullets=["Verified 106 foundational references via PubMed/Crossref/arXiv","Built a 1,336-series GEO ground-truth catalogue with modality evidence","Documented queries, regex rules, audit and counts in methods file"],
 deviations=["LLM adjudication of GEO summaries was not run (the per-frame host.llm 2M-token ceiling was reached). Modality and cancer-type calls are regex-only, spot-audited on 8-10 records per modality; precision figures are provisional and recall was not measured.",
 "GEO sample-level metadata (characteristics, library strategy) was not parsed: only series title, summary, overall design and the first 80 sample titles were used, so counts are lower than raw GEO index hits.",
 "A modality call means the study states it generated the data; actual deposition (e.g. WES in dbGaP/EGA, or companion SubSeries) was not checked. genotype_multiplexed also includes hashtag/CMO multiplexing.",
 "Dropped as unresolvable: CONICS (Müller 2018), Hurlbert 1984, a Lareau mtDNA-artifact paper. Guo 2017 verified via arXiv only (not in PubMed/Crossref). The Nature Genetics 2024 annotation-uncertainty record is an author-less research briefing; the underlying research article was not found.",
 "Only GEO was searched (no ArrayExpress/HTAN/CELLxGENE).",
 "Reviewer finding on PMID 40595413 rebutted: it was returned by the Q2 'openproblems' esearch (logged in pm_hits2.tsv) and re-resolved via esummary with matching title, journal, year and DOI 10.1038/s41587-025-02694-w."])
```
