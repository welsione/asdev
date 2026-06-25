# Goal-Driven Workflow

This workflow is the core of the skill.

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

### 1. Understand The User Goal

The main agent restates the goal in operational terms before launching specialist agents:

- What behavior should change?
- Which boundary must observe the behavior? Controller, API, UI, CLI, job, event listener, etc.
- What must remain compatible?
- What evidence will prove success?

### 2. Investigate Current Code

Launch an independent Investigator Agent to gather code facts. The main agent may do additional reading, but the investigation record must include the independent agent's findings.
Save the investigation output according to `references/recording-protocol.md`.

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

Review dimensions:

- Fact completeness: based on real code investigation, not imagination.
- Impact scope: covers direct and indirect call paths.
- Feasibility: implementable in the existing architecture.
- Consistency: respects project rules and existing patterns.
- Verifiability: can become objective task acceptance criteria.

If the review fails, return to investigation, user alignment, or design revision as needed.

## Phase 2 - Task Decomposition

Use the accepted Phase 1 design as input.

Launch a Development Manager Agent to create the task decomposition.
Save the task document according to `references/recording-protocol.md`.

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

Review dimensions:

- Task granularity.
- Dependency order.
- Objective acceptance criteria.
- Missing risk-reduction tasks.
- Whether tests/verification are realistic.

If the review fails, revise the task plan and review again.

After Phase 2, pause and ask whether to proceed with development unless the user already asked for full execution.

## Phase 3 - Task-By-Task Implementation And Acceptance

For each task in order:

1. Read the task and relevant project rules.
2. Investigate the exact files before editing.
3. Implement the smallest coherent change, using an Implementation Agent when the platform supports agent file edits in the active workspace.
4. Run focused verification.
5. Run broader verification when risk or acceptance criteria require it.
6. Submit to an independent Task Acceptance Agent.
7. Save the acceptance output according to `references/recording-protocol.md`.
8. If accepted, update task status and acceptance report.
9. If rejected, fix according to review findings and re-run acceptance.

Acceptance reports should record:

- Files changed.
- Verification commands and summarized results.
- Which acceptance criteria passed.
- Any criteria not verified and why.
- Residual risks.

Do not mark a task complete until the acceptance criteria are actually satisfied or the user explicitly changes the criteria.

## Completion

When all tasks are complete:

- Summarize what changed.
- Summarize verification.
- Point to the product/task records.
- Mention residual risks or skipped tests.

Keep the final response concise; the detailed evidence belongs in the record files.
