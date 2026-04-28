import math
from qiskit import QuantumCircuit
circuit = QuantumCircuit(8)
circuit.h(0).cx(0, 2).cx(0, 4)
circuit.rz(math.pi/3, 1).rz(math.pi/5, 3).rz(math.pi/7, 5)
circuit.cx(0, 1).cx(2, 3).cx(4, 5)
circuit.h(0).h(2).h(4)
