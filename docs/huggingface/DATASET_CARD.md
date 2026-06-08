---
license: mit
language:
  - en
  - zh
pretty_name: QCV-Dataset
tags:
  - quantum-computing
  - quantum-circuits
  - code-generation
  - multimodal
  - image-to-text
  - braket
  - qiskit
  - science
  - physics
  - machine-learning
  - bilingual
task_categories:
  - image-to-text
  - text-generation
  - visual-question-answering
task_ids:
  - image-captioning
  - text2text-generation     
  - visual-question-answering 
size_categories:
  - n<1K
annotations_creators:
  - expert-generated
  - machine-generated
language_creators:
  - expert-generated
multilinguality:
  - multilingual
source_datasets:
  - original
---
# QCV-Dataset

**132 Quantum Circuits · 5 Core Modalities · 792 Experiment Results · Bilingual Annotations**

The first multimodal quantum circuit dataset for training and evaluating AI systems on quantum circuit understanding, code generation, and verification.

## Dataset Description

- **Curated by:** Dongping Liu, Aoyu Zhang, Luyao Zhang
- **Language(s):** English (EN), Chinese (CN) — bilingual annotations
- **License:** MIT
- **Modality:** Multimodal — Images (circuit diagrams), Text (code + descriptions), Numerical (state vectors)

## Dataset Summary

QCV-Dataset contains 132 quantum circuits across 13 categories, each with 5 core modalities: circuit diagram image, Amazon Braket SDK code, Qiskit code, simulation results (state vectors), and bilingual expert annotations. Additionally, 792 experimental model invocations (3 models × 2 prompting modes × 132 circuits) provide a comprehensive benchmark for evaluating visual AI agents on quantum code generation.

## Dataset Structure

### Config: `circuits` (default)

| Feature | Type | Description |
|---|---|---|
| `id` | string | Unique circuit identifier (e.g., `C01_deutsch_jozsa_3`) |
| `circuit_image` | Image | Qiskit-generated circuit diagram (PNG, 150 DPI, IQP style) |
| `braket_code` | string | Amazon Braket SDK executable Python code |
| `qiskit_code` | string | Qiskit equivalent implementation |
| `description_en` | string | English algorithm description |
| `description_cn` | string | Chinese algorithm description |
| `category` | string | Circuit category (13 categories) |
| `difficulty` | string | Difficulty level: `basic`, `intermediate`, `advanced` |
| `qubits` | int32 | Number of qubits (1–10) |
| `gate_count` | int32 | Number of gates (or null) |
| `depth` | int32 | Circuit depth (1–27) |
| `blockchain_relevance` | string | Blockchain relevance tag (if applicable) |
| `state_vector_dim` | int32 | Dimension of state vector (2^qubits) |
| `nonzero_amplitudes` | int32 | Number of nonzero amplitudes |
| `state_vector_real` | sequence[float64] | Real components of simulated state vector |
| `state_vector_imag` | sequence[float64] | Imaginary components of simulated state vector |
| `target_description` | string | Target task description |
| `best_pass_rate` | string | Best pass rate across all models (e.g., "5/6") |
| `all_pass` | bool | Whether circuit passed all model-mode combinations |
| `all_fail` | bool | Whether circuit failed all model-mode combinations |

### Config: `experiments`

| Feature | Type | Description |
|---|---|---|
| `circuit_id` | string | Reference to circuit |
| `model` | string | Model name (claude-opus-4.6, claude-sonnet-4.6, claude-haiku-4.5) |
| `mode` | string | Prompting mode (bv = base vision, tv = thinking vision / chain-of-thought) |
| `syntax_ok` | bool | Whether generated code compiles |
| `exec_ok` | bool | Whether code executes without runtime errors |
| `fidelity` | float64 | Unitary matrix fidelity score |
| `pass` | bool | Whether verification passed (fidelity >= 0.99) |
| `error` | string | Error message (if failed) |

### Config: `failures`

Annotated failure cases from model evaluation with error type classification.

### Config: `equivalences`

Circuit equivalence pairs for verification benchmarking.

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

## Dataset Creation

### Data Collection
- Circuit diagrams generated with Qiskit `QuantumCircuit.draw("mpl", style="iqp")` at 150 DPI with tight bounding boxes
- Ground-truth code implemented in Amazon Braket SDK
- All circuits verified executable on Amazon Braket `LocalSimulator`

### Annotations
- Bilingual descriptions (EN/CN) created by domain experts
- Categories assigned based on algorithm type and complexity
- Difficulty levels determined by circuit depth and gate complexity

## Experiment Results

| Model | BV Pass% | TV Pass% | Credits/Correct |
|---|---|---|---|
| Claude Opus 4.6 | 78% | 75% | 0.778 |
| Claude Sonnet 4.6 | 77% | 75% | 0.142 |
| Claude Haiku 4.5 | 43% | 46% | 0.072 |

**Key Findings:**
- **45 circuits** passed all 6 model-mode combinations
- **18 circuits** failed all 6 combinations
- Structural complexity (not qubit count) determines success
- Chain-of-thought provides no benefit for strong models (delta = -3 to -4%) but modest improvement for weakest (delta = +5%)

## Usage

### Load the dataset

```python
from datasets import load_dataset

# Load main circuits dataset
circuits = load_dataset("QuantBlockchain/qcv-dataset", "circuits", split="train")

# Load experiment results
experiments = load_dataset("QuantBlockchain/qcv-dataset", "experiments", split="train")

# Access a sample
sample = circuits[0]
print(sample["id"])              # C01_deutsch_jozsa_3
print(sample["circuit_image"])    # PIL.Image object
print(sample["braket_code"])      # Python code string
print(sample["description_en"])   # English description
print(sample["description_cn"])   # Chinese description
```

### Filter by category

```python
algo_circuits = circuits.filter(lambda x: x["category"] == "classical_algorithms")
small_circuits = circuits.filter(lambda x: x["qubits"] <= 3)
passing_circuits = circuits.filter(lambda x: x["all_pass"] == True)
```

### Analyze experiment results

```python
from collections import Counter

model_pass = {}
for exp in experiments:
    model = exp["model"]
    if model not in model_pass:
        model_pass[model] = {"total": 0, "passed": 0}
    model_pass[model]["total"] += 1
    if exp["pass"]:
        model_pass[model]["passed"] += 1

for model, stats in model_pass.items():
    rate = stats["passed"] / stats["total"] * 100
    print(f"{model}: {rate:.1f}% ({stats['passed']}/{stats['total']})")
```

## Data Governance & Croissant

This dataset follows [Croissant](https://github.com/mlcommons/croissant) metadata standards for machine-readable dataset descriptions. The dataset card uses structured YAML front matter for discoverability and includes:

- **Data provenance:** Synthetic generation via Qiskit + expert curation
- **Annotation methodology:** Expert-generated bilingual descriptions
- **Verification protocol:** Unitary matrix fidelity >= 0.99 on Braket LocalSimulator
- **Known limitations:** Framework-specific (Braket SDK), simulation-only, EN/CN bilingual only
- **Bias considerations:** 23.5% blockchain-relevant circuits may skew toward cryptographic applications

The dataset also includes a Croissant-RAI (`croissant-rai.jsonld`) extension documenting responsible AI considerations, data limitations, and recommended use cases.

## Limitations and Biases

| Limitation | Description |
|---|---|
| Framework lock-in | Code is Amazon Braket SDK specific |
| Simulation gap | No hardware execution data; LocalSimulator results may differ from real QPUs |
| Language coverage | Bilingual EN/CN only |
| Depth range | 1-27; may not represent extremely deep circuits |
| Domain skew | 23.5% blockchain-relevant circuits over-represents cryptographic applications |

## Citation

```bibtex
@misc{liu2026qcv,
  title={QCV: Cost-Aware Evaluation of Visual AI Agents for Quantum Code Generation},
  author={Liu, Dongping and Zhang, Aoyu and Zhang, Luyao},
  year={2026},
  url={https://github.com/QuantBlockchain/quantum-circuit-vision}
}
```

## License

MIT — see [LICENSE](LICENSE)

## Additional Documentation

- [DATASHEET.md](https://github.com/QuantBlockchain/quantum-circuit-vision/blob/main/DATASHEET.md) — Full dataset documentation following Gebru et al. (2021)
- [CITATION.cff](https://github.com/QuantBlockchain/quantum-circuit-vision/blob/main/CITATION.cff) — Machine-readable citation metadata
- [CIRCUIT_CATALOG.md](https://github.com/QuantBlockchain/quantum-circuit-vision/blob/main/CIRCUIT_CATALOG.md) — Full listing of all 132 circuits
