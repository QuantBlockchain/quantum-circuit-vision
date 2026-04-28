from qiskit import QuantumCircuit
circuit = QuantumCircuit(5)
circuit.cx(0, 1).cx(0, 2).cx(0, 3).cx(0, 4)
