"""Phase 2: 生成 Intermediate 级别量子电路图"""
from qiskit import QuantumCircuit
import numpy as np, os

OUT = os.path.join(os.path.dirname(__file__), "circuits")
os.makedirs(OUT, exist_ok=True)

circuits = {}

# I01: SWAP 分解 (3 CNOT = 1 SWAP)
c = QuantumCircuit(2); c.cx(0,1); c.cx(1,0); c.cx(0,1)
circuits["inter_01_swap_decomp"] = c

# I02: 2-qubit QFT
c = QuantumCircuit(2); c.h(0); c.cp(np.pi/2, 1, 0); c.h(1); c.swap(0,1)
circuits["inter_02_qft2"] = c

# I03: 量子隐形传态
c = QuantumCircuit(3); c.h(1); c.cx(1,2); c.cx(0,1); c.h(0)
circuits["inter_03_teleport_prep"] = c

# I04: Deutsch 算法 (balanced oracle)
c = QuantumCircuit(2); c.x(1); c.h(0); c.h(1); c.cx(0,1); c.h(0)
circuits["inter_04_deutsch"] = c

# I05: 超密编码
c = QuantumCircuit(2); c.h(0); c.cx(0,1); c.x(0); c.z(0); c.cx(0,1); c.h(0)
circuits["inter_05_superdense"] = c

# I06: Grover 2-qubit (oracle for |11⟩)
c = QuantumCircuit(2); c.h(0); c.h(1); c.cz(0,1); c.h(0); c.h(1); c.z(0); c.z(1); c.cz(0,1); c.h(0); c.h(1)
circuits["inter_06_grover2"] = c

# I07: 带参数旋转 Rz(π/4) + Rx(π/3)
c = QuantumCircuit(2); c.rx(np.pi/3, 0); c.rz(np.pi/4, 1); c.cx(0,1)
circuits["inter_07_param_rot"] = c

# I08: Fredkin (CSWAP)
c = QuantumCircuit(3); c.cswap(0,1,2)
circuits["inter_08_fredkin"] = c

# I09: 移位寄存器 (DFF chain analog: CNOT cascade)
c = QuantumCircuit(4); c.x(0); c.cx(0,1); c.cx(1,2); c.cx(2,3)
circuits["inter_09_shift_reg"] = c

# I10: 相位估计核心 (controlled-Rz)
c = QuantumCircuit(3); c.h(0); c.h(1); c.crz(np.pi/2, 0, 2); c.crz(np.pi/4, 1, 2); c.h(0); c.h(1)
circuits["inter_10_phase_est"] = c

for name, qc in circuits.items():
    fig = qc.draw("mpl", style="iqp")
    path = os.path.join(OUT, f"{name}.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    print(f"✓ {path}")
    import matplotlib.pyplot as plt
    plt.close(fig)

print(f"\n共生成 {len(circuits)} 张 Intermediate 电路图")
