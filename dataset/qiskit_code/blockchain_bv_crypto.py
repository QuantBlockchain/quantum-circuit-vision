from qiskit import QuantumCircuit
circuit = QuantumCircuit(3)

circuit.h(0)
circuit.h(1)
circuit.x(2)
circuit.h(1)
circuit.h(2)
circuit.cx(0, 2)
circuit.h(0)

print(circuit)
