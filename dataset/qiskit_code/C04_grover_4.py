from qiskit import QuantumCircuit
circuit = QuantumCircuit(3)
circuit.h(0).h(1)
circuit.h(1).ccx(0, 1, 2).h(1)
circuit.h(0).h(1).x(0).x(1)
circuit.h(1).cx(0, 1).h(1)
circuit.x(0).x(1).h(0).h(1)
