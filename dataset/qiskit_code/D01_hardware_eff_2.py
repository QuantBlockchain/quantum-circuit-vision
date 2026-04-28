import math
from qiskit import QuantumCircuit
circuit = QuantumCircuit(11)
circuit.ry(math.pi/4, 0).rz(math.pi/3, 0)
circuit.ry(math.pi/5, 1).rz(math.pi/6, 1)
circuit.cx(0, 1)
circuit.ry(math.pi/7, 0).rz(math.pi/8, 0)
circuit.ry(math.pi/9, 1).rz(math.pi/10, 1)
