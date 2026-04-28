import math
from qiskit import QuantumCircuit

circuit = QuantumCircuit(8)

# Layer 1: H gates
circuit.h([0, 2, 4, 6])

# Layer 2: CNOT pairs
circuit.cx(0, 1).cx(2, 3).cx(4, 5).cx(6, 7)

# Layer 3: CNOT chain
circuit.cx(1, 2).cx(3, 4).cx(5, 6)

# Layer 4: CNOT wrap-around
circuit.cx(7, 0)

# Layer 5: Rz(pi/4)
circuit.rz([0, 2, 4, 6], math.pi / 4)

# Layer 6: H gates
circuit.h([0, 2, 4, 6])

print(circuit)
