# QCV: Quantum Circuit Vision

**Quantum Circuit Code Generation using Visual Capabilities of Multi-Modal Large Language Models**

QCV investigates whether multimodal large language models (MMLLMs) can generate executable quantum code directly from circuit diagram images. We construct a difficulty-graded benchmark of **132 quantum circuits** across 13 categories and evaluate multiple MMLLMs under two visual prompting modes: Basic Vision (BV) and Thinking Vision (TV).

## Key Findings

- **Claude Opus 4.6** achieves a **97.0% weighted score** under BV (20/21 pass on main benchmark)
- **CoT Sensitivity Window**: Chain-of-thought (TV) only helps near a model's capability boundary — it improves weaker models on simpler tasks but *degrades* performance on advanced circuits (−17pp)
- **Structural regularity > qubit count**: An 8-qubit regular circuit passes while 5-qubit and 7-qubit irregular circuits fail
- All generated code is verified end-to-end using **unitary matrix fidelity** on Amazon Braket's LocalSimulator

## Benchmark Overview

### 132 Circuits · 13 Categories · 1–10 Qubits

| Category | ID | Count | Qubits | Status | Examples |
|:---|:---:|:---:|:---:|:---:|:---|
| Basic | demo | 5 | 1–3 | ✅ Tested | Hadamard, CNOT, Bell, GHZ, Toffoli |
| Intermediate | inter | 10 | 2–4 | ✅ Tested | QFT, Grover, Teleportation, Deutsch, Phase Est. |
| Advanced | adv | 6 | 3–5 | ✅ Tested | 3-Qubit QFT, QAOA, VQE Ansatz, Bernstein-Vazirani |
| Blockchain | blockchain | 11 | 2–8 | 🔶 Partial | QRNG, BB84 QKD, Grover Mining, Consensus Protocol |
| Gate Coverage | A | 15 | 1–3 | ⬜ Pending | Y, S, T, Rx, Ry, Rz, √X, CZ, CRy, CRx, CCZ, iSWAP |
| Qubit Scaling | B | 12 | 4–10 | ⬜ Pending | GHZ 4–10q, QFT 4–5q, Ring/Star/Full Entanglement |
| Classical Algorithms | C | 15 | 2–4 | ⬜ Pending | Deutsch-Jozsa, Simon, Grover-4, Shor, QPE, HHL |
| Variational | D | 10 | 2–4 | ⬜ Pending | Hardware-efficient, UCCSD, QAOA-2layer, Data Reuploading |
| Error Correction | E | 8 | 3–9 | ⬜ Pending | Bit/Phase Flip, Shor-9, Steane-7, Surface Code |
| Quantum ML | F | 10 | 2–8 | ⬜ Pending | QNN, QCNN-8q, Quantum Kernel, QGAN, Classifier |
| Blockchain Extended | G | 8 | 3–6 | ⬜ Pending | E91 QKD, Quantum Money, Blind QC, Voting, Auction |
| Visual Variants | H | 10 | 2–4 | ⬜ Pending | Barrier, Compressed, Reversed Labels, Decomposed |
| **BTC/Blockchain Security** | **I** | **12** | **4–7** | ⬜ Pending | **Shor vs ECDSA, Grover vs SHA-256/AES, Kyber, Dilithium, SPHINCS+** |

> ✅ = 3 models × 2 modes tested · 🔶 = Opus BV only · ⬜ = Circuit + ground truth ready, experiments pending

### BTC/Blockchain Quantum Security (Direction I) — Detail

Circuits directly relevant to Bitcoin and blockchain quantum security:

| ID | Circuit | Qubits | Theme | Description |
|:---|:---|:---:|:---|:---|
| I01 | Shor vs ECDSA | 6 | 🔴 Attack | Period finding targeting elliptic curve (secp256k1 threat) |
| I02 | Grover vs SHA-256 | 4 | 🔴 Attack | Preimage search on hash function (mining/address threat) |
| I03 | Grover vs AES | 5 | 🔴 Attack | Key search on symmetric encryption (AES-128 → AES-64 effective) |
| I10 | PoW Quantum Speedup | 4 | 🔴 Attack | Quadratic speedup on proof-of-work nonce search |
| I04 | Lamport Signature | 4 | 🟢 Defense | One-time quantum-safe signature verification |
| I08 | Kyber (CRYSTALS) | 6 | 🟢 Defense | Lattice-based key encapsulation (NIST PQC standard) |
| I09 | Dilithium | 5 | 🟢 Defense | Lattice-based digital signature (NIST PQC standard) |
| I12 | SPHINCS+ | 7 | 🟢 Defense | Hash-based signature scheme (NIST PQC standard) |
| I05 | Quantum Random Beacon | 6 | 🔵 Infra | Multi-party randomness for consensus |
| I06 | QKD Network | 6 | 🔵 Infra | 3-node key distribution with entanglement swapping |
| I07 | Quantum Timestamp | 4 | 🔵 Infra | Unforgeable time proof for blockchain |
| I11 | Quantum Merkle Tree | 5 | 🔵 Infra | On-chain verification with quantum leaf hashing |

> 🔴 Attack surface · 🟢 Post-quantum defense · 🔵 Quantum-enhanced infrastructure

### Blockchain Coverage Summary

Total blockchain-related circuits: **31 / 132 (23.5%)**

| Group | Count | Focus |
|:---|:---:|:---|
| blockchain (original) | 11 | General quantum protocols for blockchain |
| G (extended) | 8 | Cryptographic protocols (QKD, voting, auction) |
| I (BTC security) | 12 | BTC-specific attack/defense/infrastructure |

## Results (Evaluated Subset: 21 Main + 11 Blockchain)

### Main Benchmark (21 circuits × 3 models × 2 modes)

| Model | Mode | Basic (5) | Intermediate (10) | Advanced (6) | Weighted Score |
|:---|:---:|:---:|:---:|:---:|:---:|
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
├── benchmark/                  # 132 circuit diagram images (PNG)
│   └── ground_truth/           # 132 ground truth Braket SDK code (.py)
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
