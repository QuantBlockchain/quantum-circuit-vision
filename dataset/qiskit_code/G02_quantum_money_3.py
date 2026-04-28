from qiskit import QuantumCircuit
circuit = QuantumCircuit(3)
circuit.h(0)
circuit.x(1)
circuit.h(2).s(2)
