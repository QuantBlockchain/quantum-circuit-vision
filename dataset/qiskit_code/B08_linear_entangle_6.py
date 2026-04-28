from qiskit import QuantumCircuit
circuit = QuantumCircuit(2)
circuit.h(0)
for i in range(5):
    circuit.cx(i, i + 1)
