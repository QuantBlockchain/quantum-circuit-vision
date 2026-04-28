import math
from braket.circuits import Circuit
# Braket 没有原生 CRy，用分解: Ry(θ/2)-CNOT-Ry(-θ/2)-CNOT
theta = math.pi / 4
circuit = Circuit()
circuit.ry(1, theta / 2)
circuit.cnot(0, 1)
circuit.ry(1, -theta / 2)
circuit.cnot(0, 1)
