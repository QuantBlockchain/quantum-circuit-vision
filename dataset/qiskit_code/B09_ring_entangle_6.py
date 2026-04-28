from qiskit import QuantumCircuit
circuit = QuantumCircuit(6)
circuit.h(0)
for i in range(5):
    circuit.cx(i, i + 1)
circuit.cx(5, 0)
