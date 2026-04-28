import math
from qiskit import QuantumCircuit

circuit = QuantumCircuit(6)

# Layer 1: H gates
circuit.h(0).h(3).h(4).h(5)

# Layer 2: CNOT q0->q1, q0->q2
circuit.cx(0, 1)
circuit.cx(0, 2)

# Layer 3: CNOT q3->q1, CNOT q4->q0
circuit.cx(3, 1)
circuit.cx(4, 0)

# Layer 4: CNOT q5->q2
circuit.cx(5, 2)

# CRz(pi/6): q1 controls Rz(pi/6) on q4
a = math.pi / 6
circuit.rz(a / 2, 4)
circuit.cx(1, 4)
circuit.rz(-a / 2, 4)
circuit.cx(1, 4)

# H on q4
circuit.h(4)

# CRz(pi/4): q0 controls Rz(pi/4) on q3
a = math.pi / 4
circuit.rz(a / 2, 3)
circuit.cx(0, 3)
circuit.rz(-a / 2, 3)
circuit.cx(0, 3)

# CRz(pi/8): q2 controls Rz(pi/8) on q5
a = math.pi / 8
circuit.rz(a / 2, 5)
circuit.cx(2, 5)
circuit.rz(-a / 2, 5)
circuit.cx(2, 5)

# Final H gates
circuit.h(3)
circuit.h(5)

print(circuit)
