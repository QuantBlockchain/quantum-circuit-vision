#!/bin/bash
# Phase 1 补跑: Basic TV 模式 (5题 × 2模型 = 10 次调用)
# 用法: cd demo && bash run_basic_tv.sh

set -e
DEMO_DIR="$(cd "$(dirname "$0")" && pwd)"
CIRCUITS_DIR="$DEMO_DIR/circuits"
RESULTS_DIR="$DEMO_DIR/results"
mkdir -p "$RESULTS_DIR"

TV_PROMPT='请先分析这张量子电路图:
1. 有几条 qubit 线? 编号分别是什么?
2. 从左到右依次有哪些量子门?
3. 哪些门有控制位? 控制哪条 qubit 线, 目标是哪条?
然后根据分析生成 Amazon Braket SDK Python 代码。
要求:
- 使用 from braket.circuits import Circuit
- 输出完整可执行的 Python 代码'

MODELS="claude-opus-4.6 claude-haiku-4.5"

find "$CIRCUITS_DIR" -maxdepth 1 -name 'demo_*.png' -type f | sort | while read -r img; do
  name=$(basename "$img" .png)
  for model in $MODELS; do
    model_short=$(echo "$model" | sed 's/claude-//')
    outfile="$RESULTS_DIR/${model_short}_tv_${name}_raw.txt"
    if [ -f "$outfile" ]; then
      echo "跳过 (已存在): $(basename "$outfile")"
      continue
    fi
    echo ">>> $model | tv | $name"
    kiro-cli chat --no-interactive --model "$model" -a \
      "请看这张量子电路图: circuits/${name}.png

$TV_PROMPT" 2>&1 | tee "$outfile"
    echo "---"
    sleep 2
  done
done

echo ""
echo "========================================="
echo "Basic TV 补跑完成, 结果在: $RESULTS_DIR/"
echo "========================================="
