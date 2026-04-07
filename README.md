# QCV: Quantum Circuit Vision

**Quantum Circuit Code Generation using Visual Capabilities of Multi-Modal Large Language Models**

QCV investigates whether multimodal large language models (MMLLMs) can generate executable quantum code directly from circuit diagram images. We construct a difficulty-graded benchmark of **120 quantum circuits** across 12 categories and evaluate multiple MMLLMs under two visual prompting modes: Basic Vision (BV) and Thinking Vision (TV).

## Key Findings

- **Claude Opus 4.6** achieves a **97.0% weighted score** under BV (20/21 pass on main benchmark)
- **CoT Sensitivity Window**: Chain-of-thought (TV) only helps near a model's capability boundary — it improves weaker models on simpler tasks but *degrades* performance on advanced circuits (−17pp)
- **Structural regularity > qubit count**: An 8-qubit regular circuit passes while 5-qubit and 7-qubit irregular circuits fail
- All generated code is verified end-to-end using **unitary matrix fidelity** on Amazon Braket's LocalSimulator

## Benchmark

120 quantum circuits across 12 categories:

| Category | ID | Count | Qubits | Examples |
|---|---|---|---|---|
| Basic | demo | 5 | 1–3 | Hadamard, CNOT, Bell, GHZ, Toffoli |
| Intermediate | inter | 10 | 2–4 | QFT, Grover, Teleportation, Deutsch, Phase Estimation |
| Advanced | adv | 6 | 3–5 | 3-Qubit QFT, QAOA, VQE Ansatz, Bernstein-Vazirani |
| Blockchain | blockchain | 11 | 2–8 | QRNG, BB84 QKD, Grover Mining, Consensus Protocol |
| Gate Coverage | A | 15 | 1–3 | Y, S, T, Rx, Ry, Rz, √X, CZ, CRy, CRx, CCZ, iSWAP |
| Qubit Scaling | B | 12 | 4–10 | GHZ-4/5/6/8/10, QFT-4/5, Ring/Star/Full Entanglement |
| Classical Algorithms | C | 15 | 2–4 | Deutsch-Jozsa, Simon, Grover-4, Shor, QPE, HHL, W-state |
| Variational | D | 10 | 2–4 | Hardware-efficient, UCCSD, QAOA-2layer, Data Reuploading |
| Error Correction | E | 8 | 3–9 | Bit/Phase Flip, Shor-9, Steane-7, Surface Code, Logical CNOT |
| Quantum ML | F | 10 | 2–8 | Angle/IQP Encoding, QNN, QCNN, Kernel, QGAN, Classifier |
| Blockchain Extended | G | 8 | 3–6 | E91 QKD, Quantum Money, Blind QC, Voting, Auction |
| Visual Variants | H | 10 | 2–4 | Barrier, Compressed, Wide, Reversed Labels, Decomposed |

Each circuit includes:
- Circuit diagram image (PNG) in `benchmark/`
- Ground truth Amazon Braket SDK code in `benchmark/ground_truth/`

## Results Summary

### Main Benchmark (21 circuits × 3 models × 2 modes)

| Model | Mode | Basic (5) | Intermediate (10) | Advanced (6) | Weighted Score |
|---|---|---|---|---|---|
| Claude Opus 4.6 | BV | 100% | 90% | 100% | **97.0%** |
| Claude Opus 4.6 | TV | 100% | 100% | 83% | 91.5% |
| Claude Sonnet 4.6 | BV | 100% | 90% | 83% | 88.5% |
| Claude Sonnet 4.6 | TV | 100% | 90% | 83% | 88.5% |
| Claude Haiku 4.5 | BV | 60% | 60% | 33% | 46.5% |
| Claude Haiku 4.5 | TV | 80% | 70% | 16% | 45.0% |

Weighted score = 0.2 × Basic + 0.3 × Intermediate + 0.5 × Advanced

### Blockchain Extension (11 circuits, Opus BV)

Pass rate: **9/11 (81.8%)** — including an 8-qubit consensus protocol (256×256 unitary verified)

## Repository Structure

```
quantum-circuit-vision/
├── benchmark/                  # Circuit diagram images (PNG)
│   └── ground_truth/           # Ground truth Braket SDK code
├── prompts/                    # BV and TV prompt templates
├── scripts/                    # Circuit generation, experiment, and verification scripts
├── results/                    # Aggregated experiment results
├── requirements.txt
└── LICENSE
```

## Quick Start

### Install dependencies

```bash
pip install -r requirements.txt
```

### Generate circuit diagrams

```bash
python scripts/generate_circuits.py        # Basic (5 circuits)
python scripts/generate_intermediate.py    # Intermediate (10 circuits)
python scripts/generate_advanced.py        # Advanced (6 circuits)
```

### Verify a generated code file

```bash
python scripts/verify.py demo_03_bell path/to/generated_code.py
```

## Prompting Modes

**Basic Vision (BV):** Provide the circuit image with a direct code generation instruction.

**Thinking Vision (TV):** Ask the model to first analyze the circuit structure (qubit count, gate sequence, control relationships), then generate code based on its analysis.

See `prompts/prompts.txt` for the exact templates.

## Verification Pipeline

1. **Syntax check** — Python `compile()`
2. **Execution check** — Run in sandboxed namespace, verify a valid Braket `Circuit` object is produced
3. **Unitary fidelity** — Compute full unitary matrices for generated and ground truth circuits on LocalSimulator; pass if fidelity ≥ 0.99

## Citation

```bibtex
@inproceedings{liu2026qcv,
  title={QCV: Quantum Circuit Code Generation using Visual Capabilities of Multi-Modal Large Language Models},
  author={Liu, Dongping and Zhang, Aoyu and Zhang, Luyao},
  year={2026}
}
```

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.
