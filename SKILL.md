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

1. Create `.record/` directories if missing: `.record/.goal/`, `.record/.prod/`, `.record/.task/`, `.record/.review/`. If creation fails, stop and report.
2. Confirm the platform can spawn independent 子代理 (Agent tool in Claude Code, subagent tools in Codex). If not, stop — asdev requires multi-agent support.
3. Detect optional capabilities (`codegraph`, `superpowers`) but do not block on them.
4. Read project-local rules (CLAUDE.md, AGENTS.md) before planning.

For detailed bootstrap guidance, see `references/bootstrap.md`.

## Cross-Goal Memory

asdev is record-first, but records are useless if every goal starts from zero. When a new goal begins, the main agent MUST read existing `.record/` content to carry forward what was learned.

Before Phase 1 investigation:

1. Scan `.record/.prod/` for prior investigation and design documents.
2. Scan `.record/.task/` for prior task records and their completion status.
3. Scan `.record/.review/` for prior acceptance and review outcomes.
4. Build a **historical context summary**: what was done, what passed, what failed, what was deferred, what patterns were established.
5. Pass this summary to the Investigator Agent as `{HISTORICAL_CONTEXT}` so it does not re-derive what is already known.

The historical context summary should be concise (5-10 bullets). It is not a substitute for fresh investigation — the Investigator Agent still must verify current code state. But it prevents the loop from re-discovering the same facts every run.

If `.record/` is empty (first goal), skip this step. The memory builds up over time as goals are completed.

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

## Operating Notes

- Respect the user's dirty worktree. Do not revert unrelated changes.
- Use existing project patterns over new abstractions.
- Keep task records updated as work progresses.
- Do not create broad process overhead for small tasks.
- Do not install dependencies, initialize heavyweight indexes, or modify global agent config without explicit user approval.

## Comprehension Debt Guard

A loop that ships code the user cannot read is a loop that erodes understanding. The faster the loop produces, the wider the gap between what exists and what the user actually comprehends.

asdev guards against comprehension debt with three mechanisms:

### 1. Change Summary After Each Task

When a task passes acceptance (not before), the main agent MUST present a concise change summary to the user:

- **What files changed** and where (file paths + brief description of the change in each).
- **What behavior changed** — in plain language, not code.
- **What the user should verify manually** if they want confidence beyond the acceptance report.

This summary is written into the task's acceptance report in `.record/` AND shown to the user directly. The user cannot be cut out of the loop by a process that only talks to itself.

### 2. Anti-Cognitive-Surrender Check

After every 3 tasks completed (or after each goal-mode iteration), the main agent MUST ask the user:

- "以下任务已完成验收。请确认你是否理解变更内容，或是否需要我解释任何部分。"

If the user responds that they do not understand a change, the main agent MUST explain it before proceeding. Do not accumulate code the user cannot read.

### 3. Final Comprehension Report

At Completion (or Goal Check PASS), the main agent MUST produce a comprehension report alongside the standard summary:

- A list of all changed files with one-line descriptions.
- A list of new concepts, patterns, or abstractions introduced.
- Any risks or side effects that the acceptance reports flagged but the user may not have seen.

This report is written into `.record/.prod/` as part of the goal's final record.
