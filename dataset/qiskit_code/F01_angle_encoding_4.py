import math
from qiskit import QuantumCircuit
angles = [math.pi/3, math.pi/4, math.pi/5, math.pi/6]
circuit = QuantumCircuit(1)
for i in range(4):
    circuit.rx(angles[i], i)
