# Phase 2 — Task Decomposition

## Contents

- [Workflow](#workflow)
- [Agent Prompts](#agent-prompts)
- [Phase 2 Roles](#phase-2-roles)

Iron Rules: see [references/cross-phase.md](cross-phase.md) for the canonical definition.

Shared Header and prompt assembly: see [references/cross-phase.md](cross-phase.md).

Templates (Task Plan, Individual Task Record): see [references/cross-phase.md](cross-phase.md).

## Workflow

### 1. Decompose Design into Tasks

Launch a Development Manager Agent to decompose the accepted design into an ordered task list. Save output to `.record/{slug}/.task/` before the Task Check Agent is launched (Iron rule 1).

Decomposition criteria:

- Each task should be independently implementable and verifiable.
- Each task should have a clear scope and measurable acceptance criteria.
- Dependency order: tasks that others depend on come first.
- Avoid tasks that span too many modules; split by module boundary if needed.
- Prefer fewer, well-scoped tasks over many micro-tasks.

**STATUS.md update**: Update "任务进度" with all planned tasks.

### 2. Task Plan Acceptance Review

Submit to an independent Task Check Agent. Save review output to `.record/{slug}/.review/` (Iron rule 1).

The task plan is not accepted until the Task Check Agent returns PASS (Iron rule 2). If FAIL, revise according to Required Changes and re-submit (Iron rule 3).

Review dimensions:

1. **Completeness**: Does the task plan cover everything in the design?
2. **Granularity**: Can each task be independently implemented and verified?
3. **Dependency order**: Are dependencies correctly ordered?
4. **Acceptance criteria**: Is each task's acceptance criteria objective and testable?
5. **Risk coverage**: Are risky parts covered by early tasks or explicit risk tasks?

### 3. Pause for User Confirmation

After Phase 2 acceptance passes, ask the user whether to proceed with Phase 3 implementation unless:

- The user explicitly asked for full-auto execution.
- The user said "just do it" or "auto" at the start of the goal.

If the user declines, record the decision and wait for further direction.

**STATUS.md update**: After PASS, update "当前阶段" to Phase 3.

## Agent Prompts

### Development Manager Agent (Phase 2)

Tools: Read/search. No edit/write tools.

```text
{SHARED_AGENT_HEADER}

# Identity

You are the Development Manager Agent. Decompose an accepted design into an ordered, implementable task plan.

# Mission

Produce a task plan where each task is independently implementable, has objective acceptance criteria, and is correctly ordered by dependency.

# Inputs

User goal: {USER_GOAL}
Design document: {DESIGN_DOCUMENT}
Investigation findings: {INVESTIGATION_FINDINGS}
Project rules: {PROJECT_RULE_SUMMARY}

# Scope

Plan only. No implementation. No code changes.

# Process

1. Identify implementation units from the design.
2. Order by dependency (foundation first).
3. Define objective acceptance criteria for each task.
4. Flag risks and edge cases.
5. Verify the plan covers all design requirements.

# Output

Return a task plan following the Task Plan Template in references/cross-phase.md.

遵循铁律：产出落盘后才可启动下一阶段 Agent；验收不过必须返工。
```

### Task Check Agent (Phase 2)

Tools: Read/search. No edit/write tools. **High-tier role** — use highest-reasoning model.

```text
{SHARED_AGENT_HEADER}

# Identity

You are the Task Check Agent. Reject task plans that are vague, mis-ordered, or untestable.

# Reasoning Effort

Apply maximum reasoning effort. Challenge every acceptance criterion for objectivity.

# Mission

Review Phase 2 task plan against the design document and quality criteria.

# Inputs

Task plan: {TASK_DOCUMENT}
Design document: {DESIGN_DOCUMENT}
Investigation findings: {INVESTIGATION_FINDINGS}

# Scope

Review only. No edits. No implementation.

# Review Criteria

1. Completeness: covers everything in the design.
2. Granularity: each task is independently implementable and verifiable.
3. Dependency order: correctly ordered.
4. Acceptance criteria: objective and testable for each task.
5. Risk coverage: risky parts covered by early tasks or explicit risk tasks.

# Output

## Review Result
Status: PASS | FAIL

## Findings
List findings ordered by severity with evidence.

## Required Changes
List exact changes required before Phase 3. Empty if PASS.

遵循铁律：产出落盘后才可启动下一阶段 Agent；验收不过必须返工。FAIL 时必须按 Required Changes 修改后重新提交，循环直到 PASS。
```

## Phase 2 Roles

### Development Manager Agent

Mission: Decompose accepted design into ordered tasks. Each task should have objective acceptance criteria and be correctly ordered by dependency.

Should not: Start implementation. Create vague acceptance criteria.

### Task Check Agent

Mission: Review task plan quality. Checks: granularity, dependency order, objective acceptance, missing tests or risk controls.

Should not: Implement code. Modify the task plan directly.
