from qiskit import QuantumCircuit
circuit = QuantumCircuit(4)
circuit.x(0).x(2)
circuit.h(0).h(2)
circuit.cx(0, 1).cx(2, 3)
circuit.h(0).h(2)
