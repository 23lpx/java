#!/usr/bin/env python3
"""对 Obsidian Vault 做只读完整性检查，不修改任何文件。"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEARNING_QUEUE = ROOT / "00-第一轮学习队列.md"
DAILY_REVIEW_TEMPLATE = ROOT / "00-每日学习与闭卷考核模板.md"
SECOND_ROUND_REVIEW_TEMPLATE = ROOT / "00-第二轮诊断与复习模板.md"
MOCK_INTERVIEW_TEMPLATE = ROOT / "00-模拟面试记录模板.md"
PROJECT_EVIDENCE_TEMPLATE = ROOT / "00-项目证据卡模板.md"
FOLLOWUP_TRAINING_TEMPLATE = ROOT / "00-追问链训练模板.md"
RESUME_EVIDENCE_DOCS = {
    ROOT / "00-简历证据与追问地图.md",
    ROOT / "00-苍穹外卖项目证据卡.md",
    PROJECT_EVIDENCE_TEMPLATE,
}
EXCLUDED_PARTS = {".git", ".github", ".obsidian", ".idea", ".claude"}
REQUIRED_FIELDS = {"category", "priority", "status", "tags"}
VALID_PRIORITIES = {"P0", "P1", "P2"}
VALID_STATUSES = {"未学习", "看过", "能回答", "需复习"}

QUESTION_RE = re.compile(r"^##\s+(\d+)\.\s+(.+?)\s*$", re.MULTILINE)
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.MULTILINE)
WIKILINK_RE = re.compile(r"!?\[\[([^\]]+)\]\]")
FIELD_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):", re.MULTILINE)
DAILY_REVIEW_HEADINGS = {
    "今日计划",
    "白天学习记录",
    "晚间闭卷考核",
    "错题复盘",
    "学习状态变更",
    "当日结果",
    "明日行动",
}
SECOND_ROUND_REVIEW_HEADINGS = {
    "六线输入",
    "白天断点修复",
    "场景复盘",
    "算法与手写",
    "晚间闭卷考核",
    "项目真实性检查",
    "学习状态变更",
    "队列更新",
}
MOCK_INTERVIEW_HEADINGS = {
    "面试信息",
    "面试前",
    "六线面试记录",
    "单题证据",
    "项目真实性检查",
    "算法与手写",
    "面试后复盘",
    "第二轮队列回流",
    "状态变更",
    "下一次面试",
}
PROJECT_EVIDENCE_HEADINGS = {
    "证据元数据",
    "简历主张",
    "知识链",
    "60 秒回答骨架",
    "追问树",
    "证据清单",
    "真实性边界",
    "复测记录",
}
FOLLOWUP_TRAINING_HEADINGS = {
    "训练信息",
    "母题入口",
    "30 秒核心回答",
    "60 秒机制与边界",
    "120 秒场景闭环",
    "连续追问记录",
    "错误断点",
    "六线结果",
    "第二轮回流",
    "复测",
}
PRIVATE_CONTACT_RE = re.compile(
    r"(?:1[3-9]\d{9}|[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,})",
    re.IGNORECASE,
)


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def markdown_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.md")
        if not any(part in EXCLUDED_PARTS for part in path.relative_to(ROOT).parts)
    )


def is_knowledge_note(path: Path) -> bool:
    parts = path.relative_to(ROOT).parts
    return len(parts) > 1 and re.fullmatch(r"\d{2}-.+", parts[0]) is not None


def split_frontmatter(text: str) -> tuple[str | None, str]:
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, text
    return text[4:end], text[end + 5 :]


def remove_code_examples(text: str) -> str:
    """移除代码示例，避免把示例中的 Wikilink 当成真实链接。"""
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)


def frontmatter_value(frontmatter: str, key: str) -> str | None:
    match = re.search(rf"^{re.escape(key)}:\s*(.*?)\s*$", frontmatter, re.MULTILINE)
    return match.group(1) if match else None


def resolve_note(
    source: Path,
    target: str,
    notes_by_stem: dict[str, list[Path]],
) -> tuple[Path | None, str | None]:
    cleaned = target.strip().replace("\\", "/")
    if not cleaned:
        return source, None

    target_path = Path(cleaned)
    if target_path.suffix != ".md":
        target_path = target_path.with_suffix(".md")

    candidates = [ROOT / target_path, source.parent / target_path]
    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve(), None

    matches = notes_by_stem.get(Path(cleaned).stem, [])
    if len(matches) == 1:
        return matches[0], None
    if len(matches) > 1:
        return None, f"目标文件名不唯一：{cleaned}"
    return None, f"目标文件不存在：{cleaned}"


def main() -> int:
    errors: list[str] = []
    files = markdown_files()
    texts: dict[Path, str] = {}
    headings: dict[Path, set[str]] = {}
    notes_by_stem: dict[str, list[Path]] = defaultdict(list)

    for path in files:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            errors.append(f"{relative(path)}：不是有效的 UTF-8 文件（{exc}）")
            continue
        texts[path.resolve()] = text
        headings[path.resolve()] = {value.strip() for value in HEADING_RE.findall(text)}
        notes_by_stem[path.stem].append(path.resolve())

    question_ids: dict[int, list[tuple[Path, str]]] = defaultdict(list)
    question_count = 0

    for path, text in texts.items():
        frontmatter, _ = split_frontmatter(text)
        if is_knowledge_note(path):
            if frontmatter is None:
                errors.append(f"{relative(path)}：缺少或未闭合 YAML Frontmatter")
            else:
                fields = set(FIELD_RE.findall(frontmatter))
                missing = sorted(REQUIRED_FIELDS - fields)
                if missing:
                    errors.append(f"{relative(path)}：缺少 Frontmatter 字段 {', '.join(missing)}")

                priority = frontmatter_value(frontmatter, "priority")
                if priority not in VALID_PRIORITIES:
                    errors.append(f"{relative(path)}：priority 值无效：{priority!r}")

                status = frontmatter_value(frontmatter, "status")
                if status not in VALID_STATUSES:
                    errors.append(f"{relative(path)}：status 值无效：{status!r}")

        for number, title in QUESTION_RE.findall(text):
            question_count += 1
            question_ids[int(number)].append((path, title))

        for raw_link in WIKILINK_RE.findall(remove_code_examples(text)):
            link = raw_link.split("|", 1)[0].strip()
            target_text, separator, heading = link.partition("#")
            target_path, error = resolve_note(path, target_text, notes_by_stem)
            if error:
                errors.append(f"{relative(path)}：Wikilink `{raw_link}` {error}")
                continue
            if separator and heading.strip() and target_path is not None:
                target_headings = headings.get(target_path.resolve(), set())
                if heading.strip() not in target_headings:
                    errors.append(
                        f"{relative(path)}：Wikilink `{raw_link}` 的标题锚点不存在"
                    )

    for number, locations in sorted(question_ids.items()):
        if len(locations) > 1:
            detail = "; ".join(
                f"{relative(path)} -> {title}" for path, title in locations
            )
            errors.append(f"题号 {number} 重复：{detail}")

    queue_path = LEARNING_QUEUE.resolve()
    queue_notes: list[Path] = []
    if queue_path not in texts:
        errors.append(f"{relative(LEARNING_QUEUE)}：第一轮学习队列不存在")
    else:
        for raw_link in WIKILINK_RE.findall(remove_code_examples(texts[queue_path])):
            link = raw_link.split("|", 1)[0].strip()
            target_text = link.partition("#")[0]
            target_path, error = resolve_note(
                LEARNING_QUEUE, target_text, notes_by_stem
            )
            if error is None and target_path is not None and is_knowledge_note(target_path):
                queue_notes.append(target_path.resolve())

        knowledge_notes = {path for path in texts if is_knowledge_note(path)}
        queued_note_set = set(queue_notes)
        for path in sorted(knowledge_notes - queued_note_set):
            errors.append(f"{relative(path)}：未加入第一轮学习队列")
        for path in sorted(queued_note_set - knowledge_notes):
            errors.append(f"{relative(path)}：不是有效的知识笔记")

        queue_counts: dict[Path, int] = defaultdict(int)
        for path in queue_notes:
            queue_counts[path] += 1
        for path, count in sorted(queue_counts.items()):
            if count > 1:
                errors.append(
                    f"{relative(path)}：在第一轮学习队列中重复 {count} 次"
                )

    required_templates = {
        DAILY_REVIEW_TEMPLATE: DAILY_REVIEW_HEADINGS,
        SECOND_ROUND_REVIEW_TEMPLATE: SECOND_ROUND_REVIEW_HEADINGS,
        MOCK_INTERVIEW_TEMPLATE: MOCK_INTERVIEW_HEADINGS,
        PROJECT_EVIDENCE_TEMPLATE: PROJECT_EVIDENCE_HEADINGS,
        FOLLOWUP_TRAINING_TEMPLATE: FOLLOWUP_TRAINING_HEADINGS,
    }
    for template_path, required_headings in required_templates.items():
        resolved_path = template_path.resolve()
        if resolved_path not in texts:
            errors.append(f"{relative(template_path)}：模板不存在")
            continue
        missing_headings = sorted(required_headings - headings[resolved_path])
        if missing_headings:
            errors.append(
                f"{relative(template_path)}：缺少模板标题 "
                f"{', '.join(missing_headings)}"
            )

    for evidence_path in RESUME_EVIDENCE_DOCS:
        resolved_path = evidence_path.resolve()
        if resolved_path not in texts:
            errors.append(f"{relative(evidence_path)}：简历证据文件不存在")
            continue
        if PRIVATE_CONTACT_RE.search(texts[resolved_path]):
            errors.append(
                f"{relative(evidence_path)}：不得保存手机号或邮箱等私人联系方式"
            )

    if errors:
        print(f"Obsidian Vault 检查失败：{len(errors)} 个问题", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "Obsidian Vault 检查通过："
        f"{len(files)} 个 Markdown 文件，{question_count} 道编号题，"
        f"{sum(len(WIKILINK_RE.findall(remove_code_examples(text))) for text in texts.values())} 个 Wikilink，"
        f"学习队列覆盖 {len(queue_notes)} 个知识节点。"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
