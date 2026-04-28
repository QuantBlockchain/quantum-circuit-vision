from qiskit import QuantumCircuit
circuit = QuantumCircuit(4)
for i in range(3):
    circuit.h(i)
circuit.x(3).h(3)
circuit.ccx(0, 1, 3).cx(2, 3)
for i in range(3):
    circuit.h(i).x(i)
circuit.h(2).ccx(0, 1, 2).h(2)
for i in range(3):
    circuit.x(i).h(i)
