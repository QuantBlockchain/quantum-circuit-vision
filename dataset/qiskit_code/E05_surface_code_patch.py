from qiskit import QuantumCircuit
circuit = QuantumCircuit(9)
circuit.h(4).cx(4, 0).cx(4, 1).h(4)
circuit.h(5).cx(5, 2).cx(5, 3).h(5)
circuit.cx(0, 6).cx(2, 6)
circuit.cx(1, 7).cx(3, 7)
circuit.cx(0, 8).cx(1, 8)
