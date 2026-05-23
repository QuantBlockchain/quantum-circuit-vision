# Datasheet for QCV-Dataset

Following the framework of [Gebru et al. (2021), "Datasheets for Datasets"](https://arxiv.org/abs/1803.09010).

## Motivation

**Purpose:** QCV-Dataset was created to enable systematic evaluation of multimodal AI systems on quantum circuit visual understanding and code generation—a task with no prior benchmark.

**Creators:** Dongping Liu (Tenorshare), Aoyu Zhang (AWS), Luyao Zhang (Duke Kunshan University).

**Funding:** No external funding. Computational costs covered by the authors.

## Composition

**Instances:** 132 quantum circuits, each with 5+ data modalities.

**Modalities per circuit:**
| Modality | Format | Count | Description |
|---|---|---|---|
| Circuit diagrams | PNG | 132 | Qiskit matplotlib, 150 DPI |
| Braket code | .py | 132 | Amazon Braket SDK ground truth |
| Qiskit code | .py | 132 | Qiskit implementation |
| Simulation results | JSON | 132 | State vectors from LocalSimulator |
| Annotations | JSON | 132 | Bilingual (EN/CN), structured metadata |
| Target descriptions | JSON | 132 | Natural language synthesis targets |
| Equivalence pairs | JSON | 12 | Circuit optimization pairs |
| Failure cases | JSON | 268 | Annotated model errors |
| Experiment results | CSV + TXT | 1,422 | 792 (n=1) + 630 (n=5) raw outputs |
| Cost analysis | CSV | 1 | Per-invocation credits and latency |

**Categories:** 13 categories spanning basic gates (1q) to blockchain security (7q). See Table 1 in the paper.

**Qubit range:** 1–10 qubits. Depth range: 1–27 gates.

**Sensitive data:** None. All circuits are synthetic (programmatically generated). No personal data.

## Collection Process

**Circuit generation:** All diagrams generated programmatically using `Qiskit 1.x` with `QuantumCircuit.draw("mpl", style="iqp")` at 150 DPI. No hand-drawn or scanned circuits.

**Ground truth:** Braket SDK code written by the authors and verified on LocalSimulator. Qiskit code auto-generated or manually written.

**Experiment data:** Collected via `kiro-cli` non-interactive mode (April 2026). Models: Claude Opus 4.6, Sonnet 4.6, Haiku 4.5. Each circuit evaluated under BV and TV prompting modes.

**Cost data:** Extracted from model output logs (`▸ Credits: X.XX • Time: Xs`).

## Preprocessing

- Circuit diagrams: tight bounding box, no padding normalization
- Raw model outputs: contain ANSI escape codes (documented cleaning procedure in Appendix C of paper)
- Annotations: programmatically extracted gate counts, depths; descriptions manually written

## Uses

**Intended uses:**
- Benchmarking multimodal AI on scientific diagram understanding
- Evaluating cost-accuracy tradeoffs in AI agent deployment
- Training/fine-tuning models for quantum code generation
- Studying failure modes in visual scientific reasoning

**Not intended for:**
- Running on real quantum hardware (circuits are for simulation only)
- Production quantum software development without human verification
- Claims about quantum advantage or quantum supremacy

## Distribution

**License:** MIT
**Repository:** https://github.com/QuantBlockchain/quantum-circuit-vision
**Format:** Files on GitHub (PNG, .py, JSON, CSV, TXT)
**Access:** Public, no registration required

## Maintenance

**Maintainer:** Dongping Liu (dpliu@tenorshare.com)
**Updates:** Dataset will be expanded with additional models and circuits. Version history tracked via git.
**Deprecation:** No planned deprecation.
