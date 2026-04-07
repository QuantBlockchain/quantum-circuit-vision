import math
from braket.circuits import Circuit
circuit = Circuit()
circuit.rx(0, math.pi/4).rx(1, math.pi/5)
circuit.cnot(0, 1)
circuit.rx(0, math.pi/3).rx(1, math.pi/6)
circuit.cnot(0, 1)
