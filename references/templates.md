# Templates

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

## 备注

- [可选]
```
