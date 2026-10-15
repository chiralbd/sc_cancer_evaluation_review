# Sub-agent: Validation (second-pass benchmark classification, problem-type re-coding, kappa)
Verbatim record of every code cell executed in this session, in execution order. Cells are notebook-style: they share one persistent interpreter, so later cells use variables created by earlier ones. Failed cells are kept and marked; the cell that follows usually corrects them.
Tool legend: `python` = persistent Python kernel; `bash` = fresh shell; `repl` = orchestration kernel of the analysis platform (sub-agent dispatch, artifact and memory calls; not needed to reproduce results). Calls to `host.*` (e.g. `host.llm`, `host.artifact_path`) are platform services; `src/` provides public equivalents.
Cells: 26; failed: 2.

## Cell 1 · bash (python) · ok

Unzipping prior analysis artifact

```bash
mkdir -p prior && cd prior && unzip -o -q "/Users/jubayer/.claude-science/orgs/89d7686f-eb25-4116-8f44-856d205cc44b/artifacts/proj_e32ccc743087/c1980142-77dc-48d1-aeeb-c35fa1fd69f3/vbd928677_artifacts-sc.zip" && find . -type f | head -30 && python -c "
import pandas as pd,glob
b=pd.read_csv(glob.glob('**/benchmark_classification.csv',recursive=True)[0]);print(b.columns.tolist(),len(b));print(b.is_benchmark.value_counts())
l=pd.read_csv(glob.glob('**/limitations_extracted.csv',recursive=True)[0]);print(l.columns.tolist(),len(l),l.id.nunique());print(l.problem_type.value_counts())
c=pd.read_csv(glob.glob('**/sc_cancer_corpus.csv',recursive=True)[0]);print(c.columns.tolist());print(b.columns)
"
```

## Cell 2 · bash (python) · ok

Inspecting limitations file and review methods

```bash
cd prior && python -c "
import pandas as pd
l=pd.read_csv('limitations_extracted.csv');print(l.head(8).to_string());print(l.about_field.value_counts(dropna=False));print(l['none'].value_counts(dropna=False))
print(l.id.astype(str).str[:12].head())
b=pd.read_csv('benchmark_classification.csv');print(b.head().to_string());print(b.benchmark_kind.value_counts())
c=pd.read_csv('sc_cancer_corpus.csv');print(b.id.isin(c.pmid).sum(), c.abstract.isna().sum())
"; grep -n -i -E "1,506|limitation|benchmark.*classif|LLM|model|ground truth" sc_cancer_genomics_gap_review.md | head -40
```

## Cell 3 · python (python) · ok

Inspecting host.llm API

```python
help(host.llm)
```

## Cell 4 · python (python) · ok

Loading data, checking abstract coverage and models

```python

import pandas as pd, numpy as np, json
P='prior/'
b=pd.read_csv(P+'benchmark_classification.csv'); l=pd.read_csv(P+'limitations_extracted.csv'); c=pd.read_csv(P+'sc_cancer_corpus.csv')
c['pmid']=c.pmid.astype(str); b['id']=b.id.astype(str); l['id']=l.id.astype(str)
print(l.id.isin(c.pmid).mean(), b.id.isin(c.pmid).mean(), (c.abstract.fillna('').str.len()<100).sum())
m=l[(l.problem_type!='none')]
print(len(m), (m.about_field==True).sum(), len(l[l['none']==False]), len(m[m['none']!=True]))
print(365/1506)
print(host.list_models())
```

## Cell 5 · python (python) · ok

Running second-pass benchmark classification on 486 abstracts

```python

abs_=c.drop_duplicates('pmid').set_index('pmid')
SYS_B=("You screen biomedical abstracts for a meta-research study. Decide whether the paper is a BENCHMARK. "
"Definition: a benchmark is a study whose stated purpose includes a systematic, head-to-head comparison of at least two "
"named computational tools, algorithms, pipelines, or experimental platforms/protocols applied to a shared task "
"(same data or same samples), with performance assessed on common criteria. "
"Count as benchmark: dedicated tool/method comparisons; platform or protocol comparisons on matched samples; "
"new-method papers ONLY if they report a systematic comparison against >=2 named existing tools on shared data. "
"NOT a benchmark: reviews/perspectives without new comparative analysis; biological or clinical 'evaluation' of a gene, "
"drug, cell population, model system or patient cohort; single-tool validation; comparisons of biological conditions, tissues or species.")
tool_b={"name":"record","input_schema":{"type":"object","properties":{
 "is_benchmark":{"type":"boolean"},
 "n_named_entities_compared":{"type":"integer","description":"number of named tools/platforms compared head-to-head (0 if none)"},
 "comparison_type":{"type":"string","enum":["computational_methods","experimental_platforms","new_method_vs_baselines","none"]},
 "rationale":{"type":"string","description":"<=25 words"}},"required":["is_benchmark","n_named_entities_compared","comparison_type","rationale"]}}
def reqB(pid):
    r=abs_.loc[pid]
    return {"prompt":f"TITLE: {r.title}\n\nABSTRACT: {r.abstract}\n\nClassify using the record tool.","system":SYS_B,
            "tools":[tool_b],"tool_choice":{"type":"tool","name":"record"},"max_tokens":400,"temperature":0}
ids=b.id.tolist()
res=host.llm([reqB(p) for p in ids],max_concurrency=16)
errs=[i for i,r in enumerate(res) if 'error' in r or not r.get('tool_use')]
print(len(errs), res[0]['model'])
```

## Cell 6 · python (python) · ok

Inspecting failed LLM requests

```python
print([res[i].get('error', res[i].get('stop_reason'))[:200] for i in errs[:3]])
```

## Cell 7 · python (python) · ok

Checking token usage per request

```python
ok=[r for r in res if 'usage' in r]; print(ok[0]['usage']); print(sum(r['usage'].get('input_tokens',0)+r['usage'].get('output_tokens',0) for r in ok))
```

## Cell 8 · python (python) · ok

Testing whether LLM ceiling still blocks

```python

try: print(host.llm("Say ok",max_tokens=5))
except Exception as e: print(repr(e)[:300])
```

## Cell 9 · python (python) · ok

Saving Haiku results and drawing 200-PMID subsample

```python

rows=[]
for p,r in zip(ids,res):
    if r.get('tool_use'):
        d=r['tool_use']['input']; rows.append(dict(id=p,sp_is_benchmark=bool(d['is_benchmark']),sp_n_compared=d.get('n_named_entities_compared'),sp_comparison_type=d.get('comparison_type'),sp_rationale=d.get('rationale'),rater='claude-haiku-4-5 (host.llm utility tier)'))
    else: rows.append(dict(id=p,rater='PENDING'))
sp=pd.DataFrame(rows); sp.to_csv('bench_haiku_raw.csv',index=False)
pend=sp[sp.rater=='PENDING'].id.tolist(); print(len(pend), [ids.index(x) for x in pend][:5])
rng=np.random.default_rng(1)
sub=sorted(rng.choice(l.id.unique(),200,replace=False).tolist())
pd.Series(sub,name='id').to_csv('pt_subsample_ids.csv',index=False)
print(len(set(sub)&set(l.id.head(8))))
```

## Cell 10 · python (python) · ok

Writing pending abstracts to text files

```python

def dump(pids,fn):
    with open(fn,'w') as f:
        for i,p in enumerate(pids):
            r=abs_.loc[p]; f.write(f"[{i}] {p} | {r.title}\n{r.abstract}\n\n")
dump(pend,'pend_bench.txt'); dump(sub,'pt_sub.txt')
import os; print(os.path.getsize('pend_bench.txt'), os.path.getsize('pt_sub.txt'))
```

## Cell 11 · python (python) · ok

Writing condensed abstract files for manual rating

```python

def dumpc(pids,fn,head,tail):
    with open(fn,'w') as f:
        for i,p in enumerate(pids):
            r=abs_.loc[p]; a=r.abstract
            t=a if len(a)<=head+tail+50 else a[:head]+' … '+a[-tail:]
            f.write(f"[{i}] {r.title}\n{t}\n")
dumpc(pend,'pend_bench_c.txt',650,300); dumpc(sub,'pt_sub_c.txt',750,300)
print(os.path.getsize('pend_bench_c.txt'), os.path.getsize('pt_sub_c.txt'))
```

## Cell 12 · bash (python) · ok

Counting lines in subsample file

```bash
wc -l pt_sub_c.txt; grep -n "^\[50\]\|^\[100\]\|^\[150\]" pt_sub_c.txt
```

## Cell 13 · python (python) · ok

Recording manual problem-type labels 0-49

```python

pt_lab={}
s="""resolution_limit,resolution_limit,technical_artifact,data_access,generalization,clinical_translation,causality,clinical_translation,clinical_translation,reproducibility,
technical_artifact,interpretability,clinical_translation,other,causality,none,causality,other,interpretability,causality,
none,causality,causality,other,causality,causality,causality,interpretability,other,interpretability,
causality,causality,causality,no_benchmark,resolution_limit,none,other,causality,cost_scalability,causality,
causality,causality,causality,causality,other,interpretability,no_benchmark,causality,resolution_limit,causality"""
labs=[x.strip() for x in s.replace('\n','').split(',')]
assert len(labs)==50
for i,x in enumerate(labs): pt_lab[i]=x
import json; json.dump(pt_lab,open('pt_manual_labels.json','w'))
```

## Cell 14 · python (python) · ok

Recording manual problem-type labels 50-99

```python

s="""causality,clinical_translation,causality,causality,causality,causality,causality,causality,causality,interpretability,
interpretability,causality,clinical_translation,causality,interpretability,causality,clinical_translation,causality,interpretability,causality,
causality,interpretability,causality,cost_scalability,none,other,technical_artifact,resolution_limit,other,causality,
reproducibility,causality,no_benchmark,none,causality,causality,causality,other,causality,causality,
none,resolution_limit,interpretability,interpretability,causality,other,technical_artifact,other,interpretability,interpretability"""
labs=[x.strip() for x in s.replace('\n','').split(',')]; assert len(labs)==50
for i,x in enumerate(labs): pt_lab[50+i]=x
json.dump(pt_lab,open('pt_manual_labels.json','w')); print(len(pt_lab))
```

## Cell 15 · python (python) · ok

Recording manual problem-type labels 100-149

```python

s="""clinical_translation,causality,causality,clinical_translation,interpretability,causality,clinical_translation,resolution_limit,other,causality,
causality,causality,no_benchmark,causality,generalization,causality,interpretability,confounding,causality,causality,
causality,none,other,causality,clinical_translation,causality,reproducibility,clinical_translation,causality,causality,
clinical_translation,clinical_translation,other,causality,interpretability,causality,other,causality,causality,causality,
causality,clinical_translation,no_ground_truth,causality,causality,other,causality,causality,causality,none"""
labs=[x.strip() for x in s.replace('\n','').split(',')]; assert len(labs)==50
for i,x in enumerate(labs): pt_lab[100+i]=x
json.dump(pt_lab,open('pt_manual_labels.json','w')); print(len(pt_lab))
```

## Cell 16 · python (python) · ok

Recording labels 150-199 and saving all manual labels

```python

s="""interpretability,causality,causality,clinical_translation,causality,clinical_translation,clinical_translation,causality,causality,causality,
causality,causality,resolution_limit,interpretability,causality,none,causality,cost_scalability,causality,resolution_limit,
interpretability,causality,interpretability,causality,none,causality,clinical_translation,causality,causality,other,
clinical_translation,other,causality,interpretability,causality,clinical_translation,causality,resolution_limit,causality,clinical_translation,
interpretability,causality,causality,causality,causality,causality,none,resolution_limit,causality,causality"""
labs=[x.strip() for x in s.replace('\n','').split(',')]; assert len(labs)==50
for i,x in enumerate(labs): pt_lab[150+i]=x
json.dump(pt_lab,open('pt_manual_labels.json','w'))
vocab=set(l.problem_type.unique()); print(len(pt_lab), set(pt_lab.values())-vocab)
bench_manual_true={9,10,19,26,29,35,75}
```

## Cell 17 · python (python) · FAILED

Computing kappa, confusion matrices, bootstrap CIs

```python

from sklearn.metrics import cohen_kappa_score as ck
rng=np.random.default_rng(1)
def kap(a,b):
    a=np.asarray(a);b=np.asarray(b)
    if len(set(a)|set(b))<2: return np.nan
    return ck(a,b)
def boot(a,b,B=2000):
    a=np.asarray(a);b=np.asarray(b);n=len(a);ks=[]
    for _ in range(B):
        i=rng.integers(0,n,n); k=kap(a[i],b[i])
        if not np.isnan(k): ks.append(k)
    return np.percentile(ks,[2.5,97.5]) if ks else (np.nan,np.nan)
# benchmark
sp=pd.read_csv('bench_haiku_raw.csv',dtype={'id':str})
for j,p in enumerate(pend):
    m=sp.id==p
    sp.loc[m,'sp_is_benchmark']=j in bench_manual_true; sp.loc[m,'rater']='session model (manual reading, condensed abstract)'
    sp.loc[m,'sp_rationale']='manual rating; see validation_methods.md'
bb=b.merge(sp,on='id'); bb['first_pass']=bb.is_benchmark.astype(bool); bb['second_pass']=bb.sp_is_benchmark.astype(bool)
bb['consensus']=bb.first_pass&bb.second_pass
rows=[]
def addrow(level,cat,a,b_,subset):
    a=np.asarray(a).astype(int);b_=np.asarray(b_).astype(int)
    lo,hi=boot(a,b_)
    rows.append(dict(analysis=level,category=cat,subset=subset,n=len(a),first_pos=int(a.sum()),second_pos=int(b_.sum()),
      both_pos=int(((a==1)&(b_==1)).sum()),first_only=int(((a==1)&(b_==0)).sum()),second_only=int(((a==0)&(b_==1)).sum()),
      both_neg=int(((a==0)&(b_==0)).sum()),pct_agreement=round(100*(a==b_).mean(),1),kappa=round(kap(a,b_),3),
      kappa_ci_lo=round(lo,3),kappa_ci_hi=round(hi,3)))
hk=bb.rater.str.startswith('claude-haiku')
addrow('benchmark','is_benchmark',bb.first_pass,bb.second_pass,'all 486 (mixed second raters)')
addrow('benchmark','is_benchmark',bb[hk].first_pass,bb[hk].second_pass,'394 rated by Haiku-4.5 (prompted)')
addrow('benchmark','is_benchmark',bb[~hk].first_pass,bb[~hk].second_pass,'92 rated manually by session model')
print(pd.DataFrame(rows).to_string())
print(bb[hk].first_pass.mean(), bb[~hk].first_pass.mean())
```

## Cell 18 · python (python) · ok

Computing kappa, confusion matrices, bootstrap CIs

```python

def ck(a,b):
    a=np.asarray(a);b=np.asarray(b); cats=np.union1d(a,b)
    po=(a==b).mean(); pe=sum((a==c).mean()*(b==c).mean() for c in cats)
    return (po-pe)/(1-pe) if pe<1 else np.nan
exec(compile(open('/dev/null').read(),'x','exec'))
rng=np.random.default_rng(1)
def kap(a,b):
    a=np.asarray(a);b=np.asarray(b)
    if len(set(a)|set(b))<2: return np.nan
    return ck(a,b)
def boot(a,b,B=2000):
    a=np.asarray(a);b=np.asarray(b);n=len(a);ks=[]
    for _ in range(B):
        i=rng.integers(0,n,n); k=kap(a[i],b[i])
        if not np.isnan(k): ks.append(k)
    return np.percentile(ks,[2.5,97.5]) if ks else (np.nan,np.nan)
sp=pd.read_csv('bench_haiku_raw.csv',dtype={'id':str})
for j,p in enumerate(pend):
    m=sp.id==p
    sp.loc[m,'sp_is_benchmark']=j in bench_manual_true; sp.loc[m,'rater']='session model (manual reading, condensed abstract)'
    sp.loc[m,'sp_rationale']='manual rating; see validation_methods.md'
bb=b.merge(sp,on='id'); bb['first_pass']=bb.is_benchmark.astype(bool); bb['second_pass']=bb.sp_is_benchmark.astype(bool)
bb['consensus']=bb.first_pass&bb.second_pass
rows=[]
def addrow(level,cat,a,b_,subset):
    a=np.asarray(a).astype(int);b_=np.asarray(b_).astype(int)
    lo,hi=boot(a,b_)
    rows.append(dict(analysis=level,category=cat,subset=subset,n=len(a),first_pos=int(a.sum()),second_pos=int(b_.sum()),
      both_pos=int(((a==1)&(b_==1)).sum()),first_only=int(((a==1)&(b_==0)).sum()),second_only=int(((a==0)&(b_==1)).sum()),
      both_neg=int(((a==0)&(b_==0)).sum()),pct_agreement=round(100*(a==b_).mean(),1),kappa=round(kap(a,b_),3),
      kappa_ci_lo=round(lo,3),kappa_ci_hi=round(hi,3)))
hk=bb.rater.str.startswith('claude-haiku')
addrow('benchmark','is_benchmark',bb.first_pass,bb.second_pass,'all 486 (mixed second raters)')
addrow('benchmark','is_benchmark',bb[hk].first_pass,bb[hk].second_pass,'394 rated by Haiku-4.5 (prompted)')
addrow('benchmark','is_benchmark',bb[~hk].first_pass,bb[~hk].second_pass,'92 rated manually by session model')
print(pd.DataFrame(rows).to_string())
print(bb[hk].first_pass.mean(), bb[~hk].first_pass.mean(), bb.consensus.sum())
```

## Cell 19 · python (python) · ok

Inspecting disagreements by first-pass benchmark kind

```python

d=bb[bb.first_pass!=bb.second_pass]
print(pd.crosstab(d.benchmark_kind,[d.first_pass,d.rater.str[:7]]))
print(d[~hk.loc[d.index]][['id','benchmark_kind','what_is_compared']].to_string()[:2500])
```

## Cell 20 · python (python) · FAILED

Computing problem-type agreement on 200 subsample

```python

sub_df=pd.DataFrame({'id':sub,'second_pass':[pt_lab[i] for i in range(200)]})
sub_df=sub_df.merge(l[['id','problem_type','none']].rename(columns={'problem_type':'first_pass'}),on='id')
assert len(sub_df)==200
cats=sorted(vocab)
for c in cats:
    addrow('problem_type',c,sub_df.first_pass==c,sub_df.second_pass==c,'200 random PMIDs (seed 1)')
# pooled paper x category presence/absence
A=np.concatenate([(sub_df.first_pass==c).values for c in cats]);Bv=np.concatenate([(sub_df.second_pass==c).values for c in cats])
addrow('problem_type','OVERALL_pooled_paper_x_category',A,Bv,'200 x 18 cells')
# multiclass
mk=kap(sub_df.first_pass,sub_df.second_pass); lo,hi=boot(sub_df.first_pass.values,sub_df.second_pass.values)
rows.append(dict(analysis='problem_type',category='OVERALL_multiclass_primary_label',subset='200 random PMIDs (seed 1)',n=200,
   pct_agreement=round(100*(sub_df.first_pass==sub_df.second_pass).mean(),1),kappa=round(mk,3),kappa_ci_lo=round(lo,3),kappa_ci_hi=round(hi,3)))
va=pd.DataFrame(rows)
print(va[va.analysis=='problem_type'][['category','first_pos','second_pos','both_pos','pct_agreement','kappa','kappa_ci_lo','kappa_ci_hi']].to_string())
```

## Cell 21 · python (python) · ok

Computing problem-type agreement on 200 subsample

```python

print(l.problem_type.isna().sum(), sub_df.first_pass.isna().sum())
sub_df['first_pass']=sub_df.first_pass.fillna('none')
cats=sorted(x for x in vocab if isinstance(x,str))
for c in cats:
    addrow('problem_type',c,sub_df.first_pass==c,sub_df.second_pass==c,'200 random PMIDs (seed 1)')
A=np.concatenate([(sub_df.first_pass==c).values for c in cats]);Bv=np.concatenate([(sub_df.second_pass==c).values for c in cats])
addrow('problem_type','OVERALL_pooled_paper_x_category',A,Bv,f'200 x {len(cats)} cells')
mk=kap(sub_df.first_pass,sub_df.second_pass); lo,hi=boot(sub_df.first_pass.values,sub_df.second_pass.values)
rows.append(dict(analysis='problem_type',category='OVERALL_multiclass_primary_label',subset='200 random PMIDs (seed 1)',n=200,
   pct_agreement=round(100*(sub_df.first_pass==sub_df.second_pass).mean(),1),kappa=round(mk,3),kappa_ci_lo=round(lo,3),kappa_ci_hi=round(hi,3)))
va=pd.DataFrame(rows)
print(va[va.analysis=='problem_type'][['category','first_pos','second_pos','both_pos','pct_agreement','kappa','kappa_ci_lo','kappa_ci_hi']].to_string())
```

## Cell 22 · python (python) · ok

Inspecting first-pass no_ground_truth statements in subsample

```python

x=sub_df.merge(l[['id','statement']],on='id')
print(pd.crosstab(x.first_pass,x.second_pass).loc['no_ground_truth'].loc[lambda s:s>0])
pd.set_option('display.max_colwidth',110)
print(x[x.first_pass=='no_ground_truth'][['second_pass','statement']].head(25).to_string())
```

## Cell 23 · python (python) · ok

Collapsed-category sensitivity analysis and saving outputs

```python

col=lambda s: s.replace({'no_ground_truth':'knowledge_gap','causality':'knowledge_gap','interpretability':'knowledge_gap'})
f2,s2=col(sub_df.first_pass),col(sub_df.second_pass)
addrow('problem_type_sensitivity','knowledge_gap (no_ground_truth+causality+interpretability merged)',f2=='knowledge_gap',s2=='knowledge_gap','200 random PMIDs (seed 1)')
lo,hi=boot(f2.values,s2.values)
rows.append(dict(analysis='problem_type_sensitivity',category='OVERALL_multiclass_after_merge',subset='200 random PMIDs (seed 1)',n=200,
   pct_agreement=round(100*(f2==s2).mean(),1),kappa=round(kap(f2,s2),3),kappa_ci_lo=round(lo,3),kappa_ci_hi=round(hi,3)))
va=pd.DataFrame(rows); print(va.tail(2)[['category','first_pos','second_pos','pct_agreement','kappa','kappa_ci_lo','kappa_ci_hi']].to_string())
va.to_csv('validation_agreement.csv',index=False)
out=bb[['id','first_pass','benchmark_kind','what_is_compared','second_pass','sp_n_compared','sp_comparison_type','sp_rationale','rater','consensus']].rename(
  columns={'first_pass':'first_pass_is_benchmark','second_pass':'second_pass_is_benchmark','benchmark_kind':'first_pass_kind','what_is_compared':'first_pass_what_is_compared','consensus':'consensus_benchmark'})
out['title']=out.id.map(abs_.title); out.to_csv('benchmark_second_pass.csv',index=False)
pt=x[['id','first_pass','second_pass','statement']].rename(columns={'first_pass':'first_pass_problem_type','second_pass':'second_pass_problem_type','statement':'first_pass_statement'})
pt['title']=pt.id.map(abs_.title); pt['agree']=pt.first_pass_problem_type==pt.second_pass_problem_type
pt['rater']='session model (manual reading, condensed abstract: first 750 + last 300 chars)'
pt.to_csv('problem_types_second_pass.csv',index=False)
print(pd.crosstab(pt.first_pass_problem_type,pt.second_pass_problem_type).to_string())
```

## Cell 24 · bash (python) · ok

Writing validation_methods.md

```bash
cat > validation_methods.md <<'EOF'
# Second-pass classification reliability: methods and results

Date run: 14 Oct 2026. The inputs are the 4 Oct 2026 data-pull files from the prior-analysis zip (`benchmark_classification.csv`, `limitations_extracted.csv`, `sc_cancer_corpus.csv`).

## Abstract source
All 486 benchmark PMIDs and all 200 subsample PMIDs already had a title and an abstract in `sc_cancer_corpus.csv` (100% coverage). That file holds PubMed-derived records, so no new efetch call was made.

## Part 1: benchmark re-classification (n = 486)
- **Definition given to the rater.** A benchmark is a study whose stated purpose includes a systematic, head-to-head comparison of at least 2 named computational tools, algorithms, pipelines or experimental platforms/protocols on a shared task (same data or same samples), assessed on common criteria. A new-method paper counts only if it reports a systematic comparison against at least 2 named existing tools on shared data. The following do not count: reviews; biological or clinical "evaluation" of a gene, drug, cell population, model system or cohort; validation of a single tool; comparisons of biological conditions, tissues or species.
- **Blinding.** The rater saw only the title and abstract. First-pass labels were never shown to it.
- **Rater A: 394 PMIDs.** These were rated by `host.llm` at the utility (Haiku-class) tier. The resolved model was claude-haiku-4-5-20251001, run with temperature 0 and a forced-tool structured output: is_benchmark, n_named_entities_compared, comparison_type and rationale. This tier differs from the platform's default reasoning (Sonnet-class) tier.
- **Rater B: 92 PMIDs** (positions 395–486 in file order). The host enforces a 2.0M-token ceiling per frame on `host.llm`, and the batch hit it after 394 requests. Each request cost about 5.1k input tokens because the host system prompt is large. The remaining 92 abstracts were therefore rated by hand by the session model, which is a different model again. The same written definition was applied, and first-pass labels were not viewed until rating was finished. The reading used condensed text: the title, the first 650 characters and the last 300 characters of each abstract.

## Part 2: problem-type re-extraction (200 PMIDs)
- **Sample.** 200 PMIDs were drawn with `numpy.random.default_rng(1).choice(unique ids, 200, replace=False)` from the 1,757 PMIDs in `limitations_extracted.csv`.
- **Unit of agreement.** The first pass assigned one primary problem type per paper (1,757 rows for 1,757 PMIDs). The second pass therefore also assigned one primary label per paper, from the same 18-value vocabulary: causality, clinical_translation, confounding, cost_scalability, data_access, generalization, interpretability, metric_invalid, no_benchmark, no_ground_truth, none, other, parameter_sensitivity, reproducibility, resolution_limit, sample_size, technical_artifact, uncertainty. Presence/absence per paper × category is the one-hot coding of these labels.
- **Rater.** The LLM ceiling was already exhausted, so all 200 abstracts were labelled by hand by the session model, blind to the first-pass label and statement. The reading used the title, the first 750 characters and the last 300 characters of each abstract.
- **Working definitions of the second pass.** The first-pass category definitions were not available, so these were written fresh:
  - no_ground_truth: absence of a validated reference standard, labels or gold standard against which a method or result could be checked.
  - causality: a mechanism, role or driver is unknown.
  - interpretability: composition, heterogeneity or landscape is poorly characterised.
  - metric_invalid: a performance metric does not measure what it claims to.
  - parameter_sensitivity: results depend on analysis choices.
  - uncertainty: lack of error or confidence quantification.

## Statistics
Cohen's kappa was computed directly as (po − pe)/(1 − pe), together with percent agreement and the 2×2 cells (both+, first-only, second-only, both−). 95% CIs come from a nonparametric bootstrap over papers (2,000 resamples, numpy seed 1, percentile method). Two overall problem-type measures are reported:
1. pooled paper × category presence/absence (200 × 18 cells);
2. multiclass kappa on the primary label.

A sensitivity analysis merges no_ground_truth, causality and interpretability into one "knowledge_gap" class.

## Results
### Benchmark (validation_agreement.csv)
| subset | n | first + | second + | both + | first only | second only | % agree | kappa [95% CI] |
|---|---|---|---|---|---|---|---|---|
| all 486 (mixed raters) | 486 | 158 | 166 | 134 | 24 | 32 | 88.5 | 0.741 [0.676, 0.798] |
| Haiku-4.5 subset | 394 | 139 | 159 | 127 | 12 | 32 | 88.8 | 0.763 [0.693, 0.829] |
| manual subset | 92 | 19 | 7 | 7 | 12 | 0 | 87.0 | 0.481 [0.229, 0.700] |

- **Counts.** The second pass found 166 benchmarks; the first pass found 158. The consensus count (both raters positive) is **134**.
- **Where the raters disagree.**
  - Of the 32 second-pass-only positives, 14 were first-pass new_method_with_baselines and 16 were biological_evaluation. The second rater counted new-method papers with ≥2 named baselines as benchmarks.
  - All 24 first-pass-only positives were first-pass method_comparison or platform_comparison. Many compare non-tools: CAR-T cell types, xenograft routes, SGLT2 inhibitors, radionuclides, organs.
- **Interpretation.** A defensible range for the benchmark count is **134–166**, with 158 inside it. Agreement is "substantial" on the Landis–Koch scale.

### Problem types (n = 200)
- **Overall agreement is low.** Pooled presence/absence: 91.9% agreement, kappa 0.227 [0.170, 0.287]. Multiclass primary label: 27.0% agreement, kappa 0.167 [0.110, 0.229]. After merging into knowledge_gap: multiclass kappa 0.302 [0.225, 0.380]; knowledge_gap itself 0.505 [0.378, 0.620].
- **no_ground_truth.** The first pass assigned it to 45/200 papers; the second pass to 1/200. None overlapped: kappa −0.010 [−0.029, 0.000]. Of the 45 first-pass no_ground_truth papers, the second pass coded 30 as causality and 9 as interpretability. Their first-pass statements are mostly "mechanism/landscape unknown" (e.g. "Mechanisms of circulating tumor cell immune evasion unknown"). These are not statements about a missing reference standard.
- **metric_invalid.** First pass 4/200, second pass 0/200: kappa 0.000.
- **parameter_sensitivity.** First pass 2/200, second pass 0/200: kappa 0.000.
- **uncertainty.** Neither pass assigned it in the subsample (0/0), so kappa is undefined.
- **Categories with moderate agreement.** reproducibility 0.798 and data_access 0.664 rest on 1–2 positives each and have wide CIs. technical_artifact is 0.446 and resolution_limit 0.304.

## Implications for the review's claims
1. The 158/486 benchmark count is reasonably reliable (kappa ≈ 0.74). Report it as 158 (second-pass 166; consensus 134).
2. The headline "no ground truth = 24.2% of methodological problems" does **not** replicate under a strict reading of "ground truth". The first-pass label mostly captured unknown biological mechanism or landscape. The claim should be reworded (e.g. "unresolved biology / absent reference knowledge") or the 1,757 statements should be re-coded with explicit definitions before it is used.
3. The rare categories (metric validity 1.1%, parameter sensitivity 2.3%, uncertainty 0.7%) stayed rare, or became rarer, in the second pass. The qualitative claim "rarely stated in abstracts" holds, but the per-category kappa cannot be estimated reliably at these prevalences.

## Limitations
- The second raters are mixed: Haiku-4.5 for 394 benchmark abstracts; the session model, reading by hand, for 92 benchmark and all 200 problem-type abstracts. The cause was the per-frame LLM token ceiling.
- The manual ratings used condensed abstracts (mid-abstract text truncated). This can miss baseline comparisons, e.g. for the TRACE, Hypatia and GATE papers, which the first pass called method comparisons.
- The first-pass category definitions were unavailable. Part of the problem-type disagreement is therefore a difference in definitions rather than random error, and that is itself a finding about construct validity.
- This is one second pass, not adjudicated by a human. Counts in this file are provisional.
EOF
echo ok
```

## Cell 25 · repl · ok

Submitting structured output

```python

out={
 "summary":("Second-pass reliability check. Benchmark calls (n=486): agreement 88.5%, Cohen's kappa 0.741 [95% bootstrap CI 0.676-0.798]; "
  "2x2 = both+ 134, first-only 24, second-only 32, both- 296. Second pass 166 benchmarks vs first-pass 158; consensus 134. "
  "Haiku-4.5 subset (394): kappa 0.763 [0.693-0.829]; manually rated subset (92): kappa 0.481 [0.229-0.700]. "
  "Problem types (200 random PMIDs, seed 1, single primary label as in first pass): pooled paper x category kappa 0.227 [0.170-0.287], multiclass kappa 0.167 [0.110-0.229] (27% exact agreement). "
  "KEY FINDING: first-pass 'no_ground_truth' does not replicate (45/200 first vs 1/200 second, kappa -0.010); 30 of the 45 were recoded as causality and 9 as interpretability. "
  "Their statements are 'mechanism/landscape unknown', not absence of a reference standard, so the 24.2% 'no ground truth' headline needs rewording or re-coding. "
  "metric_invalid 4 vs 0 (kappa 0), parameter_sensitivity 2 vs 0 (kappa 0), uncertainty 0 vs 0 (undefined). The rare categories stay rare. "
  "All counts are provisional: mixed second raters and condensed abstracts for manual ratings."),
 "kappa_benchmark":"0.741 (95% bootstrap CI 0.676-0.798), 88.5% agreement, n=486; Haiku-only subset 0.763 [0.693-0.829], n=394",
 "second_pass_benchmark_count":166,
 "problem_type_agreement":("Overall pooled presence/absence kappa 0.227 [0.170-0.287]; multiclass 0.167 [0.110-0.229]; merged knowledge_gap (no_ground_truth+causality+interpretability) kappa 0.505 [0.378-0.620]. "
  "Per category: no_ground_truth -0.010 [-0.029,0.000] (45 vs 1 positives); metric_invalid 0.000 (4 vs 0); parameter_sensitivity 0.000 (2 vs 0); uncertainty undefined (0 vs 0); "
  "causality 0.262; interpretability 0.074; technical_artifact 0.446; resolution_limit 0.304; reproducibility 0.798 (2 vs 3)."),
 "artifacts":["validation_agreement.csv (51ce5aae-8c42-45b1-881f-579498152a54)","benchmark_second_pass.csv (2247019b-0846-4bde-8fce-c97aaec1eb2e)",
   "problem_types_second_pass.csv (6b13a5c6-6344-459c-90e2-5dabb0ca5c76)","validation_methods.md (916b24df-7071-4085-8ff9-685885dd1c0c)"]}
r=host.submit_output(out,completion_bullets=["Re-classified all 486 evaluation-titled abstracts blind to first-pass labels",
  "Re-extracted problem types for 200 random PMIDs (seed 1)","Computed kappa, bootstrap CIs and confusion matrices",
  "Found that the first-pass no_ground_truth label does not replicate"],
 deviations=["host.llm hit the 2.0M per-frame token ceiling after 394/486 benchmark requests (~5.1k input tokens each). The remaining 92 benchmark abstracts (file positions 395-486) and ALL 200 problem-type abstracts were rated by hand by the session model, not by a Haiku-tier LLM, so the second raters are mixed. Kappas are reported per rater subset.",
  "Manual ratings used condensed abstracts (title + first 650/750 chars + last 300 chars), not full abstracts. Mid-abstract baseline comparisons may have been missed.",
  "No new PubMed efetch: all 486 + 200 abstracts were taken from sc_cancer_corpus.csv (100% coverage), which the task permits.",
  "First-pass category definitions were unavailable; second-pass working definitions were written fresh (in validation_methods.md). The problem-type second pass is single-label to match the first-pass structure (one row per PMID).",
  "All second-pass counts (166, consensus 134, per-category prevalences) are provisional: one non-adjudicated second pass."])
print(r)
```

## Cell 26 · repl · ok

Checking open reviewer findings

```python
print(host.findings())
```
