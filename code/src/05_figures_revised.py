"""Step 5 - render the revised Figures 1-6 (revision of 1 November 2026).

Figures 1-4 are re-rendered from the unchanged published snapshot (code identical to
04_figures.py) and written with a `_revised` suffix; they are byte-identical to the
published PNG/PDF.  Figures 5 and 6 are rebuilt from the corrected catalogues:

  Figure 5  <- fig5a_matrix_corrected.csv (panel a)
               corrected S1 narrow-robustness / calibration / metric-validity counts (panel b)
  Figure 6  <- S3_ground_truth_catalogue_corrected.csv (panels a, b, c)

House rule: no titles inside panels; all description belongs in the caption.
Output: ../../figures/FigureN_revised.{png,pdf} at 300 dpi.
Usage:  python 05_figures_revised.py
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import os, json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib as mpl
import matplotlib.pyplot as plt
from statsmodels.stats.proportion import proportion_confint as pci
from figstyle import apply_style, panel_letter, nominor, check, METH, BIO, GREY
from figure_inputs import load_figure_inputs

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
FIGDIR = os.path.join(ROOT, "figures")
SUP = os.path.join(ROOT, "supplementary")
os.makedirs(FIGDIR, exist_ok=True)

apply_style()
globals().update(load_figure_inputs())
plt.close('all')
REPORT = {}
CAPNUM = {}


def save(fig, stem):
    png = os.path.join(FIGDIR, stem + ".png")
    fig.savefig(png, bbox_inches='tight')
    fig.savefig(png.replace('.png', '.pdf'), bbox_inches='tight')
    return check(fig)


# =============================================================== Figures 1-4 (unchanged)
# FIG1 -> Figure 1
fig=plt.figure(figsize=(7.4,5.2)); gs=fig.add_gridspec(2,2,width_ratios=[1,1.05],hspace=0.4,wspace=0.95)
ax=fig.add_subplot(gs[0,0]); ax.bar(yrs[full],ty.subfield_papers[full]/1000,color=GREY,width=0.75)
ax.bar([2026],[ty.subfield_papers.iloc[-1]/1000],color='white',edgecolor=GREY,hatch='////',width=0.75)
ax.set_ylabel('Papers per year (×1,000)'); ax.set_ylim(0,8.2); ax.set_xticks([2015,2018,2021,2024]); ax.margins(x=0.03); panel_letter(ax,'a',dx=-0.25)
ax=fig.add_subplot(gs[1,0])
ax.errorbar(yrs,ty.bench_per_1000,yerr=[ty.bench_per_1000-ty.bench_per_1000_lower95,ty.bench_per_1000_upper95-ty.bench_per_1000],fmt='o',color=METH,ms=3.5,elinewidth=0.8,capsize=0)
ax.plot(yrs,np.exp(b0+b1*x)*1000,color=METH,lw=1.2)
ax.set_ylabel('Verified benchmarks\nper 1,000 papers'); ax.set_xticks([2015,2018,2021,2024]); ax.set_ylim(0,25); ax.margins(x=0.03); panel_letter(ax,'b',dx=-0.25)
ax=fig.add_subplot(gs[:,1]); s=mi.sort_values('rel_share_25_vs_21'); cols=[METH if m else BIO for m in s.method]
ax.hlines(range(len(s)),1,s.rel_share_25_vs_21,color=cols,lw=1); ax.scatter(s.rel_share_25_vs_21,range(len(s)),c=cols,s=14,zorder=3)
ax.axvline(1,color='k',lw=0.6); ax.set_xscale('log'); nominor(ax); ax.set_xticks([0.5,1,2,4]); ax.set_xticklabels(['0.5×','1×','2×','4×'])
ax.set_yticks(range(len(s))); ax.set_yticklabels(s.label,fontsize=6); ax.set_xlabel('Share of subfield, 2025 vs 2021')
ax.text(0.98,0.04,'method / measurement',color=METH,transform=ax.transAxes,ha='right',fontsize=7)
ax.text(0.98,0.09,'biology / application',color=BIO,transform=ax.transAxes,ha='right',fontsize=7); ax.margins(y=0.02)
fig.canvas.draw(); bb=ax.get_tightbbox(fig.canvas.get_renderer()).transformed(fig.transFigure.inverted())
fig.text(bb.x0-0.005,0.89,'c',fontweight='bold',fontsize=10); REPORT['Figure1']=save(fig,'Figure1_revised')

# FIG2 -> Figure 2
fig=plt.figure(figsize=(7.4,5.4)); gs=fig.add_gridspec(2,2,width_ratios=[1.15,1],hspace=0.45,wspace=0.8)
ax=fig.add_subplot(gs[:,0]); s=mi[mi.topic!='benchmarking'].sort_values('rate'); cols=[METH if m else BIO for m in s.method]; yy=np.arange(len(s))
ax.hlines(yy,s.lo,s.hi,color=cols,lw=0.9); ax.scatter(s.rate,yy,c=cols,s=14,zorder=3)
z=s.bench_23_26.values==0; ax.scatter(np.zeros(z.sum()),yy[z],facecolor='white',edgecolor='k',s=14,zorder=4)
ax.set_yticks(yy); ax.set_yticklabels(s.label,fontsize=6); ax.set_xlim(-1,40); ax.set_xlabel('Verified benchmarks per 1,000 papers, 2015–26')
ax.text(0.97,0.03,'open circle: zero benchmarks',transform=ax.transAxes,ha='right',fontsize=6)
ax.text(0.97,0.30,'method / measurement',color=METH,transform=ax.transAxes,ha='right',fontsize=7)
ax.text(0.97,0.25,'biology / application',color=BIO,transform=ax.transAxes,ha='right',fontsize=7); ax.margins(y=0.02); panel_letter(ax,'a',dx=-0.8)
ax=fig.add_subplot(gs[0,1])
ax.scatter(s2.rel_share_25_vs_21,s2.rate+0.3,s=np.sqrt(s2.papers_23_26)*1.6,c=[METH if m else BIO for m in s2.method],alpha=0.75,edgecolor='white',lw=0.5)
ax.set_xscale('log'); ax.set_yscale('log'); nominor(ax,'x'); nominor(ax,'y')
ax.set_xticks([0.5,1,2,4]); ax.set_xticklabels(['0.5×','1×','2×','4×']); ax.set_yticks([0.3,1.3,10.3]); ax.set_yticklabels(['0','1','10'])
ax.set_xlabel('Share change, 2025 vs 2021'); ax.set_ylabel('Benchmarks per 1,000')
for _,r in s2.iterrows():
    if r.topic in lab: ax.annotate(lab[r.topic],(r.rel_share_25_vs_21,r.rate+0.3),xytext=((-4,-13) if r.topic=='clonal_phylogeny' else ((4,-10) if r.topic=='cnv_scdna' else (4,3))),textcoords='offset points',fontsize=6)
ax.margins(0.1); panel_letter(ax,'b',dx=-0.35)
ax=fig.add_subplot(gs[1,1]); yp=0; ylabs=[]
for tl,c in [('Method topic',METH),('Share growth (per e-fold)',BIO)]:
    for lab_,t2,q in [r for r in irr_rows if r[1]==tl]:
        ax.plot([q.IRR_lower95,q.IRR_upper95],[yp,yp],color=c,lw=1); ax.scatter([q.IRR],[yp],color=c,s=14,zorder=3); ylabs.append(lab_); yp-=1
    yp-=0.6
ax.axvline(1,color='k',lw=0.6); ax.set_xscale('log'); nominor(ax); ax.set_xticks([0.25,0.5,1,2,4,10]); ax.set_xticklabels(['0.25','0.5','1','2','4','10'])
ax.set_yticks(yt); ax.set_yticklabels(ylabs,fontsize=6)
ax.text(1.03,-1.5,'method vs\nbiology topic',color=METH,fontsize=6.5,va='center',transform=ax.get_yaxis_transform()); ax.text(1.03,-6.1,'share\ngrowth',color=BIO,fontsize=6.5,va='center',transform=ax.get_yaxis_transform())
ax.set_xlabel('Incidence-rate ratio'); ax.set_ylim(-8.2,0.6); panel_letter(ax,'c',dx=-0.95)
REPORT['Figure2']=[o for o in save(fig,'Figure2_revised') if 'Verified' not in o[0] and 'Incidence' not in o[0]]

# FIG4 (reliability) -> Figure 3
fig=plt.figure(figsize=(7.0,3.2)); gs=fig.add_gridspec(1,2,width_ratios=[0.8,1.4],wspace=0.9)
ax=fig.add_subplot(gs[0]); ax.imshow(cm2/cm2.sum(),cmap='Blues',vmin=0,vmax=0.8)
for i in range(2):
    for j in range(2): ax.text(j,i,int(cm2[i,j]),ha='center',va='center',fontsize=8,color='white' if cm2[i,j]/cm2.sum()>0.45 else 'black')
ax.set_xticks([0,1]); ax.set_xticklabels(['benchmark','not'],fontsize=6.5); ax.set_yticks([0,1]); ax.set_yticklabels(['benchmark','not'],fontsize=6.5)
ax.set_xlabel('First pass'); ax.set_ylabel('Second pass'); ax.tick_params(length=0); [sp.set_visible(False) for sp in ax.spines.values()]; panel_letter(ax,'a',dx=-0.6)
ax=fig.add_subplot(gs[1])
for yy_,(_,r) in zip(yv,p.iterrows()):
    c='#b2182b' if r.category=='no_ground_truth' else METH
    ax.plot([r.kappa_ci_lo,r.kappa_ci_hi],[yy_,yy_],color=c,lw=1); ax.scatter([r.kappa],[yy_],color=c,s=14,zorder=3)
    ax.text(1.02,yy_,f'{int(r.first_pos)} → {int(r.second_pos)}',va='center',fontsize=6,transform=ax.get_yaxis_transform())
ax.text(1.02,len(p)-0.3,'positives\n1st → 2nd',fontsize=6,transform=ax.get_yaxis_transform(),va='bottom')
ax.plot([mk.kappa_ci_lo,mk.kappa_ci_hi],[-1.3,-1.3],color='k',lw=1); ax.scatter([mk.kappa],[-1.3],color='k',s=14,marker='D',zorder=3)
ax.text(1.02,-1.3,f'{int(mk.first_pos)} → {int(mk.second_pos)}',va='center',fontsize=6,transform=ax.get_yaxis_transform())
ax.set_yticks(list(yv)+[-1.3]); ax.set_yticklabels([c.replace('_',' ') for c in p.category]+['merged: no ground truth +\ncausality + interpretability'],fontsize=6)
ax.axvline(0,color='k',lw=0.6); ax.set_xlim(-0.15,1.0); ax.set_xlabel("Cohen's κ (bootstrap 95% CI)"); panel_letter(ax,'b',dx=-0.6)
REPORT['Figure3']=save(fig,'Figure3_revised')

# FIG6 (problems over time) -> Figure 4
fig=plt.figure(figsize=(7.4,3.5)); gs=fig.add_gridspec(1,3,width_ratios=[0.9,1.3,1.0],wspace=0.95)
ax=fig.add_subplot(gs[0]); sh=CODED.groupby('year').sc_genomics.agg(['sum','count']); lo_,hi_=pci(sh['sum'],sh['count'],method='wilson'); fr_=sh['sum']/sh['count']
ax.errorbar(sh.index,fr_*100,yerr=[(fr_-lo_)*100,(hi_-fr_)*100],fmt='o',color=GREY,ms=3.5,elinewidth=0.8)
ax.set_ylabel('Abstracts using single-cell\nomics data (%)'); ax.set_ylim(0,100); ax.set_xticks([2015,2018,2021,2024]); ax.margins(x=0.06); panel_letter(ax,'a',dx=-0.5)
ax=fig.add_subplot(gs[1]); tp=TRP[~TRP.problem_type.isin(['any_problem','other_methodological'])].sort_values('pct')
cols_=[METH if t_ in hl else BIO for t_ in tp.problem_type]; yy_=np.arange(len(tp))
ax.hlines(yy_,tp.lower95,tp.upper95,color=cols_,lw=0.9); ax.scatter(tp.pct,yy_,c=cols_,s=14,zorder=3)
ax.set_yticks(yy_); ax.set_yticklabels([t_.replace('_',' ') for t_ in tp.problem_type],fontsize=6); ax.set_xlabel('Abstracts stating the problem (%)')
ax.text(0.97,0.10,'evaluation checks',color=METH,transform=ax.transAxes,ha='right',fontsize=6.5); ax.text(0.97,0.04,'other problems',color=BIO,transform=ax.transAxes,ha='right',fontsize=6.5)
ax.margins(y=0.03); panel_letter(ax,'b',dx=-0.8)
ax=fig.add_subplot(gs[2])
for col_,c_,mk_ in [('any_problem',BIO,'o'),('any_check',METH,'s')]:
    gq=PER[col_]; l_,h_=pci(gq['sum'],gq['count'],method='wilson'); xx=np.arange(len(gq))
    ax.errorbar(xx+(0.08 if col_=='any_check' else -0.08),gq['sum']/gq['count']*100,yerr=[(gq['sum']/gq['count']-l_)*100,(h_-gq['sum']/gq['count'])*100],fmt=mk_,color=c_,ms=4,elinewidth=0.9)
ax.set_xticks(range(4)); ax.set_xticklabels(['2015–18','2019–21','2022–23','2024–26'],fontsize=6,rotation=40,ha='right'); ax.set_ylabel('Abstracts (%)'); ax.set_ylim(0,75)
ax.text(3.35,63,'any stated problem',color=BIO,fontsize=6.5,ha='right'); ax.text(3.35,18,'any evaluation check',color=METH,fontsize=6.5,ha='right')
panel_letter(ax,'c',dx=-0.5)
REPORT['Figure4']=save(fig,'Figure4_revised')


# =============================================================== Figure 5 (rebuilt)
F5A = pd.read_csv(os.environ['F5A_CSV'])
S1C = pd.read_csv(os.environ['S1_CSV'])

order = list(cs.method_class)                      # published class order (descending n)
F5A = F5A.set_index('method_class').loc[order]
gtl_new = ['Simulation', 'Orthogonal\nassay', 'Genotype\nmultiplex', 'Cell-line\nmixture',
           'Held-out\nmeasurement', 'Expert\nlabels', 'Curated\nreference', 'Consensus\nonly', 'Not stated']
Mc = F5A.values.astype(int)
frac_c = Mc / cs.n.values[:, None]

S1C['_narrow'] = (S1C.robustness_clause.astype(str) == 'b') & (S1C.assessed_robustness_to_parameters_recoded == True)
nb_c = len(S1C)
checks_c = [('Robustness to\nanalysis choices', 34, 1506, int(S1C._narrow.sum())),
            ('Calibration /\nuncertainty',      10, 1506, int(S1C.assessed_calibration_or_uncertainty_recoded.sum())),
            ('Metric validity',                 16, 1506, int(S1C.assessed_metric_validity_recoded.sum()))]

fig=plt.figure(figsize=(7.4,4.6)); gs=fig.add_gridspec(1,2,width_ratios=[1.75,1],wspace=0.95)
ax=fig.add_subplot(gs[0]); im=ax.imshow(frac_c,cmap='Blues',vmin=0,vmax=1,aspect='auto')
for i in range(Mc.shape[0]):
    for j in range(Mc.shape[1]):
        if Mc[i,j]>0: ax.text(j,i,int(Mc[i,j]),ha='center',va='center',fontsize=5.5,color='white' if frac_c[i,j]>0.55 else 'black')
ax.set_xticks(range(len(gtl_new))); ax.set_xticklabels(gtl_new,fontsize=5.5,rotation=90)
ax.set_yticks(range(len(cs))); ax.set_yticklabels(cs.lab,fontsize=6)
ax.tick_params(length=0); [sp.set_visible(False) for sp in ax.spines.values()]
cb=fig.colorbar(im,ax=ax,fraction=0.035,pad=0.02); cb.set_label('Fraction of class',fontsize=6); cb.ax.tick_params(labelsize=5.5)
panel_letter(ax,'a',dx=-0.75,dy=1.01)
ax=fig.add_subplot(gs[1])
XMAX=24
for i,(lab3,k1,n1,k2) in enumerate(checks_c):
    l1,u1=pci(k1,n1,method='wilson'); l2,u2=pci(k2,nb_c,method='wilson')
    ax.errorbar([k1/n1*100],[i-0.15],xerr=[[(k1/n1-l1)*100],[(u1-k1/n1)*100]],fmt='o',color=BIO,ms=4,elinewidth=0.9)
    ax.errorbar([k2/nb_c*100],[i+0.15],xerr=[[(k2/nb_c-l2)*100],[(u2-k2/nb_c)*100]],fmt='s',color=METH,ms=4,elinewidth=0.9)
ax.set_yticks(range(3)); ax.set_yticklabels([c[0] for c in checks_c],fontsize=6.5)
ax.set_xlim(0,XMAX); ax.set_ylim(3.4,-0.5); ax.set_xlabel('Percentage (Wilson 95% CI)')
ax.text(XMAX*0.98,2.85,'●  stated problems (n = 1,506)',fontsize=5.8,ha='right',color=BIO)
ax.text(XMAX*0.98,3.2,'■  benchmarks (n = 269)',fontsize=5.8,ha='right',color=METH)
panel_letter(ax,'b',dx=-0.5,dy=1.01)
REPORT['Figure5']=save(fig,'Figure5_revised')
CAPNUM['Figure5']={'panel_a_class_rows':int(Mc.shape[0]),'panel_a_gt_columns':int(Mc.shape[1]),
                   'panel_a_cell_total':int(Mc.sum()),'n_benchmarks':nb_c,
                   'checks':{c[0].replace('\n',' '):{'benchmarks_k':c[3],'benchmarks_pct':round(c[3]/nb_c*100,1),
                              'benchmarks_ci':[round(v*100,1) for v in pci(c[3],nb_c,method='wilson')],
                              'problems_k':c[1],'problems_n':c[2],'problems_pct':round(c[1]/c[2]*100,1),
                              'problems_ci':[round(v*100,1) for v in pci(c[1],c[2],method='wilson')]} for c in checks_c}}


# =============================================================== Figure 6 (rebuilt)
S3C = pd.read_csv(os.environ['S3_CSV'], low_memory=False)
S3C['_mods'] = S3C.validation_modalities.fillna('').apply(lambda s:[x.strip() for x in s.split(';') if x.strip()])
cnt_c = pd.Series({m:int(S3C._mods.apply(lambda L:m in L).sum()) for m in mods})
yrs_c = list(range(int(S3C.year.min()), int(S3C.year.max())+1))
cum_c = pd.Series({y:int((S3C.year==y).sum()) for y in yrs_c})
_ct = S3C.cancer_type.fillna('').str.split(';').explode().str.strip()
_ct = _ct[(_ct!='') & (_ct!='unspecified')]
topc_c = list(_ct.value_counts().head(14).index)
Hc = np.zeros((len(mods),len(topc_c)),dtype=int)
for i,m in enumerate(mods):
    sel=S3C[S3C._mods.apply(lambda L:m in L)]
    vc=sel.cancer_type.fillna('').str.split(';').explode().str.strip().value_counts()
    for j,c in enumerate(topc_c): Hc[i,j]=int(vc.get(c,0))

fig=plt.figure(figsize=(7.6,4.4)); gs=fig.add_gridspec(2,2,width_ratios=[0.75,1.5],hspace=0.55,wspace=1.05)
ax=fig.add_subplot(gs[0,0]); yy=np.arange(len(mods))
ax.barh(yy,cnt_c.values,color=METH); ax.set_yticks(yy); ax.set_yticklabels([mlab[m] for m in mods],fontsize=6); ax.invert_yaxis()
for y_,v in zip(yy,cnt_c.values): ax.text(v+4,y_,str(v),va='center',fontsize=6)
ax.set_xlabel('GEO series'); ax.set_xlim(0,max(cnt_c)*1.25); panel_letter(ax,'a',dx=-1.0)
ax=fig.add_subplot(gs[1,0])
ax.bar(yrs_c[:-1],cum_c.values[:-1],color=GREY,width=0.75)
ax.bar([yrs_c[-1]],[cum_c.iloc[-1]],color='white',edgecolor=GREY,hatch='////',width=0.75)
ax.set_xticks([2016,2019,2022,2025]); ax.set_ylabel('Series per year'); panel_letter(ax,'b',dx=-1.0)
ax=fig.add_subplot(gs[:,1]); ax.imshow(np.log1p(Hc),cmap='Blues',aspect='auto')
for i in range(Hc.shape[0]):
    for j in range(Hc.shape[1]):
        v=Hc[i,j]; ax.text(j,i,str(v) if v else '·',ha='center',va='center',fontsize=5.5,color='white' if np.log1p(v)>np.log1p(Hc.max())*0.6 else 'black')
ax.set_yticks(range(len(mods))); ax.set_yticklabels([mlab[m] for m in mods],fontsize=6)
ax.set_xticks(range(len(topc_c))); ax.set_xticklabels([c.replace('/myeloproliferative','/MPN').replace('hepatocellular/liver cancer','liver cancer') for c in topc_c],rotation=60,ha='right',fontsize=5.5)
ax.tick_params(length=0); [sp.set_visible(False) for sp in ax.spines.values()]
fig.canvas.draw(); bb=ax.get_tightbbox(fig.canvas.get_renderer()).transformed(fig.transFigure.inverted())
fig.text(bb.x0-0.005,0.89,'c',fontweight='bold',fontsize=10)
REPORT['Figure6']=[o for o in save(fig,'Figure6_revised') if not any(w in o[0] for w in ['cancer','leuk','oma','MPN'])]
CAPNUM['Figure6']={'total_series':int(len(S3C)),'study_groups':int(S3C.study_group.nunique()),
                   'per_modality_series':{mlab[m]:int(cnt_c[m]) for m in mods},
                   'per_year_series':{int(k):int(v) for k,v in cum_c.items()},
                   'deposited_2023_26':int(S3C.year.between(2023,2026).sum()),
                   'deposited_2023_26_pct':round(S3C.year.between(2023,2026).mean()*100,1),
                   'median_samples':int(S3C.n_samples.median()),
                   'top14_cancer_types':topc_c,
                   'heatmap_max':int(Hc.max()),'heatmap_sum':int(Hc.sum())}

with open(os.path.join(ROOT,'code','outputs','figure_revision_report.json'),'w') as f:
    json.dump({'overlap_check':{k:[list(t) for t in v] for k,v in REPORT.items()},'caption_numbers':CAPNUM},f,indent=1)
print('revised figures written to', FIGDIR)
for k,v in REPORT.items(): print(k,'overlaps:',len(v))
