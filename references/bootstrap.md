# First-Run Bootstrap And Capability Detection

Use this reference during Phase 0, before requirement exploration.

The goal of bootstrap is to make the project ready for repeatable goal-mode work without forcing heavyweight dependencies.

## Table of Contents

- [Detect Project Context](#detect-project-context)
- [Create Local Record Structure](#create-local-record-structure)
- [Create Lightweight Templates](#create-lightweight-templates)
- [Capability Detection](#capability-detection)
- [Dependency Policy](#dependency-policy)
- [Suggested Goal Config](#suggested-goal-config)

## Detect Project Context

Look for project-local guidance first:

- `CLAUDE.md`
- `AGENTS.md`
- `README.md`
- `docs/architecture/`
- `docs/`
- Existing `.record/`
- Existing task/review/design files
- Build files such as `pom.xml`, `package.json`, `build.gradle`, `Cargo.toml`, `pyproject.toml`

Read only the files needed to understand rules, architecture, and verification commands.

## Create Local Record Structure

If the workflow directories are missing and the workspace is writable, create:

```text
.record/
├── STATUS.md
└── .knowledge/                  ← shared across goals
```

The goal-scoped subdirectory (`.record/{slug}/.goal/`, `.record/{slug}/.prod/`, `.record/{slug}/.task/`, `.record/{slug}/.review/`) is created at Phase 1 after the goal slug is generated. See `references/recording-protocol.md` for the Goal Slug Generation rules.

**Iron rule 1 enforcement**: The `.record/` root and `.knowledge/` MUST exist before Phase 1 begins. The goal-scoped subdirectories MUST exist before Phase 1 investigation begins. If they cannot be created, stop and report.

If the project already has a different record convention, follow the existing convention instead of forcing this one.

## Create STATUS.md Aggregated View

When creating the record structure, also create `.record/STATUS.md` using the STATUS Template from `references/templates.md`. STATUS.md is the aggregated state view — Cross-Goal Memory reads this file first to recover context efficiently (O(1) instead of scanning all `.record/` directories).

**Initial content** (when no prior goals exist):

```markdown
# STATUS

> 最后更新：[当前时间]
> 当前模式：交互
> 当前阶段：Phase 0

## 活跃目标

（暂无活跃目标）

## 任务进度

（暂无任务）

## 历史目标摘要

（暂无历史目标）

## 知识要点

（暂无知识条目）

## 可用连接器

（待 Phase 0 连接器发现阶段填充）

## 最近变更摘要

（暂无变更）
```

## Create Lightweight Templates

If missing, create project-local templates from `references/templates.md`:

- `.record/.knowledge/KNOW_TEMPLATE.md` (knowledge item template, see `references/templates.md`)

Goal-scoped templates are created inside the goal subdirectory when a new goal starts at Phase 1:

- `.record/{slug}/.prod/PROD_TEMPLATE.md`
- `.record/{slug}/.task/TASK_TEMPLATE.md`
- `.record/{slug}/.goal/GOAL_CONFIG_TEMPLATE.md`

Do not overwrite existing templates without user approval.

## Capability Detection

Detect tools and capabilities before relying on them:

- `rg`: primary text search tool.
- `git`: useful for status and diffs.
- Build/test command: infer from project files.
- `codegraph`: optional for call-chain and dependency graph exploration.
- Subagents or Agent tool (子代理): required for independent role execution.
- Related skills such as `superpowers`: optional reasoning/review enhancement.

Use `references/multi-agent-contract.md` for the exact acceptance criteria for independent agent capability.

Record the useful findings in the product/design notes when they affect execution.

## Dependency Policy

Do not install external dependencies automatically.

If a useful optional tool is missing:

1. Continue with available tools when practical.
2. Mention the missing tool and the benefit it would provide.
3. Ask the user before installing or requiring it.

Examples:

- If `codegraph` is missing, use `rg`, static reading, compiler/test output, and local architecture docs.
- If `superpowers` is unavailable, use this skill's built-in planning and review flow.

If independent multi-agent capability is missing, stop. asdev requires real independent agents and must not continue as a single-agent self-review workflow.

## Suggested Goal Config

When useful, create a config like this:

```yaml
recordRoot: .record
goalSlug: {generated at Phase 1}
prodDir: .record/{slug}/.prod
taskDir: .record/{slug}/.task
reviewDir: .record/{slug}/.review
knowledgeDir: .record/.knowledge
language: zh-CN
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

Keep the config descriptive. Do not make it a fragile source of truth unless the user asks for automation around it.
