# asdev Agent Prompt Index

Use this file to choose the role-specific prompt for the current phase.

Before launching any agent:

1. Read `references/prompt-assembly.md`.
2. Read only the role prompt files needed for the current phase.
3. Fill the required placeholders.
4. Launch the agent through the platform's independent agent mechanism.
5. Save the agent output using `references/recording-protocol.md`.

## Prompt Files

Phase 1:

- `references/prompts/investigator.md`
- `references/prompts/product-designer.md`
- `references/prompts/design-acceptance.md`

Phase 2:

- `references/prompts/development-manager.md`
- `references/prompts/task-check.md`

Phase 3:

- `references/prompts/implementation.md`
- `references/prompts/task-acceptance.md`
- `references/prompts/verification.md`

## Role Summary

- Investigator Agent: discovers code facts and call chains.
- Product/Design Agent: writes requirement exploration and design notes.
- Design Acceptance Agent: reviews design readiness.
- Development Manager Agent: decomposes accepted design into ordered tasks.
- Task Check Agent: reviews task plan quality.
- Implementation Agent: implements one approved task.
- Task Acceptance Agent: verifies one implemented task.
- Verification Agent: performs deeper boundary, API, security, architecture, or regression checks.

## Claude Code Subagent Skeleton

When creating Claude Code project subagents, adapt this skeleton. Use project-level `.claude/agents/` for team-shared agents.

```markdown
---
name: asdev-investigator
description: Use proactively during asdev Phase 1 to investigate real code facts, direct and indirect call sites, boundary entry points, and current behavior before design.
tools: Read, Glob, Grep, Bash
model: inherit
---

[Paste the Investigator Agent prompt body here.]
```

For review agents, prefer read-only tools. For implementation agents, allow edit tools only when the platform/workspace isolation is appropriate.
