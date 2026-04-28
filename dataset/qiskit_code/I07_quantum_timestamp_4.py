import math
from qiskit import QuantumCircuit
circuit = QuantumCircuit(5)
circuit.h(0).h(1)
circuit.cx(0, 2).cx(1, 3)
circuit.rz(math.pi/4, 2).rz(math.pi/3, 3)
circuit.h(0).h(1)
