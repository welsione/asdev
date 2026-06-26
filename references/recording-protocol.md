# Recording Protocol

## Table of Contents

- [Iron Rule Enforcement](#iron-rule-enforcement)
- [Naming](#naming)
- [STATUS.md Aggregated State](#statusmd-aggregated-state)
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

Use the project's existing `.record/` convention when present. Otherwise use the goal-scoped directory structure:

```text
.record/
├── STATUS.md
├── {goal-slug}/                 ← one subdirectory per goal
│   ├── .goal/
│   ├── .prod/
│   ├── .task/
│   └── .review/
└── .knowledge/                  ← shared across goals
```

**Goal Slug**: Every goal gets a short directory name (slug) generated at Phase 1. See Goal Slug Generation below.

**Iron rule 1 enforcement**: Record directories for the current goal MUST exist before Phase 1 begins. If they cannot be created, stop and report.

## Goal Slug Generation

Each goal generates a slug at Phase 1 to create an isolated subdirectory under `.record/`. Rules:

1. Extract 2-3 core keywords from the goal summary.
2. Join with hyphens, all lowercase, ASCII only (transliterate or drop non-ASCII).
3. Total length ≤ 24 characters.
4. If the slug collides with an existing `.record/{slug}/`, append a numeric suffix (e.g. `loop-eng-2`).

Examples:

- "Loop Engineering Skill Optimization" → `loop-eng`
- "Fix payment timeout propagation" → `payment-timeout`
- "Refactor auth middleware" → `auth-refactor`

The slug is written into STATUS.md's "活跃目标" table and the Goal Config.

## Naming

Use stable, sortable names within each goal's subdirectory. Replace `{slug}` with the current goal's slug:

- Goal config: `.record/{slug}/.goal/GOAL_CONFIG.md`
- Investigation: `.record/{slug}/.prod/INVESTIGATION_YYYYMMDD_HHMM.md`
- Requirement/design: `.record/{slug}/.prod/PROD_YYYYMMDD_HHMM.md`
- Design review: `.record/{slug}/.review/DESIGN_REVIEW_YYYYMMDD_HHMM.md`
- Task plan: `.record/{slug}/.task/TASK_YYYYMMDD_HHMM.md`
- Task check: `.record/{slug}/.review/TASK_CHECK_YYYYMMDD_HHMM.md`
- Task acceptance: `.record/{slug}/.review/TASK_TXX_ACCEPTANCE_YYYYMMDD_HHMM.md`
- Verification report: `.record/{slug}/.review/VERIFICATION_TXX_YYYYMMDD_HHMM.md`
- Goal check: `.record/{slug}/.review/GOAL_CHECK_RXX_YYYYMMDD_HHMM.md` (RXX = iteration round)
- Comprehension report: `.record/{slug}/.prod/COMPREHENSION_YYYYMMDD_HHMM.md`
- Knowledge item: `.record/.knowledge/KNOW_YYYYMMDD_HHMM_[short_topic].md` (shared, no slug prefix)

If the project already uses names such as `TASK_01.md`, follow that style.

## STATUS.md Aggregated State

STATUS.md is the aggregated state view of `.record/`, written to `.record/STATUS.md`. The main agent MUST maintain it at the following five event points (not on every file write):

1. **Phase 0 完成后**：写入初始状态。
2. **每个阶段转换时**：更新当前阶段（Phase 0 → 1 → 2 → 3 → Completion → Goal Check）。
3. **每个任务状态变更时**：更新任务进度表（任务 ID、状态、验收结果、验收报告路径）。
4. **Goal Check 后**：更新迭代轮次和结果。
5. **目标完成时**：从活跃目标移入历史目标摘要（最多 10 条，更早的通过日期索引指向具体文件）。

**STATUS.md 与铁律1的边界**：STATUS.md 不是 Agent 产出，因此不绑定铁律1的"每次产出落盘"。铁律1保证记录文件存在且完整，STATUS.md 在上述 5 个事件点读取记录文件后聚合更新。

**不一致解决规则**：STATUS.md 与记录文件不一致时，以记录文件为准，STATUS.md 应在下一事件点修正。不一致检测依赖主 Agent 在更新时读取记录文件后重新计算——这是主 Agent 的职责，不依赖自动校验。

**STATUS.md 模板**：参见 `references/templates.md` 中的 STATUS Template。

## Knowledge Items (.record/.knowledge/)

`.record/.knowledge/` holds **distilled experience** — non-obvious patterns, gotchas, project conventions, and architectural decisions that future goals should know about. Unlike `.record/.prod/` and `.record/.review/` which record facts, `.knowledge/` records **intent** ("what to do" / "what not to do") extracted from execution experience.

### Naming

Knowledge item: `.record/.knowledge/KNOW_YYYYMMDD_HHMM_[short_topic].md`

### Format (frontmatter + body)

```markdown
---
name: KNOW_YYYYMMDD_HHMM_[short_topic]
source_goal: [goal summary or .record/.goal/ path]
source_task: [T01/T02/... or N/A]
date: YYYY-MM-DD
confidence: confirmed | inferred | assumed
scope: [description of where this knowledge applies]
status: active | outdated
outdated_reason: [reason if outdated]
outdated_date: [date if outdated]
---

## Content

[One paragraph: what to do, what not to do, and why]

## Evidence

- [code fact or acceptance report path that supports this knowledge]

## Counter-examples (if any)

- [scenarios where this knowledge does NOT apply]
```

### Confidence Levels

- **confirmed**: backed by code facts AND an acceptance report (strongest).
- **inferred**: derived from multiple execution experiences, not yet independently verified.
- **assumed**: based on limited experience, needs future verification.

Confidence can be **upgraded** when new evidence references the item (e.g. an inferred becomes confirmed when a second goal's acceptance report confirms the same pattern).

### Outdated Marking

When a new goal's implementation modifies a file/symbol referenced in a knowledge item's `scope`, the main agent MUST mark the item as outdated:

1. Set `status: outdated`.
2. Append `outdated_reason` (which goal/task invalidated it).
3. Append `outdated_date`.

**Outdated items are still passed to the Investigator Agent** as `{PROJECT_KNOWLEDGE}`, but they are tagged with "⚠️ 已过时，请验证当前代码状态" so the agent does not treat them as authoritative.

### Extraction Triggers

The main agent generates knowledge items at three event points:

1. **Task PASS**: when an implementation surfaced a non-obvious pattern, gotcha, or constraint.
2. **Goal Check PASS**: when the overall goal experience has cross-goal reuse value.
3. **FAIL → Rework → PASS**: when the rework reason reveals a hidden constraint (failures teach the most).

Extraction is **opportunistic, not mandatory**. Not every task produces a knowledge item. Items must capture non-obvious insights, not routine work.

### Knowledge Items vs STATUS.md

- **Knowledge items** (`.record/.knowledge/`) are **long-form** records with full reasoning and evidence — consult when you need depth.
- **STATUS.md** `知识要点` region shows the **5 most recent** knowledge items as a one-line summary — consult for quick reference.

## Main Agent Responsibilities

The main agent must:

1. Create record directories for the current goal during Phase 0 when missing: `.record/{slug}/.goal/`, `.record/{slug}/.prod/`, `.record/{slug}/.task/`, `.record/{slug}/.review/`, `.record/.knowledge/`.
2. Save each specialist agent's final output to the appropriate record file under the current goal's `.record/{slug}/` subdirectory.
3. Add cross-links between records.
4. Update task status only after Task Acceptance Agent returns PASS.
5. Maintain `.record/STATUS.md` at the five event points (Phase 0 完成后、阶段转换时、任务状态变更时、Goal Check 后、目标完成时).
6. Extract knowledge items into `.record/.knowledge/` at the three trigger event points (Task PASS, Goal Check PASS, FAIL→Rework→PASS).
7. Mark knowledge items as outdated when their referenced files/symbols are modified.
8. Generate a goal slug at Phase 1 and create the goal-scoped subdirectory `.record/{slug}/`.
9. Preserve failed reviews and rejected attempts; they are part of the audit trail and prove the revision loop was followed.

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

1. The main agent **first reads `.record/STATUS.md`** to get an aggregated view of prior goals, task progress, and history.
2. The main agent **scans `.record/` for goal subdirectories** (any directory matching `.record/{slug}/` with a `.goal/` or `.prod/` inside). For each prior goal, it scans its `.prod/`, `.task/`, and `.review/` directories.
3. The main agent **scans `.record/.knowledge/`** for project experience items relevant to the current goal. It builds a `{PROJECT_KNOWLEDGE}` summary with each item's scope, confidence level, and content. Items marked `status: outdated` are included with an "⚠️ 已过时" warning. It also checks whether any item's `scope` references files/symbols the current goal will modify — if so, marks them as outdated.
4. It builds a concise historical context summary (5-10 bullets) covering: what was done, what passed, what failed, what was deferred, what patterns were established.
5. This summary is passed to the Investigator Agent as `{HISTORICAL_CONTEXT}` and the project knowledge as `{PROJECT_KNOWLEDGE}`.
6. If `.record/STATUS.md` does not exist or is empty, fall back to scanning `.record/` directories for goal subdirectories.
7. The Investigator Agent uses the historical context and project knowledge to avoid re-deriving known facts, but still verifies current code state for the new goal.

The historical context summary should be stored in the new goal's investigation record as a "Historical Context" section, so the chain of knowledge transfer is visible in the records.
