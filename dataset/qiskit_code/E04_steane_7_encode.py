from qiskit import QuantumCircuit
circuit = QuantumCircuit(7)
circuit.h(0).h(1).h(2)
circuit.cx(0, 3).cx(0, 4).cx(0, 5)
circuit.cx(1, 3).cx(1, 5).cx(1, 6)
circuit.cx(2, 4).cx(2, 5).cx(2, 6)
