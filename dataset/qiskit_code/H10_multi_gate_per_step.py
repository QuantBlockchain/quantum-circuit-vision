from qiskit import QuantumCircuit
circuit = QuantumCircuit(4)
circuit.h(0).h(1).h(2).h(3)
circuit.cx(0, 1).cx(2, 3)
circuit.cx(1, 2)
circuit.h(0).h(1).h(2).h(3)
