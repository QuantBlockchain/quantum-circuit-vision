import math
from braket.circuits import Circuit
circuit = (Circuit()
    .h(0)
    .cphaseshift(1, 0, math.pi/2)
    .cphaseshift(2, 0, math.pi/4)
    .h(1)
    .cphaseshift(2, 1, math.pi/2)
    .h(2)
    .swap(0, 2))
