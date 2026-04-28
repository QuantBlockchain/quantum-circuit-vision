import math
from braket.circuits import Circuit
circuit = Circuit().h(0).cphaseshift(0, 1, math.pi/2).h(1).swap(0, 1)
