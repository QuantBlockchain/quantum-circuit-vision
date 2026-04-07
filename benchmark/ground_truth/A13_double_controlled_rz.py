import math
from braket.circuits import Circuit
# CCRz(π/4) decomposed
circuit = Circuit()
circuit.cnot(1, 2)
circuit.rz(2, -math.pi / 8)
circuit.cnot(0, 2)
circuit.rz(2, math.pi / 8)
circuit.cnot(1, 2)
circuit.rz(2, -math.pi / 8)
circuit.cnot(0, 2)
circuit.rz(2, math.pi / 8)
