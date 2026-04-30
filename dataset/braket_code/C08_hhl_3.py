import math
from braket.circuits import Circuit
circuit = Circuit()
circuit.ry(2, math.pi / 3)
circuit.h(1)
circuit.cphaseshift(1, 2, math.pi / 2)
circuit.h(1)
# controlled Ry on ancilla
circuit.ry(0, math.pi / 8)
circuit.cnot(1, 0)
circuit.ry(0, -math.pi / 8)
circuit.cnot(1, 0)
