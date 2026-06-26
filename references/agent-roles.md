# Agent Roles

## Table of Contents

| # | Section | Description |
|---|---------|-------------|
| 1 | [Iron Rules For All Roles](#iron-rules-for-all-roles) | Mandatory recording, acceptance, and rework rules |
| 2 | [Mandatory Multi-Agent Contract](#mandatory-multi-agent-contract) | Platform requirements for independent agent support |
| 3 | [Model Configuration Guidance](#model-configuration-guidance) | Recommended model tier and reasoning effort per role |
| 4 | [Main Agent Responsibilities (Phase 3 Comprehension Guard)](#main-agent-responsibilities-phase-3-comprehension-guard) | Main agent runs the four comprehension-debt-guard layers |
| 5 | [Main Agent Responsibilities (Knowledge Extraction)](#main-agent-responsibilities-knowledge-extraction) | Main agent distills experience into `.record/.knowledge/` |
| 4 | [Investigator Agent](#investigator-agent) | Discovers code facts and call chains before design |
| 5 | [Product/Design Agent](#productdesign-agent) | Converts facts and goals into design documents |
| 6 | [Design Acceptance Agent](#design-acceptance-agent) | Reviews Phase 1 design before task decomposition |
| 7 | [Development Manager Agent](#development-manager-agent) | Decomposes accepted design into ordered tasks |
| 8 | [Task Check Agent](#task-check-agent) | Reviews task plan quality and granularity |
| 9 | [Implementation Agent](#implementation-agent) | Implements one approved task at a time |
| 10 | [Task Acceptance Agent](#task-acceptance-agent) | Verifies completed tasks against acceptance criteria |
| 11 | [Goal Check Agent](#goal-check-agent) | Evaluates whether the verifiable stop condition is met |

asdev requires real independent agents. Use the platform's multi-agent mechanism for every review/check role. If independent agents cannot be spawned, stop the workflow and tell the user that asdev requires multi-agent support in the current environment.

The purpose of roles is separation of concerns. Review roles identify issues; implementation roles make changes.

## Iron Rules For All Roles

1. **强制记录**：Every agent output MUST be saved to `.record/{slug}/` (where `{slug}` is the current goal's slug) before any next-phase agent is launched.
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

## Main Agent Responsibilities (Phase 3 Comprehension Guard)

The main agent (orchestrator) is responsible for running the four comprehension-debt-guard layers defined in `SKILL.md`:

1. **Layer 1 — Per-Task Change Summary**: After each task PASS, present files changed, behavior changed, manual verification hints. Write the summary into the acceptance report AND show to the user.
2. **Layer 2 — Understanding Verification**: Every 3 tasks, present concrete inferences for the user to judge (NOT a passive "do you understand?" question). User says "no" → explain and re-verify before proceeding.
3. **Layer 3 — Pre-Implementation Confirmation**: Before each task, present implementation intent (task description, files involved, expected behavior change, files NOT involved) and confirm scope. Adjustments allowed only on implementation details; acceptance criteria changes re-trigger Task Check. Full-auto exception: skipped if user opted into full-auto at goal start.
4. **Layer 4 — Change Density Warning**: Before each task, check whether the same file/module has been modified in the previous 2 tasks. If yes, present the warning and pause for confirmation. Applies in both interactive and full-auto modes.

The main agent tracks which files/modules each task has modified (in `.record/STATUS.md` "最近变更摘要" and "任务进度" sections) to enable Layer 4 detection.

## Main Agent Responsibilities (Knowledge Extraction)

The main agent is also responsible for **distilling execution experience** into reusable knowledge items in `.record/.knowledge/`. Three trigger event points:

1. **Task PASS**: after a task passes acceptance, evaluate whether the implementation surfaced a non-obvious pattern. If yes, write a `.record/.knowledge/KNOW_*.md`.
2. **Goal Check PASS**: after the goal completes, evaluate whether the overall experience has cross-goal reuse value. If yes, write a knowledge item.
3. **FAIL → Rework → PASS**: when rework reveals a hidden constraint, that failure teaches the most — capture it.

Extraction is opportunistic, not mandatory. Items must capture non-obvious insights, not routine work. When a new goal's implementation modifies files/symbols referenced in a knowledge item's `scope`, the main agent MUST mark the item as `status: outdated` and pass it to the Investigator Agent with an outdated warning. See `references/recording-protocol.md` for the full knowledge-item format.

## Model Configuration Guidance

asdev's "maker does not grade own homework" principle is enforced at the agent role level (separate Implementation Agent vs Task Acceptance Agent). To strengthen this principle, **recommend a higher-reasoning model tier for review/acceptance roles** so they do not share the same cognitive blind spots as the implementation roles.

This is **advisory** — the platform may not support per-agent model selection. When unsupported, fall back to prompt-level reasoning-effort instructions and record the degradation in `.record/`.

### Role-Model Mapping

| Role | Recommended Tier | Reasoning Effort | Reason |
|------|------------------|------------------|--------|
| Investigator Agent | Standard | Medium | Facts are facts; needs breadth, not depth |
| Product/Design Agent | Standard | Medium | Creative + structured output; standard model is enough |
| Design Acceptance Agent | **High** | **High** | Reviewer must catch design blind spots; reasoning effort must exceed the designer's |
| Development Manager Agent | Standard | Medium | Structured decomposition; standard model is enough |
| Task Check Agent | **High** | **High** | Reviewer must find task plan defects |
| Implementation Agent | Standard | Medium | Execution role; follow the spec |
| Task Acceptance Agent | **High** | **High** | Reviewer must find implementation vs. spec deviations |
| Goal Check Agent | **High** | **High** | Final acceptance; highest reasoning effort |

### Platform Implementation

- **Claude Code**: Pass `model: "opus"` (or the platform's highest-reasoning model) to the Agent tool when launching the four high-tier roles. Implementation and investigation roles use the default model (e.g. `model: "sonnet"` or omitted).
- **Codex**: If the platform supports per-agent model selection, follow the same mapping. If not, fall back to adding "请以最高推理努力执行审查" to the prompts of high-tier roles as a prompt-level reasoning-effort instruction.
- **Detection**: In Phase 0 Bootstrap, attempt to launch a read-only test agent (e.g. one that runs `echo "test"`) with a specified model identifier. If the launch succeeds, the platform supports model selection. If it fails, record the failure and use the prompt-level fallback.
- **Degradation record**: When the platform does not support model selection, the main agent MUST record the degradation fact and its residual risk in `.record/{slug}/` (e.g. in the Goal Config or a Phase 0 note in `.record/{slug}/.prod/`).

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

If status is PASS, the goal is achieved. Record the result in `.record/{slug}/.goal/`.

If status is FAIL, the main agent MUST return to Phase 1 to investigate the gap, update the design and tasks, re-implement, and re-submit for Goal Check. This loop is mandatory and continues until PASS. The convergence safeguard in `references/workflow.md` applies.
