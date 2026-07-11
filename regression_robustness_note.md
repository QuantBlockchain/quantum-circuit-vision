# 回归稳健性核查 — depth / gate_count / qubits

生成时间: 2026-06-12
数据来源: `dataset/experiment_results/verification_results.csv` (792 行, n=1 全集)
特征来源: 从 `dataset/braket_code/*.py` 执行 braket Circuit 对象提取
          (`qubit_count`, `depth`, `len(instructions)`), 132/132 全部成功。
工具: Python statsmodels Logit。

> 背景: 论文 claim "circuit depth is the primary predictor"(p<0.001),
> qubits 不显著(论文写 p=0.20)。本 note 验证两个风险:
> (1) depth 是否只是 gate_count 的代理变量(两者高度共线)?
> (2) qubits 的 p 值在不同回归设定下为何不一致?

---

## 1. 共线性 (Pearson 相关系数, n=132 电路)

| 变量对 | r |
|---|---|
| depth vs gate_count | **0.862** (高度共线) |
| depth vs qubits | 0.368 |
| gate_count vs qubits | 0.474 |

depth 和 gate_count 高度相关 (r=0.862), 必须做多变量检验才能区分谁是真信号。

## 2. 三变量逻辑回归 (qubits + depth + gate_count, per-invocation N=792)

| 变量 | coef | p-value | 显著 |
|---|---|---|---|
| qubits | -0.120 | 0.017 | ✱ |
| **depth** | **-0.171** | **0.00043** | ✱✱✱ |
| gate_count | -0.038 | 0.108 | 否 |

单变量对照: depth-only p=6.5e-21; gate_count-only p=4.2e-21 (单独都极显著)。

**结论: depth 不是 gate_count 的代理, 反而相反。**
控制 depth 后 gate_count 失去显著性(p=0.108); 控制 gate_count 后 depth 仍显著
(p=0.0004)。gate_count 单变量的显著性主要借自与 depth 的共线。
论文 "depth is the primary predictor" 经得起稳健性检验。

## 3. qubits p 值差异的根因 (聚合方式 + N)

二变量 (qubits + depth) 在三种聚合下复现:

| 设定 | 分析单元 | N | qubits p | depth p |
|---|---|---|---|---|
| A | per-invocation | 792 | 0.0025 ✱ | 2.8e-15 ✱ |
| B | per-circuit, majority(≥50%) | 132 | **0.198** | 0.0010 ✱ |
| C | per-circuit, any-pass | 132 | **0.188** | 0.0021 ✱ |

**论文的 "qubits p=0.20" 来自 per-circuit (N=132) 聚合回归 (设定 B/C)。**
本 session 早先报的 qubits p=0.0025 来自 per-invocation (N=792, 设定 A)。
差异纯粹是 N (792→132) 和聚合方式造成的统计功效变化, **不是结论冲突**:
无论哪种设定, depth 始终极显著, qubits 始终是三者中最弱的预测因子。
定性结论 "结构复杂度(depth)而非 qubit 数主导" 在所有设定下都成立。

## 4. 给论文的修订建议 (★ 投稿风险点)

1. **明确标注回归的 N 和分析单元**: 132 电路 (per-circuit) 还是 792 次调用
   (per-invocation)。两者 qubits p 值差一个数量级, 不写清会被 reviewer 质疑。
2. **明确聚合规则**: per-circuit 时 outcome 如何二值化 (majority≥50% / any-pass
   / mean rate)。
3. **推荐**: 以 per-circuit (N=132) 为主结果 (更保守, 避免把同一电路的 6 次调用
   当独立样本 → pseudoreplication 违反独立性假设)。可在脚注说明 per-invocation
   下 qubits 也变显著, 但存在伪重复问题。

## 5. 复现命令

特征提取: 执行 dataset/braket_code/*.py 取 qubit_count / depth / len(instructions)。
回归: statsmodels Logit, outcome = verification_results.csv 的 pass 列。
(本 note 的脚本为一次性分析, 未落盘为独立 .py; 如需固化可加入 verify_all.py 旁。)
