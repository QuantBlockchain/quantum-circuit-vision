from qiskit import QuantumCircuit
circuit = QuantumCircuit(4)
circuit.x(0)
circuit.h(1)
circuit.x(2).h(2)
circuit.h(3)
