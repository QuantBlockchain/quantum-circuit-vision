import math
from qiskit import QuantumCircuit
circuit = QuantumCircuit(6)
circuit.h(0).h(1).h(2)
circuit.cx(0, 3).cx(1, 4).cx(2, 5)
circuit.rz(math.pi/4, 3).rz(math.pi/3, 4).rz(math.pi/5, 5)
circuit.cx(3, 4).cx(4, 5).cx(5, 3)
circuit.h(3).h(4).h(5)
