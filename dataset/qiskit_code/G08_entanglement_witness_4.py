from qiskit import QuantumCircuit
circuit = QuantumCircuit(4)
circuit.h(0).cx(0, 1)
circuit.h(2).cx(2, 3)
circuit.cx(1, 2)
circuit.h(1)
