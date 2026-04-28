from qiskit import QuantumCircuit
circuit = QuantumCircuit(5)
circuit.x(4).h(4)
for i in range(4):
    circuit.h(i)
circuit.cx(0, 4).cx(1, 4).cx(3, 4)
for i in range(4):
    circuit.h(i)
