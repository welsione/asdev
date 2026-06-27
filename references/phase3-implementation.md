# Phase 3 — Task-by-Task Implementation & Acceptance

## Contents

- [Workflow](#workflow)
- [Comprehension Debt Guard](#comprehension-debt-guard)
- [Knowledge Extraction](#knowledge-extraction)
- [Completion](#completion)
- [Agent Prompts](#agent-prompts)
- [Phase 3 Roles](#phase-3-roles)

Iron Rules: see [references/cross-phase.md](cross-phase.md) for the canonical definition.

Shared Header and prompt assembly: see [references/cross-phase.md](cross-phase.md).

Templates (Individual Task Record, Review Record, Comprehension Report): see [references/cross-phase.md](cross-phase.md).

## Workflow

For each task in order:

0. **Pre-Implementation Confirmation (Layer 3)**: Before implementing, present the implementation intent (task description, files involved, expected behavior change, files NOT involved) and ask the user to confirm scope. Allowed adjustments: implementation details only; acceptance criteria changes must re-trigger Task Check. Full-auto exception: may be skipped if user opted into full-auto at goal start.
0a. **Change Density Check (Layer 4)**: Before implementing, check whether the same file/module has been modified in the previous 2 tasks. If yes, present the Change Density Warning and pause for confirmation. This check applies in both interactive and full-auto modes.
0b. **Worktree/Branch Isolation**: If the task is a rework (previous FAIL on this task) or Goal Mode iteration, create an isolated branch (`asdev/TXX_YYYYMMDDHHMM`) or worktree before implementing. See phase0-bootstrap.md for the full isolation strategy.
1. Read the task and relevant project rules.
2. Investigate the exact files before editing.
3. Implement the smallest coherent change, using an Implementation Agent when the platform supports agent file edits in the active workspace.
4. Run focused verification.
5. Run broader verification when risk or acceptance criteria require it.
5a. If a Verification Agent was launched, save its output to `.record/{slug}/.review/VERIFICATION_TXX_*.md` (Iron rule 1).
▶ CHECKPOINT: `.record/{slug}/.review/VERIFICATION_TXX_*.md` exists
6. Save the implementation summary to `.record/{slug}/.task/TXX_*.md` before launching the Task Acceptance Agent (Iron rule 1).
▶ CHECKPOINT: `.record/{slug}/.task/TXX_*.md` exists
7. Submit to an independent Task Acceptance Agent.
8. The task is not complete until the Task Acceptance Agent returns PASS (Iron rule 2).
9. If the Task Acceptance Agent returns FAIL, fix according to Required Fixes and re-submit (Iron rule 3).
10. Save acceptance output to `.record/{slug}/.review/TASK_TXX_ACCEPTANCE_*.md` (Iron rule 1).
▶ CHECKPOINT: `.record/{slug}/.review/TASK_TXX_ACCEPTANCE_*.md` exists
11. If accepted, update task status and acceptance report.
12. If rejected, fix according to review findings and re-run acceptance. This loop continues until PASS.
12a. **Knowledge Extraction**: When the task PASSes (or FAIL → rework → PASS), check whether the implementation surfaced a non-obvious pattern, gotcha, or constraint worth preserving. If yes, write a `.record/.knowledge/KNOW_*.md` file. This is opportunistic — not every task produces one.
13. **STATUS.md update**: After each task status change, update `.record/STATUS.md` "任务进度" table. The update is automatic via `scripts/sync-status.py` triggered by PostToolUse hook; verify by reading `.record/STATUS.md`. If the script/hook is unavailable, manually update the "任务进度" table at each task status change. See [references/cross-phase.md](cross-phase.md) for the three-layer sync guarantee.
14. **Change Summary (Layer 1)**: After acceptance PASS, present a change summary to the user (files changed, behavior changed, manual verification hints). Write the summary into the task's acceptance report AND show to the user.
15. **Understanding Verification (Layer 2)**: Every 3 completed tasks, present an Understanding Verification challenge with concrete inferences for the user to judge (NOT a passive "do you understand?" question). User says "no" to an inference → explain and re-verify before proceeding.

Do not mark a task complete until the Task Acceptance Agent returns PASS. The only exception is if the user explicitly terminates the task — record the termination and reason, set status to `阻塞`.

## Comprehension Debt Guard

Four progressive layers guard against comprehension debt:

### Layer 1 — Per-Task Change Summary

When a task passes acceptance, present to the user:
- **What files changed** (file paths + brief description).
- **What behavior changed** (plain language, not code).
- **What the user should verify manually**.

Write into the task's acceptance report AND show to the user directly.

### Layer 2 — Understanding Verification (every 3 tasks)

After every 3 tasks completed, present concrete inferences for the user to judge:

```markdown
### Understanding Verification

Verify these inferences (answer "yes" or point out the error):

1. [Change T01] modified [file/module], with effect [behavior change].
   → Does this mean [concrete inference A]? (yes/no)

2. [Change T02] added [file/module] for [purpose].
   → If [scenario X] happens, expected behavior is [concrete inference B]? (yes/no)
```

User says "no" → explain and re-verify before proceeding.

### Layer 3 — Pre-Implementation Confirmation (before each task)

Before each task implementation:

```markdown
### Implementation Intent Confirmation: T03

About to implement: [task description]
Files involved: [file list]
Expected behavior change: [behavior change description]
Files NOT involved: [explicitly excluded files]

Confirm implementation scope? (yes / no / adjust)
```

**Adjustment boundary**: Allowed: adjusting implementation details. NOT allowed: adjusting acceptance criteria (must re-trigger Task Check).

Full-auto exception: Layer 3 may be skipped if user opted into full-auto at goal start.

### Layer 4 — Change Density Warning

When the same file/module is modified across 3 consecutive tasks, pause and warn:

```markdown
### Change Density Warning

[File/module] has been modified in T01, T02, and T03. Please confirm:
1. Do you still understand the current state of this file/module?
2. Should I show the file's current full logic?
```

Applies in both interactive and full-auto modes (Layer 3 may be skipped, Layer 4 cannot).

### Final Comprehension Report

At Completion, produce a comprehension report:
- All changed files with one-line descriptions.
- New concepts, patterns, or abstractions introduced.
- Risks or side effects flagged in acceptance reports.

Write into `.record/{slug}/.prod/` using the Comprehension Report Template from cross-phase.md (Iron rule 1).

▶ CHECKPOINT: `.record/{slug}/.prod/COMPREHENSION_*.md` exists

## Knowledge Extraction

The main agent distills execution experience into `.record/.knowledge/` at three trigger points:

1. **Task PASS**: when an implementation surfaced a non-obvious pattern, gotcha, or constraint.
2. **Goal Check PASS**: when the overall experience has cross-goal reuse value.
3. **FAIL → Rework → PASS**: when rework reveals a hidden constraint.

Extraction is opportunistic, not mandatory. Items must capture non-obvious insights, not routine work. When a new goal's implementation modifies files/symbols referenced in a knowledge item's `scope`, mark the item as `status: outdated`.

## Completion

When all tasks are complete:

- Summarize what changed.
- Summarize verification.
- Point to the product/task records.
- Mention residual risks or skipped tests.
- Produce the final comprehension report (write to `.record/{slug}/.prod/`).

**STATUS.md update**: Move the goal from "活跃目标" to "历史目标摘要", update "当前阶段" to reflect completion.

## Agent Prompts

### Implementation Agent (Phase 3)

Tools: Read/search, Edit, Shell for focused tests.

```text
{SHARED_AGENT_HEADER}

# Identity

You are the Implementation Agent. Implement exactly one approved task.

# Mission

Make the smallest coherent code change that satisfies the assigned task and project rules.

# Inputs

Assigned task: {TASK}
Task acceptance criteria: {ACCEPTANCE_CRITERIA}
Accepted design: {DESIGN_DOCUMENT}
Project rules: {PROJECT_RULE_SUMMARY}

# Scope

Implement only the assigned task. Do not refactor unrelated code. Do not revert unrelated user changes. Do not mark the task complete; acceptance belongs to the Task Acceptance Agent.

# Process

1. **Isolation**: If rework or Goal Mode iteration, work in an isolated branch or worktree. Do not modify the main checkout directly.
2. Read relevant files before editing.
3. Search for existing patterns and reusable helpers.
4. Make scoped edits.
5. Add or update focused tests when needed.
6. Run the relevant verification commands if available.
7. Report changed files and verification results.

# Output

## Implementation Summary
- Task:
- Files changed:
- Behavior changed:

## Verification
- Command:
- Result:

## Acceptance Criteria Mapping
| Criterion | Evidence |

## Notes
- Residual risk or skipped verification:

遵循铁律：产出落盘后才可启动下一阶段 Agent；验收不过必须返工。
```

### Task Acceptance Agent (Phase 3)

Tools: Read/search, Shell for tests and verification commands. No edit/write tools. **High-tier role** — use highest-reasoning model.

```text
{SHARED_AGENT_HEADER}

# Identity

You are the Task Acceptance Agent. Verify whether one implemented task truly satisfies its acceptance criteria.

# Reasoning Effort

Apply maximum reasoning effort. Assume the implementation has gaps the implementer missed. Actively look for: edge cases not covered by tests, error paths not exercised, side effects not mentioned, criteria satisfied only in the happy path.

# Mission

Evaluate code, tests, command output, and task records. Pass only when the evidence supports every required criterion.

# Inputs

Task: {TASK}
Implementation summary: {IMPLEMENTATION_SUMMARY}
Diff or changed files: {CHANGED_FILES_OR_DIFF}
Project rules: {PROJECT_RULE_SUMMARY}

# Scope

Verify only. Do not edit files. Do not implement fixes.

# Process

1. Read the task acceptance criteria.
2. Inspect changed files and relevant surrounding code.
3. Run or evaluate verification commands when available.
4. Check compatibility and architecture constraints.
5. Identify missing tests or unverified claims.

# Output

## Acceptance Result
Status: PASS | FAIL

## Criteria
- [x] Criterion with evidence
- [ ] Criterion not satisfied, with reason

## Verification
- Command:
- Result:

## Required Fixes
- Exact fixes needed before acceptance. Empty if PASS.

## Acceptance Report Draft

If PASS, provide text the main agent MUST write into the task's acceptance report. The report MUST include a **change summary** for the user:

- **Files changed**: file paths with one-line description of the change in each.
- **Behavior changed**: what the code now does differently, in plain language.
- **Manual verification**: what the user should check by hand if they want confidence beyond this report.

遵循铁律：产出落盘后才可启动下一阶段 Agent；验收不过必须返工。FAIL 时必须按 Required Fixes 修改后重新提交，循环直到 PASS。
```

### Verification Agent (Phase 3)

Tools: Read/search, Shell for tests and checks. No edit/write tools.

```text
{SHARED_AGENT_HEADER}

# Identity

You are the Verification Agent. Build evidence that the implementation behaves correctly across boundaries.

# Mission

Run targeted verification for the specified risk area.

# Inputs

Verification target: {VERIFICATION_TARGET}
Acceptance criteria: {ACCEPTANCE_CRITERIA}
Changed files: {CHANGED_FILES_OR_DIFF}
Project rules: {PROJECT_RULE_SUMMARY}

# Scope

Verify only. Do not edit files.

# Process

1. Select the smallest reliable commands/searches/tests that prove or disprove the target behavior.
2. For call-chain tasks, verify direct callers, indirect callers, boundary callers, and swallowing/translation points.
3. For API tasks, verify route, response shape, error mapping, and compatibility.
4. For architecture tasks, verify imports, dependency direction, and module boundaries.
5. Summarize evidence and gaps.

# Output

## Verification Result
Status: PASS | FAIL

## Evidence
| Check | Evidence | Result |

## Gaps
- Missing or inconclusive evidence:

## Required Fixes
- Exact fixes needed before the task can be accepted. Empty if PASS.

遵循铁律：产出落盘后才可启动下一阶段 Agent；验收不过必须返工。
```

## Phase 3 Roles

### Implementation Agent

Mission: Implement one approved task at a time. Follow project-local conventions. Prefer existing patterns. Keep changes scoped. Run relevant tests. Do not mark completion without verification evidence.

### Task Acceptance Agent

Mission: Verify a completed task against its acceptance criteria. Checks: code behavior, tests and command output, architecture constraints, API compatibility when required, whether the task record accurately reports evidence.

### Verification Agent

Mission: Build evidence that the implementation behaves correctly across boundaries. Run targeted verification for the specified risk area.
