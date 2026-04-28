from qiskit import QuantumCircuit
circuit = QuantumCircuit(2)

# Initial Hadamard
circuit.h(0).h(1)

# Oracle: CZ
circuit.cz(0, 1)

# Diffusion operator
circuit.h(0).h(1)
circuit.z(0).z(1)
circuit.cz(0, 1)
circuit.h(0).h(1)

print(circuit)
