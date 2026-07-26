# Cross-Vendor Evaluation (GPT-5.6)

**Question.** The main QCV results are Claude-only. Do they generalize to another
vendor?

**Design.** Core 21 circuits x 3 OpenAI GPT-5.6 models (Sol, Terra, Luna) x
{BV, TV} x {Chinese, English} x n=5 = 1260 runs. Chinese and English were run
interleaved per (circuit, mode) on the same current model (drift-controlled).
Verification is identical to the main pipeline (unitary fidelity F>=0.99). GPT TV
outputs wrap the circuit in `def main():`; the verifier was extended to lift such
code to module level before execution (see `gpt_verify_compare.py`).

**Pass rate (%), core n=5.**

| model | BV-cn | BV-en | TV-cn | TV-en |
|---|---|---|---|---|
| Sol   | 78.1 | 75.2 | 82.9 | 91.4 |
| Terra | 75.2 | 76.2 | 89.5 | 93.3 |
| Luna  | 81.9 | 78.1 | 56.2 | 88.6 |

**Findings.**
1. **Chain-of-thought (TV) helps GPT**: EN TV−BV = +16.2 (Sol), +17.1 (Terra),
   +10.5 (Luna) pp. This contrasts with Claude, where CoT shows no significant
   effect. CoT benefit is therefore **model-family-dependent**, not universal.
2. **Cross-vendor accuracy (EN, BV)**: GPT 75–78% is comparable to Claude Opus
   (77.1%), below Claude Sonnet (88.6%), and well above Claude Haiku (37.1%).
3. **Difficulty gradient holds** (GPT, EN BV, pooled): basic 100% -> intermediate
   75.3% -> advanced 58.9%. Structural difficulty determines success across vendors.
4. **Language sensitivity is low for GPT** (EN−CN BV: −2.9 / +1.0 / −3.8 pp),
   unlike Claude Opus (+23.8pp). The large language effect is Claude-Opus-specific.

**Note on absolute values.** Chinese/English pass rates here are from the current
model version, drift-controlled within this experiment; they are not directly
comparable to the paper's earlier-model core numbers.

**Files.**
- `gpt_verification.csv` — per-run pass/fidelity (circuit_name, model, mode, lang, run).
- `run_gpt_full.sh` — server runner (1260 calls, interleaved, skip-existing).
- `gpt_verify_compare.py` — verification + comparison (reproduces the tables above).
