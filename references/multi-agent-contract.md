# Multi-Agent Capability Contract

asdev requires real independent agents. Do this check before Phase 1.

The main agent is the orchestrator and record keeper. Specialist agents must run in separate agent contexts provided by the host platform.

## Minimum Required Capability

The environment must support launching independent agents for at least these roles:

- Investigator Agent
- Product/Design Agent
- Design Acceptance Agent
- Development Manager Agent
- Task Check Agent
- Task Acceptance Agent

Implementation Agent is recommended when the platform can safely let agents edit a shared workspace or isolated worktree. If not, the main agent may implement, but independent task acceptance is still mandatory.

## Codex Detection

In Codex:

1. Check whether multi-agent tools are already exposed.
2. If tool discovery is available, search for tools with queries such as:
   - `subagent`
   - `multi-agent`
   - `spawn agent`
   - `task agent`
3. Accept the environment only if it can launch a separate agent with its own instructions and return a bounded result.

If no such capability is available, stop with this message shape:

```text
asdev cannot continue because this Codex session does not expose a multi-agent/subagent capability. Enable a multi-agent tool or run this workflow in an environment that can launch independent specialist agents.
```

## Claude Code Detection

In Claude Code:

1. Use the Task tool for each specialist role.
2. If project-level subagents are available in `.claude/agents/`, prefer those when they match asdev roles.
3. If the Task tool is unavailable, stop.

Stop message shape:

```text
asdev cannot continue because Claude Code Task/multi-agent support is unavailable. Enable the Task tool or run in a Claude Code environment that supports subagents.
```

## Agent Independence Rules

Independent agents should receive:

- The role-specific prompt.
- The user goal.
- Relevant record paths.
- Relevant project rules or summaries.
- Bounded excerpts, file paths, or investigation outputs.

Independent agents should not rely on hidden main-agent reasoning.

Review agents must be read-only unless the platform enforces a separate worktree and the user explicitly asks them to patch their own findings. Default to read-only review.

## Failure Handling

Do not replace missing independent agents with main-agent self-review.

If an individual agent fails:

1. Record the failure in `.record/.review/`.
2. Retry once with a smaller, clearer prompt if the failure is due to context size or ambiguity.
3. If the retry fails, stop and ask the user whether to adjust scope, provide missing context, or change platform.

## Optional Capabilities

These improve results but are not required:

- `codegraph`
- `superpowers`
- framework-specific skills
- browser/UI automation tools

Missing optional capabilities must not block asdev unless the user explicitly made them mandatory.
