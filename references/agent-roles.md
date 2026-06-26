# Agent Roles

## Table of Contents

| # | Section | Description |
|---|---------|-------------|
| 1 | [Iron Rules For All Roles](#iron-rules-for-all-roles) | Mandatory recording, acceptance, and rework rules |
| 2 | [Mandatory Multi-Agent Contract](#mandatory-multi-agent-contract) | Platform requirements for independent agent support |
| 3 | [Investigator Agent](#investigator-agent) | Discovers code facts and call chains before design |
| 4 | [Product/Design Agent](#productdesign-agent) | Converts facts and goals into design documents |
| 5 | [Design Acceptance Agent](#design-acceptance-agent) | Reviews Phase 1 design before task decomposition |
| 6 | [Development Manager Agent](#development-manager-agent) | Decomposes accepted design into ordered tasks |
| 7 | [Task Check Agent](#task-check-agent) | Reviews task plan quality and granularity |
| 8 | [Implementation Agent](#implementation-agent) | Implements one approved task at a time |
| 9 | [Task Acceptance Agent](#task-acceptance-agent) | Verifies completed tasks against acceptance criteria |
| 10 | [Goal Check Agent](#goal-check-agent) | Evaluates whether the verifiable stop condition is met |

asdev requires real independent agents. Use the platform's multi-agent mechanism for every review/check role. If independent agents cannot be spawned, stop the workflow and tell the user that asdev requires multi-agent support in the current environment.

The purpose of roles is separation of concerns. Review roles identify issues; implementation roles make changes.

## Iron Rules For All Roles

1. **强制记录**：Every agent output MUST be saved to `.record/` before any next-phase agent is launched.
2. **强制验收**：No deliverable is accepted until the corresponding acceptance agent returns PASS.
3. **验收不过必须返工**：When an acceptance agent returns FAIL, the deliverable MUST be revised and re-submitted. This loop continues until PASS.

## Mandatory Multi-Agent Contract

Before Phase 1, confirm that the platform can create independent agents:

- Codex: use the available multi-agent/subagent tooling exposed in the session.
- Claude Code: use the Agent tool (子代理).

Use `references/multi-agent-contract.md` for detailed detection and failure handling.

At minimum, asdev must be able to run these independent roles:

- Investigator Agent.
- Product/Design Agent.
- Design Acceptance Agent.
- Development Manager Agent.
- Task Check Agent.
- Task Acceptance Agent.

For implementation, use a separate Implementation Agent per task when the platform supports agent file edits in the active workspace. If implementation agents cannot safely edit the shared workspace, the main agent may implement, but independent task acceptance remains mandatory.

Do not replace review agents with main-agent self-review.

Use `references/agent-prompts.md` and `references/prompt-assembly.md` for the default prompts and output contracts of each role.

## Investigator Agent

Mission:

- Discover code facts before design.
- Find direct and indirect call sites.
- Identify current behavior, wrappers, exception translators, and boundary endpoints.

Inputs:

- User goal.
- Project rule files.
- Relevant code search results.

Outputs:

- Factual investigation notes.
- Call-chain summary when relevant.
- Unknowns that require user alignment.

Should not:

- Implement fixes.
- Invent requirements.

## Product/Design Agent

Mission:

- Convert code facts and user goal into a design/requirement exploration document.

Outputs:

- Background and goal.
- Current code facts.
- Impact scope.
- Proposed design.
- Verification strategy.

Should not:

- Skip unresolved questions.
- Hide assumptions.

## Design Acceptance Agent

Mission:

- Review the Phase 1 document before task decomposition.

Checks:

- Completeness.
- Feasibility.
- Consistency with architecture.
- Verifiability.
- Coverage of direct and indirect call paths when relevant.

Output format:

```markdown
## Review Result

Status: PASS | FAIL

## Findings

- [severity] Finding with evidence

## Required Changes

- Change needed before approval

## Notes

- Additional observations
```

Should not:

- Modify the design directly unless the workflow explicitly asks for revision.

## Development Manager Agent

Mission:

- Decompose accepted design into ordered tasks.

Outputs:

- Task document following `TASK_TEMPLATE.md`.
- Dependency order.
- Objective acceptance criteria.

Should not:

- Start implementation.

## Task Check Agent

Mission:

- Review task plan quality.

Checks:

- Granularity.
- Dependency order.
- Objective acceptance.
- Missing tests or risk controls.

Output format:

```markdown
## Check Result

Status: PASS | FAIL

## Findings

- [severity] Finding with evidence

## Required Changes

- Change needed before development
```

## Implementation Agent

Mission:

- Implement one approved task at a time.

Rules:

- Follow project-local conventions.
- Prefer existing patterns.
- Keep changes scoped.
- Run relevant tests.
- Do not mark completion without verification evidence.

## Task Acceptance Agent

Mission:

- Verify a completed task against its acceptance criteria.

Checks:

- Code behavior.
- Tests and command output.
- Architecture constraints.
- API compatibility when required.
- Whether the task record accurately reports evidence.

Output format:

```markdown
## Acceptance Result

Status: PASS | FAIL

## Criteria

- [x] Criterion with evidence
- [ ] Criterion not satisfied

## Verification

- Command: `...`
- Result: summarized result

## Required Fixes

- Fix needed before completion
```

If status is PASS, the task status and acceptance report MUST be updated.

If status is FAIL, the Implementation Agent MUST fix according to Required Fixes and re-submit for acceptance. This loop is mandatory and continues until PASS.

## Goal Check Agent

Mission:

- Evaluate whether a verifiable stop condition is met after all tasks are complete.
- Only used in goal mode.

Inputs:

- The verifiable stop condition.
- The design document with task records.
- Changed files and verification evidence.

Checks:

- The stop condition is objectively testable.
- Each part of the stop condition is satisfied by actual code/test evidence.
- No part of the stop condition relies on narrative judgment.

Output format:

```markdown
## Goal Check Result

Status: PASS | FAIL

## Stop Condition Evaluation

| Condition | Evidence | Result |
| --- | --- | --- |

## Gap Analysis

- Unsatisfied conditions and why:

## Recommended Next Steps

If FAIL, describe what is still needed to satisfy the stop condition.
```

If status is PASS, the goal is achieved. Record the result in `.record/.goal/`.

If status is FAIL, the main agent MUST return to Phase 1 to investigate the gap, update the design and tasks, re-implement, and re-submit for Goal Check. This loop is mandatory and continues until PASS. The convergence safeguard in `references/workflow.md` applies.
