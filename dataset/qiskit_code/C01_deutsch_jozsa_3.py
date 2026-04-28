from qiskit import QuantumCircuit
circuit = QuantumCircuit(3)
circuit.x(2).h(0).h(1).h(2)
circuit.cx(0, 2).cx(1, 2)
circuit.h(0).h(1)
