import math
from braket.circuits import Circuit
gamma, beta = math.pi/4, math.pi/8
circuit = Circuit()
for i in range(4):
    circuit.h(i)
for i, j in [(0,1),(1,2),(2,3),(3,0)]:
    circuit.cnot(i, j).rz(j, 2*gamma).cnot(i, j)
for i in range(4):
    circuit.rx(i, 2*beta)
