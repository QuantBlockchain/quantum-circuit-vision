import math
from qiskit import QuantumCircuit
# Braket 没有原生 CRy，用分解: Ry(θ/2)-CNOT-Ry(-θ/2)-CNOT
theta = math.pi / 4
circuit = QuantumCircuit(3)
circuit.ry(theta / 2, 1)
circuit.cx(0, 1)
circuit.ry(-theta / 2, 1)
circuit.cx(0, 1)
