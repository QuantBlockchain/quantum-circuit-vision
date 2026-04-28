import math
from qiskit import QuantumCircuit
circuit = QuantumCircuit(10)
circuit.rz(math.pi/3, 0).rz(math.pi/5, 1).rz(math.pi/7, 2).rz(math.pi/9, 3)
circuit.cx(0, 1).cx(1, 2).cx(2, 3)
circuit.rz(math.pi/4, 0).rz(math.pi/6, 2)
