import math
from qiskit import QuantumCircuit
gamma, beta = math.pi/4, math.pi/8
circuit = QuantumCircuit(3)
for i in range(4):
    circuit.h(i)
for i, j in [(0,1),(1,2),(2,3),(3,0)]:
    circuit.cx(i, j).rz(2*gamma, j).cx(i, j)
for i in range(4):
    circuit.rx(2*beta, i)
