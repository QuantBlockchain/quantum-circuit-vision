import math
from braket.circuits import Circuit
circuit = Circuit()
circuit.ry(0, math.pi/3).ry(1, math.pi/4).ry(2, math.pi/5).ry(3, math.pi/6)
circuit.cnot(0, 2).cnot(1, 3)
circuit.ccnot(2, 3, 0)
