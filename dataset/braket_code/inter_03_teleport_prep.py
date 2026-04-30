from braket.circuits import Circuit

circuit = Circuit()
circuit.h(1)
circuit.cnot(1, 2)
circuit.cnot(0, 1)
circuit.h(0)

print(circuit)
