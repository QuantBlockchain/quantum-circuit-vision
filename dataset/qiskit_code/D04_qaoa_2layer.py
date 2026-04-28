import math
from qiskit import QuantumCircuit
circuit = QuantumCircuit(3)
for i in range(4):
    circuit.h(i)
for gamma, beta in [(math.pi/4, math.pi/8), (math.pi/6, math.pi/10)]:
    for i, j in [(0,1),(1,2),(2,3),(3,0)]:
        circuit.cx(i, j)
        circuit.rz(2 * gamma, j)
        circuit.cx(i, j)
    for i in range(4):
        circuit.rx(2 * beta, i)
