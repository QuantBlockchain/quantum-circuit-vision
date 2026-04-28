from qiskit import QuantumCircuit
circuit = QuantumCircuit(2)
circuit.s(0)
circuit.t(0)
circuit.cx(0, 1)
circuit.tdg(0)
circuit.sdg(0)
