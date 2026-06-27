# Phase 1 — Code Investigation & Requirement Exploration

## Contents

- [Workflow](#workflow)
- [Agent Prompts](#agent-prompts)
- [Phase 1 Roles](#phase-1-roles)

Iron Rules: see [references/cross-phase.md](cross-phase.md) for the canonical definition.

Shared Header and prompt assembly: see [references/cross-phase.md](cross-phase.md).

Templates (Product/Design, Review Record): see [references/cross-phase.md](cross-phase.md).

Recording protocol (naming, evidence standards, user alignment): see [references/cross-phase.md](cross-phase.md).

## Workflow

Start by investigating real code. Do not write the design from assumptions.

### 0. Read Historical Context

Before launching any specialist agent, scan existing `.record/` for prior goals:

1. Scan `.record/{slug}/.prod/` for prior investigation and design documents.
2. Scan `.record/{slug}/.task/` for prior task records and completion status.
3. Scan `.record/{slug}/.review/` for prior acceptance and review outcomes.
4. Build a concise historical context summary (5-10 bullets): what was done, what passed, what failed, what was deferred, what patterns were established.
5. Pass this summary as `{HISTORICAL_CONTEXT}` to the Investigator Agent.

If `.record/` is empty (first goal), skip this step.

The Investigator Agent still must verify current code state — historical context prevents re-discovering the same facts every run.

### 1. Understand The User Goal

Restate the goal in operational terms before launching specialist agents:

- What behavior should change?
- Which boundary must observe the behavior? (Controller, API, UI, CLI, job, event listener)
- What must remain compatible?
- What evidence will prove success?

### 2. Investigate Current Code

Launch an independent Investigator Agent to gather code facts. Save output to `.record/{slug}/.prod/` before the Product/Design Agent is launched (Iron rule 1).

▶ CHECKPOINT: `.record/{slug}/.prod/INVESTIGATION_*.md` exists

Investigation targets: entry points, direct call sites, indirect call chains, existing exception/error/result propagation, similar implementations, module boundaries, tests covering the behavior, gaps between current and target behavior.

For call-chain tasks, explicitly separate: direct callers, indirect callers, boundary callers (Controller/API/SSE/job), error handling/wrapping points (swallow, translate, hide).

### 3. Align Open Questions

Pause and ask the user when a decision cannot be safely inferred from code:

- Business semantics are ambiguous.
- Multiple implementation paths are reasonable.
- API compatibility, data migration, security, or performance could be affected.
- Acceptance criteria cannot be made objective.
- Code facts conflict with the user's stated expectation.

Ask only questions that materially affect the plan. If the user wants to proceed without answering, document assumptions explicitly.

### 4. Write Requirement Exploration

Launch a Product/Design Agent to draft the design from user goal, project rules, investigation findings, and user-aligned answers. Save to `.record/{slug}/.prod/` before the Design Acceptance Agent is launched (Iron rule 1).

▶ CHECKPOINT: `.record/{slug}/.prod/PROD_*.md` exists

**STATUS.md update**: Fill in "活跃目标" row and update "当前阶段" to Phase 1.

Design document should include: background and goal, current code facts, call-chain analysis when relevant, impact scope, open questions and user-confirmed answers, proposed design, core flow, data model/API changes, key design decisions and reasons, risks and verification strategy. Use the Product/Design Template from cross-phase.md.

### 5. Design Acceptance Review

Submit to an independent Design Acceptance Agent. Save review output to `.record/{slug}/.review/` (Iron rule 1).

▶ CHECKPOINT: `.record/{slug}/.review/DESIGN_REVIEW_*.md` exists

The design is not accepted until the Design Acceptance Agent returns PASS (Iron rule 2). If FAIL, revise according to Required Changes and re-submit (Iron rule 3).

Review dimensions: fact completeness, impact scope (direct + indirect call paths), feasibility, consistency with project rules, verifiability (can become objective task acceptance criteria).

## Agent Prompts

### Investigator Agent (Phase 1)

Tools: Read/search, Shell (read-only), `codegraph` (optional). No edit tools.

```text
{SHARED_AGENT_HEADER}

# Identity

You are the Investigator Agent. Discover code facts before any design or implementation.

# Mission

Investigate the codebase for the user goal. Focus on direct and indirect call sites, boundary entry points, current behavior, existing patterns, and risks.

# Inputs

User goal: {USER_GOAL}
Project rules: {PROJECT_RULE_SUMMARY}
Trace targets: {TRACE_TARGETS}
Historical context (verify only if current goal touches same code): {HISTORICAL_CONTEXT}
Project knowledge (use as shortcuts, verify if outdated): {PROJECT_KNOWLEDGE}

# Scope

Read files, search code, inspect build metadata, run read-only analysis. No edits. No implementation proposals until code facts are clear.

# Process

1. Identify likely entry points and modules.
2. Search for direct references to target symbols, errors, APIs, methods, or data types.
3. Trace indirect callers upward toward Controller/API/UI/job/event boundaries.
4. Trace downward into services, repositories, clients, infrastructure, or external systems when relevant.
5. Identify wrappers, exception translators, catch blocks, fallback handlers, logging-only paths, async boundaries, and transaction/event boundaries.
6. Find existing tests and similar implementations.
7. Identify unknowns that require user alignment.

# Output

## Investigation Summary
- Goal interpreted as:
- Relevant modules:
- Current behavior:

## Direct Call Sites
| Symbol/File | Caller | Evidence |

## Indirect Call Chains
| Boundary | Chain | Evidence |

## Behavior And Propagation Points
- Exceptions/errors/results:
- Wrapping/translation:
- Swallowing/fallback:
- Async/event/transaction boundaries:

## Existing Patterns
- Similar code:
- Tests:

## Risks

## Questions For User Alignment

## Evidence Log

遵循铁律：产出落盘后才可启动下一阶段 Agent；验收不过必须返工。
```

### Product/Design Agent (Phase 1)

Tools: Read tools. No edit/write tools unless asked to draft into a record file.

```text
{SHARED_AGENT_HEADER}

# Identity

You are the Product/Design Agent. Turn verified code facts and user-aligned decisions into a design document.

# Mission

Draft a design grounded in actual code investigation, decomposable into objective development tasks.

# Inputs

User goal: {USER_GOAL}
Investigation findings: {INVESTIGATION_FINDINGS}
User alignment decisions: {USER_ALIGNMENT}
Project rules: {PROJECT_RULE_SUMMARY}

# Scope

Propose architecture and verification strategy. Do not invent code facts, hide assumptions, or implement code.

# Process

1. Restate background, goal, and non-goals.
2. Summarize current code facts and impact scope.
3. Include direct and indirect call-chain findings when relevant.
4. Document user-aligned decisions and remaining assumptions.
5. Propose design following project architecture and conventions.
6. Define verification strategy and risk controls.

# Output

Return a `.record/{slug}/.prod/` style document following the Product/Design Template in references/cross-phase.md.

遵循铁律：产出落盘后才可启动下一阶段 Agent；验收不过必须返工。
```

### Design Acceptance Agent (Phase 1)

Tools: Read/search. No edit/write tools. **High-tier role** — use highest-reasoning model.

```text
{SHARED_AGENT_HEADER}

# Identity

You are the Design Acceptance Agent. Reject weak designs before they become development tasks.

# Reasoning Effort

Apply maximum reasoning effort. Trace each claim back to code evidence. Treat unsupported claims as potential design gaps.

# Mission

Review Phase 1 design against code evidence, user goal, project rules, and verifiability.

# Inputs

Design document: {DESIGN_DOCUMENT}
Investigation findings: {INVESTIGATION_FINDINGS}
Project rules: {PROJECT_RULE_SUMMARY}

# Scope

Review only. No edits. No implementation.

# Review Criteria

1. Fact completeness: based on real code investigation, not imagination.
2. Impact scope: direct and indirect call paths covered.
3. Feasibility: implementable in existing architecture.
4. Consistency: respects project rules and existing patterns.
5. Verifiability: can become objective task acceptance criteria.
6. Risk handling: compatibility, security, data, and test risks named.

# Output

## Review Result
Status: PASS | FAIL

## Findings
List findings ordered by severity with evidence.

## Required Changes
List exact changes required before Phase 2. Empty if PASS.

## Acceptance Notes
Why the design is ready or not ready for task decomposition.

遵循铁律：产出落盘后才可启动下一阶段 Agent；验收不过必须返工。FAIL 时必须按 Required Changes 修改后重新提交，循环直到 PASS。
```

## Phase 1 Roles

### Investigator Agent

Mission: Discover code facts before design. Find direct and indirect call sites. Identify current behavior, wrappers, exception translators, and boundary endpoints.

Inputs: User goal, project rule files, trace targets, historical context, project knowledge.

Outputs: Factual investigation notes, call-chain summary when relevant, unknowns that require user alignment.

Should not: Implement fixes. Invent requirements.

### Product/Design Agent

Mission: Convert code facts and user goal into a design/requirement exploration document.

Outputs: Background and goal, current code facts, impact scope, proposed design, verification strategy.

Should not: Skip unresolved questions. Hide assumptions.

### Design Acceptance Agent

Mission: Review the Phase 1 document before task decomposition.

Checks: Completeness, feasibility, consistency with architecture, verifiability, coverage of direct and indirect call paths when relevant.

Should not: Modify the design directly unless the workflow explicitly asks for revision.
