import math
from qiskit import QuantumCircuit

circuit = QuantumCircuit(5)

# Layer 1: H on q0, q1
circuit.h(0)
circuit.h(1)

# Layer 2: CNOT q0->q2, CNOT q1->q3
circuit.cx(0, 2)
circuit.cx(1, 3)

# Layer 3: H on q0, q1, q2, q3
circuit.h(0)
circuit.h(1)
circuit.h(2)
circuit.h(3)

# Layer 4: CNOT q2->q4
circuit.cx(2, 4)

# Layer 5: CNOT q3->q4
circuit.cx(3, 4)

# Layer 6: Rz(pi/3) on q4
circuit.rz(math.pi / 3, 4)

# Layer 7: CNOT q2->q4
circuit.cx(2, 4)

# Layer 8: CNOT q3->q4
circuit.cx(3, 4)

print(circuit)
