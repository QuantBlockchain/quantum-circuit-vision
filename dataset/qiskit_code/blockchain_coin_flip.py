import math
from qiskit import QuantumCircuit

circuit = QuantumCircuit(5)

circuit.h(0)
circuit.cx(0, 1)
circuit.rz(math.pi / 4, 0)
circuit.h(1)
circuit.h(0)
circuit.cx(0, 2)
circuit.cx(1, 2)

print(circuit)
