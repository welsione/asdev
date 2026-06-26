# asdev Agent Prompt Index

All agent prompts are in a single file: `references/agent-prompts-full.md`.

Before launching any agent:

1. Read `references/prompt-assembly.md` for placeholder definitions.
2. Read the relevant section of `references/agent-prompts-full.md` for the current phase.
3. Fill the required placeholders.
4. Launch the agent through the platform's 子代理 mechanism.
5. **Iron rule 1**: Save the agent output to `.record/` before launching any next-phase agent.
6. **Iron rule 2**: Review/acceptance roles do not advance the phase until they return PASS.
7. **Iron rule 3**: FAIL triggers mandatory revision and re-submission until PASS.

## Prompt Locations in agent-prompts-full.md

| Phase | Role | Section | Recommended Model Tier |
| --- | --- | --- | --- |
| Phase 1 | Investigator Agent | "# Investigator Agent Prompt" | Standard |
| Phase 1 | Product/Design Agent | "# Product/Design Agent Prompt" | Standard |
| Phase 1 | Design Acceptance Agent | "# Design Acceptance Agent Prompt" | **High** (e.g. opus) |
| Phase 2 | Development Manager Agent | "# Development Manager Agent Prompt" | Standard |
| Phase 2 | Task Check Agent | "# Task Check Agent Prompt" | **High** (e.g. opus) |
| Phase 3 | Implementation Agent | "# Implementation Agent Prompt" | Standard |
| Phase 3 | Task Acceptance Agent | "# Task Acceptance Agent Prompt" | **High** (e.g. opus) |
| Phase 3 | Verification Agent | "# Verification Agent Prompt" | Standard |
| Goal Mode | Goal Check Agent | "# Goal Check Agent Prompt" | **High** (e.g. opus) |

**Model tier guidance**: The four **High**-tier roles (review/acceptance) should use the platform's highest-reasoning model (e.g. `model: "opus"` in Claude Code) to reduce shared cognitive bias with the implementation roles. The five **Standard**-tier roles use the platform's default model. When the platform does not support per-agent model selection, the High-tier prompts already include a prompt-level reasoning-effort instruction as a fallback. See `references/agent-roles.md` and `references/compatibility.md` for full details.
