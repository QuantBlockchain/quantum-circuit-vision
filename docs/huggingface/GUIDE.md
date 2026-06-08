# QCV-Dataset Hugging Face Upload Guide

Complete step-by-step guide to upload the QCV-Dataset from your GitHub Codespace to Hugging Face Hub, with full Croissant/RAI data governance support.

---

## Prerequisites

Before starting, you need:
1. A Hugging Face account: https://huggingface.co/join
2. A Hugging Face access token with **Write** permission
3. An active GitHub Codespace for the `quantum-circuit-vision` repo

---

## Step 1: Get Your Hugging Face Access Token

1. Go to https://huggingface.co/settings/tokens
2. Click **New token**
3. Name: `qcv-upload`
4. Role: **Write**
5. Click **Generate token**
6. **Copy the token** (you will not see it again)

---

## Step 2: Open Your GitHub Codespace

1. Go to https://github.com/QuantBlockchain/quantum-circuit-vision
2. Click the **Code** button (green)
3. Select the **Codespaces** tab
4. Click on your existing Codespace (or create a new one)
5. Wait for the Codespace to fully load

You should see the repo files in the Explorer panel on the left:
```
quantum-circuit-vision/
  dataset/
    annotations/
    braket_code/
    circuits/
    equivalences/
    experiment_results/
    failures/
    qiskit_code/
    simulations/
    targets/
    README.md
    statistics.json
  scripts/
    load_dataset.py
    ...
  requirements.txt
  ...
```

---

## Step 3: Open a Terminal in Codespace

1. In VS Code (Codespace), press **Ctrl+`** (backtick) or go to **Terminal > New Terminal**
2. You should be in the repo root: `~/workspaces/quantum-circuit-vision$`
3. Verify the dataset folder exists:

```bash
ls dataset/
```

Expected output:
```
annotations  braket_code  circuits  equivalences  experiment_results  failures  qiskit_code  README.md  simulations  statistics.json  targets
```

---

## Step 4: Install Dependencies

In the terminal, run:

```bash
pip install datasets huggingface_hub
```

Wait for installation to complete. You should see something like:
```
Successfully installed datasets-3.x.x huggingface_hub-0.x.x ...
```

---

## Step 5: Authenticate with Hugging Face

In the terminal, run:

```bash
huggingface-cli login
```

When prompted, paste your Hugging Face access token (from Step 1) and press **Enter**.

You should see:
```
Token is valid (permission: write).
Your token has been saved to /home/codespace/.cache/huggingface/token
Login successful
```

---

## Step 6: Copy the Upload Script

Create the upload script in the `scripts/` folder. Run these commands in the terminal:

```bash
cat > scripts/upload_to_huggingface.py << 'PYEOF'
#!/usr/bin/env python3
"""QCV-Dataset Hugging Face Upload Script."""

import os
import json
import csv
import argparse
from pathlib import Path
from datasets import Dataset, Features, Image, Value, Sequence
from huggingface_hub import create_repo, upload_file


def get_dataset_root():
    """Locate the dataset folder relative to this script."""
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent
    dataset_root = repo_root / "dataset"
    if not dataset_root.exists():
        raise FileNotFoundError(f"Dataset folder not found at {dataset_root}")
    return dataset_root


def load_circuits_dataset(dataset_root):
    """Load the main circuits dataset with all 5 core modalities."""
    circuits_dir = dataset_root / "circuits"
    braket_dir = dataset_root / "braket_code"
    qiskit_dir = dataset_root / "qiskit_code"
    annotations_dir = dataset_root / "annotations"
    simulations_dir = dataset_root / "simulations"
    targets_dir = dataset_root / "targets"

    annotation_files = sorted(annotations_dir.glob("*.json"))
    print(f"Found {len(annotation_files)} annotation files")

    records = []
    for ann_file in annotation_files:
        with open(ann_file, "r", encoding="utf-8") as f:
            annotation = json.load(f)

        cid = annotation["id"]

        img_path = circuits_dir / f"{cid}.png"
        circuit_image = str(img_path) if img_path.exists() else None
        if not img_path.exists():
            print(f"  WARNING: Image not found for {cid}")

        braket_path = braket_dir / f"{cid}.py"
        braket_code = (
            open(braket_path, "r", encoding="utf-8").read()
            if braket_path.exists() else None
        )

        qiskit_path = qiskit_dir / f"{cid}.py"
        qiskit_code = (
            open(qiskit_path, "r", encoding="utf-8").read()
            if qiskit_path.exists() else None
        )

        sim_path = simulations_dir / f"{cid}.json"
        state_vector_real = None
        state_vector_imag = None
        if sim_path.exists():
            with open(sim_path, "r", encoding="utf-8") as f:
                sim_data = json.load(f)
            state_vector_real = sim_data.get("state_vector_real", [])
            state_vector_imag = sim_data.get("state_vector_imag", [])

        target_path = targets_dir / f"{cid}.json"
        target_description = None
        if target_path.exists():
            with open(target_path, "r", encoding="utf-8") as f:
                target_data = json.load(f)
            target_description = target_data.get("description")

        exp_results = annotation.get("experiment_results", {})

        record = {
            "id": cid,
            "circuit_image": circuit_image,
            "braket_code": braket_code,
            "qiskit_code": qiskit_code,
            "category": annotation.get("category"),
            "difficulty": annotation.get("difficulty"),
            "qubits": annotation.get("qubits"),
            "gate_count": annotation.get("gate_count"),
            "depth": annotation.get("depth"),
            "description_en": annotation.get("description_en"),
            "description_cn": annotation.get("description_cn"),
            "blockchain_relevance": annotation.get("blockchain_relevance"),
            "state_vector_dim": annotation.get("state_vector_dim"),
            "nonzero_amplitudes": annotation.get("nonzero_amplitudes"),
            "state_vector_real": state_vector_real,
            "state_vector_imag": state_vector_imag,
            "target_description": target_description,
            "best_pass_rate": exp_results.get("best_pass_rate"),
            "all_pass": exp_results.get("all_pass"),
            "all_fail": exp_results.get("all_fail"),
        }
        records.append(record)

    features = Features({
        "id": Value("string"),
        "circuit_image": Image(),
        "braket_code": Value("string"),
        "qiskit_code": Value("string"),
        "category": Value("string"),
        "difficulty": Value("string"),
        "qubits": Value("int32"),
        "gate_count": Value("int32"),
        "depth": Value("int32"),
        "description_en": Value("string"),
        "description_cn": Value("string"),
        "blockchain_relevance": Value("string"),
        "state_vector_dim": Value("int32"),
        "nonzero_amplitudes": Value("int32"),
        "state_vector_real": Sequence(Value("float64")),
        "state_vector_imag": Sequence(Value("float64")),
        "target_description": Value("string"),
        "best_pass_rate": Value("string"),
        "all_pass": Value("bool"),
        "all_fail": Value("bool"),
    })

    return Dataset.from_list(records, features=features)


def load_experiments_dataset(dataset_root):
    """Load the 792 experiment results from verification_results.csv."""
    csv_path = dataset_root / "experiment_results" / "verification_results.csv"

    records = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append({
                "circuit_id": row.get("circuit_name", ""),
                "model": row.get("model", ""),
                "mode": row.get("mode", ""),
                "syntax_ok": row.get("syntax_ok", "").lower() == "true",
                "exec_ok": row.get("exec_ok", "").lower() == "true",
                "fidelity": float(row["fidelity"]) if row.get("fidelity") else 0.0,
                "pass": row.get("pass", "").lower() == "true",
                "error": row.get("error", ""),
            })

    features = Features({
        "circuit_id": Value("string"),
        "model": Value("string"),
        "mode": Value("string"),
        "syntax_ok": Value("bool"),
        "exec_ok": Value("bool"),
        "fidelity": Value("float64"),
        "pass": Value("bool"),
        "error": Value("string"),
    })

    return Dataset.from_list(records, features=features)


def load_failures_dataset(dataset_root):
    """Load failure cases from failures/failures.json."""
    failures_file = dataset_root / "failures" / "failures.json"
    if not failures_file.exists():
        return None
    with open(failures_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    records = data if isinstance(data, list) else data.get("failures", [])
    if not records:
        return None
    features = Features({
        "id": Value("string"),
        "model": Value("string"),
        "mode": Value("string"),
        "circuit": Value("string"),
        "error_type": Value("string"),
        "fidelity": Value("float64"),
        "error_detail": Value("string"),
    })
    return Dataset.from_list(records, features=features)


def load_equivalences_dataset(dataset_root):
    """Load circuit equivalence pairs."""
    equiv_dir = dataset_root / "equivalences"
    equiv_files = list(equiv_dir.glob("*.json"))
    if not equiv_files:
        return None
    records = []
    for ef in equiv_files:
        with open(ef, "r", encoding="utf-8") as f:
            data = json.load(f)
        pairs = data if isinstance(data, list) else data.get("equivalence_pairs", [])
        for pair in pairs:
            records.append({
                "pair_id": pair.get("id"),
                "circuit_a_id": pair.get("circuit_a"),
                "circuit_b_id": pair.get("circuit_b"),
                "equivalence_type": pair.get("type"),
                "verified": pair.get("verified", False),
            })
    if not records:
        return None
    features = Features({
        "pair_id": Value("string"),
        "circuit_a_id": Value("string"),
        "circuit_b_id": Value("string"),
        "equivalence_type": Value("string"),
        "verified": Value("bool"),
    })
    return Dataset.from_list(records, features=features)


def main():
    parser = argparse.ArgumentParser(description="Upload QCV-Dataset to Hugging Face")
    parser.add_argument("--repo_id", type=str, default="QuantBlockchain/qcv-dataset",
                        help="Hugging Face repo ID")
    parser.add_argument("--private", action="store_true", help="Create private dataset")
    parser.add_argument("--skip_upload", action="store_true",
                        help="Skip upload (test preparation only)")
    args = parser.parse_args()

    print("=" * 60)
    print("QCV-Dataset Hugging Face Upload")
    print("=" * 60)

    print("\n[Step 1] Locating dataset folder...")
    dataset_root = get_dataset_root()
    print(f"  Dataset root: {dataset_root}")

    print("\n[Step 2] Loading main circuits dataset...")
    circuits_ds = load_circuits_dataset(dataset_root)
    print(f"  Loaded {len(circuits_ds)} circuits")
    sample = circuits_ds[0]
    print(f"  Sample: {sample['id']} | qubits={sample['qubits']} | depth={sample['depth']}")
    print(f"  Image: {type(sample['circuit_image']).__name__}")

    print("\n[Step 3] Loading experiments dataset...")
    experiments_ds = load_experiments_dataset(dataset_root)
    print(f"  Loaded {len(experiments_ds)} experiment results")

    print("\n[Step 4] Loading failures dataset...")
    failures_ds = load_failures_dataset(dataset_root)
    print(f"  Failures: {len(failures_ds) if failures_ds else 'None'}")

    print("\n[Step 5] Loading equivalences dataset...")
    equiv_ds = load_equivalences_dataset(dataset_root)
    print(f"  Equivalences: {len(equiv_ds) if equiv_ds else 'None'}")

    if args.skip_upload:
        print("\n[SKIP] Saving locally for inspection...")
        circuits_ds.save_to_disk("hf_circuits_preview")
        experiments_ds.save_to_disk("hf_experiments_preview")
        return

    print(f"\n[Step 6] Creating repo: {args.repo_id}...")
    create_repo(repo_id=args.repo_id, repo_type="dataset",
                private=args.private, exist_ok=True)
    print("  Repo ready!")

    print("\n[Step 7] Uploading 'circuits' config...")
    circuits_ds.push_to_hub(args.repo_id, config_name="circuits", private=args.private)
    print("  Done!")

    print("\n[Step 8] Uploading 'experiments' config...")
    experiments_ds.push_to_hub(args.repo_id, config_name="experiments", private=args.private)
    print("  Done!")

    if failures_ds:
        print("\n[Step 9] Uploading 'failures' config...")
        failures_ds.push_to_hub(args.repo_id, config_name="failures", private=args.private)
        print("  Done!")

    if equiv_ds:
        print("\n[Step 10] Uploading 'equivalences' config...")
        equiv_ds.push_to_hub(args.repo_id, config_name="equivalences", private=args.private)
        print("  Done!")

    print("\n[Step 11] Uploading Croissant-RAI metadata...")
    citation = ("@misc{liu2026qcv, "
                "title={QCV: Cost-Aware Evaluation of Visual AI Agents for Quantum Code Generation}, "
                "author={Liu, Dongping and Zhang, Aoyu and Zhang, Luyao}, "
                "year={2026}, "
                "url={https://github.com/QuantBlockchain/quantum-circuit-vision}}")
    croissant_rai = {
        "@context": {"@vocab": "https://schema.org/",
                     "cr": "http://mlcommons.org/croissant/",
                     "rai": "http://mlcommons.org/croissant/RAI/"},
        "@type": "sc:Dataset",
        "@id": f"https://huggingface.co/datasets/{args.repo_id}",
        "name": "QCV-Dataset",
        "description": "132 Quantum Circuits, 5 Core Modalities, 792 Experiment Results, Bilingual Annotations.",
        "license": "https://spdx.org/licenses/MIT.html",
        "url": f"https://huggingface.co/datasets/{args.repo_id}",
        "sameAs": "https://github.com/QuantBlockchain/quantum-circuit-vision",
        "citeAs": citation,
        "creator": [{"@type": "Person", "name": "Dongping Liu"},
                    {"@type": "Person", "name": "Aoyu Zhang"},
                    {"@type": "Person", "name": "Luyao Zhang"}],
        "datePublished": "2026-04",
        "version": "1.0.0",
        "rai:dataCollection": {
            "description": "Circuits generated using Qiskit + expert curation. Verified on Braket LocalSimulator.",
            "collectionMethod": "Computational generation with manual expert annotation",
            "source": "Synthetic generation via Qiskit + expert curation"
        },
        "rai:dataLimitations": [
            "Limited to Amazon Braket SDK circuits; framework-specific syntax",
            "State vectors from LocalSimulator only; hardware results may differ",
            "Bilingual annotations cover EN/CN only",
            "Depth range 1-27; may not represent extremely deep circuits",
            "No real quantum hardware execution data"
        ],
        "rai:dataBiases": "Dataset includes 23.5% blockchain-relevant circuits, which may over-represent cryptographic applications relative to general quantum computing.",
        "rai:useCases": [
            "Training visual AI agents for quantum circuit understanding",
            "Evaluating multimodal LLMs on code generation from circuit diagrams",
            "Quantum program verification and equivalence checking",
            "Cost-aware model selection for quantum code generation tasks"
        ],
        "rai:dataReleaseMaintenance": {
            "version": "1.0.0",
            "releaseDate": "2026-04",
            "maintenancePlan": "Community-driven updates; issue tracking via GitHub"
        },
        "rai:securityPrivacy": {
            "personalInformation": "No personal information included",
            "sensitiveData": "No sensitive data; all synthetic quantum circuits"
        }
    }
    croissant_path = "/tmp/croissant-rai.jsonld"
    with open(croissant_path, "w", encoding="utf-8") as f:
        json.dump(croissant_rai, f, indent=2, ensure_ascii=False)
    upload_file(path_or_fileobj=croissant_path, path_in_repo="croissant-rai.jsonld",
                repo_id=args.repo_id, repo_type="dataset")
    print("  Done!")

    print("\n" + "=" * 60)
    print("UPLOAD COMPLETE!")
    print("=" * 60)
    print(f"\nDataset URL: https://huggingface.co/datasets/{args.repo_id}")
    print("\nNext: Upload README.md (dataset card) via the Hugging Face web UI.")


if __name__ == "__main__":
    main()
PYEOF
```

> **Note:** This uses a heredoc (`<< 'PYEOF'`) to create the file. The single quotes around `PYEOF` prevent shell variable expansion.

Verify the file was created:

```bash
ls -la scripts/upload_to_huggingface.py
```

---

## Step 7: Run the Upload Script

In the terminal, run:

```bash
python scripts/upload_to_huggingface.py --repo_id QuantBlockchain/qcv-dataset
```

**If you want a private dataset first (recommended for testing):**

```bash
python scripts/upload_to_huggingface.py --repo_id QuantBlockchain/qcv-dataset --private
```

You should see output like:
```
============================================================
QCV-Dataset Hugging Face Upload
============================================================

[Step 1] Locating dataset folder...
  Dataset root: /home/codespace/workspaces/quantum-circuit-vision/dataset

[Step 2] Loading main circuits dataset...
Found 132 annotation files
  Loaded 132 circuits
  Sample: A01_single_y | qubits=1 | depth=1
  Image: dict

[Step 3] Loading experiments dataset...
  Loaded 792 experiment results

[Step 4] Loading failures dataset...
  Failures: 27

[Step 5] Loading equivalences dataset...
  Equivalences: 12

[Step 6] Creating repo: QuantBlockchain/qcv-dataset...
  Repo ready!

[Step 7] Uploading 'circuits' config...
  Done!

[Step 8] Uploading 'experiments' config...
  Done!

[Step 9] Uploading 'failures' config...
  Done!

[Step 10] Uploading 'equivalences' config...
  Done!

[Step 11] Uploading Croissant-RAI metadata...
  Done!

============================================================
UPLOAD COMPLETE!
============================================================

Dataset URL: https://huggingface.co/datasets/QuantBlockchain/qcv-dataset

Next: Upload README.md (dataset card) via the Hugging Face web UI.
```

> **Troubleshooting:** If you see `Token is required but not provided`, re-run `huggingface-cli login`.
> If you see `Repository not found`, the repo may need to be created on the Hugging Face website first.

---

## Step 8: Upload the Dataset Card (README.md)

After the script finishes, you need to upload the dataset card via the Hugging Face web UI:

1. Open your dataset page:
   ```
   https://huggingface.co/datasets/QuantBlockchain/qcv-dataset
   ```

2. Click the **Files and versions** tab

3. Click **Add file** (top right of the file list)

4. Select **Upload files**

5. Click **Choose files** and select the `README.md` file (or drag and drop it)

6. Scroll down and click **Commit changes to main**

Alternatively, upload via the terminal:

```bash
# Create README with proper YAML front matter
cat > /tmp/hf_readme.md << 'READMEOF'
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
  - code-generation
  - visual-reasoning
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
configs:
  - config_name: circuits
    data_files:
      - split: train
        path: data/circuits-*.parquet
  - config_name: experiments
    data_files:
      - split: train
        path: data/experiments-*.parquet
  - config_name: failures
    data_files:
      - split: train
        path: data/failures-*.parquet
  - config_name: equivalences
    data_files:
      - split: train
        path: data/equivalences-*.parquet
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
READMEOF

# Upload via CLI
huggingface-cli upload QuantBlockchain/qcv-dataset /tmp/hf_readme.md README.md --repo-type dataset
```

---

## Step 9: Verify the Upload

### 9.1 Check the Dataset Viewer

1. Visit: `https://huggingface.co/datasets/QuantBlockchain/qcv-dataset`
2. Click the **Dataset Viewer** tab (next to "Files and versions")
3. You should see:
   - A table with circuit data
   - Image previews of circuit diagrams
   - Code columns with syntax highlighting
   - Bilingual description columns

### 9.2 Test Loading from the Hub

Back in your Codespace terminal, run:

```bash
python -c "
from datasets import load_dataset

print('Testing load from Hugging Face Hub...')
circuits = load_dataset('QuantBlockchain/qcv-dataset', 'circuits', split='train')
print(f'Loaded {len(circuits)} circuits')

sample = circuits[0]
print(f'ID: {sample[\"id\"]}')
print(f'Category: {sample[\"category\"]}')
print(f'Qubits: {sample[\"qubits\"]}')
print(f'Depth: {sample[\"depth\"]}')
print(f'Image type: {type(sample[\"circuit_image\"]).__name__}')
print(f'EN: {sample[\"description_en\"][:80]}...')
print(f'CN: {sample[\"description_cn\"][:80]}...')

experiments = load_dataset('QuantBlockchain/qcv-dataset', 'experiments', split='train')
print(f'Loaded {len(experiments)} experiment results')

print('SUCCESS!')
"
```

### 9.3 Verify Croissant Metadata

```bash
curl -s https://huggingface.co/api/datasets/QuantBlockchain/qcv-dataset/croissant | head -50
```

You should see JSON-LD output with Croissant metadata.

---

## Step 10: Make Public (if uploaded as private)

If you uploaded with `--private` and want to make it public:

1. Go to `https://huggingface.co/datasets/QuantBlockchain/qcv-dataset/settings`
2. Scroll to **Dataset visibility**
3. Select **Public**
4. Click **Save**

Or via terminal:

```bash
python -c "
from huggingface_hub import update_repo_settings
update_repo_settings('QuantBlockchain/qcv-dataset', repo_type='dataset', private=False)
print('Dataset is now public!')
"
```

---

## Quick Reference: All Commands at Once

If you want to run everything in one go (after `huggingface-cli login`):

```bash
# 1. Install dependencies
pip install datasets huggingface_hub

# 2. Create and run upload script (copy from Step 6 above, then run)
python scripts/upload_to_huggingface.py --repo_id QuantBlockchain/qcv-dataset

# 3. Upload README (copy from Step 8 above, then run)
huggingface-cli upload QuantBlockchain/qcv-dataset /tmp/hf_readme.md README.md --repo-type dataset

# 4. Verify
python -c "from datasets import load_dataset; ds = load_dataset('QuantBlockchain/qcv-dataset', 'circuits', split='train'); print(f'OK: {len(ds)} circuits loaded')"
```

---

## Troubleshooting

| Issue | Solution |
|---|---|
| `Token is required but not provided` | Run `huggingface-cli login` again |
| `Repository not found` | Create repo on HF web UI first, or check repo_id spelling |
| `Dataset folder not found` | Make sure you're running from repo root and `dataset/` exists |
| Images not showing in Viewer | Ensure `Image()` feature type was used (not string paths) |
| `ModuleNotFoundError: No module named datasets` | Run `pip install datasets` |
| Upload is slow | Normal for first upload (132 images + code). Wait 5-10 minutes |
| Dataset Viewer shows "Rendering..." | HF processes Parquet files in background. Wait 10-15 minutes |

---

## What Gets Uploaded

| Config | Records | Content |
|---|---|---|
| `circuits` (default) | 132 | Circuit images, Braket code, Qiskit code, bilingual descriptions, state vectors, targets, experiment summaries |
| `experiments` | 792 | All model invocations with fidelity, pass/fail, errors |
| `failures` | 27 | Annotated failure cases with error types |
| `equivalences` | 12 | Circuit equivalence pairs for verification |

Plus `croissant-rai.jsonld` for data governance documentation.
