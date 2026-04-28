from qiskit import QuantumCircuit
circuit = QuantumCircuit(5)
for i in range(4):
    circuit.h(i)
circuit.x(4).h(4)
circuit.cx(0, 4).cx(1, 4).ccx(2, 3, 4)
for i in range(4):
    circuit.h(i)
for i in range(4):
    circuit.x(i)
circuit.h(3).ccx(0, 1, 2).cx(2, 3).h(3)
for i in range(4):
    circuit.x(i)
for i in range(4):
    circuit.h(i)
