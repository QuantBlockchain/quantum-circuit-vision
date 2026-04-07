import math
from braket.circuits import Circuit
circuit = Circuit()
circuit.rx(0, math.pi / 4)
circuit.ry(0, math.pi / 3).ry(1, math.pi / 5)
circuit.cnot(0, 1)
circuit.ry(0, math.pi / 6).ry(1, math.pi / 7)
