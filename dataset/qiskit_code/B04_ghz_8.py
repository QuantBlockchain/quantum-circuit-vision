from qiskit import QuantumCircuit
circuit = QuantumCircuit(1)
circuit.h(0)
for i in range(1, 8):
    circuit.cx(0, i)
