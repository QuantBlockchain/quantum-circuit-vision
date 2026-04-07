import math
from braket.circuits import Circuit
circuit = Circuit().rx(0, math.pi/3).rz(1, math.pi/4).cnot(0, 1)
