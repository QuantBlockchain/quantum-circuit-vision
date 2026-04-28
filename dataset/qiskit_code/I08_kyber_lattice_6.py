import math
from qiskit import QuantumCircuit
circuit = QuantumCircuit(6)
for i in range(3):
    circuit.h(i)
circuit.cx(0, 3).rz(math.pi/4, 3)
circuit.cx(1, 4).rz(math.pi/3, 4)
circuit.cx(2, 5).rz(math.pi/5, 5)
circuit.cx(3, 4).cx(4, 5).cx(5, 3)
circuit.h(3).h(4).h(5)
