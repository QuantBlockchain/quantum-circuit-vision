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
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent
    dataset_root = repo_root / "dataset"
    if not dataset_root.exists():
        raise FileNotFoundError(f"Dataset folder not found at {dataset_root}")
    return dataset_root


def load_circuits_dataset(dataset_root):
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
        braket_code = open(braket_path, "r", encoding="utf-8").read() if braket_path.exists() else None

        qiskit_path = qiskit_dir / f"{cid}.py"
        qiskit_code = open(qiskit_path, "r", encoding="utf-8").read() if qiskit_path.exists() else None

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
    failures_file = dataset_root / "failures" / "failures.json"
    if not failures_file.exists():
        return None
    with open(failures_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    records = data if isinstance(data, list) else data.get("failures", [])
    if not records:
        return None
    features = Features({
        "id": Value("string"), "model": Value("string"), "mode": Value("string"),
        "circuit": Value("string"), "error_type": Value("string"),
        "fidelity": Value("float64"), "error_detail": Value("string"),
    })
    return Dataset.from_list(records, features=features)


def load_equivalences_dataset(dataset_root):
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
        "pair_id": Value("string"), "circuit_a_id": Value("string"),
        "circuit_b_id": Value("string"), "equivalence_type": Value("string"),
        "verified": Value("bool"),
    })
    return Dataset.from_list(records, features=features)


def main():
    parser = argparse.ArgumentParser(description="Upload QCV-Dataset to Hugging Face")
    parser.add_argument("--repo_id", type=str, default="QuantBlockchain/qcv-dataset")
    parser.add_argument("--private", action="store_true", help="Create private dataset")
    parser.add_argument("--skip_upload", action="store_true", help="Test preparation only")
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
    print(f"  Image type: {type(sample['circuit_image']).__name__}")

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
    try:
        create_repo(repo_id=args.repo_id, repo_type="dataset", private=args.private, exist_ok=True)
        print("  Repo ready!")
    except Exception as e:
        print(f"  Error: {e}")
        print("  Make sure you ran 'hf auth login' with a write token.")
        return

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
    citation = ("@misc{liu2026qcv, title={QCV: Cost-Aware Evaluation of Visual AI Agents for Quantum Code Generation}, "
                "author={Liu, Dongping and Zhang, Aoyu and Zhang, Luyao}, year={2026}, "
                "url={https://github.com/QuantBlockchain/quantum-circuit-vision}}")
    croissant_rai = {
        "@context": {"@vocab": "https://schema.org/", "cr": "http://mlcommons.org/croissant/", "rai": "http://mlcommons.org/croissant/RAI/"},
        "@type": "sc:Dataset", "@id": f"https://huggingface.co/datasets/{args.repo_id}",
        "name": "QCV-Dataset",
        "description": "132 Quantum Circuits, 5 Core Modalities, 792 Experiment Results, Bilingual Annotations.",
        "license": "https://spdx.org/licenses/MIT.html",
        "url": f"https://huggingface.co/datasets/{args.repo_id}",
        "sameAs": "https://github.com/QuantBlockchain/quantum-circuit-vision",
        "citeAs": citation,
        "creator": [{"@type": "Person", "name": "Dongping Liu"}, {"@type": "Person", "name": "Aoyu Zhang"}, {"@type": "Person", "name": "Luyao Zhang"}],
        "datePublished": "2026-04", "version": "1.0.0",
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
        "rai:dataReleaseMaintenance": {"version": "1.0.0", "releaseDate": "2026-04", "maintenancePlan": "Community-driven updates; issue tracking via GitHub"},
        "rai:securityPrivacy": {"personalInformation": "No personal information included", "sensitiveData": "No sensitive data; all synthetic quantum circuits"}
    }
    croissant_path = "/tmp/croissant-rai.jsonld"
    with open(croissant_path, "w", encoding="utf-8") as f:
        json.dump(croissant_rai, f, indent=2, ensure_ascii=False)
    upload_file(path_or_fileobj=croissant_path, path_in_repo="croissant-rai.jsonld", repo_id=args.repo_id, repo_type="dataset")
    print("  Done!")

    print("\n" + "=" * 60)
    print("UPLOAD COMPLETE!")
    print("=" * 60)
    print(f"\nDataset URL: https://huggingface.co/datasets/{args.repo_id}")


if __name__ == "__main__":
    main()
