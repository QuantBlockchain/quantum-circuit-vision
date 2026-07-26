#!/bin/bash
# Cross-vendor GPT experiment: core 21 x 3 GPT models x {bv,tv} x {cn,en} x n=5.
# CN/EN interleaved per (circuit,mode) so language pairs are seconds apart (drift-controlled).
# Skip-existing -> safe restart. sleep 2. timeout 300. Output -> results_gpt/.
export PATH="$HOME/.local/bin:$PATH"
CIRCUITS_DIR="$HOME/qcv-experiments/circuits"
OUT="$HOME/qcv-experiments/results_gpt"
mkdir -p "$OUT"

CN_BV='请根据这张量子电路图生成 Amazon Braket SDK Python 代码。要求: 使用 from braket.circuits import Circuit; 只输出完整可执行的 Python 代码; 不要解释, 不要 markdown 格式。图片路径:'
EN_BV='Generate Amazon Braket SDK Python code from this quantum circuit diagram. Requirements: use from braket.circuits import Circuit; output only complete, executable Python code; no explanation, no markdown formatting. Image path:'
CN_TV='请先分析这张量子电路图: 1. 有几条 qubit 线? 编号分别是什么? 2. 从左到右依次有哪些量子门? 3. 哪些门有控制位? 控制哪条 qubit 线, 目标是哪条? 然后根据你的分析, 生成 Amazon Braket SDK Python 代码。要求: 使用 from braket.circuits import Circuit; 输出完整可执行的 Python 代码; 代码放在分析之后。图片路径:'
EN_TV='First analyze this quantum circuit diagram: 1. How many qubit lines are there, and what are their indices? 2. From left to right, which quantum gates appear? 3. Which gates have control qubits; which line is the control and which is the target? Then, based on your analysis, generate Amazon Braket SDK Python code. Requirements: use from braket.circuits import Circuit; output complete, executable Python code; place the code after the analysis. Image path:'

MODELS=("gpt-5.6-sol" "gpt-5.6-terra" "gpt-5.6-luna")
CORE=(demo_01_hadamard demo_02_cnot demo_03_bell demo_04_ghz demo_05_toffoli \
      inter_01_swap_decomp inter_02_qft2 inter_03_teleport_prep inter_04_deutsch \
      inter_05_superdense inter_06_grover2 inter_07_param_rot inter_08_fredkin \
      inter_09_shift_reg inter_10_phase_est adv_01_qft3 adv_02_grover3 \
      adv_03_vqe_ansatz adv_04_qaoa adv_05_qwalk adv_06_bv)

total=0
for run in 1 2 3 4 5; do
  for model in "${MODELS[@]}"; do
    for name in "${CORE[@]}"; do
      img="$CIRCUITS_DIR/${name}.png"
      [ ! -f "$img" ] && { echo "MISSING $img"; continue; }
      for mode in bv tv; do
        for lang in cn en; do
          outfile="$OUT/${lang}_${model}_${mode}_${name}_run${run}_raw.txt"
          [ -f "$outfile" ] && continue
          case "${lang}_${mode}" in
            cn_bv) prompt="$CN_BV $img";; en_bv) prompt="$EN_BV $img";;
            cn_tv) prompt="$CN_TV $img";; en_tv) prompt="$EN_TV $img";;
          esac
          total=$((total+1))
          echo "[$total] run$run $lang $model $mode $name $(date '+%H:%M:%S')"
          timeout 300 kiro-cli chat --no-interactive --model "$model" -a "$prompt" > "$outfile" 2>&1 || true
          sleep 2
        done
      done
    done
  done
done
echo "ALL DONE $(date '+%Y-%m-%d %H:%M:%S')  total new calls: $total"
