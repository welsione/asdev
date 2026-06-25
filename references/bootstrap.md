# First-Run Bootstrap And Capability Detection

Use this reference during Phase 0, before requirement exploration.

The goal of bootstrap is to make the project ready for repeatable goal-mode work without forcing heavyweight dependencies.

## Detect Project Context

Look for project-local guidance first:

- `CLAUDE.md`
- `AGENTS.md`
- `README.md`
- `docs/architecture/`
- `docs/`
- Existing `.record/`
- Existing task/review/design files
- Build files such as `pom.xml`, `package.json`, `build.gradle`, `Cargo.toml`, `pyproject.toml`

Read only the files needed to understand rules, architecture, and verification commands.

## Create Local Record Structure

If the workflow directories are missing and the workspace is writable, create:

```text
.record/
├── .goal/
├── .prod/
├── .task/
└── .review/
```

If the project already has a different record convention, follow the existing convention instead of forcing this one.

## Create Lightweight Templates

If missing, create project-local templates from `references/templates.md`:

- `.record/.prod/PROD_TEMPLATE.md`
- `.record/.task/TASK_TEMPLATE.md`
- `.record/.goal/GOAL_CONFIG_TEMPLATE.md`

Do not overwrite existing templates without user approval.

## Capability Detection

Detect tools and capabilities before relying on them:

- `rg`: primary text search tool.
- `git`: useful for status and diffs.
- Build/test command: infer from project files.
- `codegraph`: optional for call-chain and dependency graph exploration.
- Subagents or Task tool: required for independent role execution.
- Related skills such as `superpowers`: optional reasoning/review enhancement.

Use `references/multi-agent-contract.md` for the exact acceptance criteria for independent agent capability.

Record the useful findings in the product/design notes when they affect execution.

## Dependency Policy

Do not install external dependencies automatically.

If a useful optional tool is missing:

1. Continue with available tools when practical.
2. Mention the missing tool and the benefit it would provide.
3. Ask the user before installing or requiring it.

Examples:

- If `codegraph` is missing, use `rg`, static reading, compiler/test output, and local architecture docs.
- If `superpowers` is unavailable, use this skill's built-in planning and review flow.

If independent multi-agent capability is missing, stop. asdev requires real independent agents and must not continue as a single-agent self-review workflow.

## Suggested Goal Config

When useful, create a config like this:

```yaml
recordRoot: .record
prodDir: .record/.prod
taskDir: .record/.task
reviewDir: .record/.review
language: zh-CN
rulesFiles:
  - CLAUDE.md
testCommands: {}
recordNaming:
  investigation: INVESTIGATION_YYYYMMDD_HHMM.md
  product: PROD_YYYYMMDD_HHMM.md
  task: TASK_YYYYMMDD_HHMM.md
codeSearch:
  primary: rg
  optional:
    - codegraph
pauseAfterTaskPlanning: true
multiAgent:
  required: true
  contract: references/multi-agent-contract.md
prompts:
  index: references/agent-prompts.md
  assembly: references/prompt-assembly.md
optionalSkills:
  - superpowers
```

Keep the config descriptive. Do not make it a fragile source of truth unless the user asks for automation around it.
