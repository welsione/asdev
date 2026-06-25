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

- Use the Task tool for independent roles.
- If Task is unavailable, stop and tell the user that asdev requires Claude Code Task/multi-agent support.
- Use TodoWrite if available to track phases and task progress.
- Use Read/Grep/Glob/Bash/Edit tools according to Claude Code conventions.
- Use `references/agent-prompts.md` as the prompt source when creating Task prompts or project-level `.claude/agents/` files.

Recommended Task prompts:

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
