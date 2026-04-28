import math
from qiskit import QuantumCircuit
circuit = QuantumCircuit(9)
circuit.h(0).cx(0, 1)
circuit.h(2).cx(2, 3)
circuit.cx(1, 2).h(1)
circuit.ry(math.pi/8, 4).ry(math.pi/4, 5)
circuit.cx(0, 4).cx(3, 5)
