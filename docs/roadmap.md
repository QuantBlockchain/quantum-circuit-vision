# QCV Dataset & Research Roadmap

## For Luyao — Status Update & Tonight's Plan
**Date:** 2026-04-29  
**From:** Dongping

---

## 1. Current State (What We Have)

| Component | Count | Status |
|:---|:---:|:---:|
| Circuit diagrams (PNG) | 132 | ✅ Done |
| Ground truth code (Braket .py) | 132 | ✅ Done |
| Simulation results (state vectors) | 132 | ✅ Done |
| Structured annotations (JSON) | 132 | ✅ Done |
| Failure cases (annotated) | 27 | ✅ Done |
| Multi-SDK (Qiskit/Cirq) | 0 | 📋 Planned |
| Circuit equivalence pairs | 0 | 📋 Planned |
| Optimization pairs | 0 | 📋 Planned |
| Target→Circuit pairs | 0 | 📋 Planned |

---

## 2. Tonight's Deliverables (April 29, before morning)

### 2a. Simulation Results for All 132 Circuits
- Run each ground truth on Braket LocalSimulator
- Save: state vector (|0...0⟩ input), full unitary matrix, circuit metadata
- Output format: `dataset/results/{circuit_name}.json`
- Fields: `state_vector`, `unitary_shape`, `circuit_depth`, `gate_count`, `qubit_count`

### 2b. Structured Annotations for All 132 Circuits
- Auto-generate + human-verify
- Output format: `dataset/annotations/{circuit_name}.json`
- Fields:
  ```json
  {
    "id": "C01_deutsch_jozsa_3",
    "name": "Deutsch-Jozsa Algorithm (2-bit)",
    "category": "classical_algorithms",
    "difficulty": "advanced",
    "qubits": 3,
    "gate_count": 7,
    "depth": 4,
    "gates_used": ["H", "X", "CNOT"],
    "description_en": "Determines if a function is constant or balanced in one query",
    "description_cn": "一次查询判断函数是常数还是平衡的",
    "application": ["quantum_algorithms", "oracle_problems"],
    "blockchain_relevance": null,
    "visual_complexity": "medium",
    "entanglement_type": "linear"
  }
  ```

### 2c. Reorganized GitHub Structure
```
quantum-circuit-vision/
├── README.md
├── CIRCUIT_CATALOG.md
├── dataset/                    ← Unified data directory (556 files)
│   ├── circuits/          # 132 PNG circuit diagram images
│   ├── ground_truth/      # 132 Braket SDK ground truth (.py)
│   ├── results/           # 132 simulation results (state vectors, JSON)
│   ├── annotations/       # 132 structured annotations (bilingual, JSON)
│   └── failures/          # 28 annotated failure cases (JSON)
├── docs/
│   ├── roadmap.md         # This file
│   └── dongping_deliverables_for_luyao.txt
├── prompts/               # BV and TV prompt templates
├── scripts/               # Generation, verification, experiment scripts
├── results/               # Aggregated experiment summaries
└── assets/                # Montage overview images
```

---

## 3. Dataset Vision: The 6-Part Quantum Circuit Dataset

Our ultimate goal is the **first multimodal quantum circuit dataset** that enables AI to not just *understand* circuits, but *discover* new ones.

### The 6 Parts

| Part | What | Purpose | Status |
|:---:|:---|:---|:---:|
| 1 | Circuit diagram images | AI learns to **see** | ✅ 132 |
| 2 | Executable code (multi-SDK) | AI learns to **write** | ✅ Braket, 📋 Qiskit/Cirq |
| 3 | Simulation results | AI learns to **verify** | ✅ 132 |
| 4 | Structured annotations | AI learns to **understand** | ✅ 132 |
| 5 | Equivalence & optimization pairs | AI learns to **improve** | 📋 Next phase |
| 6 | Target→Circuit mappings | AI learns to **design** | 📋 Next phase |

### Why This Matters: From Understanding to Discovery

```
AlphaFold analogy:
  Training data = known protein structures
  Breakthrough  = predicting UNKNOWN structures

QCV-Dataset analogy:
  Training data = known quantum circuits (Parts 1-4)
  Breakthrough  = discovering NEW quantum circuits (enabled by Parts 5-6)
```

**The key insight:** Parts 1-4 teach AI the "language" of quantum circuits. Parts 5-6 teach AI the "grammar" — how circuits can be transformed, optimized, and designed from scratch.

---

## 4. Research Trajectory: Three Levels

### Level 1: Benchmark & Tool (Current Paper — ICML AI4Science)
- **Claim:** MMLLMs can reliably translate quantum circuit diagrams to executable code
- **Evidence:** 97% accuracy, CoT Sensitivity Window discovery
- **Dataset:** 132 circuits with images + code + results + annotations
- **Contribution:** First visual quantum circuit benchmark; first systematic CoT analysis

### Level 2: Quantum Protocol Design Co-pilot (Next 6 months)
- **Claim:** AI can assist in designing and verifying quantum-safe protocols
- **Method:** Expand dataset with equivalence pairs + optimization pairs
- **Use case:** Researcher draws circuit sketch → AI generates, verifies, suggests improvements
- **Target:** Nature Machine Intelligence / IEEE TQE

### Level 3: AI-Discovered Quantum Circuits (12-18 months)
- **Claim:** AI can discover novel quantum circuits that outperform known designs
- **Method:** Train on target→circuit pairs; evaluate on unseen targets
- **Validation:** QCV verification pipeline confirms correctness
- **Potential discoveries:**
  - More efficient gate decompositions
  - Novel error correction codes
  - Better variational ansätze for specific problems
  - New quantum cryptographic protocols
- **Target:** Nature / Science
- **Analogy:** AlphaFold for quantum circuits

### Connection to Luyao's "Trilemma to Trinity" Framework

```
Luyao's Framework          QCV Dataset Coverage         AI Discovery Potential
─────────────────          ────────────────────         ──────────────────────
Security                   BB84, E91, Kyber,            AI discovers new PQC
(No-Cloning, PQC)          Dilithium, SPHINCS+,         protocols or more
                           Shor/Grover threats          efficient QKD circuits

Decentralization           QRNG, Voting, Beacon,        AI discovers fairer
(Entanglement, QRNG)       QSS, Coin Flip               consensus mechanisms

Scalability                QAOA, VQE, QFT,              AI discovers better
(Tunneling, Hilbert)       Grover, Quantum Walk          optimization circuits

Integration (Gap 4)        QCV pipeline itself          AI as the unifying
                           = diagram → code → verify    protocol designer
```

---

## 5. What Luyao Can Write in the Paper Based on This

### For the current ICML submission:
1. **Introduction:** Position QCV as infrastructure for quantum-enabled Web3 (Trilemma→Trinity)
2. **Dataset section:** "We release a 132-circuit multimodal dataset with images, code, simulation results, and structured annotations"
3. **Future Work:** Clearly state the Level 2→3 trajectory, referencing AlphaFold analogy
4. **Broader Impact:** "This dataset and pipeline lay the foundation for AI-driven quantum circuit discovery"

### Key sentence for the paper:
> "Beyond benchmarking visual comprehension, QCV-Dataset provides the foundation for a longer-term goal: enabling AI systems to not merely translate but *discover* novel quantum circuits — analogous to how AlphaFold moved from understanding known protein structures to predicting unknown ones."

---

## 6. Timeline

| Date | Milestone |
|:---|:---|
| Apr 29 (tonight) | Parts 3+4 complete, GitHub reorganized |
| Apr 29 (morning) | Luyao integrates into final submission |
| May (KDD version) | Add Parts 5+6, expand to 500+ circuits |
| Jun 1 | KDD Workshop submission |
| Jul-Dec | Level 2 experiments (co-pilot evaluation) |
| 2027 | Level 3 experiments (circuit discovery) |

---

## 7. No Contradictions with Previous Documents

This roadmap is **consistent with and extends** the earlier deliverables:
- `dongping_deliverables_for_luyao.txt` → Technical details (roadmap, inclusive principle, refs)
- `benchmark_expansion_plan.txt` → Circuit expansion plan (A-I directions)
- This document → **Strategic vision** connecting dataset to discovery goal

The hierarchy is:
```
This roadmap (WHY + WHERE)
  └── deliverables.txt (WHAT — technical content for paper)
       └── expansion_plan.txt (HOW — circuit generation details)
```
