# Recording Protocol

## Table of Contents

- [Iron Rule Enforcement](#iron-rule-enforcement)
- [Naming](#naming)
- [Main Agent Responsibilities](#main-agent-responsibilities)
- [Required Record Links](#required-record-links)
- [Status Values](#status-values)
- [Evidence Standards](#evidence-standards)
- [User Alignment Records](#user-alignment-records)
- [Cross-Goal Memory](#cross-goal-memory)

## Iron Rule Enforcement

asdev is record-first. Agent outputs MUST be written into project-local records so later agents can consume evidence instead of relying on chat history.

**Iron rule 1 — 强制记录阻断**：No phase may advance until all prior agent outputs are saved to `.record/`. If saving fails, stop and report the error. There is no override.

**Iron rule 3 — 验收不过必须返工**：When any review/acceptance agent returns FAIL, the deliverable MUST be revised according to Required Changes/Required Fixes and re-submitted. This loop is mandatory and continues until PASS. There is no skip or downgrade.

Use the project's existing `.record/` convention when present. Otherwise use:

```text
.record/
├── .goal/
├── .prod/
├── .task/
└── .review/
```

## Naming

Use stable, sortable names:

- Goal config: `.record/.goal/GOAL_CONFIG.md`
- Investigation: `.record/.prod/INVESTIGATION_YYYYMMDD_HHMM.md`
- Requirement/design: `.record/.prod/PROD_YYYYMMDD_HHMM.md`
- Design review: `.record/.review/DESIGN_REVIEW_YYYYMMDD_HHMM.md`
- Task plan: `.record/.task/TASK_YYYYMMDD_HHMM.md`
- Task check: `.record/.review/TASK_CHECK_YYYYMMDD_HHMM.md`
- Task acceptance: `.record/.review/TASK_TXX_ACCEPTANCE_YYYYMMDD_HHMM.md`
- Verification report: `.record/.review/VERIFICATION_TXX_YYYYMMDD_HHMM.md`
- Goal check: `.record/.review/GOAL_CHECK_RXX_YYYYMMDD_HHMM.md` (RXX = iteration round)
- Comprehension report: `.record/.prod/COMPREHENSION_YYYYMMDD_HHMM.md`

If the project already uses names such as `TASK_01.md`, follow that style.

## Main Agent Responsibilities

The main agent must:

1. Create record directories/templates during Phase 0 when missing.
2. Save each specialist agent's final output to the appropriate record file.
3. Add cross-links between records.
4. Update task status only after Task Acceptance Agent returns PASS.
5. Preserve failed reviews and rejected attempts; they are part of the audit trail and prove the revision loop was followed.

## Required Record Links

Each product/design document should link:

- Investigation record.
- User alignment decisions.
- Design review record.
- Task plan after Phase 2 completes.

Each task plan should link:

- Product/design document.
- Task check review.
- Per-task acceptance reports as tasks complete.

Each task acceptance report should link:

- Task document.
- Changed files or diff summary.
- Verification commands.

## Status Values

Use these status values unless the project template says otherwise:

- `草稿`
- `待验收`
- `已验收`
- `未完成`
- `进行中`
- `完成`
- `阻塞`

Do not mark a record as `已验收` or `完成` without evidence from an independent acceptance agent that returned PASS.

## Evidence Standards

Good evidence includes:

- File paths and symbol names.
- Search queries and summarized results.
- Test/build commands and summarized results.
- API route and response shape checks.
- Import/dependency checks.
- Reviewer findings with PASS/FAIL.

Avoid unsupported claims like "should work" or "looks fine".

## User Alignment Records

When the workflow pauses to ask the user a question:

1. Record the question.
2. Record the user's answer.
3. Record how the answer affects design or task criteria.

If the user asks to proceed without answering, record the assumption explicitly.

## Cross-Goal Memory

Records are not just audit trails — they are the memory that lets future goals start from what is already known instead of from zero.

When a new goal begins:

1. The main agent scans existing `.record/` directories for prior investigation, design, task, and review documents.
2. It builds a concise historical context summary (5-10 bullets) covering: what was done, what passed, what failed, what was deferred, what patterns were established.
3. This summary is passed to the Investigator Agent as `{HISTORICAL_CONTEXT}`.
4. The Investigator Agent uses it to avoid re-deriving known facts, but still verifies current code state for the new goal.

The historical context summary should be stored in the new goal's investigation record as a "Historical Context" section, so the chain of knowledge transfer is visible in the records.
