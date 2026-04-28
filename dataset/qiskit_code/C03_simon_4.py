from qiskit import QuantumCircuit
circuit = QuantumCircuit(4)
circuit.h(0).h(1)
circuit.cx(0, 2).cx(0, 3).cx(1, 2).cx(1, 3)
circuit.h(0).h(1)
