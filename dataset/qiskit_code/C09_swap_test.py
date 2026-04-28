from qiskit import QuantumCircuit
circuit = QuantumCircuit(3)
circuit.h(0)
circuit.cswap(0, 1, 2)
circuit.h(0)
