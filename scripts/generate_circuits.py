"""生成 5 张 Demo 量子电路图 PNG"""
from qiskit import QuantumCircuit
import os

OUT = os.path.join(os.path.dirname(__file__), "circuits")
os.makedirs(OUT, exist_ok=True)

circuits = {
    "demo_01_hadamard": QuantumCircuit(1),
    "demo_02_cnot": QuantumCircuit(2),
    "demo_03_bell": QuantumCircuit(2),
    "demo_04_ghz": QuantumCircuit(3),
    "demo_05_toffoli": QuantumCircuit(3),
}

circuits["demo_01_hadamard"].h(0)
circuits["demo_02_cnot"].cx(0, 1)
circuits["demo_03_bell"].h(0); circuits["demo_03_bell"].cx(0, 1)
circuits["demo_04_ghz"].h(0); circuits["demo_04_ghz"].cx(0, 1); circuits["demo_04_ghz"].cx(0, 2)
circuits["demo_05_toffoli"].ccx(0, 1, 2)

for name, qc in circuits.items():
    fig = qc.draw("mpl", style="iqp")
    path = os.path.join(OUT, f"{name}.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    print(f"✓ {path}")
    import matplotlib.pyplot as plt
    plt.close(fig)

print(f"\n共生成 {len(circuits)} 张电路图")
