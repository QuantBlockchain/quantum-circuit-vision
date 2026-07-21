"""
Reproduce the four QCV poster analysis charts DIRECTLY FROM the released dataset
(dataset/experiment_results/*.csv + dataset/annotations/*.json). No hard-coded
numbers: every value is computed from the open-access data, so the figures are
provably consistent with the released experimental results.

Inputs (all under quantum-circuit-vision/dataset/):
  experiment_results/cost_analysis.csv          (credits per call, n=1 full)
  experiment_results/verification_results.csv   (pass/fidelity, n=1 full 132)
  experiment_results/repeat5/verification_repeat5.csv (core 21, n=5)
  annotations/*.json                            (per-circuit difficulty)
Run: python make_poster_figures.py  -> writes the four .pdf files here + prints values.
"""
import os, glob, json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DS = os.path.join(HERE, "..", "dataset")
ER = os.path.join(DS, "experiment_results")

NAVY="#0B3D91"; DKNAVY="#08306B"; BLUE="#356AA0"; TEAL="#2CA089"; CORAL="#E1634A"
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":12,
    "axes.titlesize":15,"axes.titleweight":"bold","axes.titlecolor":NAVY,
    "axes.edgecolor":"#333333"})
MODELS=["claude-opus-4.6","claude-sonnet-4.6","claude-haiku-4.5"]
SHORT={"claude-opus-4.6":"Opus","claude-sonnet-4.6":"Sonnet","claude-haiku-4.5":"Haiku"}

def pr(df): return (df["pass"].astype(str)=="True").mean()*100.0

cost = pd.read_csv(os.path.join(ER,"cost_analysis.csv"))
vr   = pd.read_csv(os.path.join(ER,"verification_results.csv"))
r5   = pd.read_csv(os.path.join(ER,"repeat5","verification_repeat5.csv"))
diff = {}
for f in glob.glob(os.path.join(DS,"annotations","*.json")):
    d=json.load(open(f)); diff[d["id"]]=d.get("difficulty")

# ---- computed values (from data) ----
core_bv={m:pr(r5[(r5.model==m)&(r5["mode"]=="bv")]) for m in MODELS}
core_tv={m:pr(r5[(r5.model==m)&(r5["mode"]=="tv")]) for m in MODELS}
credits={m:cost[(cost.model==m)&(cost["mode"]=="bv")]["credits"].mean() for m in MODELS}
vr["difficulty"]=vr.circuit_name.map(diff)
opusbv=vr[(vr.model=="claude-opus-4.6")&(vr["mode"]=="bv")]
TIERS=["basic","intermediate","advanced"]
diffrate={t:pr(opusbv[opusbv.difficulty==t]) for t in TIERS}
fails=vr[vr["pass"].astype(str)!="True"]
n_fail=len(fails)
exec_share=(fails["error"].astype(str).str.startswith("exec")).mean()*100
fid_share=100-exec_share

print("== computed from released data ==")
print("core n=5 BV:", {SHORT[m]:round(core_bv[m],1) for m in MODELS})
print("core n=5 TV:", {SHORT[m]:round(core_tv[m],1) for m in MODELS})
print("credits/call BV:", {SHORT[m]:round(credits[m],3) for m in MODELS})
print("difficulty (Opus BV full):", {t:round(diffrate[t],1) for t in TIERS})
print(f"failures total={n_fail}  fidelity={fid_share:.0f}%  exec/API={exec_share:.0f}%")

# ---- 1. Pareto ----
fig,ax=plt.subplots(figsize=(6.2,4.3))
cols={"claude-haiku-4.5":CORAL,"claude-sonnet-4.6":TEAL,"claude-opus-4.6":BLUE}
order=sorted(MODELS,key=lambda m:credits[m])
ax.plot([credits[m] for m in order],[core_bv[m] for m in order],"--",color="#9A9A9A",lw=1.6,zorder=1,label="Pareto frontier")
for m in order:
    ax.scatter(credits[m],core_bv[m],s=1300,c=cols[m],edgecolors=NAVY,linewidths=2.2,zorder=3)
    ax.annotate(SHORT[m],(credits[m],core_bv[m]),xytext=(0,24),textcoords="offset points",ha="center",color=NAVY,fontweight="bold",fontsize=14)
ax.set_xscale("log"); ax.set_xlabel("Cost per call (credits, log)")
ax.set_ylabel("Core pass rate (%)   n=5 BV"); ax.set_title("Cost-Accuracy Pareto Frontier")
ax.set_ylim(40,100); ax.grid(True,which="both",alpha=0.25); ax.legend(loc="lower right",fontsize=10)
fig.tight_layout(); fig.savefig(os.path.join(HERE,"fig_pareto.pdf"))

# ---- 2. Difficulty ----
fig,ax=plt.subplots(figsize=(6.2,3.8))
labels=["Advanced","Intermediate","Basic"]; vals=[diffrate["advanced"],diffrate["intermediate"],diffrate["basic"]]
cols2=[CORAL,DKNAVY,TEAL]; y=range(3)
ax.barh(y,vals,color=cols2,edgecolor="white")
for yi,v in zip(y,vals): ax.text(v+1.5,yi,f"{v:.0f}%",va="center",color=NAVY,fontweight="bold",fontsize=14)
ax.set_yticks(list(y)); ax.set_yticklabels(labels); ax.set_xlim(0,100)
ax.set_xlabel("Opus BV pass rate (%)"); ax.set_title("Difficulty gradient (n=1 full)")
for s in ["top","right"]: ax.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig(os.path.join(HERE,"fig_difficulty.pdf"))

# ---- 3. BV vs TV ----
fig,ax=plt.subplots(figsize=(6.4,4.3))
ms=["claude-sonnet-4.6","claude-opus-4.6","claude-haiku-4.5"]
bv=[core_bv[m] for m in ms]; tv=[core_tv[m] for m in ms]; x=range(3); w=0.38
ax.bar([i-w/2 for i in x],bv,w,color=DKNAVY,label="BV")
ax.bar([i+w/2 for i in x],tv,w,color=TEAL,label="TV (CoT)")
ax.set_xticks(list(x)); ax.set_xticklabels([SHORT[m] for m in ms]); ax.set_ylim(0,100)
ax.set_ylabel("Core pass rate (%)   n=5"); ax.set_title("BV vs TV: CoT has no significant effect")
ax.legend(loc="upper right")
for s in ["top","right"]: ax.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig(os.path.join(HERE,"fig_bvtv.pdf"))

# ---- 4. Failure modes ----
fig,ax=plt.subplots(figsize=(6.0,4.6))
ax.pie([exec_share,fid_share],
       labels=[f"Exec / API\nerror\n{exec_share:.0f}%",f"Fidelity\n(wrong circuit)\n{fid_share:.0f}%"],
       colors=[CORAL,DKNAVY],startangle=90,counterclock=False,
       textprops={"color":NAVY,"fontweight":"bold","fontsize":12},
       wedgeprops={"edgecolor":"white","linewidth":2})
ax.set_title(f"Failure Modes ({n_fail} failures, n=1 full)")
fig.tight_layout(); fig.savefig(os.path.join(HERE,"fig_failmodes.pdf"))
print("wrote 4 PDFs")
