from braket.circuits import Circuit

circuit = Circuit()
circuit.h(0).h(1).h(2).h(3)

print(circuit)
