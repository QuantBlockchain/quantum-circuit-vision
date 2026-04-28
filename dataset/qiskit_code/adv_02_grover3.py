from qiskit import QuantumCircuit
circuit = QuantumCircuit(3)
circuit.h(0).h(1).h(2)
circuit.h(2).ccx(0, 1, 2).h(2)
circuit.h(0).h(1).h(2)
circuit.x(0).x(1).x(2)
circuit.h(2).ccx(0, 1, 2).h(2)
circuit.x(0).x(1).x(2)
circuit.h(0).h(1).h(2)
