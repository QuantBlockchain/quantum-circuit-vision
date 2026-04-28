import math
from qiskit import QuantumCircuit
angles = [math.pi/4, math.pi/3, math.pi/6, math.pi/5]
circuit = QuantumCircuit(4)
for i in range(4):
    circuit.ry(angles[i], i)
for i in range(3):
    circuit.cx(i, i + 1)
for i in range(4):
    circuit.ry(angles[3 - i], i)
