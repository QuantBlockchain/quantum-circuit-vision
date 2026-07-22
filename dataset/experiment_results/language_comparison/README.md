# Prompt-Language Comparison (Chinese vs English)

**Question.** The main QCV experiments used Chinese prompts (see `prompts/`). Prior
work shows prompt language can affect LLM outputs (Behzad et al., 2024). Does it
here?

**Design.** Core 21 circuits x 3 Claude models x BV mode x n=5 x {Chinese, English}.
The two languages were run **fresh and interleaved per circuit** (Chinese and
English for the same image seconds apart) on the **same current model**, so the
comparison isolates prompt language from model drift. The English prompt is a
faithful, word-for-word translation of the Chinese one (only the language differs).
Verification is identical to the main pipeline (unitary fidelity F>=0.99).

**Result (BV, core, n=5; 315 calls per language).**

| model | Chinese | English | Δ (EN−CN) |
|---|---|---|---|
| Opus   | 53.3% | 77.1% | **+23.8pp** |
| Sonnet | 90.5% | 88.6% | −1.9pp |
| Haiku  | 39.0% | 37.1% | −1.9pp |
| **all**| 61.0% | 67.6% | **+6.7pp** |

Paired test (circuit x model, N=63): mean Δ = +6.7pp; paired t p=0.075, Wilcoxon
p=0.087 (not significant at α=0.05).

**Conclusion.** Prompt-language sensitivity is **model-specific**. English gives a
modest, marginally-significant overall gain (+6.7pp), driven almost entirely by
**Opus (+23.8pp)**; Sonnet and Haiku are essentially language-invariant (±2pp).
Results for language-sensitive models should therefore be read with the prompt
language in mind.

**Note on absolute values.** The Chinese pass rates here are from the *current*
model and are lower than the paper's core numbers (which were collected on an
earlier model version); that gap reflects model drift, a separate phenomenon. The
Chinese-vs-English contrast here is drift-controlled (both arms run back-to-back on
the same current model).

**Files.**
- `lang_compare_verification.csv` — per-run pass/fidelity (lang, model, circuit, run).
- `run_lang_compare.sh` — server runner (630 calls, interleaved, skip-existing).
- `lang_verify_compare.py` — verification + comparison (reproduces the table above).
