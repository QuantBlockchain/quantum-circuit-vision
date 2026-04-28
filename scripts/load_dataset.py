"""QCV Dataset Loader — load all 132 circuits with one function call."""
import os, json

def load_dataset(base_dir=None):
    """Load the full QCV dataset.
    
    Returns:
        list of dicts, each with keys:
        - id: circuit identifier
        - image_path: path to PNG
        - code_path: path to ground truth .py
        - code: ground truth source code (str)
        - annotation: dict from annotations JSON
        - result: dict from results JSON (or None)
    """
    if base_dir is None:
        base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dataset")

    circuits_dir = os.path.join(base_dir, "circuits")
    gt_dir = os.path.join(base_dir, "ground_truth")
    ann_dir = os.path.join(base_dir, "annotations")
    res_dir = os.path.join(base_dir, "results")

    dataset = []
    for fname in sorted(os.listdir(ann_dir)):
        if not fname.endswith('.json'):
            continue
        cid = fname[:-5]

        # Annotation
        with open(os.path.join(ann_dir, fname)) as f:
            annotation = json.load(f)

        # Code
        code_path = os.path.join(gt_dir, f"{cid}.py")
        code = open(code_path).read() if os.path.exists(code_path) else None

        # Result
        res_path = os.path.join(res_dir, f"{cid}.json")
        if os.path.exists(res_path):
            with open(res_path) as f:
                result = json.load(f)
        else:
            result = None

        dataset.append({
            "id": cid,
            "image_path": os.path.join(circuits_dir, f"{cid}.png"),
            "code_path": code_path,
            "code": code,
            "annotation": annotation,
            "result": result,
        })

    return dataset


def load_failures(base_dir=None):
    """Load all failure cases.
    
    Returns:
        list of dicts with error details.
    """
    if base_dir is None:
        base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dataset")

    fail_dir = os.path.join(base_dir, "failures")
    failures = []
    for fname in sorted(os.listdir(fail_dir)):
        if fname.startswith('_') or not fname.endswith('.json'):
            continue
        with open(os.path.join(fail_dir, fname)) as f:
            failures.append(json.load(f))
    return failures


if __name__ == "__main__":
    ds = load_dataset()
    print(f"Loaded {len(ds)} circuits")
    print(f"Categories: {sorted(set(d['annotation']['category'] for d in ds))}")
    print(f"Qubit range: {min(d['annotation']['qubits'] for d in ds)}-{max(d['annotation']['qubits'] for d in ds)}")
    print(f"\nExample: {ds[0]['id']}")
    print(f"  {ds[0]['annotation']['description_en']}")
    print(f"  {ds[0]['annotation']['description_cn']}")

    fails = load_failures()
    print(f"\nLoaded {len(fails)} failure cases")
