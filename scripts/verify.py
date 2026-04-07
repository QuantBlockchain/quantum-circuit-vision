"""验证生成的 Braket 代码是否正确"""
import numpy as np
import sys, ast, importlib, tempfile, os

# Ground truth 态向量 (输入全 |0⟩)
GROUND_TRUTH = {
    "demo_01_hadamard": np.array([1, 1]) / np.sqrt(2),
    "demo_02_cnot": np.array([1, 0, 0, 0]),  # |00⟩ → |00⟩
    "demo_03_bell": np.array([1, 0, 0, 1]) / np.sqrt(2),
    "demo_04_ghz": np.array([1, 0, 0, 0, 0, 0, 0, 1]) / np.sqrt(2),
    "demo_05_toffoli": np.array([1, 0, 0, 0, 0, 0, 0, 0]),  # |000⟩ → |000⟩
}

def check_syntax(code_str):
    """Level 1: Python 语法检查"""
    try:
        ast.parse(code_str)
        return True, None
    except SyntaxError as e:
        return False, str(e)

def execute_and_get_statevector(code_str):
    """Level 2+3: 执行并获取态向量"""
    from braket.devices import LocalSimulator
    from braket.circuits import Circuit

    # 写入临时文件执行
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        # 包装代码, 捕获 Circuit 对象
        wrapped = code_str + "\n"
        f.write(wrapped)
        f.flush()
        tmp = f.name

    try:
        ns = {"__builtins__": __builtins__}
        exec(compile(open(tmp).read(), tmp, 'exec'), ns)
        # 找到 Circuit 对象
        circ = None
        for v in ns.values():
            if isinstance(v, Circuit):
                circ = v
                break
        if circ is None:
            return False, "未找到 Circuit 对象", None

        device = LocalSimulator()
        result = device.run(circ, shots=0).result()
        sv = np.array(result.result_types[0].value)
        return True, None, sv
    except Exception as e:
        return False, str(e), None
    finally:
        os.unlink(tmp)

def fidelity(sv1, sv2):
    """计算态向量保真度"""
    return abs(np.dot(np.conj(sv1), sv2)) ** 2

def verify_one(demo_name, code_str):
    """验证单个用例"""
    print(f"\n{'='*60}")
    print(f"验证: {demo_name}")
    print(f"{'='*60}")

    # Level 1
    ok, err = check_syntax(code_str)
    print(f"  语法检查: {'✓' if ok else '✗ ' + err}")
    if not ok:
        return {"syntax": False, "executable": False, "correct": False}

    # Level 2+3
    ok, err, sv = execute_and_get_statevector(code_str)
    print(f"  执行检查: {'✓' if ok else '✗ ' + err}")
    if not ok:
        return {"syntax": True, "executable": False, "correct": False}

    # Fidelity
    gt = GROUND_TRUTH[demo_name]
    f = fidelity(sv, gt)
    correct = f >= 0.99
    print(f"  保真度:   {f:.4f} {'✓' if correct else '✗'}")
    return {"syntax": True, "executable": True, "correct": correct, "fidelity": f}

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python verify.py <demo_name> <code_file>")
        print("例:   python verify.py demo_03_bell results/opus_bv_demo_03.py")
        sys.exit(1)
    name = sys.argv[1]
    with open(sys.argv[2]) as f:
        code = f.read()
    verify_one(name, code)
