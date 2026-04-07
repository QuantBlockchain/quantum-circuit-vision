"""Phase 1: 批量验证 Basic 电路 (BV + TV), 从 raw 提取代码, 酉矩阵 fidelity"""
import re, os, math, numpy as np
from braket.circuits import Circuit
from braket.devices import LocalSimulator

RESULTS = os.path.join(os.path.dirname(__file__), "results")
device = LocalSimulator()

# ── Ground truth circuits (Braket SDK) ──────────────────────────────
def gt_circuits():
    d = {}
    d["demo_01_hadamard"] = Circuit().h(0)
    d["demo_02_cnot"] = Circuit().cnot(0, 1)
    d["demo_03_bell"] = Circuit().h(0).cnot(0, 1)
    d["demo_04_ghz"] = Circuit().h(0).cnot(0, 1).cnot(0, 2)
    d["demo_05_toffoli"] = Circuit().ccnot(0, 1, 2)
    return d

GT = gt_circuits()

# ── Helpers (synced from verify_advanced.py) ────────────────────────
def get_unitary_columns(circuit):
    n = circuit.qubit_count
    cols = []
    for i in range(2**n):
        prep = Circuit()
        for bit in range(n):
            if (i >> bit) & 1:
                prep.x(bit)
        full = prep.add_circuit(circuit)
        full.state_vector()
        r = device.run(full, shots=0).result()
        cols.append(np.array(r.values[0]))
    return np.column_stack(cols)

def unitary_fidelity(u1, u2):
    if u1.shape != u2.shape:
        return 0.0
    return abs(np.trace(u1.conj().T @ u2)) / u1.shape[0]

def extract_code(raw_text):
    def clean_ansi(s):
        s = re.sub(r'\[[\d;?]*[a-zA-Z]', '', s)
        s = re.sub(r'[\x1b\x00-\x09\x0b\x0c\x0e-\x1f]', '', s)
        return s.strip()

    green_blocks = re.findall(r'\[38;5;10m(.*?)(?:\[0m)+', raw_text, re.DOTALL)
    for block in green_blocks:
        clean = clean_ansi(block)
        if 'Circuit' in clean and ('from braket' in clean or 'circuit' in clean.lower()):
            return clean

    diff_lines = re.findall(r'\+\s*\d+.*?:\s*(.*?)(?:\[K|\n)', raw_text)
    if diff_lines:
        code_lines = [clean_ansi(dl) for dl in diff_lines]
        code = '\n'.join(l for l in code_lines if l)
        if 'Circuit' in code:
            return code

    text = clean_ansi(raw_text)
    m = re.search(r'((?:import [^\n]+\n)*from braket[^\n]*\n.*?print\([^)]*\))', text, re.DOTALL)
    if m:
        return m.group(1).strip()
    m = re.search(r'((?:import [^\n]+\n)*from braket[^\n]*\n(?:.*\n)*?.*(?:circuit|swap|cnot|ccnot|\.h\(|\.x\(|\.ry\(|\.rx\(|\.rz\().*)', text)
    if m:
        return m.group(0).strip()

    return None

def safe_exec_circuit(code_str):
    clean = re.sub(r'print\(.*?\)', '', code_str)
    ns = {"math": math, "np": np, "numpy": np}
    exec(clean, ns)
    for v in ns.values():
        if isinstance(v, Circuit):
            return v
    return None

# ── Main ────────────────────────────────────────────────────────────
CIRCUIT_NAMES = sorted(GT.keys())
MODELS = ["opus-4.6", "sonnet-4.6", "haiku-4.5"]
# BV: Phase 1 旧命名 (opus_bv_demo_01_...), TV: 新命名 (opus-4.6_tv_demo_01_...)
MODES = ["bv", "tv"]

print("预计算 ground truth 酉矩阵...")
GT_U = {}
for cname, circ in GT.items():
    GT_U[cname] = get_unitary_columns(circ)
print("完成\n")

results = {}

for model in MODELS:
    for mode in MODES:
        for cname in CIRCUIT_NAMES:
            key = (model, mode, cname)

            # Phase 1 BV 用旧命名: opus_bv_demo_01_hadamard_raw.txt
            # Phase 1 TV 和所有新模型用新命名: opus-4.6_tv_demo_01_hadamard_raw.txt
            if mode == "bv" and model in ("opus-4.6", "haiku-4.5"):
                model_prefix = model.split("-")[0]  # opus / haiku
                fname = f"{model_prefix}_{mode}_{cname}_raw.txt"
            else:
                fname = f"{model}_{mode}_{cname}_raw.txt"

            fpath = os.path.join(RESULTS, fname)

            if not os.path.exists(fpath):
                results[key] = {"syntax": False, "exec": False, "fidelity": 0,
                                "pass": False, "code": "", "error": "文件不存在"}
                continue

            if os.path.getsize(fpath) < 1024:
                # lesson learned #5: < 1KB 大概率废数据
                pass  # 仍然尝试提取，但标记警告

            with open(fpath) as f:
                raw = f.read()

            code = extract_code(raw)
            if not code:
                results[key] = {"syntax": False, "exec": False, "fidelity": 0,
                                "pass": False, "code": "", "error": "无法提取代码"}
                continue

            clean = re.sub(r'print\(.*?\)', '', code)
            try:
                compile(clean, '<string>', 'exec')
            except SyntaxError as e:
                results[key] = {"syntax": False, "exec": False, "fidelity": 0,
                                "pass": False, "code": code, "error": f"语法错误: {e}"}
                continue

            try:
                gen_circuit = safe_exec_circuit(code)
                if gen_circuit is None:
                    results[key] = {"syntax": True, "exec": False, "fidelity": 0,
                                    "pass": False, "code": code, "error": "未生成 Circuit 对象"}
                    continue
            except Exception as e:
                results[key] = {"syntax": True, "exec": False, "fidelity": 0,
                                "pass": False, "code": code, "error": f"执行错误: {e}"}
                continue

            try:
                u_gen = get_unitary_columns(gen_circuit)
                f = unitary_fidelity(GT_U[cname], u_gen)
                passed = f >= 0.99
                results[key] = {"syntax": True, "exec": True, "fidelity": f,
                                "pass": passed, "code": code,
                                "error": "" if passed else f"Fidelity={f:.4f}"}
            except Exception as e:
                results[key] = {"syntax": True, "exec": True, "fidelity": 0,
                                "pass": False, "code": code, "error": f"验证错误: {e}"}

# ── Report ──────────────────────────────────────────────────────────
NUM = len(CIRCUIT_NAMES)
L = []
L.append("=" * 80)
L.append("  QCV Phase 1 Basic 结果汇总 (BV + TV)")
L.append(f"  题数: {NUM}")
L.append("  日期: 2026-03-25")
L.append("  验证方式: Braket LocalSimulator, 酉矩阵 fidelity ≥ 0.99 判定通过")
L.append("=" * 80)

for model in MODELS:
    for mode in MODES:
        label = f"claude-{model} ({'BV 直接看图' if mode == 'bv' else 'TV 先分析再生成'})"
        L.append("")
        L.append("=" * 80)
        L.append(label)
        L.append("=" * 80)
        L.append("")
        L.append(f"{'用例':<25s} {'语法':>4s} {'执行':>4s} {'Fidelity':>10s} {'通过':>4s}  备注")
        L.append("─" * 80)

        pc = 0
        for cname in CIRCUIT_NAMES:
            r = results[(model, mode, cname)]
            if r["pass"]: pc += 1
            syn = "✓" if r["syntax"] else "✗"
            exe = "✓" if r["exec"] else "✗"
            fid = f'{r["fidelity"]:.4f}' if r["exec"] else "N/A"
            pas = "✓" if r["pass"] else "✗"
            note = r.get("error", "")
            short = cname.replace("demo_", "")
            L.append(f"{short:<25s} {syn:>4s} {exe:>4s} {fid:>10s} {pas:>4s}  {note}")

        L.append("")
        L.append(f"Pass Rate: {pc}/{NUM} = {pc*100//NUM}%")

L.append("")
L.append("=" * 80)
L.append("模型对比汇总")
L.append("=" * 80)
L.append("")
L.append(f"{'模型+模式':<35s} {'Pass Rate':>12s}")
L.append("─" * 50)
for model in MODELS:
    for mode in MODES:
        p = sum(1 for c in CIRCUIT_NAMES if results[(model, mode, c)]["pass"])
        lbl = f"claude-{model} {'BV' if mode == 'bv' else 'TV'}"
        L.append(f"{lbl:<35s} {p}/{NUM} = {p*100//NUM}%")

L.append("")
L.append("=" * 80)
L.append("错误类型分析")
L.append("=" * 80)
for model in MODELS:
    for mode in MODES:
        fails = [(c, results[(model, mode, c)]) for c in CIRCUIT_NAMES
                 if not results[(model, mode, c)]["pass"]]
        if fails:
            L.append("")
            L.append(f"claude-{model} {'BV' if mode == 'bv' else 'TV'} 失败用例:")
            for c, r in fails:
                L.append(f"  {c.replace('demo_','')}: {r['error']}")

L.append("")
L.append("=" * 80)

report = "\n".join(L)
print(report)

out = os.path.join(RESULTS, "basic_results_summary.txt")
with open(out, "w") as f:
    f.write(report)
print(f"\n>>> 报告已写入: {out}")
