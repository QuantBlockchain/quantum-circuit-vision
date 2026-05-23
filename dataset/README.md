# QCV-Dataset

**132 Quantum Circuits · 5 Core Modalities · 792 Experiment Results · Bilingual Annotations**

The first multimodal quantum circuit dataset for training and evaluating AI systems on quantum circuit understanding, code generation, and verification.

## Structure

```
dataset/
├── circuits/            132 circuit diagram images (PNG, Qiskit-generated)
├── braket_code/         132 executable ground truth code (Amazon Braket SDK, .py)
├── simulations/         132 simulation results (JSON, state vectors from LocalSimulator)
├── annotations/         132 structured annotations (JSON, bilingual EN/CN, + experiment results)
├── failures/            annotated failure cases + summary (JSON)
├── qiskit_code/         132 Qiskit implementations (.py)
├── targets/             132 target descriptions (JSON)
├── equivalences/         12 circuit equivalence pairs (JSON)
├── experiment_results/  792 raw model outputs + verification CSV
├── statistics.json      dataset and experiment statistics
└── README.md            this file
```

## Quick Load

```python
from scripts.load_dataset import load_dataset

dataset = load_dataset()  # returns list of 132 circuit entries

# Each entry:
# {
#   "id": "C01_deutsch_jozsa_3",
#   "image_path": "dataset/circuits/C01_deutsch_jozsa_3.png",
#   "code_path": "dataset/ground_truth/C01_deutsch_jozsa_3.py",
#   "code": "from braket.circuits import Circuit\n...",
#   "annotation": { ... },
#   "result": { ... }
# }
```

## Data Format

### circuits/ (PNG)
- Generated with Qiskit `QuantumCircuit.draw("mpl", style="iqp")`
- 150 DPI, tight bounding box
- 1–10 qubits, varying widths

### ground_truth/ (.py)
- Amazon Braket SDK Python code
- Each file defines a `circuit` variable of type `braket.circuits.Circuit`
- All verified executable on LocalSimulator

### results/ (JSON)
```json
{
  "id": "C01_deutsch_jozsa_3",
  "qubits": 3,
  "depth": 5,
  "state_vector_real": [0.0, 0.0, ...],
  "state_vector_imag": [0.0, 0.0, ...],
  "state_vector_dim": 8,
  "nonzero_amplitudes": 2
}
```

### annotations/ (JSON)
```json
{
  "id": "C01_deutsch_jozsa_3",
  "category": "classical_algorithms",
  "difficulty": "advanced",
  "qubits": 3,
  "depth": 5,
  "description_en": "Deutsch-Jozsa algorithm (2-bit): constant vs balanced",
  "description_cn": "Deutsch-Jozsa算法（2比特）：常数vs平衡",
  "blockchain_relevance": null,
  "state_vector_dim": 8,
  "nonzero_amplitudes": 2
}
```

### failures/ (JSON)
```json
{
  "id": "failure_001",
  "model": "haiku-4.5",
  "mode": "bv",
  "circuit": "demo_05_toffoli",
  "error_type": "api_error",
  "fidelity": null,
  "error_detail": "'Circuit' object has no attribute 'toffoli'"
}
```

## Categories (13)

| ID | Category | Count | Qubits |
|:---|:---|:---:|:---:|
| demo | Basic Gates | 5 | 1–3 |
| inter | Intermediate | 10 | 2–4 |
| adv | Advanced Algorithms | 6 | 3–5 |
| blockchain | Blockchain Protocols | 11 | 2–8 |
| A | Gate Type Coverage | 15 | 1–3 |
| B | Qubit Scaling | 12 | 4–10 |
| C | Classical Algorithms | 15 | 2–4 |
| D | Variational/Parameterized | 10 | 2–4 |
| E | Error Correction | 8 | 3–9 |
| F | Quantum ML | 10 | 2–8 |
| G | Blockchain Extended | 8 | 3–6 |
| H | Visual Variants | 10 | 2–4 |
| I | BTC/Blockchain Security | 12 | 4–7 |

## Statistics

- Total circuits: 132
- Qubit range: 1–10
- Depth range: 1–27
- Blockchain-relevant: 31 (23.5%)
- Failure cases: 27 (from 126 MMLLM experiments)

## License

MIT — see [LICENSE](../LICENSE)

## Experiment Results (April 2026)

We evaluated 3 models × 2 prompting modes × 132 circuits = **792 invocations**.

| Model | BV | TV |
|:---|:---:|:---:|
| Claude Opus 4.6 | **78%** | 75% |
| Claude Sonnet 4.6 | **77%** | 75% |
| Claude Haiku 4.5 | 43% | **46%** |

- **45 circuits** passed all 6 model–mode combinations
- **18 circuits** failed all 6 combinations
- Verification: unitary matrix fidelity ≥ 0.99 on Braket LocalSimulator

### Loading Experiment Results

```python
from scripts.load_dataset import load_dataset

dataset = load_dataset()
for entry in dataset:
    ann = entry["annotation"]
    if "experiment_results" in ann:
        opus_bv = ann["experiment_results"]["claude-opus-4.6"]["bv"]
        print(f"{entry['id']}: pass={opus_bv['pass']}, fidelity={opus_bv['fidelity']}")
```

### Raw Model Outputs

The `experiment_results/` directory contains:
- `verification_results.csv` — 792-row summary (circuit, model, mode, pass, fidelity, error)
- `raw/` — original model outputs from `kiro-cli` non-interactive mode

### Key Findings

1. **Structural complexity, not qubit count, determines success.** 8-qubit regular circuits pass; 5-qubit irregular circuits fail.
2. **Chain-of-thought (TV) provides no benefit for strong models** (Δ = −3 to −4) but modest improvement for the weakest model (Δ = +5).
3. **18 "impossible" circuits** are predominantly complex algorithms (Shor, HHL, QAOA), error correction (surface code), and cryptographic protocols.

## Cost Analysis

| Model | Tier | Credits/call | Time | Pass% (BV) | Credits/correct |
|:---|:---:|:---:|:---:|:---:|:---:|
| Opus 4.6 | 2.20× | 0.618 | 24.4s | 78% | 0.778 |
| Sonnet 4.6 | 1.30× | 0.110 | 6.0s | 77% | **0.142** |
| Haiku 4.5 | 0.40× | 0.031 | 3.7s | 43% | 0.072 |

Sonnet achieves Pareto-optimal cost-accuracy: same pass rate as Opus at 18% of the cost.

See `experiment_results/cost_analysis.csv` for per-invocation data.

## Citation

```bibtex
@misc{liu2026qcv,
  title={QCV: Cost-Aware Evaluation of Visual AI Agents for Quantum Code Generation},
  author={Liu, Dongping and Zhang, Aoyu and Zhang, Luyao},
  year={2026},
  url={https://github.com/QuantBlockchain/quantum-circuit-vision}
}
```

## Documentation

- [DATASHEET.md](../DATASHEET.md) — Dataset documentation following Gebru et al. (2021)
- [CITATION.cff](../CITATION.cff) — Machine-readable citation metadata
