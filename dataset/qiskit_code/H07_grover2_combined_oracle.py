from qiskit import QuantumCircuit
circuit = QuantumCircuit(2)
circuit.h(0).h(1)
circuit.cz(0, 1)
circuit.h(0).h(1).z(0).z(1).cz(0, 1).h(0).h(1)
