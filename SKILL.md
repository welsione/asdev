---
name: asdev
description: Handles complex software goals through mandatory multi-agent investigation, design, task decomposition, independent review, and acceptance validation with iterative rework. Trigger on /asdev, /goal, goal mode, 多Agent, 验收Agent, 任务拆解, 调用点, call-chain investigation, or any multi-module change requiring reliable end-to-end delivery.
---

# asdev

This skill turns a complex user goal into a disciplined delivery loop:

1. Bootstrap and detect project capabilities.
2. Investigate the real code before designing.
3. Align open questions with the user when code facts are insufficient.
4. Produce product/design notes.
5. Decompose into objective development tasks.
6. Implement tasks one by one.
7. Verify each task through tests and mandatory independent review.
8. Write acceptance status and reports back into project records.
9. **Goal mode**: iterate the whole loop until a verifiable stop condition is met, checked by an independent agent — not the one that did the work.

This skill is governed by three iron rules that no phase, no agent, and no user override may bypass:

1. **强制记录**：每个 Agent 产出必须写入 `.record/`，不落盘不推进下一阶段。
2. **强制验收**：每个阶段产出必须经独立验收 Agent 审查并返回 PASS，没有 PASS 阶段不算完成。
3. **验收不过必须返工**：FAIL 后必须按验收意见修改再提交，循环直到 PASS。无跳过、无降级、无绕过。

The central rule is: investigate first, align uncertainty with the user, design second, implement third, and verify through mandatory independent agents. The loop runs until the goal condition is proven true — the maker does not grade its own homework.

## When To Use

Use this skill for complex work that benefits from a goal-mode workflow:

- The user asks for `/asdev`, `asdev`, `/goal`, goal mode, or a multi-agent workflow.
- The task requires finding direct and indirect call sites.
- The task must prove behavior reaches a Controller/API/UI boundary.
- The task needs architecture planning, task decomposition, and acceptance criteria.
- The change spans multiple modules, services, repositories, or layers.
- The user wants review/validation agents before or after implementation.
- The request is risky enough that a one-shot edit would be brittle.

Do not use this skill for tiny one-file edits, simple questions, or direct command requests unless the user explicitly asks for goal-mode handling.

## Platform Compatibility

This skill is written for both Codex and Claude Code.

Read `references/compatibility.md` before starting if the platform/tooling situation is unclear.
Read `references/multi-agent-contract.md` before Phase 1 to confirm that mandatory independent agents can be launched.

In short:

- In Codex, discover and use the available multi-agent/subagent tools before Phase 1.
- In Claude Code, use the Agent tool (子代理) for each independent role.
- Real independent agents are mandatory. If the platform cannot spawn independent agents, stop and tell the user asdev cannot run in this environment until multi-agent support is available.
- `codegraph` and `superpowers` are optional enhancements. Detect them and use them only when available and helpful.

## First-Run Bootstrap

**Before any other work**, execute these steps:

1. Create `.record/` root and `.record/.knowledge/` if missing. The goal-scoped subdirectory `.record/{slug}/` (with `.goal/`, `.prod/`, `.task/`, `.review/`) is created at Phase 1 after the goal slug is generated.
2. Confirm the platform can spawn independent 子代理 (Agent tool in Claude Code, subagent tools in Codex). If not, stop — asdev requires multi-agent support.
3. Detect optional capabilities (`codegraph`, `superpowers`) but do not block on them.
4. Read project-local rules (CLAUDE.md, AGENTS.md) before planning.

For detailed bootstrap guidance, see `references/bootstrap.md`.

## Record Structure (Goal-Scoped)

Each goal gets its own isolated subdirectory under `.record/`:

```text
.record/
├── STATUS.md
├── loop-eng/                    ← goal slug as directory name
│   ├── .goal/
│   ├── .prod/
│   ├── .task/
│   └── .review/
├── next-goal/                   ← another goal
│   ├── .goal/
│   ├── .prod/
│   ├── .task/
│   └── .review/
└── .knowledge/                  ← shared across all goals
```

This ensures that files from different goals never mix. A goal's slug is generated at Phase 1 from 2-3 core keywords (e.g. "Loop Engineering Optimization" → `loop-eng`). See `references/recording-protocol.md` for the full slug generation rules.

## Cross-Goal Memory

asdev is record-first, but records are useless if every goal starts from zero. When a new goal begins, the main agent MUST read existing `.record/STATUS.md` first to carry forward what was learned. STATUS.md is the aggregated state view — reading it first avoids scanning all goal subdirectories.

Before Phase 1 investigation:

1. Read `.record/STATUS.md` to get the aggregated view: active goals, task progress, history, knowledge points, available connectors, recent change summaries.
2. Scan `.record/` for goal subdirectories (any directory containing `.goal/` or `.prod/`). For each prior goal, scan its `.prod/`, `.task/`, and `.review/` directories for relevant documents.
3. Scan `.record/.knowledge/` for project experience items relevant to the current goal. Build a `{PROJECT_KNOWLEDGE}` summary: each item's scope, confidence level (confirmed/inferred/assumed), and content. Items marked `status: outdated` are included with "⚠️ 已过时，请验证当前代码状态" warning. Check whether any item's `scope` references files/symbols the current goal will modify — if so, mark them as outdated.
4. Build a **historical context summary**: what was done, what passed, what failed, what was deferred, what patterns were established.
5. Pass the historical context to the Investigator Agent as `{HISTORICAL_CONTEXT}` and the project knowledge as `{PROJECT_KNOWLEDGE}`.

The historical context summary should be concise (5-10 bullets). It is not a substitute for fresh investigation — the Investigator Agent still must verify current code state. But it prevents the loop from re-discovering the same facts every run.

If `.record/` is empty (first goal), skip this step. The memory builds up over time as goals are completed. STATUS.md is created during Phase 0 Bootstrap (see `references/bootstrap.md`).

## Workflow

Read `references/workflow.md` for the complete phase-by-phase workflow.
Read `references/recording-protocol.md` before creating or updating any `.record/` files.

Default phases:

- Phase 0: First-run bootstrap and capability detection.
- Phase 1: Code investigation and requirement exploration.
- Phase 2: Task decomposition.
- Phase 3: Task-by-task implementation and acceptance.

Important pause point:

- After Phase 2, ask the user whether to proceed with development unless the user has already explicitly asked for full automatic execution.

## Running Modes

asdev supports two running modes:

| Dimension | Interactive Mode (default) | Loop Mode |
|-----------|---------------------------|-----------|
| Trigger | `/asdev` or `/goal` | Goal description contains "循环模式", "无人值守", or "自动迭代" keywords; or host platform scheduled dispatch calls `/asdev` |
| Iteration start | Manual confirmation | Automatic (depends on host scheduling or user manual re-trigger; STATUS.md breakpoint recovery) |
| User interaction | May pause at each phase | Pauses only when convergence safeguard triggers |
| Pre-implementation confirmation (Layer 3) | Enabled | Skipped (unless change density warning triggers) |
| Cognitive surrender check (Layer 2) | Understanding verification questions | Change summaries written to STATUS.md "最近变更摘要" region |
| Stop condition | Goal Check PASS or user terminates | Goal Check PASS or convergence safeguard triggers or user says "终止循环" or `/stop` |

**Loop mode activation**: Loop mode activates when the user's goal description contains one of the trigger keywords ("循环模式", "无人值守", "自动迭代"), or when the host platform's scheduling mechanism (Claude Code's `/loop` skill, hooks, cron, GitHub Actions; Codex's Automations tab) calls `/asdev` on a schedule.

**Loop mode fallback**: If the host platform's scheduling mechanism is unavailable, loop mode still works — the user manually re-triggers `/asdev [goal]` after each iteration. STATUS.md ensures breakpoint recovery so the workflow continues from where it left off, not from scratch.

**Breakpoint recovery**: When loop mode starts (or restarts), the main agent:
1. Reads `.record/STATUS.md`.
2. If an active goal exists with status "进行中", continues from the current phase.
3. If no active goal exists, starts from Phase 0.

**Mode switching**: A convergence safeguard trigger downgrades loop mode to interactive mode (waiting for user decision). After the user decides, they may choose to continue in loop mode or stay in interactive mode. The user may also switch to loop mode at any time by including a trigger keyword in their next message.

**Behavior differences by optimization**:

| Optimization | Interactive Mode | Loop Mode |
|-------------|-----------------|-----------|
| STATUS.md | Updated but optional | **Required** (breakpoint recovery depends on it) |
| Model configuration | Recommended | **Strongly recommended** (unattended review needs highest quality) |
| .knowledge/ | Recommended | Recommended |
| Cognitive surrender - Understanding verification (Layer 2) | Enabled | Skipped (written to STATUS.md instead) |
| Cognitive surrender - Pre-implementation confirmation (Layer 3) | Enabled | Skipped |
| Cognitive surrender - Change density (Layer 4) | Enabled | Enabled (still applies) |
| Worktree isolation | Branch isolation (optional) | **Worktree isolation** (recommended) |

Full behavioral difference table also available in the design document §2.7.

## Goal Mode (/goal)

Goal mode is the loop engineering layer on top of the phased workflow. Instead of running the workflow once and stopping, the workflow iterates until a **verifiable stop condition** is met.

The stop condition is a concrete, testable statement defined at Phase 1. Examples:

- "All tests in `test/auth` pass and lint is clean."
- "The `PAYMENT_TIMEOUT` error code propagates to the Controller response in all call chains."
- "The migration script runs end-to-end on the staging database with zero data loss."

### How It Works

1. **Define the stop condition** at Phase 1 alongside the design document. The stop condition must be objectively verifiable by reading files, running commands, or checking API responses — not by narrative judgment.
2. **Run the phased workflow** (Phase 0 → 1 → 2 → 3) as normal.
3. **After all tasks are complete**, launch an independent Goal Check Agent to evaluate the stop condition against actual code and test evidence.
4. **If the Goal Check Agent returns PASS**, the goal is achieved. Record the result in `.record/.goal/` and report to the user.
5. **If the Goal Check Agent returns FAIL**, it must report what is still unsatisfied. The main agent must:
   - Record the failure and the gap analysis in `.record/.review/`.
   - Return to Phase 1 to investigate the gap (not from scratch — only the unsatisfied part).
   - Update the design, task plan, or add new tasks as needed.
   - Re-run Phase 3 for the new/updated tasks.
   - Re-run the Goal Check Agent.
6. **This loop continues until the Goal Check Agent returns PASS.**

### Goal Check Agent Rules

- The Goal Check Agent MUST be a different agent from the Implementation Agent. The one that wrote the code does not grade its own homework.
- The Goal Check Agent evaluates only the stop condition — it does not re-review the design or task plan.
- The stop condition does not change between iterations. If the user wants to change it, that is a new goal.
- Each iteration's Goal Check result MUST be recorded in `.record/.review/`.

### Goal Mode Activation

Goal mode activates when:

- The user explicitly says `/goal`, "goal mode", or provides a verifiable stop condition.
- The user's goal statement already contains a concrete, testable completion criterion.

Goal mode does NOT activate when:

- The user only asks for a design or task plan without implementation.
- The user explicitly says "just the plan" or "stop after Phase 2".

### Convergence Safeguard

If the goal loop runs 3 full iterations without the Goal Check Agent returning PASS, pause and report to the user:

- What has been tried.
- What remains unsatisfied.
- Whether the stop condition may be unrealistic or requires decomposition into smaller goals.

Do not loop infinitely. The user must decide whether to adjust the goal, continue, or stop.

**Loop mode convergence adjustment**: In loop mode, the convergence safeguard is stricter — pause after 2 full iterations without PASS, or if cumulative changed files exceed 30. The stricter threshold accounts for the higher risk of unattended execution. When the safeguard triggers in loop mode, downgrade to interactive mode and notify the user.

## Mandatory Agent Roles

Read `references/agent-roles.md` before creating specialized agents.
Read `references/agent-prompts-full.md` for role-specific prompts when launching agents.

Default roles:

- Investigator Agent: discovers code facts and call chains.
- Product/Design Agent: writes requirement exploration and design notes.
- Design Acceptance Agent: reviews completeness, feasibility, consistency, and verifiability.
- Development Manager Agent: decomposes design into ordered tasks.
- Task Check Agent: reviews task granularity, dependency order, and objective acceptance criteria.
- Implementation Agent: makes code changes.
- Task Acceptance Agent: verifies task acceptance criteria and writes acceptance reports.
- Goal Check Agent: evaluates whether the verifiable stop condition is met after all tasks are complete. Only used in goal mode.

Keep role boundaries crisp. A review agent should review and report; it must not silently implement fixes unless the workflow explicitly moves back to an implementation step.

## Templates

Read `references/templates.md` when creating project-local templates or writing record files.

Default project-local outputs:

- Product/design notes: `.record/.prod/`
- Task records: `.record/.task/`
- Review records: `.record/.review/`
- Goal config: `.record/.goal/`

All generated project records should be in the user's preferred language. For Chinese projects or Chinese user prompts, default to Chinese.

## Skill Composition

This skill is the orchestration layer. Other skills may be used as subroutines.

If another available skill is clearly relevant:

1. Read that skill's `SKILL.md` before using it.
2. Apply only the parts relevant to the current phase.
3. Keep this skill's workflow as the outer delivery loop.
4. If instructions conflict, follow system/developer instructions first, then explicit user instructions, then project-local rules, then this skill, then auxiliary skills.

Examples:

- Use `superpowers` if available and helpful for planning, reflection, or review discipline.
- Use a language/framework skill during implementation if it matches the codebase.
- Use a browser skill only when the task requires browser interaction or UI verification.

If an auxiliary skill is unavailable, continue without it. This does not apply to independent multi-agent capability, which is required.

## Verification Defaults

Prefer objective verification over narrative confidence:

- Run the most relevant unit/integration tests.
- Search for forbidden imports, dependency violations, or changed API paths when those are acceptance criteria.
- Use call-chain checks for propagation tasks.
- Verify both direct and indirect call sites when the goal mentions them.
- Record exact commands and summarized results in the acceptance report.
- If tests cannot be run, explain why and record the residual risk. This does NOT bypass the iron rules — if acceptance criteria cannot be verified, the task cannot be marked complete.

## Iron Rules

These rules are absolute and apply to every phase, every agent, and every deliverable:

1. **强制记录**：每个 Agent 产出必须写入 `.record/` 对应目录。产出未落盘，下一阶段不得启动。如果保存失败，停止并报告错误，不允许跳过。
2. **强制验收**：设计文档、任务拆解、每个任务的实现——都必须经独立验收 Agent 审查并返回 PASS。没有 PASS，该阶段/任务不算完成。主 Agent 自审不算验收。
3. **验收不过必须返工**：验收 Agent 返回 FAIL 后，必须按 Required Changes / Required Fixes 修改产出，重新提交同一验收 Agent 审查。此循环持续直到 PASS。不允许跳过、降级、绕过或以"用户确认"代替验收。

Exceptions: if the user explicitly terminates a task before acceptance, record the termination and the reason in `.record/`. The task status becomes `阻塞` with documented rationale. This is the only permitted deviation from the iron rules.

## Status Aggregated View (STATUS.md)

`.record/STATUS.md` is the aggregated state view of `.record/`. The main agent maintains it at five event points: Phase 0 完成后、阶段转换时、任务状态变更时、Goal Check 后、目标完成时. STATUS.md is not an agent output and is NOT bound to Iron Rule 1's per-write enforcement. When STATUS.md conflicts with record files, record files are the source of truth and STATUS.md should be corrected at the next event point. See `references/recording-protocol.md` for full details.

## Operating Notes

- Respect the user's dirty worktree. Do not revert unrelated changes.
- Use existing project patterns over new abstractions.
- Keep task records updated as work progresses.
- Do not create broad process overhead for small tasks.
- Do not install dependencies, initialize heavyweight indexes, or modify global agent config without explicit user approval.

## Comprehension Debt Guard

A loop that ships code the user cannot read is a loop that erodes understanding. The faster the loop produces, the wider the gap between what exists and the user actually comprehends.

asdev guards against comprehension debt with **four progressive layers** that evolve the original passive check ("do you understand?") into active verification:

### Layer 1 — Per-Task Change Summary

When a task passes acceptance (not before), the main agent MUST present a concise change summary to the user:

- **What files changed** and where (file paths + brief description of the change in each).
- **What behavior changed** — in plain language, not code.
- **What the user should verify manually** if they want confidence beyond the acceptance report.

This summary is written into the task's acceptance report in `.record/` AND shown to the user directly. The user cannot be cut out of the loop by a process that only talks to itself.

### Layer 2 — Understanding Verification (every 3 tasks)

After every 3 tasks completed (or after each goal-mode iteration), the main agent MUST present an **understanding verification challenge** — NOT a passive "do you understand?" question. The user is given concrete inferences and asked to judge them. Saying "no, this inference is wrong" has a much lower psychological barrier than saying "I don't understand".

```markdown
### Understanding Verification

The following tasks have passed acceptance. Verify these inferences (answer "yes" or point out the error):

1. [Change T01] modified [file/module], with effect [behavior change].
   → Does this mean [concrete inference A]? (yes/no)

2. [Change T02] added [file/module] for [purpose].
   → If [scenario X] happens, expected behavior is [concrete inference B]? (yes/no)
```

Key difference: the question is "is this inference correct?", not "do you understand?". This shifts the cognitive load from admitting ignorance to checking a specific claim.

### Layer 3 — Pre-Implementation Confirmation (before each task)

Before each task implementation begins, the main agent MUST present the implementation intent:

```markdown
### Implementation Intent Confirmation: T03

About to implement: [task description]
Files involved: [file list]
Expected behavior change: [behavior change description]
Files NOT involved: [explicitly excluded files]

Confirm implementation scope? (yes / no / adjust)
```

**Adjustment boundary** (iron rule compatible):

- **Allowed**: adjusting implementation details (file choice, technique, scope boundary).
- **NOT allowed**: adjusting the task's **acceptance criteria**. If the user wants to change acceptance criteria, that is a task plan change — it MUST be re-submitted to the Task Check Agent for acceptance. Do not bypass the iron rules through "user confirmation".

If the user says "no", the main agent records the reason, marks the task as `阻塞`, and waits for further direction.

**Full-auto exception**: When the user explicitly opts into full-auto execution (e.g. by saying "just do it" or "auto" at the start of the goal), Layer 3 may be skipped. Layer 2 (understanding verification) is still mandatory. The choice to go full-auto is recorded in `.record/`.

### Layer 4 — Change Density Warning (within Phase 3)

When the **same file or same module** is modified across **3 consecutive tasks** in Phase 3, the main agent MUST pause and warn:

```markdown
### Change Density Warning

[File/module] has been modified in T01, T02, and T03. Please confirm:
1. Do you still understand the current state of this file/module?
2. Should I show the file's current full logic?
```

This catches the "edited too many times, lost track" failure mode before it compounds. The change density rule applies in both interactive and full-auto modes (Layer 3 may be skipped, Layer 4 cannot).

### Final Comprehension Report

At Completion (or Goal Check PASS), the main agent MUST produce a comprehension report alongside the standard summary:

- A list of all changed files with one-line descriptions.
- A list of new concepts, patterns, or abstractions introduced.
- Any risks or side effects that the acceptance reports flagged but the user may not have seen.

This report is written into `.record/.prod/` as part of the goal's final record.
