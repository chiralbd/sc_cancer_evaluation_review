"""Step 4 - render Figures 1-6 exactly as published.

Inputs are the in-memory objects the figure code consumed in the analysis session,
snapshotted to data/figure_inputs/ (see figure_inputs.py). Figure code below is the
code that produced the published figures, unchanged except for this header.
Output: outputs/fig/*.png (300 dpi) and *.pdf. File names keep the analysis-stage
names; their manuscript numbers are:
  fig1_landscape -> Figure 1, fig2_coverage -> Figure 2, fig4_reliability -> Figure 3,
  fig6_problems_time -> Figure 4, fig3_practice -> Figure 5, fig5_ground_truth -> Figure 6.
Usage:  python 04_figures.py
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib as mpl
import matplotlib.pyplot as plt
from statsmodels.stats.proportion import proportion_confint as pci
from figstyle import apply_style, panel_letter, nominor, check, METH, BIO, GREY
from figure_inputs import load_figure_inputs

apply_style()
globals().update(load_figure_inputs())
OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "outputs")
os.makedirs(os.path.join(OUTDIR, "fig"), exist_ok=True)
os.chdir(OUTDIR)

# ---------------------------------------------------------------- Figures 1, 2, 3, 5, 6
plt.close('all')
def save(fig,path):
    fig.savefig(path,bbox_inches='tight'); fig.savefig(path.replace('.png','.pdf'),bbox_inches='tight'); return check(fig)
REPORT={}
# FIG1
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
fig.text(bb.x0-0.005,0.89,'c',fontweight='bold',fontsize=10); REPORT['f1']=save(fig,'fig/fig1_landscape.png')
# FIG2
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
REPORT['f2']=[o for o in save(fig,'fig/fig2_coverage.png') if 'Verified' not in o[0] and 'Incidence' not in o[0]]
# FIG3
fig=plt.figure(figsize=(7.4,4.6)); gs=fig.add_gridspec(1,2,width_ratios=[1.75,1],wspace=0.95)
ax=fig.add_subplot(gs[0]); im=ax.imshow(frac,cmap='Blues',vmin=0,vmax=1,aspect='auto')
for i in range(M.shape[0]):
    for j in range(M.shape[1]):
        if M[i,j]>0: ax.text(j,i,int(M[i,j]),ha='center',va='center',fontsize=5.5,color='white' if frac[i,j]>0.55 else 'black')
ax.set_xticks(range(len(gtl))); ax.set_xticklabels(gtl,fontsize=5.5,rotation=90); ax.set_yticks(range(len(cs))); ax.set_yticklabels(cs.lab,fontsize=6)
ax.tick_params(length=0); [sp.set_visible(False) for sp in ax.spines.values()]
cb=fig.colorbar(im,ax=ax,fraction=0.035,pad=0.02); cb.set_label('Fraction of class',fontsize=6); cb.ax.tick_params(labelsize=5.5); panel_letter(ax,'a',dx=-0.75,dy=1.01)
ax=fig.add_subplot(gs[1])
for i,(lab3,pt,col) in enumerate(checks):
    _,k1,n1,k2,_n=out[i]; l1,u1=pci(k1,n1,method='wilson'); l2,u2=pci(k2,nb,method='wilson')
    ax.errorbar([k1/n1*100],[i-0.15],xerr=[[(k1/n1-l1)*100],[(u1-k1/n1)*100]],fmt='o',color=BIO,ms=4,elinewidth=0.9)
    ax.errorbar([k2/nb*100],[i+0.15],xerr=[[(k2/nb-l2)*100],[(u2-k2/nb)*100]],fmt='s',color=METH,ms=4,elinewidth=0.9)
ax.set_yticks(range(3)); ax.set_yticklabels([c[0] for c in checks],fontsize=6.5); ax.set_xlim(0,10); ax.set_ylim(3.4,-0.5); ax.set_xlabel('Percentage (Wilson 95% CI)')
ax.text(9.8,2.85,'●  stated problems (n = 1,506)',fontsize=5.8,ha='right',color=BIO); ax.text(9.8,3.2,'■  benchmarks (n = 269)',fontsize=5.8,ha='right',color=METH)
panel_letter(ax,'b',dx=-0.5,dy=1.01); REPORT['f3']=save(fig,'fig/fig3_practice.png')
# FIG4
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
REPORT['f4']=save(fig,'fig/fig4_reliability.png')
# FIG5
fig=plt.figure(figsize=(7.6,4.4)); gs=fig.add_gridspec(2,2,width_ratios=[0.75,1.5],hspace=0.55,wspace=1.05)
ax=fig.add_subplot(gs[0,0]); yy=np.arange(len(mods))
ax.barh(yy,cnt.values,color=METH); ax.set_yticks(yy); ax.set_yticklabels([mlab[m] for m in mods],fontsize=6); ax.invert_yaxis()
for y_,v in zip(yy,cnt.values): ax.text(v+8,y_,str(v),va='center',fontsize=6)
ax.set_xlabel('GEO series'); ax.set_xlim(0,max(cnt)*1.25); panel_letter(ax,'a',dx=-1.0)
ax=fig.add_subplot(gs[1,0])
ax.bar(list(yrs_)[:-1],cum.values[:-1],color=GREY,width=0.75); ax.bar([2026],[cum[2026]],color='white',edgecolor=GREY,hatch='////',width=0.75)
ax.set_xticks([2016,2019,2022,2025]); ax.set_ylabel('Series per year'); panel_letter(ax,'b',dx=-1.0)
ax=fig.add_subplot(gs[:,1]); ax.imshow(np.log1p(Hv),cmap='Blues',aspect='auto')
for i in range(Hv.shape[0]):
    for j in range(Hv.shape[1]):
        v=Hv[i,j]; ax.text(j,i,str(v) if v else '·',ha='center',va='center',fontsize=5.5,color='white' if np.log1p(v)>np.log1p(Hv.max())*0.6 else 'black')
ax.set_yticks(range(len(mods))); ax.set_yticklabels([mlab[m] for m in mods],fontsize=6)
ax.set_xticks(range(len(topc))); ax.set_xticklabels([c.replace('/myeloproliferative','/MPN').replace('hepatocellular/liver cancer','liver cancer') for c in topc],rotation=60,ha='right',fontsize=5.5)
ax.tick_params(length=0); [sp.set_visible(False) for sp in ax.spines.values()]
fig.canvas.draw(); bb=ax.get_tightbbox(fig.canvas.get_renderer()).transformed(fig.transFigure.inverted())
fig.text(bb.x0-0.005,0.89,'c',fontweight='bold',fontsize=10)
REPORT['f5']=[o for o in save(fig,'fig/fig5_ground_truth.png') if not any(w in o[0] for w in ['cancer','leuk','oma','MPN'])]


# ---------------------------------------------------------------- Figure 4 (fig6_problems_time)

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
fig.savefig('fig/fig6_problems_time.png',bbox_inches='tight'); fig.savefig('fig/fig6_problems_time.pdf',bbox_inches='tight')

print('figures written to', os.path.join(OUTDIR, 'fig'))
