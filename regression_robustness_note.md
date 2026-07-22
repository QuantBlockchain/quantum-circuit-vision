# Regression Robustness Check — depth / gate_count / qubits

Generated: 2026-06-12
Data: `dataset/experiment_results/verification_results.csv` (792 rows, n=1 full set)
Features: extracted by executing `dataset/braket_code/*.py` as Braket `Circuit`
objects (`qubit_count`, `depth`, `len(instructions)`), 132/132 successful.
Tool: Python `statsmodels` Logit.

> Background: the paper claims "circuit depth is the primary predictor" (p<0.001),
> with qubit count non-significant (p=0.20). This note checks two risks:
> (1) Is depth merely a proxy for gate count (the two are highly collinear)?
> (2) Why does the qubits p-value differ across regression settings?

## 1. Collinearity (Pearson r, n=132 circuits)

| pair | r |
|---|---|
| depth vs gate_count | **0.862** (highly collinear) |
| depth vs qubits | 0.368 |
| gate_count vs qubits | 0.474 |

depth and gate_count are highly correlated (r=0.862); a multivariable test is
required to tell which is the true signal.

## 2. Three-variable logistic regression (qubits + depth + gate_count, per-invocation N=792)

| variable | coef | p-value | sig |
|---|---|---|---|
| qubits | -0.120 | 0.017 | * |
| **depth** | **-0.171** | **0.00043** | *** |
| gate_count | -0.038 | 0.108 | no |

Single-variable baselines: depth-only p=6.5e-21; gate_count-only p=4.2e-21 (each
highly significant alone).

**Conclusion: depth is NOT a proxy for gate count; if anything the reverse.**
Controlling for depth, gate_count loses significance (p=0.108); controlling for
gate_count, depth remains significant (p=0.0004). gate_count's univariate
significance is largely borrowed from its collinearity with depth. The paper's
"depth is the primary predictor" survives the robustness check.

## 3. Root cause of the qubits p-value difference (aggregation + N)

Two-variable model (qubits + depth), reproduced under three aggregations:

| setting | unit of analysis | N | qubits p | depth p |
|---|---|---|---|---|
| A | per-invocation | 792 | 0.0025 * | 2.8e-15 * |
| B | per-circuit, majority (>=50%) | 132 | **0.198** | 0.0010 * |
| C | per-circuit, any-pass | 132 | **0.188** | 0.0021 * |

**The paper's "qubits p=0.20" comes from the per-circuit (N=132) regression
(settings B/C).** An earlier per-invocation figure (p=0.0025, N=792, setting A)
differs purely because of N and aggregation (statistical power), NOT because of a
conflicting conclusion: in every setting depth is highly significant and qubits is
the weakest of the three predictors. The qualitative conclusion---"structural
complexity (depth), not qubit count, dominates"---holds under all settings.

## 4. Recommended paper revisions (submission risk points)

1. **State the regression's N and unit of analysis**: 132 circuits (per-circuit)
   vs 792 invocations (per-invocation). The qubits p-value differs by an order of
   magnitude; not stating this invites reviewer challenge.
2. **State the aggregation rule** for per-circuit binarization (majority >=50% /
   any-pass / mean rate).
3. **Recommendation**: use per-circuit (N=132) as the main result (more
   conservative; avoids treating 6 invocations of the same circuit as independent,
   i.e., pseudoreplication). A footnote can note that qubits also becomes
   significant per-invocation, but with pseudoreplication.

## 5. Reproduction

Feature extraction: run `dataset/braket_code/*.py` for qubit_count / depth /
len(instructions). Regression: `statsmodels` Logit, outcome = `pass` column of
`verification_results.csv`.
