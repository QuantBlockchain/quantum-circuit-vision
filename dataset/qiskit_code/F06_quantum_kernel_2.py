import math
from qiskit import QuantumCircuit
circuit = QuantumCircuit(6)
circuit.h(0).h(1)
circuit.rz(math.pi / 4, 0).rz(math.pi / 3, 1)
circuit.cx(0, 1).rz(math.pi / 5, 1).cx(0, 1)
circuit.h(0).h(1)
