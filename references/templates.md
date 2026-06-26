# Templates

## Contents

- [Product/Design Template](#productdesign-template)
- [Task Template](#task-template)
- [Goal Config Template](#goal-config-template)
- [Review Record Template](#review-record-template)
- [Comprehension Report Template](#comprehension-report-template)
- [Goal Check Record Template](#goal-check-record-template)

Use these templates when project-local templates are missing.

Prefer the project's existing template if one already exists.

## Product/Design Template

Recommended path:

`.record/.prod/PROD_TEMPLATE.md`

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

`.record/.task/TASK_TEMPLATE.md`

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

`.record/.goal/GOAL_CONFIG_TEMPLATE.md`

````markdown
# Goal Workflow Config

```yaml
recordRoot: .record
prodDir: .record/.prod
taskDir: .record/.task
reviewDir: .record/.review
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

`.record/.review/REVIEW_TEMPLATE.md`

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

Produced at Completion or Goal Check PASS. Written to `.record/.prod/`.

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

Written to `.record/.review/` after each Goal Check Agent run.

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
