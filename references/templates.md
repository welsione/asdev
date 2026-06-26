# Templates

## Contents

- [STATUS Template](#status-template)
- [Knowledge Item Template](#knowledge-item-template)
- [Product/Design Template](#productdesign-template)
- [Task Template](#task-template)
- [Goal Config Template](#goal-config-template)
- [Review Record Template](#review-record-template)
- [Comprehension Report Template](#comprehension-report-template)
- [Goal Check Record Template](#goal-check-record-template)

Use these templates when project-local templates are missing.

Prefer the project's existing template if one already exists.

## STATUS Template

Recommended path:

`.record/STATUS.md`

STATUS.md 是 `.record/` 的聚合状态视图，由主 Agent 在 5 个事件点维护：Phase 0 完成后、阶段转换时、任务状态变更时、Goal Check 后、目标完成时。Cross-Goal Memory 优先读取此文件。

```markdown
# STATUS

> 最后更新：YYYY-MM-DD HH:MM
> 当前模式：交互 | 循环
> 当前阶段：Phase 0 | Phase 1 | Phase 2 | Phase 3 | Completion | Goal Check

## 活跃目标

| 目标 | Slug | 停止条件 | 迭代轮次 | 当前阶段 | 状态 |
|------|------|----------|----------|----------|------|
| [目标摘要] | loop-eng | [停止条件或 N/A] | R1 | Phase 3 | 进行中 |

## 任务进度

| 任务 | 状态 | 验收结果 | 验收报告 |
|------|------|----------|----------|
| T01 | 完成 | PASS | .record/loop-eng/.review/TASK_T01_ACCEPTANCE_*.md |
| T02 | 进行中 | — | — |
| T03 | 阻塞 | — | [阻塞原因] |

## 历史目标摘要

> 最多保留最近 10 条。完成时从活跃目标移入此区域，更早的通过日期索引指向具体文件。

| 目标 | Slug | 完成日期 | 最终结果 | 关键产出 |
|------|------|----------|----------|----------|
| [目标摘要] | loop-eng | YYYY-MM-DD | PASS | .record/loop-eng/.prod/PROD_*.md |

## 知识要点

> 从 .record/.knowledge/ 提取的最近 5 条可复用知识条目摘要（路径 + 主题）。由 T04 维护。

- [路径] | [主题] | [置信度]

## 可用连接器

> Phase 0 连接器发现阶段记录的可用 MCP 工具，按功能分类（PR 管理 / Issue 管理 / CI/CD / 通知等）。由 T09 维护。

- [连接器名称]：[功能] — [能力描述]

## 最近变更摘要

> 循环模式下的认知投降替代机制：每完成一个任务后追加变更摘要，供用户随时查看。交互模式下此区域可选。

- [YYYY-MM-DD] T01: [变更摘要] → [验收结果]
- [YYYY-MM-DD] T02: [变更摘要] → [验收结果]
```

**STATUS.md 与铁律1的边界**：STATUS.md 不是 Agent 产出，绑定上述 5 个事件点而非铁律1的每次文件写入。STATUS.md 与记录文件不一致时，以记录文件为准，STATUS.md 应在下一事件点修正。

## Knowledge Item Template

Recommended path:

`.record/.knowledge/KNOW_YYYYMMDD_HHMM_[short_topic].md`

```markdown
---
name: KNOW_YYYYMMDD_HHMM_[short_topic]
source_goal: [goal summary or .record/{slug}/.goal/ path]
source_task: [T01/T02/... or N/A]
date: YYYY-MM-DD
confidence: confirmed | inferred | assumed
scope: [description of where this knowledge applies — files, modules, patterns]
status: active | outdated
outdated_reason: [reason if outdated, else omit]
outdated_date: [date if outdated, else omit]
---

## Content

[One paragraph: what to do, what not to do, and why this is non-obvious]

## Evidence

- [code fact or acceptance report path that supports this knowledge]

## Counter-examples (if any)

- [scenarios where this knowledge does NOT apply]
```

**Confidence levels**:

- **confirmed**: backed by code facts AND an acceptance report.
- **inferred**: derived from multiple execution experiences, not yet independently verified.
- **assumed**: based on limited experience, needs future verification.

Confidence can be upgraded when new evidence references the item.

**Outdated marking**: When a new goal modifies files/symbols in the item's `scope`, set `status: outdated` and add `outdated_reason` and `outdated_date`. Outdated items are still passed to the Investigator Agent with an "⚠️ 已过时" warning.

## Product/Design Template

Recommended path:

`.record/{slug}/.prod/PROD_TEMPLATE.md`

Where `{slug}` is the current goal's slug.

```markdown
# 需求探索：[目标名称]

> 来源：[用户目标或会话摘要]
> 创建日期：[YYYY-MM-DD]
> 状态：草稿 | 已验收

## 1. 背景与目标

- 背景：
- 目标：
- 非目标：

## 2. 项目规范与上下文

- 读取的规范文件：
- 相关模块：
- 约束：

## 3. 当前代码事实

- 入口：
- 直接调用点：
- 间接调用点：
- 当前行为：
- 已有相似实现：
- 测试覆盖：

## 4. 疑问与对齐结论

| 问题 | 用户结论 | 影响 |
| --- | --- | --- |
|  |  |  |

## 5. 影响范围

- 后端：
- 前端：
- 数据库：
- 接口：
- 任务/定时/事件：
- 测试：

## 6. 方案设计

- 总体方案：
- 核心流程：
- 错误/异常/状态传播：
- 兼容性：

## 7. 数据模型与接口变更

- 数据模型：
- API：
- 配置：
- 迁移：

## 8. 关键设计决策

| 决策 | 原因 | 替代方案 |
| --- | --- | --- |
|  |  |  |

## 9. 风险与验证策略

- 风险：
- 验证命令：
- 验收证据：

## 10. 设计验收记录

- 验收 Agent：
- 结论：
- 修改记录：
- **铁律提醒**：若验收结果为 FAIL，必须按验收意见修改后重新提交验收，循环直到 PASS。

## 10. 停止条件（仅目标模式）

> 如果激活了 /goal 或目标模式，在此定义可验证的停止条件。停止条件在迭代之间不变。如果用户想改变停止条件，需要开启新的目标。

- 停止条件：
- 验证方式：
```

## Task Template

Recommended path:

`.record/{slug}/.task/TASK_TEMPLATE.md`

```markdown
# 任务档案 [TASK_ID]

> 来源：[PROD 文档或目标]
> 创建日期：[YYYY-MM-DD]
> 状态：未完成

## 优先级说明

[说明排序依据，例如风险、依赖、影响范围、验证成本]

---

## T01 - [任务标题]

- **任务描述**：[做什么]
- **任务原因**：[为什么做，关联设计目标或前置依赖]
- **任务目标**：
  - [可量化目标 1]
  - [可量化目标 2]
- **任务验收规范**：
  - [ ] [客观验收项 1]
  - [ ] [客观验收项 2]
  - [ ] [测试/构建命令通过]
- **任务状态**：未完成
- **任务验收报告**：
  - 待填写
```

## Goal Config Template

Recommended path:

`.record/{slug}/.goal/GOAL_CONFIG_TEMPLATE.md`

````markdown
# Goal Workflow Config

```yaml
recordRoot: .record
prodDir: .record/{slug}/.prod
taskDir: .record/{slug}/.task
reviewDir: .record/{slug}/.review
language: zh-CN
rulesFiles:
  - CLAUDE.md
testCommands: {}
recordNaming:
  investigation: INVESTIGATION_YYYYMMDD_HHMM.md
  product: PROD_YYYYMMDD_HHMM.md
  task: TASK_YYYYMMDD_HHMM.md
codeSearch:
  primary: rg
  optional:
    - codegraph
pauseAfterTaskPlanning: true
multiAgent:
  required: true
  contract: references/multi-agent-contract.md
prompts:
  index: references/agent-prompts.md
  assembly: references/prompt-assembly.md
optionalSkills:
  - superpowers
```
````

## Review Record Template

Recommended path:

`.record/{slug}/.review/REVIEW_TEMPLATE.md`

```markdown
# 审阅记录：[对象名称]

> 审阅对象：
> 审阅日期：
> 审阅角色：

## 结论

Status: PASS | FAIL

## 发现

- [severity] [问题描述与证据]

## 必须修改

- [修改项]

## 返工记录

> 铁律3：验收不过必须返工。每次 FAIL 后的修改和重新提交必须记录在此。

| 轮次 | 审阅结果 | 修改内容 | 重新提交日期 |
| --- | --- | --- | --- |
| 1 | FAIL | [按 Required Changes 修改的内容] | [日期] |
| 2 | PASS | — | [日期] |

## 备注

- [可选]
```

## Comprehension Report Template

Produced at Completion or Goal Check PASS. Written to `.record/{slug}/.prod/`.

```markdown
# 理解腐烂防护报告：[目标名称]

> 生成日期：
> 关联设计文档：

## 变更文件摘要

| 文件路径 | 变更描述 |
| --- | --- |
| | |

## 新引入的概念、模式或抽象

- [概念/模式/抽象]：[简要说明]

## 验收报告标记的风险或副作用

- [风险/副作用]：[来源任务和验收报告路径]

## 用户需手动确认的项

- [ ] [确认项]
```

## Goal Check Record Template

Written to `.record/{slug}/.review/` after each Goal Check Agent run.

```markdown
# 目标检查记录：[停止条件摘要]

> 检查日期：
> 迭代轮次：

## 检查结果

Status: PASS | FAIL

## 停止条件评估

| 条件 | 证据 | 结果 |
| --- | --- | --- |

## 差距分析

- 未满足的条件及原因：

## 建议下一步

- [如果 FAIL，描述还需做什么]

## 返工记录

| 轮次 | 检查结果 | 差距 | 修改内容 | 重新提交日期 |
| --- | --- | --- | --- | --- |
| | | | | |
```
