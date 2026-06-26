# Codex And Claude Code Compatibility

This skill should work in both Codex and Claude Code.

The workflow is platform-neutral. Tool usage adapts to the host.

## Shared Rules

- Read project-local rules before planning.
- Use `rg` for search when available.
- Use optional tools only after detecting them.
- Confirm independent multi-agent capability before Phase 1.
- Follow `references/multi-agent-contract.md` for the exact capability check and failure behavior.
- Do not install dependencies without explicit user approval.
- Keep generated records inside the project workspace.
- Preserve user changes in the worktree.

## Iron Rules (Cross-Platform)

These rules apply on every platform with no exception:

1. **强制记录**：Every agent output MUST be saved to `.record/{slug}/` (where `{slug}` is the current goal's slug) before the next phase starts. No phase advances without records on disk.
2. **强制验收**：Every phase deliverable MUST pass independent acceptance review (PASS). No PASS = phase not complete.
3. **验收不过必须返工**：FAIL triggers mandatory revision and re-submission. The loop continues until PASS. No skip, no override.

## Codex

In Codex:

- Use the available shell/search/edit tools according to system instructions.
- Use planning tools when the work is multi-step.
- Use the available multi-agent/subagent tools for required asdev roles. If multi-agent tools are not currently visible but tool discovery is available, search for them before declaring the environment unsupported.
- If the user asks for a browser/UI check, use the relevant browser skill/tool if available.
- If a skill applies, read its `SKILL.md` before relying on it.

Codex may have a stricter filesystem sandbox. If project records need to be created outside the writable root, ask for permission or ask the user to run the skill from the project root.

If no multi-agent/subagent capability is exposed in the Codex session after following `references/multi-agent-contract.md`, stop and tell the user that asdev requires multi-agent support.

## Claude Code

In Claude Code:

- Use the Agent tool (子代理) for independent roles.
- If the Agent tool (子代理) is unavailable, stop and tell the user that asdev requires Claude Code Agent tool (子代理)/multi-agent support.
- Use TodoWrite if available to track phases and task progress.
- Use Read/Grep/Glob/Bash/Edit tools according to Claude Code conventions.
- Use `references/agent-prompts.md` as the prompt source when creating Agent tool (子代理) prompts or project-level `.claude/agents/` files.

Recommended Agent tool (子代理) prompts:

```text
You are the Design Acceptance Agent. Review the attached Phase 1 design document against completeness, feasibility, architecture consistency, and verifiability. Do not implement changes. Return PASS or FAIL with findings and required changes.
```

```text
You are the Task Acceptance Agent. Verify task Txx against its acceptance criteria and the code/test evidence. Do not implement changes. Return PASS or FAIL with criteria-level evidence and required fixes.
```

## Optional codegraph

Use `codegraph` when already available and useful for:

- Call-chain discovery.
- Dependency graph exploration.
- Finding entry points.
- Understanding architecture relationships.

If unavailable, continue with:

- `rg`
- static code reading
- compiler/test output
- framework conventions
- project docs

## Optional superpowers

Use `superpowers` only when it is available and relevant.

Good uses:

- Planning discipline.
- Reflection before risky edits.
- Review checklists.
- Debugging process.

Do not make this skill depend on `superpowers`. This skill remains the outer orchestration layer.

## No Independent Agents Available

asdev cannot run without independent agents.

If independent agents are unavailable, do not continue with a self-review substitute. Follow the stop message shape in `references/multi-agent-contract.md`.

## Worktree Capability

asdev can use git worktrees to isolate concurrent or iterative work. Detection:

- **Claude Code**: The Agent tool's `isolation: "worktree"` parameter creates a subagent in its own worktree that auto-cleans if unchanged. `git worktree` is also available directly.
- **Codex**: Check whether the platform exposes worktree support or built-in per-thread worktree isolation. If not, fall back to branch isolation (see `references/multi-agent-contract.md`).

If worktree capability is unavailable, branch isolation is the fallback. Both achieve the same goal (main checkout stays clean during rework/iteration), but worktree is preferred for Goal Mode iterations because it provides a fully separate working directory.

## Loop Mode Scheduling

Loop mode requires a scheduling mechanism to automatically re-trigger asdev on a cadence. Available options:

- **Claude Code `/loop` skill**: If the `/loop` skill is in the available skills list, loop mode can use `"/loop 10m /asdev [goal]"` for automatic re-triggering.
- **Claude Code hooks/cron**: If `.claude/settings.json` contains hook or cron configurations, they can be used for scheduled dispatch.
- **Codex Automations tab**: If the Codex environment exposes an Automations tab, use it for scheduled runs.
- **Manual re-trigger**: If no scheduling is available, loop mode still works — the user manually re-triggers `/asdev [goal]` after each iteration, with STATUS.md ensuring breakpoint recovery.

**Detection**: In Phase 0, check for the `/loop` skill in available skills and for hooks/cron configuration in `.claude/settings.json`. Record findings in the Phase 0 capability notes. If neither is available, note that loop mode will use manual re-trigger as fallback.

## Model Selection Capability

Some platforms allow per-agent model selection (e.g. Claude Code's Agent tool `model` parameter). When available, the role-model mapping in `references/agent-roles.md` is used to give review/acceptance roles a higher-reasoning model than implementation roles. This is **recommended but optional** — when unsupported, fall back to prompt-level reasoning-effort instructions.

### Detection (Phase 0)

In Phase 0 Bootstrap, the main agent detects model-selection capability by:

1. Attempting to launch a read-only test agent (e.g. one that runs `echo "test"`) with a specified model identifier such as `"opus"`.
2. If the launch succeeds and returns a result, the platform supports model selection — record the available model identifiers in the Phase 0 capability notes.
3. If the launch fails or returns an error indicating the model identifier is unknown, the platform does not (currently) support model selection — record the failure and use the prompt-level fallback.

### Claude Code Known Model Identifiers

The Claude Code Agent tool's `model` parameter accepts the following values (subject to the user's subscription tier and platform availability):

- `"opus"` — highest reasoning effort, slower, higher token cost.
- `"sonnet"` — standard reasoning, default for most roles.
- `"haiku"` — fastest, lowest token cost, for simple tasks.

Use `"opus"` for the four high-tier review/acceptance roles (Design Acceptance, Task Check, Task Acceptance, Goal Check). Use the default (or `"sonnet"`) for the four standard-tier roles (Investigator, Product/Design, Development Manager, Implementation).

**Note**: Model availability depends on the user's subscription tier. If `"opus"` is unavailable to the current user, fall back to the highest available tier or use the prompt-level fallback.

### Codex Fallback

If Codex does not expose per-agent model selection:

1. For each high-tier review/acceptance role, add a prompt-level reasoning-effort instruction: "请以最高推理努力执行审查" or its English equivalent.
2. Record the degradation fact and the residual risk (reviewer and implementer may still share some cognitive bias) in `.record/{slug}/`.
3. The workflow is not blocked — degraded review is still better than self-review.

### Degradation Record Template

When model selection is unavailable, record the following in `.record/{slug}/`:

```markdown
## Model Selection Degradation Note

> Phase 0 capability detection on YYYY-MM-DD
> Platform: [Claude Code / Codex]
> Detection result: [failure reason]
> Affected roles: [list of high-tier roles]
> Fallback: prompt-level reasoning-effort instruction
> Residual risk: reviewer/implementer may share cognitive bias from same model
```
