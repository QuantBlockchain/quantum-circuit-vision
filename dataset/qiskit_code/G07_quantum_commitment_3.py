import math
from qiskit import QuantumCircuit
circuit = QuantumCircuit(5)
circuit.h(0)
circuit.cx(0, 1).cx(0, 2)
circuit.rz(math.pi / 4, 0)
