#!/bin/bash
# Sonnet 4.6: 全部 21 题 × BV/TV = 42 次调用
# 用法: cd demo && bash run_sonnet.sh

set -e
DEMO_DIR="$(cd "$(dirname "$0")" && pwd)"
CIRCUITS_DIR="$DEMO_DIR/circuits"
RESULTS_DIR="$DEMO_DIR/results"
mkdir -p "$RESULTS_DIR"

MODEL="claude-sonnet-4.6"
MODEL_SHORT="sonnet-4.6"

BV_PROMPT='请根据这张量子电路图生成 Amazon Braket SDK Python 代码。
要求:
- 使用 from braket.circuits import Circuit
- 只输出完整可执行的 Python 代码
- 不要解释, 不要 markdown 格式'

TV_PROMPT='请先分析这张量子电路图:
1. 有几条 qubit 线? 编号分别是什么?
2. 从左到右依次有哪些量子门?
3. 哪些门有控制位? 控制哪条 qubit 线, 目标是哪条?
然后根据分析生成 Amazon Braket SDK Python 代码。
要求:
- 使用 from braket.circuits import Circuit
- 输出完整可执行的 Python 代码'

for mode in bv tv; do
  if [ "$mode" = "bv" ]; then
    PROMPT="$BV_PROMPT"
  else
    PROMPT="$TV_PROMPT"
  fi

  # Find all circuit PNGs (demo_*, inter_*, adv_*) safely
  find "$CIRCUITS_DIR" -maxdepth 1 -name '*.png' -type f | sort | while read -r img; do
    name=$(basename "$img" .png)
    # Skip non-circuit files
    case "$name" in
      demo_*|inter_*|adv_*) ;;
      *) continue ;;
    esac
    outfile="$RESULTS_DIR/${MODEL_SHORT}_${mode}_${name}_raw.txt"
    if [ -f "$outfile" ]; then
      echo "跳过 (已存在): $(basename "$outfile")"
      continue
    fi
    echo ">>> $MODEL | $mode | $name"
    kiro-cli chat --no-interactive --model "$MODEL" -a \
      "请看这张量子电路图: circuits/${name}.png

$PROMPT" 2>&1 | tee "$outfile"
    echo "---"
    sleep 2
  done
done

echo ""
echo "========================================="
echo "Sonnet 4.6 全部测试完成, 结果在: $RESULTS_DIR/"
echo "========================================="
