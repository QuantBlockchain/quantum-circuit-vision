from qiskit import QuantumCircuit
# Toffoli decomposition into 1/2-qubit gates
circuit = QuantumCircuit(3)
circuit.h(2)
circuit.cx(1, 2).tdg(2).cx(0, 2)
circuit.t(2).cx(1, 2).tdg(2).cx(0, 2)
circuit.t(1).t(2).h(2)
circuit.cx(0, 1).t(0).tdg(1).cx(0, 1)
