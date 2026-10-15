# Sub-agent: Statistics (re-verification of 120 quantities, CIs, NB2 coverage models, trend tests)
Verbatim record of every code cell executed in this session, in execution order. Cells are notebook-style: they share one persistent interpreter, so later cells use variables created by earlier ones. Failed cells are kept and marked; the cell that follows usually corrects them.
Tool legend: `python` = persistent Python kernel; `bash` = fresh shell; `repl` = orchestration kernel of the analysis platform (sub-agent dispatch, artifact and memory calls; not needed to reproduce results). Calls to `host.*` (e.g. `host.llm`, `host.artifact_path`) are platform services; `src/` provides public equivalents.
Cells: 21; failed: 0.

## Cell 1 · bash (python) · ok

Unzipping archive and listing files

```bash
mkdir -p arc && cd arc && unzip -o -q "/Users/jubayer/.claude-science/orgs/89d7686f-eb25-4116-8f44-856d205cc44b/artifacts/proj_e32ccc743087/c1980142-77dc-48d1-aeeb-c35fa1fd69f3/vbd928677_artifacts-sc.zip" && find . -type f | head -50 && wc -c $(find . -name "*.md")
```

## Cell 2 · python (python) · ok

Inspecting CSV schemas

```python
import pandas as pd, os
os.chdir('arc') if os.path.exists('arc') else None
for f in ['gap_scores.csv','pubmed_topic_volume.csv','pubmed_topic_volume_long.csv','problem_type_by_topic.csv','limitations_extracted.csv','benchmark_classification.csv','sc_cancer_corpus.csv']:
    d=pd.read_csv(f); print(f,d.shape,list(d.columns)[:20])
```

## Cell 3 · python (python) · ok

Exploring volume, gap scores, limitations

```python
L=pd.read_csv('pubmed_topic_volume_long.csv'); print(L.topic.unique(), L.year.unique())
print(L[~L.topic.isin(pd.read_csv('pubmed_topic_volume.csv').topic)])
G=pd.read_csv('gap_scores.csv'); pd.set_option('display.width',250); print(G[['topic','topic_papers_23_26','true_benchmarks','papers_per_benchmark','rel_share_25_vs_21','methodological_problems','n_problems']])
V=pd.read_csv('pubmed_topic_volume.csv'); print(V[['topic','n2025','n2026_partial','n2026_proj','share_2025','rel_share_25_vs_21']])
Lim=pd.read_csv('limitations_extracted.csv'); print(Lim.problem_type.value_counts(), Lim.about_field.value_counts(dropna=False), Lim['none'].value_counts(dropna=False))
B=pd.read_csv('benchmark_classification.csv'); print(B.is_benchmark.value_counts(), B.head())
```

## Cell 4 · python (python) · ok

Checking denominators and auxiliary files

```python
print(G.methodological_problems.sum(), G.n_problems.sum())
m=Lim[(Lim.problem_type!='none')]; print(len(m), m['none'].value_counts(dropna=False))
for cond,name in [((Lim.problem_type!='none')&(Lim['none']!=True),'notnone&flag'),((Lim.problem_type!='none')&(Lim.about_field==True),'about'),((Lim.problem_type!='none')&(Lim.problem_type!='other'),'noother')]:
    print(name,cond.sum())
P=pd.read_csv('problem_type_by_topic.csv'); print(P.head(3).T)
S=pd.read_csv('project_shortlist.csv'); print(S.columns.tolist()); print(S.iloc[:, :6])
Bx=pd.read_csv('biorxiv_sc_cancer_preprints.csv'); print(Bx.shape, Bx.columns.tolist())
C=pd.read_csv('sc_cancer_corpus.csv'); print(C.is_eval_title.sum(), C.year.value_counts().sort_index().to_dict()); print(B.id.isin(C.pmid).sum())
```

## Cell 5 · python (python) · ok

Checking topic tags, preprint ratios, problem shares

```python
print(C.topics.head(3).tolist()); print(Bx.topics.head(3).tolist(), Bx.date.min(), Bx.date.max())
lab=dict(zip(G.label,G.topic)); P['topic']=P.topics.map(lab); print(P.topic.isna().sum())
cols=[c for c in P.columns if c not in('topics','topic')]
P['rowsum']=P[cols].sum(1); print(P.set_index('topic').rowsum.reindex(G.topic).values - G.methodological_problems.values)
print(P[cols].sum().sum())
```

## Cell 6 · python (python) · ok

Identifying methodological category set

```python
import itertools, numpy as np
Pm=P.set_index('topic').reindex(G.topic)[cols]; tgt=G.methodological_problems.values
diff=Pm.sum(1).values-tgt
for k in range(1,6):
    for comb in itertools.combinations(cols,k):
        if (Pm[list(comb)].sum(1).values==diff).all(): print('excluded',comb)
for den_name,den in [('n_problems',Pm.sum(1)),('meth',pd.Series(tgt,index=Pm.index)),('no_other',Pm.drop(columns='other').sum(1))]:
    sh=Pm.div(den,axis=0)
    top=(Pm.idxmax(1)=='no_ground_truth').sum()
    print(den_name,'top NGT',top, 'metric max excl bench',sh.drop('benchmarking').metric_invalid.max().round(4),'unc max',sh.uncertainty.max().round(4),'param bench',sh.loc['benchmarking','parameter_sensitivity'].round(3),'param>5%',(sh.parameter_sensitivity>0.05).sum())
print(Pm.idxmax(1)[Pm.idxmax(1)!='no_ground_truth'])
```

## Cell 7 · python (python) · ok

Recomputing benchmark counts and preprint ratios

```python
import ast
C['tl']=C.topics.fillna('').str.split('|')
Bj=B.merge(C[['pmid','tl','year']],left_on='id',right_on='pmid')
bt=Bj[Bj.is_benchmark].explode('tl').tl.value_counts()
G['bench_recomp']=G.topic.map(bt).fillna(0).astype(int)
print((G.bench_recomp==G.true_benchmarks).all(), G.true_benchmarks.sum())
ev=Bj.explode('tl').tl.value_counts(); print((G.topic.map(ev).fillna(0)==G.eval_papers_all_years).all())
Bx['tl']=Bx.topics.apply(ast.literal_eval); pc=Bx.explode('tl').tl.value_counts()
W=L.pivot(index='topic',columns='year',values='count')
for name,den in [('25+26p',W[2025]+W[2026]),('0.75*25+26p',0.75*W[2025]+W[2026]),('26p',W[2026]),('24-26',W[2024]+W[2025]+W[2026])]:
    r=(pc/den*100).reindex(['benchmarking','clonal_phylogeny','perturbseq','lineage_barcoding','ith_quantification','spatial_tumor']).round(1)
    print(name, r.tolist())
print(pc.get('benchmarking'), Bx.is_sc.all(), Bx.is_cancer.all())
```

## Cell 8 · python (python) · ok

Inferring preprint ratio denominator

```python
rev={'benchmarking':4.8,'clonal_phylogeny':3.9,'perturbseq':3.9,'lineage_barcoding':3.5,'ith_quantification':3.3,'spatial_tumor':3.2}
for t,v in rev.items(): print(t, pc[t], round(pc[t]/v*100), W.loc[t,[2024,2025,2026]].tolist(), round(V.set_index('topic').n2026_proj[t]))
```

## Cell 9 · python (python) · ok

Checking shortlist datasets and growth claims

```python
print(S[['id','weeks','score','datasets','papers_per_benchmark','topic_papers']].to_string())
tot=W.loc['__SUBFIELD_TOTAL__']; Wt=W.drop('__SUBFIELD_TOTAL__')
rs=(Wt[2025]/tot[2025])/(Wt[2021]/tot[2021]); print((rs.reindex(G.topic).values-G.rel_share_25_vs_21.values).max())
print('growing 26proj>25:',(V.n2026_proj>V.n2025).sum(), 'cagr>0', (V.cagr_21_25>0).sum(), 'n2026p>n2025', (V.n2026_partial>V.n2025).sum())
print(C.tl.apply(len).median(), (C.topics.fillna('')=='').sum())
```

## Cell 10 · python (python) · ok

Building verified_quantities table

```python
import re
rows=[]
def add(q,rev,rec,src,match=None,tol=None,note=''):
    if match is None:
        if isinstance(rev,(int,float)) and isinstance(rec,(int,float,np.floating,np.integer)):
            match = abs(float(rec)-float(rev))<= (tol if tol is not None else 0)
        else: match = str(rev)==str(rec)
    rows.append(dict(quantity=q,value_in_review=rev,recomputed=rec,source_file=src,match=bool(match) if not isinstance(match,str) else match,note=note))
pv='pubmed_topic_volume_long.csv'
add('Subfield PubMed records 2015',443,int(tot[2015]),pv)
add('Subfield PubMed records 2025',7556,int(tot[2025]),pv)
proj=tot[2026]*365/277
add('Subfield projected 2026 (~)',9700,round(proj,1),pv,tol=100,note='2026 partial (7,342, to 4 Oct = day 277) x 365/277; review says "roughly 9,700"')
add('Subfield papers 2023-2026',24226,int(tot[[2023,2024,2025,2026]].sum()),pv)
add('PubMed per-year counts',324,len(L),pv,note='27 series (26 topics + subfield total) x 12 years')
add('Topics with absolute growth (2026 projected > 2025)',26,int((V.n2026_proj>V.n2025).sum()),'pubmed_topic_volume.csv',note=f'all 26 have CAGR21-25>0; only {(V.n2026_partial>V.n2025).sum()}/26 already exceed 2025 with partial 2026')
add('Abstracts in corpus',3627,len(C),'sc_cancer_corpus.csv')
add('Limitation extraction rows',1757,len(Lim),'limitations_extracted.csv')
meth=Lim[(Lim.problem_type!='none')&(Lim['none']!=True)]
add('Methodological open problems',1506,len(meth),'limitations_extracted.csv',note="rows with problem_type!='none' and none!=True")
add('Evaluation-titled papers',486,len(B),'benchmark_classification.csv')
add('Verified benchmarks',158,int(B.is_benchmark.sum()),'benchmark_classification.csv')
add('Verified benchmark share (%)',33,round(100*B.is_benchmark.mean(),1),'benchmark_classification.csv',tol=0.5)
add('bioRxiv sc-cancer preprints',372,len(Bx),'biorxiv_sc_cancer_preprints.csv')
lab_rs={'spatial_tumor':6.2,'drug_response_pred':3.2,'foundation_dl':3.1,'cell_communication':2.3,'clonal_phylogeny':0.44,'ctc_liquid_biopsy':0.46,'ith_quantification':0.67,'lineage_barcoding':0.68,'benchmarking':None}
for t,v in lab_rs.items():
    if v is None: continue
    d=1 if v>1 else 2
    add(f'Share change 2025/2021: {t}',v,round(rs[t],d),pv+' (recomputed from counts)')
add('Spatial tumour papers 2025',970,int(W.loc['spatial_tumor',2025]),pv)
add('Benchmarking papers 2025',87,int(W.loc['benchmarking',2025]),pv)
add('Benchmarking share of subfield 2025 (%)',1.2,round(100*W.loc['benchmarking',2025]/tot[2025],1),pv)
# table
tab={'lineage_barcoding':(260,0,None),'perturbseq':(108,0,None),'longitudinal_therapy':(670,1,670),'drug_response_pred':(3888,6,648),'immunotherapy_resp':(7484,13,576),'metastasis':(5663,12,472),'cell_communication':(2169,5,434),'tme_composition':(9284,22,422),'ctc_liquid_biopsy':(562,8,70),'clonal_phylogeny':(464,7,66),'cnv_scdna':(1041,16,65),'deconvolution':(838,13,64),
     'clinical_prognosis':(13409,37,362),'malignant_calling':(1204,8,150),'epigenome_multiome':(566,3,189)}
tp=Wt[[2023,2024,2025,2026]].sum(1)
for t,(p,b,ppb) in tab.items():
    add(f'Papers 2023-26: {t}',p,int(tp[t]),pv)
    add(f'Verified benchmarks: {t}',b,int(bt.get(t,0)),'benchmark_classification.csv + sc_cancer_corpus.csv topic tags')
    if ppb: add(f'Papers per benchmark: {t}',ppb,int(round(tp[t]/bt[t])),'derived')
add('Topics with zero verified benchmarks',2,int((G.bench_recomp==0).sum()),'derived')
ppb_all=(tp/bt.reindex(tp.index)).replace(np.inf,np.nan)
for grp,rng in [(['cnv_scdna','deconvolution','clonal_phylogeny','ctc_liquid_biopsy'],'64-70'),(['longitudinal_therapy','drug_response_pred','immunotherapy_resp','metastasis','cell_communication','tme_composition'],'400-670')]:
    r=ppb_all[grp].round(); add(f'Papers-per-benchmark range ({",".join(grp)})',rng,f'{int(r.min())}-{int(r.max())}','derived', match=(f'{int(r.min())}-{int(r.max())}'==rng) or 'approx', note='review range "400-670" is rounded; actual min 422' if rng=='400-670' else '')
# problem types
for pt,v in [('no_ground_truth',24.2),('no_benchmark',5.8),('metric_invalid',1.1),('uncertainty',0.7),('parameter_sensitivity',2.3)]:
    k=(meth.problem_type==pt).sum(); add(f'Share of 1,506 problems: {pt} (%)',v,round(100*k/len(meth),1),'limitations_extracted.csv',note=f'{k}/{len(meth)}')
sh=Pm.div(Pm.sum(1),axis=0)
add('Topics where no_ground_truth is top problem',21,int((Pm.idxmax(1)=='no_ground_truth').sum()),'problem_type_by_topic.csv')
add('Topics where causality displaces no_ground_truth',3,int((Pm.idxmax(1)=='causality').sum()),'problem_type_by_topic.csv')
add('Max metric_invalid share outside benchmarking (%)',2.1,round(100*sh.drop('benchmarking').metric_invalid.max(),1),'problem_type_by_topic.csv',note='denominator = all extracted problems per topic (row sum)')
add('Max uncertainty share in any topic (%)',2.6,round(100*sh.uncertainty.max(),1),'problem_type_by_topic.csv')
add('parameter_sensitivity share in benchmarking (%)',13,round(100*sh.loc['benchmarking','parameter_sensitivity'],1),'problem_type_by_topic.csv',tol=0.5)
add('Topics with parameter_sensitivity >5%',1,int((sh.parameter_sensitivity>0.05).sum()),'problem_type_by_topic.csv')
add('Topics with parameter_sensitivity 0-5%',25,int((sh.parameter_sensitivity<=0.05).sum()),'problem_type_by_topic.csv')
add('Topics with uncertainty <3%',26,int((sh.uncertainty<0.03).sum()),'problem_type_by_topic.csv')
add('Cell-communication share change (P4, -fold)',2.3,round(rs['cell_communication'],1),pv)
ntags=C.topics.fillna('').apply(lambda s: len([x for x in s.split('|') if x]))
add('Median topic tags per paper',3,float(ntags.median()),'sc_cancer_corpus.csv',note=f'all 3,627; {int((ntags==0).sum())} untagged papers included as 0; median over tagged = {ntags[ntags>0].median()}')
for t,v in rev.items():
    r=round(pc[t]/(W.loc[t,2025]+W.loc[t,2026])*100,1)
    add(f'Preprints per 100 papers: {t}',v,r,'biorxiv_sc_cancer_preprints.csv + '+pv,match=False,note=f'{pc[t]} preprints; original "equivalent window" denominator not recorded; recomputed with 2025+2026-partial PubMed counts; rank order of the six largely preserved')
Ss=S.set_index('id')
for pid,sc,wk in [('P1',4.85,6),('P6',4.69,7),('P8',4.62,5),('P2',4.59,7),('P3',3.80,9),('P4',3.71,8),('P5',3.04,10),('P7',2.64,12)]:
    add(f'Shortlist score {pid}',sc,round(Ss.loc[pid,'score'],2),'project_shortlist.csv',tol=0.005)
    add(f'Shortlist weeks {pid}',wk,int(Ss.loc[pid,'weeks']),'project_shortlist.csv')
for q,v in [('GEO human tumour scRNA-seq series',818),('GEO tumour spatial series',925),('GEO scATAC/multiome series',444),('GEO sc + matched WES/WGS',158),('GEO CITE-seq',149),('GEO paired spatial+scRNA',145),('GEO paired bulk+sc',437),('GEO mito-lineage',79),('GEO longitudinal',49),('GEO Perturb-seq/CROP-seq',174),('bioRxiv preprints screened',15682),('GEO availability probes',12)]:
    inS=any(str(v) in s for s in S.datasets)
    add(q,v,'not in archive CSVs','project_shortlist.csv (text)' if inS else 'none',match='not_verifiable',note='appears in project_shortlist.datasets text' if inS else 'GEO/bioRxiv probe results not stored in archive')
VQ=pd.DataFrame(rows); VQ.to_csv('../verified_quantities.csv',index=False)
print(VQ.match.astype(str).value_counts()); print(VQ[VQ.match.astype(str)!='True'][['quantity','value_in_review','recomputed']].to_string())
```

## Cell 11 · python (python) · ok

Checking year distribution of eval-titled papers

```python
add('Raw-to-verified evaluation ratio ("three times thinner")',3,round(len(B)/B.is_benchmark.sum(),2),'benchmark_classification.csv',tol=0.1)
VQ=pd.DataFrame(rows); VQ.to_csv('../verified_quantities.csv',index=False)
print(pd.crosstab(Bj.year,Bj.is_benchmark).T)
print(pd.crosstab(C.year,C.is_eval_title).T)
print(C.pubdate.head(3).tolist(), C[['year']].isna().sum())
```

## Cell 12 · python (python) · ok

Computing Wilson and Poisson CI tables

```python
try:
    import statsmodels, statsmodels.api as sm; print(statsmodels.__version__)
except Exception as e: print(e)
from scipy import stats
from statsmodels.stats.proportion import proportion_confint
ci=[]
def wil(name,k,n,group,src):
    lo,hi=proportion_confint(k,n,alpha=0.05,method='wilson'); ci.append(dict(table='proportion',quantity=name,group=group,k=int(k),n=int(n),estimate=k/n,lower95=lo,upper95=hi,method='Wilson score',source_file=src))
wil('verified benchmarks / evaluation-titled',B.is_benchmark.sum(),len(B),'all','benchmark_classification.csv')
for kind,k in B[B.is_benchmark].benchmark_kind.value_counts().items(): wil(f'benchmark_kind={kind} among verified',k,158,'all','benchmark_classification.csv')
for pt,k in meth.problem_type.value_counts().items(): wil(f'problem_type={pt} among methodological problems',k,len(meth),'all','limitations_extracted.csv')
wil('benchmarking topic share of subfield 2025',W.loc['benchmarking',2025],tot[2025],'2025',pv)
for t in Pm.index:
    n=Pm.loc[t].sum()
    for pt in ['no_ground_truth','no_benchmark','metric_invalid','parameter_sensitivity','uncertainty','causality']:
        wil(f'problem_type={pt} share of topic problems',Pm.loc[t,pt],n,t,'problem_type_by_topic.csv')
    g=G.set_index('topic').loc[t]
    if g.eval_papers_all_years>0: wil('verified benchmarks / evaluation-titled papers in topic',g.true_benchmarks,g.eval_papers_all_years,t,'gap_scores.csv')
for t in G.topic:
    k=int(bt.get(t,0)); n=int(tp[t])
    lo=0 if k==0 else stats.chi2.ppf(0.025,2*k)/2; hi=stats.chi2.ppf(0.975,2*k+2)/2
    ci.append(dict(table='poisson_rate',quantity='verified benchmarks per 1,000 topic papers 2023-26',group=t,k=k,n=n,estimate=1000*k/n,lower95=1000*lo/n,upper95=1000*hi/n,method='exact Poisson (Garwood)',source_file='gap_scores.csv',papers_per_benchmark=(n/k if k else np.nan),ppb_lower95=(n/(hi) ),ppb_upper95=(n/lo if k else np.inf)))
CI=pd.DataFrame(ci); CI.to_csv('../ci_tables.csv',index=False)
print(len(CI)); print(CI[CI.table=='poisson_rate'][['group','k','n','estimate','lower95','upper95']].round(2).sort_values('estimate').to_string())
print(CI[(CI.group=='all')][['quantity','k','n','estimate','lower95','upper95']].round(4).to_string())
```

## Cell 13 · bash (python) · ok

Searching plan JSONs for method-topic definition

```bash
cd arc; for f in plan_*.json; do python -c "import json,sys;d=json.load(open('$f'));print(json.dumps(d)[:3000])"; echo; done | grep -o -i '.\{200\}method.\{200\}' | head -10
```

## Cell 14 · python (python) · ok

Fitting NB and Poisson coverage GLMs

```python
import statsmodels.formula.api as smf, warnings
method_topics={'cnv_scdna','clonal_phylogeny','malignant_calling','ith_quantification','deconvolution','lineage_barcoding','perturbseq','benchmarking','integration_batch','qc_artifacts','foundation_dl','cell_communication','spatial_tumor','epigenome_multiome','tcr_bcr_repertoire','ctc_liquid_biopsy'}
ambig={'drug_response_pred':'method','spatial_tumor':'biology','tcr_bcr_repertoire':'biology','ctc_liquid_biopsy':'biology','epigenome_multiome':'biology','cell_communication':'biology'}
rationale={'cnv_scdna':'computational inference task (copy-number calling) / scDNA assay','clonal_phylogeny':'computational inference task (tree/clone reconstruction)','malignant_calling':'computational inference task (cell classification)','ith_quantification':'quantification metric/method','deconvolution':'computational inference task','lineage_barcoding':'measurement technology (barcoding, mtDNA lineage)','perturbseq':'measurement technology (pooled perturbation assay)','benchmarking':'evaluation of methods','integration_batch':'computational preprocessing task','qc_artifacts':'computational preprocessing / QC','foundation_dl':'modelling methodology','cell_communication':'computational inference task (ligand-receptor inference) [ambiguous]','spatial_tumor':'measurement modality [ambiguous]','epigenome_multiome':'measurement modality [ambiguous]','tcr_bcr_repertoire':'measurement modality [ambiguous]','ctc_liquid_biopsy':'measurement/assay context [ambiguous]',
 'tme_composition':'biological question','tcell_exhaustion':'biological question','resistance_persister':'biological question','drug_response_pred':'clinical/application endpoint [ambiguous: computational prediction]','immunotherapy_resp':'clinical/application endpoint','metastasis':'biological question','pancancer_atlas':'descriptive atlas/application','clinical_prognosis':'clinical/application endpoint','plasticity_emt':'biological question','longitudinal_therapy':'clinical study design/application'}
D=G[['topic','label','true_benchmarks','rel_share_25_vs_21']].copy()
D['papers_23_26']=D.topic.map(tp).astype(int)
D['bench_23_26']=D.topic.map(Bj[Bj.is_benchmark&Bj.year.between(2023,2026)].explode('tl').tl.value_counts()).fillna(0).astype(int)
D['method']=D.topic.isin(method_topics).astype(int)
D['method_alt']=[ (1 if ambig[t]=='method' else 0) if t in ambig else m for t,m in zip(D.topic,D.method)]
D['log_share_change']=np.log(D.rel_share_25_vs_21); D['logoff']=np.log(D.papers_23_26)
M=D[['topic','label','method','method_alt']].copy(); M['class']=np.where(M.method==1,'method/measurement','biology/application'); M['class_alt']=np.where(M.method_alt==1,'method/measurement','biology/application'); M['rationale']=M.topic.map(rationale)
M.to_csv('../topic_class_mapping.csv',index=False); print(M['class'].value_counts().to_dict())
res=[]
def fit(name,data,y,mvar='method'):
    f=f'{y} ~ log_share_change + {mvar}'
    nb=smf.negativebinomial(f,data,offset=data.logoff).fit(disp=0,maxiter=500,method='bfgs')
    nb=smf.negativebinomial(f,data,offset=data.logoff).fit(start_params=nb.params,disp=0,maxiter=200,method='newton')
    po=smf.glm(f,data,family=sm.families.Poisson(),offset=data.logoff).fit()
    lr=2*(nb.llf-po.llf); p_lr=0.5*stats.chi2.sf(lr,1)
    alpha=nb.params['alpha']; ci_a=nb.conf_int().loc['alpha']
    for mod,mn in [(nb,'NB2'),(po,'Poisson')]:
        cis=mod.conf_int()
        for term in ['Intercept','log_share_change',mvar]:
            res.append(dict(fit=name,model=mn,outcome=y,term=term,n_topics=len(data),coef=mod.params[term],IRR=np.exp(mod.params[term]),IRR_lower95=np.exp(cis.loc[term,0]),IRR_upper95=np.exp(cis.loc[term,1]),z=mod.tvalues[term],p=mod.pvalues[term],
              alpha=alpha if mn=='NB2' else np.nan,alpha_lower95=ci_a[0] if mn=='NB2' else np.nan,alpha_upper95=ci_a[1] if mn=='NB2' else np.nan,
              loglik=mod.llf,aic=mod.aic,pearson_chi2_over_df=(po.pearson_chi2/po.df_resid if mn=='Poisson' else np.nan),LR_alpha_vs_Poisson=lr,LR_p_boundary=p_lr,converged=(nb.mle_retvals['converged'] if mn=='NB2' else True)))
fits=[('primary',D,'true_benchmarks','method'),('excl_benchmarking',D[D.topic!='benchmarking'],'true_benchmarks','method'),
      ('window_matched_23_26',D,'bench_23_26','method'),('window_matched_excl_benchmarking',D[D.topic!='benchmarking'],'bench_23_26','method'),
      ('alt_classification',D,'true_benchmarks','method_alt'),('alt_classification_excl_benchmarking',D[D.topic!='benchmarking'],'true_benchmarks','method_alt')]
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    for a in fits: fit(*a)
R=pd.DataFrame(res); R.to_csv('../coverage_model.csv',index=False)
print(R[R.term!='Intercept'][['fit','model','term','IRR','IRR_lower95','IRR_upper95','p','alpha','LR_p_boundary','pearson_chi2_over_df','aic','converged']].round(3).to_string())
```

## Cell 15 · python (python) · ok

Fitting temporal benchmark coverage trend

```python
R['IRR_per_doubling_share']=np.where(R.term=='log_share_change',np.exp(R.coef*np.log(2)),np.nan)
R.to_csv('../coverage_model.csv',index=False)
yrs=range(2015,2027)
T=pd.DataFrame({'year':list(yrs)})
T['subfield_papers']=T.year.map(tot).astype(int)
T['eval_titled']=T.year.map(Bj.year.value_counts()).fillna(0).astype(int)
T['verified_benchmarks']=T.year.map(Bj[Bj.is_benchmark].year.value_counts()).fillna(0).astype(int)
k=T.verified_benchmarks.values; n=T.subfield_papers.values
T['bench_per_1000']=1000*k/n
T['bench_per_1000_lower95']=[1000*(0 if x==0 else stats.chi2.ppf(.025,2*x)/2)/m for x,m in zip(k,n)]
T['bench_per_1000_upper95']=[1000*(stats.chi2.ppf(.975,2*x+2)/2)/m for x,m in zip(k,n)]
T['verified_frac_of_eval']=T.verified_benchmarks/T.eval_titled
T['year_c']=T.year-2020; T['logn']=np.log(T.subfield_papers)
tr=[]
po=smf.glm('verified_benchmarks ~ year_c',T,family=sm.families.Poisson(),offset=T.logn).fit()
nb=smf.negativebinomial('verified_benchmarks ~ year_c',T,offset=T.logn).fit(disp=0,maxiter=500)
bi=smf.glm('verified_benchmarks + I(subfield_papers-verified_benchmarks) ~ year_c',T,family=sm.families.Binomial()).fit()
bf=smf.glm('verified_benchmarks + I(eval_titled-verified_benchmarks) ~ year_c',T,family=sm.families.Binomial()).fit()
pe=smf.glm('eval_titled ~ year_c',T,family=sm.families.Poisson(),offset=T.logn).fit()
T2=T[T.year<=2025]
po25=smf.glm('verified_benchmarks ~ year_c',T2,family=sm.families.Poisson(),offset=T2.logn).fit()
for nm,m,eff in [('Poisson GLM: benchmarks ~ year, offset log(subfield papers)',po,'rate ratio per year'),('NB2: benchmarks ~ year, offset log(subfield papers)',nb,'rate ratio per year'),('Binomial GLM: benchmarks of subfield papers ~ year',bi,'odds ratio per year'),('Binomial GLM: verified fraction of evaluation-titled ~ year',bf,'odds ratio per year'),('Poisson GLM: evaluation-titled ~ year, offset log(subfield papers)',pe,'rate ratio per year'),('Poisson GLM 2015-2025 only (exclude partial 2026)',po25,'rate ratio per year')]:
    c=m.conf_int().loc['year_c']
    tr.append(dict(model=nm,effect=eff,estimate=np.exp(m.params['year_c']),lower95=np.exp(c[0]),upper95=np.exp(c[1]),z=m.tvalues['year_c'],p=m.pvalues['year_c'],
     alpha=m.params.get('alpha',np.nan),pearson_chi2_over_df=(m.pearson_chi2/m.df_resid if hasattr(m,'pearson_chi2') else np.nan),n_years=int(m.nobs)))
TR=pd.DataFrame(tr)
# also pooled early vs late
early=T[T.year.between(2015,2020)]; late=T[T.year.between(2023,2026)]
r1=early.verified_benchmarks.sum()/early.subfield_papers.sum(); r2=late.verified_benchmarks.sum()/late.subfield_papers.sum()
from statsmodels.stats.rates import test_poisson_2indep
tt=test_poisson_2indep(late.verified_benchmarks.sum(),late.subfield_papers.sum(),early.verified_benchmarks.sum(),early.subfield_papers.sum(),method='exact-cond')
tr.append(dict(model='Exact conditional rate comparison: 2023-26 vs 2015-20',effect='rate ratio late/early',estimate=r2/r1,lower95=np.nan,upper95=np.nan,z=np.nan,p=tt.pvalue,alpha=np.nan,pearson_chi2_over_df=np.nan,n_years=10))
TR=pd.DataFrame(tr)
out=pd.concat([T.drop(columns=['year_c','logn']).assign(record='per_year'),TR.assign(record='trend_test')],ignore_index=True)
out.to_csv('../coverage_trend.csv',index=False)
print(T[['year','subfield_papers','eval_titled','verified_benchmarks','bench_per_1000','bench_per_1000_lower95','bench_per_1000_upper95']].round(2).to_string())
print(TR.round(4).to_string()); print(1000*r1,1000*r2)
```

## Cell 16 · python (python) · ok

Summarising window-matched counts and tag median

```python
print(D.set_index('topic').loc[list(tab.keys()),['papers_23_26','true_benchmarks','bench_23_26']].T.to_string())
print(VQ[VQ.quantity.str.startswith('Median')].note.values)
print(D.bench_23_26.sum(), Bj[Bj.is_benchmark&Bj.year.between(2023,2026)].shape[0])
```

## Cell 17 · python (python) · ok

Writing methods_statistics.md

```python
def g(fitn,model,term,col='IRR'): return R[(R.fit==fitn)&(R.model==model)&(R.term==term)].iloc[0]
def irr(fitn,term,model='NB2'):
    r=g(fitn,model,term); return f"{r.IRR:.2f} (95% CI {r.IRR_lower95:.2f}–{r.IRR_upper95:.2f}; p={r.p:.3g})"
md=f"""# Statistical methods: verification, intervals and coverage models

Inputs: archive `artifacts-sc.zip` (data pull 4 Oct 2026). All numbers below were computed by code from the archive CSVs; no new PubMed queries were made.

## 1. Re-derivation of quoted quantities (`verified_quantities.csv`)
Every numeric claim in `sc_cancer_genomics_gap_review.md` that can be derived from the archive was recomputed (119 rows: {int((VQ.match.astype(str)=='True').sum())} match, 1 approximate, 6 mismatch, 12 not verifiable from the archive).
- Subfield volume: `pubmed_topic_volume_long.csv`, series `__SUBFIELD_TOTAL__`. 2026 projection = 2026 partial count (7,342 to 4 Oct, day 277) × 365/277 = {proj:.0f}.
- Topic volume 2023–26 = sum of the 2023–2026 per-topic PubMed counts (2026 partial, not projected).
- Share change = (topic_2025/total_2025)/(topic_2021/total_2021), recomputed from counts.
- Verified benchmarks per topic = PMIDs with `is_benchmark==True` in `benchmark_classification.csv`, joined to topic tags in `sc_cancer_corpus.csv` (pipe-separated; tags overlap, so per-topic counts sum to 274 over 158 unique benchmarks).
- Methodological problems: rows of `limitations_extracted.csv` with `problem_type != 'none'` and `none != True` (n = 1,506). Per-topic shares use the row sums of `problem_type_by_topic.csv` (all extracted problems for the topic, including `other`) as denominator; that denominator reproduces the review's 2.1%, 2.6% and 13% figures.

## 2. Intervals (`ci_tables.csv`)
- Proportions: Wilson score 95% intervals (`statsmodels.stats.proportion.proportion_confint(method='wilson')`). Covered: 158/486 verified-benchmark share; benchmark-kind mix; all 17 problem types over 1,506; benchmarking-topic share of the 2025 subfield; per-topic shares of no_ground_truth, no_benchmark, metric_invalid, parameter_sensitivity, uncertainty and causality; per-topic verified/evaluation-titled fraction.
- Rates: exact (Garwood) Poisson 95% intervals for verified benchmarks per 1,000 topic papers 2023–26: lower = χ²(0.025; 2k)/2, upper = χ²(0.975; 2k+2)/2, divided by papers and scaled by 1,000. Papers-per-benchmark intervals are the reciprocals.

## 3. Topic-level coverage model (`coverage_model.csv`, `topic_class_mapping.csv`)
Unit: topic (n = 26). Outcome: verified benchmark count. Offset: log(topic PubMed papers 2023–26). Covariates: log(share change 2025 vs 2021); binary `method` = 1 for method/measurement topics.
**Indicator definition.** `method` = 1 if the topic's object is an analytic/computational task, an evaluation activity, or a measurement technology/assay (16 topics: cnv_scdna, clonal_phylogeny, malignant_calling, ith_quantification, deconvolution, lineage_barcoding, perturbseq, benchmarking, integration_batch, qc_artifacts, foundation_dl, cell_communication, spatial_tumor, epigenome_multiome, tcr_bcr_repertoire, ctc_liquid_biopsy); `method` = 0 if the object is a biological question or clinical/application endpoint (10 topics: tme_composition, tcell_exhaustion, resistance_persister, drug_response_pred, immunotherapy_resp, metastasis, pancancer_atlas, clinical_prognosis, plasticity_emt, longitudinal_therapy). Six ambiguous topics are flagged in the mapping; `method_alt` flips them (drug_response_pred → method; spatial_tumor, tcr_bcr_repertoire, ctc_liquid_biopsy, epigenome_multiome, cell_communication → biology).
**Models.** NB2 (`statsmodels.formula.api.negativebinomial`, ML estimation of α, BFGS then Newton), and Poisson GLM with the same formula and offset. Poisson vs NB compared by likelihood ratio on α with a boundary-corrected p (½·χ²₁), Pearson χ²/df for the Poisson fit, and AIC. Fits: primary; excluding the `benchmarking` topic; window-matched outcome (benchmarks published 2023–26 only, matching the offset window); alternative classification (each with and without `benchmarking`).

**Results (NB2 IRRs).**
- Primary: method {irr('primary','method')}; log share change {irr('primary','log_share_change')}; α = {g('primary','NB2','method').alpha:.2f}. Poisson Pearson χ²/df = {g('primary','Poisson','method').pearson_chi2_over_df:.1f}; LR test for α p < 0.001. The overdispersion is almost entirely the benchmarking topic (164 benchmarks per 1,000 papers).
- Excluding benchmarking: method {irr('excl_benchmarking','method')}; log share change {irr('excl_benchmarking','log_share_change')} (IRR per doubling of share = {g('excl_benchmarking','NB2','log_share_change').IRR_per_doubling_share:.2f}); α = {g('excl_benchmarking','NB2','method').alpha:.3f}, LR p = {g('excl_benchmarking','NB2','method').LR_p_boundary:.3f}; Poisson χ²/df = {g('excl_benchmarking','Poisson','method').pearson_chi2_over_df:.2f} — Poisson and NB give near-identical estimates.
- Window-matched, excl. benchmarking: method {irr('window_matched_excl_benchmarking','method')}; log share change {irr('window_matched_excl_benchmarking','log_share_change')}.
- Alternative classification, excl. benchmarking: method {irr('alt_classification_excl_benchmarking','method_alt')}; log share change {irr('alt_classification_excl_benchmarking','log_share_change')}.
Interpretation: method/measurement topics carry roughly 2–3× the benchmark rate of biology/application topics after adjusting for volume, robust to classification and window. A negative association with share growth (faster-growing topics less benchmarked per paper) is present when benchmarking is excluded with all-year counts, but it is not significant with the window-matched outcome (p = {g('window_matched_excl_benchmarking','NB2','log_share_change').p:.2f}), so it should be reported as suggestive.

## 4. Temporal trend (`coverage_trend.csv`)
Per year 2015–2026: verified benchmarks (publication year from `sc_cancer_corpus.csv` `year`, all 486 PMIDs matched) against subfield PubMed volume. 2014 (2 evaluation-titled papers, 1 benchmark) is excluded because the volume series starts in 2015. 2026 is partial in both numerator and denominator (to 4 Oct), so its ratio is used unprojected.
Tests of year (centred at 2020): Poisson GLM with offset log(subfield papers); NB2 with the same offset; binomial GLM (benchmarks out of subfield papers); Poisson fit restricted to 2015–2025; binomial GLM of verified fraction among evaluation-titled papers; Poisson GLM of evaluation-titled papers; exact conditional comparison of pooled rates 2023–26 vs 2015–20.
Results: benchmarks per 1,000 papers fell by a rate ratio of {TR.estimate[0]:.3f} per year (95% CI {TR.lower95[0]:.3f}–{TR.upper95[0]:.3f}; p = {TR.p[0]:.4f}); NB α ≈ {TR.alpha[1]:.3f} (no overdispersion); 2015–2025 only: {TR.estimate[5]:.3f} ({TR.lower95[5]:.3f}–{TR.upper95[5]:.3f}; p = {TR.p[5]:.3f}). Pooled rate {1000*r1:.2f}/1,000 in 2015–20 vs {1000*r2:.2f}/1,000 in 2023–26 (ratio {r2/r1:.2f}; exact conditional p = {TR.p[6]:.4f}). The verified fraction among evaluation-titled papers shows no trend (OR/year {TR.estimate[3]:.3f}, p = {TR.p[3]:.2f}), so the decline is in evaluation-titled output relative to volume, not in classification yield.

## 5. Caveats
- Topics overlap (median 3 tags per paper), so the 26 topic observations are not independent; model SEs are optimistic.
- Benchmark numerators come from an LLM-assisted classification of a title-keyword query (`benchmark|comparison|evaluation|assessment`); benchmarks without these title words are missed, uniformly across years only if title conventions are stable.
- Denominators are independent PubMed topic queries; numerators rest on keyword topic tagging of the corpus.
- The review's papers-per-benchmark table divides all-year (2014–2026) benchmark counts by 2023–26 papers; window-matched counts are given in the model input and reduce several topic counts (e.g. ctc_liquid_biopsy 8 → 3; clinical_prognosis 37 → 23).
"""
open('../methods_statistics.md','w').write(md)
D.to_csv('../coverage_model_input.csv',index=False)
print(md[2500:4200])
```

## Cell 18 · repl · ok

Submitting structured output

```python
out={
"summary":"Restored the 4 Oct 2026 archive and recomputed 119 quantities quoted in sc_cancer_genomics_gap_review.md: 100 match exactly, 1 is approximate, 6 do not match and 12 cannot be checked from the archive. Computed Wilson CIs for 207 proportions and exact Poisson CIs for benchmark rates in all 26 topics. Fitted NB2 and Poisson GLMs of verified benchmarks per topic: the primary fit, a fit excluding the benchmarking topic, a fit with the benchmark count restricted to 2023-26, and a fit with an alternative topic classification. Tested the yearly trend in benchmarks per 1,000 subfield papers for 2015-2026.",
"key_results":"Verified: 443 (2015), 7,556 (2025), 2026 projection 9,675 (7,342 x 365/277; the review's ~9,700), 24,226 papers 2023-26; all 8 quoted share changes; 158/486 = 32.5% (Wilson 28.5-36.8%); every row of the papers-per-benchmark table. Problem types out of 1,506: no_ground_truth 364 (24.2%, CI 22.1-26.4), no_benchmark 5.8% (4.7-7.1), parameter_sensitivity 2.3% (1.6-3.1), metric_invalid 1.1% (0.7-1.7), uncertainty 0.7% (0.4-1.2). no_ground_truth is the top problem in 21/26 topics. Exact Poisson rates per 1,000 papers: lineage_barcoding 0 (0-14.2), perturbseq 0 (0-34.2), longitudinal 1.49 (0.04-8.3), drug_response 1.54 (0.57-3.36), immunotherapy 1.74 (0.92-2.97), CNV 15.4 (8.8-25.0), deconvolution 15.5 (8.3-26.5), benchmarking 164 (120-219). NB2 primary (n=26): method/measurement IRR 4.87 (2.13-11.13, p=1.7e-4); log share-change IRR 0.56 (0.24-1.29, p=0.17); alpha 0.86; Poisson Pearson chi2/df 29.2; LR test for alpha p<0.001. Excluding benchmarking (n=25): method IRR 2.44 (1.72-3.47, p=5.6e-7); log share-change IRR 0.64 (0.48-0.86, p=0.003), 0.73 per doubling of share; alpha 0.061, LR p=0.072, so Poisson is adequate (chi2/df 1.86, same estimates). With the benchmark count restricted to 2023-26 and benchmarking excluded: method IRR 2.81 (1.87-4.22); share-change IRR 0.78 (0.56-1.08, p=0.13, not significant). Alternative classification, benchmarking excluded: method IRR 1.89 (1.18-3.03). Trend 2015-2026: benchmarks per 1,000 subfield papers fall by RR 0.924/yr (0.877-0.975, p=0.0036); NB alpha about 0.01; binomial OR 0.924; 2015-2025 only RR 0.930 (p=0.020). Pooled rate 6.77/1,000 in 2015-20 vs 3.92/1,000 in 2023-26 (ratio 0.58, exact conditional p=0.0089). The verified share of evaluation-titled papers has no trend (OR 0.976/yr, p=0.46).",
"discrepancies":[
"Preprints-per-100-papers ratios (benchmarking 4.8, clonal 3.9, perturbseq 3.9, lineage 3.5, ITH 3.3, spatial 3.2) cannot be reproduced. The 'equivalent window' denominator is not recorded. Using 2025 + partial-2026 PubMed counts gives 5.2, 4.2, 4.1, 3.8, 3.2, 3.7.",
"'400-670 papers per benchmark at the open end' is rounded: the actual range across the six open-end topics is 422-670.",
"The review's papers-per-benchmark table divides benchmarks from all years (2014-2026) by 2023-26 papers. Counting only 2023-26 benchmarks lowers several numerators: ctc_liquid_biopsy 8->3 (ratio ~187 rather than 70), clinical_prognosis 37->23 (~583 rather than 362), tme_composition 22->16, CNV 16->12, deconvolution 13->10, longitudinal 1->0. Calling CTC/MRD 'well benchmarked' depends on including older benchmarks.",
"no_ground_truth has 365 rows in the raw extraction but 364 in the 1,506-row methodological set (one row is flagged none=True). The 24.2% share is unaffected.",
"Per-topic verified benchmark counts sum to 274 because topic tags overlap; there are 158 unique benchmarks.",
"12 numbers cannot be checked from the archive because the GEO/bioRxiv probe results were not stored: GEO series counts (818, 925, 444, 158, 149, 145, 437, 79, 49, 174), 15,682 bioRxiv screened, 12 GEO probes. Some appear only as text in project_shortlist.datasets.",
"Median of 3 topic tags includes 96 untagged corpus papers; the median over tagged papers is also 3."],
"artifacts":["verified_quantities.csv (2c3a7911-7fcc-4008-bba8-df4c9ee81984)","ci_tables.csv (06e2bca7-4614-451f-8e9e-bff47eb22534)","coverage_model.csv (45bc47f7-3380-4b37-95c6-6ea3347aec8f)","coverage_model_input.csv (a1de4047-b68e-4549-b9b4-0193e8e3258b)","topic_class_mapping.csv (6d198360-0af6-4908-8434-17f3532445c7)","coverage_trend.csv (f11cb083-0039-4a30-a419-fcb106aef156)","methods_statistics.md (4aa4caf8-98ac-4969-adc5-1fd6e9d94b32)"]}
r=host.submit_output(out,completion_bullets=["Re-derived 119 review quantities against archive CSVs","Computed Wilson and exact Poisson CI tables","Fitted NB2/Poisson topic coverage GLMs with sensitivity fits","Tested yearly benchmark-coverage trend 2015-2026"],
 deviations=["Temporal trend excludes 2014 (2 evaluation-titled papers, 1 benchmark) because the subfield volume series starts in 2015; 2026 is partial to 4 Oct in both numerator and denominator.","Publication years come from the corpus 'year' field (all 486 PMIDs matched); not re-checked against PubMed esummary.","The method-vs-biology indicator is my own classification (6 of 26 topics are ambiguous); an alternative mapping was fitted as a sensitivity check.","12 GEO/bioRxiv-probe numbers could not be verified because the raw probe results are not in the archive."])
print(r)
```

## Cell 19 · python (python) · ok

Checking final verified_quantities counts

```python
v=pd.read_csv('../verified_quantities.csv'); print(len(v), v.match.astype(str).value_counts().to_dict())
s=open('../methods_statistics.md').read(); print(s[s.find('(119'):s.find('(119')+120])
```

## Cell 20 · python (python) · ok

Correcting row count in methods file

```python
open('../methods_statistics.md','w').write(s.replace('(119 rows:','(120 rows:'))
```

## Cell 21 · repl · ok

Resubmitting output with corrected counts

```python
out['summary']=out['summary'].replace('recomputed 119 quantities','recomputed 120 quantities').replace('100 match exactly','101 match exactly')
out['artifacts'][-1]='methods_statistics.md (ed3a64c5-658f-4a43-90f5-d88b87ba51af)'
r=host.submit_output(out,completion_bullets=["Re-derived 120 review quantities against archive CSVs","Computed Wilson and exact Poisson CI tables","Fitted NB2/Poisson topic coverage GLMs with sensitivity fits","Tested yearly benchmark-coverage trend 2015-2026"],
 deviations=["Temporal trend excludes 2014 (2 evaluation-titled papers, 1 benchmark) because the subfield volume series starts in 2015; 2026 is partial to 4 Oct in both numerator and denominator.","Publication years come from the corpus 'year' field (all 486 PMIDs matched); not re-checked against PubMed esummary.","The method-vs-biology indicator is my own classification (6 of 26 topics are ambiguous); an alternative mapping was fitted as a sensitivity check.","12 GEO/bioRxiv-probe numbers could not be verified because the raw probe results are not in the archive."])
print(r['status'], out['summary'][:120])
```
