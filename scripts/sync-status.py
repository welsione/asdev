#!/usr/bin/env python3
"""
sync-status.py — Auto-generate STATUS.md from .record/ directory

This is the root-solution layer of the asdev Skill STATUS.md auto-sync mechanism.
Regardless of whether the agent manually updates STATUS.md, this script can rebuild
STATUS.md from record files (source of truth).

Usage:
    python3 scripts/sync-status.py          # Standard: generate and write .record/STATUS.md
    python3 scripts/sync-status.py --quiet  # Quiet: no stdout output, for hook calls
    python3 scripts/sync-status.py --dry-run # Output to stdout, do not write file
    python3 scripts/sync-status.py --check  # Consistency check: warn to stderr on mismatch

Design principles (following official Skill authoring best practices):
- Scripts solve problems, not delegate to Claude (provide specific info on errors and continue)
- Paths always use forward slashes (pathlib.Path cross-platform compatibility)
- No "magic constants" (all thresholds have comments explaining rationale)
- Fault-tolerance first (don't crash on missing or malformed frontmatter)
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


# ============================================================================
# Constants — All constants have comments explaining rationale (best practice: no magic constants)
# ============================================================================

# .record/ root directory relative to current working directory
RECORD_ROOT = Path(".record")

# STATUS.md path under .record/
STATUS_FILE = RECORD_ROOT / "STATUS.md"

# Show at most 5 knowledge highlights to keep STATUS.md concise
# 5 is enough to cover recent key knowledge; more available via .knowledge/ directory
MAX_KNOWLEDGE_ITEMS = 5

# At most 10 historical goals, consistent with cross-phase.md definition
MAX_HISTORY_GOALS = 10

# At most 10 recent change entries
MAX_RECENT_CHANGES = 10

# STATUS.md is considered "just changed" within 2 seconds after .record/ file changes
# 2 seconds covers most file write scenarios while avoiding false positives
# Used for PostToolUse hook fast-exit optimization
RECENT_CHANGE_THRESHOLD_SECONDS = 2


# ============================================================================
# Frontmatter Parsing — Fault-tolerance first, return empty dict on missing/malformed
# ============================================================================

FRONTMATTER_PATTERN = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_frontmatter(filepath: Path) -> dict[str, str]:
    """
    Parse YAML frontmatter from a Markdown file.

    Fault-tolerance:
    - File does not exist or cannot be read → return empty dict
    - Frontmatter missing → return empty dict
    - Frontmatter malformed → return empty dict
    - Field value missing → skip that field

    Returns:
        dict[str, str]: frontmatter field dictionary
    """
    if not filepath.exists():
        return {}

    try:
        content = filepath.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return {}

    match = FRONTMATTER_PATTERN.match(content)
    if not match:
        return {}

    result: dict[str, str] = {}
    for line in match.group(1).splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        # Strip optional quotes
        if (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            value = value[1:-1]
        if key:
            result[key] = value

    return result


# ============================================================================
# .record/ Directory Scanning
# ============================================================================


def is_goal_dir(path: Path) -> bool:
    """
    Determine if a path is a goal subdirectory (contains .goal/ subdirectory).

    Per cross-phase.md record structure definition:
    .record/{slug}/ contains .goal/, .prod/, .task/, .review/ subdirectories
    """
    if not path.is_dir():
        return False
    return (path / ".goal").is_dir()


def scan_goal_dirs(record_root: Path) -> list[Path]:
    """
    Scan all goal subdirectories.

    Skips .knowledge/ and other non-goal directories.
    """
    if not record_root.exists():
        return []
    return sorted(
        p for p in record_root.iterdir()
        if is_goal_dir(p)
    )


def get_recent_mtime(record_root: Path) -> float:
    """
    Get the most recent file modification time under .record/.

    Used for hook fast-exit optimization: if no file changed in the last N seconds,
    there's no need to regenerate STATUS.md.
    """
    if not record_root.exists():
        return 0.0

    max_mtime = 0.0
    try:
        for path in record_root.rglob("*"):
            if path.is_file():
                try:
                    mtime = path.stat().st_mtime
                    if mtime > max_mtime:
                        max_mtime = mtime
                except OSError:
                    continue
    except OSError:
        pass

    return max_mtime


# ============================================================================
# Goal Data Extraction
# ============================================================================


def extract_goal_data(goal_dir: Path) -> dict[str, Any] | None:
    """
    Extract data from a single goal directory.

    Returns:
        dict or None: returns None if directory structure is incomplete
    """
    slug = goal_dir.name

    # Read GOAL_CONFIG.md if it exists
    goal_config_path = goal_dir / ".goal" / "GOAL_CONFIG.md"
    goal_config = parse_frontmatter(goal_config_path)

    # Extract task progress
    task_progress = extract_task_progress(goal_dir)

    # Infer current phase
    current_phase = infer_phase(goal_dir)

    # Extract recent changes
    recent_changes = extract_recent_changes(goal_dir)

    return {
        "slug": slug,
        "name": goal_config.get("name", slug),
        "stop_condition": goal_config.get("stop_condition", ""),
        "status": goal_config.get("status", "In Progress"),
        "iteration": goal_config.get("iteration", "R1"),
        "current_phase": current_phase,
        "task_progress": task_progress,
        "recent_changes": recent_changes,
    }


def extract_task_progress(goal_dir: Path) -> list[dict[str, str]]:
    """
    Extract task progress table.

    Reads task status from .task/TXX_*.md.
    Reads acceptance results from .review/TASK_TXX_ACCEPTANCE_*.md.
    """
    task_dir = goal_dir / ".task"
    review_dir = goal_dir / ".review"

    tasks: list[dict[str, str]] = []
    if not task_dir.exists():
        return tasks

    # Collect task files (TXX_*.md, excluding TASK_PLAN_*.md)
    task_files = sorted(
        f for f in task_dir.glob("T*_*.md")
        if not f.name.startswith("TASK_PLAN_")
    )

    for task_file in task_files:
        fm = parse_frontmatter(task_file)

        # Task ID extraction: T01, T02, T10, etc.
        task_id_match = re.match(r"^(T\d+)", task_file.name)
        task_id = task_id_match.group(1) if task_id_match else task_file.stem

        # Task name
        task_name = fm.get("name", task_file.stem)

        # Task status
        status = fm.get("status", "Not Started")

        # Find corresponding acceptance report
        acceptance_status = "—"
        acceptance_report = "—"
        if review_dir.exists():
            acceptance_files = list(review_dir.glob(f"TASK_{task_id}_ACCEPTANCE_*.md"))
            if acceptance_files:
                acceptance_file = acceptance_files[0]
                acceptance_fm = parse_frontmatter(acceptance_file)
                acceptance_status = acceptance_fm.get("status", "—")
                rel_path = acceptance_file.relative_to(Path(".record"))
                acceptance_report = f".record/{rel_path.as_posix()}"

        tasks.append({
            "task_id": task_id,
            "task_name": task_name,
            "status": status,
            "acceptance_status": acceptance_status,
            "acceptance_report": acceptance_report,
        })

    return tasks


def infer_phase(goal_dir: Path) -> str:
    """
    Infer the goal's current phase.

    Inference logic (based on file existence):
    - Only .goal/ → Phase 0 (Bootstrap)
    - Has .prod/ but no .task/ → Phase 1 (Investigation)
    - Has .task/TASK_PLAN but no ACCEPTANCE → Phase 2 (Planning)
    - Has .task/TXX + .review/TASK_TXX_ACCEPTANCE → Phase 3 (Implementation)
    - All tasks status=Completed → Completion
    - Has .review/GOAL_CHECK → Goal Check
    """
    has_goal = (goal_dir / ".goal").exists()
    has_prod = (goal_dir / ".prod").exists()
    has_task = (goal_dir / ".task").exists()
    has_review = (goal_dir / ".review").exists()

    if not has_goal:
        return "Unknown"

    # Check task completion
    tasks = extract_task_progress(goal_dir)
    all_done = tasks and all(t["status"] == "Completed" for t in tasks)

    # Check Goal Check
    if has_review and list((goal_dir / ".review").glob("GOAL_CHECK_*.md")):
        return "Goal Check"

    if all_done and tasks:
        return "Completion"

    if has_review:
        review_files = list((goal_dir / ".review").glob("TASK_T*_ACCEPTANCE_*.md"))
        if review_files:
            return "Phase 3"

    if has_task:
        task_plan_files = list((goal_dir / ".task").glob("TASK_PLAN_*.md"))
        if task_plan_files:
            return "Phase 2"

    if has_prod:
        return "Phase 1"

    return "Phase 0"


def extract_recent_changes(goal_dir: Path) -> list[dict[str, str]]:
    """
    Extract recent change summary.

    Reads task acceptance reports from .review/, sorted by date, taking the most recent MAX_RECENT_CHANGES entries.
    """
    review_dir = goal_dir / ".review"
    if not review_dir.exists():
        return []

    changes: list[dict[str, str]] = []
    for review_file in sorted(review_dir.glob("TASK_T*_ACCEPTANCE_*.md"), reverse=True):
        fm = parse_frontmatter(review_file)
        if not fm:
            continue

        # Extract task ID
        task_id_match = re.match(r"TASK_(T\d+)_ACCEPTANCE", review_file.name)
        task_id = task_id_match.group(1) if task_id_match else "T??"

        date = fm.get("date", "")
        status = fm.get("status", "")
        summary = fm.get("summary", "")

        if date and status:
            changes.append({
                "date": date,
                "task_id": task_id,
                "status": status,
                "summary": summary,
            })

        if len(changes) >= MAX_RECENT_CHANGES:
            break

    return changes


# ============================================================================
# Knowledge Extraction
# ============================================================================


def extract_knowledge(record_root: Path) -> list[dict[str, str]]:
    """
    Extract the most recent MAX_KNOWLEDGE_ITEMS knowledge items.

    Reads from .record/.knowledge/KNOW_*.md.
    """
    knowledge_dir = record_root / ".knowledge"
    if not knowledge_dir.exists():
        return []

    items: list[dict[str, str]] = []
    for know_file in sorted(knowledge_dir.glob("KNOW_*.md"), reverse=True):
        fm = parse_frontmatter(know_file)
        if not fm:
            continue

        items.append({
            "name": fm.get("name", know_file.stem),
            "topic": fm.get("topic", know_file.stem),
            "date": fm.get("date", ""),
            "confidence": fm.get("confidence", ""),
            "scope": fm.get("scope", ""),
            "status": fm.get("status", "active"),
        })

        if len(items) >= MAX_KNOWLEDGE_ITEMS:
            break

    return items


# ============================================================================
# Historical Goals Extraction
# ============================================================================


def extract_history_goals(goal_dirs: list[Path]) -> list[dict[str, str]]:
    """
    Extract completed historical goals.

    Criteria: all tasks status=Completed + has acceptance reports in .review/.
    """
    history: list[dict[str, str]] = []
    for goal_dir in goal_dirs:
        data = extract_goal_data(goal_dir)
        if not data:
            continue
        if data["current_phase"] in ("Completion", "Goal Check"):
            history.append({
                "slug": data["slug"],
                "name": data["name"],
                "status": data["status"],
                "stop_condition": data["stop_condition"],
            })

    return history[:MAX_HISTORY_GOALS]


# ============================================================================
# STATUS.md Generation
# ============================================================================


def generate_status(data: dict[str, Any]) -> str:
    """
    Generate content in STATUS.md template format.

    See cross-phase.md STATUS Template.
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    active_goals = [g for g in data["goals"] if g["current_phase"] not in ("Completion", "Goal Check")]
    completed_goals = [g for g in data["goals"] if g["current_phase"] in ("Completion", "Goal Check")]

    # Current phase from first active goal
    current_phase = active_goals[0]["current_phase"] if active_goals else "—"
    current_mode = "Loop" if "loop" in data.get("mode", "").lower() else "Interactive"

    lines: list[str] = [
        "# STATUS",
        "",
        f"> Last updated: {now}",
        f"> Current mode: {current_mode}",
        f"> Current phase: {current_phase}",
        "",
        "## Active Goals",
        "",
        "| Goal | Slug | Stop Condition | Iteration | Current Phase | Status |",
        "|------|------|----------------|-----------|---------------|--------|",
    ]

    if active_goals:
        for goal in active_goals:
            lines.append(
                f"| {goal['name']} | `{goal['slug']}` | {goal['stop_condition'] or '—'} "
                f"| {goal['iteration']} | {goal['current_phase']} | {goal['status']} |"
            )
    else:
        lines.append("| — | — | — | — | — | — |")

    # Task progress (from first active goal's tasks)
    lines.extend([
        "",
        "## Task Progress",
        "",
        "| Task | Status | Acceptance | Report |",
        "|------|--------|------------|--------|",
    ])

    if active_goals and active_goals[0]["task_progress"]:
        for task in active_goals[0]["task_progress"]:
            lines.append(
                f"| {task['task_id']} {task['task_name']} | {task['status']} "
                f"| {task['acceptance_status']} | {task['acceptance_report']} |"
            )
    else:
        lines.append("| — | — | — | — |")

    # Historical goals
    lines.extend([
        "",
        "## Historical Goals",
        "",
        "> At most 10 entries; older ones accessible via date index to specific files.",
        "",
        "| Goal | Slug | Completion Date | Final Result | Key Artifacts |",
        "|------|------|-----------------|--------------|---------------|",
    ])

    if completed_goals:
        for goal in completed_goals:
            lines.append(
                f"| {goal['name']} | `{goal['slug']}` | — | {goal['status']} | {goal['stop_condition'] or '—'} |"
            )
    else:
        lines.append("| — | — | — | — | — |")

    # Knowledge highlights
    lines.extend([
        "",
        "## Knowledge Highlights",
        "",
        "> Most recent 5 reusable knowledge item summaries.",
        "",
    ])

    if data["knowledge"]:
        for item in data["knowledge"]:
            status_marker = " ⚠️ Outdated" if item["status"] == "outdated" else ""
            lines.append(
                f"- **{item['name']}** ({item['date']}) — {item['scope']}{status_marker}"
            )
    else:
        lines.append("(No knowledge items yet; maintained by future goals)")

    # Available connectors
    lines.extend([
        "",
        "## Available Connectors",
        "",
        "> Available MCP tools discovered during Phase 0.",
        "",
        "(Maintained after Phase 0 implementation)",
    ])

    # Recent changes
    lines.extend([
        "",
        "## Recent Changes",
        "",
    ])

    all_changes: list[dict[str, str]] = []
    for goal in data["goals"]:
        all_changes.extend(goal["recent_changes"])
    # Sort by date descending
    all_changes.sort(key=lambda c: c["date"], reverse=True)

    if all_changes:
        for change in all_changes[:MAX_RECENT_CHANGES]:
            lines.append(
                f"- {change['date']} {change['task_id']} {change['summary'] or '(no summary)'} — {change['status']}"
            )
    else:
        lines.append("- (No change records yet)")

    lines.append("")
    return "\n".join(lines)


# ============================================================================
# Main
# ============================================================================


def collect_data(record_root: Path) -> dict[str, Any]:
    """Collect all required data."""
    goal_dirs = scan_goal_dirs(record_root)
    goals = []
    for goal_dir in goal_dirs:
        data = extract_goal_data(goal_dir)
        if data:
            goals.append(data)

    knowledge = extract_knowledge(record_root)

    return {
        "mode": "",
        "goals": goals,
        "knowledge": knowledge,
    }


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Auto-generate STATUS.md from .record/ directory"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Quiet mode: no stdout output, for hook calls",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Output to stdout, do not write file",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Consistency check: warn to stderr on mismatch",
    )
    args = parser.parse_args()

    # Fast-exit optimization: if no .record/ file changed in the last N seconds
    # and STATUS.md exists, no need to regenerate (avoids unnecessary hook calls)
    if args.quiet:
        if STATUS_FILE.exists():
            import time
            now = time.time()
            try:
                status_mtime = STATUS_FILE.stat().st_mtime
                record_mtime = get_recent_mtime(RECORD_ROOT)
                if record_mtime <= status_mtime and (now - status_mtime) > RECENT_CHANGE_THRESHOLD_SECONDS:
                    # No .record/ files newer than STATUS.md, and STATUS.md was not just generated
                    return 0
            except OSError:
                pass

    # Collect data
    data = collect_data(RECORD_ROOT)

    # Generate STATUS.md content
    content = generate_status(data)

    # --check mode: compare current STATUS.md with generated version
    if args.check:
        if not STATUS_FILE.exists():
            print(
                "WARNING: STATUS.md does not exist, run sync-status.py to generate",
                file=sys.stderr,
            )
            return 1
        try:
            current = STATUS_FILE.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as e:
            print(f"WARNING: Failed to read STATUS.md: {e}", file=sys.stderr)
            return 1
        if current != content:
            print(
                "WARNING: STATUS.md is out of sync with record files. "
                "Run python3 scripts/sync-status.py to sync",
                file=sys.stderr,
            )
            return 1
        return 0

    # --dry-run mode: output to stdout
    if args.dry_run:
        print(content)
        return 0

    # Standard mode: write STATUS.md
    try:
        STATUS_FILE.parent.mkdir(parents=True, exist_ok=True)
        STATUS_FILE.write_text(content, encoding="utf-8")
    except OSError as e:
        print(f"ERROR: Failed to write STATUS.md: {e}", file=sys.stderr)
        return 1

    if not args.quiet:
        print(f"Generated {STATUS_FILE}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
