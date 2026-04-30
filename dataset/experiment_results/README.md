# Experiment Results

792 model invocations: 132 circuits × 3 models × 2 prompting modes.

## Files

- `verification_results.csv` — Summary: circuit_name, model, mode, syntax_ok, exec_ok, fidelity, pass, error
- `raw/` — Original model outputs from `kiro-cli chat --no-interactive`

## Models

| Model | Credits | Pass Rate (BV) | Pass Rate (TV) |
|:---|:---:|:---:|:---:|
| claude-opus-4.6 | 2.20× | 78% | 75% |
| claude-sonnet-4.6 | 1.30× | 77% | 75% |
| claude-haiku-4.5 | 0.40× | 43% | 46% |

## Verification

- Metric: unitary matrix fidelity ≥ 0.99
- Simulator: Amazon Braket LocalSimulator (shots=0, state vector)
- Date: 2026-04-30

## Raw File Naming

`{model}_{mode}_{circuit_name}_raw.txt`

Example: `claude-opus-4.6_bv_A01_single_y_raw.txt`

Note: Raw files contain ANSI escape codes from terminal output. Clean with:
```python
import re
clean = re.sub(r'\x1b\[[\d;?]*[a-zA-Z]', '', raw_text)
```
