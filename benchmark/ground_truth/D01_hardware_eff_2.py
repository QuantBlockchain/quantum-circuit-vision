import math
from braket.circuits import Circuit
circuit = Circuit()
circuit.ry(0, math.pi/4).rz(0, math.pi/3)
circuit.ry(1, math.pi/5).rz(1, math.pi/6)
circuit.cnot(0, 1)
circuit.ry(0, math.pi/7).rz(0, math.pi/8)
circuit.ry(1, math.pi/9).rz(1, math.pi/10)
