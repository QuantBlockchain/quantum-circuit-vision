import math
from braket.circuits import Circuit
circuit = Circuit()
circuit.h(0).h(1).h(2)
circuit.ry(0, math.pi / 4).ry(1, math.pi / 5).ry(2, math.pi / 6)
circuit.cnot(0, 1).cnot(1, 2)
circuit.ry(0, math.pi / 3).ry(1, math.pi / 4).ry(2, math.pi / 5)
