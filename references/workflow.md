# Goal-Driven Workflow

## Contents

- [Iron Rules](#iron-rules)
- [Phase 0 - Bootstrap](#phase-0---bootstrap)
- [Phase 1 - Code Investigation And Requirement Exploration](#phase-1---code-investigation-and-requirement-exploration)
  - [0. Read Historical Context](#0-read-historical-context)
  - [1. Understand The User Goal](#1-understand-the-user-goal)
  - [2. Investigate Current Code](#2-investigate-current-code)
  - [3. Align Open Questions](#3-align-open-questions)
  - [4. Write Requirement Exploration](#4-write-requirement-exploration)
  - [5. Design Acceptance Review](#5-design-acceptance-review)
- [Phase 2 - Task Decomposition](#phase-2---task-decomposition)
- [Phase 3 - Task-By-Task Implementation And Acceptance](#phase-3---task-by-task-implementation-and-acceptance)
  - [Comprehension Debt Guard (Phase 3)](#comprehension-debt-guard-phase-3)
- [Completion](#completion)
- [Goal Mode Loop](#goal-mode-loop)
  - [Phase 1 Addition: Define Stop Condition](#phase-1-addition-define-stop-condition)
  - [After Completion: Goal Check](#after-completion-goal-check)
  - [Convergence Safeguard](#convergence-safeguard)

This workflow is the core of the skill.

## Iron Rules

These rules are absolute and apply to every phase:

1. **强制记录**：每个 Agent 产出必须写入 `.record/` 对应目录。产出未落盘，下一阶段不得启动。
2. **强制验收**：每个阶段产出必须经独立验收 Agent 审查并返回 PASS。没有 PASS，阶段不算完成。
3. **验收不过必须返工**：FAIL 后必须按验收意见修改再提交，循环直到 PASS。无跳过、无降级、无绕过。

## Phase 0 - Bootstrap

Use `references/bootstrap.md`.
Use `references/multi-agent-contract.md` to confirm that independent agents are available.
Use `references/recording-protocol.md` for record paths and naming.

Outputs:

- Confirmed project rule files.
- Record directories/templates when missing.
- Detected verification commands when obvious.
- Capability notes, including confirmation that multi-agent execution is available.

Do not spend too long on Phase 0. Its job is to prepare the workflow, not to solve the feature.

## Phase 1 - Code Investigation And Requirement Exploration

Start by investigating real code. Do not write the design document from assumptions.

### 0. Read Historical Context

Before launching any specialist agent, scan existing `.record/` for prior goals:

1. Scan `.record/.prod/` for prior investigation and design documents.
2. Scan `.record/.task/` for prior task records and completion status.
3. Scan `.record/.review/` for prior acceptance and review outcomes.
4. Build a concise historical context summary (5-10 bullets): what was done, what passed, what failed, what was deferred, what patterns were established.
5. Pass this summary as `{HISTORICAL_CONTEXT}` to the Investigator Agent.

If `.record/` is empty (first goal), skip this step. The memory builds up over time.

The historical context does not replace fresh investigation. The Investigator Agent still must verify current code state. But it prevents re-discovering the same facts every run — the agent forgets, the repo doesn't.

### 1. Understand The User Goal

The main agent restates the goal in operational terms before launching specialist agents:

- What behavior should change?
- Which boundary must observe the behavior? Controller, API, UI, CLI, job, event listener, etc.
- What must remain compatible?
- What evidence will prove success?

### 2. Investigate Current Code

Launch an independent Investigator Agent to gather code facts. The main agent may do additional reading, but the investigation record must include the independent agent's findings.
Save the investigation output according to `references/recording-protocol.md`.

**Iron rule 1 enforcement**: The investigation output MUST be written to `.record/.prod/` before the Product/Design Agent is launched. If saving fails, stop and report.

Use code search and project rules to gather facts:

- Entry points and outward-facing interfaces.
- Direct call sites.
- Indirect call chains.
- Existing exception/error/result propagation.
- Existing similar implementations.
- Module boundaries and dependency direction.
- Tests that cover the behavior.
- Gaps between current behavior and target behavior.

For call-chain tasks, explicitly separate:

- Direct callers.
- Indirect callers.
- Boundary callers such as Controller/API/SSE/job endpoints.
- Error handling or wrapping points that may swallow, translate, or hide the target behavior.

### 3. Align Open Questions

Pause and ask the user when a decision cannot be safely inferred from code:

- Business semantics are ambiguous.
- Multiple implementation paths are reasonable.
- API compatibility, data migration, security, permission, or performance could be affected.
- Acceptance criteria cannot be made objective.
- The code facts conflict with the user's stated expectation.

Ask only the questions that materially affect the plan.

If the user does not want to discuss details and asks you to proceed, document assumptions clearly.

### 4. Write Requirement Exploration

Launch a Product/Design Agent to draft the requirement exploration from the user goal, project rules, investigation findings, and user-aligned answers.
Save the design document according to `references/recording-protocol.md`.

**Iron rule 1 enforcement**: The design document MUST be written to `.record/.prod/` before the Design Acceptance Agent is launched. If saving fails, stop and report.

Create a document in `.record/.prod/`, unless the project uses another convention.

The document should include:

- Background and goal.
- Current code facts.
- Direct and indirect call-chain analysis when relevant.
- Impact scope.
- Open questions and user-confirmed answers.
- Proposed architecture/design.
- Core flow.
- Data model/API changes, or "none".
- Key design decisions and reasons.
- Risks and verification strategy.

### 5. Design Acceptance Review

Submit the design to an independent Design Acceptance Agent.
Save the review output according to `references/recording-protocol.md`.

**Iron rule 2 enforcement**: The design is not accepted until the Design Acceptance Agent returns PASS.

**Iron rule 3 enforcement**: If the Design Acceptance Agent returns FAIL, the design MUST be revised according to Required Changes and re-submitted for another acceptance review. This revision loop is mandatory and continues until PASS. There is no skip or override.

Review dimensions:

- Fact completeness: based on real code investigation, not imagination.
- Impact scope: covers direct and indirect call paths.
- Feasibility: implementable in the existing architecture.
- Consistency: respects project rules and existing patterns.
- Verifiability: can become objective task acceptance criteria.

If the review fails, the design MUST be revised and re-submitted. This loop is mandatory and continues until the Design Acceptance Agent returns PASS.

## Phase 2 - Task Decomposition

Use the accepted Phase 1 design as input.

Launch a Development Manager Agent to create the task decomposition.
Save the task document according to `references/recording-protocol.md`.

**Iron rule 1 enforcement**: The task document MUST be written to `.record/.task/` before the Task Check Agent is launched. If saving fails, stop and report.

Create a task document in `.record/.task/`, unless the project uses another convention.

Each task should include:

- Task description: what to do.
- Task reason: why it matters and what design goal it supports.
- Task goal: measurable completion target.
- Acceptance criteria: objective checklist.
- Task status: initially incomplete.
- Acceptance report: initially empty.

Task quality rules:

- Order tasks by dependencies and risk.
- Keep each task independently reviewable.
- Include test/build verification in each task when meaningful.
- Avoid vague criteria such as "works well" or "improve quality".
- Mention compatibility requirements explicitly.

Submit the task plan to an independent Task Check Agent.
Save the task check output according to `references/recording-protocol.md`.

**Iron rule 2 enforcement**: The task plan is not accepted until the Task Check Agent returns PASS.

**Iron rule 3 enforcement**: If the Task Check Agent returns FAIL, the task plan MUST be revised according to Required Changes and re-submitted. This loop is mandatory and continues until PASS.

Review dimensions:

- Task granularity.
- Dependency order.
- Objective acceptance criteria.
- Missing risk-reduction tasks.
- Whether tests/verification are realistic.

If the review fails, the task plan MUST be revised and re-submitted. This loop is mandatory and continues until PASS.

After Phase 2, pause and ask whether to proceed with development unless the user already asked for full execution.

## Phase 3 - Task-By-Task Implementation And Acceptance

For each task in order:

1. Read the task and relevant project rules.
2. Investigate the exact files before editing.
3. Implement the smallest coherent change, using an Implementation Agent when the platform supports agent file edits in the active workspace.
4. Run focused verification.
5. Run broader verification when risk or acceptance criteria require it.
6. **Iron rule 1 enforcement**: Save the implementation summary to `.record/` before launching the Task Acceptance Agent. If saving fails, stop and report.
7. Submit to an independent Task Acceptance Agent.
8. **Iron rule 2 enforcement**: The task is not complete until the Task Acceptance Agent returns PASS.
9. **Iron rule 3 enforcement**: If the Task Acceptance Agent returns FAIL, fix according to Required Fixes and re-submit. This loop is mandatory and continues until PASS.
10. Save the acceptance output according to `references/recording-protocol.md`.
11. If accepted, update task status and acceptance report.
12. If rejected, fix according to review findings and re-run acceptance. This loop continues until PASS.

Acceptance reports should record:

- Files changed.
- Verification commands and summarized results.
- Which acceptance criteria passed.
- Any criteria not verified and why.
- Residual risks.

Do not mark a task complete until the Task Acceptance Agent returns PASS. The only exception is if the user explicitly terminates the task — in that case, record the termination and reason in `.record/`, set status to `阻塞`, and document it as an exception.

### Comprehension Debt Guard (Phase 3)

After each task passes acceptance, the main agent MUST present a **change summary** to the user:

- What files changed and where (file paths + brief description).
- What behavior changed — in plain language, not code.
- What the user should verify manually if they want confidence beyond the acceptance report.

This summary is written into the task's acceptance report AND shown to the user. The user cannot be cut out of the loop.

After every 3 tasks completed, the main agent MUST ask the user:

> "以下任务已完成验收。请确认你是否理解变更内容，或是否需要我解释任何部分。"

If the user does not understand a change, the main agent MUST explain it before proceeding. Do not accumulate code the user cannot read.

## Completion

When all tasks are complete:

- Summarize what changed.
- Summarize verification.
- Point to the product/task records.
- Mention residual risks or skipped tests.
- **Comprehension Debt Guard**: Produce a final comprehension report:
  - All changed files with one-line descriptions.
  - New concepts, patterns, or abstractions introduced.
  - Risks or side effects flagged in acceptance reports that the user may not have seen.
  - Write this report into `.record/.prod/` as part of the goal's final record.

Keep the final response concise; the detailed evidence belongs in the record files.

## Goal Mode Loop

Goal mode activates when the user provides a verifiable stop condition or explicitly requests `/goal` or goal mode. It wraps the phased workflow in an outer loop that iterates until the stop condition is proven true.

### Phase 1 Addition: Define Stop Condition

When goal mode is active, add this step after "Write Requirement Exploration":

1. Extract or refine the **verifiable stop condition** from the user's goal.
2. The stop condition must be objectively testable: a command that exits 0, a test suite that passes, an API response that matches a shape, a grep that finds/does not find a pattern.
3. Write the stop condition into the design document under a new section: "## 停止条件 (Stop Condition)".
4. The stop condition does not change between iterations. If the user wants to change it, that is a new goal.

### After Completion: Goal Check

When all tasks are complete and the standard Completion step is done:

1. Launch an independent **Goal Check Agent** to evaluate the stop condition.
2. The Goal Check Agent MUST be different from the Implementation Agent. The maker does not grade its own homework.
3. The Goal Check Agent reads the stop condition, inspects the code, runs verification commands, and returns PASS or FAIL with evidence.

**Iron rule 1 enforcement**: The Goal Check result MUST be saved to `.record/.review/` before any next action.

**Iron rule 2 enforcement**: The goal is not achieved until the Goal Check Agent returns PASS.

**Iron rule 3 enforcement**: If the Goal Check Agent returns FAIL, the main agent MUST:

1. Record the failure and gap analysis in `.record/.review/`.
2. Return to Phase 1 to investigate the gap — not from scratch, only the unsatisfied part.
3. Update the design, add or revise tasks as needed.
4. Re-run Phase 3 for the new/updated tasks.
5. Re-run the Goal Check Agent.
6. This loop continues until PASS.

### Convergence Safeguard

If the goal loop runs 3 full iterations (Phase 1 → 3 → Goal Check) without PASS:

1. Pause the loop.
2. Report to the user:
   - What has been tried across all iterations.
   - What remains unsatisfied and why.
   - Whether the stop condition may be unrealistic or needs decomposition.
3. The user must decide: adjust the goal, continue, or stop.
4. Record the decision in `.record/.goal/`.

Do not loop infinitely. The safeguard exists because a loop that cannot converge is a design problem, not a persistence problem.
