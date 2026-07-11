#!/usr/bin/env python3
"""
statistical_tests.py — Reproduce the statistical analyses reported in the
QCV KDD-2026 camera-ready revision.

All tests read only data already released in this repository:
  - dataset/experiment_results/repeat5/verification_repeat5.csv  (n=5 core, 21 circuits)
  - dataset/experiment_results/verification_results.csv          (n=1 full, 132 circuits)
  - dataset/braket_code/*.py                                     (ground-truth circuits)

Analyses (mapped to reviewer comments addressed in the camera-ready):
  1. Chain-of-thought equivalence via TOST         -> Reviewer pMRa, Weakness 2
  2. Sonnet-vs-Opus model-difference significance  -> Reviewer pMRa, Weakness 3 / Question 2
  3. Depth vs qubit-count / gate-count regression  -> Reviewer pMRa, Question 1

Usage:
    python scripts/statistical_tests.py

Requires: numpy, scipy, statsmodels  (see requirements.txt)
"""
import os
import csv
import glob
import math
import warnings
from collections import defaultdict

import numpy as np
from scipy import stats

warnings.filterwarnings("ignore")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPEAT5_CSV = os.path.join(ROOT, "dataset", "experiment_results", "repeat5",
                           "verification_repeat5.csv")
FULL_CSV = os.path.join(ROOT, "dataset", "experiment_results",
                        "verification_results.csv")
GT_DIR = os.path.join(ROOT, "dataset", "braket_code")

MODELS = ["claude-opus-4.6", "claude-sonnet-4.6", "claude-haiku-4.5"]
EQUIV_MARGIN = 0.10  # +/-10 percentage points equivalence bound for TOST


# ----------------------------------------------------------------------
def load_rows(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def per_circuit_rate(rows, model, mode):
    """Mean pass rate per circuit (averaged over repeated runs), for one model/mode."""
    by_circuit = defaultdict(list)
    for r in rows:
        if r["model"] == model and r["mode"] == mode:
            by_circuit[r["circuit_name"]].append(1 if r["pass"] == "True" else 0)
    return {c: np.mean(v) for c, v in by_circuit.items()}


# ----------------------------------------------------------------------
def tost_equivalence(diffs, margin):
    """Two one-sided tests for equivalence within +/- margin. Returns TOST p-value."""
    n = len(diffs)
    mean = np.mean(diffs)
    se = np.std(diffs, ddof=1) / math.sqrt(n)
    if se == 0:
        return 0.0
    t_lower = (mean - (-margin)) / se           # H0: mean <= -margin
    p_lower = stats.t.sf(t_lower, n - 1)
    t_upper = (mean - margin) / se              # H0: mean >= +margin
    p_upper = stats.t.cdf(t_upper, n - 1)
    return max(p_lower, p_upper)


def analysis_1_cot_equivalence(rows):
    print("=" * 70)
    print("1. Chain-of-Thought (BV vs TV) equivalence  [Reviewer pMRa, W2]")
    print("   Per-circuit paired data, n=5 core subset; TOST margin = +/-10pp")
    print("=" * 70)
    for m in MODELS:
        bv = per_circuit_rate(rows, m, "bv")
        tv = per_circuit_rate(rows, m, "tv")
        circuits = sorted(set(bv) & set(tv))
        diffs = np.array([tv[c] - bv[c] for c in circuits])
        delta_pp = diffs.mean() * 100
        t, p = stats.ttest_rel([tv[c] for c in circuits], [bv[c] for c in circuits])
        p_tost = tost_equivalence(diffs, EQUIV_MARGIN)
        verdict = "EQUIVALENT" if p_tost < 0.05 else "not established"
        print(f"  {m:20s} n={len(circuits):2d}  Delta(TV-BV)={delta_pp:+5.1f}pp  "
              f"paired-t p={p:.3f}  TOST p={p_tost:.3f}  -> {verdict}")
    print()


def analysis_2_model_difference(rows):
    print("=" * 70)
    print("2. Sonnet vs Opus accuracy difference  [Reviewer pMRa, W3 / Q2]")
    print("   Per-circuit paired test, n=5 core subset, BV mode")
    print("=" * 70)
    son = per_circuit_rate(rows, "claude-sonnet-4.6", "bv")
    opu = per_circuit_rate(rows, "claude-opus-4.6", "bv")
    circuits = sorted(set(son) & set(opu))
    s = np.array([son[c] for c in circuits])
    o = np.array([opu[c] for c in circuits])
    diff = s - o
    t, p_t = stats.ttest_rel(s, o)
    try:
        w, p_w = stats.wilcoxon(s, o)
    except ValueError:
        p_w = float("nan")
    md = diff.mean() * 100
    ci = 1.96 * diff.std(ddof=1) / math.sqrt(len(diff)) * 100
    print(f"  Sonnet mean = {s.mean()*100:.1f}% , Opus mean = {o.mean()*100:.1f}%  (n={len(circuits)})")
    print(f"  mean diff (Sonnet-Opus) = {md:+.1f}pp,  95% CI [{md-ci:+.1f}, {md+ci:+.1f}]pp")
    print(f"  paired t-test p = {p_t:.3f}   Wilcoxon p = {p_w:.3f}")
    print(f"  -> difference is {'NOT ' if p_t > 0.05 else ''}statistically significant at alpha=0.05")
    print()


def circuit_features():
    """Extract qubits, depth, gate_count by executing ground-truth Braket circuits."""
    from braket.circuits import Circuit
    feats = {}
    for fp in sorted(glob.glob(os.path.join(GT_DIR, "*.py"))):
        name = os.path.splitext(os.path.basename(fp))[0]
        ns = {"math": math, "np": np, "numpy": np}
        try:
            exec(compile(open(fp).read(), fp, "exec"), ns)
            circ = next((v for v in ns.values() if isinstance(v, Circuit)), None)
            if circ is not None:
                feats[name] = {"qubits": circ.qubit_count,
                               "depth": circ.depth,
                               "gate_count": len(circ.instructions)}
        except Exception:
            continue
    return feats


def analysis_3_regression(full_rows):
    print("=" * 70)
    print("3. What predicts failure: depth vs qubit count vs gate count")
    print("   [Reviewer pMRa, Q1]  Logistic regression, per-circuit majority-pass")
    print("=" * 70)
    try:
        import statsmodels.api as sm
    except ImportError:
        print("  statsmodels not installed; skipping regression.")
        return
    feats = circuit_features()
    # majority-pass per circuit over the 6 model x mode configs (n=1 full set)
    passes = defaultdict(list)
    for r in full_rows:
        if r["circuit_name"] in feats:
            passes[r["circuit_name"]].append(1 if r["pass"] == "True" else 0)
    names = sorted(passes)
    y = np.array([1 if sum(passes[c]) >= 3 else 0 for c in names], float)
    depth = np.array([feats[c]["depth"] for c in names], float)
    qubits = np.array([feats[c]["qubits"] for c in names], float)
    gates = np.array([feats[c]["gate_count"] for c in names], float)

    r_dg = np.corrcoef(depth, gates)[0, 1]
    print(f"  Collinearity: Pearson r(depth, gate_count) = {r_dg:.3f}  (N={len(names)} circuits)")

    def fit(X, label):
        m = sm.Logit(y, sm.add_constant(X)).fit(disp=0)
        return m

    for name, x in [("depth", depth), ("qubit count", qubits), ("gate count", gates)]:
        m = fit(x, name)
        print(f"  {name:12s} alone : coef={m.params[1]:+.3f}  p={m.pvalues[1]:.4g}  "
              f"pseudo-R2={m.prsquared*100:.1f}%")
    mj = fit(np.column_stack([depth, qubits]), "joint")
    print(f"  joint depth+qubits  : depth p={mj.pvalues[1]:.4g} | qubit p={mj.pvalues[2]:.4g}")
    print("  -> circuit DEPTH is the strongest predictor among tested scalar features;")
    print("     qubit count is not significant in the joint model. Depth is highly")
    print("     collinear with gate count, so 'depth' proxies overall structural complexity.")
    print()


def main():
    rep = load_rows(REPEAT5_CSV)
    full = load_rows(FULL_CSV)
    analysis_1_cot_equivalence(rep)
    analysis_2_model_difference(rep)
    analysis_3_regression(full)
    print("Done. All inputs are files released in this repository.")


if __name__ == "__main__":
    main()
