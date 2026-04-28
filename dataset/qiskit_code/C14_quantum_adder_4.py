from qiskit import QuantumCircuit
circuit = QuantumCircuit(4)
circuit.ccx(0, 2, 3)
circuit.cx(0, 2)
circuit.ccx(1, 2, 3)
