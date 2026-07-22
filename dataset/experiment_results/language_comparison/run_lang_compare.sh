#!/bin/bash
# Language comparison (CN vs EN prompt): core 21 circuits x 3 models x BV x n=5.
# Both languages run FRESH and INTERLEAVED per circuit, so CN and EN for the same
# image are seconds apart -> isolates prompt-language effect from model drift.
# Skip-existing -> safe to restart. sleep 2 between calls. timeout 300 per call.
export PATH="$HOME/.local/bin:$PATH"

CIRCUITS_DIR="$HOME/qcv-experiments/circuits"
OUT="$HOME/qcv-experiments/results_lang"
mkdir -p "$OUT"

# CN and EN are word-for-word equivalent; only the language differs.
CN_BV='请根据这张量子电路图生成 Amazon Braket SDK Python 代码。要求: 使用 from braket.circuits import Circuit; 只输出完整可执行的 Python 代码; 不要解释, 不要 markdown 格式。图片路径:'
EN_BV='Generate Amazon Braket SDK Python code from this quantum circuit diagram. Requirements: use from braket.circuits import Circuit; output only complete, executable Python code; no explanation, no markdown formatting. Image path:'

MODELS=("claude-opus-4.6" "claude-sonnet-4.6" "claude-haiku-4.5")
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
      for lang in cn en; do
        outfile="$OUT/${lang}_${model}_bv_${name}_run${run}_raw.txt"
        [ -f "$outfile" ] && continue
        if [ "$lang" = "cn" ]; then prompt="$CN_BV $img"; else prompt="$EN_BV $img"; fi
        total=$((total+1))
        echo "[$total] run$run $lang $model $name $(date '+%H:%M:%S')"
        timeout 300 kiro-cli chat --no-interactive --model "$model" -a "$prompt" > "$outfile" 2>&1 || true
        sleep 2
      done
    done
  done
done
echo "ALL DONE $(date '+%Y-%m-%d %H:%M:%S')"
