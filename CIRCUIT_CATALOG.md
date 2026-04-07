```
QCV Benchmark: 132 Quantum Circuits
====================================

GENERAL QUANTUM CIRCUITS (101)
==============================

[demo] Basic Gates (5)                    1-3 qubits
  demo_01  Hadamard                       1q   Single-qubit superposition
  demo_02  CNOT                           2q   Two-qubit entangling gate
  demo_03  Bell State                     2q   H + CNOT
  demo_04  GHZ State                      3q   H + 2xCNOT
  demo_05  Toffoli                        3q   CCX (3-qubit controlled)

[inter] Intermediate (10)                 2-4 qubits
  inter_01  SWAP Decomposition            2q   3xCNOT = SWAP
  inter_02  2-Qubit QFT                   2q   H + CPhase + SWAP
  inter_03  Teleportation Prep            3q   Bell pair + CNOT + H
  inter_04  Deutsch Algorithm             2q   Oracle + Hadamard test
  inter_05  Superdense Coding             2q   2 classical bits via 1 qubit
  inter_06  2-Qubit Grover                2q   Oracle + Diffusion
  inter_07  Parameterized Rotation        2q   Rx + Rz + CNOT
  inter_08  Fredkin (CSWAP)               3q   Controlled-SWAP
  inter_09  Shift Register                4q   CNOT chain
  inter_10  Phase Estimation              3q   CPhase + inverse QFT

[adv] Advanced Algorithms (6)             3-5 qubits
  adv_01  3-Qubit QFT                     3q   Full quantum Fourier transform
  adv_02  3-Qubit Grover                  3q   Oracle(|111>) + Diffusion
  adv_03  VQE Ansatz                      4q   Ry layers + CNOT entangling
  adv_04  QAOA MaxCut                     4q   Cost(ZZ) + Mixer(Rx)
  adv_05  Quantum Walk                    4q   Coin + Position shift
  adv_06  Bernstein-Vazirani              5q   Hidden string s=1011

[A] Gate Type Coverage (15)               1-3 qubits
  A01  Y gate                             1q
  A02  S gate                             1q
  A03  T gate                             1q
  A04  Rx(pi/4)                           1q
  A05  Ry(pi/3)                           1q
  A06  Rz(pi/6)                           1q
  A07  sqrt(X) / V gate                   1q
  A08  Controlled-Z                       2q
  A09  Controlled-Ry                      2q   Decomposed: Ry-CNOT-Ry-CNOT
  A10  Controlled-Rx                      2q   Decomposed: Rx-CNOT-Rx-CNOT
  A11  CCZ                                3q   H-CCX-H
  A12  iSWAP                              2q   S-S-H-CNOT-CNOT-H
  A13  Double-Controlled Rz               3q   CCRz decomposed
  A14  Multi-Rotation                     2q   Rx-Ry-Rz-CNOT chain
  A15  Global Phase                       2q   S-T-CNOT-Tdg-Sdg

[B] Qubit Scaling (12)                    4-10 qubits
  B01  GHZ-4                              4q
  B02  GHZ-5                              5q
  B03  GHZ-6                              6q
  B04  GHZ-8                              8q
  B05  GHZ-10                             10q  Largest circuit
  B06  QFT-4                              4q
  B07  QFT-5                              5q
  B08  Linear Entanglement                6q   CNOT chain
  B09  Ring Entanglement                  6q   CNOT chain + wrap-around
  B10  Ladder                             4q   CNOT ring topology
  B11  Full Entanglement                  4q   All-pairs CNOT
  B12  Star Entanglement                  5q   q0 controls all others

[C] Classical Quantum Algorithms (15)     2-4 qubits
  C01  Deutsch-Jozsa (2-bit)              3q
  C02  Deutsch-Jozsa (3-bit)              4q
  C03  Simon's Algorithm                  4q   Hidden subgroup
  C04  Grover (4-qubit)                   4q   With ancilla
  C05  Shor Period Finding                4q   Simplified mod-15
  C06  QPE (3-qubit)                      3q   Phase = pi/4
  C07  QPE (4-qubit)                      4q
  C08  HHL Algorithm                      3q   Simplified linear solver
  C09  SWAP Test                          3q   State comparison
  C10  W State (3-qubit)                  3q   |001>+|010>+|100>
  C11  W State (4-qubit)                  4q
  C12  Amplitude Encoding (2q)            2q   Uniform superposition
  C13  Amplitude Encoding (3q)            3q
  C14  Quantum Adder                      4q   Ripple-carry
  C15  QFT-based Addition                 4q   Add in Fourier space

[D] Variational / Parameterized (10)      2-4 qubits
  D01  Hardware-Efficient (2q)            2q   Ry-Rz + CNOT layers
  D02  Hardware-Efficient (4q)            4q   2 layers
  D03  UCCSD (H2 molecule)               2q   Unitary coupled cluster
  D04  QAOA 2-Layer                       4q   MaxCut ring, 2 iterations
  D05  VQE Ry-Linear                      4q   Ry + linear CNOT
  D06  VQE Ry-Circular                    4q   Ry + circular CNOT
  D07  Parameter Shift                    2q   Rx-CNOT-Ry
  D08  Data Reuploading                   2q   Rx-CNOT-Rx-CNOT
  D09  Alternating Layers                 4q   3x (Ry + CNOT)
  D10  Strongly Entangling                3q   Rx-Ry-Rz + long-range CNOT

[E] Error Correction (8)                  3-9 qubits
  E01  Bit-Flip Code                      3q   |psi> -> |psi psi psi>
  E02  Phase-Flip Code                    3q   Bit-flip + Hadamard
  E03  Shor 9-Qubit Code                  9q   Concatenated bit+phase
  E04  Steane [[7,1,3]]                   7q   CSS code
  E05  Surface Code Patch                 9q   4 data + 4 syndrome + 1
  E06  Repetition Code (5q)               5q
  E07  Cat State (5q)                     5q   |00000>+|11111>
  E08  Logical CNOT                       6q   Transversal between 2 codes

[F] Quantum Machine Learning (10)         2-8 qubits
  F01  Angle Encoding                     4q   Rx(x_i) per qubit
  F02  Amplitude Encoding                 2q   Ry-CNOT-Ry tree
  F03  IQP Encoding                       4q   H-ZZ-H
  F04  QNN Layer                          4q   Rx-Rz + CNOT + Rz
  F05  QCNN                               8q   Conv + Pool layers
  F06  Quantum Kernel                     2q   Feature map + inner product
  F07  Classifier                         2q   Encode + trainable + CNOT
  F08  QGAN Generator                     3q   H + Ry + CNOT layers
  F09  Barren Plateau                     4q   Deep random-like circuit
  F10  Expressibility Test                3q   Rx-Rz + long-range CNOT

[H] Visual Variants (10)                  2-4 qubits
  H01  Bell + Barrier                     2q   Same logic, barrier line
  H02  Bell Compressed                    2q   Tight layout
  H03  Bell Wide                          2q   Identity padding
  H04  GHZ Reversed Labels                3q   q2 as source, not q0
  H05  Toffoli Decomposed                 3q   15 gates (H,T,Tdg,CNOT)
  H06  QFT3 No Swap                       3q   Without final bit reversal
  H07  Grover2 Combined                   2q   Oracle+diffusion merged
  H08  CNOT Reversed                      2q   q1->q0 instead of q0->q1
  H09  Parametric Symbolic                2q   Rx(0.7), Ry(1.2)
  H10  Multi-Gate Parallel                4q   Simultaneous H and CNOT


BTC / BLOCKCHAIN QUANTUM CIRCUITS (31)
=======================================

[blockchain] Original Blockchain (11)     2-8 qubits
  blockchain_qrng              4q   Consensus randomness (H gates)
  blockchain_bv_crypto         3q   BV oracle for key extraction
  blockchain_grover_mining     2q   Grover attack on PoW mining
  blockchain_bb84              4q   BB84 QKD for node communication
  blockchain_lattice_pqc       5q   Lattice-based PQC analysis
  blockchain_qss               4q   GHZ-based secret sharing
  blockchain_coin_flip         3q   Fair commit-reveal protocol
  blockchain_oblivious_transfer 5q  Private data exchange
  blockchain_vrf               6q   Verifiable random function
  blockchain_qds               7q   Quantum digital signature
  blockchain_consensus         8q   Validator agreement protocol

[G] Blockchain Extended (8)               3-6 qubits
  G01  E91 QKD Protocol         4q   Bell inequality key distribution
  G02  Quantum Money            3q   Wiesner unclonable banknotes
  G03  Blind Quantum Computing  4q   Client-server delegated QC
  G04  Quantum Voting           5q   GHZ-based anonymous voting
  G05  Quantum Auction          4q   Sealed-bid with amplitude encoding
  G06  Post-Quantum Hash        6q   Lattice-inspired hash circuit
  G07  Quantum Commitment       3q   Entanglement-based commit scheme
  G08  Entanglement Witness     4q   Verify entanglement resource

[I] BTC/Blockchain Quantum Security (12)  4-7 qubits

  ATTACK SURFACE (what quantum computers threaten)
  ------------------------------------------------
  I01  Shor vs ECDSA            6q   Break Bitcoin signatures (secp256k1)
  I02  Grover vs SHA-256        4q   Break Bitcoin hash (preimage search)
  I03  Grover vs AES            5q   Break symmetric encryption (128->64 bit)
  I10  PoW Quantum Speedup      4q   Quadratic speedup on nonce mining

  POST-QUANTUM DEFENSE (NIST PQC standards)
  ------------------------------------------
  I04  Lamport Signature        4q   One-time hash-based signature
  I08  Kyber / CRYSTALS         6q   Lattice key encapsulation (NIST std)
  I09  Dilithium                5q   Lattice digital signature (NIST std)
  I12  SPHINCS+                 7q   Hash-based signature (NIST std)

  QUANTUM-ENHANCED INFRASTRUCTURE
  --------------------------------
  I05  Quantum Random Beacon    6q   Multi-party randomness for consensus
  I06  QKD Network              6q   3-node key distribution (entanglement swap)
  I07  Quantum Timestamp        4q   Unforgeable time proof on-chain
  I11  Quantum Merkle Tree      5q   Quantum leaf hashing + verification


SUMMARY
=======
  General circuits:     101
  Blockchain circuits:   31  (23.5%)
  -------------------------
  Total:                132

  Tested:                32  (21 full + 11 partial)
  Pending:              100
```
