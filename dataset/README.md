# QCV-Dataset

**132 Quantum Circuits · 5 Modalities · Bilingual Annotations**

The first multimodal quantum circuit dataset for training and evaluating AI systems on quantum circuit understanding, code generation, and verification.

## Structure

```
dataset/
├── circuits/        132 circuit diagram images (PNG, Qiskit-generated)
├── ground_truth/    132 executable ground truth code (Amazon Braket SDK, .py)
├── results/         132 simulation results (JSON, state vectors from LocalSimulator)
├── annotations/     132 structured annotations (JSON, bilingual EN/CN)
└── failures/         27 annotated failure cases + summary (JSON)
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
