import math
from qiskit import QuantumCircuit
# Braket 没有原生 CRx，用分解: Rz(-π/2)-CNOT-Rz(π/2)-Ry(-θ/2)-CNOT-Ry(θ/2)
# 等价分解: Rx(θ/2)-CNOT-Rx(-θ/2)-CNOT (简化)
theta = math.pi / 3
circuit = QuantumCircuit(3)
circuit.rx(theta / 2, 1)
circuit.cx(0, 1)
circuit.rx(-theta / 2, 1)
circuit.cx(0, 1)
