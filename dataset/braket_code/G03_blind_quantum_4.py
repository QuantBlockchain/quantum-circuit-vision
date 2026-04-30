import math
from braket.circuits import Circuit
circuit = Circuit()
circuit.rz(0, math.pi/3).rz(1, math.pi/5).rz(2, math.pi/7).rz(3, math.pi/9)
circuit.cnot(0, 1).cnot(1, 2).cnot(2, 3)
circuit.rz(0, math.pi/4).rz(2, math.pi/6)
