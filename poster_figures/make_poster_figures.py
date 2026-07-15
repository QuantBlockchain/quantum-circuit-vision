"""
Reproduce the four QCV poster analysis figures with Matplotlib.
These charts are not in the paper LaTeX (results there are tables); they were
made for the poster from the paper's reported numbers. Values below are the
paper's published aggregates (core n=5 pass rates, per-call credits, difficulty
tiers, failure taxonomy), hard-coded with sources so the figures are reproducible
and match the poster exactly.

Sources:
  core n=5 pass rates & per-call credits -> paper Table (full-benchmark) & cost table
  difficulty tiers (Opus BV, full n=1)    -> paper difficulty gradient
  failure taxonomy (267 failures)         -> paper failure analysis
Run: python make_poster_figures.py   ->  writes fig_pareto/difficulty/bvtv/failmodes.pdf
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---- palette (matches poster) ----
NAVY   = "#0B3D91"   # titles / labels
DKNAVY = "#08306B"   # BV bars, fidelity slice
BLUE   = "#356AA0"   # Opus point
TEAL   = "#2CA089"   # Sonnet / TV / basic
CORAL  = "#E1634A"   # Haiku / advanced / exec-error

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 12,
    "axes.titlesize": 15, "axes.titleweight": "bold", "axes.titlecolor": NAVY,
    "axes.edgecolor": "#333333",
})

OUT = "."

# ---- data (paper's published numbers) ----
# core n=5 pass rate (%)   BV, TV
CORE = {"Sonnet": (91.4, 88.6), "Opus": (85.7, 81.9), "Haiku": (48.6, 53.3)}
CREDITS = {"Haiku": 0.031, "Sonnet": 0.110, "Opus": 0.618}      # credits per call
DIFF = [("Basic", 93, TEAL), ("Intermediate", 81, DKNAVY), ("Advanced", 70, CORAL)]
FAIL = [("Exec / API\nerror\n31%", 31, CORAL), ("Fidelity\n(wrong circuit)\n69%", 69, DKNAVY)]  # Exec first -> upper-right, matches poster

# ---- 1. Pareto frontier ----
def pareto():
    fig, ax = plt.subplots(figsize=(6.2, 4.3))
    pts = {"Haiku": (CREDITS["Haiku"], CORE["Haiku"][0], CORAL),
           "Sonnet": (CREDITS["Sonnet"], CORE["Sonnet"][0], TEAL),
           "Opus": (CREDITS["Opus"], CORE["Opus"][0], BLUE)}
    order = ["Haiku", "Sonnet", "Opus"]
    ax.plot([pts[m][0] for m in order], [pts[m][1] for m in order],
            "--", color="#9A9A9A", lw=1.6, zorder=1, label="Pareto frontier")
    for m in order:
        x, y, c = pts[m]
        ax.scatter(x, y, s=1300, c=c, edgecolors=NAVY, linewidths=2.2, zorder=3)
        dy = 6 if m != "Opus" else 4
        ax.annotate(m, (x, y), xytext=(0, 24), textcoords="offset points",
                    ha="center", color=NAVY, fontweight="bold", fontsize=14)
    ax.set_xscale("log")
    ax.set_xlabel("Cost per call (credits, log)")
    ax.set_ylabel("Core pass rate (%)   n=5 BV")
    ax.set_title("Cost-Accuracy Pareto Frontier")
    ax.set_ylim(40, 100)
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(loc="lower right", fontsize=10)
    fig.tight_layout(); fig.savefig(f"{OUT}/fig_pareto.pdf")

# ---- 2. Difficulty gradient ----
def difficulty():
    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    labels = [d[0] for d in DIFF][::-1]
    vals = [d[1] for d in DIFF][::-1]
    cols = [d[2] for d in DIFF][::-1]
    y = range(len(labels))
    ax.barh(y, vals, color=cols, edgecolor="white")
    for yi, v in zip(y, vals):
        ax.text(v + 1.5, yi, f"{v}%", va="center", color=NAVY, fontweight="bold", fontsize=14)
    ax.set_yticks(list(y)); ax.set_yticklabels(labels)
    ax.set_xlim(0, 100); ax.set_xlabel("Opus BV pass rate (%)")
    ax.set_title("Difficulty gradient (n=1 full)")
    for s in ["top", "right"]: ax.spines[s].set_visible(False)
    fig.tight_layout(); fig.savefig(f"{OUT}/fig_difficulty.pdf")

# ---- 3. BV vs TV grouped bars ----
def bvtv():
    fig, ax = plt.subplots(figsize=(6.4, 4.3))
    models = ["Sonnet", "Opus", "Haiku"]
    bv = [CORE[m][0] for m in models]; tv = [CORE[m][1] for m in models]
    x = range(len(models)); w = 0.38
    ax.bar([i - w/2 for i in x], bv, w, color=DKNAVY, label="BV")
    ax.bar([i + w/2 for i in x], tv, w, color=TEAL, label="TV (CoT)")
    ax.set_xticks(list(x)); ax.set_xticklabels(models)
    ax.set_ylim(0, 100); ax.set_ylabel("Core pass rate (%)   n=5")
    ax.set_title("BV vs TV: CoT has no significant effect")
    ax.legend(loc="upper right")
    for s in ["top", "right"]: ax.spines[s].set_visible(False)
    fig.tight_layout(); fig.savefig(f"{OUT}/fig_bvtv.pdf")

# ---- 4. Failure modes pie ----
def failmodes():
    fig, ax = plt.subplots(figsize=(6.0, 4.6))
    labels = [f[0] for f in FAIL]; sizes = [f[1] for f in FAIL]; cols = [f[2] for f in FAIL]
    ax.pie(sizes, labels=labels, colors=cols, startangle=90, counterclock=False,
           textprops={"color": NAVY, "fontweight": "bold", "fontsize": 12},
           wedgeprops={"edgecolor": "white", "linewidth": 2})
    ax.set_title("Failure Modes (267 failures, n=1 full)")
    fig.tight_layout(); fig.savefig(f"{OUT}/fig_failmodes.pdf")

if __name__ == "__main__":
    pareto(); difficulty(); bvtv(); failmodes()
    print("wrote fig_pareto.pdf, fig_difficulty.pdf, fig_bvtv.pdf, fig_failmodes.pdf")
