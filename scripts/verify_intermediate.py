"""Phase 2: 从 raw 输出提取代码, 用 LocalSimulator 验证, 生成汇总"""
import re, os, math, numpy as np
from braket.circuits import Circuit
from braket.devices import LocalSimulator

RESULTS = os.path.join(os.path.dirname(__file__), "results")
device = LocalSimulator()

# ── Ground truth circuits (Braket SDK) ──────────────────────────────
def gt_circuits():
    d = {}
    d["inter_01_swap_decomp"] = Circuit().cnot(0,1).cnot(1,0).cnot(0,1)
    d["inter_02_qft2"] = Circuit().h(0).cphaseshift(0,1,math.pi/2).h(1).swap(0,1)
    d["inter_03_teleport_prep"] = Circuit().h(1).cnot(1,2).cnot(0,1).h(0)
    d["inter_04_deutsch"] = Circuit().x(1).h(0).h(1).cnot(0,1).h(0)
    d["inter_05_superdense"] = Circuit().h(0).cnot(0,1).x(0).z(0).cnot(0,1).h(0)
    d["inter_06_grover2"] = Circuit().h(0).h(1).cz(0,1).h(0).h(1).z(0).z(1).cz(0,1).h(0).h(1)
    d["inter_07_param_rot"] = Circuit().rx(0,math.pi/3).rz(1,math.pi/4).cnot(0,1)
    d["inter_08_fredkin"] = Circuit().cswap(0,1,2)
    d["inter_09_shift_reg"] = Circuit().x(0).cnot(0,1).cnot(1,2).cnot(2,3)
    d["inter_10_phase_est"] = Circuit().h(0).h(1).cphaseshift(0,2,math.pi/2).cphaseshift(1,2,math.pi/4).h(0).h(1)
    return d

GT = gt_circuits()

# ── Helpers ─────────────────────────────────────────────────────────
def get_statevector(circuit):
    """Run circuit on |0...0⟩ and return state vector."""
    c = circuit.copy()
    c.state_vector()
    r = device.run(c, shots=0).result()
    return np.array(r.values[0])

def get_unitary_columns(circuit):
    """Get unitary matrix by running each basis state."""
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
    """Fidelity tolerant of global phase: |Tr(U1† U2)|/dim."""
    if u1.shape != u2.shape:
        return 0.0
    dim = u1.shape[0]
    return abs(np.trace(u1.conj().T @ u2)) / dim

def extract_code(raw_text):
    """Extract Python code from raw kiro-cli output with ANSI codes."""
    def clean_ansi(s):
        s = re.sub(r'\[[\d;?]*[a-zA-Z]', '', s)
        s = re.sub(r'[\x1b\x00-\x09\x0b\x0c\x0e-\x1f]', '', s)
        return s.strip()

    # Strategy 1: green-colored code blocks (1+ trailing [0m)
    green_blocks = re.findall(r'\[38;5;10m(.*?)(?:\[0m)+', raw_text, re.DOTALL)
    for block in green_blocks:
        clean = clean_ansi(block)
        if 'Circuit' in clean and ('from braket' in clean or 'circuit' in clean.lower()):
            return clean

    # Strategy 2: diff-style output
    diff_lines = re.findall(r'\+\s*\d+.*?:\s*(.*?)(?:\[K|\n)', raw_text)
    if diff_lines:
        code_lines = [clean_ansi(dl) for dl in diff_lines]
        code = '\n'.join(l for l in code_lines if l)
        if 'Circuit' in code:
            return code

    # Strategy 3: strip all ANSI, find code block (with or without print)
    text = clean_ansi(raw_text)
    m = re.search(r'((?:import [^\n]+\n)*from braket[^\n]*\n.*?print\([^)]*\))', text, re.DOTALL)
    if m:
        return m.group(1).strip()
    m = re.search(r'((?:import [^\n]+\n)*from braket[^\n]*\n(?:.*\n)*?.*(?:circuit|swap|cnot|ccnot|\.h\(|\.x\(|\.ry\(|\.rx\(|\.rz\().*)', text)
    if m:
        return m.group(0).strip()

    return None

def safe_exec_circuit(code_str):
    """Execute code, return Circuit object. Provides common imports in namespace."""
    clean = re.sub(r'print\(.*?\)', '', code_str)
    ns = {"math": math, "np": np, "numpy": np}
    exec(clean, ns)
    for v in ns.values():
        if isinstance(v, Circuit):
            return v
    return None

# ── Main verification loop ──────────────────────────────────────────
CIRCUIT_NAMES = sorted(GT.keys())
MODELS = ["opus-4.6", "sonnet-4.6", "haiku-4.5"]
MODES = ["bv", "tv"]

# Pre-compute ground truth unitaries
GT_U = {}
for cname, circ in GT.items():
    GT_U[cname] = get_unitary_columns(circ)

results = {}

for model in MODELS:
    for mode in MODES:
        for cname in CIRCUIT_NAMES:
            key = (model, mode, cname)
            fname = f"{model}_{mode}_{cname}_raw.txt"
            fpath = os.path.join(RESULTS, fname)

            if not os.path.exists(fpath):
                results[key] = {"syntax": False, "exec": False, "fidelity": 0,
                                "pass": False, "code": "", "error": "文件不存在"}
                continue

            with open(fpath) as f:
                raw = f.read()

            code = extract_code(raw)
            if not code:
                results[key] = {"syntax": False, "exec": False, "fidelity": 0,
                                "pass": False, "code": "", "error": "无法提取代码"}
                continue

            # Syntax check
            clean = re.sub(r'print\(.*?\)', '', code)
            try:
                compile(clean, '<string>', 'exec')
            except SyntaxError as e:
                results[key] = {"syntax": False, "exec": False, "fidelity": 0,
                                "pass": False, "code": code, "error": f"语法错误: {e}"}
                continue

            # Execution check
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

            # Fidelity check
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

# ── Generate summary report ─────────────────────────────────────────
L = []
L.append("=" * 80)
L.append("  QCV Phase 2 Intermediate 结果汇总")
L.append("  日期: 2026-03-25")
L.append("  执行方式: kiro-cli chat --no-interactive --model <模型> -a \"prompt\"")
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
        L.append(f"{'用例':<30s} {'语法':>4s} {'执行':>4s} {'Fidelity':>10s} {'通过':>4s}  备注")
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
            short = cname.replace("inter_", "")
            L.append(f"{short:<30s} {syn:>4s} {exe:>4s} {fid:>10s} {pas:>4s}  {note}")

        L.append("")
        L.append(f"Pass Rate: {pc}/10 = {pc*10}%")

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
        L.append(f"{lbl:<35s} {p}/10 = {p*10}%")

L.append("")
L.append("=" * 80)
L.append("错误类型分析")
L.append("=" * 80)
for model in MODELS:
    for mode in MODES:
        fails = [(c, results[(model, mode, c)]) for c in CIRCUIT_NAMES if not results[(model, mode, c)]["pass"]]
        if fails:
            L.append("")
            L.append(f"claude-{model} {'BV' if mode == 'bv' else 'TV'} 失败用例:")
            for c, r in fails:
                L.append(f"  {c.replace('inter_','')}: {r['error']}")

L.append("")
L.append("=" * 80)

report = "\n".join(L)
print(report)

out = os.path.join(RESULTS, "intermediate_results_summary.txt")
with open(out, "w") as f:
    f.write(report)
print(f"\n>>> 报告已写入: {out}")
