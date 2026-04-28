import math
from qiskit import QuantumCircuit
# iSWAP = SWAP · (CZ on both directions) = specific decomposition
# iSWAP matrix: |00⟩→|00⟩, |01⟩→i|10⟩, |10⟩→i|01⟩, |11⟩→|11⟩
circuit = QuantumCircuit(2)
circuit.s(0)
circuit.s(1)
circuit.h(0)
circuit.cx(0, 1)
circuit.cx(1, 0)
circuit.h(1)
