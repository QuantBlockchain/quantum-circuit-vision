from qiskit import QuantumCircuit
circuit = QuantumCircuit(4)
circuit.x(3).h(0).h(1).h(2).h(3)
circuit.cx(0, 3).cx(2, 3)
circuit.h(0).h(1).h(2)
