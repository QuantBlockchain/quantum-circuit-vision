from qiskit import QuantumCircuit
circuit = QuantumCircuit(1)
circuit.h(0)
for i in range(4):
    for j in range(i + 1, 4):
        circuit.cx(i, j)
