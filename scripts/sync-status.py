#!/usr/bin/env python3
"""
sync-status.py — 从 .record/ 目录自动生成 STATUS.md

这是 asdev Skill STATUS.md 自动同步机制的根本解层。
无论 Agent 是否手动更新 STATUS.md，本脚本都能从 record files (source of truth) 重建 STATUS.md。

Usage:
    python3 scripts/sync-status.py          # 标准模式：生成并写入 .record/STATUS.md
    python3 scripts/sync-status.py --quiet  # 静默模式：hook 调用用，无 stdout 输出
    python3 scripts/sync-status.py --dry-run # 输出到 stdout，不写文件
    python3 scripts/sync-status.py --check  # 一致性检查：不一致时输出警告到 stderr

设计原则（遵循官方 Skill 编写最佳实践）：
- 脚本解决问题而非推卸给 Claude（错误时提供具体信息并继续处理）
- 路径始终使用正斜杠（pathlib.Path 跨平台兼容）
- 无"巫术常量"（所有阈值都有注释说明理由）
- 容错优先（frontmatter 缺失或格式错误时不崩溃）
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


# ============================================================================
# Constants — 所有常量都有注释说明理由（官方最佳实践：无"巫术常量"）
# ============================================================================

# .record/ 根目录相对于当前工作目录
RECORD_ROOT = Path(".record")

# STATUS.md 在 .record/ 下的路径
STATUS_FILE = RECORD_ROOT / "STATUS.md"

# 知识要点最多展示 5 条，保持 STATUS.md 简洁
# 5 条足以覆盖最近关键知识，更多可通过 .knowledge/ 目录查看
MAX_KNOWLEDGE_ITEMS = 5

# 历史目标最多 10 条，与 cross-phase.md 定义一致
MAX_HISTORY_GOALS = 10

# 最近变更摘要最多 10 条
MAX_RECENT_CHANGES = 10

# STATUS.md 在 .record/ 下文件变更后 2 秒内视为"刚变更"
# 2 秒覆盖了绝大多数文件写入场景，同时避免误判
# 用于 PostToolUse hook 的快速退出优化
RECENT_CHANGE_THRESHOLD_SECONDS = 2


# ============================================================================
# Frontmatter Parsing — 容错优先，缺失/格式错误时返回空 dict
# ============================================================================

FRONTMATTER_PATTERN = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_frontmatter(filepath: Path) -> dict[str, str]:
    """
    解析 Markdown 文件的 YAML frontmatter。

    容错处理：
    - 文件不存在或无法读取 → 返回空 dict
    - frontmatter 缺失 → 返回空 dict
    - frontmatter 格式错误 → 返回空 dict
    - 字段值缺失 → 跳过该字段

    Returns:
        dict[str, str]: frontmatter 字段字典
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
        # 去掉可选的引号
        if (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            value = value[1:-1]
        if key:
            result[key] = value

    return result


# ============================================================================
# .record/ 目录扫描
# ============================================================================


def is_goal_dir(path: Path) -> bool:
    """
    判断是否为 goal 子目录（含 .goal/ 子目录）。

    参考 cross-phase.md 的 record structure 定义：
    .record/{slug}/ 含 .goal/, .prod/, .task/, .review/ 子目录
    """
    if not path.is_dir():
        return False
    return (path / ".goal").is_dir()


def scan_goal_dirs(record_root: Path) -> list[Path]:
    """
    扫描所有 goal 子目录。

    跳过 .knowledge/ 和其他非 goal 目录。
    """
    if not record_root.exists():
        return []
    return sorted(
        p for p in record_root.iterdir()
        if is_goal_dir(p)
    )


def get_recent_mtime(record_root: Path) -> float:
    """
    获取 .record/ 下最近文件修改时间。

    用于 hook 快速退出优化：如果最近 N 秒内没有文件变更，无需重新生成 STATUS.md。
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
# Goal 数据提取
# ============================================================================


def extract_goal_data(goal_dir: Path) -> dict[str, Any] | None:
    """
    从单个 goal 目录提取数据。

    Returns:
        dict or None: 如果目录结构不完整则返回 None
    """
    slug = goal_dir.name

    # 读取 GOAL_CONFIG.md（如果存在）
    goal_config_path = goal_dir / ".goal" / "GOAL_CONFIG.md"
    goal_config = parse_frontmatter(goal_config_path)

    # 提取任务进度
    task_progress = extract_task_progress(goal_dir)

    # 推断当前阶段
    current_phase = infer_phase(goal_dir)

    # 提取最近变更
    recent_changes = extract_recent_changes(goal_dir)

    return {
        "slug": slug,
        "name": goal_config.get("name", slug),
        "stop_condition": goal_config.get("stop_condition", ""),
        "status": goal_config.get("status", "进行中"),
        "iteration": goal_config.get("iteration", "R1"),
        "current_phase": current_phase,
        "task_progress": task_progress,
        "recent_changes": recent_changes,
    }


def extract_task_progress(goal_dir: Path) -> list[dict[str, str]]:
    """
    提取任务进度表。

    从 .task/TXX_*.md 读取任务状态。
    从 .review/TASK_TXX_ACCEPTANCE_*.md 读取验收结果。
    """
    task_dir = goal_dir / ".task"
    review_dir = goal_dir / ".review"

    tasks: list[dict[str, str]] = []
    if not task_dir.exists():
        return tasks

    # 收集任务文件（TXX_*.md，排除 TASK_PLAN_*.md）
    task_files = sorted(
        f for f in task_dir.glob("T*_*.md")
        if not f.name.startswith("TASK_PLAN_")
    )

    for task_file in task_files:
        fm = parse_frontmatter(task_file)

        # 任务 ID 提取：T01, T02, T10 等
        task_id_match = re.match(r"^(T\d+)", task_file.name)
        task_id = task_id_match.group(1) if task_id_match else task_file.stem

        # 任务名称
        task_name = fm.get("name", task_file.stem)

        # 任务状态
        status = fm.get("status", "未开始")

        # 查找对应的验收报告
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
    推断 goal 的当前阶段。

    推断逻辑（基于文件存在性）：
    - 只有 .goal/ → Phase 0 (Bootstrap)
    - 有 .prod/ 但无 .task/ → Phase 1 (Investigation)
    - 有 .task/TASK_PLAN 但无 ACCEPTANCE → Phase 2 (Planning)
    - 有 .task/TXX + .review/TASK_TXX_ACCEPTANCE → Phase 3 (Implementation)
    - 所有任务 status=完成 → Completion
    - 有 .review/GOAL_CHECK → Goal Check
    """
    has_goal = (goal_dir / ".goal").exists()
    has_prod = (goal_dir / ".prod").exists()
    has_task = (goal_dir / ".task").exists()
    has_review = (goal_dir / ".review").exists()

    if not has_goal:
        return "Unknown"

    # 检查任务完成情况
    tasks = extract_task_progress(goal_dir)
    all_done = tasks and all(t["status"] == "完成" for t in tasks)

    # 检查 Goal Check
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
    提取最近变更摘要。

    从 .review/ 中读取任务验收报告，按日期排序取最近 MAX_RECENT_CHANGES 条。
    """
    review_dir = goal_dir / ".review"
    if not review_dir.exists():
        return []

    changes: list[dict[str, str]] = []
    for review_file in sorted(review_dir.glob("TASK_T*_ACCEPTANCE_*.md"), reverse=True):
        fm = parse_frontmatter(review_file)
        if not fm:
            continue

        # 提取任务 ID
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
# Knowledge 提取
# ============================================================================


def extract_knowledge(record_root: Path) -> list[dict[str, str]]:
    """
    提取最近 MAX_KNOWLEDGE_ITEMS 条知识条目。

    从 .record/.knowledge/KNOW_*.md 读取。
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
# 历史目标摘要提取
# ============================================================================


def extract_history_goals(goal_dirs: list[Path]) -> list[dict[str, str]]:
    """
    提取已完成的历史目标。

    判定：所有任务 status=完成 + 有 .review/ 中的验收报告。
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
# STATUS.md 生成
# ============================================================================


def generate_status(data: dict[str, Any]) -> str:
    """
    按 STATUS.md 模板格式生成内容。

    参考 cross-phase.md 中的 STATUS Template。
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    active_goals = [g for g in data["goals"] if g["current_phase"] not in ("Completion", "Goal Check")]
    completed_goals = [g for g in data["goals"] if g["current_phase"] in ("Completion", "Goal Check")]

    # 当前阶段取第一个活跃目标的阶段
    current_phase = active_goals[0]["current_phase"] if active_goals else "—"
    current_mode = "循环" if "loop" in data.get("mode", "").lower() else "交互"

    lines: list[str] = [
        "# STATUS",
        "",
        f"> 最后更新：{now}",
        f"> 当前模式：{current_mode}",
        f"> 当前阶段：{current_phase}",
        "",
        "## 活跃目标",
        "",
        "| 目标 | Slug | 停止条件 | 迭代轮次 | 当前阶段 | 状态 |",
        "|------|------|----------|----------|----------|------|",
    ]

    if active_goals:
        for goal in active_goals:
            lines.append(
                f"| {goal['name']} | `{goal['slug']}` | {goal['stop_condition'] or '—'} "
                f"| {goal['iteration']} | {goal['current_phase']} | {goal['status']} |"
            )
    else:
        lines.append("| — | — | — | — | — | — |")

    # 任务进度（取第一个活跃目标的任务）
    lines.extend([
        "",
        "## 任务进度",
        "",
        "| 任务 | 状态 | 验收结果 | 验收报告 |",
        "|------|------|----------|----------|",
    ])

    if active_goals and active_goals[0]["task_progress"]:
        for task in active_goals[0]["task_progress"]:
            lines.append(
                f"| {task['task_id']} {task['task_name']} | {task['status']} "
                f"| {task['acceptance_status']} | {task['acceptance_report']} |"
            )
    else:
        lines.append("| — | — | — | — |")

    # 历史目标摘要
    lines.extend([
        "",
        "## 历史目标摘要",
        "",
        "> 最多 10 条，更早的通过日期索引指向具体文件。",
        "",
        "| 目标 | Slug | 完成日期 | 最终结果 | 关键产出 |",
        "|------|------|----------|----------|----------|",
    ])

    if completed_goals:
        for goal in completed_goals:
            lines.append(
                f"| {goal['name']} | `{goal['slug']}` | — | {goal['status']} | {goal['stop_condition'] or '—'} |"
            )
    else:
        lines.append("| — | — | — | — | — |")

    # 知识要点
    lines.extend([
        "",
        "## 知识要点",
        "",
        "> 最近 5 条可复用知识条目摘要。",
        "",
    ])

    if data["knowledge"]:
        for item in data["knowledge"]:
            status_marker = " ⚠️ 已过时" if item["status"] == "outdated" else ""
            lines.append(
                f"- **{item['name']}** ({item['date']}) — {item['scope']}{status_marker}"
            )
    else:
        lines.append("（暂无知识条目，待后续目标维护）")

    # 可用连接器
    lines.extend([
        "",
        "## 可用连接器",
        "",
        "> Phase 0 连接器发现阶段记录的可用 MCP 工具。",
        "",
        "（待 Phase 0 实施后维护）",
    ])

    # 最近变更摘要
    lines.extend([
        "",
        "## 最近变更摘要",
        "",
    ])

    all_changes: list[dict[str, str]] = []
    for goal in data["goals"]:
        all_changes.extend(goal["recent_changes"])
    # 按日期降序排序
    all_changes.sort(key=lambda c: c["date"], reverse=True)

    if all_changes:
        for change in all_changes[:MAX_RECENT_CHANGES]:
            lines.append(
                f"- {change['date']} {change['task_id']} {change['summary'] or '（无摘要）'} — {change['status']}"
            )
    else:
        lines.append("- （暂无变更记录）")

    lines.append("")
    return "\n".join(lines)


# ============================================================================
# Main
# ============================================================================


def collect_data(record_root: Path) -> dict[str, Any]:
    """收集所有需要的数据。"""
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
    """主入口。"""
    parser = argparse.ArgumentParser(
        description="从 .record/ 目录自动生成 STATUS.md"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="静默模式：无 stdout 输出，hook 调用时使用",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="输出到 stdout，不写文件",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="一致性检查：不一致时输出警告到 stderr",
    )
    args = parser.parse_args()

    # 快速退出优化：如果最近 N 秒内没有 .record/ 文件变更，且 STATUS.md 存在，
    # 则无需重新生成（避免无意义的 hook 调用）
    if args.quiet:
        if STATUS_FILE.exists():
            import time
            now = time.time()
            try:
                status_mtime = STATUS_FILE.stat().st_mtime
                record_mtime = get_recent_mtime(RECORD_ROOT)
                if record_mtime <= status_mtime and (now - status_mtime) > RECENT_CHANGE_THRESHOLD_SECONDS:
                    # .record/ 没有比 STATUS.md 更新的文件，且 STATUS.md 不是刚刚生成
                    return 0
            except OSError:
                pass

    # 收集数据
    data = collect_data(RECORD_ROOT)

    # 生成 STATUS.md 内容
    content = generate_status(data)

    # --check 模式：比较当前 STATUS.md 与生成版本
    if args.check:
        if not STATUS_FILE.exists():
            print(
                f"WARNING: STATUS.md 不存在，需要运行 sync-status.py 生成",
                file=sys.stderr,
            )
            return 1
        try:
            current = STATUS_FILE.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as e:
            print(f"WARNING: 读取 STATUS.md 失败: {e}", file=sys.stderr)
            return 1
        if current != content:
            print(
                "WARNING: STATUS.md 与 record files 不一致，请运行 "
                "python3 scripts/sync-status.py 同步",
                file=sys.stderr,
            )
            return 1
        return 0

    # --dry-run 模式：输出到 stdout
    if args.dry_run:
        print(content)
        return 0

    # 标准模式：写入 STATUS.md
    try:
        STATUS_FILE.parent.mkdir(parents=True, exist_ok=True)
        STATUS_FILE.write_text(content, encoding="utf-8")
    except OSError as e:
        print(f"ERROR: 写入 STATUS.md 失败: {e}", file=sys.stderr)
        return 1

    if not args.quiet:
        print(f"已生成 {STATUS_FILE}")

    return 0


if __name__ == "__main__":
    sys.exit(main())