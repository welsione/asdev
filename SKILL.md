---
name: asdev
description: Handles multi-module software goals through mandatory multi-agent investigation, design, task decomposition, independent review, and acceptance validation with iterative rework. Use when the user invokes /asdev, /goal, goal mode, multi-agent, acceptance-agent, task-decomposition, call-site, call-chain investigation, or any multi-module change requiring reliable end-to-end delivery.
---

# asdev

Turn a multi-module goal into a disciplined delivery loop: investigate → design → decompose → implement → verify. Each phase requires independent agent acceptance before advancing.

## Iron Rules

1. **Mandatory Recording**: Every agent output must be written to `.record/`. No save, no advance to the next phase.
2. **Mandatory Acceptance**: Every phase output must be reviewed by an independent acceptance agent returning PASS. Main agent self-review does not count.
3. **Mandatory Rework on Rejection**: On FAIL, revise per acceptance feedback and resubmit. Loop until PASS. No skip, no downgrade, no bypass.

The only exception: when the user explicitly terminates a task, record the reason and set status to `Blocked`.

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
├── STATUS.md              ← aggregated state (auto-synced by scripts/sync-status.py)
├── {goal-slug}/           ← one per goal (e.g. payment-timeout)
│   ├── .goal/
│   ├── .prod/
│   ├── .task/
│   └── .review/
└── .knowledge/            ← shared across all goals
```

Slug: 2-3 core keywords, lowercase, ≤24 chars. Generated at Phase 1. See [references/cross-phase.md](references/cross-phase.md) for slug rules and naming conventions.

**STATUS.md auto-sync**: Run `python3 scripts/sync-status.py` to regenerate STATUS.md from record files. PostToolUse hook in `.claude/settings.local.json` calls this script automatically after every Write/Edit. STATUS.md is the aggregated view — record files are source of truth. See [references/cross-phase.md](references/cross-phase.md) for the three-layer sync guarantee (script + hook + constraints).

**Python 3 dependency**: The sync script requires Python 3 (standard library only, no external packages). If Python 3 is unavailable, install it first or fall back to manually updating STATUS.md at the 5 event points.

## Cross-Goal Memory

Before Phase 1: read `.record/STATUS.md` → scan prior goal directories → scan `.record/.knowledge/` → build historical context (5-10 bullets) → pass as `{HISTORICAL_CONTEXT}` and `{PROJECT_KNOWLEDGE}` to the Investigator Agent. Skip if `.record/` is empty. See [references/cross-phase.md](references/cross-phase.md) for full protocol.

## Platform Compatibility

- **Claude Code**: Agent tool (subagent). Required; stop if unavailable.
- **Codex**: Available multi-agent/subagent tools. Stop if unavailable.
- **Optional**: `codegraph`, `superpowers`. Detect and use only when available.

See [references/phase0-bootstrap.md](references/phase0-bootstrap.md) for detection, model selection, and worktree guidance.

## Verification Defaults

Prefer objective verification: run tests, search for forbidden imports, use call-chain checks. Record exact commands and results. If tests cannot be run, explain why and record residual risk — this does NOT bypass iron rules.

## Operating Notes

- Respect the user's dirty worktree. Do not revert unrelated changes.
- Use existing project patterns over new abstractions.
- Do not install dependencies or modify global agent config without explicit approval.
- All generated records in the user's preferred language (default: matching the project/prompt language).
