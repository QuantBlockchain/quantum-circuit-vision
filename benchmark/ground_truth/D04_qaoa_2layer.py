import math
from braket.circuits import Circuit
circuit = Circuit()
for i in range(4):
    circuit.h(i)
for gamma, beta in [(math.pi/4, math.pi/8), (math.pi/6, math.pi/10)]:
    for i, j in [(0,1),(1,2),(2,3),(3,0)]:
        circuit.cnot(i, j)
        circuit.rz(j, 2 * gamma)
        circuit.cnot(i, j)
    for i in range(4):
        circuit.rx(i, 2 * beta)
