import math
from qiskit import QuantumCircuit

circuit = QuantumCircuit(8)

# Layer 1: Hadamard gates
circuit.h(0).h(1).h(3).h(5)

# Layer 2: CNOT(1,2), CNOT(5,6)
circuit.cx(1, 2).cx(5, 6)

# Layer 3: Rz on q2, CNOT(0,1), CNOT(1,4)
circuit.rz(math.pi / 3, 2).cx(0, 1).cx(1, 4)

# Layer 4: Rz on q4, CNOT(0,3), Rz on q6
circuit.rz(math.pi / 5, 4).cx(0, 3).rz(math.pi / 7, 6)

# Layer 5: H on q1, H on q3
circuit.h(1).h(3)

# Layer 6: CNOT(0,5)
circuit.cx(0, 5)

# Layer 7: H on q5
circuit.h(5)

print(circuit)
