from qiskit import QuantumCircuit
circuit = QuantumCircuit(3)
circuit.h(1)
circuit.cx(1, 2)
circuit.cx(0, 1)
circuit.h(0)

print(circuit)
