from qiskit import QuantumCircuit
circuit = QuantumCircuit(5)
circuit.h(0).h(2)
circuit.cx(0, 1).cx(2, 3)
circuit.cx(1, 4).cx(3, 4)
circuit.h(4)
circuit.ccx(0, 2, 4)
