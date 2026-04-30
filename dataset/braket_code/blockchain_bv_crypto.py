from braket.circuits import Circuit

circuit = Circuit()

circuit.h(0)
circuit.h(1)
circuit.x(2)
circuit.h(1)
circuit.h(2)
circuit.cnot(0, 2)
circuit.h(0)

print(circuit)
