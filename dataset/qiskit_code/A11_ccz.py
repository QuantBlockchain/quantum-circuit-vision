from qiskit import QuantumCircuit
# CCZ = H(2)-CCX-H(2)
circuit = QuantumCircuit(3)
circuit.h(2)
circuit.ccx(0, 1, 2)
circuit.h(2)
