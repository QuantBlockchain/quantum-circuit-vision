from qiskit import QuantumCircuit
circuit = QuantumCircuit(3)
circuit.h(2)
circuit.cx(2, 1).cx(2, 0)
