#!/bin/bash
# Phase 3: 批量测试 Advanced 电路图
# 用法: bash run_advanced.sh
# 在 demo/ 目录下执行

set -e
DEMO_DIR="$(cd "$(dirname "$0")" && pwd)"
CIRCUITS_DIR="$DEMO_DIR/circuits"
RESULTS_DIR="$DEMO_DIR/results"
mkdir -p "$RESULTS_DIR"

# Step 1: 生成电路图 (如果还没生成)
if [ ! -f "$CIRCUITS_DIR/adv_01_qft3.png" ]; then
  echo ">>> 生成 Advanced 电路图..."
  python3 "$DEMO_DIR/generate_advanced.py"
fi

# BV prompt
BV_PROMPT='请根据这张量子电路图生成 Amazon Braket SDK Python 代码。
要求:
- 使用 from braket.circuits import Circuit
- 只输出完整可执行的 Python 代码
- 不要解释, 不要 markdown 格式'

# TV prompt
TV_PROMPT='请先分析这张量子电路图:
1. 有几条 qubit 线? 编号分别是什么?
2. 从左到右依次有哪些量子门?
3. 哪些门有控制位? 控制哪条 qubit 线, 目标是哪条?
然后根据分析生成 Amazon Braket SDK Python 代码。
要求:
- 使用 from braket.circuits import Circuit
- 输出完整可执行的 Python 代码'

MODELS="claude-opus-4.6 claude-haiku-4.5"
CIRCUITS=$(find "$CIRCUITS_DIR" -maxdepth 1 -name 'adv_*.png' -type f | sort)

if [ -z "$CIRCUITS" ]; then
  echo "错误: 没有找到 adv_*.png 电路图, 先运行 generate_advanced.py"
  exit 1
fi

echo "将测试以下电路图:"
for img in $CIRCUITS; do
  echo "  $(basename "$img")"
done
echo ""

for model in $MODELS; do
  model_short=$(echo "$model" | sed 's/claude-//')
  for mode in bv tv; do
    if [ "$mode" = "bv" ]; then
      PROMPT="$BV_PROMPT"
    else
      PROMPT="$TV_PROMPT"
    fi
    for img in $CIRCUITS; do
      name=$(basename "$img" .png)
      outfile="$RESULTS_DIR/${model_short}_${mode}_${name}_raw.txt"
      if [ -f "$outfile" ]; then
        echo "跳过 (已存在): $outfile"
        continue
      fi
      echo ">>> $model | $mode | $name"
      kiro-cli chat --no-interactive --model "$model" -a \
        "请看这张量子电路图: circuits/${name}.png

$PROMPT" 2>&1 | tee "$outfile"
      echo "---"
      sleep 2  # 避免 rate limit
    done
  done
done

echo ""
echo "========================================="
echo "批量测试完成, 结果在: $RESULTS_DIR/"
echo "========================================="
