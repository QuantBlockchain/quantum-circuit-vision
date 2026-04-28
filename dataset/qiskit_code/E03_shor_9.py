from qiskit import QuantumCircuit
circuit = QuantumCircuit(9)
circuit.cx(0, 3).cx(0, 6)
circuit.h(0).h(3).h(6)
circuit.cx(0, 1).cx(0, 2)
circuit.cx(3, 4).cx(3, 5)
circuit.cx(6, 7).cx(6, 8)
