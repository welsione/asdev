---
name: asdev
description: Use this skill whenever the user asks to handle a complex software goal, refactor, architecture change, security fix, call-chain investigation, multi-step implementation, or goal-mode workflow with mandatory multi-agent task decomposition, independent review, acceptance validation, and iterative verification. Trigger especially when the user mentions /asdev, asdev, goal mode, /goal, 多Agent, 验收Agent, 检查Agent, 需求探索, 任务拆解, 调用点, 间接调用点, or wants reliable end-to-end delivery instead of a one-shot code edit. This skill supports both Codex and Claude Code and requires real independent agent capability; codegraph and superpowers are optional enhancements.
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

The central rule is: investigate first, align uncertainty with the user, design second, implement third, and verify through mandatory independent agents.

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
- In Claude Code, use the Task tool for each independent role.
- Real independent agents are mandatory. If the platform cannot spawn independent agents, stop and tell the user asdev cannot run in this environment until multi-agent support is available.
- `codegraph` and `superpowers` are optional enhancements. Detect them and use them only when available and helpful.

## First-Run Bootstrap

Before Phase 1, check whether this project has already been initialized for this workflow.

Read `references/bootstrap.md` and follow it when:

- `.record/` does not exist.
- There is no task template.
- There is no product/design template.
- The project has no local goal configuration.
- This is the user's first time using this skill in the project.

The bootstrap should be lightweight. Create directories and templates only inside the current project/workspace. Do not install external tools automatically.

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

## Mandatory Agent Roles

Read `references/agent-roles.md` before creating specialized agents.
Read `references/agent-prompts.md` and `references/prompt-assembly.md` before launching agents. Then read only the role-specific prompt files needed for the current phase.

Default roles:

- Investigator Agent: discovers code facts and call chains.
- Product/Design Agent: writes requirement exploration and design notes.
- Design Acceptance Agent: reviews completeness, feasibility, consistency, and verifiability.
- Development Manager Agent: decomposes design into ordered tasks.
- Task Check Agent: reviews task granularity, dependency order, and objective acceptance criteria.
- Implementation Agent: makes code changes.
- Task Acceptance Agent: verifies task acceptance criteria and writes acceptance reports.

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

If tests cannot be run, explain why and record the residual risk.

## Operating Notes

- Respect the user's dirty worktree. Do not revert unrelated changes.
- Use existing project patterns over new abstractions.
- Keep task records updated as work progresses.
- Do not create broad process overhead for small tasks.
- Do not install dependencies, initialize heavyweight indexes, or modify global agent config without explicit user approval.
