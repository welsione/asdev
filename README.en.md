<p align="right">
  <strong>English</strong> | <a href="README.md">中文</a>
</p>

<p align="center">
  <img src="assets/logo.svg" alt="asdev logo" width="760" />
</p>

<p align="center">
  <strong>Turn complex software goals over to an agent team that investigates, decomposes, and accepts.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Mandatory_Multi_Agent-7DD3FC?style=flat-square" alt="Mandatory Multi Agent" />
  <img src="https://img.shields.io/badge/Iron_Rule_Driven-34D399?style=flat-square" alt="Iron Rule Driven" />
  <img src="https://img.shields.io/badge/Comprehension_Debt_Guard-FDE68A?style=flat-square&color=FDE68A" alt="Comprehension Debt Guard" />
  <img src="https://img.shields.io/badge/Loop_Mode-A7F3D0?style=flat-square" alt="Loop Mode" />
</p>

---

## AI coding fails not because it can't write code

But because it starts writing too soon. You've been here:

<table>
<tr>
<td width="48" align="center">🔴</td>
<td><strong>Self-review masquerading as acceptance</strong> — The agent writes code, checks it itself, and says "done." The maker grades its own homework.</td>
</tr>
<tr>
<td width="48" align="center">🔴</td>
<td><strong>One-shot big risk</strong> — Complex requirement → start coding immediately → halfway in, wrong direction → massive rollback cost.</td>
</tr>
<tr>
<td align="center">🔴</td>
<td><strong>Comprehension debt</strong> — The faster the loop ships code, the less you understand what the code has become. Eventually you either "trust" or "give up" — cognitive surrender.</td>
</tr>
<tr>
<td align="center">🔴</td>
<td><strong>Cross-goal amnesia</strong> — Every new session starts from zero, re-discovering facts you already knew last time.</td>
</tr>
<tr>
<td align="center">🔴</td>
<td><strong>Vague acceptance criteria</strong> — "Looks fine", "Should work", "Logically correct" — subjective standards that can't be objectively verified.</td>
</tr>
</table>

`asdev` restructures complex requirements into a goal-mode workflow: investigate real code first, align on uncertainties, decompose into verifiable tasks, then use independent agents for checking and acceptance. It breaks one big risk into many small, discoverable, correctable risks.

---

## Before & After: Night and Day in Delivery Quality

> Same requirement, same model. The only difference is the process.

<table>
<tr>
<th width="18%" align="center">Dimension</th>
<th width="41%" style="background:#1c1012;">❌&nbsp; Before — without asdev</th>
<th width="41%" style="background:#0a1f17;">✅&nbsp; After — with asdev</th>
</tr>
<tr>
<td align="center"><strong>Acceptance</strong></td>
<td style="background:#1c1012;color:#fca5a5;">Main agent writes code, checks it itself, says "looks fine, completed"</td>
<td style="background:#0a1f17;color:#86efac;">Independent Task Acceptance Agent verifies each criterion using command output, test results, and search evidence</td>
</tr>
<tr>
<td align="center"><strong>Risk control</strong></td>
<td style="background:#1c1012;color:#fca5a5;">Complex requirement → code immediately → massive rollback on failure</td>
<td style="background:#0a1f17;color:#86efac;">Investigate → design → decompose → implement task-by-task, one big risk becomes many correctable small risks</td>
</tr>
<tr>
<td align="center"><strong>Transparency</strong></td>
<td style="background:#1c1012;color:#fca5a5;">The faster the loop, the less you understand — eventually "trust" or "give up"</td>
<td style="background:#0a1f17;color:#86efac;">4-layer comprehension guard: change summary → inference verification → pre-implementation confirmation → density warning</td>
</tr>
<tr>
<td align="center"><strong>Memory</strong></td>
<td style="background:#1c1012;color:#fca5a5;">Every session starts from zero, re-discovering known facts</td>
<td style="background:#0a1f17;color:#86efac;">.record/ persistence + .knowledge/ items + STATUS.md aggregated view, new goals inherit prior experience</td>
</tr>
<tr>
<td align="center"><strong>Criteria</strong></td>
<td style="background:#1c1012;color:#fca5a5;">"Looks fine" / "Should work" / "Logically correct"</td>
<td style="background:#0a1f17;color:#86efac;">Each task has objective acceptance criteria; acceptance agent uses evidence, rejects "looks like" judgments</td>
</tr>
<tr>
<td align="center"><strong>Iteration</strong></td>
<td style="background:#1c1012;color:#fca5a5;">Acceptance fails → manual patching with no closed loop, or skip and mark "confirmed"</td>
<td style="background:#0a1f17;color:#86efac;">FAIL → rework per feedback → resubmit → until PASS. No skip, no downgrade, no bypass.</td>
</tr>
</table>

---

## Three Iron Rules: No Bypass, No Downgrade

<table>
<tr>
<td width="33%" style="background:#102A2F;border-left:4px solid #FDE68A;padding:20px;vertical-align:top;">
<h3 style="color:#F8FAFC;margin-top:0;">Mandatory Recording</h3>
<p style="color:#FDE68A;font-size:15px;font-weight:700;margin:-8px 0 12px;">No save, no advance</p>
<p style="color:#D1FAE5;font-size:14px;">Every agent output must be written to <code>.record/</code>. If output is not persisted, the next phase must not start. Save failure → stop and report. Skipping is not allowed.</p>
<p><code style="background:#D9F99D;color:#0F172A;padding:2px 8px;border-radius:4px;font-size:12px;">Phase Gate</code></p>
</td>
<td width="33%" style="background:#102A2F;border-left:4px solid #FDE68A;padding:20px;vertical-align:top;">
<h3 style="color:#F8FAFC;margin-top:0;">Mandatory Acceptance</h3>
<p style="color:#FDE68A;font-size:15px;font-weight:700;margin:-8px 0 12px;">No PASS, no completion</p>
<p style="color:#D1FAE5;font-size:14px;">Design documents, task decomposition, every task implementation — all must be reviewed by an independent acceptance agent returning PASS. Main agent self-review does not count.</p>
<p><code style="background:#D9F99D;color:#0F172A;padding:2px 8px;border-radius:4px;font-size:12px;">Independent Review</code></p>
</td>
<td width="33%" style="background:#102A2F;border-left:4px solid #FDE68A;padding:20px;vertical-align:top;">
<h3 style="color:#F8FAFC;margin-top:0;">Mandatory Rework</h3>
<p style="color:#FDE68A;font-size:15px;font-weight:700;margin:-8px 0 12px;">No skip · No downgrade · No bypass</p>
<p style="color:#D1FAE5;font-size:14px;">On FAIL, revise per acceptance feedback and resubmit. Loop until PASS. "User confirmation" cannot substitute for acceptance. No acceptance step may be skipped.</p>
<p><code style="background:#D9F99D;color:#0F172A;padding:2px 8px;border-radius:4px;font-size:12px;">Mandatory Rework</code></p>
</td>
</tr>
</table>

> **Iron Rule Enforcement Checkpoint**: After each output is saved, the main agent must verify the file exists before advancing. Checkpoint not passed = step not completed. The only exception: user explicitly terminates the task — record the reason, set status to `Blocked`.

---

## Four-Phase Delivery: From Code Facts to Verifiable Delivery

<p align="center">
  <img src="assets/workflow.svg" alt="asdev four-phase workflow" width="880" />
</p>

<table>
<tr>
<td width="25%" style="background:#102A2F;border-top:3px solid #7DD3FC;padding:16px;vertical-align:top;">
<code style="background:#7DD3FC;color:#0F172A;padding:2px 8px;border-radius:4px;font-size:12px;">Phase 0</code>
<h4 style="color:#F8FAFC;margin:8px 0 4px;">Bootstrap</h4>
<p style="color:#D1FAE5;font-size:13px;">Confirm multi-agent capability<br/>Read project rules<br/>Init .record/ + STATUS.md</p>
</td>
<td width="25%" style="background:#102A2F;border-top:3px solid #34D399;padding:16px;vertical-align:top;">
<code style="background:#34D399;color:#0F172A;padding:2px 8px;border-radius:4px;font-size:12px;">Phase 1</code>
<h4 style="color:#F8FAFC;margin:8px 0 4px;">Investigation</h4>
<p style="color:#D1FAE5;font-size:13px;">Independent agent finds code facts & call chains<br/>Align uncertainties with user<br/>Design acceptance</p>
</td>
<td width="25%" style="background:#102A2F;border-top:3px solid #A7F3D0;padding:16px;vertical-align:top;">
<code style="background:#A7F3D0;color:#0F172A;padding:2px 8px;border-radius:4px;font-size:12px;">Phase 2</code>
<h4 style="color:#F8FAFC;margin:8px 0 4px;">Decomposition</h4>
<p style="color:#D1FAE5;font-size:13px;">Independent agent decomposes design into ordered tasks<br/>Each task has reason, goal, objective acceptance criteria<br/>Pause for user confirmation</p>
</td>
<td width="25%" style="background:#102A2F;border-top:3px solid #FDE68A;padding:16px;vertical-align:top;">
<code style="background:#FDE68A;color:#0F172A;padding:2px 8px;border-radius:4px;font-size:12px;">Phase 3</code>
<h4 style="color:#F8FAFC;margin:8px 0 4px;">Implementation</h4>
<p style="color:#D1FAE5;font-size:13px;">Implement task by task<br/>Independent acceptance agent verifies each<br/>FAIL → mandatory rework until PASS</p>
</td>
</tr>
</table>

---

## 9 Independent Agents: The Maker Doesn't Grade Its Own Homework

<p align="center">
  <img src="assets/agents.svg" alt="asdev multi-agent team" width="880" />
</p>

<table>
<tr>
<th width="50%" style="background:#102A2F;border-top:3px solid #7DD3FC;padding:12px;">
<code style="background:#7DD3FC;color:#0F172A;padding:2px 8px;border-radius:4px;font-size:12px;">Execution Roles — Standard Tier</code>
</th>
<th width="50%" style="background:#102A2F;border-top:3px solid #FDE68A;padding:12px;">
<code style="background:#FDE68A;color:#0F172A;padding:2px 8px;border-radius:4px;font-size:12px;">Review Roles — High Tier (Opus recommended)</code>
</th>
</tr>
<tr>
<td style="background:#102A2F;padding:16px;vertical-align:top;color:#D1FAE5;font-size:14px;">
<strong style="color:#F8FAFC;">Investigator</strong><br/>
Discover code facts, call chains, impact scope<br/><br/>
<strong style="color:#F8FAFC;">Product / Design</strong><br/>
Requirement exploration, design, risk strategy<br/><br/>
<strong style="color:#F8FAFC;">Development Manager</strong><br/>
Task decomposition, dependency order, acceptance criteria<br/><br/>
<strong style="color:#F8FAFC;">Implementation</strong><br/>
Single-task implementation, testing, change notes
</td>
<td style="background:#102A2F;padding:16px;vertical-align:top;color:#D1FAE5;font-size:14px;">
<strong style="color:#F8FAFC;">Design Acceptance</strong><br/>
Completeness, feasibility, consistency review<br/><br/>
<strong style="color:#F8FAFC;">Task Check</strong><br/>
Task granularity, dependency order, objective criteria<br/><br/>
<strong style="color:#F8FAFC;">Task Acceptance</strong><br/>
Item-by-item verification, evidence check, rework guidance<br/><br/>
<strong style="color:#F8FAFC;">Goal Check</strong><br/>
Evaluate whether stop condition is met
</td>
</tr>
</table>

> Review roles should use the platform's highest-reasoning model (e.g. Opus) to further reduce shared cognitive bias with execution roles. When per-role model selection is unavailable, fall back to prompt-level reasoning effort instructions.

---

## 4-Layer Comprehension Debt Guard: From Passive Asking to Active Inference Verification

> A loop that ships code faster than the user can understand it isn't efficient — it's erosion.

<table>
<tr>
<td width="60" align="center" style="background:#7DD3FC;color:#0F172A;font-weight:900;font-size:20px;border-radius:8px;">L1</td>
<td style="background:#102A2F;padding:16px;">
<strong style="color:#F8FAFC;">Per-Task Change Summary</strong><br/>
<span style="color:#7DD3FC;font-size:13px;">Trigger: after each task acceptance PASS</span><br/>
<p style="color:#D1FAE5;font-size:14px;">Show changed files, behavior changes, manual verification hints. Written to acceptance report AND shown directly to the user — you're never cut out of the loop.</p>
</td>
</tr>
<tr>
<td width="60" align="center" style="background:#34D399;color:#0F172A;font-weight:900;font-size:20px;border-radius:8px;">L2</td>
<td style="background:#102A2F;padding:16px;">
<strong style="color:#F8FAFC;">Inference Verification (every 3 tasks)</strong><br/>
<span style="color:#34D399;font-size:13px;">Trigger: every 3 completed tasks</span><br/>
<p style="color:#D1FAE5;font-size:14px;">Not "do you understand?" — instead, present concrete inferences for you to judge. Saying "this inference is wrong" has a much lower psychological barrier than admitting "I don't understand."</p>
<blockquote style="background:#0F172A;border-left:3px solid #34D399;padding:12px;border-radius:4px;color:#D1FAE5;font-size:13px;">
[Change T01] modified [file/module], effect is [behavior change]<br/>
→ Does this mean [concrete inference A]? (yes/no)
</blockquote>
</td>
</tr>
<tr>
<td width="60" align="center" style="background:#A7F3D0;color:#0F172A;font-weight:900;font-size:20px;border-radius:8px;">L3</td>
<td style="background:#102A2F;padding:16px;">
<strong style="color:#F8FAFC;">Pre-Implementation Confirmation</strong><br/>
<span style="color:#A7F3D0;font-size:13px;">Trigger: before each task implementation</span><br/>
<p style="color:#D1FAE5;font-size:14px;">Present implementation intent (task description, files involved, expected behavior change, files NOT involved). Implementation detail adjustments allowed; acceptance criteria changes must re-trigger Task Check. Full-auto mode may skip this layer.</p>
</td>
</tr>
<tr>
<td width="60" align="center" style="background:#FDE68A;color:#0F172A;font-weight:900;font-size:20px;border-radius:8px;">L4</td>
<td style="background:#102A2F;padding:16px;">
<strong style="color:#F8FAFC;">Change Density Warning</strong><br/>
<span style="color:#FDE68A;font-size:13px;">Trigger: same file/module modified in 3 consecutive tasks</span><br/>
<p style="color:#D1FAE5;font-size:14px;">Pause and warn: do you still understand the current state of this file/module? Applies in <strong style="color:#FDE68A;">both interactive and full-auto modes</strong> — cannot be skipped.</p>
</td>
</tr>
</table>

---

## Loop Mode: Unattended Auto-Iteration + Breakpoint Recovery

<table>
<tr>
<td width="50%" style="background:#102A2F;border-top:3px solid #7DD3FC;padding:20px;vertical-align:top;">
<h4 style="color:#F8FAFC;margin-top:0;">🖱️ Interactive Mode (default)</h4>
<p style="color:#7DD3FC;font-size:13px;">Trigger: /asdev or /goal</p>
<ul style="color:#D1FAE5;font-size:14px;padding-left:20px;">
<li>May pause at each phase for confirmation</li>
<li>Layer 3 pre-implementation confirmation — enabled</li>
<li>Layer 2 inference verification — enabled</li>
<li>Stop: Goal Check PASS or user terminates</li>
<li>Convergence safeguard: 3 iterations without PASS → pause</li>
</ul>
</td>
<td width="50%" style="background:#102A2F;border-top:3px solid #FDE68A;padding:20px;vertical-align:top;">
<h4 style="color:#F8FAFC;margin-top:0;">🔄 Loop Mode</h4>
<p style="color:#FDE68A;font-size:13px;">Trigger: goal contains "loop mode" / "unattended" / "auto-iteration", or scheduled dispatch</p>
<ul style="color:#D1FAE5;font-size:14px;padding-left:20px;">
<li>Auto-iterate, pause only when convergence safeguard triggers</li>
<li>Layer 3 pre-implementation confirmation — <strong style="color:#FDE68A;">skipped</strong></li>
<li>Layer 2 inference verification — written to STATUS.md instead</li>
<li>Stop: Goal Check PASS / convergence safeguard / "stop loop"</li>
<li>Convergence safeguard: 2 iterations without PASS or 30+ changed files → downgrade to interactive</li>
</ul>
</td>
</tr>
</table>

**Breakpoint recovery**: When loop mode starts/restarts, read `.record/STATUS.md`. If an active goal exists, continue from the current phase. Otherwise, start from Phase 0.

**Scheduling integration**:

```text
Claude Code:  /loop 10m "/asdev [goal with loop mode keyword]"
Claude Code:  hooks / cron scheduled trigger
Codex:        Automations tab → project + prompt + cadence
Manual:       /asdev [goal] — STATUS.md ensures continuity
```

> A loop that cannot converge is a design problem, not a persistence problem.

---

## Record-First: Evidence Doesn't Stay Only in Chat

<p align="center">
  <img src="assets/records.svg" alt="asdev record artifact chain" width="880" />
</p>

Each goal gets its own isolated subdirectory — records from different goals never mix:

```text
.record/
├── STATUS.md                  ← aggregated state view, breakpoint recovery foundation
├── .knowledge/                 ← cross-goal shared knowledge items
│   └── KNOW_YYYYMMDD_*.md
├── {goal-slug}/                ← one per goal (e.g. payment-timeout)
│   ├── .goal/                  ← goal config & stop condition
│   ├── .prod/                  ← investigation, requirement exploration, design
│   ├── .task/                  ← task decomposition & acceptance criteria
│   └── .review/                ← checks, acceptance, verification reports
└── {another-goal}/             ← another goal, fully isolated
```

**STATUS.md Three-Layer Sync Guarantee**:

| Layer | Mechanism | Guarantee |
|-------|-----------|-----------|
| 1 | `scripts/sync-status.py` auto-generates from record files | Regardless of agent manual updates, the script can rebuild from source of truth |
| 2 | Claude Code PostToolUse Hook auto-syncs after every file change | Real-time guarantee; fast-exit when no changes (< 100ms) |
| 3 | Agent checkpoint constraints, manual update at 5 event points | Defense in depth when hooks are unavailable |

**Cross-Goal Memory**: New goal starts → read STATUS.md for aggregated view → scan .knowledge/ for project experience (with confidence levels and outdated markers) → pass historical context to Investigator Agent, avoiding re-discovery of known facts.

**Knowledge Item Extraction**:

- 🟢 **Task PASS**: implementation surfaced a non-obvious pattern
- 🟢 **Goal Check PASS**: overall experience has cross-goal reuse value
- 🟡 **FAIL → Rework → PASS**: rework reason reveals a hidden constraint (failures teach the most)

---

## When to Use asdev

<table>
<tr>
<td width="50%" style="background:#0a1f17;border-top:3px solid #34D399;padding:20px;vertical-align:top;">
<h4 style="color:#86efac;margin-top:0;">✅ Use when</h4>
<ul style="color:#D1FAE5;font-size:14px;padding-left:20px;">
<li>Requirement spans multiple modules, roles, or runtime boundaries</li>
<li>Need to find direct/indirect call sites, state flows, data flows, event flows</li>
<li>Need requirement exploration → task decomposition → incremental development</li>
<li>Need a check agent to review design or task plan before implementation</li>
<li>Need an acceptance agent to independently verify against criteria after completion</li>
<li>Need unattended auto-iteration until a verifiable condition is met</li>
</ul>
</td>
<td width="50%" style="background:#1c1012;border-top:3px solid #7F1D1D;padding:20px;vertical-align:top;">
<h4 style="color:#fca5a5;margin-top:0;">❌ Don't use for</h4>
<ul style="color:#D1FAE5;font-size:14px;padding-left:20px;">
<li>Simple one-line edits</li>
<li>General Q&A</li>
<li>Single-file explanations</li>
<li>Small tasks that don't need acceptance</li>
</ul>
</td>
</tr>
</table>

---

## Quick Start

**Prerequisites**: Claude Code or Codex environment + platform supports independent subagents (Agent tool / subagent tools) + Git

**Install**: give this one sentence to your Agent: `Install the asdev skill from https://github.com/welsione/asdev into the current environment's skills directory; use ~/.claude/skills/asdev for Claude Code or ~/.codex/skills/asdev for Codex, then remind me to restart or open a new session.`

**Usage examples**:

```text
/asdev Handle this goal:
After editing profile on mobile, avatar and nickname occasionally fail to sync to the personal page.
Investigate the frontend state flow, API calls, cache updates, and backend response chain first;
align any uncertain business rules with me, then produce requirement exploration and task decomposition.
```

```text
/asdev loop mode:
Migrate the legacy order status field to the new state machine model while keeping API, background tasks, and reports compatible.
Stop condition: all test/order-related tests pass and lint has no new warnings.
```

---

## Design Philosophy

<table>
<tr>
<td width="33%" style="background:#102A2F;border-left:4px solid #7DD3FC;padding:20px;vertical-align:top;">
<h4 style="color:#F8FAFC;margin-top:0;">🔍 Investigation Before Design</h4>
<p style="color:#D1FAE5;font-size:14px;">AI coding fails not because it can't write code, but because it starts writing too soon. asdev mandates finding code facts, call chains, boundary entry points, and existing patterns before touching the design.</p>
</td>
<td width="33%" style="background:#102A2F;border-left:4px solid #34D399;padding:20px;vertical-align:top;">
<h4 style="color:#F8FAFC;margin-top:0;">⚖️ The Maker Doesn't Grade Its Own Homework</h4>
<p style="color:#D1FAE5;font-size:14px;">Single-agent self-review is AI coding's biggest systemic risk. 9 independent agent roles separate execution from review. Review roles use higher-reasoning models to further reduce shared cognitive bias.</p>
</td>
<td width="33%" style="background:#102A2F;border-left:4px solid #FDE68A;padding:20px;vertical-align:top;">
<h4 style="color:#F8FAFC;margin-top:0;">🧱 Big Risks → Small Correctable Risks</h4>
<p style="color:#D1FAE5;font-size:14px;">Tackling complex requirements in one shot means massive loss on failure. asdev breaks one big risk into a pipeline: investigate → design → decompose → implement task-by-task → independent acceptance. Every step has a checkpoint and a rework loop.</p>
</td>
</tr>
</table>

---

<p align="center">
  <strong style="font-size:20px;">asdev doesn't make agents start faster — it makes them deliver more reliably.</strong>
</p>

<p align="center">
  <code>Mandatory Recording</code> · <code>Mandatory Acceptance</code> · <code>Mandatory Rework on Rejection</code>
</p>
