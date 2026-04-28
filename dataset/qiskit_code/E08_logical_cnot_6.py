from qiskit import QuantumCircuit
circuit = QuantumCircuit(6)
circuit.cx(0, 1).cx(0, 2)
circuit.cx(3, 4).cx(3, 5)
circuit.cx(0, 3).cx(1, 4).cx(2, 5)
