from qiskit import QuantumCircuit
circuit = QuantumCircuit(8)
circuit.rx(0.7, 0)
circuit.cx(0, 1)
circuit.ry(1.2, 1)
