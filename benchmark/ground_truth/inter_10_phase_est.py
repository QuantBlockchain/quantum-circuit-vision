import math
from braket.circuits import Circuit
circuit = Circuit().h(0).h(1).cphaseshift(0, 2, math.pi/2).cphaseshift(1, 2, math.pi/4).h(0).h(1)
