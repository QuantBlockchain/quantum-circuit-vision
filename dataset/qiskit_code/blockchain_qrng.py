from qiskit import QuantumCircuit
circuit = QuantumCircuit(4)
circuit.h(0).h(1).h(2).h(3)

print(circuit)
