# Goal Mode & Loop Mode

## Contents

- [Goal Mode](#goal-mode)
- [Loop Mode](#loop-mode)
- [Running Modes Comparison](#running-modes-comparison)
- [Goal Check Agent Prompt](#goal-check-agent-prompt)

Iron Rules: see [references/cross-phase.md](cross-phase.md) for the canonical definition.

Shared Header and prompt assembly: see [references/cross-phase.md](cross-phase.md).

## Goal Mode

Goal mode activates when the user provides a verifiable stop condition or explicitly requests `/goal` or goal mode. It wraps the phased workflow in an outer loop that iterates until the stop condition is proven true.

### Activation

Goal mode activates when:
- The user explicitly says `/goal`, "goal mode", or provides a verifiable stop condition.
- The user's goal statement already contains a concrete, testable completion criterion.

Goal mode does NOT activate when:
- The user only asks for a design or task plan without implementation.
- The user explicitly says "just the plan" or "stop after Phase 2".

### Phase 1 Addition: Define Stop Condition

When goal mode is active, add this step after "Write Requirement Exploration":

1. Extract or refine the **verifiable stop condition** from the user's goal.
2. The stop condition must be objectively testable: a command that exits 0, a test suite that passes, an API response that matches a shape, a grep that finds/does not find a pattern.
3. Write the stop condition into the design document under "## Stop Condition".
4. The stop condition does not change between iterations. If the user wants to change it, that is a new goal.

### After Completion: Goal Check

When all tasks are complete and the standard Completion step is done:

1. Launch an independent **Goal Check Agent** to evaluate the stop condition.
2. The Goal Check Agent MUST be different from the Implementation Agent. The maker does not grade its own homework.
3. The Goal Check Agent reads the stop condition, inspects the code, runs verification commands, and returns PASS or FAIL with evidence.

Save the Goal Check result to `.record/{slug}/.review/` before any next action (Iron rule 1).

▶ CHECKPOINT: `.record/{slug}/.review/GOAL_CHECK_*.md` exists

The goal is not achieved until the Goal Check Agent returns PASS (Iron rule 2).

**STATUS.md update**: After Goal Check, update iteration round and result, add entry to "Recent Changes" if the iteration introduced changes.

If the Goal Check Agent returns FAIL (Iron rule 3):

1. Record the failure and gap analysis in `.record/{slug}/.review/`.
2. Return to Phase 1 to investigate the gap — not from scratch, only the unsatisfied part.
3. Update the design, add or revise tasks as needed.
4. Re-run Phase 3 for the new/updated tasks.
5. Re-run the Goal Check Agent.
6. This loop continues until PASS.

### Convergence Safeguard

If the goal loop runs 3 full iterations (Phase 1 → 3 → Goal Check) without PASS:

1. Pause the loop.
2. Report to the user: what has been tried, what remains unsatisfied, whether the stop condition may be unrealistic.
3. The user must decide: adjust the goal, continue, or stop.
4. Record the decision in `.record/{slug}/.goal/`.

**Loop mode convergence adjustment**: In loop mode, stricter — pause after 2 full iterations without PASS, or if cumulative changed files exceed 30. Downgrade to interactive mode when triggered.

## Loop Mode

Loop mode activates when the user's goal description contains "循环模式 (loop mode)", "无人值守 (unattended)", or "自动迭代 (auto-iteration)" keywords, or when the host platform's scheduling mechanism calls `/asdev` on a schedule.

### Behavior Differences

- **Phase 2 pause**: Skipped — loop mode proceeds automatically after task decomposition.
- **Layer 3 (Pre-Implementation Confirmation)**: Skipped. Layer 4 (Change Density Warning) still applies.
- **Layer 2 (Understanding Verification)**: Skipped in interactive form. Change summaries written to `.record/STATUS.md` "Recent Changes" region instead.
- **Convergence safeguard**: Stricter — pause after 2 full iterations without PASS, or if cumulative changed files exceed 30. Downgrade to interactive mode when triggered.

### Breakpoint Recovery

When loop mode starts or restarts:

1. Read `.record/STATUS.md`.
2. If an active goal exists with status "In Progress", continue from the current phase.
3. If no active goal exists, start from Phase 0.
4. If STATUS.md has pending alignment questions from a previous interactive pause, handle them before proceeding.

### Mode Switching

A convergence safeguard trigger downgrades loop mode to interactive mode (waiting for user decision). After the user decides, they may continue in loop mode or stay in interactive mode. The user may switch to loop mode at any time by including a trigger keyword in their next message.

### Host Platform Scheduling Integration

- **Claude Code `/loop` skill**: `"/loop 10m /asdev [goal with 循环模式 (loop mode) keyword]"` — automatic re-triggering.
- **Claude Code hooks/cron**: Configure in `.claude/settings.json`.
- **Codex Automations tab**: Pick project, prompt, cadence, environment.
- **Manual re-trigger**: User manually re-triggers `/asdev [goal]` after each iteration. STATUS.md ensures breakpoint recovery.

Loop mode does not depend on any specific scheduling mechanism — STATUS.md breakpoint recovery is the core, and scheduling is a convenience layer.

### STATUS.md Auto-Sync (Loop Mode Critical)

Loop mode's breakpoint recovery depends entirely on STATUS.md accuracy. To guarantee STATUS.md is always current:

1. **PostToolUse hook (preferred)**: `.claude/settings.local.json` automatically calls `python3 scripts/sync-status.py --quiet` after every Write/Edit. This is the recommended setup — no manual intervention required.

2. **Scheduled sync (fallback)**: If hooks are unavailable, integrate sync into the scheduling command:
   - Claude Code `/loop`: `"/loop 10m python3 scripts/sync-status.py && /asdev [goal]"`
   - Manual cadence: Run `python3 scripts/sync-status.py` before each `/asdev` re-trigger.

3. **Stop hook verification**: `.claude/settings.local.json` Stop hook runs `python3 scripts/sync-status.py --check` at session end. A mismatch triggers a warning — the next iteration can detect and correct stale STATUS.md before breakpoint recovery reads it.

When all three layers are active, STATUS.md is guaranteed current at every loop iteration boundary — making breakpoint recovery reliable.

## Running Modes Comparison

| Dimension | Interactive Mode (default) | Loop Mode |
|-----------|---------------------------|-----------|
| Trigger | `/asdev` or `/goal` | "循环模式 (loop mode)", "无人值守 (unattended)", "自动迭代 (auto-iteration)" keywords; or host platform scheduled dispatch |
| Iteration start | Manual confirmation | Automatic (STATUS.md breakpoint recovery) |
| User interaction | May pause at each phase | Pauses only when convergence safeguard triggers |
| Pre-implementation confirmation (Layer 3) | Enabled | Skipped (unless change density warning triggers) |
| Cognitive surrender check (Layer 2) | Understanding verification questions | Change summaries written to STATUS.md |
| Stop condition | Goal Check PASS or user terminates | Goal Check PASS or convergence safeguard or user says "stop loop" or `/stop` |
| STATUS.md | Updated but optional | **Required** (breakpoint recovery) |
| Model configuration | Recommended | **Strongly recommended** |
| .knowledge/ | Recommended | Recommended |
| Worktree isolation | Branch isolation (optional) | **Worktree isolation** (recommended) |

## Goal Check Agent Prompt

Tools: Read/search, Shell for tests and verification commands. No edit/write tools. **High-tier role** — use highest-reasoning model.

```text
{SHARED_AGENT_HEADER}

# Identity

You are the Goal Check Agent. Evaluate whether the verifiable stop condition is truly met after all implementation is done. You are the independent checker — the agent that wrote the code does not grade its own homework.

# Reasoning Effort

Apply maximum reasoning effort — this is the final acceptance gate. For each part of the stop condition, look for the strongest possible evidence and reject any claim that relies on narrative judgment. If any part is satisfied by "looks like" or "should work" instead of "verified by", return FAIL.

# Mission

Evaluate the stop condition against actual code, test, and command evidence. Return PASS only when every part is objectively satisfied.

# Inputs

Verifiable stop condition: {STOP_CONDITION}
Design document: {DESIGN_DOCUMENT}
Task records and acceptance reports: {TASK_RECORDS}
Changed files: {CHANGED_FILES_OR_DIFF}
Project rules: {PROJECT_RULE_SUMMARY}

# Scope

Evaluate only the stop condition. Do not edit files. Do not implement fixes. Do not re-review the design or task plan.

# Process

1. Read the stop condition carefully. Break it into individual testable parts.
2. For each part, find or run the most direct verification: a test command, a grep, an API check, a file inspection.
3. Record concrete evidence for each part — not narrative claims.
4. If any part cannot be verified, that part is FAIL.
5. Summarize gaps if any part is unsatisfied.

# Output

## Goal Check Result
Status: PASS | FAIL

## Stop Condition Evaluation
| Condition | Evidence | Result |

## Gap Analysis
- Unsatisfied conditions and why:

## Recommended Next Steps
If FAIL, describe exactly what is still needed to satisfy the stop condition.

Follow iron rules: do not launch the next agent until the output is saved to .record/; rework is mandatory on FAIL. On FAIL, the main agent must return to Phase 1 to investigate the gap and loop until PASS.
```
