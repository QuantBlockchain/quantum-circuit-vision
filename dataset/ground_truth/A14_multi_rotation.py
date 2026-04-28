import math
from braket.circuits import Circuit
circuit = Circuit()
circuit.rx(0, math.pi / 4)
circuit.ry(0, math.pi / 3)
circuit.rz(0, math.pi / 6)
circuit.cnot(0, 1)
