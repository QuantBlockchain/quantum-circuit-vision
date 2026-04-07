import math
from braket.circuits import Circuit

circuit = Circuit()

# Layer 1: H gates
circuit.h(0).h(3).h(4).h(5)

# Layer 2: CNOT q0->q1, q0->q2
circuit.cnot(0, 1)
circuit.cnot(0, 2)

# Layer 3: CNOT q3->q1, CNOT q4->q0
circuit.cnot(3, 1)
circuit.cnot(4, 0)

# Layer 4: CNOT q5->q2
circuit.cnot(5, 2)

# CRz(pi/6): q1 controls Rz(pi/6) on q4
a = math.pi / 6
circuit.rz(4, a / 2)
circuit.cnot(1, 4)
circuit.rz(4, -a / 2)
circuit.cnot(1, 4)

# H on q4
circuit.h(4)

# CRz(pi/4): q0 controls Rz(pi/4) on q3
a = math.pi / 4
circuit.rz(3, a / 2)
circuit.cnot(0, 3)
circuit.rz(3, -a / 2)
circuit.cnot(0, 3)

# CRz(pi/8): q2 controls Rz(pi/8) on q5
a = math.pi / 8
circuit.rz(5, a / 2)
circuit.cnot(2, 5)
circuit.rz(5, -a / 2)
circuit.cnot(2, 5)

# Final H gates
circuit.h(3)
circuit.h(5)

print(circuit)
