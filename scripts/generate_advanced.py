"""Phase 3: 生成 Advanced 级别量子电路图 (A01-A06)"""
from qiskit import QuantumCircuit
import numpy as np, os

OUT = os.path.join(os.path.dirname(__file__), "circuits")
os.makedirs(OUT, exist_ok=True)

circuits = {}

# A01: 3-qubit QFT — 多层控制旋转 + SWAP
c = QuantumCircuit(3)
c.h(0)
c.cp(np.pi/2, 1, 0)
c.cp(np.pi/4, 2, 0)
c.h(1)
c.cp(np.pi/2, 2, 1)
c.h(2)
c.swap(0, 2)
circuits["adv_01_qft3"] = c

# A02: Grover 3-qubit (oracle marks |111⟩, 1 iteration)
c = QuantumCircuit(3)
# Init
c.h(0); c.h(1); c.h(2)
# Oracle: CCZ = H(2) CCX(0,1,2) H(2)
c.h(2); c.ccx(0, 1, 2); c.h(2)
# Diffusion: H⊗3 → X⊗3 → CCZ → X⊗3 → H⊗3
c.h(0); c.h(1); c.h(2)
c.x(0); c.x(1); c.x(2)
c.h(2); c.ccx(0, 1, 2); c.h(2)
c.x(0); c.x(1); c.x(2)
c.h(0); c.h(1); c.h(2)
circuits["adv_02_grover3"] = c

# A03: VQE ansatz — 4-qubit hardware-efficient ansatz, fixed params
c = QuantumCircuit(4)
angles = [np.pi/4, np.pi/3, np.pi/6, np.pi/5]
for i in range(4):
    c.ry(angles[i], i)
for i in range(3):
    c.cx(i, i+1)
for i in range(4):
    c.ry(angles[3-i], i)
circuits["adv_03_vqe_ansatz"] = c

# A04: QAOA 单层 — 4-qubit MaxCut on ring graph, fixed γ=π/4, β=π/8
c = QuantumCircuit(4)
# Init
for i in range(4):
    c.h(i)
# Problem unitary: ZZ on edges (0,1),(1,2),(2,3),(3,0)
gamma = np.pi/4
for i, j in [(0,1),(1,2),(2,3),(3,0)]:
    c.cx(i, j)
    c.rz(2*gamma, j)
    c.cx(i, j)
# Mixer: Rx(2β) on each qubit
beta = np.pi/8
for i in range(4):
    c.rx(2*beta, i)
circuits["adv_04_qaoa"] = c

# A05: 量子随机行走 — 1 coin qubit + 3 position qubits, 1 step
c = QuantumCircuit(4)
# Coin flip
c.h(0)
# Conditional shift: if coin=1, increment position
c.cx(0, 1)
c.ccx(0, 1, 2)
# Coin flip again
c.h(0)
circuits["adv_05_qwalk"] = c

# A06: Bernstein-Vazirani — secret string s=1011, 4 qubits + 1 ancilla
c = QuantumCircuit(5)
# Ancilla in |−⟩
c.x(4); c.h(4)
# Hadamard on input qubits
for i in range(4):
    c.h(i)
# Oracle: CNOT from qubit i to ancilla where s[i]=1 (s=1011 → bits 0,1,3)
c.cx(0, 4)
c.cx(1, 4)
c.cx(3, 4)
# Hadamard on input qubits
for i in range(4):
    c.h(i)
circuits["adv_06_bv"] = c

for name, qc in circuits.items():
    fig = qc.draw("mpl", style="iqp")
    path = os.path.join(OUT, f"{name}.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    print(f"✓ {path}")
    import matplotlib.pyplot as plt
    plt.close(fig)

print(f"\n共生成 {len(circuits)} 张 Advanced 电路图")
