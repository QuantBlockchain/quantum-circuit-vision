import math
from qiskit import QuantumCircuit
circuit = QuantumCircuit(7)
for i in range(4):
    circuit.h(i)
circuit.cx(0, 4).cx(1, 4).rz(math.pi/4, 4)
circuit.cx(2, 5).cx(3, 5).rz(math.pi/3, 5)
circuit.cx(4, 6).cx(5, 6)
circuit.h(6)
circuit.ccx(4, 5, 6)
circuit.rz(math.pi/5, 6)
