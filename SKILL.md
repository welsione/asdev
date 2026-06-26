---
name: asdev
description: Handles complex software goals through mandatory multi-agent investigation, design, task decomposition, independent review, and acceptance validation with iterative rework. Trigger on /asdev, /goal, goal mode, 多Agent, 验收Agent, 任务拆解, 调用点, call-chain investigation, or any multi-module change requiring reliable end-to-end delivery.
---

# asdev

Turn a complex goal into a disciplined delivery loop: investigate → design → decompose → implement → verify. Each phase requires independent agent acceptance before advancing.

## Iron Rules

1. **强制记录**：每个 Agent 产出必须写入 `.record/`，不落盘不推进下一阶段。
2. **强制验收**：每个阶段产出必须经独立验收 Agent 审查并返回 PASS。主 Agent 自审不算验收。
3. **验收不过必须返工**：FAIL 后必须按验收意见修改再提交，循环直到 PASS。无跳过、无降级、无绕过。

唯一例外：用户显式终止任务时，记录终止原因，状态设为 `阻塞`。

## When To Use

- `/asdev`, `/goal`, goal mode, multi-agent workflow
- Requires call-chain investigation or boundary verification
- Spans multiple modules, services, or layers
- Needs architecture planning, task decomposition, and acceptance criteria
- Too risky for a one-shot edit

Do NOT use for tiny one-file edits, simple questions, or direct command requests.

## Phases

| Phase | Name | Reference |
|-------|------|-----------|
| 0 | Bootstrap & capability detection | [references/phase0-bootstrap.md](references/phase0-bootstrap.md) |
| 1 | Code investigation & requirement exploration | [references/phase1-investigation.md](references/phase1-investigation.md) |
| 2 | Task decomposition | [references/phase2-planning.md](references/phase2-planning.md) |
| 3 | Task-by-task implementation & acceptance | [references/phase3-implementation.md](references/phase3-implementation.md) |

After Phase 2, ask the user whether to proceed unless they already asked for full-auto execution.

For Goal Mode and Loop Mode, see [references/goal-mode.md](references/goal-mode.md).

Cross-phase shared definitions (templates, recording protocol, prompt assembly): [references/cross-phase.md](references/cross-phase.md)

## Agent Roles

| Role | Phase | Tier | Mission |
|------|-------|------|---------|
| Investigator | 1 | Standard | Discover code facts and call chains |
| Product/Design | 1 | Standard | Turn facts into design document |
| Design Acceptance | 1 | **High** | Review design completeness and feasibility |
| Development Manager | 2 | Standard | Decompose design into ordered tasks |
| Task Check | 2 | **High** | Review task plan quality |
| Implementation | 3 | Standard | Implement one approved task |
| Task Acceptance | 3 | **High** | Verify task against acceptance criteria |
| Verification | 3 | Standard | Build evidence for risk areas |
| Goal Check | Goal | **High** | Evaluate stop condition (goal mode only) |

**High-tier** roles (review/acceptance) should use the platform's highest-reasoning model (e.g. `model: "opus"` in Claude Code) to reduce shared cognitive bias with implementation roles.

## Record Structure

```text
.record/
├── STATUS.md              ← aggregated state (5 event points)
├── {goal-slug}/           ← one per goal (e.g. payment-timeout)
│   ├── .goal/
│   ├── .prod/
│   ├── .task/
│   └── .review/
└── .knowledge/            ← shared across all goals
```

Slug: 2-3 core keywords, lowercase, ≤24 chars. Generated at Phase 1. See [references/cross-phase.md](references/cross-phase.md) for slug rules and naming conventions.

STATUS.md update events: Phase 0 完成后、阶段转换时、任务状态变更时、Goal Check 后、目标完成时。Record files are source of truth.

## Cross-Goal Memory

Before Phase 1: read `.record/STATUS.md` → scan prior goal directories → scan `.record/.knowledge/` → build historical context (5-10 bullets) → pass as `{HISTORICAL_CONTEXT}` and `{PROJECT_KNOWLEDGE}` to the Investigator Agent. Skip if `.record/` is empty. See [references/cross-phase.md](references/cross-phase.md) for full protocol.

## Platform Compatibility

- **Claude Code**: Agent tool (子代理). Required; stop if unavailable.
- **Codex**: Available multi-agent/subagent tools. Stop if unavailable.
- **Optional**: `codegraph`, `superpowers`. Detect and use only when available.

See [references/phase0-bootstrap.md](references/phase0-bootstrap.md) for detection, model selection, and worktree guidance.

## Verification Defaults

Prefer objective verification: run tests, search for forbidden imports, use call-chain checks. Record exact commands and results. If tests cannot be run, explain why and record residual risk — this does NOT bypass iron rules.

## Operating Notes

- Respect the user's dirty worktree. Do not revert unrelated changes.
- Use existing project patterns over new abstractions.
- Do not install dependencies or modify global agent config without explicit approval.
- All generated records in the user's preferred language (default: Chinese for Chinese projects/prompts).
