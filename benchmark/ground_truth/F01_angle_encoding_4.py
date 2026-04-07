import math
from braket.circuits import Circuit
angles = [math.pi/3, math.pi/4, math.pi/5, math.pi/6]
circuit = Circuit()
for i in range(4):
    circuit.rx(i, angles[i])
