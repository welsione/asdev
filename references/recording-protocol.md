# Recording Protocol

asdev is record-first. Agent outputs must be written into project-local records so later agents can consume evidence instead of relying on chat history.

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

If the project already uses names such as `TASK_01.md`, follow that style.

## Main Agent Responsibilities

The main agent must:

1. Create record directories/templates during Phase 0 when missing.
2. Save each specialist agent's final output to the appropriate record file.
3. Add cross-links between records.
4. Update task status only after Task Acceptance Agent returns PASS.
5. Preserve failed reviews and rejected attempts; they are part of the audit trail.

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

Do not mark a record as `已验收` or `完成` without evidence.

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
