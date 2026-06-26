# Multi-Agent Capability Contract

asdev requires real independent agents. Do this check before Phase 1.

The main agent is the orchestrator and record keeper. Specialist agents must run in separate agent contexts provided by the host platform.

## Table of Contents

- [Minimum Required Capability](#minimum-required-capability)
- [Codex Detection](#codex-detection)
- [Claude Code Detection](#claude-code-detection)
- [Agent Independence Rules](#agent-independence-rules)
- [Failure Handling](#failure-handling)
- [Iron Rule Enforcement](#iron-rule-enforcement)
- [Optional Capabilities](#optional-capabilities)

## Minimum Required Capability

The environment must support launching independent agents for at least these roles:

Core roles (7 agents, required for all modes):

- Investigator Agent
- Product/Design Agent
- Design Acceptance Agent
- Development Manager Agent
- Task Check Agent
- Implementation Agent (may be replaced by main agent if platform cannot safely let agents edit the shared workspace)
- Task Acceptance Agent

Goal mode role (8th agent, required when /goal or goal mode is active):

- Goal Check Agent: evaluates whether the verifiable stop condition is met after all tasks are complete.

If the platform cannot spawn the Goal Check Agent, goal mode is unavailable but the standard phased workflow (Phase 0–3) may still run.

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

1. Use the Agent tool (子代理) for each specialist role.
2. If project-level subagents are available in `.claude/agents/`, prefer those when they match asdev roles.
3. If the Agent tool (子代理) is unavailable, stop.

Stop message shape:

```text
asdev cannot continue because Claude Code Agent tool (子代理)/multi-agent support is unavailable. Enable the Agent tool (子代理) or run in a Claude Code environment that supports subagents.
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

1. Record the failure in `.record/{slug}/.review/`.
2. Retry once with a smaller, clearer prompt if the failure is due to context size or ambiguity.
3. If the retry fails, stop and ask the user whether to adjust scope, provide missing context, or change platform.

## Iron Rule Enforcement

When a review/acceptance agent returns FAIL:

1. The deliverable MUST be revised according to Required Changes/Required Fixes.
2. The revised deliverable MUST be re-submitted to the same acceptance agent role.
3. This loop continues until PASS. There is no skip, downgrade, or override.
4. Every FAIL and revision MUST be recorded in `.record/{slug}/` to prove the revision loop was followed.

## Optional Capabilities

These improve results but are not required:

- `codegraph`
- `superpowers`
- framework-specific skills
- browser/UI automation tools

Missing optional capabilities must not block asdev unless the user explicitly made them mandatory.

### Recommended: Per-Agent Model Differentiation

When the platform supports per-agent model selection (e.g. Claude Code Agent tool's `model` parameter), **recommend** that the main agent use the role-model mapping in `references/agent-roles.md`:

- **High-tier** (opus or platform's highest reasoning): Design Acceptance, Task Check, Task Acceptance, Goal Check.
- **Standard-tier** (default, e.g. sonnet): Investigator, Product/Design, Development Manager, Implementation.

This is a recommendation, not a requirement. When the platform does not support per-agent model selection, fall back to prompt-level reasoning-effort instructions and record the degradation in `.record/`. See `references/compatibility.md` for the detection method and degradation template.

The rationale: asdev's "maker does not grade own homework" principle is enforced at the agent role level (separate Implementation Agent vs Task Acceptance Agent). Using a different model for the reviewer further reduces the risk of shared cognitive bias.

### Recommended: Worktree Isolation Strategy

When multiple agents modify files in the same repository, file collisions become the failure mode. Worktree isolation ensures one agent's edits cannot touch another agent's checkout.

**Isolation levels by scenario:**

| Scenario | Isolation Level | Operation |
|----------|----------------|-----------|
| Single task, sequential implementation | None needed | Work in main checkout |
| Task rework (FAIL → redo) | **Branch isolation** | `git checkout -b asdev/T03_$(date +%Y%m%d%H%M)` before implementing; PASS → merge; user terminates → delete branch |
| Goal Mode iteration | **Worktree isolation** | New iteration in separate worktree; PASS → merge back |
| Parallel task implementation (future) | **Worktree isolation** | Each parallel task in its own worktree |

**Branch isolation operation (task-level):**

1. Before implementing: `git checkout -b asdev/TXX_YYYYMMDDHHMM` (includes timestamp to avoid conflict with user's existing branches).
2. If branch already exists: append incrementing suffix (e.g. `_v2`).
3. Implement and verify on the branch.
4. Task Acceptance Agent verifies on the branch.
5. PASS → `git checkout main && git merge asdev/TXX_YYYYMMDDHHMM`.
6. FAIL → continue fixing on the branch (main remains clean).
7. User terminates task → `git checkout main && git branch -D asdev/TXX_YYYYMMDDHHMM`, discarding changes.

**Worktree isolation operation (iteration-level, Claude Code):**

1. Goal Mode new iteration: `git worktree add ../asdev-iter-R2 R2-branch`
2. Implement and verify in the worktree.
3. Goal Check PASS → merge back to main worktree.
4. Goal Check FAIL → continue in worktree or discard.

**Platform differences:**

- **Claude Code**: supports `git worktree` and Agent tool's `isolation: "worktree"` parameter.
- **Codex**: if worktree concept is supported, use it; if not, fall back to branch isolation.

**Worktree cleanup**: After PASS and merge, the worktree MUST be cleaned up (`git worktree remove`) to avoid accumulation. If the task is terminated, preserve the worktree for user inspection.
