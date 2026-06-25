# Agent Roles

asdev requires real independent agents. Use the platform's multi-agent mechanism for every review/check role. If independent agents cannot be spawned, stop the workflow and tell the user that asdev requires multi-agent support in the current environment.

The purpose of roles is separation of concerns. Review roles identify issues; implementation roles make changes.

## Mandatory Multi-Agent Contract

Before Phase 1, confirm that the platform can create independent agents:

- Codex: use the available multi-agent/subagent tooling exposed in the session.
- Claude Code: use the Task tool.

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

If status is PASS, the task status and acceptance report may be updated.
