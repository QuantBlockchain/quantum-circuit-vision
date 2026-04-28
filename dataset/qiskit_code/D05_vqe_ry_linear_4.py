import math
from qiskit import QuantumCircuit
angles = [math.pi/3, math.pi/4, math.pi/5, math.pi/6]
circuit = QuantumCircuit(2)
for i in range(4):
    circuit.ry(angles[i], i)
for i in range(3):
    circuit.cx(i, i + 1)
